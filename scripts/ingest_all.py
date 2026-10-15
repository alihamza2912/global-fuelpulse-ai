"""
CLI Automated Data Ingestion Runner.
Executes scheduled or manual ETL runs across all registered data pipelines.
"""

import sys
import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.ingestion.orchestrator import orchestrator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    print("==================================================")
    print("⚡ Global FuelPulse AI — Data Ingestion Pipeline")
    print("==================================================")
    summaries = orchestrator.run_all()
    print("\n✅ Ingestion Results Summary:")
    for s in summaries:
        status_sym = "🟢" if s.get("status") == "SUCCESS" else "🟡"
        print(f"  {status_sym} [{s.get('source_id')}] {s.get('pipeline_name')}: {s.get('status')} | {s.get('rows_inserted', 0)} inserted | {s.get('duration_ms', 0)}ms")

if __name__ == "__main__":
    main()
