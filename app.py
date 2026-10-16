"""
GLOBAL FUELPULSE AI — EDITORIAL INDUSTRIAL ENERGY INTELLIGENCE PLATFORM
Main Application Entrypoint & Modular Navigation Controller.
Architecture: Modular view routing, sub-50ms caching hierarchy, and unified editorial design.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure project root is ALWAYS in sys.path (crucial for Streamlit Cloud)
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Ensure .env is loaded using absolute path from project root
ENV_FILE = ROOT_DIR / ".env"
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE, override=True)

import streamlit as st
import pandas as pd
from datetime import datetime

from config.settings import settings
from src.database.connection import db_manager
from src.database.migrations import init_database

from src.ui_components import (
    apply_theme,
    render_command_strip,
    render_html,
    get_brand_logo_svg,
    get_fuel_client_logo_html,
    COLOR_AMBER,
    COLOR_WHITE,
    COLOR_INK,
    COLOR_GRAY_MUTED
)

# Modular Product Views
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
NAV_OPTIONS = [
    "🏠 Overview",
    "⚡ Intelligence Dashboard",
    "🇮🇳 India Fuel Center",
    "📖 About Project",
    "⚙️ How It Works",
    "📋 Features",
    "🔒 Data Trust",
    "📐 Methodology",
    "🗺️ Roadmap",
    "❓ Docs & FAQ"
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
if "active_nav" not in st.session_state:
    if qp_tab and qp_tab in KEY_TO_NAV:
        st.session_state.active_nav = KEY_TO_NAV[qp_tab]
    else:
        st.session_state.active_nav = "🏠 Overview"
elif qp_tab and qp_tab in KEY_TO_NAV and KEY_TO_NAV[qp_tab] != st.session_state.active_nav:
    st.session_state.active_nav = KEY_TO_NAV[qp_tab]


def navigate_to(target: str):
    """Central programmatic navigation function updating state, query parameters, and triggering rerun."""
    alias_map = {
        "home": "🏠 Overview",
        "overview": "🏠 Overview",
        "dashboard": "⚡ Intelligence Dashboard",
        "live intelligence dashboard": "⚡ Intelligence Dashboard",
        "india": "🇮🇳 India Fuel Center",
        "india fuel center": "🇮🇳 India Fuel Center",
        "about": "📖 About Project",
        "about the project": "📖 About Project",
        "how it works": "⚙️ How It Works",
        "how it works & architecture": "⚙️ How It Works",
        "architecture": "⚙️ How It Works",
        "features": "📋 Features",
        "features catalog": "📋 Features",
        "data trust": "🔒 Data Trust",
        "data trust center": "🔒 Data Trust",
        "methodology": "📐 Methodology",
        "methodology & calculations": "📐 Methodology",
        "roadmap": "🗺️ Roadmap",
        "roadmap & status": "🗺️ Roadmap",
        "faq": "❓ Docs & FAQ",
        "docs & faq": "❓ Docs & FAQ",
        "documentation & faq": "❓ Docs & FAQ",
    }
    canonical = alias_map.get(target.strip().lower(), target if target in NAV_OPTIONS else "🏠 Overview")
    st.session_state.active_nav = canonical
    st.query_params["tab"] = NAV_MAP.get(canonical, "home")
    st.rerun()


# 4. Sidebar Telemetry & Quick Navigation
render_html(
    """
    <div style="padding: 10px 0 16px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.12);">
        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; font-weight: 800; color: #F9FAFB;">GLOBAL FUELPULSE AI</div>
        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.78rem; color: #94A3B8; font-weight: 700; letter-spacing: 0.05em;">ENERGY INTELLIGENCE PLATFORM</div>
    </div>
    """,
    container=st.sidebar
)

# Engine Health Badge
health = db_manager.check_health()
engine_sym = "🟢" if health["connected"] else "🔴"
render_html(
    f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; color: #F9FAFB; margin-top: 12px; margin-bottom: 16px; background: rgba(14, 21, 38, 0.8); backdrop-filter: blur(12px); padding: 12px; border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3); border-radius: 6px; line-height: 1.5;">
        <div><b>DATA ENGINE:</b> {engine_sym} {health['dialect'].upper()}</div>
        <div><b>REPOSITORY:</b> {health['database']}</div>
        <div><b>ACTIVE TABLES:</b> {health['tables_count']} data marts</div>
        <div><b>STATUS:</b> {'VERIFIED BENCHMARKS' if settings.is_demo_mode else 'LIVE APIS'}</div>
    </div>
    """,
    container=st.sidebar
)

# Platform Portal Section in Sidebar
st.sidebar.markdown("### Platform Portal")
for opt in NAV_OPTIONS:
    is_active = (opt == st.session_state.active_nav)
    btn_label = f"▶ {opt}" if is_active else opt
    if st.sidebar.button(btn_label, key=f"side_portal_{opt}", use_container_width=True, type="primary" if is_active else "secondary"):
        navigate_to(opt)

# Live Pipeline Refresh Controls & Timestamps
st.sidebar.markdown("### Live Pipeline Sync")
if st.sidebar.button("⚡ Refresh Live Data", key="sidebar_live_refresh_btn", use_container_width=True):
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
        <div style="font-weight: 800; color: #F9FAFB; margin-bottom: 4px;">📡 DATA PROVENANCE & SYNC:</div>
        <div>• EIA & FRED: <span style="font-weight: 700; color: #F5B942;">{last_eia}</span></div>
        <div>• PPAC India: <span style="font-weight: 700; color: #F5B942;">{last_ppac}</span></div>
        <div>• FX Rates: <span style="font-weight: 700; color: #F5B942;">{last_fx}</span></div>
    </div>
    """,
    container=st.sidebar
)

# Deep Drill-Down Pages in Sidebar
st.sidebar.markdown("### Granular Drill-Down Pages")
render_html(
    """
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.82rem; line-height: 2.1; font-weight: 700;">
        <div>01. 🌐 <a href="/Global_Command_Center" style="color: #94A3B8; text-decoration: none;">Global Command Center</a></div>
        <div>02. ⛽ <a href="/Fuel_Price_Explorer" style="color: #94A3B8; text-decoration: none;">Fuel Price Explorer</a></div>
        <div>03. 🚢 <a href="/Global_Trade" style="color: #94A3B8; text-decoration: none;">Petroleum Trade & Flows</a></div>
        <div>04. ⚖️ <a href="/Affordability" style="color: #94A3B8; text-decoration: none;">Affordability Index</a></div>
        <div>05. 🛡️ <a href="/Supply_Risk" style="color: #94A3B8; text-decoration: none;">Supply Risk & Chokepoints</a></div>
        <div>06. ⚡ <a href="/Shock_Simulator" style="color: #94A3B8; text-decoration: none;">Shock Simulator</a></div>
        <div>07. 📈 <a href="/Forecasting" style="color: #94A3B8; text-decoration: none;">Forecasting & ML Radar</a></div>
        <div>08. 🔒 <a href="/Data_Trust" style="color: #94A3B8; text-decoration: none;">Data Trust Center</a></div>
        <div>09. 🤖 <a href="/AI_Analyst" style="color: #94A3B8; text-decoration: none;">AI Energy Analyst</a></div>
        <div>10. 🇮🇳 <a href="/India_Intelligence" style="color: #94A3B8; text-decoration: none;">India Intelligence</a></div>
        <div>11. 📖 <a href="/Product_Guide" style="color: #94A3B8; text-decoration: none;">Product Guide & Docs</a></div>
    </div>
    """,
    container=st.sidebar
)


# 5. Top Brand Navigation Strip
render_command_strip(
    active_page=st.session_state.active_nav,
    region_tag="GLOBAL & INDIA",
    product_tag="CRUDE OIL & FUELS",
    reporting_period="2024–2026 LIVE COVERAGE"
)

# 6. Interactive Horizontal Product Ribbon Selector
curr_idx = NAV_OPTIONS.index(st.session_state.active_nav) if st.session_state.active_nav in NAV_OPTIONS else 0
selected_nav = st.pills(
    "Navigation Portal",
    options=NAV_OPTIONS,
    default=NAV_OPTIONS[curr_idx],
    label_visibility="collapsed",
    key="global_nav_pills"
)

if selected_nav and selected_nav != st.session_state.active_nav:
    navigate_to(selected_nav)


# 7. Modular View Router
if st.session_state.active_nav == "🏠 Overview":
    render_home_view(navigate_to)
elif st.session_state.active_nav == "⚡ Intelligence Dashboard":
    render_dashboard_view(navigate_to)
elif st.session_state.active_nav == "🇮🇳 India Fuel Center":
    render_india_center_view(navigate_to)
elif st.session_state.active_nav == "📖 About Project":
    render_about_view(navigate_to)
elif st.session_state.active_nav == "⚙️ How It Works":
    render_how_it_works_view(navigate_to)
elif st.session_state.active_nav == "📋 Features":
    render_features_view(navigate_to)
elif st.session_state.active_nav == "🔒 Data Trust":
    render_data_trust_view(navigate_to)
elif st.session_state.active_nav == "📐 Methodology":
    render_methodology_view(navigate_to)
elif st.session_state.active_nav == "🗺️ Roadmap":
    render_roadmap_view(navigate_to)
elif st.session_state.active_nav == "❓ Docs & FAQ":
    render_faq_view(navigate_to)
else:
    render_home_view(navigate_to)
