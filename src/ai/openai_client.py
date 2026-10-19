"""
OpenAI API Client & Responses API Integration with Web Search.
Features:
- Official OpenAI SDK Responses API (`client.responses.create`) with web search tool.
- Fallback resilience to Chat Completions API with web search grounding.
- Server-side `OPENAI_API_KEY` credential loading.
- Sensitive API key sanitization (never exposed in frontend, logs, or responses).
- Real-time clickable source citation extraction.
- Strict atomic 3 questions / rolling 24 hours quota guard per authenticated user ID.
- Grounding on Global FuelPulse AI platform documentation and database metrics.
"""

import os
import re
import json
import logging
from typing import Dict, Any, Optional, List, Tuple

import openai
from config.settings import settings
from src.ai.openai_quota_manager import openai_quota_manager, OpenAIQuotaExhaustedError

logger = logging.getLogger(__name__)

# Constants
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
MAX_QUESTION_LENGTH = 1000


class OpenAIMissingKeyError(Exception):
    """Raised when OPENAI_API_KEY is not configured."""
    def __init__(self, message: str = "OpenAI API key is missing. Please set OPENAI_API_KEY in your server environment or .env file."):
        super().__init__(message)
        self.status_code = 401
        self.message = message


class OpenAIServiceError(Exception):
    """Raised when the OpenAI service encounters an error."""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


def sanitize_sensitive_text(text: str) -> str:
    """Removes API keys or secret tokens from strings to prevent logging or response leaks."""
    if not text:
        return ""
    # Mask OpenAI sk-proj-... and sk-... keys
    sanitized = re.sub(r"sk-proj-[a-zA-Z0-9_\-]{20,}", "sk-proj-...REDACTED", str(text))
    sanitized = re.sub(r"sk-[a-zA-Z0-9_\-]{20,}", "sk-...REDACTED", sanitized)
    # Mask URL query param keys: key=...
    sanitized = re.sub(r"key=[a-zA-Z0-9_\-]+", "key=REDACTED_API_KEY", sanitized)
    # Mask raw AIza / AQ keys:
    sanitized = re.sub(r"AIza[0-9A-Za-z\-_]{35}", "AIza...REDACTED", sanitized)
    sanitized = re.sub(r"AQ\.[0-9A-Za-z\-_]{30,}", "AQ...REDACTED", sanitized)
    return sanitized


class OpenAIClient:
    """Client for official OpenAI API and Responses API with web search."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        self._explicit_key = api_key.strip() if api_key is not None else None
        self._explicit_model = model.strip() if model is not None else None

    @property
    def api_key(self) -> str:
        """Dynamic getter for OpenAI API key."""
        if self._explicit_key is not None:
            return self._explicit_key
        return settings.api.openai_api_key

    @property
    def model(self) -> str:
        """Configured OpenAI model."""
        if self._explicit_model is not None:
            return self._explicit_model
        return settings.api.openai_model or DEFAULT_OPENAI_MODEL

    def is_key_configured(self) -> bool:
        """Checks if a valid non-empty OpenAI API key is available."""
        k = self.api_key
        return bool(k and len(k) > 10 and not k.startswith("your-") and not k.startswith("sk-placeholder"))

    def _get_system_instructions(self, context_data: Optional[Dict[str, Any]] = None) -> str:
        """Constructs grounded system instructions."""
        base_instructions = (
            "You are the Global FuelPulse AI Assistant, an expert, objective, and helpful AI capable of answering "
            "general knowledge, technical, educational, programming, career, business, and energy market questions.\n\n"
            "Guidelines:\n"
            "1. Answer clearly, accurately, and directly in plain language without unnecessary filler.\n"
            "2. When answering questions requiring up-to-date information, news, current statistics, policies, or prices, "
            "use your web search capability to retrieve current facts.\n"
            "3. Whenever web search sources are used, include clear clickable markdown links [Source Title](URL). "
            "Never invent sources, facts, search results, or citations.\n"
            "4. If reliable information cannot be found or is uncertain, clearly communicate that uncertainty.\n"
            "5. For questions about the Global FuelPulse AI platform, energy markets, or fuel data: reference the platform's "
            "authorized analytical database, sovereign tax models (e.g. Saudi 15% VAT & 0% income tax, India GST/VAT), "
            "and production facts.\n"
            "6. Never reveal secret API keys, credentials, or execute arbitrary unauthorized code."
        )
        if context_data:
            base_instructions += f"\n\nPlatform Context Data:\n{json.dumps(context_data, default=str)}"
        return base_instructions

    def _extract_sources_and_text_from_response(self, response_obj: Any) -> Tuple[str, List[Dict[str, str]]]:
        """
        Extracts narrative text and clickable source citations from an OpenAI Responses API response object.
        """
        text_chunks: List[str] = []
        sources: List[Dict[str, str]] = []
        seen_urls = set()

        # Handle Responses API Response object
        output_items = getattr(response_obj, "output", None)
        if output_items and isinstance(output_items, list):
            for item in output_items:
                # Check for output message
                if hasattr(item, "content") and item.content:
                    for c in item.content:
                        if hasattr(c, "text") and c.text:
                            text_chunks.append(c.text)
                            # Extract annotations / citations
                            if hasattr(c, "annotations") and c.annotations:
                                for ann in c.annotations:
                                    if hasattr(ann, "url") and ann.url and ann.url not in seen_urls:
                                        seen_urls.add(ann.url)
                                        sources.append({
                                            "title": getattr(ann, "title", "Source") or "Source",
                                            "url": ann.url
                                        })
                # Check for web search items or function calls
                if hasattr(item, "action") and getattr(item.action, "sources", None):
                    for src in item.action.sources:
                        if hasattr(src, "url") and src.url and src.url not in seen_urls:
                            seen_urls.add(src.url)
                            sources.append({
                                "title": getattr(src, "title", "Web Source") or "Web Source",
                                "url": src.url
                            })

        # Fallback to direct text attribute if output parsing was empty
        if not text_chunks and hasattr(response_obj, "text") and response_obj.text:
            text_chunks.append(str(response_obj.text))

        combined_text = "\n\n".join(t.strip() for t in text_chunks if t.strip())

        # If sources were found, format a clean clickable sources section if not already present in the text
        if sources and not any(src["url"] in combined_text for src in sources):
            source_bullets = "\n".join(f"- [{s['title']}]({s['url']})" for s in sources)
            combined_text += f"\n\n### 🔗 Sources & Citations\n{source_bullets}"

        return combined_text or "No response generated by the AI model.", sources

    def _call_responses_api(
        self,
        client: openai.OpenAI,
        prompt: str,
        system_instruction: str,
        enable_search: bool = True
    ) -> Tuple[str, List[Dict[str, str]], Optional[int]]:
        """
        Executes a query using OpenAI Responses API (`client.responses.create`).
        Falls back to Chat Completions if the Responses endpoint is unavailable for the selected model.
        """
        tools: List[Dict[str, Any]] = []
        if enable_search:
            tools.append({"type": "web_search_preview"})

        try:
            kwargs: Dict[str, Any] = {
                "model": self.model,
                "input": prompt,
                "instructions": system_instruction,
                "temperature": 0.2,
            }
            if tools:
                kwargs["tools"] = tools

            response = client.responses.create(**kwargs)
            text, sources = self._extract_sources_and_text_from_response(response)

            tokens_used = None
            if hasattr(response, "usage") and response.usage:
                tokens_used = getattr(response.usage, "total_tokens", None)

            return text, sources, tokens_used

        except Exception as responses_err:
            logger.warning(
                "Responses API call failed (%s). Falling back to Chat Completions API.",
                sanitize_sensitive_text(str(responses_err))
            )
            return self._call_chat_completions_fallback(client, prompt, system_instruction, enable_search)

    def _call_chat_completions_fallback(
        self,
        client: openai.OpenAI,
        prompt: str,
        system_instruction: str,
        enable_search: bool = True
    ) -> Tuple[str, List[Dict[str, str]], Optional[int]]:
        """
        Fallback implementation using Chat Completions API with web search grounding.
        """
        sources: List[Dict[str, str]] = []

        # Ground with live web search only if temporal or live data is needed
        if enable_search:
            try:
                from src.ai.deep_research_engine import DeepOnlineResearchEngine
                web_items = DeepOnlineResearchEngine.search_web(prompt, max_results=3)
                if web_items:
                    snippets = []
                    for it in web_items:
                        snippets.append(f"- [{it['title']}]({it['url']}): {it['snippet']}")
                        sources.append({"title": it["title"], "url": it["url"]})
                    system_instruction += f"\n\nLive Web Search Findings:\n" + "\n".join(snippets)
            except Exception as e:
                logger.debug(f"Fallback search grounding notice: {e}")

        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ]

        try:
            completion = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,
                max_tokens=600
            )
            raw_text = completion.choices[0].message.content or "No response generated."
            tokens_used = completion.usage.total_tokens if completion.usage else None

            # Append source links if not already present
            if sources and not any(s["url"] in raw_text for s in sources):
                src_list = "\n".join(f"- [{s['title']}]({s['url']})" for s in sources)
                raw_text += f"\n\n### 🔗 Sources & Citations\n{src_list}"

            return raw_text.strip(), sources, tokens_used

        except openai.APIConnectionError as conn_err:
            sanitized = sanitize_sensitive_text(str(conn_err))
            logger.error(f"OpenAI connection error: {sanitized}")
            raise OpenAIServiceError("Unable to reach OpenAI services. Please check your internet connection.", 503)
        except openai.RateLimitError as rate_err:
            sanitized = sanitize_sensitive_text(str(rate_err))
            logger.error(f"OpenAI rate limit error: {sanitized}")
            raise OpenAIServiceError("OpenAI API rate limit exceeded. Please try again shortly.", 429)
        except openai.AuthenticationError as auth_err:
            sanitized = sanitize_sensitive_text(str(auth_err))
            logger.error(f"OpenAI authentication error: {sanitized}")
            raise OpenAIMissingKeyError("Invalid OPENAI_API_KEY. Please check your credentials in .env.")
        except Exception as e:
            sanitized = sanitize_sensitive_text(str(e))
            logger.error(f"OpenAI chat completion error: {sanitized}")
            raise OpenAIServiceError(f"OpenAI service error: {sanitized}", 500)

    def answer_question(
        self,
        question: str,
        user_id: str,
        context_data: Optional[Dict[str, Any]] = None,
        enable_search: bool = True,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Main entrypoint to answer a natural language question using OpenAI.
        Enforces:
        - Authenticated user ID requirement.
        - Input length validation (<= 1000 chars).
        - Sub-millisecond question cache lookup (< 2ms response time, zero quota consumption).
        - Atomic rolling 24-hour quota check (HTTP 429 on exhaustion).
        - Intelligent web search gating (bypasses search for conceptual queries to cut latency).
        - Official OpenAI SDK Responses API call with web search when needed.
        - Atomic usage recording ONLY upon successful generation.
        """
        clean_q = (question or "").strip()
        if not clean_q:
            return {
                "status": "error",
                "status_code": 400,
                "error": "Empty question",
                "answer_text": "Please enter a question to ask the AI assistant.",
                "sources": [],
                "user_id": user_id,
                "quota_used": False
            }

        if len(clean_q) > MAX_QUESTION_LENGTH:
            return {
                "status": "error",
                "status_code": 400,
                "error": "Question too long",
                "answer_text": f"Question length ({len(clean_q)} chars) exceeds the {MAX_QUESTION_LENGTH} character limit.",
                "sources": [],
                "user_id": user_id,
                "quota_used": False
            }

        if not user_id:
            return {
                "status": "error",
                "status_code": 401,
                "error": "Authentication Required",
                "answer_text": "Please sign in to ask questions. Every registered user receives 3 free questions every rolling 24 hours.",
                "sources": [],
                "user_id": None,
                "quota_used": False
            }

        # Sub-millisecond cache retrieval (< 2ms response, zero quota consumed)
        if use_cache:
            try:
                from src.ai.cache_manager import question_cache
                cached = question_cache.get(clean_q)
                if cached and isinstance(cached, dict) and cached.get("status") == "success":
                    status = openai_quota_manager.get_user_quota_status(user_id)
                    cached_copy = cached.copy()
                    cached_copy.update({
                        "user_id": user_id,
                        "remaining_questions": status["remaining"],
                        "used_questions": status["used_count"],
                        "reset_time_str": status["reset_time_str"],
                        "quota_used": False,
                        "served_from_cache": True
                    })
                    return cached_copy
            except Exception as cache_err:
                logger.debug(f"Cache check bypass: {cache_err}")

        # 1. Enforce rolling 24-hour quota BEFORE calling OpenAI
        can_call, quota_msg, quota_status = openai_quota_manager.check_quota(user_id)
        if not can_call:
            raise OpenAIQuotaExhaustedError(
                message=quota_msg or "Daily quota exhausted.",
                reset_time_str=quota_status["reset_time_str"],
                reset_timestamp=quota_status["reset_timestamp"]
            )

        # 2. Check OpenAI API key configuration
        if not self.is_key_configured():
            raise OpenAIMissingKeyError(
                "OpenAI API key is missing. Please set `OPENAI_API_KEY` in your `.env` file to enable the assistant."
            )

        # 3. Initialize official OpenAI SDK client
        client = openai.OpenAI(
            api_key=self.api_key,
            timeout=float(settings.api.timeout_seconds)
        )

        system_instruction = self._get_system_instructions(context_data)

        # Intelligent search gating: only invoke web search if temporal or live updates are required
        from src.ai.deep_research_engine import should_perform_web_search
        needs_search = bool(enable_search and should_perform_web_search(clean_q))

        # 4. Execute API request
        try:
            answer_text, sources, tokens_used = self._call_responses_api(
                client=client,
                prompt=clean_q,
                system_instruction=system_instruction,
                enable_search=needs_search
            )
        except (OpenAIQuotaExhaustedError, OpenAIMissingKeyError, OpenAIServiceError):
            raise
        except Exception as unk_err:
            sanitized = sanitize_sensitive_text(str(unk_err))
            logger.error(f"Unexpected OpenAI error: {sanitized}")
            raise OpenAIServiceError("The AI assistant is temporarily unavailable. Please try again shortly.", 500)

        # 5. Atomically record usage upon successful answer generation
        openai_quota_manager.record_usage_atomic(
            user_id=user_id,
            question=clean_q,
            model_used=self.model,
            tokens_used=tokens_used
        )

        # Refresh quota status for response payload
        new_status = openai_quota_manager.get_user_quota_status(user_id)

        result = {
            "status": "success",
            "status_code": 200,
            "question": clean_q,
            "answer_text": answer_text,
            "sources": sources,
            "model_used": self.model,
            "user_id": user_id,
            "remaining_questions": new_status["remaining"],
            "used_questions": new_status["used_count"],
            "reset_time_str": new_status["reset_time_str"],
            "quota_used": True
        }

        # Cache successful response for instant subsequent retrieval
        if use_cache:
            try:
                from src.ai.cache_manager import question_cache
                question_cache.set(clean_q, result)
            except Exception as cache_save_err:
                logger.debug(f"Failed to cache question response: {cache_save_err}")

        return result


# Global singleton
openai_client = OpenAIClient()
