"""
Automated Test Suite for AI Quota Protection, Rate Limiting, and Abuse Prevention.
Verifies:
1. Provider HTTP 429 / RESOURCE_EXHAUSTED detection and latching.
2. Daily cap enforcement and exact reset time messaging.
3. Rolling 60-second per-minute rate limit.
4. Graceful handling of missing API key without crashes.
5. Multi-user concurrent execution safety with file/thread locks.
6. Question caching (0 quota consumed on repeated questions).
7. Direct database query routing for simple price inquiries (0 quota consumed).
8. Per-user session protection (500 char limit, 3s cooldown, 15 msgs/hour).
9. Key sanitation (API key never leaked or logged).
10. Strict free-tier model whitelisting.
"""

import time
import threading
from unittest.mock import patch, MagicMock
import pytest

from config.settings import settings
from src.ai.quota_manager import AIQuotaManager, quota_manager
from src.ai.cache_manager import QuestionCacheManager, question_cache
from src.ai.gemini_client import (
    GeminiFreeTierClient,
    AIQuotaExhaustedError,
    AIMissingKeyError,
    AIServiceUnavailableError,
    sanitize_sensitive_text,
    ALLOWED_FREE_MODELS,
    DEFAULT_FREE_MODEL
)
from src.ai.nl_query_engine import AIEnergyMarketAnalyst, SessionAbuseProtector


@pytest.fixture(autouse=True)
def clean_test_state(tmp_path):
    """Resets quota and cache state for each test."""
    test_quota_file = tmp_path / "test_quota_state.json"
    test_cache_file = tmp_path / "test_cache_state.json"

    # Patch global quota_manager and question_cache paths
    quota_manager.state_file_path = test_quota_file
    quota_manager.reset_state()

    question_cache.cache_file_path = test_cache_file
    question_cache.clear()

    yield

    quota_manager.reset_state()
    question_cache.clear()


def test_provider_429_quota_error_latches():
    """Simulates HTTP 429 quota error and confirms AI stops completely until reset."""
    client = GeminiFreeTierClient(api_key="AIzaSyDummyKeyForTestingOnly123456789")

    # Mock requests.post to return HTTP 429
    mock_resp = MagicMock()
    mock_resp.status_code = 429
    mock_resp.text = '{"error": {"code": 429, "message": "Resource has been exhausted (e.g. check quota)."}}'

    with patch("requests.post", return_value=mock_resp):
        with pytest.raises(AIQuotaExhaustedError) as exc_info:
            client.generate_intelligence("Explain global crude supply")

        err_text = str(exc_info.value)
        assert "The free AI quota for today is finished" in err_text
        assert "Meanwhile you can still use the charts, tables and forecasts on the dashboard" in err_text

    # Verify quota_manager status is marked as finished
    status = quota_manager.get_quota_status()
    assert status["is_finished"] is True
    assert status["provider_exhausted"] is True

    # Subsequent check_quota must immediately block without network calls
    can_call, reason, user_msg = quota_manager.check_quota()
    assert can_call is False
    assert reason == "PROVIDER_EXHAUSTED"
    assert "The free AI quota for today is finished" in user_msg


def test_daily_cap_reached_blocks_calls():
    """Verifies that reaching MAX_AI_CALLS_PER_DAY blocks further calls with reset message."""
    max_daily = settings.api.max_ai_calls_per_day

    # Increment calls up to max_daily
    for _ in range(max_daily):
        quota_manager.record_call_success()

    status = quota_manager.get_quota_status()
    assert status["calls_today"] == max_daily
    assert status["calls_remaining"] == 0
    assert status["is_finished"] is True

    can_call, reason, user_msg = quota_manager.check_quota()
    assert can_call is False
    assert reason == "DAILY_LIMIT_REACHED"
    assert "The free AI quota for today is finished" in user_msg
    assert status["reset_time_str"] in user_msg


def test_per_minute_rate_limit():
    """Verifies that reaching MAX_AI_CALLS_PER_MINUTE returns the minute rate limit notice."""
    max_minute = settings.api.max_ai_calls_per_minute

    # Record max_minute calls
    for _ in range(max_minute):
        quota_manager.record_call_success()

    can_call, reason, user_msg = quota_manager.check_quota()
    assert can_call is False
    assert reason == "MINUTE_RATE_LIMIT"
    assert user_msg == "Too many questions right now. Please try again in a minute."


def test_missing_api_key_graceful_message():
    """Verifies that a missing API key returns a friendly notice without crashing when autonomous mode is off."""
    client = GeminiFreeTierClient(api_key="")
    assert client.is_key_configured() is False

    ans = AIEnergyMarketAnalyst.answer_question(
        question="What is the outlook for refining margins in Europe?",
        session_id="test_key_session",
        bypass_session_limits=True
    )
    assert ans["is_fallback"] is True
    assert "The AI assistant requires a free Gemini API key" in ans["answer_text"]
    assert "GEMINI_API_KEY" in ans["answer_text"]


def test_autonomous_free_ai_mode_without_api_key():
    """Verifies that free autonomous mode answers questions seamlessly without any API key or quota."""
    client = GeminiFreeTierClient(api_key="")
    assert client.is_key_configured() is False

    # 1. European refining margins query with allow_free_autonomous=True
    ans_europe = AIEnergyMarketAnalyst.answer_question(
        question="What is the outlook for refining margins in Europe?",
        session_id="free_ai_session_1",
        bypass_session_limits=True,
        allow_free_autonomous=True
    )
    assert ans_europe["is_fallback"] is False
    assert ans_europe["autonomous_free_mode"] is True
    assert ans_europe["quota_used"] is False
    assert "refining" in ans_europe["answer_text"].lower()

    # 2. Prayagraj petrol tax query
    ans_prayagraj = AIEnergyMarketAnalyst.answer_question(
        question="What is the petrol price in Prayagraj and how much tax does the state take?",
        session_id="free_ai_session_2",
        bypass_session_limits=True,
        allow_free_autonomous=True
    )
    assert ans_prayagraj["is_fallback"] is False
    assert "101.45" in ans_prayagraj["answer_text"]
    assert "Prayagraj" in ans_prayagraj["answer_text"]

    # 3. Indian PSU OMCs query
    ans_omc = AIEnergyMarketAnalyst.answer_question(
        question="What is the market share of IOCL, BPCL and HPCL?",
        session_id="free_ai_session_3",
        bypass_session_limits=True,
        allow_free_autonomous=True
    )
    assert ans_omc["is_fallback"] is False
    assert "IOCL" in ans_omc["answer_text"]
    assert "BPCL" in ans_omc["answer_text"]


def test_concurrent_multi_user_locking():
    """Verifies thread-safe atomic counter updates under concurrent multi-user load."""
    threads = []
    num_threads = 12
    calls_per_thread = 5

    def worker():
        for _ in range(calls_per_thread):
            quota_manager.record_call_success()

    for _ in range(num_threads):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    status = quota_manager.get_quota_status()
    assert status["calls_today"] == num_threads * calls_per_thread


def test_question_caching_saves_quota():
    """Verifies that asking the same question twice serves from cache and uses 0 quota."""
    question = "Which countries exported the most crude oil in the latest available reporting year?"

    # First call - queries DB and populates cache
    ans1 = AIEnergyMarketAnalyst.answer_question(
        question=question,
        session_id="cache_session_1",
        bypass_session_limits=True
    )
    assert ans1["quota_used"] is False

    # Second call - must come from cache
    ans2 = AIEnergyMarketAnalyst.answer_question(
        question=question,
        session_id="cache_session_2",
        bypass_session_limits=True
    )
    assert ans2["served_from_cache"] is True
    assert ans2["quota_used"] is False
    assert ans2["topic"] == ans1["topic"]


def test_direct_database_query_routing():
    """Verifies that simple retail fuel price questions are answered from DB with 0 quota."""
    question = "Compare petrol prices in India, Germany and the United States."
    ans = AIEnergyMarketAnalyst.answer_question(
        question=question,
        session_id="db_session_1",
        bypass_session_limits=True
    )
    assert ans["served_from_db"] is True
    assert ans["quota_used"] is False
    assert len(ans["data_records"]) > 0


def test_session_abuse_protection():
    """Verifies per-user protection: length limit, cooldown, and hourly frequency."""
    protector = SessionAbuseProtector()

    # 1. Message Length Limit (>500 characters)
    long_q = "fuel " * 150  # 750 characters
    valid, topic, msg = protector.validate_and_record("s1", long_q)
    assert valid is False
    assert "Message Length Limit" in topic
    assert "maximum is 500" in msg

    # 2. Cooldown check (minimum 3 seconds)
    valid1, _, _ = protector.validate_and_record("s2", "What is the price of petrol?")
    assert valid1 is True

    # Immediate second request should trigger cooldown
    valid2, topic2, msg2 = protector.validate_and_record("s2", "What is the price of diesel?")
    assert valid2 is False
    assert "Cooldown Active" in topic2
    assert "wait at least 3 seconds" in msg2

    # 3. Frequency limit (max 15 questions per hour)
    protector.reset()
    for i in range(15):
        # Artificially shift timestamp backward to bypass cooldown for frequency testing
        protector._sessions.setdefault("s3", {"last_timestamp": 0.0, "hourly_timestamps": []})
        protector._sessions["s3"]["last_timestamp"] = time.time() - 10.0
        v, _, _ = protector.validate_and_record("s3", f"Question {i}")
        assert v is True

    # 16th question in 1 hour should be rejected
    protector._sessions["s3"]["last_timestamp"] = time.time() - 10.0
    v16, topic16, msg16 = protector.validate_and_record("s3", "Question 16")
    assert v16 is False
    assert "Session Limit Reached" in topic16
    assert "limit of 15 questions per hour" in msg16


def test_api_key_sanitization():
    """Verifies that API keys are completely stripped and never logged or exposed in strings."""
    secret = "AIzaSyB1234567890abcdefghijklmnopqrstuv"
    raw_error = f"Failed to connect to https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={secret}"

    cleaned = sanitize_sensitive_text(raw_error)
    assert secret not in cleaned
    assert "REDACTED" in cleaned


def test_strict_free_tier_model_whitelisting():
    """Verifies that only free-tier models are accepted and paid models fall back safely."""
    # Paid or pro model should fall back to DEFAULT_FREE_MODEL
    client = GeminiFreeTierClient(api_key="dummy", model="gemini-1.5-pro")
    assert client.model == DEFAULT_FREE_MODEL

    # Valid free tier model should be preserved
    client2 = GeminiFreeTierClient(api_key="dummy", model="gemini-1.5-flash")
    assert client2.model == "gemini-1.5-flash"


def test_who_is_more_contributor_of_petrol_in_the_world():
    """Verifies that the specific query answers from project data with sources, year, and disclosures."""
    question = "who is the more contributor of petrol in the world"
    ans = AIEnergyMarketAnalyst.answer_question(
        question=question,
        session_id="petrol_contrib_test_session",
        bypass_session_limits=True
    )

    assert ans["topic"] == "Global Petroleum & Petrol Contribution"
    assert ans["quota_used"] is False
    assert ans["served_from_db"] is True
    assert len(ans["data_records"]) >= 5

    # Check top producer is United States
    top_country = ans["data_records"][0]["Country"]
    assert "United States" in top_country

    # Check that sources and year (2024) are explicitly cited
    sources_text = " ".join(ans["sources_cited"])
    assert "EIA" in sources_text
    assert "2024" in sources_text
    assert "Energy Institute" in sources_text

    # Check narrative text contains proper data scope disclosure
    text = ans["answer_text"]
    assert "United States" in text
    assert "2024" in text
    assert "Data Scope & Limitations" in text
    assert "13.20" in text or "mbpd" in text


def test_ai_api_key_fallback_resolution():
    """Verifies that AI_API_KEY is accepted as a valid fallback for GEMINI_API_KEY."""
    import os
    from config.settings import settings

    old_gemini = os.environ.get("GEMINI_API_KEY")
    old_ai = os.environ.get("AI_API_KEY")

    try:
        # Clear GEMINI_API_KEY and set AI_API_KEY
        os.environ["GEMINI_API_KEY"] = ""
        os.environ["AI_API_KEY"] = "AIzaSyTestFallbackKey12345"

        client = GeminiFreeTierClient()
        assert client.api_key == "AIzaSyTestFallbackKey12345"
        assert client.is_key_configured() is True
    finally:
        if old_gemini is not None:
            os.environ["GEMINI_API_KEY"] = old_gemini
        else:
            os.environ.pop("GEMINI_API_KEY", None)
        if old_ai is not None:
            os.environ["AI_API_KEY"] = old_ai
        else:
            os.environ.pop("AI_API_KEY", None)

