"""
Google Gemini Free-Tier Client.
Strictly restricted to free-tier Flash and Flash-Lite models.
Enforces zero billing-linked features, redacts API keys, and detects quota errors.
"""

import os
import re
import json
import logging
from typing import Dict, Any, Optional, List
import requests

from config.settings import settings
from src.ai.quota_manager import quota_manager

logger = logging.getLogger(__name__)

# Allowed free-tier models (protects user from paid model calls)
ALLOWED_FREE_MODELS = {
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.8-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
}

DEFAULT_FREE_MODEL = "gemini-3.5-flash-lite"


class AIQuotaExhaustedError(Exception):
    """Raised when Google Gemini returns HTTP 429, RESOURCE_EXHAUSTED, or quota limits."""
    pass


class AIMissingKeyError(Exception):
    """Raised when GEMINI_API_KEY is not configured."""
    pass


class AIServiceUnavailableError(Exception):
    """Raised for general network failures or timeouts."""
    pass


def sanitize_sensitive_text(text: str) -> str:
    """Removes API keys or secret tokens from strings to prevent logging leaks."""
    if not text:
        return ""
    # Mask URL query param keys: key=AIza... or key=AQ...
    sanitized = re.sub(r"key=[a-zA-Z0-9_\-]+", "key=REDACTED_API_KEY", str(text))
    # Mask raw AIza keys:
    sanitized = re.sub(r"AIza[0-9A-Za-z\-_]{35}", "AIza...REDACTED", sanitized)
    # Mask raw AQ keys:
    sanitized = re.sub(r"AQ\.[0-9A-Za-z\-_]{30,}", "AQ...REDACTED", sanitized)
    return sanitized


class GeminiFreeTierClient:
    """Client for Google Gemini Free-Tier REST API."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self._explicit_key = api_key.strip() if api_key is not None else None
        self._explicit_model = model.strip() if model is not None else None

    @property
    def api_key(self) -> str:
        """Dynamic getter for API key."""
        if self._explicit_key is not None:
            return self._explicit_key
        return settings.api.gemini_api_key

    @property
    def model(self) -> str:
        """Dynamic getter for model with strict free-tier whitelist enforcement."""
        configured = (self._explicit_model or settings.api.ai_model).strip()
        if configured in ALLOWED_FREE_MODELS:
            return configured
        logger.warning(
            f"Configured model '{configured}' is not in free-tier whitelist. "
            f"Falling back to free model '{DEFAULT_FREE_MODEL}'."
        )
        return DEFAULT_FREE_MODEL

    def is_key_configured(self) -> bool:
        """Checks if a valid non-empty API key is available."""
        k = self.api_key
        return bool(k and len(k) > 5)

    def is_antigravity_token(self) -> bool:
        """Checks if the configured key is an Antigravity token rather than an external Google AI Studio key."""
        k = (self.api_key or "").strip()
        if not k:
            return False
        # External Google API keys or OAuth tokens
        if k.startswith("AIza") or k.startswith("AQ.") or k.startswith("ya29."):
            return False
        return k.startswith("agy_") or "antigravity" in k.lower()

    def generate_intelligence(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        context_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Calls Gemini free-tier REST API or Antigravity Enterprise Engine to generate an analytical briefing.
        Detects HTTP 429 / RESOURCE_EXHAUSTED and triggers quota latching.
        Never exposes the API key in logs or exceptions.
        """
        if not self.is_key_configured():
            raise AIMissingKeyError("Google Gemini API key is missing. Please set GEMINI_API_KEY in .env.")

        # Check quota manager before making the outbound network call
        can_call, reason, user_msg = quota_manager.check_quota()
        if not can_call:
            raise AIQuotaExhaustedError(user_msg)

        # 1. Antigravity Enterprise Engine routing (for connected Antigravity tokens)
        if self.is_antigravity_token():
            from src.ai.nl_query_engine import AIEnergyMarketAnalyst
            resp_dict = AIEnergyMarketAnalyst._generate_autonomous_free_ai_answer(prompt)
            quota_manager.record_call_success()
            return resp_dict.get("answer_text", "")

        # 2. Google Gemini REST API routing (for Google AI Studio / Gemini API keys or OAuth tokens)
        headers = {"Content-Type": "application/json"}
        if self.api_key.startswith("ya29."):
            headers["Authorization"] = f"Bearer {self.api_key}"
            params = {}
        else:
            params = {"key": self.api_key}

        payload: Dict[str, Any] = {}

        # Default professional analyst grounding instruction
        default_system = (
            "You are Global FuelPulse AI, a professional, world-class executive AI assistant and market intelligence analyst. "
            "You provide rigorous, objective, and deeply grounded answers across all domains: general knowledge, "
            "science, programming, business, macroeconomics, policy, and global energy markets.\n\n"
            "Professional Guidelines:\n"
            "1. Answer the question directly and articulately in clear, executive-grade language without conversational filler or meta-labels.\n"
            "2. Whenever explaining a concept, workflow, supply chain, system architecture, or economic cycle, provide a clean Mermaid flowchart diagram (using ```mermaid ... ```).\n"
            "3. Provide structured '### 🔍 Key Facts & Analytical Breakdown' with bullet points, figures, and verified insights.\n"
            "4. Never invent speculative prices or hallucinatory statistics."
        )
        sys_text = system_instruction or default_system
        if context_data:
            sys_text += f"\n\nContext Data from Database:\n{json.dumps(context_data, default=str)}"

        # Enrich with live web research grounding
        try:
            from src.ai.deep_research_engine import DeepOnlineResearchEngine
            web_items = DeepOnlineResearchEngine.search_web(prompt, max_results=4)
            if web_items:
                snippets_text = "\n".join(f"- [{it['title']}]({it['url']}): {it['snippet']}" for it in web_items)
                sys_text += f"\n\nLive External Web Research Grounding (Real-Time Current Web Findings):\n{snippets_text}\n"
                sys_text += "Always incorporate these live search findings and cite the sources as clickable markdown links [Source Title](URL)."
        except Exception as e:
            logger.debug(f"Web research grounding notice: {e}")

        payload["system_instruction"] = {
            "parts": [{"text": sys_text}]
        }

        payload["contents"] = [
            {
                "parts": [{"text": prompt}]
            }
        ]

        # Generation config (strict free tier parameters, low temperature & bounded tokens for fast response)
        payload["generationConfig"] = {
            "temperature": 0.1,
            "maxOutputTokens": 600,
            "topP": 0.8,
        }

        # Multi-model resilience: try primary model, fall back to companion models if Google returns 429/404/503/500
        models_to_try = [self.model]
        for companion in ["gemini-3.5-flash-lite", "gemini-2.5-flash-lite", "gemini-3.5-flash"]:
            if companion not in models_to_try and companion in ALLOWED_FREE_MODELS:
                models_to_try.append(companion)

        last_response = None
        for candidate_model in models_to_try:
            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{candidate_model}:generateContent"
            try:
                response = requests.post(
                    endpoint,
                    params=params,
                    json=payload,
                    timeout=settings.api.timeout_seconds,
                    headers=headers
                )
                last_response = response
            except requests.exceptions.RequestException as req_err:
                sanitized_err = sanitize_sensitive_text(str(req_err))
                logger.error(f"Gemini API request failed for {candidate_model}: {sanitized_err}")
                if candidate_model == models_to_try[-1]:
                    raise AIServiceUnavailableError(
                        "Unable to connect to the energy AI service at this moment. "
                        "Please check your internet connection."
                    )
                continue

            # Success
            if response.status_code == 200:
                break

            # If quota exceeded, model not found, or capacity spike, try fallback model if available
            if response.status_code in (429, 404, 500, 502, 503, 504) and candidate_model != models_to_try[-1]:
                logger.warning(
                    f"Gemini model '{candidate_model}' returned status {response.status_code}. "
                    f"Attempting fallback to companion model..."
                )
                continue

            # Provider quota error on final candidate model
            if response.status_code == 429:
                quota_manager.record_provider_quota_error("HTTP 429: Too Many Requests / Free Quota Exceeded")
                reset_str = quota_manager.get_formatted_reset_time()
                raise AIQuotaExhaustedError(
                    f"The free AI quota for today is finished. The AI assistant will be available "
                    f"again after {reset_str}. Meanwhile you can still use the charts, tables and "
                    f"forecasts on the dashboard."
                )

            # Non-transient or final attempt failure
            break

        response = last_response
        if response is None:
            raise AIServiceUnavailableError("The AI assistant is temporarily unavailable. Please try again shortly.")

        if response.status_code != 200:
            resp_text = sanitize_sensitive_text(response.text)
            logger.warning(f"Gemini API returned status {response.status_code}: {resp_text[:300]}")

            # Check if error message mentions quota, rate limit, or resource exhausted
            if any(term in resp_text.lower() for term in ["quota", "resource_exhausted", "rate_limit", "billing"]):
                quota_manager.record_provider_quota_error(f"Status {response.status_code}: {resp_text[:150]}")
                reset_str = quota_manager.get_formatted_reset_time()
                raise AIQuotaExhaustedError(
                    f"The free AI quota for today is finished. The AI assistant will be available "
                    f"again after {reset_str}. Meanwhile you can still use the charts, tables and "
                    f"forecasts on the dashboard."
                )

            raise AIServiceUnavailableError(
                "The AI assistant is temporarily unavailable. Please try again shortly."
            )

        # Parse success response
        try:
            data = response.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                text_pieces = [
                    p.get("text", "")
                    for p in parts
                    if isinstance(p, dict) and "text" in p and not p.get("thought", False)
                ]
                if not text_pieces:
                    # Fallback to any part with text
                    text_pieces = [
                        p.get("text", "")
                        for p in parts
                        if isinstance(p, dict) and "text" in p
                    ]
                if text_pieces:
                    full_text = "\n".join(t.strip() for t in text_pieces if t.strip())
                    if full_text:
                        quota_manager.record_call_success()
                        return full_text

            return "No narrative response generated by the AI model."
        except Exception as e:
            logger.error(f"Failed to parse Gemini response JSON: {sanitize_sensitive_text(str(e))}")
            raise AIServiceUnavailableError("Failed to parse market intelligence briefing.")


# Global singleton client
gemini_client = GeminiFreeTierClient()
