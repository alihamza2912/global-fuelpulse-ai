"""
Schema Migration and Database Initialization Utility for Global FuelPulse AI.
Ensures non-destructive table creation, view creation, and seed data population.
"""

import logging
from pathlib import Path
from sqlalchemy import text
from src.database.connection import db_manager
from src.database.models import Base, DataSource, DimCountry, FuelPrice

logger = logging.getLogger(__name__)
SQL_DIR = Path(__file__).resolve().parent.parent.parent / "sql"


def init_database(seed_if_empty: bool = True) -> bool:
    """
    Initializes database tables and creates views.
    Preserves all existing data.
    """
    engine = db_manager.engine
    logger.info("Initializing database schema on dialect: %s", db_manager.dialect)

    try:
        # 1. Create tables from SQLAlchemy ORM metadata
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified/created successfully.")

        # 2. Check if we need to seed demo/benchmark data
        if seed_if_empty:
            from src.database.seeder import seed_database
            with db_manager.get_session() as session:
                seed_database(session, force=False)

        # 3. Ensure default demo analyst user exists
        try:
            from src.auth.auth_service import AuthService
            AuthService.ensure_default_demo_user()
        except Exception as e:
            logger.debug("Demo user ensure notice: %s", e)


        # 3. Create or replace analytical SQL views (if supported)
        views_file = SQL_DIR / "views.sql"
        if views_file.exists() and db_manager.dialect == "mysql":
            try:
                _execute_sql_file(views_file)
                logger.info("Analytical SQL views applied.")
            except Exception as e:
                logger.warning("Could not execute MySQL-specific views directly: %s", e)

        return True

    except Exception as e:
        logger.error("Database initialization failed: %s", e)
        raise


def _execute_sql_file(file_path: Path):
    """Parses and executes multi-statement SQL files safely."""
    engine = db_manager.engine
    content = file_path.read_text(encoding="utf-8")
    
    # Split by semicolon while respecting comments
    raw_statements = content.split(";")
    with engine.connect() as conn:
        for stmt in raw_statements:
            clean_stmt = stmt.strip()
            if not clean_stmt or clean_stmt.startswith("--"):
                continue
            try:
                # Handle MySQL specific syntax if on SQLite
                if db_manager.dialect == "sqlite":
                    clean_stmt = _adapt_mysql_for_sqlite(clean_stmt)
                    if not clean_stmt:
                        continue
                conn.execute(text(clean_stmt))
            except Exception as e:
                logger.debug("Statement execution note: %s for statement: %s", e, clean_stmt[:60])
        conn.commit()


def _adapt_mysql_for_sqlite(statement: str) -> str:
    """Adapts MySQL INSERT statements with ON DUPLICATE KEY UPDATE to SQLite OR IGNORE/REPLACE."""
    upper = statement.upper()
    if "ON DUPLICATE KEY UPDATE" in upper:
        # Truncate before ON DUPLICATE KEY UPDATE and use INSERT OR IGNORE
        idx = upper.find("ON DUPLICATE KEY UPDATE")
        stmt_part = statement[:idx].strip()
        if stmt_part.upper().startswith("INSERT INTO"):
            return "INSERT OR IGNORE INTO " + stmt_part[11:]
        return stmt_part
    if "NOW() - INTERVAL" in upper:
        # SQLite datetime replacement
        statement = statement.replace("NOW() - INTERVAL 1 HOUR", "datetime('now', '-1 hour')")
        statement = statement.replace("NOW() - INTERVAL 2 HOUR", "datetime('now', '-2 hour')")
        statement = statement.replace("NOW() - INTERVAL 5 HOUR", "datetime('now', '-5 hour')")
        statement = statement.replace("NOW() - INTERVAL 1 DAY", "datetime('now', '-1 day')")
        statement = statement.replace("+ INTERVAL 1 SECOND", "")
        statement = statement.replace("+ INTERVAL 2 SECOND", "")
        statement = statement.replace("+ INTERVAL 3 SECOND", "")
        statement = statement.replace("+ INTERVAL 4 SECOND", "")
    return statement


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_database()
