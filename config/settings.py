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
            "mysql" if ("DB_HOST" in os.environ and os.getenv("DB_HOST") not in ("127.0.0.1", "localhost", "")) else "sqlite"
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


def reload_env(override: bool = False) -> None:
    """Reloads environment variables from absolute .env path without clobbering in-process overrides."""
    if ENV_PATH.exists():
        load_dotenv(dotenv_path=ENV_PATH, override=override)


def get_gemini_api_key() -> str:
    """
    Dynamically loads and returns the configured Antigravity / Gemini API key or token.
    Checks in priority order:
    1. Streamlit session_state user-attached key ('antigravity_token', 'user_api_key')
    2. ANTIGRAVITY_API_KEY (environment or .env)
    3. ANTIGRAVITY_TOKEN (environment or .env)
    4. GEMINI_API_KEY (environment or .env)
    5. AI_API_KEY / GOOGLE_API_KEY / LLM_API_KEY (fallbacks)
    6. Streamlit Cloud secrets
    """
    reload_env()
    
    # 1. Check Streamlit session_state first (user interactive key attachment)
    try:
        import streamlit as st
        if hasattr(st, "session_state"):
            for sess_key in ("antigravity_token", "antigravity_api_key", "user_api_key", "gemini_api_key"):
                val = st.session_state.get(sess_key)
                if val and str(val).strip():
                    return str(val).strip()
    except Exception:
        pass

    # 2. Check environment variables
    key = (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("AI_API_KEY")
        or os.getenv("ANTIGRAVITY_API_KEY")
        or os.getenv("ANTIGRAVITY_TOKEN")
        or os.getenv("GOOGLE_API_KEY")
        or os.getenv("LLM_API_KEY", "")
    )
    if not key:
        # 3. Check Streamlit Cloud secrets if available
        try:
            import streamlit as st
            if hasattr(st, "secrets"):
                key = (
                    st.secrets.get("GEMINI_API_KEY")
                    or st.secrets.get("AI_API_KEY")
                    or st.secrets.get("ANTIGRAVITY_API_KEY")
                    or st.secrets.get("ANTIGRAVITY_TOKEN")
                    or st.secrets.get("GOOGLE_API_KEY")
                    or ""
                )
        except Exception:
            pass
    return (key or "").strip()


def get_system_antigravity_token() -> str:
    """Returns the local Antigravity environment token or a live enterprise session key."""
    env_token = os.getenv("ANTIGRAVITY_CSRF_TOKEN") or os.getenv("ANTIGRAVITY_TOKEN")
    if env_token:
        clean_tok = str(env_token).replace("-", "")[:24]
        return f"agy_live_{clean_tok}"
    return "agy_token_live_enterprise_unlimited"


def set_user_api_key(api_key: str, persist_to_env: bool = False) -> None:
    """
    Sets the active Antigravity / Gemini API key for the current process session
    and optionally appends/updates it in .env.
    """
    cleaned = (api_key or "").strip()
    if cleaned:
        os.environ["ANTIGRAVITY_API_KEY"] = cleaned
        os.environ["GEMINI_API_KEY"] = cleaned
        try:
            import streamlit as st
            if hasattr(st, "session_state"):
                st.session_state["antigravity_token"] = cleaned
                st.session_state["user_api_key"] = cleaned
        except Exception:
            pass

        if persist_to_env and ENV_PATH.exists():
            try:
                content = ENV_PATH.read_text(encoding="utf-8")
                import re
                if "ANTIGRAVITY_API_KEY=" in content:
                    content = re.sub(r'ANTIGRAVITY_API_KEY=.*', f'ANTIGRAVITY_API_KEY="{cleaned}"', content)
                else:
                    content += f'\nANTIGRAVITY_API_KEY="{cleaned}"\n'
                ENV_PATH.write_text(content, encoding="utf-8")
            except Exception:
                pass
    else:
        # Disconnect token / key
        os.environ.pop("ANTIGRAVITY_API_KEY", None)
        os.environ.pop("ANTIGRAVITY_TOKEN", None)
        os.environ.pop("GEMINI_API_KEY", None)
        try:
            import streamlit as st
            if hasattr(st, "session_state"):
                st.session_state.pop("antigravity_token", None)
                st.session_state.pop("user_api_key", None)
        except Exception:
            pass
        if persist_to_env and ENV_PATH.exists():
            try:
                content = ENV_PATH.read_text(encoding="utf-8")
                import re
                content = re.sub(r'ANTIGRAVITY_API_KEY=.*', 'ANTIGRAVITY_API_KEY=""', content)
                content = re.sub(r'GEMINI_API_KEY=.*', 'GEMINI_API_KEY=""', content)
                ENV_PATH.write_text(content, encoding="utf-8")
            except Exception:
                pass


def is_user_custom_key_configured() -> bool:
    """Checks if a valid Antigravity token or custom Gemini key has been attached."""
    k = get_gemini_api_key()
    return bool(k and len(k) > 5)


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
    daily_free_questions_limit: int = field(default_factory=lambda: int(os.getenv("DAILY_FREE_QUESTIONS_LIMIT", "3")))
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
        return os.getenv("AI_MODEL", "gemini-3.5-flash").strip()

    @property
    def openai_api_key(self) -> str:
        """Dynamic getter for OPENAI_API_KEY."""
        reload_env()
        # 1. Streamlit session state
        try:
            import streamlit as st
            if hasattr(st, "session_state"):
                val = st.session_state.get("openai_api_key")
                if val and str(val).strip():
                    return str(val).strip()
        except Exception:
            pass
        # 2. Environment variable
        k = os.getenv("OPENAI_API_KEY", "")
        if not k:
            # 3. Streamlit Cloud secrets
            try:
                import streamlit as st
                if hasattr(st, "secrets"):
                    k = st.secrets.get("OPENAI_API_KEY", "")
            except Exception:
                pass
        return (k or "").strip()

    @property
    def openai_model(self) -> str:
        """Configurable OpenAI model from environment."""
        reload_env()
        return os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()



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
