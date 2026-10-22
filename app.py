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
""")

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


# 4. Sidebar Brand Lockup
# 4. Sidebar Brand Lockup (WorkspaceSwitcher styling from dashboard-sidebar.tsx)
render_html(
    f"""
    <div style="display: flex; align-items: center; justify-content: space-between; padding: 8px 10px; margin-bottom: 12px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.08); background: rgba(255, 255, 255, 0.02); select-none;">
        <div style="display: flex; align-items: center; gap: 10px; min-width: 0;">
            <div style="width: 32px; height: 32px; min-width: 32px; border-radius: 6px; background: #F5B942; color: #0B101E; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; box-shadow: 0 1px 3px rgba(0,0,0,0.3);">
                FP
            </div>
            <div style="display: flex; flex-direction: column; overflow: hidden; min-width: 0;">
                <span style="font-size: 13px; font-weight: 600; line-height: 1.2; color: #F8FAFC; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{t('brand_title', current_lang)}</span>
                <span style="font-size: 11px; color: #94A3B8; line-height: 1.2; margin-top: 2px;">{t('brand_subtitle', current_lang)} · Live v2.0</span>
            </div>
        </div>
        <div style="color: rgba(148, 163, 184, 0.5); display: flex; align-items: center; shrink-0;">
            {get_lucide_icon_svg('chevron-down', size=15, color='#94A3B8')}
        </div>
    </div>
    """,
    container=st.sidebar
)

# Engine Health Badge (Sleek minimalist card)
health = db_manager.check_health()
engine_sym = "🟢" if health["connected"] else "🔴"
render_html(
    f"""
    <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 8px 10px; margin-bottom: 10px; font-size: 11px; line-height: 1.5; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 600; color: #71717A; text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 6px;">
                <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: {'#10B981' if health['connected'] else '#EF4444'};"></span>
                Engine
            </span>
            <span style="font-family: monospace; color: #E2E8F0; font-weight: 500;">{health['dialect'].upper()} · {health['database']}</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 3px;">
            <span style="font-weight: 600; color: #71717A; text-transform: uppercase; letter-spacing: 0.05em;">Pipeline</span>
            <span style="font-size: 10px; font-weight: 600; background: rgba(16, 185, 129, 0.12); color: #10B981; padding: 1px 6px; border-radius: 4px; border: 1px solid rgba(16, 185, 129, 0.25);">{'VERIFIED' if settings.is_demo_mode else 'LIVE 2026'}</span>
        </div>
    </div>
    """,
    container=st.sidebar
)

# User Account & Sign In Console in Sidebar
auth_user = st.session_state.get("auth_user")
if auth_user:
    disp_name = (auth_user.get("full_name") or auth_user.get("username") or "Analyst")
    user_email = auth_user.get("email", "")
    initials = (disp_name[0] if disp_name else "A").upper()
    render_html(
        f"""
        <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 8px 10px; margin-bottom: 8px; display: flex; align-items: center; gap: 10px;">
            <div style="width: 28px; height: 28px; border-radius: 6px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #10B981; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700;">
                {initials}
            </div>
            <div style="overflow: hidden; min-width: 0;">
                <div style="font-size: 10px; color: #10B981; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">● Active Session</div>
                <div style="font-size: 12px; font-weight: 600; color: #F8FAFC; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{disp_name}</div>
            </div>
        </div>
        """,
        container=st.sidebar
    )
    if st.sidebar.button("👤 Manage Account / Logout", key="sb_manage_account_btn", use_container_width=True):
        show_sign_in_dialog()
else:
    render_html(
        """
        <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 8px 10px; margin-bottom: 8px; display: flex; align-items: center; gap: 10px;">
            <div style="width: 28px; height: 28px; border-radius: 6px; background: rgba(245, 185, 66, 0.15); border: 1px solid rgba(245, 185, 66, 0.3); color: #F5B942; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700;">
                🔐
            </div>
            <div>
                <div style="font-size: 10px; color: #F5B942; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Client Access</div>
                <div style="font-size: 11px; color: #94A3B8;">3 free AI questions / 24h</div>
            </div>
        </div>
        """,
        container=st.sidebar
    )
    if st.sidebar.button("🔐 Sign In / Create Account", key="sb_signin_btn", type="primary", use_container_width=True):
        show_sign_in_dialog()

st.sidebar.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

# Auto-open sign-in dialog if query parameter ?login=1 or ?auth=1 is present
if st.query_params.get("login") in ("1", "true") or st.query_params.get("auth") in ("1", "true"):
    st.query_params.pop("login", None)
    st.query_params.pop("auth", None)
    show_sign_in_dialog()

# Authentic Navigation Items matching dashboard-sidebar.tsx
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

render_html(f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 600; color: #71717A; text-transform: uppercase; letter-spacing: 0.08em; padding: 4px 4px 6px 4px;">
    {t('sidebar_tree_nav', current_lang)}
</div>
""", container=st.sidebar)

for item in TREE_NAV_ITEMS:
    is_active = (item["tab"] == st.session_state.active_canonical)
    badge_str = f" · {item['badge']}" if item.get("badge") else ""
    btn_label = f"{item['label']}{badge_str}"
    if st.sidebar.button(btn_label, key=f"sb_nav_btn_{item['tab']}", type="primary" if is_active else "secondary", use_container_width=True):
        navigate_to(item["tab"])


# Live Pipeline Refresh Controls & Timestamps (Group Header styling from dashboard-sidebar.tsx)
render_html(f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 600; color: #71717A; text-transform: uppercase; letter-spacing: 0.08em; padding: 14px 4px 6px 4px;">
    ⚡ {t('sidebar_sync_title', current_lang)}
</div>
""", container=st.sidebar)

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
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; color: #94A3B8; margin-bottom: 14px; background: rgba(255, 255, 255, 0.02); padding: 8px 10px; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; line-height: 1.6;">
        <div style="font-weight: 600; color: #CBD5E1; margin-bottom: 4px; display: flex; align-items: center; justify-content: space-between;">
            <span>{t('sidebar_provenance_title', current_lang)}</span>
            <span style="font-size: 9px; color: #64748B;">SYNCED</span>
        </div>
        <div style="display: flex; justify-content: space-between; color: #94A3B8;"><span>• EIA & FRED</span><span style="font-weight: 600; color: #F5B942;">{last_eia}</span></div>
        <div style="display: flex; justify-content: space-between; color: #94A3B8;"><span>• PPAC India</span><span style="font-weight: 600; color: #F5B942;">{last_ppac}</span></div>
        <div style="display: flex; justify-content: space-between; color: #94A3B8;"><span>• FX Rates</span><span style="font-weight: 600; color: #F5B942;">{last_fx}</span></div>
    </div>
    """,
    container=st.sidebar
)

# Deep Drill-Down Pages in Sidebar rendered with Tree Rail hierarchy
render_html(f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 600; color: #71717A; text-transform: uppercase; letter-spacing: 0.08em; padding: 4px 4px 6px 4px;">
    🌿 {t('sidebar_drilldown', current_lang)}
</div>
""", container=st.sidebar)

render_html(
    f"""
    <div style="position: relative; padding-left: 12px; margin-left: 6px; border-left: 1px solid rgba(255, 255, 255, 0.08); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; line-height: 2.1;">
        <div style="position: absolute; bottom: 0; left: -3px; width: 5px; height: 5px; border-radius: 50%; background: #60A5FA;"></div>
        <div><a href="/Global_Command_Center" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center; padding: 2px 6px; border-radius: 4px; transition: all 0.15s ease;" onmouseover="this.style.background='rgba(255,255,255,0.05)'; this.style.color='#FFFFFF';" onmouseout="this.style.background='transparent'; this.style.color='#94A3B8';"><span style="color: #CBD5E1;">{t('sidebar_01_command', current_lang)}</span><span style="font-size: 10px; font-weight: 500; background: rgba(59,130,246,0.12); color: #60A5FA; border: 1px solid rgba(59,130,246,0.25); padding: 0 6px; border-radius: 9999px;">Exec</span></a></div>
        <div><a href="/Fuel_Price_Explorer" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center; padding: 2px 6px; border-radius: 4px; transition: all 0.15s ease;" onmouseover="this.style.background='rgba(255,255,255,0.05)'; this.style.color='#FFFFFF';" onmouseout="this.style.background='transparent'; this.style.color='#94A3B8';"><span style="color: #CBD5E1;">{t('sidebar_02_explorer', current_lang)}</span><span style="font-size: 10px; font-weight: 500; background: rgba(59,130,246,0.12); color: #60A5FA; border: 1px solid rgba(59,130,246,0.25); padding: 0 6px; border-radius: 9999px;">Daily</span></a></div>
        <div><a href="/Global_Trade" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center; padding: 2px 6px; border-radius: 4px; transition: all 0.15s ease;" onmouseover="this.style.background='rgba(255,255,255,0.05)'; this.style.color='#FFFFFF';" onmouseout="this.style.background='transparent'; this.style.color='#94A3B8';"><span style="color: #CBD5E1;">{t('sidebar_03_trade', current_lang)}</span><span style="font-size: 10px; font-weight: 500; background: rgba(59,130,246,0.12); color: #60A5FA; border: 1px solid rgba(59,130,246,0.25); padding: 0 6px; border-radius: 9999px;">Comtrade</span></a></div>
        <div><a href="/Affordability" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center; padding: 2px 6px; border-radius: 4px; transition: all 0.15s ease;" onmouseover="this.style.background='rgba(255,255,255,0.05)'; this.style.color='#FFFFFF';" onmouseout="this.style.background='transparent'; this.style.color='#94A3B8';"><span style="color: #CBD5E1;">{t('sidebar_04_afford', current_lang)}</span><span style="font-size: 10px; font-weight: 500; background: rgba(59,130,246,0.12); color: #60A5FA; border: 1px solid rgba(59,130,246,0.25); padding: 0 6px; border-radius: 9999px;">GDP/365</span></a></div>
        <div><a href="/Supply_Risk" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center; padding: 2px 6px; border-radius: 4px; transition: all 0.15s ease;" onmouseover="this.style.background='rgba(255,255,255,0.05)'; this.style.color='#FFFFFF';" onmouseout="this.style.background='transparent'; this.style.color='#94A3B8';"><span style="color: #CBD5E1;">{t('sidebar_05_risk', current_lang)}</span><span style="font-size: 10px; font-weight: 500; background: rgba(59,130,246,0.12); color: #60A5FA; border: 1px solid rgba(59,130,246,0.25); padding: 0 6px; border-radius: 9999px;">HHI</span></a></div>
        <div><a href="/Shock_Simulator" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center; padding: 2px 6px; border-radius: 4px; transition: all 0.15s ease;" onmouseover="this.style.background='rgba(255,255,255,0.05)'; this.style.color='#FFFFFF';" onmouseout="this.style.background='transparent'; this.style.color='#94A3B8';"><span style="color: #CBD5E1;">{t('sidebar_06_shock', current_lang)}</span><span style="font-size: 10px; font-weight: 500; background: rgba(59,130,246,0.12); color: #60A5FA; border: 1px solid rgba(59,130,246,0.25); padding: 0 6px; border-radius: 9999px;">Sens</span></a></div>
        <div><a href="/Forecasting" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center; padding: 2px 6px; border-radius: 4px; transition: all 0.15s ease;" onmouseover="this.style.background='rgba(255,255,255,0.05)'; this.style.color='#FFFFFF';" onmouseout="this.style.background='transparent'; this.style.color='#94A3B8';"><span style="color: #CBD5E1;">{t('sidebar_07_forecast', current_lang)}</span><span style="font-size: 10px; font-weight: 500; background: rgba(59,130,246,0.12); color: #60A5FA; border: 1px solid rgba(59,130,246,0.25); padding: 0 6px; border-radius: 9999px;">Holt-W</span></a></div>
        <div><a href="/Data_Trust" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center; padding: 2px 6px; border-radius: 4px; transition: all 0.15s ease;" onmouseover="this.style.background='rgba(255,255,255,0.05)'; this.style.color='#FFFFFF';" onmouseout="this.style.background='transparent'; this.style.color='#94A3B8';"><span style="color: #CBD5E1;">{t('sidebar_08_trust', current_lang)}</span><span style="font-size: 10px; font-weight: 500; background: rgba(59,130,246,0.12); color: #60A5FA; border: 1px solid rgba(59,130,246,0.25); padding: 0 6px; border-radius: 9999px;">Health</span></a></div>
        <div><a href="/AI_Analyst" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center; padding: 2px 6px; border-radius: 4px; transition: all 0.15s ease;" onmouseover="this.style.background='rgba(255,255,255,0.05)'; this.style.color='#FFFFFF';" onmouseout="this.style.background='transparent'; this.style.color='#94A3B8';"><span style="color: #CBD5E1;">{t('sidebar_09_ai', current_lang)}</span><span style="font-size: 10px; font-weight: 500; background: rgba(59,130,246,0.12); color: #60A5FA; border: 1px solid rgba(59,130,246,0.25); padding: 0 6px; border-radius: 9999px;">Gemini</span></a></div>
        <div><a href="/India_Intelligence" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center; padding: 2px 6px; border-radius: 4px; transition: all 0.15s ease;" onmouseover="this.style.background='rgba(255,255,255,0.05)'; this.style.color='#FFFFFF';" onmouseout="this.style.background='transparent'; this.style.color='#94A3B8';"><span style="color: #CBD5E1;">{t('sidebar_10_india', current_lang)}</span><span style="font-size: 10px; font-weight: 500; background: rgba(59,130,246,0.12); color: #60A5FA; border: 1px solid rgba(59,130,246,0.25); padding: 0 6px; border-radius: 9999px;">PPAC</span></a></div>
        <div><a href="/Product_Guide" style="color: #94A3B8; text-decoration: none; display: flex; justify-content: space-between; align-items: center; padding: 2px 6px; border-radius: 4px; transition: all 0.15s ease;" onmouseover="this.style.background='rgba(255,255,255,0.05)'; this.style.color='#FFFFFF';" onmouseout="this.style.background='transparent'; this.style.color='#94A3B8';"><span style="color: #CBD5E1;">{t('sidebar_11_guide', current_lang)}</span><span style="font-size: 10px; font-weight: 500; background: rgba(59,130,246,0.12); color: #60A5FA; border: 1px solid rgba(59,130,246,0.25); padding: 0 6px; border-radius: 9999px;">Guide</span></a></div>
    </div>
    <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); margin-top: 16px; padding-top: 8px;"></div>
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
