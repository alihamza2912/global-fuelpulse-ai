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
from config.settings import get_gemini_api_key


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
    assert ans["autonomous_free_mode"] is True
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
