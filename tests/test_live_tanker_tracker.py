"""
Unit tests for Live Maritime Fuel Tanker Tracker and AIS Telemetry Engine.
"""

import pytest
from src.analytics.live_tanker_tracker import LiveTankerTracker


def test_get_fleet_telemetry_returns_vessels():
    fleet = LiveTankerTracker.get_fleet_telemetry()
    assert len(fleet) >= 10
    v = fleet[0]
    assert "vessel_id" in v
    assert "name" in v
    assert "imo" in v
    assert "speed_knots" in v
    assert "remaining_distance_nm" in v
    assert "days_remaining" in v
    assert "eta_human" in v
    assert "cargo_value_usd" in v
    assert v["cargo_value_usd"] > 0


def test_eta_and_distance_math():
    fleet = LiveTankerTracker.get_fleet_telemetry()
    for v in fleet:
        assert v["total_distance_nm"] > 0
        assert v["sailed_distance_nm"] >= 0
        assert v["remaining_distance_nm"] >= 0
        assert v["speed_knots"] > 0
        expected_hours = v["remaining_distance_nm"] / v["speed_knots"]
        assert pytest.approx(v["hours_remaining"], rel=1e-2) == expected_hours
        assert v["days_remaining"] >= 0
        assert 0 <= v["progress_pct"] <= 100


def test_cargo_filtering():
    crude_fleet = LiveTankerTracker.get_fleet_telemetry(cargo_filter="crude")
    assert len(crude_fleet) > 0
    for v in crude_fleet:
        assert v["cargo_type"] == "crude"

    product_fleet = LiveTankerTracker.get_fleet_telemetry(cargo_filter="product")
    assert len(product_fleet) > 0
    for v in product_fleet:
        assert v["cargo_type"] == "product"

    lng_fleet = LiveTankerTracker.get_fleet_telemetry(cargo_filter="lng")
    assert len(lng_fleet) > 0
    for v in lng_fleet:
        assert v["cargo_type"] == "lng"


def test_search_filtering():
    res = LiveTankerTracker.get_fleet_telemetry(search_query="Maran")
    assert len(res) == 1
    assert res[0]["name"] == "Maran Canopus"

    res_imo = LiveTankerTracker.get_fleet_telemetry(search_query="9235268")
    assert len(res_imo) == 1
    assert res_imo[0]["name"] == "TI Europe"


def test_summary_kpis():
    kpis = LiveTankerTracker.get_summary_kpis()
    assert kpis["active_vessels"] >= 10
    assert kpis["total_barrels_at_sea"] > 10_000_000
    assert kpis["total_cargo_value_usd"] > 500_000_000
    assert kpis["avg_fleet_speed_knots"] > 10.0


def test_get_vessel_by_id():
    v = LiveTankerTracker.get_vessel_by_id("TNK-01")
    assert v is not None
    assert v["name"] == "Maran Canopus"
    assert len(v["waypoints"]) >= 2
    for wp in v["waypoints"]:
        assert len(wp) == 2
        assert -90 <= wp[0] <= 90
        assert -180 <= wp[1] <= 180


def test_dynamic_dead_reckoning_motion():
    from datetime import datetime, timezone
    base_v = LiveTankerTracker.VESSELS[0]
    now = datetime.now(timezone.utc)
    dyn_v = LiveTankerTracker.compute_dynamic_waypoint_position(base_v, now)
    assert "current_lat" in dyn_v
    assert "current_lon" in dyn_v
    assert -90.0 <= dyn_v["current_lat"] <= 90.0
    assert -180.0 <= dyn_v["current_lon"] <= 180.0
    assert 0 <= dyn_v["heading_deg"] <= 360


def test_open_ais_connector_and_live_fleet():
    from src.connectors.open_ais_connector import fetch_live_open_ais_tankers
    live_tankers = fetch_live_open_ais_tankers()
    assert isinstance(live_tankers, list)
    if live_tankers:
        t = live_tankers[0]
        assert "vessel_id" in t
        assert "current_lat" in t
        assert "current_lon" in t
        assert "speed_knots" in t
        assert t.get("is_real_live_ais") is True


def test_combined_fleet_modes():
    strategic = LiveTankerTracker.get_combined_fleet(fleet_source="strategic")
    assert len(strategic) >= 10
    
    live_ais = LiveTankerTracker.get_combined_fleet(fleet_source="live_open_ais")
    assert isinstance(live_ais, list)
    
    combined = LiveTankerTracker.get_combined_fleet(fleet_source="combined")
    assert len(combined) >= len(strategic)

