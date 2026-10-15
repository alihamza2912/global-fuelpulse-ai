"""
Base Ingestion Framework for Global FuelPulse AI Platform.
Provides standardized abstract connector, error quarantine, and ETL logging.
"""

import time
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.database.models import EtlRunLog

logger = logging.getLogger(__name__)


class BaseConnector(ABC):
    """Abstract base class for all external data source pipelines."""

    def __init__(self, source_id: str, pipeline_name: str):
        self.source_id = source_id
        self.pipeline_name = pipeline_name
        self.quarantined_records: List[Dict[str, Any]] = []

    @abstractmethod
    def fetch_raw_data(self) -> Any:
        """Connects to external authorized API or feed and retrieves payload."""
        pass

    @abstractmethod
    def validate_schema(self, raw_data: Any) -> bool:
        """Validates payload schema and required keys."""
        pass

    @abstractmethod
    def transform_records(self, raw_data: Any) -> List[Dict[str, Any]]:
        """Normalizes entities, standardizes units/currencies, and filters invalid rows."""
        pass

    @abstractmethod
    def load_to_database(self, records: List[Dict[str, Any]], session: Session) -> Dict[str, int]:
        """Idempotently writes transformed records to database tables."""
        pass

    def run_pipeline(self, session: Session) -> Dict[str, Any]:
        """
        Executes complete ETL lifecycle with timing, error quarantine, and telemetry logging.
        Returns execution statistics summary.
        """
        start_time = time.time()
        start_dt = datetime.now(timezone.utc)
        status = "SUCCESS"
        error_msg = None
        rows_fetched = 0
        rows_inserted = 0
        rows_updated = 0
        rows_rejected = 0
        duplicate_count = 0

        logger.info("Starting pipeline [%s] for source [%s]...", self.pipeline_name, self.source_id)

        try:
            raw_data = self.fetch_raw_data()
            if not self.validate_schema(raw_data):
                raise ValueError(f"Schema validation failed for pipeline {self.pipeline_name}")

            transformed_records = self.transform_records(raw_data)
            rows_fetched = len(transformed_records) + len(self.quarantined_records)
            rows_rejected = len(self.quarantined_records)

            if transformed_records:
                load_stats = self.load_to_database(transformed_records, session)
                rows_inserted = load_stats.get("inserted", 0)
                rows_updated = load_stats.get("updated", 0)
                duplicate_count = load_stats.get("duplicates", 0)
            else:
                logger.warning("Pipeline [%s] yielded 0 valid transformed records.", self.pipeline_name)
                status = "PARTIAL"

        except Exception as e:
            logger.error("Pipeline [%s] execution error: %s", self.pipeline_name, e, exc_info=True)
            status = "FAILED"
            error_msg = str(e)
            # Re-raise or record status

        duration_ms = int((time.time() - start_time) * 1000)

        # Log pipeline execution to etl_run_log table
        try:
            log_entry = EtlRunLog(
                source_id=self.source_id,
                pipeline_name=self.pipeline_name,
                status=status,
                rows_fetched=rows_fetched,
                rows_inserted=rows_inserted,
                rows_updated=rows_updated,
                rows_rejected=rows_rejected,
                duplicate_count=duplicate_count,
                duration_ms=duration_ms,
                error_message=error_msg,
                started_at=start_dt,
                completed_at=datetime.now(timezone.utc)
            )
            session.add(log_entry)
            session.commit()
        except Exception as log_err:
            logger.error("Failed to commit ETL telemetry log: %s", log_err)
            session.rollback()

        return {
            "source_id": self.source_id,
            "pipeline_name": self.pipeline_name,
            "status": status,
            "rows_fetched": rows_fetched,
            "rows_inserted": rows_inserted,
            "rows_updated": rows_updated,
            "rows_rejected": rows_rejected,
            "duplicate_count": duplicate_count,
            "duration_ms": duration_ms,
            "error_message": error_msg,
            "completed_at": datetime.now(timezone.utc).isoformat()
        }
