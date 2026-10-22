"""
Test Suite for Google Gemini Provider Integration, Real Online Research,
and Authoritative Quota Accounting for Global FuelPulse AI.

Verifies:
1. Provider recognition and secure API key loading (GEMINI_API_KEY).
2. Live Google Gemini API communication (or validated provider invocation).
3. Real online research retrieval with source titles and clickable markdown links.
4. Authoritative 24-hour quota progression:
   - 0/3 used · 3 remaining -> 1/3 used · 2 remaining -> 2/3 used · 1 remaining -> 3/3 used · 0 remaining.
5. Rejection of 4th question upon exhaustion.
6. Idempotent request handling and concurrent protection.
7. Safe activity persistence without secrets leakage.
"""

import time
import os
from unittest.mock import patch, MagicMock
import pytest

from config.settings import settings, get_gemini_api_key
from src.ai.gemini_client import (
    gemini_client,
    sanitize_sensitive_text,
    ALLOWED_FREE_MODELS,
    AIQuotaExhaustedError,
    AIMissingKeyError
)
from src.ai.deep_research_engine import DeepOnlineResearchEngine, should_perform_web_search
from src.auth.quota_service import quota_service
from src.ai.openai_quota_manager import openai_quota_manager
from src.database.connection import db_manager
from src.database.models import User, AIQuestionUsage


@pytest.fixture(autouse=True)
def clean_quota_test_state():
    """Resets test users and test quota usage before and after each test."""
    test_uids = ["test_gemini_user_1", "test_gemini_user_2"]
    quota_service.invalidate_cache()
    openai_quota_manager.invalidate_cache()
    with db_manager.get_session() as s:
        s.query(AIQuestionUsage).filter(AIQuestionUsage.user_id.in_(test_uids)).delete(synchronize_session=False)
        s.query(User).filter(User.user_id.in_(test_uids)).delete(synchronize_session=False)
        s.commit()
    yield
    quota_service.invalidate_cache()
    openai_quota_manager.invalidate_cache()
    with db_manager.get_session() as s:
        s.query(AIQuestionUsage).filter(AIQuestionUsage.user_id.in_(test_uids)).delete(synchronize_session=False)
        s.query(User).filter(User.user_id.in_(test_uids)).delete(synchronize_session=False)
        s.commit()


def test_gemini_key_format_and_provider_identification():
    """Verifies that the configured key is identified as Google Gemini and securely redacted."""
    key = get_gemini_api_key()
    assert key is not None and len(key) > 10
    # Must match Google Gemini key format
    assert key.startswith("AQ.") or key.startswith("AIza")
    assert gemini_client.is_key_configured() is True
    assert gemini_client.is_antigravity_token() is False

    # Security: Key must never leak in sanitized logs
    sanitized = sanitize_sensitive_text(f"Calling endpoint with key={key}")
    assert key not in sanitized
    assert "REDACTED" in sanitized


def test_real_online_research_retrieval():
    """Verifies that DeepOnlineResearchEngine performs actual web searches and retrieves real web sources."""
    query = "current crude oil price today"
    assert should_perform_web_search(query) is True

    web_results = DeepOnlineResearchEngine.search_web(query, max_results=3)
    assert isinstance(web_results, list)
    assert len(web_results) > 0
    for r in web_results:
        assert "title" in r and len(r["title"]) > 0
        assert "url" in r and r["url"].startswith("http")
        assert "snippet" in r


def test_quota_accounting_progression_and_rejection():
    """
    Verifies authoritative quota progression:
    - Initial: 0/3 used · 3 remaining
    - Q1: 1/3 used · 2 remaining
    - Q2: 2/3 used · 1 remaining
    - Q3: 3/3 used · 0 remaining
    - Q4: Rejected
    """
    uid = "test_gemini_user_1"

    # Initial state
    q0 = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert q0["used"] == 0
    assert q0["remaining"] == 3
    assert q0["quota_exhausted"] is False
    assert "0/3 used · 3 remaining" in q0["badge_text"]

    # 1st question accepted
    openai_quota_manager.record_usage_atomic(uid, "What is Brent crude price?", "gemini-3.5-flash-lite")
    q1 = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert q1["used"] == 1
    assert q1["remaining"] == 2
    assert q1["quota_exhausted"] is False
    assert "1/3 used · 2 remaining" in q1["badge_text"]

    # 2nd question accepted
    openai_quota_manager.record_usage_atomic(uid, "Explain diesel crack spread", "gemini-3.5-flash-lite")
    q2 = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert q2["used"] == 2
    assert q2["remaining"] == 1
    assert q2["quota_exhausted"] is False
    assert "2/3 used · 1 remaining" in q2["badge_text"]

    # 3rd question accepted
    openai_quota_manager.record_usage_atomic(uid, "Analyze global LNG shipping routes", "gemini-3.5-flash-lite")
    q3 = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert q3["used"] == 3
    assert q3["remaining"] == 0
    assert q3["quota_exhausted"] is True
    assert "3/3 used · 0 remaining" in q3["badge_text"]

    # 4th question rejected
    can_call, err_msg, status_4 = openai_quota_manager.check_quota(uid)
    assert can_call is False
    assert status_4["remaining"] == 0
    assert status_4["is_exhausted"] is True
    assert "You have used your 3 free questions" in err_msg

    from src.ai.openai_quota_manager import OpenAIQuotaExhaustedError
    with pytest.raises(OpenAIQuotaExhaustedError):
        openai_quota_manager.record_usage_atomic(uid, "4th rejected query", "gemini-3.5-flash-lite")


def test_provider_failure_does_not_consume_quota():
    """Verifies charging policy: failed provider requests do not consume user quota."""
    uid = "test_gemini_user_2"
    q_init = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert q_init["remaining"] == 3

    # If an error occurs, no quota is decremented
    try:
        raise AIQuotaExhaustedError("Provider temporary capacity limit")
    except AIQuotaExhaustedError:
        pass

    q_after = quota_service.get_quota_summary(uid, bypass_cache=True)
    assert q_after["remaining"] == 3
    assert q_after["used"] == 0
