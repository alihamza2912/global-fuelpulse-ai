"""
Configuration Management for Global FuelPulse AI Platform.
Loads environment variables and system settings with safe defaults.
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Base project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env if present
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)


@dataclass
class DatabaseSettings:
    """Database connectivity settings."""
    host: str = field(default_factory=lambda: os.getenv("DB_HOST", "127.0.0.1"))
    port: int = field(default_factory=lambda: int(os.getenv("DB_PORT", "3306")))
    name: str = field(default_factory=lambda: os.getenv("DB_NAME", "fuelx_db"))
    user: str = field(default_factory=lambda: os.getenv("DB_USER", "root"))
    password: str = field(default_factory=lambda: os.getenv("DB_PASSWORD", ""))
    engine_type: str = field(
        default_factory=lambda: os.getenv(
            "DB_ENGINE",
            "sqlite" if (BASE_DIR / "fuelx_local.db").exists() and "DB_HOST" not in os.environ else "mysql"
        )
    )
    sqlite_fallback_path: Path = field(
        default_factory=lambda: BASE_DIR / "fuelx_local.db"
    )

    @property
    def mysql_url(self) -> str:
        """Constructs MySQL SQLAlchemy connection string."""
        if self.password:
            return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}?charset=utf8mb4"
        return f"mysql+pymysql://{self.user}@{self.host}:{self.port}/{self.name}?charset=utf8mb4"

    @property
    def sqlite_url(self) -> str:
        """Constructs SQLite fallback connection string."""
        return f"sqlite:///{self.sqlite_fallback_path}"


def reload_env() -> None:
    """Forces reloading environment variables from absolute .env path."""
    if ENV_PATH.exists():
        load_dotenv(dotenv_path=ENV_PATH, override=True)


def get_gemini_api_key() -> str:
    """
    Dynamically loads and returns the configured Gemini API key from .env.
    Checks in priority order:
    1. GEMINI_API_KEY (primary)
    2. AI_API_KEY (fallback)
    3. LLM_API_KEY (legacy fallback)
    """
    reload_env()
    key = os.getenv("GEMINI_API_KEY") or os.getenv("AI_API_KEY") or os.getenv("LLM_API_KEY", "")
    if not key:
        # Check Streamlit Cloud secrets if available
        try:
            import streamlit as st
            if hasattr(st, "secrets"):
                key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("AI_API_KEY") or ""
        except Exception:
            pass
    return (key or "").strip()


@dataclass
class APISettings:
    """External API credentials and endpoints."""
    eia_api_key: str = field(default_factory=lambda: os.getenv("EIA_API_KEY", ""))
    un_comtrade_key: str = field(default_factory=lambda: os.getenv("UN_COMTRADE_SUBSCRIPTION_KEY", ""))
    globalpetrolprices_key: str = field(default_factory=lambda: os.getenv("GLOBALPETROLPRICES_API_KEY", ""))
    data_gov_api_key: str = field(default_factory=lambda: os.getenv("DATA_GOV_API_KEY", ""))
    llm_provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "gemini"))
    max_ai_calls_per_day: int = field(default_factory=lambda: int(os.getenv("MAX_AI_CALLS_PER_DAY", "200")))
    max_ai_calls_per_minute: int = field(default_factory=lambda: int(os.getenv("MAX_AI_CALLS_PER_MINUTE", "10")))
    session_max_questions_per_hour: int = field(default_factory=lambda: int(os.getenv("SESSION_MAX_QUESTIONS_PER_HOUR", "15")))
    session_cooldown_seconds: float = field(default_factory=lambda: float(os.getenv("SESSION_COOLDOWN_SECONDS", "3.0")))
    max_question_length: int = field(default_factory=lambda: int(os.getenv("MAX_QUESTION_LENGTH", "500")))
    timeout_seconds: int = field(default_factory=lambda: int(os.getenv("API_TIMEOUT_SECONDS", "15")))

    @property
    def gemini_api_key(self) -> str:
        """Dynamic getter for Gemini API key."""
        return get_gemini_api_key()

    @property
    def ai_api_key(self) -> str:
        """Alias for GEMINI_API_KEY / AI_API_KEY."""
        return self.gemini_api_key

    @property
    def llm_api_key(self) -> str:
        """Legacy alias."""
        return self.gemini_api_key

    @property
    def ai_model(self) -> str:
        """Dynamic getter for AI_MODEL from .env."""
        reload_env()
        return os.getenv("AI_MODEL", "gemini-2.0-flash").strip()



@dataclass
class AppSettings:
    """Master application configuration."""
    app_name: str = "Global FuelPulse AI"
    version: str = "1.0.0"
    base_dir: Path = BASE_DIR
    mode: str = field(default_factory=lambda: os.getenv("APP_MODE", "DEMO").upper())
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "False").lower() in ("true", "1", "yes"))
    cache_ttl: int = field(default_factory=lambda: int(os.getenv("CACHE_TTL_SECONDS", "3600")))
    
    db: DatabaseSettings = field(default_factory=DatabaseSettings)
    api: APISettings = field(default_factory=APISettings)

    @property
    def is_real_mode(self) -> bool:
        return self.mode == "REAL"

    @property
    def is_demo_mode(self) -> bool:
        return self.mode != "REAL"


# Global singleton settings instance
settings = AppSettings()
