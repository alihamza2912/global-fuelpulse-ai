"""
Indian Regional Petroleum Consumption & Demand Analytics Engine.
Grounded in official Petroleum Planning & Analysis Cell (PPAC) data from the Ministry of Petroleum & Natural Gas.
Tracks national product-level demand (HSD, MS, LPG, ATF, Bitumen, Petcoke) and regional geographic distribution.
"""

import pandas as pd
from typing import Dict, Any, List


# Official PPAC National Petroleum Consumption Benchmark (FY2023–24 & FY2024–25 Run-rate)
# Units in Million Metric Tonnes (MMT)
PRODUCT_CONSUMPTION_BENCHMARKS = [
    {
        "product_code": "HSD", "product_name": "High-Speed Diesel", "category": "Transport & Logistics",
        "consumption_mmt": 89.10, "share_pct": 38.2, "yoy_growth_pct": 4.4,
        "primary_sectors": "Heavy road freight, agricultural tractors, railway traction, captive backup power"
    },
    {
        "product_code": "MS", "product_name": "Motor Spirit (Petrol)", "category": "Personal Mobility",
        "consumption_mmt": 37.20, "share_pct": 15.9, "yoy_growth_pct": 6.8,
        "primary_sectors": "Two-wheelers (70%+ consumption), passenger cars, light urban transport"
    },
    {
        "product_code": "LPG", "product_name": "Liquefied Petroleum Gas", "category": "Household & Commercial",
        "consumption_mmt": 29.60, "share_pct": 12.7, "yoy_growth_pct": 3.5,
        "primary_sectors": "Residential cooking (Pradhan Mantri Ujjwala Yojana), commercial catering, autogas"
    },
    {
        "product_code": "PETCOKE", "product_name": "Petroleum Coke", "category": "Industrial Fuel",
        "consumption_mmt": 18.50, "share_pct": 7.9, "yoy_growth_pct": 5.1,
        "primary_sectors": "Cement manufacturing kilns, blast furnaces, metallurgical coke blending"
    },
    {
        "product_code": "NAPHTHA", "product_name": "Naphtha", "category": "Petrochemical Feedstock",
        "consumption_mmt": 12.80, "share_pct": 5.5, "yoy_growth_pct": 1.2,
        "primary_sectors": "Ethylene crackers, polymer synthesis, ammonia fertilizer synthesis"
    },
    {
        "product_code": "BITUMEN", "product_name": "Bitumen / Asphalt", "category": "Infrastructure",
        "consumption_mmt": 8.80, "share_pct": 3.8, "yoy_growth_pct": 7.5,
        "primary_sectors": "National highways (NHAI Bharatmala corridor), state expressway paving"
    },
    {
        "product_code": "ATF", "product_name": "Aviation Turbine Fuel", "category": "Aviation",
        "consumption_mmt": 8.30, "share_pct": 3.6, "yoy_growth_pct": 10.2,
        "primary_sectors": "Domestic scheduled commercial aviation, international passenger & air cargo"
    },
    {
        "product_code": "OTHERS", "product_name": "Furnace Oil, Lubes, LDO & Solvents", "category": "Industrial & Specialty",
        "consumption_mmt": 29.00, "share_pct": 12.4, "yoy_growth_pct": 2.1,
        "primary_sectors": "Industrial boilers, maritime bunkering, automotive engine lubricants"
    }
]

# PPAC Geographic Regional Consumption Distribution
REGIONAL_CONSUMPTION_DATA = [
    {
        "region": "Northern Region",
        "states_covered": "Delhi NCT, Uttar Pradesh, Punjab, Haryana, Rajasthan, Uttarakhand, HP, J&K",
        "consumption_share_pct": 30.1,
        "consumption_mmt": 70.2,
        "demand_driver": "Extensive agricultural irrigation diesel, dense passenger vehicle ownership, heavy winter heating"
    },
    {
        "region": "Western Region",
        "states_covered": "Maharashtra, Gujarat, Madhya Pradesh, Goa, D&NH and D&D",
        "consumption_share_pct": 32.4,
        "consumption_mmt": 75.6,
        "demand_driver": "Highest refining density (Jamnagar, Mumbai), petrochemical hubs, chemical corridors, major ports"
    },
    {
        "region": "Southern Region",
        "states_covered": "Tamil Nadu, Karnataka, Telangana, Andhra Pradesh, Kerala, Puducherry",
        "consumption_share_pct": 25.8,
        "consumption_mmt": 60.2,
        "demand_driver": "Heavy industrial manufacturing corridors, automobile hubs, tech delivery fleets, coastal maritime bunkering"
    },
    {
        "region": "Eastern & North-Eastern",
        "states_covered": "West Bengal, Bihar, Odisha, Jharkhand, Assam and 7 NE states",
        "consumption_share_pct": 11.7,
        "consumption_mmt": 27.3,
        "demand_driver": "Coal and mineral freight corridors, steel plants, expanding riverine and road logistics network"
    }
]


class IndiaDemandAnalytics:
    """Provides product-level consumption breakdown and regional demand intelligence."""

    @staticmethod
    def get_national_product_consumption() -> pd.DataFrame:
        """Returns national demand by petroleum commodity in MMT with YoY growth rates."""
        return pd.DataFrame(PRODUCT_CONSUMPTION_BENCHMARKS)

    @staticmethod
    def get_regional_demand_shares() -> pd.DataFrame:
        """Returns geographic demand distribution across Northern, Western, Southern, and Eastern regions."""
        return pd.DataFrame(REGIONAL_CONSUMPTION_DATA)

    @staticmethod
    def get_demand_summary() -> Dict[str, Any]:
        """Returns headline demand metrics for Indian petroleum consumption."""
        total_mmt = sum(p["consumption_mmt"] for p in PRODUCT_CONSUMPTION_BENCHMARKS)
        hsd_item = next(p for p in PRODUCT_CONSUMPTION_BENCHMARKS if p["product_code"] == "HSD")
        ms_item = next(p for p in PRODUCT_CONSUMPTION_BENCHMARKS if p["product_code"] == "MS")
        atf_item = next(p for p in PRODUCT_CONSUMPTION_BENCHMARKS if p["product_code"] == "ATF")

        return {
            "total_consumption_mmt": round(total_mmt, 1),
            "hsd_consumption_mmt": hsd_item["consumption_mmt"],
            "hsd_share_pct": hsd_item["share_pct"],
            "ms_consumption_mmt": ms_item["consumption_mmt"],
            "ms_share_pct": ms_item["share_pct"],
            "atf_growth_pct": atf_item["yoy_growth_pct"],
            "top_consuming_region": "Western Region (32.4%)",
            "reporting_authority": "Petroleum Planning & Analysis Cell (PPAC)"
        }
