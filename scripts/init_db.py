"""
CLI Database Initialization & Migration Tool.
Executes schema creation, creates views, and verifies database health.
"""

import sys
import logging
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.database.migrations import init_database
from src.database.connection import db_manager

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    print("==================================================")
    print("🛢️ Global FuelPulse AI — Database Initialization")
    print("==================================================")
    success = init_database(seed_if_empty=True)
    health = db_manager.check_health()
    print("\n✅ Health Check Summary:")
    print(f"  - Connected: {health['connected']}")
    print(f"  - Dialect:   {health['dialect']}")
    print(f"  - Database:  {health['database']}")
    print(f"  - Tables:    {health['tables_count']} tables present")
    print("\nReady for production intelligence queries.")

if __name__ == "__main__":
    main()
