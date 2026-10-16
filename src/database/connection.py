"""
Database Connection and Session Management for Global FuelPulse AI.
Supports MySQL fuelx_db with automatic failover to local SQLite storage.
"""

import logging
from contextlib import contextmanager
from typing import Generator, Dict, Any, Optional
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from config.settings import settings
from src.database.models import Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages SQLAlchemy engine, session pools, and healthchecks."""

    def __init__(self):
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None
        self._active_dialect: str = "unknown"
        self._initialize_engine()

    def _initialize_engine(self):
        """Attempts connection to MySQL when configured; otherwise connects instantly to SQLite."""
        if settings.db.engine_type.lower() != "sqlite":
            try:
                mysql_url = settings.db.mysql_url
                test_engine = create_engine(
                    mysql_url,
                    pool_pre_ping=True,
                    pool_recycle=3600,
                    connect_args={"connect_timeout": 1}
                )
                with test_engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                self._engine = test_engine
                self._active_dialect = "mysql"
                logger.info("Successfully connected to MySQL database: %s", settings.db.name)
                self._session_factory = sessionmaker(bind=self._engine, autocommit=False, autoflush=False)
                return
            except Exception as e:
                logger.warning("Could not connect to MySQL at %s:%s (%s). Falling back to SQLite local storage.",
                               settings.db.host, settings.db.port, e)

        sqlite_url = settings.db.sqlite_url
        self._engine = create_engine(
            sqlite_url,
            connect_args={"check_same_thread": False}
        )
        self._active_dialect = "sqlite"
        logger.info("Active database: SQLite local file (%s)", settings.db.sqlite_fallback_path)
        self._session_factory = sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False
        )

    @property
    def engine(self) -> Engine:
        if self._engine is None:
            self._initialize_engine()
        return self._engine

    @property
    def dialect(self) -> str:
        return self._active_dialect

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Context manager providing a transactional database session."""
        session: Session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error("Database session transaction error: %s", e)
            raise
        finally:
            session.close()

    def check_health(self) -> Dict[str, Any]:
        """Evaluates database connectivity and schema readiness."""
        status = {
            "connected": False,
            "dialect": self._active_dialect,
            "database": settings.db.name if self._active_dialect == "mysql" else "sqlite_fallback",
            "host": settings.db.host if self._active_dialect == "mysql" else "localhost",
            "port": settings.db.port if self._active_dialect == "mysql" else None,
            "tables_count": 0,
            "tables": [],
            "error": None
        }
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                status["connected"] = True
                inspector = inspect(self.engine)
                table_names = inspector.get_table_names()
                status["tables_count"] = len(table_names)
                status["tables"] = table_names
        except Exception as e:
            status["error"] = str(e)
            logger.error("Database healthcheck failed: %s", e)
        return status

    def safe_sql(self, query: str):
        """Wraps a SQL query string into an executable SQLAlchemy TextClause."""
        return text(query)

    def execute_read_only_query(self, query: str, params: Optional[Dict[str, Any]] = None):
        """Safely executes read-only SELECT queries with parameterization."""
        forbidden_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "REPLACE"]
        normalized_q = query.strip().upper()
        for kw in forbidden_keywords:
            if normalized_q.startswith(kw) or f" {kw} " in normalized_q:
                raise PermissionError(f"Query contains forbidden mutation keyword: {kw}")

        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            cols = result.keys()
            rows = result.fetchall()
            return [dict(zip(cols, row)) for row in rows]


# Global database manager instance
db_manager = DatabaseManager()
