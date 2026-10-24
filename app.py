"""
GLOBAL FUELPULSE AI — EDITORIAL INDUSTRIAL ENERGY INTELLIGENCE PLATFORM
Main Application Entrypoint & Modular Navigation Controller.
Architecture: Modular view routing, sub-50ms caching hierarchy, and unified editorial design.
"""

import os
import sys
import re
from pathlib import Path
from dotenv import load_dotenv

# Ensure project root AND src directory are ALWAYS at the front of sys.path (crucial for Streamlit Cloud)
ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"

# Strip conflicting parent mount directories (such as /mount/src on Streamlit Cloud)
parent_mount = ROOT_DIR.parent
sys.path = [p for p in sys.path if Path(p).resolve() != parent_mount and Path(p).resolve() != parent_mount.parent]

for d in [str(ROOT_DIR), str(SRC_DIR)]:
    while d in sys.path:
        sys.path.remove(d)
    sys.path.insert(0, d)

# Ensure .env is loaded using absolute path from project root
ENV_FILE = ROOT_DIR / ".env"
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE, override=True)

import streamlit as st
import pandas as pd
from datetime import datetime

from config.settings import settings
try:
    from src.database.connection import db_manager
    from src.database.migrations import init_database
except (ImportError, ModuleNotFoundError):
    from database.connection import db_manager
    from database.migrations import init_database

try:
    from src.ui_components import (
        apply_theme,
        render_command_strip,
        render_html,
        get_brand_logo_svg,
        get_logo_mark_svg,
        get_news_globe_icon_svg,
        get_fuel_client_logo_html,
        render_app_header_brand_html,
        render_universal_top_header,
        render_universal_ai_assistant,
        render_two_tier_nav_html,
        render_two_tier_navigation,
        show_sign_in_dialog,
        get_lucide_icon_svg,
        COLOR_AMBER,
        COLOR_WHITE,
        COLOR_INK,
        COLOR_GRAY_MUTED
    )
except (ImportError, ModuleNotFoundError):
    from ui_components import (
        apply_theme,
        render_command_strip,
        render_html,
        get_brand_logo_svg,
        get_logo_mark_svg,
        get_news_globe_icon_svg,
        get_fuel_client_logo_html,
        render_app_header_brand_html,
        render_universal_top_header,
        render_universal_ai_assistant,
        render_two_tier_nav_html,
        render_two_tier_navigation,
        show_sign_in_dialog,
        get_lucide_icon_svg,
        COLOR_AMBER,
        COLOR_WHITE,
        COLOR_INK,
        COLOR_GRAY_MUTED
    )

try:
    from src.localization.i18n import (
        t,
        get_current_language,
        set_language,
        get_available_languages,
        get_localized_nav_map
    )
except (ImportError, ModuleNotFoundError):
    from localization.i18n import (
        t,
        get_current_language,
        set_language,
        get_available_languages,
        get_localized_nav_map
    )

# Modular Product Views
try:
    from src.views.home import render_home_view
    from src.views.dashboard import render_dashboard_view
    from src.views.india_center import render_india_center_view
    from src.views.about import render_about_view
    from src.views.how_it_works import render_how_it_works_view
    from src.views.features import render_features_view
    from src.views.data_trust import render_data_trust_view
    from src.views.methodology import render_methodology_view
    from src.views.roadmap import render_roadmap_view
    from src.views.faq import render_faq_view
except (ImportError, ModuleNotFoundError):
    from views.home import render_home_view
    from views.dashboard import render_dashboard_view
    from views.india_center import render_india_center_view
    from views.about import render_about_view
    from views.how_it_works import render_how_it_works_view
    from views.features import render_features_view
    from views.data_trust import render_data_trust_view
    from views.methodology import render_methodology_view
    from views.roadmap import render_roadmap_view
    from views.faq import render_faq_view


# 1. Page Configuration
st.set_page_config(
    page_title="GLOBAL FUELPULSE AI — Energy Flows",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply global dark obsidian & glassmorphic styling
apply_theme()


# 2. Database Initialization (Cached)
@st.cache_resource(show_spinner=False)
def ensure_database_ready():
    """Initializes and seeds the database once per session."""
    try:
        init_database(seed_if_empty=True)
        return True
    except Exception:
        return False

ensure_database_ready()

# 2.5 Handle OAuth Return Callbacks (Supabase Google / GitHub)
render_html("""
<script>
(function() {
    if (window.location.hash && window.location.hash.includes('access_token=')) {
        var hash = window.location.hash.substring(1);
        var params = new URLSearchParams(hash);
        var token = params.get('access_token');
        if (token) {
            var searchParams = new URLSearchParams(window.location.search);
            searchParams.set('access_token', token);
            window.location.replace(window.location.pathname + '?' + searchParams.toString());
        }
    }
})();
</script>
""", container=st.sidebar)

if hasattr(st, "query_params"):
    qp_code = st.query_params.get("code")
    qp_token = st.query_params.get("access_token")
    qp_err = st.query_params.get("error") or st.query_params.get("error_description")

    if qp_err:
        st.error(f"Authentication Error: {st.query_params.get('error_description') or qp_err}")
        st.query_params.clear()
    elif qp_code or qp_token:
        try:
            from src.auth.auth_service import AuthService
            ok, msg, token, udict = AuthService.handle_oauth_callback(
                code=qp_code,
                access_token=qp_token,
                user_agent="GlobalFuelPulse/2.0 Browser"
            )
            if ok and udict:
                st.session_state["auth_user"] = udict
                st.session_state["auth_token"] = token
                st.toast(f"Signed in as {udict.get('full_name') or udict.get('username')} via {udict.get('provider', 'OAuth')}!")
            else:
                st.error(f"Sign In Notice: {msg}")
        except Exception as e:
            st.error(f"OAuth callback handling exception: {e}")
        finally:
            st.query_params.clear()
            st.rerun()


# 3. Navigation Structure & URL Routing
current_lang = get_current_language()

CANONICAL_TABS = [
    "home",
    "dashboard",
    "india",
    "about",
    "how_it_works",
    "features",
    "data_trust",
    "methodology",
    "roadmap",
    "faq"
]

NAV_MAP = {
    "🏠 Overview": "home",
    "⚡ Intelligence Dashboard": "dashboard",
    "🇮🇳 India Fuel Center": "india",
    "📖 About Project": "about",
    "⚙️ How It Works": "how_it_works",
    "📋 Features": "features",
    "🔒 Data Trust": "data_trust",
    "📐 Methodology": "methodology",
    "🗺️ Roadmap": "roadmap",
    "❓ Docs & FAQ": "faq"
}

KEY_TO_NAV = {v: k for k, v in NAV_MAP.items()}

# URL Query Param Synchronization
qp_tab = st.query_params.get("tab") or st.query_params.get("view")
if qp_tab:
    if isinstance(qp_tab, list):
        qp_tab = qp_tab[0]
    tab_aliases = {
        "trust": "data_trust",
        "data-trust": "data_trust",
        "architecture": "how_it_works",
        "center": "india",
        "overview": "home",
    }
    canonical_tab = tab_aliases.get(str(qp_tab).lower().strip(), str(qp_tab).lower().strip())
    if canonical_tab in CANONICAL_TABS:
        st.session_state.active_canonical = canonical_tab
elif "active_canonical" not in st.session_state:
    st.session_state.active_canonical = "home"

# Maintain backwards compatibility for tests and legacy callers
st.session_state.active_nav = KEY_TO_NAV.get(st.session_state.active_canonical, "🏠 Overview")


def navigate_to(target: str):
    """Central programmatic navigation function updating state, query parameters, and triggering rerun."""
    alias_map = {
        "home": "home",
        "overview": "home",
        "🏠 overview": "home",
        "dashboard": "dashboard",
        "live intelligence dashboard": "dashboard",
        "open dashboard": "dashboard",
        "open dashboard →": "dashboard",
        "⚡ intelligence dashboard": "dashboard",
        "india": "india",
        "india fuel center": "india",
        "open india center": "india",
        "open india center →": "india",
        "🇮🇳 india fuel center": "india",
        "about": "about",
        "about the project": "about",
        "📖 about project": "about",
        "how it works": "how_it_works",
        "how it works & architecture": "how_it_works",
        "architecture": "how_it_works",
        "⚙️ how it works": "how_it_works",
        "features": "features",
        "features catalog": "features",
        "📋 features": "features",
        "data trust": "data_trust",
        "trust": "data_trust",
        "data trust center": "data_trust",
        "data trust & provenance": "data_trust",
        "open trust center": "data_trust",
        "open trust center →": "data_trust",
        "🔒 data trust": "data_trust",
        "methodology": "methodology",
        "methodology & calculations": "methodology",
        "📐 methodology": "methodology",
        "roadmap": "roadmap",
        "roadmap & status": "roadmap",
        "🗺️ roadmap": "roadmap",
        "faq": "faq",
        "docs & faq": "faq",
        "documentation & faq": "faq",
        "❓ docs & faq": "faq",
        "ai analyst": "dashboard",
        "ai_analyst": "dashboard",
        "ai": "dashboard",
        "gemini": "dashboard",
    }
    canonical = alias_map.get(target.strip().lower(), target if target in CANONICAL_TABS else "home")
    st.session_state.active_canonical = canonical
    st.session_state.active_nav = KEY_TO_NAV.get(canonical, "🏠 Overview")
    st.query_params["tab"] = canonical
    st.query_params["lang"] = st.session_state.get("app_language", current_lang)
    st.rerun()


# 4. Sidebar Workspace Switcher & Navigation System (Minimalist Tree Navigation)
def clean_nav_title(title: str) -> str:
    """Strip leading emoji symbols and whitespace for sleek SaaS styling."""
    return re.sub(r'^[^\w\s\(\)]+\s*', '', title, flags=re.UNICODE).strip() or title


# ==============================================================================
# 4. SIDEBAR WORKSPACE & MULTIPAGE NAVIGATION
# ==============================================================================
# The synchronized, comprehensive application sidebar is now managed centrally
# and rendered automatically via render_universal_top_header() across all routes.


# Auto-open sign-in dialog if query parameter ?login=1 or ?auth=1 is present
if st.query_params.get("login") in ("1", "true") or st.query_params.get("auth") in ("1", "true"):
    st.query_params.pop("login", None)
    st.query_params.pop("auth", None)
    show_sign_in_dialog()


# 5. Top Brand Header Strip with Synchronized Multi-Language and Intelligence Center
render_universal_top_header(active_page_name=st.session_state.get("active_canonical", "home"), key_prefix="app_root")

# 6. Active Canonical Navigation State
active_canonical = st.session_state.get("active_canonical", "home")
st.session_state.active_nav = KEY_TO_NAV.get(active_canonical, "🏠 Overview")


# 7. Modular View Router
if active_canonical == "home":
    render_home_view(navigate_to)
elif active_canonical == "dashboard":
    render_dashboard_view(navigate_to)
elif active_canonical == "india":
    render_india_center_view(navigate_to)
elif active_canonical == "about":
    render_about_view(navigate_to)
elif active_canonical == "how_it_works":
    render_how_it_works_view(navigate_to)
elif active_canonical == "features":
    render_features_view(navigate_to)
elif active_canonical == "data_trust":
    render_data_trust_view(navigate_to)
elif active_canonical == "methodology":
    render_methodology_view(navigate_to)
elif active_canonical == "roadmap":
    render_roadmap_view(navigate_to)
elif active_canonical == "faq":
    render_faq_view(navigate_to)
else:
    render_home_view(navigate_to)

# 8. Universal Floating AI Assistant Dock (Bottom-Right FAB on All Views)
render_universal_ai_assistant(context_page=active_canonical.replace("_", " ").title(), key_prefix="app_root")
