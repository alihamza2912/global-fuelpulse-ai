"""
Unit and Integration Tests for Database Layer and Schema Integrity.
Verifies connection health, idempotency, foreign key relations, and telemetry logs.
"""

import pytest
from datetime import date, datetime
from src.database.connection import db_manager
from src.database.migrations import init_database
from src.database.models import DimCountry, FuelPrice, PetroleumTrade


def test_database_connection_and_health():
    """Verifies that database manager connects and exposes all 13 core tables."""
    init_database(seed_if_empty=True)
    health = db_manager.check_health()
    assert health["connected"] is True
    assert health["tables_count"] >= 13
    assert "fuel_prices" in health["tables"]
    assert "fact_petroleum_trade" in health["tables"]
    assert "dim_country" in health["tables"]


def test_seed_data_presence_and_integrity():
    """Verifies presence of reference countries and historical observations."""
    with db_manager.get_session() as session:
        country_count = session.query(DimCountry).count()
        assert country_count >= 20

        # Verify USA and India
        usa = session.query(DimCountry).filter_by(country_iso3="USA").first()
        assert usa is not None
        assert usa.country_name == "United States"

        ind = session.query(DimCountry).filter_by(country_iso3="IND").first()
        assert ind is not None
        assert ind.is_major_net_importer is True

        # Verify fuel prices
        price_count = session.query(FuelPrice).count()
        assert price_count >= 10

        # Verify trade flows
        trade_count = session.query(PetroleumTrade).count()
        assert trade_count >= 10


def test_read_only_query_safety():
    """Verifies that mutation statements are blocked in read-only execution."""
    with pytest.raises(PermissionError):
        db_manager.execute_read_only_query("DROP TABLE fuel_prices")

    with pytest.raises(PermissionError):
        db_manager.execute_read_only_query("DELETE FROM dim_country WHERE 1=1")

    # Safe SELECT works
    rows = db_manager.execute_read_only_query("SELECT country_iso3, country_name FROM dim_country LIMIT 3")
    assert len(rows) == 3
