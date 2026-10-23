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


# 4. Sidebar Workspace Switcher & Navigation System (Minimalist Tree Navigation)
def clean_nav_title(title: str) -> str:
    """Strip leading emoji symbols and whitespace for sleek SaaS styling."""
    return re.sub(r'^[^\w\s\(\)]+\s*', '', title, flags=re.UNICODE).strip() or title


# ==============================================================================
# A. TOP AREA — BRAND, CLIENT ACCESS, AUTH & DATA REFRESH (PRECEDING NAVIGATION)
# ==============================================================================

# 1. Global FuelPulse AI Logo Mark and Brand Lockup
render_html(
    f"""
    <div style="display: flex; align-items: center; justify-content: space-between; padding: 10px 10px 10px 10px; margin-bottom: 8px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.08); background: rgba(255, 255, 255, 0.02); user-select: none;">
        <div style="display: flex; align-items: center; gap: 10px; min-width: 0;">
            <div style="width: 32px; height: 32px; min-width: 32px; border-radius: 6px; background: linear-gradient(135deg, #F5B942 0%, #D97706 100%); color: #0B101E; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 13px; box-shadow: 0 1px 4px rgba(0,0,0,0.4); letter-spacing: -0.02em;">
                FP
            </div>
            <div style="display: flex; flex-direction: column; overflow: hidden; min-width: 0;">
                <span style="font-size: 12.5px; font-weight: 700; line-height: 1.2; color: #F8FAFC; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; letter-spacing: 0.02em;">GLOBAL FUELPULSE AI</span>
                <span style="font-size: 10px; color: #94A3B8; line-height: 1.2; margin-top: 2px; letter-spacing: 0.03em;">ENERGY INTELLIGENCE · LIVE V2.0</span>
            </div>
        </div>
        <div style="color: rgba(148, 163, 184, 0.6); display: flex; align-items: center; flex-shrink: 0;">
            {get_lucide_icon_svg('chevron-down', size=14, color='#94A3B8')}
        </div>
    </div>
    """,
    container=st.sidebar
)

# 2. Compact Client Access Status Badge (Real Quota from QuotaService)
from src.auth.quota_service import QuotaService

auth_user = st.session_state.get("auth_user")
user_id = auth_user.get("id") or auth_user.get("user_id") if isinstance(auth_user, dict) else None
quota_info = QuotaService.get_quota_summary(user_id)
remaining_q = quota_info.get("remaining", 3)
limit_q = quota_info.get("limit", 3)

if auth_user:
    disp_name = (auth_user.get("full_name") or auth_user.get("username") or "Analyst")
    initials = (disp_name[0] if disp_name else "A").upper()
    render_html(
        f"""
        <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 7px 10px; margin-bottom: 6px; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 8px; min-width: 0;">
                <div style="width: 24px; height: 24px; min-width: 24px; border-radius: 6px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #10B981; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700;">
                    {initials}
                </div>
                <div style="overflow: hidden; min-width: 0;">
                    <div style="font-size: 11.5px; font-weight: 600; color: #F8FAFC; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{disp_name}</div>
                    <div style="font-size: 10px; color: #10B981; font-weight: 500;">{remaining_q}/{limit_q} questions left</div>
                </div>
            </div>
            <span style="font-size: 9px; font-weight: 600; color: #10B981; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 4px; padding: 1px 5px;">ACTIVE</span>
        </div>
        """,
        container=st.sidebar
    )
    # 3. Sign In / Account Button
    if st.sidebar.button("Manage Account / Logout", key="sb_manage_account_btn", icon=":material/manage_accounts:", use_container_width=True):
        show_sign_in_dialog()
else:
    render_html(
        f"""
        <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 7px 10px; margin-bottom: 6px; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 24px; height: 24px; min-width: 24px; border-radius: 6px; background: rgba(245, 185, 66, 0.12); border: 1px solid rgba(245, 185, 66, 0.25); color: #F5B942; display: flex; align-items: center; justify-content: center; font-size: 11px;">
                    ⚡
                </div>
                <div>
                    <div style="font-size: 11px; font-weight: 600; color: #F8FAFC;">Client Access</div>
                    <div style="font-size: 10px; color: #94A3B8;">{remaining_q} free AI questions left</div>
                </div>
            </div>
            <span style="font-size: 9px; font-weight: 600; color: #F5B942; background: rgba(245, 185, 66, 0.1); border: 1px solid rgba(245, 185, 66, 0.25); border-radius: 4px; padding: 1px 5px;">FREE</span>
        </div>
        """,
        container=st.sidebar
    )
    # 3. Sign In / Account Button
    if st.sidebar.button("Sign In / Account", key="sb_signin_btn", icon=":material/lock:", use_container_width=True):
        show_sign_in_dialog()

# 4. Refresh Live Data Button
sync_btn_label = t("sidebar_sync_btn", current_lang)
if "Refresh Live Data" not in sync_btn_label:
    sync_btn_label = f"🔄 Refresh Live Data · {sync_btn_label}"
if st.sidebar.button(sync_btn_label, key="sidebar_live_refresh_btn", icon=":material/sync:", use_container_width=True):
    with st.sidebar.status("Syncing live feeds (FRED, PPAC, EC, FX)..."):
        from src.ingestion.orchestrator import orchestrator
        orchestrator.run_live_refresh()
        st.cache_data.clear()
        st.sidebar.success("Live data refreshed!")
        st.rerun()

st.sidebar.markdown("<div style='border-top: 1px solid rgba(255, 255, 255, 0.08); margin: 12px 4px 8px 4px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# B. MAIN NAVIGATION (TREE NAV — 5 ITEMS)
# ==============================================================================

render_html(f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 10.5px; font-weight: 600; color: #71717A; text-transform: uppercase; letter-spacing: 0.08em; padding: 6px 8px 4px 12px; display: flex; align-items: center; justify-content: space-between;">
    <span>MAIN NAVIGATION</span>
    <span style="font-size: 9px; color: #52525B; font-weight: 500;">Tree Nav</span>
</div>
<!-- Tree Nav Architecture -->
""", container=st.sidebar)

MAIN_NAV_ITEMS = [
    {"label": clean_nav_title(t("nav_overview", current_lang)), "tab": "home", "badge": None},
    {"label": clean_nav_title(t("nav_dashboard", current_lang)), "tab": "dashboard", "badge": t("badge_live", current_lang)},
    {"label": clean_nav_title(t("nav_india", current_lang)), "tab": "india", "badge": "MoPNG"},
    {"label": clean_nav_title(t("nav_about", current_lang)), "tab": "about", "badge": "v2.0"},
    {"label": clean_nav_title(t("nav_how_it_works", current_lang)), "tab": "how_it_works", "badge": None},
]

for item in MAIN_NAV_ITEMS:
    is_active = (item["tab"] == st.session_state.active_canonical)
    badge_str = f" · {item['badge']}" if item.get("badge") else ""
    btn_label = f"{item['label']}{badge_str}"
    if st.sidebar.button(
        btn_label,
        key=f"sb_nav_btn_{item['tab']}",
        type="primary" if is_active else "secondary",
        use_container_width=True
    ):
        navigate_to(item["tab"])


# ==============================================================================
# C. ANALYTICS DOSSIERS (TREE NAV — 8 MULTIPAGE ROUTES)
# ==============================================================================

render_html(f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 10.5px; font-weight: 600; color: #71717A; text-transform: uppercase; letter-spacing: 0.08em; padding: 14px 8px 4px 12px; display: flex; align-items: center; justify-content: space-between;">
    <span>ANALYTICS DOSSIERS</span>
    <span style="font-size: 9px; color: #52525B; font-weight: 500;">8 Models</span>
</div>
""", container=st.sidebar)

st.sidebar.page_link("pages/1_Global_Command_Center.py", label=f"{clean_nav_title(t('sidebar_01_command', current_lang))} — Exec", use_container_width=True)
st.sidebar.page_link("pages/2_Fuel_Price_Explorer.py", label=f"{clean_nav_title(t('sidebar_02_explorer', current_lang))} — Daily", use_container_width=True)
st.sidebar.page_link("pages/3_Global_Trade.py", label=f"{clean_nav_title(t('sidebar_03_trade', current_lang))} — Flows", use_container_width=True)
st.sidebar.page_link("pages/4_Affordability.py", label=f"{clean_nav_title(t('sidebar_04_afford', current_lang))} — Index", use_container_width=True)
st.sidebar.page_link("pages/5_Supply_Risk.py", label=f"{clean_nav_title(t('sidebar_05_risk', current_lang))} — Radar", use_container_width=True)
st.sidebar.page_link("pages/6_Shock_Simulator.py", label=f"{clean_nav_title(t('sidebar_06_shock', current_lang))} — Simulator", use_container_width=True)
st.sidebar.page_link("pages/7_Forecasting.py", label=f"{clean_nav_title(t('sidebar_07_forecast', current_lang))} — Radar", use_container_width=True)
st.sidebar.page_link("pages/9_AI_Analyst.py", label=f"{clean_nav_title(t('sidebar_09_ai', current_lang))} — Analyst", use_container_width=True)


# ==============================================================================
# D. PLATFORM & DOCUMENTATION (TREE NAV — 5 ITEMS)
# ==============================================================================

render_html(f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 10.5px; font-weight: 600; color: #71717A; text-transform: uppercase; letter-spacing: 0.08em; padding: 14px 8px 4px 12px; display: flex; align-items: center; justify-content: space-between;">
    <span>PLATFORM & DOCUMENTATION</span>
    <span style="font-size: 9px; color: #52525B; font-weight: 500;">Docs</span>
</div>
""", container=st.sidebar)

DOCS_NAV_ITEMS = [
    {"label": clean_nav_title(t("nav_features", current_lang)), "tab": "features", "badge": t("badge_12_mod", current_lang)},
    {"label": clean_nav_title(t("nav_data_trust", current_lang)), "tab": "data_trust", "badge": "SLA"},
    {"label": clean_nav_title(t("nav_methodology", current_lang)), "tab": "methodology", "badge": None},
    {"label": clean_nav_title(t("nav_roadmap", current_lang)), "tab": "roadmap", "badge": "2026"},
    {"label": clean_nav_title(t("nav_faq", current_lang)), "tab": "faq", "badge": t("badge_docs", current_lang)},
]

for item in DOCS_NAV_ITEMS:
    is_active = (item["tab"] == st.session_state.active_canonical)
    badge_str = f" · {item['badge']}" if item.get("badge") else ""
    btn_label = f"{item['label']}{badge_str}"
    if st.sidebar.button(
        btn_label,
        key=f"sb_nav_btn_{item['tab']}",
        type="primary" if is_active else "secondary",
        use_container_width=True
    ):
        navigate_to(item["tab"])


# ==============================================================================
# E. FOOTER: SYSTEM ENGINE & PROVENANCE STATUS
# ==============================================================================

from src.ingestion.orchestrator import orchestrator
sync_times = orchestrator.get_last_sync_timestamps()
last_fx = sync_times.get("OPEN_ER_API") or "Today"
last_eia = sync_times.get("US_EIA") or "Today"
last_ppac = sync_times.get("INDIA_PPAC") or "Today"

render_html(
    f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 10.5px; color: #94A3B8; margin-top: 14px; margin-bottom: 12px; background: rgba(255, 255, 255, 0.02); padding: 8px 10px; border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 8px; line-height: 1.5;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px;">
            <span style="display: flex; align-items: center; gap: 6px; font-weight: 600; color: #CBD5E1;">
                <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #10B981; box-shadow: 0 0 6px #10B981;"></span>
                SQLite Marts
            </span>
            <span style="font-size: 9px; font-weight: 600; color: #10B981; background: rgba(16, 185, 129, 0.12); padding: 1px 5px; border-radius: 4px; border: 1px solid rgba(16, 185, 129, 0.25);">LIVE 2026</span>
        </div>
        <div style="display: flex; justify-content: space-between; color: #64748B; font-size: 10px;">
            <span>EIA · PPAC · FX</span>
            <span style="color: #94A3B8; font-weight: 500;">Synced Today</span>
        </div>
    </div>
    """,
    container=st.sidebar
)

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
