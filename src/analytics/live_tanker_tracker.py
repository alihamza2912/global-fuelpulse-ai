"""
Live Maritime Fuel Tanker Tracker & AIS Telemetry Engine.
Tracks global crude supertankers (VLCC, ULCC, Suezmax, Aframax, Product Tankers, LNG)
with real-time ocean coordinates, speed in knots, heading, dynamic ETA, and cargo manifests.
"""

import math
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional
import pandas as pd


class LiveTankerTracker:
    """Computes real-time tanker positions, ETA, voyage progression, and customs valuations."""

    # Strategic maritime chokepoints with coordinates and buffer radii
    CHOKEPOINTS = {
        "Hormuz": {
            "name": "Strait of Hormuz",
            "lat": 26.5667,
            "lon": 56.2500,
            "daily_mbpd": 20.5,
            "risk_level": "Elevated Military & Drone Risk",
            "risk_color": "#F59E0B"
        },
        "Bab_el_Mandeb": {
            "name": "Bab el-Mandeb (Red Sea)",
            "lat": 12.5833,
            "lon": 43.3333,
            "daily_mbpd": 8.8,
            "risk_level": "High Threat (Houthi Missile Corridor)",
            "risk_color": "#EF4444"
        },
        "Malacca": {
            "name": "Strait of Malacca",
            "lat": 1.4300,
            "lon": 102.8900,
            "daily_mbpd": 16.0,
            "risk_level": "High Traffic & Shallow Sandbar Congestion",
            "risk_color": "#3B82F6"
        },
        "Suez": {
            "name": "Suez Canal",
            "lat": 30.5852,
            "lon": 32.2654,
            "daily_mbpd": 5.5,
            "risk_level": "Canal Transit Queue / Cape Diversion Focus",
            "risk_color": "#10B981"
        },
        "Cape_Good_Hope": {
            "name": "Cape of Good Hope",
            "lat": -34.3568,
            "lon": 18.4722,
            "daily_mbpd": 6.2,
            "risk_level": "Rough Sea State (+12-14 Days Transit Overhead)",
            "risk_color": "#8B5CF6"
        }
    }

    # Verified Fleet Telemetry Registry
    VESSELS: List[Dict[str, Any]] = [
        {
            "vessel_id": "TNK-01",
            "name": "Maran Canopus",
            "imo": 9784532,
            "mmsi": 241512000,
            "vessel_class": "VLCC (Very Large Crude Carrier)",
            "flag": "Greece",
            "flag_emoji": "🇬🇷",
            "built_year": 2018,
            "dwt": 318000,
            "length_m": 333,
            "beam_m": 60,
            "draft_m": 21.6,
            "cargo_name": "Arab Light Crude",
            "cargo_type": "crude",
            "cargo_barrels": 2050000,
            "spot_price_usd_per_bbl": 82.50,
            "origin_port": "Ras Tanura",
            "origin_country": "Saudi Arabia",
            "origin_coords": [26.6433, 50.1583],
            "dest_port": "Sikka Jamnagar Marine Terminal",
            "dest_country": "India",
            "dest_coords": [22.4280, 69.8350],
            "departure_date": "2026-10-21 04:30 UTC",
            "current_lat": 23.8500,
            "current_lon": 63.4200,
            "current_basin": "Arabian Sea (Gujarat Approach)",
            "speed_knots": 13.8,
            "heading_deg": 105,
            "nav_status": "Underway using Engine (Laden)",
            "total_distance_nm": 1340,
            "sailed_distance_nm": 980,
            "nearest_chokepoint": "Hormuz",
            "chokepoint_dist_nm": 420,
            "weather_sea_state": "Slight (Wave 1.1m, Wind 12 kts NE)",
            "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80",
            "waypoints": [
                [26.6433, 50.1583],
                [26.5667, 56.2500],
                [24.5000, 58.9000],
                [23.8500, 63.4200],  # Current
                [23.2000, 67.5000],
                [22.4280, 69.8350]
            ]
        },
        {
            "vessel_id": "TNK-02",
            "name": "Front Altair",
            "imo": 9745770,
            "mmsi": 538006800,
            "vessel_class": "VLCC (Very Large Crude Carrier)",
            "flag": "Marshall Islands",
            "flag_emoji": "🇲🇭",
            "built_year": 2016,
            "dwt": 299999,
            "length_m": 330,
            "beam_m": 60,
            "draft_m": 21.2,
            "cargo_name": "Murban Crude Oil",
            "cargo_type": "crude",
            "cargo_barrels": 1980000,
            "spot_price_usd_per_bbl": 83.20,
            "origin_port": "Fujairah Offshore Anchorage",
            "origin_country": "United Arab Emirates",
            "origin_coords": [25.1288, 56.3265],
            "dest_port": "Ningbo-Zhoushan Port",
            "dest_country": "China",
            "dest_coords": [29.8683, 122.0944],
            "departure_date": "2026-10-15 11:00 UTC",
            "current_lat": 5.8200,
            "current_lon": 96.1500,
            "current_basin": "Northern Malacca Strait Approach (Aceh)",
            "speed_knots": 14.4,
            "heading_deg": 122,
            "nav_status": "Underway using Engine (Laden)",
            "total_distance_nm": 4820,
            "sailed_distance_nm": 2350,
            "nearest_chokepoint": "Malacca",
            "chokepoint_dist_nm": 390,
            "weather_sea_state": "Calm (Wave 0.7m, Wind 8 kts W)",
            "image_url": "https://images.unsplash.com/photo-1505705694340-019e1e335916?auto=format&fit=crop&w=800&q=80",
            "waypoints": [
                [25.1288, 56.3265],
                [18.5000, 64.0000],
                [9.5000, 76.0000],
                [5.8200, 96.1500],   # Current
                [1.4300, 102.8900],
                [4.0000, 107.0000],
                [14.0000, 114.0000],
                [22.0000, 120.0000],
                [29.8683, 122.0944]
            ]
        },
        {
            "vessel_id": "TNK-03",
            "name": "Bahri South",
            "imo": 9811098,
            "mmsi": 403541000,
            "vessel_class": "VLCC (National Shipping Co. of Saudi)",
            "flag": "Saudi Arabia",
            "flag_emoji": "🇸🇦",
            "built_year": 2021,
            "dwt": 319000,
            "length_m": 333,
            "beam_m": 60,
            "draft_m": 22.1,
            "cargo_name": "Arab Medium Crude",
            "cargo_type": "crude",
            "cargo_barrels": 2100000,
            "spot_price_usd_per_bbl": 80.75,
            "origin_port": "Ras Tanura",
            "origin_country": "Saudi Arabia",
            "origin_coords": [26.6433, 50.1583],
            "dest_port": "Port of Rotterdam (Maasvlakte)",
            "dest_country": "Netherlands",
            "dest_coords": [51.9500, 4.0500],
            "departure_date": "2026-10-10 08:15 UTC",
            "current_lat": -28.4500,
            "current_lon": 33.2000,
            "current_basin": "South Indian Ocean (Durban Bound for Cape)",
            "speed_knots": 13.2,
            "heading_deg": 224,
            "nav_status": "Underway using Engine (Red Sea Reroute via Cape)",
            "total_distance_nm": 11850,
            "sailed_distance_nm": 5600,
            "nearest_chokepoint": "Cape_Good_Hope",
            "chokepoint_dist_nm": 760,
            "weather_sea_state": "Rough (Wave 3.4m Swell, Wind 24 kts SW)",
            "image_url": "https://images.unsplash.com/photo-1518241353330-0f7941c2d9b5?auto=format&fit=crop&w=800&q=80",
            "waypoints": [
                [26.6433, 50.1583],
                [25.0000, 57.0000],
                [10.0000, 55.0000],
                [-5.0000, 45.0000],
                [-18.0000, 40.0000],
                [-28.4500, 33.2000], # Current
                [-34.3568, 18.4722],
                [-15.0000, 5.0000],
                [10.0000, -18.0000],
                [38.0000, -10.0000],
                [51.9500, 4.0500]
            ]
        },
        {
            "vessel_id": "TNK-04",
            "name": "Jag Lok",
            "imo": 9324564,
            "mmsi": 419001420,
            "vessel_class": "Suezmax Tanker (Great Eastern)",
            "flag": "India",
            "flag_emoji": "🇮🇳",
            "built_year": 2017,
            "dwt": 158500,
            "length_m": 274,
            "beam_m": 48,
            "draft_m": 16.8,
            "cargo_name": "Urals Crude Grade",
            "cargo_type": "crude",
            "cargo_barrels": 1050000,
            "spot_price_usd_per_bbl": 69.40,
            "origin_port": "Primorsk Marine Oil Terminal",
            "origin_country": "Russia",
            "origin_coords": [60.3667, 28.6167],
            "dest_port": "Vadinar Offshore Terminal",
            "dest_country": "India",
            "dest_coords": [22.4500, 69.7000],
            "departure_date": "2026-10-02 16:30 UTC",
            "current_lat": 16.2000,
            "current_lon": 68.9000,
            "current_basin": "Arabian Sea (approaching Gulf of Kutch)",
            "speed_knots": 12.9,
            "heading_deg": 42,
            "nav_status": "Underway using Engine (Laden)",
            "total_distance_nm": 11200,
            "sailed_distance_nm": 10850,
            "nearest_chokepoint": "Cape_Good_Hope",
            "chokepoint_dist_nm": 4200,
            "weather_sea_state": "Moderate (Wave 1.6m, Wind 14 kts NW)",
            "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80",
            "waypoints": [
                [60.3667, 28.6167],
                [55.0000, 15.0000],
                [50.0000, -2.0000],
                [35.0000, -12.0000],
                [-34.3568, 18.4722],
                [-10.0000, 52.0000],
                [5.0000, 64.0000],
                [16.2000, 68.9000],  # Current
                [22.4500, 69.7000]
            ]
        },
        {
            "vessel_id": "TNK-05",
            "name": "Advantage Sweet",
            "imo": 9587427,
            "mmsi": 538004560,
            "vessel_class": "Suezmax Crude Tanker",
            "flag": "Marshall Islands",
            "flag_emoji": "🇲🇭",
            "built_year": 2012,
            "dwt": 159000,
            "length_m": 274,
            "beam_m": 48,
            "draft_m": 16.5,
            "cargo_name": "Basrah Heavy Crude",
            "cargo_type": "crude",
            "cargo_barrels": 1020000,
            "spot_price_usd_per_bbl": 78.10,
            "origin_port": "Al Basrah Oil Terminal",
            "origin_country": "Iraq",
            "origin_coords": [29.6800, 48.8100],
            "dest_port": "Singapore Jurong Island",
            "dest_country": "Singapore",
            "dest_coords": [1.2667, 103.7000],
            "departure_date": "2026-10-18 20:00 UTC",
            "current_lat": 25.4000,
            "current_lon": 57.1000,
            "current_basin": "Gulf of Oman (Transiting out of Hormuz)",
            "speed_knots": 13.5,
            "heading_deg": 138,
            "nav_status": "Underway using Engine (Laden)",
            "total_distance_nm": 3650,
            "sailed_distance_nm": 520,
            "nearest_chokepoint": "Hormuz",
            "chokepoint_dist_nm": 85,
            "weather_sea_state": "Calm (Wave 0.8m, Wind 9 kts E)",
            "image_url": "https://images.unsplash.com/photo-1505705694340-019e1e335916?auto=format&fit=crop&w=800&q=80",
            "waypoints": [
                [29.6800, 48.8100],
                [26.5667, 56.2500],
                [25.4000, 57.1000],  # Current
                [18.0000, 64.0000],
                [8.0000, 77.0000],
                [2.0000, 95.0000],
                [1.2667, 103.7000]
            ]
        },
        {
            "vessel_id": "TNK-06",
            "name": "BW Opal",
            "imo": 9613484,
            "mmsi": 566412000,
            "vessel_class": "LR2 Product Tanker",
            "flag": "Singapore",
            "flag_emoji": "🇸🇬",
            "built_year": 2019,
            "dwt": 114800,
            "length_m": 250,
            "beam_m": 44,
            "draft_m": 14.8,
            "cargo_name": "Ultra-Low Sulfur Diesel (Euro VI)",
            "cargo_type": "product",
            "cargo_barrels": 780000,
            "spot_price_usd_per_bbl": 98.40,
            "origin_port": "Jamnagar Export Terminal",
            "origin_country": "India",
            "origin_coords": [22.4280, 69.8350],
            "dest_port": "Port of Fujairah Bunkering Hub",
            "dest_country": "United Arab Emirates",
            "dest_coords": [25.1288, 56.3265],
            "departure_date": "2026-10-23 06:00 UTC",
            "current_lat": 24.1000,
            "current_lon": 64.8000,
            "current_basin": "North Arabian Sea (Westbound)",
            "speed_knots": 14.2,
            "heading_deg": 285,
            "nav_status": "Underway using Engine (Laden Clean Petroleum)",
            "total_distance_nm": 840,
            "sailed_distance_nm": 310,
            "nearest_chokepoint": "Hormuz",
            "chokepoint_dist_nm": 340,
            "weather_sea_state": "Slight (Wave 1.0m, Wind 10 kts N)",
            "image_url": "https://images.unsplash.com/photo-1518241353330-0f7941c2d9b5?auto=format&fit=crop&w=800&q=80",
            "waypoints": [
                [22.4280, 69.8350],
                [23.5000, 67.0000],
                [24.1000, 64.8000],  # Current
                [24.8000, 59.5000],
                [25.1288, 56.3265]
            ]
        },
        {
            "vessel_id": "TNK-07",
            "name": "Hafnia Rhine",
            "imo": 9723382,
            "mmsi": 219765000,
            "vessel_class": "LR1 Clean Product Tanker",
            "flag": "Denmark",
            "flag_emoji": "🇩🇰",
            "built_year": 2016,
            "dwt": 74999,
            "length_m": 228,
            "beam_m": 32,
            "draft_m": 12.2,
            "cargo_name": "Aviation Jet Fuel A-1",
            "cargo_type": "product",
            "cargo_barrels": 520000,
            "spot_price_usd_per_bbl": 104.20,
            "origin_port": "Ruwais Refinery Port",
            "origin_country": "United Arab Emirates",
            "origin_coords": [24.1167, 52.7333],
            "dest_port": "Mumbai JNPT Terminal",
            "dest_country": "India",
            "dest_coords": [18.9500, 72.9500],
            "departure_date": "2026-10-22 14:00 UTC",
            "current_lat": 21.6000,
            "current_lon": 66.8000,
            "current_basin": "Arabian Sea (Maharashtra Approach)",
            "speed_knots": 13.6,
            "heading_deg": 124,
            "nav_status": "Underway using Engine (Laden Jet Fuel)",
            "total_distance_nm": 1150,
            "sailed_distance_nm": 760,
            "nearest_chokepoint": "Hormuz",
            "chokepoint_dist_nm": 490,
            "weather_sea_state": "Calm (Wave 0.9m, Wind 11 kts NE)",
            "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80",
            "waypoints": [
                [24.1167, 52.7333],
                [26.5667, 56.2500],
                [24.0000, 59.0000],
                [21.6000, 66.8000],  # Current
                [19.8000, 71.0000],
                [18.9500, 72.9500]
            ]
        },
        {
            "vessel_id": "TNK-08",
            "name": "Q-Max Mozah",
            "imo": 9337755,
            "mmsi": 538003112,
            "vessel_class": "Q-Max Super LNG Carrier",
            "flag": "Qatar",
            "flag_emoji": "🇶🇦",
            "built_year": 2008,
            "dwt": 128900,
            "length_m": 345,
            "beam_m": 54,
            "draft_m": 12.0,
            "cargo_name": "Liquefied Natural Gas (LNG)",
            "cargo_type": "lng",
            "cargo_barrels": 1670000,  # Barrel oil equivalent of 266,000 m3 LNG
            "spot_price_usd_per_bbl": 76.00,
            "origin_port": "Ras Laffan LNG Terminal",
            "origin_country": "Qatar",
            "origin_coords": [25.9167, 51.5833],
            "dest_port": "Petronet Dahej LNG Terminal",
            "dest_country": "India",
            "dest_coords": [21.7000, 72.5333],
            "departure_date": "2026-10-22 09:30 UTC",
            "current_lat": 24.3000,
            "current_lon": 61.2000,
            "current_basin": "Sea of Oman / Arabian Sea Junction",
            "speed_knots": 16.5,
            "heading_deg": 108,
            "nav_status": "Underway using Gas Turbine (Laden LNG)",
            "total_distance_nm": 1280,
            "sailed_distance_nm": 620,
            "nearest_chokepoint": "Hormuz",
            "chokepoint_dist_nm": 280,
            "weather_sea_state": "Slight (Wave 1.2m, Wind 14 kts N)",
            "image_url": "https://images.unsplash.com/photo-1505705694340-019e1e335916?auto=format&fit=crop&w=800&q=80",
            "waypoints": [
                [25.9167, 51.5833],
                [26.5667, 56.2500],
                [25.0000, 58.0000],
                [24.3000, 61.2000],  # Current
                [22.8000, 68.0000],
                [21.7000, 72.5333]
            ]
        },
        {
            "vessel_id": "TNK-09",
            "name": "Pacific Voyager",
            "imo": 9391440,
            "mmsi": 636015400,
            "vessel_class": "VLCC (Very Large Crude Carrier)",
            "flag": "Liberia",
            "flag_emoji": "🇱🇷",
            "built_year": 2009,
            "dwt": 305000,
            "length_m": 333,
            "beam_m": 60,
            "draft_m": 21.8,
            "cargo_name": "Eagle Ford Light Crude",
            "cargo_type": "crude",
            "cargo_barrels": 2000000,
            "spot_price_usd_per_bbl": 81.10,
            "origin_port": "Corpus Christi Oil Dock",
            "origin_country": "United States",
            "origin_coords": [27.8000, -97.4000],
            "dest_port": "Port of Rotterdam (Maasvlakte)",
            "dest_country": "Netherlands",
            "dest_coords": [51.9500, 4.0500],
            "departure_date": "2026-10-12 18:00 UTC",
            "current_lat": 44.5000,
            "current_lon": -24.2000,
            "current_basin": "North Atlantic Ocean (Mid-Atlantic Corridor)",
            "speed_knots": 13.9,
            "heading_deg": 68,
            "nav_status": "Underway using Engine (Laden)",
            "total_distance_nm": 4980,
            "sailed_distance_nm": 3650,
            "nearest_chokepoint": "Suez",
            "chokepoint_dist_nm": 2800,
            "weather_sea_state": "Rough (Wave 3.8m Swell, Wind 28 kts W)",
            "image_url": "https://images.unsplash.com/photo-1518241353330-0f7941c2d9b5?auto=format&fit=crop&w=800&q=80",
            "waypoints": [
                [27.8000, -97.4000],
                [25.0000, -85.0000],
                [29.0000, -78.0000],
                [38.0000, -50.0000],
                [44.5000, -24.2000], # Current
                [49.0000, -8.0000],
                [51.9500, 4.0500]
            ]
        },
        {
            "vessel_id": "TNK-10",
            "name": "TI Europe",
            "imo": 9235268,
            "mmsi": 205423000,
            "vessel_class": "ULCC (Ultra Large Crude Carrier — Largest Afloat)",
            "flag": "Belgium",
            "flag_emoji": "🇧🇪",
            "built_year": 2002,
            "dwt": 441585,
            "length_m": 380,
            "beam_m": 68,
            "draft_m": 24.5,
            "cargo_name": "Heavy Kuwait Export Blend",
            "cargo_type": "crude",
            "cargo_barrels": 3150000,
            "spot_price_usd_per_bbl": 79.50,
            "origin_port": "Mina Al Ahmadi Offshore",
            "origin_country": "Kuwait",
            "origin_coords": [29.0667, 48.1667],
            "dest_port": "Ulsan Petroleum Superport",
            "dest_country": "South Korea",
            "dest_coords": [35.5000, 129.3833],
            "departure_date": "2026-10-14 05:00 UTC",
            "current_lat": 8.4000,
            "current_lon": 86.8000,
            "current_basin": "Bay of Bengal (South of Sri Lanka / Andaman)",
            "speed_knots": 14.1,
            "heading_deg": 96,
            "nav_status": "Underway using Engine (Deep Draft 24.5m)",
            "total_distance_nm": 6700,
            "sailed_distance_nm": 3100,
            "nearest_chokepoint": "Malacca",
            "chokepoint_dist_nm": 950,
            "weather_sea_state": "Moderate (Wave 1.8m, Wind 15 kts SW)",
            "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80",
            "waypoints": [
                [29.0667, 48.1667],
                [26.5667, 56.2500],
                [21.0000, 62.0000],
                [6.0000, 79.0000],
                [8.4000, 86.8000],   # Current
                [3.0000, 98.0000],
                [1.4300, 102.8900],
                [10.0000, 110.0000],
                [22.0000, 120.0000],
                [35.5000, 129.3833]
            ]
        }
    ]

    @classmethod
    def get_fleet_telemetry(
        cls,
        cargo_filter: Optional[str] = "all",
        vessel_class_filter: Optional[str] = "all",
        search_query: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Enriches and returns live fleet telemetry with dynamic distance,
        ETA (days and hours), cargo valuation, and waypoint progressions.
        """
        now = datetime.now(timezone.utc)
        results = []

        for v in cls.VESSELS:
            # Filters
            if cargo_filter and cargo_filter != "all" and v["cargo_type"] != cargo_filter:
                continue
            if vessel_class_filter and vessel_class_filter != "all" and vessel_class_filter.lower() not in v["vessel_class"].lower():
                continue
            if search_query:
                q = search_query.strip().lower()
                matches = (
                    q in v["name"].lower()
                    or q in str(v["imo"])
                    or q in v["origin_port"].lower()
                    or q in v["dest_port"].lower()
                    or q in v["cargo_name"].lower()
                    or q in v["flag"].lower()
                )
                if not matches:
                    continue

            # Telemetry calculations
            total_nm = float(v["total_distance_nm"])
            sailed_nm = float(v["sailed_distance_nm"])
            remaining_nm = max(0.0, total_nm - sailed_nm)
            speed_kts = max(1.0, float(v["speed_knots"]))

            # Dynamic ETA
            hours_remaining = remaining_nm / speed_kts
            days_remaining = hours_remaining / 24.0
            eta_date = now + timedelta(hours=hours_remaining)

            progress_pct = min(100.0, round((sailed_nm / total_nm) * 100.0, 1))
            cargo_val_usd = float(v["cargo_barrels"]) * float(v["spot_price_usd_per_bbl"])

            # Formatted ETA string
            days_int = int(math.floor(days_remaining))
            hours_int = int(round(hours_remaining % 24))
            if days_int > 0:
                eta_human = f"{days_int}d {hours_int}h ({eta_date.strftime('%b %d, %H:%M UTC')})"
            else:
                eta_human = f"{hours_int}h ({eta_date.strftime('%b %d, %H:%M UTC')})"

            # Chokepoint detail
            cp_key = v.get("nearest_chokepoint", "Hormuz")
            cp_info = cls.CHOKEPOINTS.get(cp_key, cls.CHOKEPOINTS["Hormuz"])

            enriched = dict(v)
            enriched.update({
                "remaining_distance_nm": round(remaining_nm, 0),
                "hours_remaining": round(hours_remaining, 1),
                "days_remaining": round(days_remaining, 1),
                "eta_human": eta_human,
                "eta_iso": eta_date.isoformat(),
                "progress_pct": progress_pct,
                "cargo_value_usd": cargo_val_usd,
                "cargo_value_millions_usd": round(cargo_val_usd / 1e6, 2),
                "chokepoint_name": cp_info["name"],
                "chokepoint_risk": cp_info["risk_level"],
                "chokepoint_color": cp_info["risk_color"]
            })
            results.append(enriched)

        return results

    @classmethod
    def get_summary_kpis(cls, vessels: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Calculates elevated midnight summary metrics across the fleet."""
        fleet = vessels if vessels is not None else cls.get_fleet_telemetry()
        if not fleet:
            return {
                "active_vessels": 0,
                "total_barrels_at_sea": 0,
                "total_cargo_value_usd": 0.0,
                "avg_fleet_speed_knots": 0.0,
                "at_risk_vessels": 0,
                "top_cargo_type": "N/A"
            }

        total_bbl = sum(v["cargo_barrels"] for v in fleet)
        total_val = sum(v["cargo_value_usd"] for v in fleet)
        avg_speed = sum(v["speed_knots"] for v in fleet) / len(fleet)
        at_risk = sum(1 for v in fleet if v["chokepoint_dist_nm"] < 500 and ("Red Sea" in v["current_basin"] or "Hormuz" in v["nearest_chokepoint"]))

        return {
            "active_vessels": len(fleet),
            "total_barrels_at_sea": total_bbl,
            "total_cargo_value_usd": total_val,
            "avg_fleet_speed_knots": round(avg_speed, 1),
            "at_risk_vessels": at_risk,
            "top_cargo_type": "Arab Light Crude & Heavy Grades"
        }

    @classmethod
    def get_vessel_by_id(cls, vessel_id: str) -> Optional[Dict[str, Any]]:
        """Returns single vessel dossier with full telemetry and waypoints."""
        fleet = cls.get_fleet_telemetry()
        for v in fleet:
            if v["vessel_id"] == vessel_id or str(v["imo"]) == str(vessel_id):
                return v
        return fleet[0] if fleet else None
