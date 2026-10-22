"""
Retail Fuel Price Analytics Engine.
Calculates price differentials, percentage movements, distribution statistics, and global rankings.
"""

import time
import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from sqlalchemy import text
from src.database.connection import db_manager

logger = logging.getLogger(__name__)


class FuelPriceAnalytics:
    """Computes retail gasoline and diesel price statistics and country comparisons."""

    _cache: Dict[str, Tuple[float, pd.DataFrame]] = {}
    CACHE_TTL_SECONDS: float = 300.0  # 5-minute read cache for high responsiveness

    @classmethod
    def invalidate_cache(cls):
        """Clears in-memory price analytics cache."""
        cls._cache.clear()

    @classmethod
    def get_latest_prices(
        cls,
        fuel_type: Optional[str] = None,
        continent: Optional[str] = None,
        country_iso3: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Retrieves latest available retail prices per country with observation timestamps and sources.
        """
        cache_key = f"latest:{fuel_type}:{continent}:{country_iso3}"
        now_ts = time.time()
        if cache_key in cls._cache:
            saved_time, cached_df = cls._cache[cache_key]
            if (now_ts - saved_time) < cls.CACHE_TTL_SECONDS:
                return cached_df.copy()

        # 1. Supabase Cloud Integration: retrieve from vw_latest_fuel_prices view when configured
        try:
            from src.auth.supabase_client import supabase_auth_client
            if supabase_auth_client.is_configured():
                sb_params = {"limit": 1000}
                if fuel_type:
                    sb_params["fuel_type"] = f"eq.{fuel_type}"
                if continent and continent != "All":
                    sb_params["continent"] = f"eq.{continent}"
                if country_iso3 and country_iso3 != "All":
                    sb_params["country_iso3"] = f"eq.{country_iso3}"
                
                ok, records, _ = supabase_auth_client.select_table("vw_latest_fuel_prices", params=sb_params)
                if ok and records:
                    df = pd.DataFrame(records)
                    for col in ["price_local", "price_usd_per_litre", "tax_component_percent"]:
                        if col in df.columns:
                            df[col] = pd.to_numeric(df[col], errors="coerce")
                    cls._cache[cache_key] = (now_ts, df)
                    return df.copy()
        except Exception as e:
            logger.debug("Supabase read fallback to local DB: %s", e)

        query = """
        SELECT 
            fp.price_id,
            fp.country_iso3,
            c.country_name,
            c.continent,
            c.region,
            fp.location_id,
            COALESCE(loc.location_name, 'National Average') AS location_name,
            fp.observation_date,
            fp.fuel_type,
            fp.price_local,
            fp.currency_local,
            fp.unit,
            fp.price_usd_per_litre,
            fp.tax_component_percent,
            fp.source_id,
            ds.name AS source_name,
            fp.source_updated_at,
            fp.ingested_at
        FROM fuel_prices fp
        JOIN dim_country c ON fp.country_iso3 = c.country_iso3
        LEFT JOIN dim_location loc ON fp.location_id = loc.location_id
        JOIN data_sources ds ON fp.source_id = ds.source_id
        WHERE 1=1
        """
        params = {}
        if fuel_type:
            query += " AND fp.fuel_type = :fuel_type"
            params["fuel_type"] = fuel_type
        if continent and continent != "All":
            query += " AND c.continent = :continent"
            params["continent"] = continent
        if country_iso3 and country_iso3 != "All":
            query += " AND fp.country_iso3 = :country_iso3"
            params["country_iso3"] = country_iso3

        query += " ORDER BY fp.observation_date DESC, fp.price_usd_per_litre ASC"

        with db_manager.engine.connect() as conn:
            df = pd.read_sql(text(query), conn, params=params)

        if not df.empty:
            # Deduplicate to latest observation per country, fuel_type, and location
            df = df.sort_values("observation_date", ascending=False).groupby(
                ["country_iso3", "fuel_type", "location_id"], as_index=False
            ).first()

        return df

    @staticmethod
    def calculate_price_change_metrics(country_iso3: str, fuel_type: str = "petrol_regular") -> Dict[str, Any]:
        """
        Calculates absolute and percentage change between latest and immediately preceding observation.
        """
        query = """
        SELECT observation_date, price_local, price_usd_per_litre, currency_local, unit
        FROM fuel_prices
        WHERE country_iso3 = :country_iso3 AND fuel_type = :fuel_type
        ORDER BY observation_date DESC
        LIMIT 2
        """
        with db_manager.engine.connect() as conn:
            df = pd.read_sql(text(query), conn, params={"country_iso3": country_iso3, "fuel_type": fuel_type})

        if len(df) < 2:
            current_row = df.iloc[0] if len(df) == 1 else None
            return {
                "has_previous": False,
                "current_price_usd": float(current_row["price_usd_per_litre"]) if current_row is not None else None,
                "current_date": str(current_row["observation_date"]) if current_row is not None else None,
                "previous_price_usd": None,
                "previous_date": None,
                "absolute_change_usd": 0.0,
                "percentage_change": 0.0
            }

        curr = df.iloc[0]
        prev = df.iloc[1]

        c_usd = float(curr["price_usd_per_litre"])
        p_usd = float(prev["price_usd_per_litre"])
        abs_diff = round(c_usd - p_usd, 4)
        pct_diff = round(((c_usd - p_usd) / p_usd) * 100.0, 2) if p_usd > 0 else 0.0

        return {
            "has_previous": True,
            "current_price_usd": c_usd,
            "current_price_local": float(curr["price_local"]),
            "currency": curr["currency_local"],
            "current_date": str(curr["observation_date"]),
            "previous_price_usd": p_usd,
            "previous_date": str(prev["observation_date"]),
            "absolute_change_usd": abs_diff,
            "percentage_change": pct_diff
        }

    @staticmethod
    def get_global_price_summary(fuel_type: str = "petrol_regular") -> Dict[str, Any]:
        """
        Computes unweighted global average, min, max, median, and dispersion statistics.
        """
        df = FuelPriceAnalytics.get_latest_prices(fuel_type=fuel_type)
        if df.empty:
            return {
                "count": 0, "unweighted_avg_usd": 0.0, "median_usd": 0.0,
                "min_price_usd": 0.0, "min_country": "N/A",
                "max_price_usd": 0.0, "max_country": "N/A", "std_usd": 0.0
            }

        prices = df["price_usd_per_litre"].values
        min_idx = np.argmin(prices)
        max_idx = np.argmax(prices)

        return {
            "count": len(df),
            "unweighted_avg_usd": round(float(np.mean(prices)), 4),
            "median_usd": round(float(np.median(prices)), 4),
            "std_usd": round(float(np.std(prices)), 4),
            "min_price_usd": round(float(prices[min_idx]), 4),
            "min_country": df.iloc[min_idx]["country_name"],
            "min_country_iso3": df.iloc[min_idx]["country_iso3"],
            "max_price_usd": round(float(prices[max_idx]), 4),
            "max_country": df.iloc[max_idx]["country_name"],
            "max_country_iso3": df.iloc[max_idx]["country_iso3"],
            "note": "Averages are unweighted arithmetic means across all reporting countries."
        }
