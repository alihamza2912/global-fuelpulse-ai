"""
Global Fuel Supply Risk & Chokepoint Monitor.
Evaluates national import dependence, supplier concentration exposure, and maritime transit chokepoints.
"""

import pandas as pd
from typing import Dict, Any, List
from src.database.connection import db_manager
from src.analytics.trade_analytics import PetroleumTradeAnalytics

# Critical Global Maritime Petroleum Shipping Chokepoints
CHOKEPOINTS_REGISTRY = [
    {
        "name": "Strait of Hormuz",
        "region": "Middle East (Oman / Iran)",
        "coordinates": [26.5667, 56.2500],
        "daily_transit_volume_mbpd": 21.0,
        "share_of_global_seaborne_oil_pct": 21.0,
        "critical_suppliers": ["Saudi Arabia", "Iraq", "UAE", "Kuwait", "Qatar"],
        "primary_destination_corridor": "Asia-Pacific (China, India, Japan, South Korea)",
        "vulnerability_notes": "Single narrow shipping lane (2 miles wide each direction). No equivalent pipeline bypass capacity."
    },
    {
        "name": "Strait of Malacca",
        "region": "Southeast Asia (Malaysia / Indonesia / Singapore)",
        "coordinates": [4.2105, 100.5566],
        "daily_transit_volume_mbpd": 16.0,
        "share_of_global_seaborne_oil_pct": 16.0,
        "critical_suppliers": ["Middle Eastern Exporters", "West African Exporters"],
        "primary_destination_corridor": "East Asia (China, Japan, South Korea, Taiwan)",
        "vulnerability_notes": "Key conduit connecting Indian and Pacific Oceans. Prone to congestion and strategic bottleneck risks."
    },
    {
        "name": "Suez Canal & SUMED Pipeline",
        "region": "Egypt (Red Sea / Mediterranean)",
        "coordinates": [30.5852, 32.2654],
        "daily_transit_volume_mbpd": 8.8,
        "share_of_global_seaborne_oil_pct": 9.0,
        "critical_suppliers": ["Gulf Producers", "European Refiners", "Russia"],
        "primary_destination_corridor": "Europe / North America / Asia bilateral flows",
        "vulnerability_notes": "Critical shortcut avoiding Cape of Good Hope detour (~10-14 days additional transit)."
    },
    {
        "name": "Bab el-Mandeb",
        "region": "Horn of Africa / Arabian Peninsula (Yemen / Djibouti)",
        "coordinates": [12.5833, 43.3333],
        "daily_transit_volume_mbpd": 8.2,
        "share_of_global_seaborne_oil_pct": 8.5,
        "critical_suppliers": ["Middle East", "Asia-bound African Crude"],
        "primary_destination_corridor": "Red Sea / Suez Canal gateway",
        "vulnerability_notes": "High regional security risk; direct gateway into Suez Canal."
    },
    {
        "name": "Danish Straits & Turkish Straits",
        "region": "Europe / Black Sea",
        "coordinates": [41.1172, 29.0710],
        "daily_transit_volume_mbpd": 3.2,
        "share_of_global_seaborne_oil_pct": 3.5,
        "critical_suppliers": ["Russia", "Kazakhstan", "Azerbaijan"],
        "primary_destination_corridor": "Mediterranean & Global markets",
        "vulnerability_notes": "Constrained maritime passages connecting Black Sea to Mediterranean."
    },
    {
        "name": "Panama Canal",
        "region": "Central America (Panama)",
        "coordinates": [9.0800, -79.6800],
        "daily_transit_volume_mbpd": 1.2,
        "share_of_global_seaborne_oil_pct": 1.5,
        "critical_suppliers": ["US Gulf Coast Refiners"],
        "primary_destination_corridor": "West Coast of South America & East Asia (LPG/Refined)",
        "vulnerability_notes": "Freshwater reservoir limitations impacting draft depths during seasonal droughts."
    }
]


class SupplyRiskMonitor:
    """Evaluates country-level petroleum supply exposure and vulnerabilities."""

    @staticmethod
    def get_import_dependence_leaderboard(period: str = "2024") -> pd.DataFrame:
        """
        Calculates net import volumes and estimated dependence levels.
        """
        importers = PetroleumTradeAnalytics.get_top_importers(product_category="crude_oil", period=period, limit=25)
        if importers.empty:
            return pd.DataFrame()

        # Augment with HHI concentration risk
        hhi_scores = []
        risk_tiers = []
        for _, row in importers.iterrows():
            iso3 = row["importer_iso3"]
            hhi_res = PetroleumTradeAnalytics.calculate_supplier_concentration_hhi(
                importer_iso3=iso3, product_category="crude_oil", period=period
            )
            hhi_scores.append(hhi_res["hhi_score"])
            risk_tiers.append(hhi_res["risk_tier"])

        importers["hhi_concentration_index"] = hhi_scores
        importers["supplier_risk_tier"] = risk_tiers
        return importers

    @staticmethod
    def get_chokepoints_data() -> List[Dict[str, Any]]:
        """Returns the verified global maritime shipping chokepoints registry."""
        return CHOKEPOINTS_REGISTRY
