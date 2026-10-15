"""
Fuel Price Affordability Analytics Engine.
Calculates fuel expenditure relative to income proxies, GDP per capita, and affordability rankings.
"""

import pandas as pd
from typing import Dict, Any, Optional
from sqlalchemy import text
from src.database.connection import db_manager


class AffordabilityAnalytics:
    """Evaluates the economic burden of retail fuel costs across nations."""

    @staticmethod
    def get_affordability_overview(reporting_year: int = 2024) -> pd.DataFrame:
        """
        Retrieves fuel affordability metrics and rankings across countries.
        """
        query = """
        SELECT 
            fa.country_iso3,
            c.country_name,
            c.continent,
            c.income_group,
            fa.reporting_year,
            fa.gdp_per_capita_nominal_usd,
            fa.daily_income_proxy_usd,
            fa.petrol_litre_percent_daily_income,
            fa.diesel_litre_percent_daily_income,
            fa.affordability_tier,
            fa.source_id
        FROM fact_affordability fa
        JOIN dim_country c ON fa.country_iso3 = c.country_iso3
        WHERE fa.reporting_year = :reporting_year
        ORDER BY fa.petrol_litre_percent_daily_income ASC
        """
        with db_manager.engine.connect() as conn:
            df = pd.read_sql(text(query), conn, params={"reporting_year": reporting_year})

        if not df.empty:
            df["rank_best_to_worst"] = range(1, len(df) + 1)
        return df

    @staticmethod
    def calculate_country_affordability(
        country_iso3: str,
        current_petrol_usd: float,
        gdp_per_capita_usd: float
    ) -> Dict[str, Any]:
        """
        Calculates fuel affordability based on current live price and GDP proxy.
        Note: GDP per capita / 365 is an analytical proxy, not actual household disposable income.
        """
        daily_income_proxy = gdp_per_capita_usd / 365.0
        pct_of_daily_income = (current_petrol_usd / daily_income_proxy) * 100.0 if daily_income_proxy > 0 else 0.0

        if pct_of_daily_income < 1.0:
            tier = "High Affordability"
            color = "#10B981"  # Emerald
        elif pct_of_daily_income <= 5.0:
            tier = "Moderate Affordability"
            color = "#F59E0B"  # Amber
        elif pct_of_daily_income <= 15.0:
            tier = "Severe Affordability Burden"
            color = "#F97316"  # Orange
        else:
            tier = "Critical Affordability Crisis"
            color = "#EF4444"  # Red

        return {
            "country_iso3": country_iso3,
            "current_petrol_usd": round(current_petrol_usd, 4),
            "gdp_per_capita_usd": round(gdp_per_capita_usd, 2),
            "daily_income_proxy_usd": round(daily_income_proxy, 2),
            "percent_of_daily_income": round(pct_of_daily_income, 2),
            "tier": tier,
            "tier_color": color,
            "disclaimer": "Daily income proxy represents (Nominal GDP per capita / 365). Actual household disposable income varies based on domestic income distribution, taxation, and subsidies."
        }
