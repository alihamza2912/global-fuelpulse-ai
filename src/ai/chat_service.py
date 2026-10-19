"""
Backend Chat and Usage Service for Global FuelPulse AI.
Provides clean service endpoints for:
- Asking natural language questions with OpenAI Responses API and web search.
- Quota status inspection and rolling 24-hour enforcement.
- Authenticated user session validation.
- Input validation, length bounds, cyber/injection screening, and API error formatting.
- Strict security: Never executes arbitrary AI-generated code or SQL.
"""

import logging
from typing import Dict, Any, Optional

from src.ai.openai_client import (
    openai_client,
    OpenAIQuotaExhaustedError,
    OpenAIMissingKeyError,
    OpenAIServiceError,
    MAX_QUESTION_LENGTH
)
from src.ai.openai_quota_manager import openai_quota_manager, MAX_QUESTIONS_PER_24H
from src.auth.auth_service import AuthService
from src.ai.nl_query_engine import session_protector

logger = logging.getLogger(__name__)


def get_user_quota_endpoint(user_id: str) -> Dict[str, Any]:
    """
    Endpoint returning the remaining question count, max allowed, and reset countdown for a user.
    """
    if not user_id:
        return {
            "status": "error",
            "status_code": 401,
            "error": "Authentication required",
            "remaining": 0,
            "max_allowed": MAX_QUESTIONS_PER_24H,
            "reset_time_str": "N/A"
        }
    status = openai_quota_manager.get_user_quota_status(user_id)
    return {
        "status": "success",
        "status_code": 200,
        "user_id": user_id,
        "max_allowed": status["max_allowed"],
        "used_count": status["used_count"],
        "remaining": status["remaining"],
        "is_exhausted": status["is_exhausted"],
        "reset_time_str": status["reset_time_str"],
        "reset_timestamp": status["reset_timestamp"].isoformat() if status["reset_timestamp"] else None
    }


def chat_endpoint(
    question: str,
    user_id: str,
    context_data: Optional[Dict[str, Any]] = None,
    enable_search: bool = True
) -> Dict[str, Any]:
    """
    Main chat endpoint for natural language query execution.
    Validates input, checks security filters, enforces rolling 24h quota, and calls OpenAI.
    """
    # 1. Validation: Clean text & length limit
    clean_q = (question or "").strip()
    if not clean_q:
        return {
            "status": "error",
            "status_code": 400,
            "error": "Empty Question",
            "message": "Please enter a question to ask the AI assistant.",
            "answer_text": "Please enter a question to ask the AI assistant.",
            "sources": [],
            "remaining": 0
        }

    if len(clean_q) > MAX_QUESTION_LENGTH:
        return {
            "status": "error",
            "status_code": 400,
            "error": "Payload Too Large",
            "message": f"Question length ({len(clean_q)} chars) exceeds maximum allowed limit of {MAX_QUESTION_LENGTH} characters.",
            "answer_text": f"Question length ({len(clean_q)} chars) exceeds maximum allowed limit of {MAX_QUESTION_LENGTH} characters.",
            "sources": [],
            "remaining": 0
        }

    # 2. Authentication check
    if not user_id or not str(user_id).strip():
        return {
            "status": "error",
            "status_code": 401,
            "error": "Authentication Required",
            "message": "You must be signed in to ask questions. Every registered user receives 3 free questions every 24 hours.",
            "answer_text": "Please sign in to ask questions. Every registered user receives 3 free questions every 24 hours.",
            "sources": [],
            "remaining": 0
        }

    # 3. Security Screening against prompt injections / exploit payloads
    is_illegal, violation = session_protector.check_illegal_activity(clean_q)
    if is_illegal:
        logger.warning("Security screening blocked payload from user %s: %s", user_id, violation)
        return {
            "status": "error",
            "status_code": 403,
            "error": "Security Violation",
            "message": "Your question was flagged by our safety shield as containing an unauthorized command or exploit pattern.",
            "answer_text": "Your question was flagged by our safety shield as containing an unauthorized command or exploit pattern.",
            "sources": [],
            "remaining": 0
        }

    # 4. Execute question through OpenAI client with atomic quota guard
    try:
        result = openai_client.answer_question(
            question=clean_q,
            user_id=str(user_id).strip(),
            context_data=context_data,
            enable_search=enable_search
        )
        return result

    except OpenAIQuotaExhaustedError as quota_err:
        logger.info("Quota exhausted for user %s (HTTP 429)", user_id)
        return {
            "status": "error",
            "status_code": 429,
            "error": "Quota Exhausted",
            "message": quota_err.message,
            "answer_text": quota_err.message,
            "sources": [],
            "remaining": 0,
            "reset_time_str": quota_err.reset_time_str,
            "reset_timestamp": quota_err.reset_timestamp.isoformat() if quota_err.reset_timestamp else None
        }

    except OpenAIMissingKeyError as key_err:
        return {
            "status": "error",
            "status_code": 401,
            "error": "Missing API Key",
            "message": key_err.message,
            "answer_text": key_err.message,
            "sources": [],
            "remaining": 0
        }

    except OpenAIServiceError as svc_err:
        return {
            "status": "error",
            "status_code": svc_err.status_code,
            "error": "Service Error",
            "message": svc_err.message,
            "answer_text": svc_err.message,
            "sources": [],
            "remaining": 0
        }

    except Exception as e:
        logger.error("Unexpected error in chat_endpoint: %s", e)
        return {
            "status": "error",
            "status_code": 500,
            "error": "Internal Error",
            "message": "An unexpected error occurred while processing your request. Please try again shortly.",
            "answer_text": "An unexpected error occurred while processing your request. Please try again shortly.",
            "sources": [],
            "remaining": 0
        }
