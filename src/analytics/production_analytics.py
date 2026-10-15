"""
Global Oil Production Atlas Analytics Engine.
Calculates country-level crude oil production rankings, regional production shares,
year-over-year trajectory changes, and distinguishes crude reserves from active extraction.
Data grounded in EIA International Energy Statistics, OPEC Annual Statistical Bulletin, and Energy Institute Statistical Review.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from src.database.connection import db_manager
from sqlalchemy import text


# Official Benchmark Production Statistics (Million Barrels per Day - mbpd)
# Strictly distinguishes Crude Oil + Lease Condensate from Natural Gas Liquids (NGLs)
PRODUCTION_BENCHMARKS = [
    {
        "country_iso3": "USA", "country_name": "United States", "continent": "North America",
        "region": "Northern America", "crude_prod_mbpd_2024": 13.20, "crude_prod_mbpd_2023": 12.93,
        "share_of_global_pct": 16.1, "reserves_billion_bbl": 47.1, "reserve_to_prod_years": 9.8,
        "is_opec": False, "is_opec_plus": False
    },
    {
        "country_iso3": "SAU", "country_name": "Saudi Arabia", "continent": "Asia",
        "region": "Middle East", "crude_prod_mbpd_2024": 9.02, "crude_prod_mbpd_2023": 9.61,
        "share_of_global_pct": 11.0, "reserves_billion_bbl": 267.2, "reserve_to_prod_years": 81.2,
        "is_opec": True, "is_opec_plus": True
    },
    {
        "country_iso3": "RUS", "country_name": "Russian Federation", "continent": "Europe",
        "region": "CIS / Eurasia", "crude_prod_mbpd_2024": 9.15, "crude_prod_mbpd_2023": 9.58,
        "share_of_global_pct": 11.2, "reserves_billion_bbl": 80.0, "reserve_to_prod_years": 23.9,
        "is_opec": False, "is_opec_plus": True
    },
    {
        "country_iso3": "CAN", "country_name": "Canada", "continent": "North America",
        "region": "Northern America", "crude_prod_mbpd_2024": 4.95, "crude_prod_mbpd_2023": 4.87,
        "share_of_global_pct": 6.0, "reserves_billion_bbl": 168.1, "reserve_to_prod_years": 93.0,
        "is_opec": False, "is_opec_plus": False
    },
    {
        "country_iso3": "IRQ", "country_name": "Iraq", "continent": "Asia",
        "region": "Middle East", "crude_prod_mbpd_2024": 4.30, "crude_prod_mbpd_2023": 4.32,
        "share_of_global_pct": 5.2, "reserves_billion_bbl": 145.0, "reserve_to_prod_years": 92.4,
        "is_opec": True, "is_opec_plus": True
    },
    {
        "country_iso3": "CHN", "country_name": "China", "continent": "Asia",
        "region": "Asia-Pacific", "crude_prod_mbpd_2024": 4.22, "crude_prod_mbpd_2023": 4.18,
        "share_of_global_pct": 5.1, "reserves_billion_bbl": 27.0, "reserve_to_prod_years": 17.5,
        "is_opec": False, "is_opec_plus": False
    },
    {
        "country_iso3": "IRN", "country_name": "Iran", "continent": "Asia",
        "region": "Middle East", "crude_prod_mbpd_2024": 3.30, "crude_prod_mbpd_2023": 2.99,
        "share_of_global_pct": 4.0, "reserves_billion_bbl": 208.6, "reserve_to_prod_years": 173.2,
        "is_opec": True, "is_opec_plus": True
    },
    {
        "country_iso3": "BRA", "country_name": "Brazil", "continent": "South America",
        "region": "Latin America", "crude_prod_mbpd_2024": 3.42, "crude_prod_mbpd_2023": 3.40,
        "share_of_global_pct": 4.2, "reserves_billion_bbl": 14.9, "reserve_to_prod_years": 11.9,
        "is_opec": False, "is_opec_plus": False
    },
    {
        "country_iso3": "ARE", "country_name": "United Arab Emirates", "continent": "Asia",
        "region": "Middle East", "crude_prod_mbpd_2024": 3.25, "crude_prod_mbpd_2023": 3.20,
        "share_of_global_pct": 4.0, "reserves_billion_bbl": 113.0, "reserve_to_prod_years": 95.3,
        "is_opec": True, "is_opec_plus": True
    },
    {
        "country_iso3": "KWT", "country_name": "Kuwait", "continent": "Asia",
        "region": "Middle East", "crude_prod_mbpd_2024": 2.55, "crude_prod_mbpd_2023": 2.61,
        "share_of_global_pct": 3.1, "reserves_billion_bbl": 101.5, "reserve_to_prod_years": 109.0,
        "is_opec": True, "is_opec_plus": True
    },
    {
        "country_iso3": "KAZ", "country_name": "Kazakhstan", "continent": "Asia",
        "region": "CIS / Eurasia", "crude_prod_mbpd_2024": 1.88, "crude_prod_mbpd_2023": 1.90,
        "share_of_global_pct": 2.3, "reserves_billion_bbl": 30.0, "reserve_to_prod_years": 43.7,
        "is_opec": False, "is_opec_plus": True
    },
    {
        "country_iso3": "NOR", "country_name": "Norway", "continent": "Europe",
        "region": "Europe", "crude_prod_mbpd_2024": 1.82, "crude_prod_mbpd_2023": 1.77,
        "share_of_global_pct": 2.2, "reserves_billion_bbl": 7.5, "reserve_to_prod_years": 11.3,
        "is_opec": False, "is_opec_plus": False
    },
    {
        "country_iso3": "MEX", "country_name": "Mexico", "continent": "North America",
        "region": "Latin America", "crude_prod_mbpd_2024": 1.85, "crude_prod_mbpd_2023": 1.94,
        "share_of_global_pct": 2.3, "reserves_billion_bbl": 6.0, "reserve_to_prod_years": 8.9,
        "is_opec": False, "is_opec_plus": True
    },
    {
        "country_iso3": "NGA", "country_name": "Nigeria", "continent": "Africa",
        "region": "Africa", "crude_prod_mbpd_2024": 1.45, "crude_prod_mbpd_2023": 1.35,
        "share_of_global_pct": 1.8, "reserves_billion_bbl": 37.0, "reserve_to_prod_years": 70.0,
        "is_opec": True, "is_opec_plus": True
    },
    {
        "country_iso3": "QAT", "country_name": "Qatar", "continent": "Asia",
        "region": "Middle East", "crude_prod_mbpd_2024": 1.30, "crude_prod_mbpd_2023": 1.32,
        "share_of_global_pct": 1.6, "reserves_billion_bbl": 25.2, "reserve_to_prod_years": 53.1,
        "is_opec": False, "is_opec_plus": False
    },
    {
        "country_iso3": "AGO", "country_name": "Angola", "continent": "Africa",
        "region": "Africa", "crude_prod_mbpd_2024": 1.15, "crude_prod_mbpd_2023": 1.14,
        "share_of_global_pct": 1.4, "reserves_billion_bbl": 7.8, "reserve_to_prod_years": 18.6,
        "is_opec": False, "is_opec_plus": False
    },
    {
        "country_iso3": "IND", "country_name": "India", "continent": "Asia",
        "region": "Asia-Pacific", "crude_prod_mbpd_2024": 0.60, "crude_prod_mbpd_2023": 0.59,
        "share_of_global_pct": 0.7, "reserves_billion_bbl": 4.7, "reserve_to_prod_years": 21.5,
        "is_opec": False, "is_opec_plus": False
    },
    {
        "country_iso3": "GBR", "country_name": "United Kingdom", "continent": "Europe",
        "region": "Europe", "crude_prod_mbpd_2024": 0.68, "crude_prod_mbpd_2023": 0.74,
        "share_of_global_pct": 0.8, "reserves_billion_bbl": 1.8, "reserve_to_prod_years": 7.2,
        "is_opec": False, "is_opec_plus": False
    }
]


class GlobalProductionAnalytics:
    """Analytical service providing production rankings, regional shares, and reserve indicators."""

    @staticmethod
    def get_production_leaderboard() -> pd.DataFrame:
        """Returns the ranked table of global crude oil producers with YoY changes."""
        df = pd.DataFrame(PRODUCTION_BENCHMARKS)
        df["yoy_change_mbpd"] = df["crude_prod_mbpd_2024"] - df["crude_prod_mbpd_2023"]
        df["yoy_change_pct"] = (df["yoy_change_mbpd"] / df["crude_prod_mbpd_2023"]) * 100.0
        return df.sort_values("crude_prod_mbpd_2024", ascending=False).reset_index(drop=True)

    @staticmethod
    def get_regional_production_shares() -> pd.DataFrame:
        """Calculates aggregated crude production volume and share across global regions."""
        df = pd.DataFrame(PRODUCTION_BENCHMARKS)
        regional = df.groupby("region", as_index=False).agg(
            total_prod_mbpd=("crude_prod_mbpd_2024", "sum"),
            total_reserves_bbl=("reserves_billion_bbl", "sum"),
            producer_count=("country_iso3", "count")
        )
        total_global = regional["total_prod_mbpd"].sum()
        regional["share_pct"] = (regional["total_prod_mbpd"] / total_global) * 100.0
        return regional.sort_values("total_prod_mbpd", ascending=False).reset_index(drop=True)

    @staticmethod
    def get_opec_vs_non_opec_breakdown() -> Dict[str, Any]:
        """Provides cartel vs market-driven supply concentration telemetry."""
        df = pd.DataFrame(PRODUCTION_BENCHMARKS)
        opec_plus_prod = df[df["is_opec_plus"]]["crude_prod_mbpd_2024"].sum()
        total_tracked = df["crude_prod_mbpd_2024"].sum()
        non_opec_prod = total_tracked - opec_plus_prod

        return {
            "total_tracked_mbpd": round(float(total_tracked), 2),
            "opec_plus_mbpd": round(float(opec_plus_prod), 2),
            "opec_plus_share_pct": round(float((opec_plus_prod / total_tracked) * 100.0), 1),
            "non_opec_mbpd": round(float(non_opec_prod), 2),
            "non_opec_share_pct": round(float((non_opec_prod / total_tracked) * 100.0), 1),
            "top_producer_iso3": "USA",
            "top_producer_mbpd": 13.20,
            "top_reserves_country": "Saudi Arabia (267.2B bbl)"
        }
