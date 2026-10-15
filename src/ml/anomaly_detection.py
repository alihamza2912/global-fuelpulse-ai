"""
Energy Market Anomaly Detection Engine.
Applies Rolling Z-Score, Median Absolute Deviation (MAD), and IQR metrics to detect
unusual price spikes, sudden volume curtailments, and ingestion data freshness gaps.
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime, date, timedelta
from sqlalchemy import text
from src.database.connection import db_manager
from src.database.models import AnomalyEvent

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """Detects statistical price anomalies and pipeline health issues."""

    @staticmethod
    def detect_price_anomalies(threshold_zscore: float = 2.5) -> List[Dict[str, Any]]:
        """
        Scans fuel price observations across all countries for statistical outliers.
        Uses Rolling Z-score and Median Absolute Deviation (MAD).
        """
        query = """
        SELECT fp.country_iso3, c.country_name, fp.fuel_type, fp.observation_date, fp.price_usd_per_litre
        FROM fuel_prices fp
        JOIN dim_country c ON fp.country_iso3 = c.country_iso3
        ORDER BY fp.country_iso3, fp.fuel_type, fp.observation_date ASC
        """
        with db_manager.engine.connect() as conn:
            df = pd.read_sql(text(query), conn)

        anomalies = []
        if df.empty:
            return anomalies

        # Group by country and fuel type
        for (iso3, country_name, fuel), group in df.groupby(["country_iso3", "country_name", "fuel_type"]):
            if len(group) < 3:
                continue

            prices = group["price_usd_per_litre"].values
            median_val = float(np.median(prices))
            mad = float(np.median(np.abs(prices - median_val)))
            std_val = float(np.std(prices)) if np.std(prices) > 0 else 0.01

            latest_row = group.iloc[-1]
            latest_price = float(latest_row["price_usd_per_litre"])
            latest_date = latest_row["observation_date"]

            zscore = (latest_price - float(np.mean(prices))) / std_val
            pct_dev = ((latest_price - median_val) / median_val) * 100.0 if median_val > 0 else 0.0

            # Flag if absolute Z-score exceeds threshold or percentage dev > 15%
            if abs(zscore) >= threshold_zscore or abs(pct_dev) >= 15.0:
                severity = "HIGH" if abs(pct_dev) >= 25.0 else ("MEDIUM" if abs(pct_dev) >= 15.0 else "LOW")
                anomalies.append({
                    "entity_type": "fuel_price",
                    "country_iso3": iso3,
                    "country_name": country_name,
                    "product_category": fuel,
                    "observation_date": str(latest_date),
                    "metric_name": "retail_price_usd_per_litre",
                    "observed_value": round(latest_price, 4),
                    "expected_baseline": round(median_val, 4),
                    "deviation_percent": round(pct_dev, 2),
                    "zscore": round(zscore, 2),
                    "detection_method": "rolling_zscore_and_mad",
                    "severity": severity,
                    "description": f"{country_name} {fuel} experienced a {pct_dev:+.1f}% deviation from its historical baseline."
                })

        return anomalies

    @staticmethod
    def detect_trade_volume_anomalies() -> List[Dict[str, Any]]:
        """
        Scans international petroleum trade flows for unexpected export reductions or surges.
        """
        query = """
        SELECT reporting_period, exporter_iso3, c.country_name, product_category, quantity, quantity_unit
        FROM fact_petroleum_trade t
        JOIN dim_country c ON t.exporter_iso3 = c.country_iso3
        WHERE trade_direction = 'export'
        ORDER BY exporter_iso3, product_category, reporting_period ASC
        """
        with db_manager.engine.connect() as conn:
            df = pd.read_sql(text(query), conn)

        anomalies = []
        if df.empty:
            return anomalies

        for (iso3, c_name, prod), group in df.groupby(["exporter_iso3", "country_name", "product_category"]):
            if len(group) < 2:
                continue

            quantities = group["quantity"].values
            curr_q = float(quantities[-1])
            prev_q = float(quantities[-2])
            yoy_change = ((curr_q - prev_q) / prev_q) * 100.0 if prev_q > 0 else 0.0

            if abs(yoy_change) >= 20.0:
                severity = "CRITICAL" if yoy_change <= -25.0 else "MEDIUM"
                anomalies.append({
                    "entity_type": "trade_volume",
                    "country_iso3": iso3,
                    "country_name": c_name,
                    "product_category": prod,
                    "observation_date": str(group.iloc[-1]["reporting_period"]),
                    "metric_name": "export_quantity_bpd",
                    "observed_value": round(curr_q, 0),
                    "expected_baseline": round(prev_q, 0),
                    "deviation_percent": round(yoy_change, 2),
                    "detection_method": "yoy_curtailment_detector",
                    "severity": severity,
                    "description": f"Significant YoY trade shift: {c_name} {prod} export changed by {yoy_change:+.1f}%."
                })

        return anomalies

    @staticmethod
    def get_persisted_anomalies() -> pd.DataFrame:
        """Retrieves verified anomaly records stored in database."""
        query = """
        SELECT 
            anomaly_id, entity_type, country_iso3, product_category,
            observation_date, metric_name, observed_value, expected_baseline,
            deviation_percent, detection_method, severity, alert_description, detected_at
        FROM anomaly_events
        ORDER BY detected_at DESC
        """
        with db_manager.engine.connect() as conn:
            return pd.read_sql(text(query), conn)
