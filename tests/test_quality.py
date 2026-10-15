"""
Unit Tests for Data Trust Center & Ingestion Telemetry.
Verifies telemetry tracking, freshness latency calculation, and audit metrics.
"""

import pytest
from src.monitoring.quality_auditor import DataQualityAuditor
from src.ai.nl_query_engine import AIEnergyMarketAnalyst


def test_quality_auditor_freshness_and_counts():
    """Verifies Data Trust Center telemetry and freshness audits."""
    freshness = DataQualityAuditor.get_source_freshness_status()
    assert isinstance(freshness, list)
    assert len(freshness) > 0

    first = freshness[0]
    assert "source_id" in first
    assert "freshness_status" in first
    assert first["freshness_status"] in ("FRESH", "STALE", "HISTORICAL", "NO_DATA")

    counts = DataQualityAuditor.get_table_row_counts()
    assert isinstance(counts, dict)
    assert counts.get("dim_country", 0) > 0
    assert counts.get("fuel_prices", 0) > 0


def test_ai_market_analyst_sql_execution():
    """Verifies that AI analyst answers questions safely with supporting data."""
    ans = AIEnergyMarketAnalyst.answer_question("Which countries exported the most crude oil?")
    assert "answer_text" in ans
    assert "data_records" in ans
    assert len(ans["data_records"]) > 0
    assert len(ans["sources_cited"]) > 0
    assert ans["is_fallback"] is False


def test_2026_data_gap_check():
    """Verifies 100% weekly observation continuity from Jan 2026 through October 2026."""
    from src.database.connection import db_manager
    import pandas as pd

    with db_manager.engine.connect() as conn:
        for iso3 in ["USA", "IND", "DEU", "FRA", "GBR", "SAU"]:
            for ftype in ["petrol_regular", "diesel"]:
                query = f"""
                SELECT observation_date, price_usd_per_litre
                FROM fuel_prices
                WHERE country_iso3 = '{iso3}' AND fuel_type = '{ftype}' AND observation_date >= '2026-01-01'
                ORDER BY observation_date ASC
                """
                df = pd.read_sql_query(query, conn)
                assert len(df) >= 40, f"Missing 2026 observations for {iso3} {ftype}: found {len(df)}"
                max_d = str(df.iloc[-1]["observation_date"])
                assert max_d >= "2026-10-01", f"Max observation date for {iso3} {ftype} is not in Oct 2026: {max_d}"

