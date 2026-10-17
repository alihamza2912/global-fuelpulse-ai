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
    assert refresh_result["total_articles"] >= 6
    assert isinstance(refresh_result["refreshed_at"], str)
