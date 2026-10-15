"""
Petroleum Trade Analytics Engine.
Calculates export/import leaderboards, bilateral flows, trade balance, and HHI concentration.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from sqlalchemy import text
from src.database.connection import db_manager


class PetroleumTradeAnalytics:
    """Computes global petroleum trade volume, value, market shares, and supplier concentration."""

    @staticmethod
    def get_top_exporters(
        product_category: str = "crude_oil",
        period: str = "2024",
        limit: int = 20
    ) -> pd.DataFrame:
        """Retrieves leading exporting countries by volume and value."""
        query = """
        SELECT 
            t.exporter_iso3,
            c.country_name,
            c.continent,
            c.is_opec,
            c.is_opec_plus,
            t.product_category,
            t.reporting_period,
            t.quantity_unit,
            SUM(t.quantity) AS total_export_quantity,
            SUM(COALESCE(t.value_usd, 0)) AS total_export_value_usd,
            t.source_id
        FROM fact_petroleum_trade t
        JOIN dim_country c ON t.exporter_iso3 = c.country_iso3
        WHERE t.trade_direction = 'export'
          AND t.product_category = :product_category
          AND t.reporting_period = :period
        GROUP BY t.exporter_iso3, c.country_name, c.continent, c.is_opec, c.is_opec_plus,
                 t.product_category, t.reporting_period, t.quantity_unit, t.source_id
        ORDER BY total_export_quantity DESC
        LIMIT :limit
        """
        with db_manager.engine.connect() as conn:
            df = pd.read_sql(text(query), conn, params={
                "product_category": product_category,
                "period": period,
                "limit": limit
            })

        if not df.empty:
            total_vol = df["total_export_quantity"].sum()
            df["global_market_share_percent"] = (df["total_export_quantity"] / total_vol) * 100.0
            df["global_market_share_percent"] = df["global_market_share_percent"].round(2)

        return df

    @staticmethod
    def get_top_importers(
        product_category: str = "crude_oil",
        period: str = "2024",
        limit: int = 20
    ) -> pd.DataFrame:
        """Retrieves leading importing countries by volume and value."""
        query = """
        SELECT 
            t.importer_iso3,
            c.country_name,
            c.continent,
            c.income_group,
            t.product_category,
            t.reporting_period,
            t.quantity_unit,
            SUM(t.quantity) AS total_import_quantity,
            SUM(COALESCE(t.value_usd, 0)) AS total_import_value_usd,
            t.source_id
        FROM fact_petroleum_trade t
        JOIN dim_country c ON t.importer_iso3 = c.country_iso3
        WHERE t.trade_direction = 'import'
          AND t.product_category = :product_category
          AND t.reporting_period = :period
        GROUP BY t.importer_iso3, c.country_name, c.continent, c.income_group,
                 t.product_category, t.reporting_period, t.quantity_unit, t.source_id
        ORDER BY total_import_quantity DESC
        LIMIT :limit
        """
        with db_manager.engine.connect() as conn:
            df = pd.read_sql(text(query), conn, params={
                "product_category": product_category,
                "period": period,
                "limit": limit
            })

        if not df.empty:
            total_vol = df["total_import_quantity"].sum()
            df["global_import_share_percent"] = (df["total_import_quantity"] / total_vol) * 100.0
            df["global_import_share_percent"] = df["global_import_share_percent"].round(2)

        return df

    @staticmethod
    def calculate_supplier_concentration_hhi(
        importer_iso3: str,
        product_category: str = "crude_oil",
        period: str = "2024"
    ) -> Dict[str, Any]:
        """
        Calculates the Herfindahl-Hirschman Index (HHI) for an importing country.
        Formula: HHI = Sum(s_i^2) where s_i is percentage market share of supplier i.
        Scale: 0 to 10,000.
        < 1,500: Unconcentrated (Diversified)
        1,500 - 2,500: Moderately Concentrated
        > 2,500: Highly Concentrated (Severe Supplier Dependence)
        """
        query = """
        SELECT 
            t.exporter_iso3,
            c.country_name AS exporter_name,
            t.quantity,
            t.quantity_unit
        FROM fact_petroleum_trade t
        JOIN dim_country c ON t.exporter_iso3 = c.country_iso3
        WHERE t.importer_iso3 = :importer_iso3
          AND t.trade_direction = 'export'
          AND t.product_category = :product_category
          AND t.reporting_period = :period
          AND t.exporter_iso3 IS NOT NULL
        """
        with db_manager.engine.connect() as conn:
            df = pd.read_sql(text(query), conn, params={
                "importer_iso3": importer_iso3,
                "product_category": product_category,
                "period": period
            })

        if df.empty or df["quantity"].sum() == 0:
            return {
                "importer_iso3": importer_iso3,
                "hhi_score": 0.0,
                "risk_tier": "Insufficient Bilateral Data",
                "supplier_count": 0,
                "suppliers": []
            }

        total_qty = df["quantity"].sum()
        df["market_share_pct"] = (df["quantity"] / total_qty) * 100.0
        df["squared_share"] = df["market_share_pct"] ** 2

        hhi = float(df["squared_share"].sum())

        if hhi < 1500:
            tier = "Low Concentration (Diverse)"
        elif hhi <= 2500:
            tier = "Moderate Concentration"
        else:
            tier = "High Concentration (High Exposure)"

        return {
            "importer_iso3": importer_iso3,
            "hhi_score": round(hhi, 2),
            "risk_tier": tier,
            "supplier_count": len(df),
            "suppliers": df[["exporter_iso3", "exporter_name", "quantity", "market_share_pct"]].to_dict(orient="records")
        }

    @staticmethod
    def get_bilateral_trade_flows(
        product_category: str = "crude_oil",
        period: str = "2024"
    ) -> pd.DataFrame:
        """Retrieves bilateral country-to-country trade flows for matrix and map visuals."""
        query = """
        SELECT 
            t.exporter_iso3,
            exp_c.country_name AS exporter_name,
            exp_c.latitude AS exp_lat,
            exp_c.longitude AS exp_lon,
            t.importer_iso3,
            imp_c.country_name AS importer_name,
            imp_c.latitude AS imp_lat,
            imp_c.longitude AS imp_lon,
            t.quantity,
            t.quantity_unit,
            COALESCE(t.value_usd, 0) AS value_usd,
            t.source_id
        FROM fact_petroleum_trade t
        JOIN dim_country exp_c ON t.exporter_iso3 = exp_c.country_iso3
        JOIN dim_country imp_c ON t.importer_iso3 = imp_c.country_iso3
        WHERE t.product_category = :product_category
          AND t.reporting_period = :period
          AND t.exporter_iso3 IS NOT NULL
          AND t.importer_iso3 IS NOT NULL
        ORDER BY t.quantity DESC
        """
        with db_manager.engine.connect() as conn:
            return pd.read_sql(text(query), conn, params={
                "product_category": product_category,
                "period": period
            })
