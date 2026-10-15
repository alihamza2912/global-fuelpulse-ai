"""
Data Quality and Ingestion Telemetry Auditor.
Computes data freshness latencies, duplicate counts, missing value audits, and ETL health metrics.
"""

import pandas as pd
from typing import Dict, Any, List
from datetime import datetime, timezone
from sqlalchemy import text
from src.database.connection import db_manager


class DataQualityAuditor:
    """Monitors ingestion pipelines, schema adherence, and data provenance."""

    @staticmethod
    def get_pipeline_telemetry() -> pd.DataFrame:
        """Retrieves history of ETL pipeline executions and row metrics."""
        query = """
        SELECT 
            run_id, source_id, pipeline_name, status,
            rows_fetched, rows_inserted, rows_updated, rows_rejected,
            duplicate_count, duration_ms, error_message, started_at, completed_at
        FROM etl_run_log
        ORDER BY started_at DESC
        LIMIT 50
        """
        with db_manager.engine.connect() as conn:
            return pd.read_sql(text(query), conn)

    @staticmethod
    def get_source_freshness_status() -> List[Dict[str, Any]]:
        """
        Calculates observation freshness latency for each registered external data source.
        """
        query = """
        SELECT 
            ds.source_id,
            ds.name,
            ds.update_frequency,
            ds.license_terms,
            MAX(fp.observation_date) AS latest_fuel_price_date,
            MAX(fp.ingested_at) AS latest_fuel_price_ingest,
            COUNT(fp.price_id) AS fuel_price_records_count
        FROM data_sources ds
        LEFT JOIN fuel_prices fp ON ds.source_id = fp.source_id
        GROUP BY ds.source_id, ds.name, ds.update_frequency, ds.license_terms
        """
        with db_manager.engine.connect() as conn:
            df = pd.read_sql(text(query), conn)

        results = []
        with db_manager.engine.connect() as conn:
            for _, row in df.iterrows():
                src_id = row["source_id"]
                last_date = row["latest_fuel_price_date"]
                rec_count = int(row["fuel_price_records_count"])

                if src_id == "OPEN_ER_API":
                    fx_max = conn.execute(text("SELECT MAX(rate_date) FROM fact_exchange_rate")).scalar()
                    fx_cnt = conn.execute(text("SELECT COUNT(*) FROM fact_exchange_rate")).scalar()
                    if fx_max:
                        last_date = fx_max
                        rec_count = int(fx_cnt)
                elif src_id == "UN_COMTRADE":
                    tr_max = conn.execute(text("SELECT MAX(reporting_period) FROM fact_petroleum_trade")).scalar()
                    tr_cnt = conn.execute(text("SELECT COUNT(*) FROM fact_petroleum_trade")).scalar()
                    if tr_max:
                        last_date = f"{tr_max}-12-31" if len(str(tr_max)) == 4 else str(tr_max)
                        rec_count = int(tr_cnt)

                if pd.notnull(last_date) and last_date is not None:
                    # Latency in days
                    if isinstance(last_date, str):
                        try:
                            last_date_obj = datetime.strptime(last_date[:10], "%Y-%m-%d").date()
                        except ValueError:
                            last_date_obj = datetime.now(timezone.utc).date()
                    elif hasattr(last_date, "date"):
                        last_date_obj = last_date.date()
                    else:
                        last_date_obj = last_date

                    latency_days = (datetime.now(timezone.utc).date() - last_date_obj).days
                    freshness_status = "FRESH" if latency_days <= 14 else ("STALE" if latency_days <= 45 else "HISTORICAL")
                else:
                    latency_days = None
                    freshness_status = "NO_DATA"

                results.append({
                    "source_id": src_id,
                    "source_name": row["name"],
                    "update_frequency": row["update_frequency"],
                    "license": row["license_terms"],
                    "latest_observation_date": str(last_date) if last_date else "N/A",
                    "records_count": rec_count,
                    "latency_days": latency_days,
                    "freshness_status": freshness_status
                })

        return results

    @staticmethod
    def get_table_row_counts() -> Dict[str, int]:
        """Returns row count summary across all core relational tables."""
        tables = [
            "data_sources", "dim_country", "dim_location", "fuel_prices",
            "fact_petroleum_trade", "fact_affordability", "anomaly_events", "etl_run_log"
        ]
        counts = {}
        with db_manager.engine.connect() as conn:
            for t in tables:
                try:
                    res = conn.execute(text(f"SELECT COUNT(*) FROM {t}")).scalar()
                    counts[t] = int(res)
                except Exception:
                    counts[t] = 0
        return counts
