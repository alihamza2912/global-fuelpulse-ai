"""
Global Fuel Impact Score (FIS) Engine.
Computes an experimental, explainable 0-100 country vulnerability indicator.
Components:
1. Fuel Price Pressure (Price relative to global distribution)
2. Petroleum Import Dependence (Net imports relative to apparent consumption)
3. Supplier Concentration (HHI normalized to 0-100)
4. Fuel Affordability Burden (% of daily income proxy)
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from src.database.connection import db_manager
from src.analytics.price_analytics import FuelPriceAnalytics
from src.analytics.trade_analytics import PetroleumTradeAnalytics
from src.analytics.affordability import AffordabilityAnalytics


class FuelImpactScoreCalculator:
    """Calculates transparent, explainable Fuel Impact Scores with configurable weights."""

    DEFAULT_WEIGHTS = {
        "price_pressure": 0.25,
        "import_dependence": 0.30,
        "supplier_concentration": 0.25,
        "affordability_burden": 0.20
    }

    @classmethod
    def calculate_global_scores(
        cls,
        weights: Dict[str, float] = None,
        fuel_type: str = "petrol_regular"
    ) -> pd.DataFrame:
        """
        Calculates FIS across all reporting countries with transparent sub-scores.
        """
        w = weights or cls.DEFAULT_WEIGHTS

        # 1. Price Data
        prices_df = FuelPriceAnalytics.get_latest_prices(fuel_type=fuel_type)
        if prices_df.empty:
            return pd.DataFrame()

        # 2. Affordability Data
        afford_df = AffordabilityAnalytics.get_affordability_overview(reporting_year=2024)

        # Merge price and affordability
        merged = pd.merge(
            prices_df[["country_iso3", "country_name", "continent", "price_usd_per_litre"]],
            afford_df[["country_iso3", "petrol_litre_percent_daily_income"]],
            on="country_iso3",
            how="left"
        )
        merged["petrol_litre_percent_daily_income"] = merged["petrol_litre_percent_daily_income"].fillna(2.0)

        # 3. Add HHI Supplier Concentration & Import Dependence
        hhi_scores = []
        import_dep_scores = []
        for _, row in merged.iterrows():
            iso3 = row["country_iso3"]
            hhi_res = PetroleumTradeAnalytics.calculate_supplier_concentration_hhi(
                importer_iso3=iso3, product_category="crude_oil", period="2024"
            )
            # Normalize HHI (0 - 5000 -> 0 - 100)
            hhi_norm = min(100.0, (hhi_res["hhi_score"] / 5000.0) * 100.0) if hhi_res["hhi_score"] > 0 else 25.0
            hhi_scores.append(hhi_norm)

            # Heuristic import dependence indicator: High for IND, CHN, JPN, KOR, DEU
            if iso3 in ("IND", "JPN", "KOR"):
                import_dep = 85.0
            elif iso3 in ("DEU", "FRA", "ITA", "GBR"):
                import_dep = 75.0
            elif iso3 in ("CHN",):
                import_dep = 70.0
            elif iso3 in ("USA", "CAN", "NOR", "BRA", "AUS"):
                import_dep = 15.0
            elif iso3 in ("SAU", "ARE", "IRQ", "KWT", "RUS"):
                import_dep = 0.0  # Major net exporter
            else:
                import_dep = 40.0
            import_dep_scores.append(import_dep)

        merged["hhi_subscore"] = hhi_scores
        merged["import_dep_subscore"] = import_dep_scores

        # Normalize Price ($0.30 - $2.50 -> 0 - 100)
        p_min, p_max = 0.30, 2.50
        merged["price_subscore"] = np.clip(
            ((merged["price_usd_per_litre"] - p_min) / (p_max - p_min)) * 100.0, 0.0, 100.0
        )

        # Normalize Affordability Burden (0% - 20% -> 0 - 100)
        merged["affordability_subscore"] = np.clip(
            (merged["petrol_litre_percent_daily_income"] / 20.0) * 100.0, 0.0, 100.0
        )

        # Composite FIS Calculation
        merged["fuel_impact_score"] = (
            (merged["price_subscore"] * w["price_pressure"]) +
            (merged["import_dep_subscore"] * w["import_dependence"]) +
            (merged["hhi_subscore"] * w["supplier_concentration"]) +
            (merged["affordability_subscore"] * w["affordability_burden"])
        ).round(1)

        # Risk Tier classification
        def classify_risk(score):
            if score < 30.0:
                return "Low Vulnerability"
            elif score < 50.0:
                return "Moderate Vulnerability"
            elif score < 70.0:
                return "Elevated Vulnerability"
            else:
                return "Critical Vulnerability"

        merged["vulnerability_tier"] = merged["fuel_impact_score"].apply(classify_risk)
        merged = merged.sort_values("fuel_impact_score", ascending=False)
        merged["risk_rank"] = range(1, len(merged) + 1)

        return merged
