"""
Unit Tests for Analytical Calculations and Intelligence Metrics.
Verifies price change %, HHI supplier concentration, affordability, and supply shock simulation.
"""

import pytest
from src.transformations.normalizers import (
    convert_fuel_price_to_usd_per_litre,
    convert_trade_quantity_to_bpd,
    normalize_country_iso3
)
from src.analytics.price_analytics import FuelPriceAnalytics
from src.analytics.trade_analytics import PetroleumTradeAnalytics
from src.analytics.affordability import AffordabilityAnalytics
from src.analytics.shock_simulator import SupplyShockSimulator
from src.analytics.fuel_impact_score import FuelImpactScoreCalculator


def test_normalizers_and_currency_conversion():
    """Verifies unit and country conversions."""
    # Country ISO-3 resolution
    assert normalize_country_iso3("United States") == "USA"
    assert normalize_country_iso3("India") == "IND"
    assert normalize_country_iso3("Germany") == "DEU"
    assert normalize_country_iso3("KSA") == "SAU"

    # US Gallon to Litre USD conversion ($3.7854 per gallon = $1.0000 per litre)
    usd_litre = convert_fuel_price_to_usd_per_litre(price_local=3.785411784, currency="USD", unit="gallon")
    assert pytest.approx(usd_litre, 0.001) == 1.0000

    # Local currency to USD (e.g. INR 86.60 / L = $1.0000 / L)
    usd_litre_inr = convert_fuel_price_to_usd_per_litre(price_local=86.60, currency="INR", unit="litre")
    assert pytest.approx(usd_litre_inr, 0.01) == 1.0000


def test_price_change_calculation():
    """Verifies period-over-period absolute and percentage change calculations."""
    metrics = FuelPriceAnalytics.calculate_price_change_metrics("USA", "petrol_regular")
    assert metrics["current_price_usd"] is not None
    assert isinstance(metrics["absolute_change_usd"], float)
    assert isinstance(metrics["percentage_change"], float)


def test_hhi_supplier_concentration():
    """Verifies Herfindahl-Hirschman Index calculation and tiering."""
    hhi_res = PetroleumTradeAnalytics.calculate_supplier_concentration_hhi(
        importer_iso3="IND", product_category="crude_oil", period="2024"
    )
    assert "hhi_score" in hhi_res
    assert hhi_res["hhi_score"] >= 0.0
    assert hhi_res["hhi_score"] <= 10000.0
    assert hhi_res["risk_tier"] in (
        "Low Concentration (Diverse)", "Moderate Concentration",
        "High Concentration (High Exposure)", "Insufficient Bilateral Data"
    )


def test_affordability_analytics():
    """Verifies GDP per capita daily income proxy and tier categorization."""
    afford_res = AffordabilityAnalytics.calculate_country_affordability(
        country_iso3="IND", current_petrol_usd=1.09, gdp_per_capita_usd=2730.0
    )
    # Daily income proxy = 2730 / 365 = 7.479
    assert pytest.approx(afford_res["daily_income_proxy_usd"], 0.1) == 7.48
    # Percent of daily income = 1.09 / 7.48 * 100 = ~14.6%
    assert afford_res["percent_of_daily_income"] > 10.0
    assert "Severe" in afford_res["tier"]


def test_supply_shock_simulator_sensitivity():
    """Verifies sensitivity calculation under user-defined export reductions."""
    sim = SupplyShockSimulator.simulate_export_curtailment(
        exporter_iso3="SAU",
        target_importer_iso3="IND",
        export_reduction_pct=20.0,
        assumed_crude_price_delta_usd_per_bbl=15.0,
        monthly_fleet_fuel_consumption_litres=100000.0,
        baseline_retail_price_usd_per_litre=1.00
    )
    assert sim["export_reduction_pct"] == 20.0
    assert sim["volume_deficit_bpd"] > 0
    assert sim["scenario_retail_price_usd"] > sim["baseline_retail_price_usd"]
    assert sim["additional_monthly_fleet_cost_usd"] > 0
    assert len(sim["sensitivity_curve"]) >= 5


def test_fuel_impact_score():
    """Verifies composite Fuel Impact Score calculation."""
    fis_df = FuelImpactScoreCalculator.calculate_global_scores()
    assert not fis_df.empty
    assert "fuel_impact_score" in fis_df.columns
    assert "vulnerability_tier" in fis_df.columns
    # Check bounds (0 to 100)
    assert fis_df["fuel_impact_score"].min() >= 0.0
    assert fis_df["fuel_impact_score"].max() <= 100.0
