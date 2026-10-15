"""
Automated unit and integration tests for Global FuelPulse AI Master Story modules.
Validates Global Production Atlas, Indian Oil Company Intelligence (HPCL & OMCs),
and Indian Regional Consumption & Demand analytics.
"""

import pytest
import pandas as pd
from src.analytics.production_analytics import GlobalProductionAnalytics
from src.analytics.india_company_analytics import IndiaCompanyAnalytics
from src.analytics.india_demand_analytics import IndiaDemandAnalytics


def test_production_leaderboard_data():
    """Validates global crude oil production rankings, shares, and YoY calculations."""
    lb = GlobalProductionAnalytics.get_production_leaderboard()
    assert not lb.empty, "Production leaderboard should not be empty"
    assert "crude_prod_mbpd_2024" in lb.columns
    assert "share_of_global_pct" in lb.columns
    assert "yoy_change_mbpd" in lb.columns

    # Verify top producer is USA and exceeds 13 mbpd
    top = lb.iloc[0]
    assert top["country_iso3"] == "USA"
    assert top["crude_prod_mbpd_2024"] >= 13.0

    # Verify sum of regional shares is logically bounded
    reg = GlobalProductionAnalytics.get_regional_production_shares()
    assert len(reg) >= 5, "Should have at least 5 reporting energy regions"
    total_share = reg["share_pct"].sum()
    assert 99.0 <= total_share <= 101.0, f"Regional shares should sum to ~100%, got {total_share}"

    # Verify OPEC vs non-OPEC split
    opec_data = GlobalProductionAnalytics.get_opec_vs_non_opec_breakdown()
    assert opec_data["total_tracked_mbpd"] > 65.0
    assert opec_data["opec_plus_share_pct"] > 45.0


def test_india_company_hpcl_and_omc_peers():
    """Validates HPCL FY2024-25 operating dossier and OMC peer comparison metrics."""
    hpcl = IndiaCompanyAnalytics.get_hpcl_overview()
    assert hpcl["company_name"].startswith("Hindustan Petroleum")
    assert hpcl["headline_financials"]["revenue_inr_crore"] > 400000.0
    assert hpcl["headline_financials"]["profit_after_tax_pat_inr_crore"] > 10000.0
    assert hpcl["refining_operations"]["total_crude_throughput_mmt"] > 20.0
    assert hpcl["refining_operations"]["average_grm_usd_per_barrel"] > 5.0
    assert hpcl["marketing_and_logistics"]["retail_outlets_count"] > 20000

    # Peer benchmark
    omc_df = IndiaCompanyAnalytics.get_omc_peer_benchmark()
    assert len(omc_df) == 3, "Should include IOCL, BPCL, and HPCL"
    assert "IOCL" in omc_df["company_code"].values
    assert "BPCL" in omc_df["company_code"].values
    assert "HPCL" in omc_df["company_code"].values

    # Product sales breakdown
    sales_df = IndiaCompanyAnalytics.get_hpcl_sales_breakdown()
    assert not sales_df.empty
    assert "High-Speed Diesel (HSD)" in sales_df["product"].values


def test_india_demand_and_regional_consumption():
    """Validates PPAC national product consumption and regional demand shares."""
    prod_demand = IndiaDemandAnalytics.get_national_product_consumption()
    assert not prod_demand.empty
    assert "consumption_mmt" in prod_demand.columns

    # Verify Diesel (HSD) is the single largest petroleum product consumed
    top_prod = prod_demand.sort_values("consumption_mmt", ascending=False).iloc[0]
    assert top_prod["product_code"] == "HSD"
    assert top_prod["consumption_mmt"] > 85.0

    # Regional demand shares
    reg_demand = IndiaDemandAnalytics.get_regional_demand_shares()
    assert len(reg_demand) == 4, "Should have 4 major regions (North, West, South, East)"
    total_reg_pct = reg_demand["consumption_share_pct"].sum()
    assert 99.0 <= total_reg_pct <= 101.0, f"Regional demand shares should sum to ~100%, got {total_reg_pct}"

    # Demand summary
    summary = IndiaDemandAnalytics.get_demand_summary()
    assert summary["total_consumption_mmt"] > 220.0
    assert summary["hsd_share_pct"] > 35.0
