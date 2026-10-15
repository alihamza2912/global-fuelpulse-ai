"""
Unit and Integration Tests for External Data Source Connectors.
Verifies API response parsing, benchmark fallbacks, schema validations, and network error handling.
"""

import pytest
from datetime import date
from src.ingestion.fuel_prices.eia_fuel_connector import EIAFuelPriceConnector
from src.ingestion.fuel_prices.ppac_india_connector import PPACIndiaConnector
from src.ingestion.fuel_prices.ec_oil_bulletin import ECOilBulletinConnector
from src.ingestion.fuel_prices.globalpetrolprices import GlobalPetrolPricesConnector
from src.ingestion.petroleum_trade.un_comtrade_connector import UNComtradeConnector
from src.ingestion.petroleum_trade.eia_trade_connector import EIATradeConnector
from src.transformations.validators import validate_fuel_price_record, validate_trade_record


def test_eia_fuel_price_connector_schema_and_transformation():
    """Verifies US EIA fuel price connector fetches and transforms weekly series."""
    connector = EIAFuelPriceConnector()
    raw = connector.fetch_raw_data()
    assert isinstance(raw, list)
    assert len(raw) > 0

    assert connector.validate_schema(raw) is True

    transformed = connector.transform_records(raw)
    assert len(transformed) > 0
    first = transformed[0]
    assert first["country_iso3"] == "USA"
    assert first["fuel_type"] in ("petrol_regular", "diesel")
    assert first["price_usd_per_litre"] > 0.40
    assert first["price_usd_per_litre"] < 2.00
    assert isinstance(first["observation_date"], date)


def test_ppac_india_connector_transformation():
    """Verifies India PPAC daily metro connector transforms Delhi/Mumbai records."""
    connector = PPACIndiaConnector()
    raw = connector.fetch_raw_data()
    assert isinstance(raw, list)
    assert len(raw) > 0

    transformed = connector.transform_records(raw)
    assert len(transformed) > 0
    # Check that Delhi is mapped to IND_DEL
    delhi_records = [r for r in transformed if r["location_id"] == "IND_DEL"]
    assert len(delhi_records) > 0
    assert delhi_records[0]["country_iso3"] == "IND"
    assert delhi_records[0]["currency_local"] == "INR"


def test_un_comtrade_connector_crude_and_refined():
    """Verifies UN Comtrade connector transforms HS 2709 (Crude) and 2710 (Refined)."""
    connector = UNComtradeConnector()
    raw = connector.fetch_raw_data()
    assert isinstance(raw, list)
    assert len(raw) > 0

    transformed = connector.transform_records(raw)
    assert len(transformed) > 0
    crude_records = [r for r in transformed if r["product_category"] == "crude_oil"]
    assert len(crude_records) > 0
    assert crude_records[0]["hs_code"] == "2709"
    assert crude_records[0]["quantity"] > 0


def test_record_validation_and_quarantine():
    """Verifies bad records are flagged with clear rejection reasons."""
    # Bad fuel price (negative price)
    bad_price = {
        "country_iso3": "USA",
        "fuel_type": "petrol_regular",
        "observation_date": date.today(),
        "price_local": -1.5,
        "price_usd_per_litre": -0.40
    }
    is_valid, reason = validate_fuel_price_record(bad_price)
    assert is_valid is False
    assert "Non-positive" in reason

    # Outlier price (> $20/litre)
    outlier_price = {
        "country_iso3": "USA",
        "fuel_type": "petrol_regular",
        "observation_date": date.today(),
        "price_local": 150.0,
        "price_usd_per_litre": 39.5
    }
    is_valid, reason = validate_fuel_price_record(outlier_price)
    assert is_valid is False
    assert "Unrealistic" in reason

    # Bad trade (negative quantity)
    bad_trade = {
        "reporting_period": "2024",
        "exporter_iso3": "SAU",
        "trade_direction": "export",
        "quantity": -5000
    }
    is_valid, reason = validate_trade_record(bad_trade)
    assert is_valid is False
    assert "Negative" in reason


def test_open_exchange_rate_connector_transformation():
    """Verifies OpenExchangeRateConnector transforms free open API FX payload."""
    from src.ingestion.exchange_rates.open_er_connector import OpenExchangeRateConnector
    connector = OpenExchangeRateConnector()
    raw = connector.fetch_raw_data()
    assert isinstance(raw, dict)
    assert connector.validate_schema(raw) is True

    records = connector.transform_records(raw)
    assert len(records) > 0
    currs = [r["currency_code"] for r in records]
    assert "EUR" in currs
    assert "INR" in currs
    assert "USD" in currs
    for r in records:
        assert r["rate_to_usd"] > 0
        assert isinstance(r["rate_date"], date)


def test_ec_oil_bulletin_connector_2026_series():
    """Verifies European Commission connector transforms 2026 weekly series for EU 5."""
    connector = ECOilBulletinConnector()
    raw = connector.fetch_raw_data()
    assert isinstance(raw, list)
    assert len(raw) >= 410

    transformed = connector.transform_records(raw)
    assert len(transformed) >= 410
    deu_records = [r for r in transformed if r["country_iso3"] == "DEU"]
    assert len(deu_records) >= 82
    assert deu_records[0]["currency_local"] == "EUR"
    assert deu_records[0]["price_usd_per_litre"] > 1.0


def test_pipeline_scheduler_lifecycle():
    """Verifies PipelineScheduler thread starts and stops gracefully."""
    from src.ingestion.scheduler import PipelineScheduler
    sched = PipelineScheduler(interval_seconds=3600)
    assert sched.is_running is False
    sched.start()
    assert sched.is_running is True
    sched.stop()
    assert sched.is_running is False

