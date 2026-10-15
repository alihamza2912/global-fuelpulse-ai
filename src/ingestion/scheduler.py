"""
Automated Pipeline Scheduler for Global FuelPulse AI.
Provides background scheduled refreshes of retail fuel prices,
crude benchmarks, and foreign exchange rates without blocking the Streamlit app.
"""

import time
import threading
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from src.ingestion.orchestrator import orchestrator

logger = logging.getLogger(__name__)


class PipelineScheduler:
    """Manages scheduled background ingestion tasks."""

    def __init__(self, interval_seconds: int = 21600):  # Default 6 hours
        self.interval_seconds = interval_seconds
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._is_running = False
        self.last_run_time: Optional[datetime] = None
        self.last_status: str = "IDLE"

    def start(self):
        """Starts the background worker thread if not already active."""
        if self._is_running:
            logger.info("Scheduler already active.")
            return

        self._stop_event.clear()
        self._is_running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True, name="PipelineSchedulerThread")
        self._thread.start()
        logger.info("Pipeline scheduler started in background thread with interval=%ds.", self.interval_seconds)

    def stop(self):
        """Signals the background thread to stop gracefully."""
        if not self._is_running:
            return
        self._stop_event.set()
        self._is_running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)
        logger.info("Pipeline scheduler stopped.")

    def trigger_now(self) -> Dict[str, Any]:
        """Triggers an immediate synchronous live data refresh."""
        logger.info("Manual/on-demand pipeline refresh triggered.")
        start_time = time.time()
        try:
            results = orchestrator.run_live_refresh()
            self.last_run_time = datetime.now(timezone.utc)
            self.last_status = "SUCCESS"
            duration = round(time.time() - start_time, 2)
            return {
                "status": "SUCCESS",
                "duration_seconds": duration,
                "timestamp": self.last_run_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
                "summaries": results
            }
        except Exception as e:
            self.last_status = "FAILED"
            logger.error("Immediate pipeline sync failed: %s", e)
            return {
                "status": "FAILED",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            }

    @property
    def is_running(self) -> bool:
        return self._is_running

    def _run_loop(self):
        """Background loop executing scheduled syncs periodically."""
        logger.info("Scheduler loop initialized.")
        while not self._stop_event.is_set():
            # Wait for interval or stop event
            if self._stop_event.wait(timeout=self.interval_seconds):
                break

            try:
                logger.info("Executing scheduled periodic data refresh...")
                orchestrator.run_live_refresh()
                self.last_run_time = datetime.now(timezone.utc)
                self.last_status = "SUCCESS"
            except Exception as e:
                self.last_status = "FAILED"
                logger.error("Periodic pipeline execution failed: %s", e)


# Global singleton scheduler instance
scheduler = PipelineScheduler()
