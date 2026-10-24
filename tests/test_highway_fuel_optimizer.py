"""
Unit tests for Highway Fuel Trip & Cross-Border Arbitrage Optimizer Engine.
"""

import pytest
from src.analytics.highway_fuel_optimizer import HighwayFuelOptimizer

def test_engine_initialization_and_nodes():
    """Verifies that all nodes, vehicles, and preset corridors are properly structured."""
    assert len(HighwayFuelOptimizer.INDIA_NODES) >= 28
    assert len(HighwayFuelOptimizer.SAUDI_NODES) >= 8
    assert len(HighwayFuelOptimizer.UAE_NODES) >= 7
    assert len(HighwayFuelOptimizer.GCC_CROSS_BORDER_NODES) >= 6
    assert len(HighwayFuelOptimizer.VEHICLE_PROFILES) >= 5

def test_delhi_mumbai_freight_corridor_optimization():
    """Verifies optimization on India's primary freight artery (Delhi to Mumbai NH48)."""
    res = HighwayFuelOptimizer.optimize_trip(
        region="india",
        origin="Delhi",
        destination="Maharashtra",
        vehicle_type="commercial_truck_40t",
        fuel_type="diesel",
        selected_corridor_id="delhi_mumbai"
    )

    assert res["region"] == "india"
    assert res["total_distance_km"] == 1420
    assert res["currency_code"] == "INR"
    assert res["total_fuel_needed_l"] > 0
    assert res["financial_summary"]["net_savings"] >= 0
    assert len(res["waypoints"]) == 5
    assert len(res["refuel_schedule"]) == 5

    # Gujarat has low VAT and should be flagged as arbitrage fill
    guinea_stops = [s for s in res["refuel_schedule"] if s["location"] == "Gujarat"]
    assert len(guinea_stops) == 1
    # Verify Rajasthan high VAT is detected
    raj_stop = [s for s in res["refuel_schedule"] if s["location"] == "Rajasthan"][0]
    assert raj_stop["vat_pct"] == 31.0

def test_saudi_arabia_riyadh_jeddah_corridor():
    """Verifies Saudi Arabia Route 40 optimization."""
    res = HighwayFuelOptimizer.optimize_trip(
        region="saudi",
        origin="Riyadh",
        destination="Jeddah",
        vehicle_type="commercial_truck_40t",
        fuel_type="diesel",
        selected_corridor_id="riyadh_jeddah"
    )

    assert res["region"] == "saudi"
    assert res["currency_code"] == "SAR"
    assert res["total_distance_km"] == 950
    assert res["price_metrics"]["min_price"] == 1.15
    assert len(res["waypoints"]) >= 3

def test_uae_dubai_fujairah_corridor():
    """Verifies UAE Emirates optimization with petrol 98 and SUV."""
    res = HighwayFuelOptimizer.optimize_trip(
        region="uae",
        origin="Abu Dhabi",
        destination="Fujairah",
        vehicle_type="suv_4x4",
        fuel_type="petrol_98",
        selected_corridor_id="abudhabi_fujairah"
    )

    assert res["region"] == "uae"
    assert res["currency_code"] == "AED"
    assert res["total_distance_km"] == 260
    assert res["financial_summary"]["optimized_cost"] > 0

def test_gcc_cross_border_dubai_riyadh_arbitrage():
    """Verifies massive cross-border arbitrage between UAE and Saudi Arabia."""
    res = HighwayFuelOptimizer.optimize_trip(
        region="gcc_cross_border",
        origin="Dubai (UAE)",
        destination="Riyadh (Saudi Arabia)",
        vehicle_type="commercial_truck_40t",
        fuel_type="diesel",
        selected_corridor_id="dubai_riyadh"
    )

    assert res["region"] == "gcc_cross_border"
    assert res["total_distance_km"] == 1050
    assert res["financial_summary"]["net_savings"] > 0
    # KSA fuel is much cheaper than UAE fuel (~1.15 vs ~3.17 SAR equiv)
    assert res["price_metrics"]["price_spread"] > 1.0

def test_custom_city_routing_and_custom_tank():
    """Verifies custom city-to-city haversine routing with custom tank & mileage."""
    res = HighwayFuelOptimizer.optimize_trip(
        region="india",
        origin="Punjab",
        destination="Kerala",
        vehicle_type="sedan_hatchback",
        fuel_type="petrol",
        custom_tank_l=50.0,
        custom_kml=18.0
    )

    assert res["total_distance_km"] > 1500
    assert res["tank_capacity_l"] == 50.0
    assert res["mileage_kml"] == 18.0
    assert res["financial_summary"]["cost_per_km"] > 0
