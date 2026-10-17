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

from src.localization.i18n import (
    t,
    get_current_language,
    set_language,
    get_available_languages,
    get_localized_nav_map
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
if "active_canonical" not in st.session_state:
    if qp_tab and qp_tab in CANONICAL_TABS:
        st.session_state.active_canonical = qp_tab
    else:
        st.session_state.active_canonical = "home"
elif qp_tab and qp_tab in CANONICAL_TABS and qp_tab != st.session_state.active_canonical:
    st.session_state.active_canonical = qp_tab

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
    }
    canonical = alias_map.get(target.strip().lower(), target if target in CANONICAL_TABS else "home")
    st.session_state.active_canonical = canonical
    st.session_state.active_nav = KEY_TO_NAV.get(canonical, "🏠 Overview")
    st.query_params["tab"] = canonical
    st.rerun()


# 4. Sidebar Brand Lockup
render_html(
    """
    <div style="padding: 10px 0 14px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 12px;">
        <div style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 1.15rem; font-weight: 800; color: #F9FAFB; display: flex; align-items: center; gap: 8px;">
            <span style="color: #3B82F6;">⚡</span> GLOBAL FUELPULSE AI
        </div>
        <div style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 0.74rem; color: #94A3B8; font-weight: 700; letter-spacing: 0.06em; margin-top: 2px;">
            ENERGY INTELLIGENCE PLATFORM v2.0
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
    {"label": "Overview", "tab": "home", "canonical": "🏠 Overview", "badge": None},
    {"label": "Intelligence Dashboard", "tab": "dashboard", "canonical": "⚡ Intelligence Dashboard", "badge": "Live"},
    {"label": "India Fuel Center", "tab": "india", "canonical": "🇮🇳 India Fuel Center", "badge": "MoPNG"},
    {"label": "About Platform", "tab": "about", "canonical": "📖 About Project", "badge": "v2.0"},
    {"label": "How It Works", "tab": "how_it_works", "canonical": "⚙️ How It Works", "badge": None},
    {"label": "Feature Catalog", "tab": "features", "canonical": "📋 Features", "badge": "12 Mod"},
    {"label": "Data Trust & SLAs", "tab": "data_trust", "canonical": "🔒 Data Trust", "badge": "SLA"},
    {"label": "Methodology", "tab": "methodology", "canonical": "📐 Methodology", "badge": None},
    {"label": "Product Roadmap", "tab": "roadmap", "canonical": "🗺️ Roadmap", "badge": "New"},
    {"label": "Documentation & FAQ", "tab": "faq", "canonical": "❓ Docs & FAQ", "badge": "Docs"},
]

active_idx = 0
for idx, item in enumerate(TREE_NAV_ITEMS):
    if item["canonical"] == st.session_state.active_nav:
        active_idx = idx
        break

ROW_H = 34
MARKER = 7
RAIL_X = 10
total_items = len(TREE_NAV_ITEMS)
end_y = total_items * ROW_H - ROW_H // 2
marker_y = active_idx * ROW_H + ROW_H // 2 - MARKER // 2

items_html = []
for idx, item in enumerate(TREE_NAV_ITEMS):
    is_active = (idx == active_idx)
    badge_html = f'<span style="display: inline-flex; height: 18px; align-items: center; border-radius: 6px; background: rgba(43, 127, 255, 0.14); padding: 0 6px; font-size: 11px; font-weight: 500; color: #60A5FA; line-height: 1;">{item["badge"]}</span>' if item.get("badge") else ''
    active_style = 'background: rgba(255, 255, 255, 0.08); color: #FFFFFF; font-weight: 500;' if is_active else 'color: #A1A1AA; font-weight: 400;'
    items_html.append(f"""
        <li style="position: relative; list-style: none; margin: 0; padding: 0;">
            <a href="?tab={item['tab']}" target="_self" style="display: flex; height: 32px; align-items: center; justify-content: space-between; border-radius: 8px; padding: 0 10px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13px; text-decoration: none; transition: all 0.15s ease-out; {active_style}">
                <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{item['label']}</span>
                {badge_html}
            </a>
        </li>
    """)

tree_nav_html = f"""
<div style="background: #09090b; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 12px 10px 14px 8px; margin-bottom: 16px; position: relative;">
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 600; color: #71717A; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; padding-left: 10px;">
        Tree Nav
    </div>
    <ul style="position: relative; display: flex; flex-direction: column; gap: 2px; padding-left: 24px; margin: 0; padding-right: 0;">
        <!-- Vertical Rail Track -->
        <span aria-hidden="true" style="pointer-events: none; position: absolute; top: 0; bottom: 0; left: 0; width: 20px;">
            <!-- Background Rail -->
            <span style="position: absolute; top: 16px; left: {RAIL_X}px; width: 1px; height: {end_y - 16}px; background: #27272a;"></span>
            <!-- Terminal Dot -->
            <span style="position: absolute; left: {RAIL_X - 1.5}px; top: {end_y - 2}px; width: 4px; height: 4px; border-radius: 50%; background: #3f3f46;"></span>
            <!-- Accent Rail (Pure White) -->
            <span style="position: absolute; top: 16px; left: {RAIL_X}px; width: 1px; height: {active_idx * ROW_H}px; background: #ffffff;"></span>
            <!-- Active Diamond Marker (Pure White 45deg) -->
            <span style="position: absolute; left: {RAIL_X - MARKER / 2 + 0.5}px; top: {marker_y + 1}px; width: {MARKER}px; height: {MARKER}px; background: #ffffff; transform: rotate(45deg); border-radius: 1px; box-shadow: 0 0 6px rgba(255, 255, 255, 0.8);"></span>
        </span>
        {''.join(items_html)}
    </ul>
</div>
"""
render_html(tree_nav_html, container=st.sidebar)

# Live Pipeline Refresh Controls & Timestamps
st.sidebar.markdown("### ⚡ Live Pipeline Sync")
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

# Deep Drill-Down Pages in Sidebar rendered with Tree Rail hierarchy
st.sidebar.markdown("### 🌿 Granular Drill-Down Tree")
render_html(
    """
    <div style="position: relative; padding-left: 14px; margin-left: 4px; border-left: 2px solid rgba(255, 255, 255, 0.12); font-family: 'Space Grotesk', sans-serif; font-size: 0.81rem; line-height: 2.15; font-weight: 600;">
        <div style="position: absolute; bottom: 0; left: -4px; width: 6px; height: 6px; border-radius: 50%; background: #60A5FA;"></div>
        <div><a href="/Global_Command_Center" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">01. 🌐 Command Center</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">Exec</span></a></div>
        <div><a href="/Fuel_Price_Explorer" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">02. ⛽ Fuel Explorer</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">Daily</span></a></div>
        <div><a href="/Global_Trade" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">03. 🚢 Trade Flows</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">Comtrade</span></a></div>
        <div><a href="/Affordability" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">04. ⚖️ Affordability</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">GDP/365</span></a></div>
        <div><a href="/Supply_Risk" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">05. 🛡️ Supply Risk</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">HHI</span></a></div>
        <div><a href="/Shock_Simulator" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">06. ⚡ Shock Simulator</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">Sens</span></a></div>
        <div><a href="/Forecasting" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">07. 📈 Forecasting Radar</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">Holt-W</span></a></div>
        <div><a href="/Data_Trust" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">08. 🔒 Data Trust Center</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">Health</span></a></div>
        <div><a href="/AI_Analyst" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">09. 🤖 AI Energy Analyst</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">Gemini</span></a></div>
        <div><a href="/India_Intelligence" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">10. 🇮🇳 India Intelligence</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">PPAC</span></a></div>
        <div><a href="/Product_Guide" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center;"><span style="color: #CBD5E1;">11. 📖 Product Guide</span><span style="font-size: 10px; background: rgba(59,130,246,0.15); color: #60A5FA; padding: 1px 6px; border-radius: 4px;">Guide</span></a></div>
    </div>
    """,
    container=st.sidebar
)


# 5. Top Brand Header Strip with Upper-Right Live Intelligence Notification Center
from src.analytics.global_news_engine import GlobalNewsEngine

top_left, top_lang, top_right = st.columns([5.5, 2.3, 2.2])
with top_left:
    health = db_manager.check_health()
    engine_name = "MYSQL 8.4" if health["dialect"] == "mysql" else "SQLITE VERIFIED"
    render_html(f"""
    <div style="background: rgba(14, 21, 38, 0.85); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.14); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); border-radius: 10px; padding: 8px 18px; margin: -0.5rem 0 0.5rem 0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            {get_brand_logo_svg(width=340, height=54)}
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="background: rgba(16, 185, 129, 0.18); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 3px 10px; border-radius: 999px; font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 700;">● {t('db_verified', current_lang)}</span>
            <span style="background: rgba(245, 185, 66, 0.18); color: #F5B942; border: 1px solid rgba(245, 185, 66, 0.4); padding: 3px 10px; border-radius: 999px; font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 700;">{t('live_indicator', current_lang)}</span>
        </div>
    </div>
    """)

with top_lang:
    all_langs = get_available_languages()
    lang_labels = {code: f"{data['flag']} {data['native']} ({data['name']})" for code, data in all_langs.items()}
    lang_codes = list(all_langs.keys())
    cur_lang_idx = lang_codes.index(current_lang) if current_lang in lang_codes else 0
    selected_lang = st.selectbox(
        "🌐 Language",
        options=lang_codes,
        index=cur_lang_idx,
        format_func=lambda code: lang_labels[code],
        label_visibility="collapsed",
        key="app_language_selector"
    )
    if selected_lang != current_lang:
        set_language(selected_lang)
        st.rerun()

with top_right:
    alerts_count = GlobalNewsEngine.get_active_alerts_count()
    news_btn_label = f"{t('live_news_button', current_lang)} ({alerts_count})"
    with st.popover(news_btn_label, use_container_width=True):
        st.markdown(f"### 📡 {t('brand_title', current_lang)} — Global Wire")
        
        c_btn, c_time = st.columns([1, 1])
        with c_btn:
            if st.button(t("refresh_feeds", current_lang), key="popover_refresh_news", use_container_width=True, type="primary"):
                GlobalNewsEngine.refresh_news()
                st.toast("Refreshed live global news & maritime feeds!", icon="📡")
                st.rerun()
        with c_time:
            st.caption(f"Sync: {GlobalNewsEngine.get_last_refresh_timestamp()}")

        tab_hormuz, tab_trade, tab_rates, tab_all = st.tabs([
            f"🚨 {t('nav_trade', current_lang)}",
            f"🚢 {t('chapter_03_title', current_lang)}",
            f"⛽ {t('chapter_05_title', current_lang)}",
            f"📰 {t('live_news_button', current_lang)}"
        ])
        
        with tab_hormuz:
            st.markdown("#### 🔴 Maritime Transit Risk Monitor")
            for chk in GlobalNewsEngine.get_chokepoint_telemetry():
                st.markdown(f"""
                <div style="background: rgba(14, 21, 38, 0.9); border: 1px solid rgba(255, 255, 255, 0.12); border-left: 4px solid {chk['status_color']}; border-radius: 6px; padding: 10px 12px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <b style="color: #F9FAFB; font-size: 0.9rem;">{chk['name']}</b>
                        <span style="background: rgba(239, 68, 68, 0.2); color: {chk['status_color']}; font-size: 0.7rem; font-weight: 800; padding: 2px 6px; border-radius: 4px;">{chk['status']}</span>
                    </div>
                    <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 4px;">Throughput: <b style="color: #F5B942;">{chk['throughput']}</b> ({chk['global_share']})</div>
                    <div style="font-size: 0.74rem; color: #CBD5E1; margin-top: 4px;"><b>Risk:</b> {chk['key_risk']}</div>
                    <div style="font-size: 0.72rem; color: #34D399; margin-top: 3px;"><b>Contingency:</b> {chk['contingency']}</div>
                </div>
                """, unsafe_allow_html=True)
                
        with tab_trade:
            st.markdown("#### 🚢 Global Petroleum Import & Export")
            for item in GlobalNewsEngine.get_live_news_feed(category="TRADE_FLOWS"):
                metrics_html = " ".join([f"<span style='background: rgba(59,130,246,0.18); color: #60A5FA; padding: 2px 6px; border-radius: 4px; font-size: 0.68rem;'><b>{k}:</b> {v}</span>" for k, v in item['metrics'].items()])
                st.markdown(f"""
                <div style="background: rgba(14, 21, 38, 0.9); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 6px; padding: 10px 12px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <b style="color: #F9FAFB; font-size: 0.85rem;">{item['headline']}</b>
                    </div>
                    <div style="font-size: 0.74rem; color: #94A3B8; margin: 4px 0;">{item['timestamp']} • Source: <i>{item['source']}</i></div>
                    <p style="font-size: 0.78rem; color: #CBD5E1; line-height: 1.4; margin-bottom: 6px;">{item['summary']}</p>
                    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                        {metrics_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        with tab_rates:
            st.markdown("#### ⛽ Verified Live Retail Rates Today (17 Oct 2026)")
            benchmarks = GlobalNewsEngine.get_live_delhi_and_metro_benchmarks()
            d = benchmarks["delhi"]
            st.markdown(f"""
            <div style="background: rgba(234, 179, 8, 0.12); border: 1.5px solid #CA8A04; border-radius: 8px; padding: 12px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 800; color: #EAB308; font-size: 0.92rem;">🇮🇳 DELHI (LIVE TODAY)</span>
                    <span style="background: #EAB308; color: #070A12; font-weight: 800; font-size: 0.68rem; padding: 2px 6px; border-radius: 4px;">PPAC VERIFIED</span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px;">
                    <div style="background: rgba(0,0,0,0.4); padding: 8px; border-radius: 6px;">
                        <div style="font-size: 0.72rem; color: #94A3B8;">Petrol RSP</div>
                        <div style="font-size: 1.25rem; font-weight: 800; color: #F9FAFB;">₹{d['petrol']:.2f}/L</div>
                    </div>
                    <div style="background: rgba(0,0,0,0.4); padding: 8px; border-radius: 6px;">
                        <div style="font-size: 0.72rem; color: #94A3B8;">Diesel RSP</div>
                        <div style="font-size: 1.25rem; font-weight: 800; color: #F9FAFB;">₹{d['diesel']:.2f}/L</div>
                    </div>
                </div>
                <div style="font-size: 0.74rem; color: #CBD5E1; margin-top: 8px; line-height: 1.4;">
                    • <b>Base Refinery Transfer:</b> ₹{d['base_petrol']:.2f}/L<br/>
                    • <b>Central Excise:</b> ₹{d['central_tax']:.2f}/L<br/>
                    • <b>Delhi State VAT (19.40%):</b> ₹{d['state_vat']:.2f}/L<br/>
                    • <b>Combined Tax Wedge:</b> ₹40.40/L ({d['tax_share_pct']}% of pump price)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**Other Indian Metros & Global:**")
            m = benchmarks["mumbai"]
            c = benchmarks["kolkata"]
            ch = benchmarks["chennai"]
            st.markdown(f"""
            <div style="font-size: 0.78rem; color: #94A3B8; line-height: 1.6;">
                • <b>Mumbai:</b> Petrol ₹{m['petrol']:.2f}/L | Diesel ₹{m['diesel']:.2f}/L (Tax: {m['tax_share_pct']}%)<br/>
                • <b>Kolkata:</b> Petrol ₹{c['petrol']:.2f}/L | Diesel ₹{c['diesel']:.2f}/L (Tax: {c['tax_share_pct']}%)<br/>
                • <b>Chennai:</b> Petrol ₹{ch['petrol']:.2f}/L | Diesel ₹{ch['diesel']:.2f}/L (Tax: {ch['tax_share_pct']}%)<br/>
                • <b>United States:</b> $3.24 / gal ($0.86/L)<br/>
                • <b>Germany (EU):</b> €1.78 / L ($1.94/L)<br/>
                • <b>United Kingdom:</b> £1.42 / L ($1.85/L)<br/>
                • <b>UAE:</b> AED 3.03 / L ($0.82/L)
            </div>
            """, unsafe_allow_html=True)
            
        with tab_all:
            st.markdown("#### 📰 Complete Real-Time Intelligence Chronology")
            for item in GlobalNewsEngine.get_live_news_feed():
                st.markdown(f"""
                <div style="background: rgba(14, 21, 38, 0.9); border: 1px solid rgba(255, 255, 255, 0.12); border-left: 3px solid {item['impact_color']}; border-radius: 6px; padding: 10px 12px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.7rem; font-weight: 700; color: #F5B942;">{item['category_label']}</span>
                        <span style="font-size: 0.65rem; background: rgba(255,255,255,0.08); color: {item['impact_color']}; padding: 1px 6px; border-radius: 4px; font-weight: 700;">{item['impact']}</span>
                    </div>
                    <b style="color: #F9FAFB; font-size: 0.84rem; display: block; margin: 4px 0;">{item['headline']}</b>
                    <div style="font-size: 0.72rem; color: #94A3B8; margin-bottom: 4px;">{item['timestamp']} • <i>{item['source']}</i></div>
                    <p style="font-size: 0.76rem; color: #CBD5E1; line-height: 1.4; margin-bottom: 6px;">{item['summary']}</p>
                </div>
                """, unsafe_allow_html=True)

# 6. Interactive Horizontal Product Ribbon Selector (Enlarged & Multi-Lingual)
localized_nav_map = get_localized_nav_map(current_lang)
label_to_canonical = {label: canonical for canonical, label in localized_nav_map.items()}
current_localized_options = list(localized_nav_map.values())
active_canonical = st.session_state.get("active_canonical", "home")
current_active_label = localized_nav_map.get(active_canonical, current_localized_options[0])

curr_idx = current_localized_options.index(current_active_label) if current_active_label in current_localized_options else 0
selected_nav_label = st.pills(
    "Navigation Portal",
    options=current_localized_options,
    selection_mode="single",
    default=current_localized_options[curr_idx],
    key=f"nav_pills_{current_lang}_{active_canonical}",
    label_visibility="collapsed"
)

if selected_nav_label and selected_nav_label != current_active_label:
    canonical = label_to_canonical.get(selected_nav_label, "home")
    st.session_state.active_canonical = canonical
    st.session_state.active_nav = KEY_TO_NAV.get(canonical, "🏠 Overview")
    st.query_params["tab"] = canonical
    st.rerun()


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
