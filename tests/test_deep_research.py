"""
Test Suite for Deep Online Research Engine and Custom User API Key Integration.
Verifies:
1. Real-time web search retrieval and Wikipedia fallback.
2. Extraction of numerical figures and generation of dynamic Mermaid diagrams.
3. NL Query Engine routing of arbitrary queries to deep research.
4. Dynamic user API key recognition in session state.
"""

from unittest.mock import patch, MagicMock
import pytest
from src.ai.deep_research_engine import DeepOnlineResearchEngine
from src.ai.nl_query_engine import AIEnergyMarketAnalyst
from src.ai.quota_manager import quota_manager
from src.ai.cache_manager import question_cache
from config.settings import get_gemini_api_key


@pytest.fixture(autouse=True)
def clean_test_state(tmp_path):
    """Resets quota and cache state for each test in this module."""
    test_quota_file = tmp_path / "test_deep_quota.json"
    test_cache_file = tmp_path / "test_deep_cache.json"
    quota_manager.state_file_path = test_quota_file
    quota_manager.reset_state()
    question_cache.cache_file_path = test_cache_file
    question_cache.clear()
    yield
    quota_manager.reset_state()
    question_cache.clear()


def test_deep_research_search_web():
    """Verifies search_web returns structured results with title, snippet, and url."""
    results = DeepOnlineResearchEngine.search_web("fuel price in Tokyo", max_results=3)
    assert isinstance(results, list)
    if results:
        first = results[0]
        assert "title" in first
        assert "snippet" in first
        assert "url" in first


def test_deep_research_extracts_and_formats_answer():
    """Verifies research_and_answer builds a full grounded briefing with Mermaid diagram and records."""
    ans = DeepOnlineResearchEngine.research_and_answer("who supplies crude oil to Sri Lanka")
    assert ans["is_fallback"] is False
    assert "autonomous_free_mode" in ans
    assert "mermaid" in ans["answer_text"].lower()
    assert len(ans["sources_cited"]) > 0
    assert "data_records" in ans


def test_arbitrary_query_never_returns_generic_three_producers():
    """Verifies arbitrary queries do NOT return the generic US 13.20 mbpd / Russia / Saudi boilerplate."""
    mock_search = [
        {
            "title": "Tokyo Fuel Market 2026",
            "snippet": "Gasoline prices in Tokyo averaged 169.6 JPY per liter with stable domestic refining margins.",
            "url": "https://example.com/tokyo-fuel",
            "source": "Web Search (Live)"
        }
    ]
    with patch.object(DeepOnlineResearchEngine, "search_web", return_value=mock_search):
        ans = AIEnergyMarketAnalyst.answer_question(
            question="what is the retail fuel price in Tokyo Japan today",
            session_id="test_tokyo_session",
            bypass_session_limits=True,
            allow_free_autonomous=True
        )
        assert ans["is_fallback"] is False
        assert "169.6" in ans["answer_text"] or "Tokyo" in ans["answer_text"]
        # Must NOT contain the old generic boilerplate
        assert "13.20 mbpd" not in ans["answer_text"]


def test_custom_user_api_key_retrieval():
    """Verifies that personal API keys stored in st.session_state are recognized dynamically."""
    import streamlit as st
    st.session_state["user_api_key"] = "AIzaSyTestUserCustomKey12345"

    try:
        retrieved_key = get_gemini_api_key()
        assert retrieved_key == "AIzaSyTestUserCustomKey12345"
    finally:
        st.session_state.pop("user_api_key", None)


def test_iocl_ownership_query_does_not_hijack_to_jio_competition():
    """Verifies that 'who is the owner of fuel company of iocl' routes to live intelligence, not Jio-bp competition."""
    from src.ai.nl_query_engine import question_cache
    question_cache.clear()

    mock_search = [
        {
            "title": "Indian Oil Corporation - Wikipedia",
            "snippet": "Indian Oil Corporation Limited (IOCL) is an Indian multinational oil and gas public sector undertaking under the ownership of Ministry of Petroleum and Natural Gas, Government of India.",
            "url": "https://en.wikipedia.org/wiki/Indian_Oil_Corporation",
            "source": "Web Search (Live)"
        }
    ]
    with patch.object(DeepOnlineResearchEngine, "search_web", return_value=mock_search):
        ans = AIEnergyMarketAnalyst.answer_question(
            question="who is the owner of fuel company of iocl",
            session_id="test_iocl_owner_session",
            bypass_session_limits=True,
            allow_free_autonomous=True
        )
        assert ans["is_fallback"] is False
        assert "Who Can Easily Compete with Jio-bp" not in ans["answer_text"]
        assert "Government of India" in ans["answer_text"] or "Indian Oil" in ans["answer_text"]


def test_jio_competition_query_retains_routing():
    """Verifies that explicit competition queries for Jio fuel still route correctly."""
    from src.ai.nl_query_engine import question_cache
    question_cache.clear()

    ans = AIEnergyMarketAnalyst.answer_question(
        question="which company can easily compete jio fuel",
        session_id="test_jio_competition_session",
        bypass_session_limits=True,
        allow_free_autonomous=True
    )
    assert ans["is_fallback"] is False
    assert "Jio-bp" in ans["answer_text"]
    assert "Competitive Market Intelligence" in ans["answer_text"]


def test_ai_modal_translation_fallbacks_never_return_raw_keys():
    """Verifies that all ai_* and home_btn_f9_* keys resolve cleanly and never return raw string keys."""
    from src.localization.i18n import t

    test_keys = [
        "ai_card_title", "ai_context_prefix", "ai_context_suffix",
        "ai_status_active", "ai_status_quota_reached", "ai_status_blocked",
        "ai_suggested_queries", "ai_tab_type", "ai_tab_voice",
        "ai_input_placeholder", "ai_btn_ask", "ai_engine_verified",
        "home_btn_f9_studio", "home_btn_f9_dash"
    ]
    for key in test_keys:
        for lang in ["en", "hi", "es", "fr"]:
            res = t(key, lang, rem_q=3, reset_str="24 hours")
            assert res != key, f"Translation key '{key}' returned raw string in language '{lang}'"
            assert len(res) > 0
