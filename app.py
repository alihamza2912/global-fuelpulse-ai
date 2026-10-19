"""
GLOBAL FUELPULSE AI — EDITORIAL INDUSTRIAL ENERGY INTELLIGENCE PLATFORM
Main Application Entrypoint & Modular Navigation Controller.
Architecture: Modular view routing, sub-50ms caching hierarchy, and unified editorial design.
"""

import os
import sys
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


# 4. Sidebar Brand Lockup
render_html(
    f"""
    <div style="padding: 10px 0 14px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 12px;">
        <div style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 1.15rem; font-weight: 800; color: #F9FAFB; display: flex; align-items: center; gap: 8px;">
            {get_lucide_icon_svg('zap', size=20, color='#F5B942')} {t('brand_title', current_lang)}
        </div>
        <div style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 0.74rem; color: #94A3B8; font-weight: 700; letter-spacing: 0.06em; margin-top: 2px;">
            {t('brand_subtitle', current_lang)} v2.0
        </div>
    </div>
    """,
    container=st.sidebar
)

# Engine Health Badge
health = db_manager.check_health()
engine_sym = "🟢" if health["connected"] else "🔴"
render_html(
    f"""
    <div style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 0.78rem; color: #F9FAFB; margin-bottom: 14px; background: rgba(14, 21, 38, 0.8); backdrop-filter: blur(12px); padding: 10px 12px; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; line-height: 1.5;">
        <div><b>ENGINE:</b> {engine_sym} {health['dialect'].upper()} &nbsp;|&nbsp; <b>REPOS:</b> {health['database']}</div>
        <div><b>TABLES:</b> {health['tables_count']} marts &nbsp;|&nbsp; <b>DATA:</b> {'VERIFIED' if settings.is_demo_mode else 'LIVE'}</div>
    </div>
    """,
    container=st.sidebar
)

# 21st.dev Authentic TreeNav Sidebar Component
TREE_NAV_ITEMS = [
    {"label": t("nav_overview", current_lang), "tab": "home", "canonical": "🏠 Overview", "badge": None},
    {"label": t("nav_dashboard", current_lang), "tab": "dashboard", "canonical": "⚡ Intelligence Dashboard", "badge": t("badge_live", current_lang)},
    {"label": t("nav_india", current_lang), "tab": "india", "canonical": "🇮🇳 India Fuel Center", "badge": "MoPNG"},
    {"label": t("nav_about", current_lang), "tab": "about", "canonical": "📖 About Project", "badge": "v2.0"},
    {"label": t("nav_how_it_works", current_lang), "tab": "how_it_works", "canonical": "⚙️ How It Works", "badge": None},
    {"label": t("nav_features", current_lang), "tab": "features", "canonical": "📋 Features", "badge": t("badge_12_mod", current_lang)},
    {"label": t("nav_data_trust", current_lang), "tab": "data_trust", "canonical": "🔒 Data Trust", "badge": "SLA"},
    {"label": t("nav_methodology", current_lang), "tab": "methodology", "canonical": "📐 Methodology", "badge": None},
    {"label": t("nav_roadmap", current_lang), "tab": "roadmap", "canonical": "🗺️ Roadmap", "badge": "New"},
    {"label": t("nav_faq", current_lang), "tab": "faq", "canonical": "❓ Docs & FAQ", "badge": t("badge_docs", current_lang)},
]

st.sidebar.markdown(f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 700; color: #71717A; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; padding-left: 2px;">
    {t('sidebar_tree_nav', current_lang)}
</div>
""", unsafe_allow_html=True)

for item in TREE_NAV_ITEMS:
    is_active = (item["tab"] == st.session_state.active_canonical)
    badge_str = f" [{item['badge']}]" if item.get("badge") else ""
    btn_label = f"{item['label']}{badge_str}"
    if st.sidebar.button(btn_label, key=f"sb_nav_btn_{item['tab']}", type="primary" if is_active else "secondary", use_container_width=True):
        navigate_to(item["tab"])


# Live Pipeline Refresh Controls & Timestamps
st.sidebar.markdown(f"### ⚡ {t('sidebar_sync_title', current_lang)}")
if st.sidebar.button(f"⚡ {t('sidebar_sync_btn', current_lang)}", key="sidebar_live_refresh_btn", use_container_width=True):
    with st.sidebar.status("Syncing live feeds (FRED, PPAC, EC, FX)..."):
        from src.ingestion.orchestrator import orchestrator
        orchestrator.run_live_refresh()
        st.cache_data.clear()
        st.sidebar.success("Live data refreshed!")
        st.rerun()

from src.ingestion.orchestrator import orchestrator
sync_times = orchestrator.get_last_sync_timestamps()
last_fx = sync_times.get("OPEN_ER_API") or "Today"
last_eia = sync_times.get("US_EIA") or "Today"
last_ppac = sync_times.get("INDIA_PPAC") or "Today"

render_html(
    f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.76rem; color: #94A3B8; margin-bottom: 16px; background: rgba(14, 21, 38, 0.6); padding: 10px; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 6px; line-height: 1.4;">
        <div style="font-weight: 800; color: #F9FAFB; margin-bottom: 4px;">{t('sidebar_provenance_title', current_lang)}</div>
        <div>• EIA & FRED: <span style="font-weight: 700; color: #F5B942;">{last_eia}</span></div>
        <div>• PPAC India: <span style="font-weight: 700; color: #F5B942;">{last_ppac}</span></div>
        <div>• FX Rates: <span style="font-weight: 700; color: #F5B942;">{last_fx}</span></div>
    </div>
    """,
    container=st.sidebar
)

# Deep Drill-Down Pages in Sidebar rendered with Tree Rail hierarchy
st.sidebar.markdown(f"### 🌿 {t('sidebar_drilldown', current_lang)}")
render_html(
    f"""
    <div style="position: relative; padding-left: 14px; margin-left: 4px; border-left: 2px solid rgba(255, 255, 255, 0.12); font-family: 'Space Grotesk', sans-serif; font-size: 0.81rem; line-height: 2.15; font-weight: 600;">
        <div style="position: absolute; bottom: 0; left: -4px; width: 6px; height: 6px; border-radius: 50%; background: #60A5FA;"></div>
        <div><a href="/Global_Command_Center" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">{t('sidebar_01_command', current_lang)}</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">Exec</span></a></div>
        <div><a href="/Fuel_Price_Explorer" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">{t('sidebar_02_explorer', current_lang)}</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">Daily</span></a></div>
        <div><a href="/Global_Trade" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">{t('sidebar_03_trade', current_lang)}</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">Comtrade</span></a></div>
        <div><a href="/Affordability" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">{t('sidebar_04_afford', current_lang)}</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">GDP/365</span></a></div>
        <div><a href="/Supply_Risk" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">{t('sidebar_05_risk', current_lang)}</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">HHI</span></a></div>
        <div><a href="/Shock_Simulator" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">{t('sidebar_06_shock', current_lang)}</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">Sens</span></a></div>
        <div><a href="/Forecasting" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">{t('sidebar_07_forecast', current_lang)}</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">Holt-W</span></a></div>
        <div><a href="/Data_Trust" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">{t('sidebar_08_trust', current_lang)}</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">Health</span></a></div>
        <div><a href="/AI_Analyst" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">{t('sidebar_09_ai', current_lang)}</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">Gemini</span></a></div>
        <div><a href="/India_Intelligence" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">{t('sidebar_10_india', current_lang)}</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">PPAC</span></a></div>
        <div><a href="/Product_Guide" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">{t('sidebar_11_guide', current_lang)}</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">Guide</span></a></div>
    </div>
    """,
    container=st.sidebar
)


# 5. Top Brand Header Strip with Synchronized Multi-Language and Intelligence Center
render_universal_top_header(active_page_name=st.session_state.get("active_canonical", "home"), key_prefix="app_root")

# 6. Structured Two-Tier Product Navigation
active_canonical = st.session_state.get("active_canonical", "home")
st.session_state.active_nav = KEY_TO_NAV.get(active_canonical, "🏠 Overview")
render_two_tier_navigation(current_lang, active_canonical, navigate_to)


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
