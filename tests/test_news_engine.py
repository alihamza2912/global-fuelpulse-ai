"""
Unit tests for GlobalNewsEngine (Live News, Maritime Chokepoints, Delhi Benchmarks).
"""

import pytest
from src.analytics.global_news_engine import GlobalNewsEngine

def test_news_feed_retrieval():
    news = GlobalNewsEngine.get_live_news_feed()
    assert isinstance(news, list)
    assert len(news) >= 6
    for item in news:
        assert "id" in item
        assert "headline" in item
        assert "summary" in item
        assert "impact" in item
        assert "metrics" in item
        assert isinstance(item["metrics"], dict)
        assert "key_takeaways" in item
        assert isinstance(item["key_takeaways"], list)

def test_category_filtering():
    hormuz_news = GlobalNewsEngine.get_live_news_feed(category="HORMUZ_MARITIME")
    assert len(hormuz_news) >= 2
    for item in hormuz_news:
        assert item["category"] == "HORMUZ_MARITIME"

    price_news = GlobalNewsEngine.get_live_news_feed(category="PRICE_TAX")
    assert len(price_news) >= 2
    for item in price_news:
        assert item["category"] == "PRICE_TAX"

def test_delhi_and_metro_benchmarks():
    benchmarks = GlobalNewsEngine.get_live_delhi_and_metro_benchmarks()
    assert "delhi" in benchmarks
    delhi = benchmarks["delhi"]
    assert delhi["petrol"] == 102.12
    assert delhi["diesel"] == 95.20
    assert delhi["tax_share_pct"] == 46.5
    assert "mumbai" in benchmarks
    assert "kolkata" in benchmarks
    assert "chennai" in benchmarks

def test_chokepoints_telemetry():
    chokepoints = GlobalNewsEngine.get_chokepoint_telemetry()
    assert isinstance(chokepoints, list)
    assert len(chokepoints) == 4
    names = [cp["name"] for cp in chokepoints]
    assert "Strait of Hormuz" in names
    assert "Bab el-Mandeb / Red Sea" in names
    assert "Strait of Malacca" in names
    assert "Suez Canal" in names

    hormuz = next(cp for cp in chokepoints if cp["name"] == "Strait of Hormuz")
    assert "20.8 mbpd" in hormuz["throughput"]
    assert "ELEVATED" in hormuz["status"]
    assert hormuz["status_color"] == "#EF4444"

def test_active_alerts_and_refresh():
    count = GlobalNewsEngine.get_active_alerts_count()
    assert count >= 4
    
    refresh_result = GlobalNewsEngine.refresh_news()
    assert refresh_result["status"] == "SUCCESS"
    assert refresh_result["total_articles"] >= 18
    assert isinstance(refresh_result["refreshed_at"], str)

def test_multilingual_chokepoints_telemetry():
    # Test Hindi
    hi_cps = GlobalNewsEngine.get_chokepoint_telemetry("hi")
    assert len(hi_cps) == 4
    hi_names = [cp["name"] for cp in hi_cps]
    assert "होर्मुज जलडमरूमध्य" in hi_names
    assert "बाब अल-मंदेब / लाल सागर" in hi_names
    assert "मलक्का जलडमरूमध्य" in hi_names
    assert "स्वेज नहर" in hi_names
    hi_hormuz = next(cp for cp in hi_cps if cp["name"] == "होर्मुज जलडमरूमध्य")
    assert "उच्च नौसैनिक गश्त" in hi_hormuz["status"]
    assert "ड्रोन" in hi_hormuz["key_risk"]
    assert "फुजैराह" in hi_hormuz["contingency"]

    # Test Spanish
    es_cps = GlobalNewsEngine.get_chokepoint_telemetry("es")
    es_names = [cp["name"] for cp in es_cps]
    assert "Estrecho de Ormuz" in es_names
    assert "Canal de Suez" in es_names

def test_expanded_live_news_catalog():
    news = GlobalNewsEngine.get_live_news_feed()
    assert len(news) >= 18
    for item in news:
        assert "timestamp" in item
        assert any(unit in item["timestamp"] for unit in ["mins ago", "hour", "hours", "Just now", "Live Wire"])


def test_news_globe_icon_svg():
    from src.ui_components import get_news_globe_icon_svg
    svg = get_news_globe_icon_svg(36)
    assert '<svg width="36" height="36"' in svg
    assert "NEWS" in svg
    assert "#38BDF8" in svg  # Cyan/sky blue globe sphere
    assert "#EF4444" in svg  # Red banner
    assert "#9F1239" in svg  # Crimson 3D ribbon back fold


def test_news_globe_icon_data_uri():
    from src.ui_components import get_news_globe_icon_data_uri
    uri = get_news_globe_icon_data_uri()
    assert uri.startswith("data:image/svg+xml,")
    assert "NEWS" in uri


def test_21_live_news_stories_and_headline_i18n():
    """Validates the 21-story news database and full headline i18n."""
    news = GlobalNewsEngine.get_live_news_feed()
    assert len(news) == 21, f"Expected 21 stories, found {len(news)}"
    
    # Check new 2026 stories
    ids = [n["id"] for n in news]
    assert "NEWS-2026-IN-SAUDI-SPR-19" in ids
    assert "NEWS-2026-MED-REFINERY-20" in ids
    assert "NEWS-2026-VLGC-LNG-21" in ids

    # Check headline localization across 18 languages for first story
    from src.localization.i18n import SUPPORTED_LANGUAGES
    for code in SUPPORTED_LANGUAGES:
        localized_feed = GlobalNewsEngine.get_live_news_feed(lang=code)
        assert len(localized_feed) == 21
        first_headline = localized_feed[0]["headline"]
        assert len(first_headline) > 0


def test_all_18_languages_chokepoints_telemetry():
    """Validates chokepoint telemetry localization across all 18 supported languages."""
    from src.localization.i18n import SUPPORTED_LANGUAGES
    for code in SUPPORTED_LANGUAGES:
        cps = GlobalNewsEngine.get_chokepoint_telemetry(code)
        assert len(cps) == 4
        for cp in cps:
            assert len(cp["name"]) > 0
            assert len(cp["status"]) > 0
            assert len(cp["key_risk"]) > 0
            assert len(cp["contingency"]) > 0



