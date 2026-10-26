"""
Page 13: Live Maritime Oil Tanker Tracker & Satellite AIS Telemetry.
Visualizes real-time global crude supertankers (VLCC, ULCC, Suezmax, Aframax, Product Tankers, LNG)
with interactive realistic ocean map, vessel photo dossiers, live speed in knots, heading, dynamic ETA to destination, and cargo valuations.
"""

import sys
import base64
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"

parent_mount = ROOT_DIR.parent
sys.path = [p for p in sys.path if Path(p).resolve() != parent_mount and Path(p).resolve() != parent_mount.parent]

for d in [str(ROOT_DIR), str(SRC_DIR)]:
    while d in sys.path:
        sys.path.remove(d)
    sys.path.insert(0, d)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.ui_components import (
    render_page_header,
    render_universal_sidebar,
    render_universal_ai_assistant,
    render_universal_top_header,
    render_instrument_card,
    render_csv_download,
    apply_theme,
    render_html,
    clean_html,
    COLOR_INK,
    COLOR_AMBER,
    COLOR_WHITE
)
from src.localization.i18n import t, get_current_language
from src.analytics.live_tanker_tracker import LiveTankerTracker

def get_vessel_image_src(vessel: dict) -> str:
    """Returns local base64 data URI for verified tanker photography."""
    asset_rel = vessel.get("asset_image") or "assets/tankers/vlcc_supertanker.jpg"
    p = ROOT_DIR / asset_rel
    if not p.exists():
        p = ROOT_DIR / "assets/tankers/vlcc_supertanker.jpg"
    try:
        b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
        return f"data:image/jpeg;base64,{b64}"
    except Exception:
        return ""

# 1. Initialize Page Architecture
apply_theme()
current_lang = get_current_language()

render_page_header(
    title=t("ltt_title", current_lang),
    subtitle=t("ltt_subtitle", current_lang),
    source_tag=t("ltt_source_tag", current_lang),
    observation_date=t("ltt_observation_date", current_lang)
)

# -------------------------------------------------------------
# 2. CONTROL & FILTER CONSOLE
# -------------------------------------------------------------
radar_banner_text = t("ltt_radar_console", current_lang)
ais_lock_text = t("ltt_ais_lock", current_lang)

render_html(f"""
<div style="background: #0D1527; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 12px; padding: 14px 20px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: space-between;">
    <span style="font-size: 13px; font-weight: 800; color: #F5B942; text-transform: uppercase; letter-spacing: 0.08em; display: flex; align-items: center; gap: 8px;">
        {radar_banner_text}
    </span>
    <span style="background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.35); font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 999px;">
        {ais_lock_text}
    </span>
</div>
""")

with st.container(key="tanker_filters_row"):
    col_f1, col_f2, col_f3 = st.columns([2, 2, 3])

    with col_f1:
        cargo_choice = st.selectbox(
            t("ltt_commodity_type", current_lang),
            options=[
                ("all", t("ltt_all_commodities", current_lang)),
                ("crude", t("ltt_crude_oil", current_lang)),
                ("product", t("ltt_refined_products", current_lang)),
                ("lng", t("ltt_lng_carriers", current_lang))
            ],
            format_func=lambda x: x[1],
            index=0,
            key="tanker_filter_cargo"
        )[0]

    with col_f2:
        class_choice = st.selectbox(
            t("ltt_vessel_class", current_lang),
            options=["all", "VLCC", "ULCC", "Suezmax", "Aframax", "LR2", "LR1", "Q-Max"],
            format_func=lambda x: t("ltt_all_classes", current_lang) if x == "all" else f"{t('tbl_vessel_class', current_lang)}: {x}",
            index=0,
            key="tanker_filter_class"
        )

    with col_f3:
        search_query = st.text_input(
            t("ltt_search_label", current_lang),
            placeholder="e.g. Maran Canopus, Ras Tanura, 9784532, India...",
            key="tanker_search_query"
        )

# -------------------------------------------------------------
# 3. COMPUTE FLEET TELEMETRY & SUMMARY METRICS
# -------------------------------------------------------------
fleet_source_col1, fleet_source_col2 = st.columns([7, 3], vertical_alignment="center")
with fleet_source_col1:
    fleet_source = st.radio(
        "🛰️ Maritime AIS Telemetry Feed",
        options=["combined", "strategic", "live_open_ais"],
        format_func=lambda x: {
            "combined": "🌐 Combined Fleet (Strategic Giants + Live AIS Satellite Stream)",
            "strategic": "🛢️ Global Strategic Supertankers (Dynamic Live GPS Motion)",
            "live_open_ais": "🛰️ Open Marine Satellite AIS (100+ Real Tankers · Free Govt API)"
        }.get(x, x),
        horizontal=True,
        index=0,
        key="tanker_fleet_source_selector"
    )

fleet = LiveTankerTracker.get_combined_fleet(
    fleet_source=fleet_source,
    cargo_filter=cargo_choice,
    vessel_class_filter=class_choice,
    search_query=search_query,
    dynamic_motion=True
)
kpis = LiveTankerTracker.get_summary_kpis(fleet)

with fleet_source_col2:
    is_live_active = any(v.get("is_real_live_ais") for v in fleet)
    stat_color = "#10B981" if is_live_active else "#38BDF8"
    stat_label = "LIVE SATELLITE AIS STREAM" if is_live_active else "DYNAMIC GPS MOTION ACTIVE"
    render_html(f"""
    <div style="background: rgba(14, 21, 38, 0.85); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 8px; padding: 6px 12px; text-align: right;">
        <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: {stat_color}; box-shadow: 0 0 8px {stat_color};"></span>
        <span style="font-size: 11px; font-weight: 800; color: {stat_color}; letter-spacing: 0.04em;">{stat_label}</span>
        <div style="font-size: 11px; color: #94A3B8; margin-top: 2px;">{len(fleet)} Active Vessels · Sub-Minute Pings</div>
    </div>
    """)

# Elevated Midnight Scorecards (Universal 195px Equal-Height Standard)
m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    render_instrument_card(
        label=t("ltt_kpi_active_fleet", current_lang),
        value=f"{kpis['active_vessels']} Vessels",
        accent="amber",
        delta=t("ltt_kpi_ais_tracked", current_lang),
        delta_is_positive_bad=False,
        subtext=t("ltt_kpi_laden_voyages", current_lang)
    )

with m2:
    render_instrument_card(
        label=t("ltt_kpi_seaborne_barrels", current_lang),
        value=f"{kpis['total_barrels_at_sea'] / 1e6:,.1f}M bbl",
        accent="amber",
        delta=t("ltt_kpi_crude_refined", current_lang),
        delta_is_positive_bad=False,
        subtext=t("ltt_kpi_in_transit", current_lang)
    )

with m3:
    render_instrument_card(
        label=t("ltt_kpi_customs_value", current_lang),
        value=f"${kpis['total_cargo_value_usd'] / 1e9:.2f}B USD",
        accent="copper",
        delta=f"₹{kpis['total_cargo_value_usd'] * 83.2 / 1e7:,.0f} Cr",
        delta_is_positive_bad=False,
        subtext=t("ltt_kpi_spot_val", current_lang)
    )

with m4:
    render_instrument_card(
        label=t("ltt_kpi_avg_speed", current_lang),
        value=f"{kpis['avg_fleet_speed_knots']:.1f} Knots",
        accent="teal",
        delta=f"{kpis['avg_fleet_speed_knots'] * 1.852:.1f} km/h",
        delta_is_positive_bad=False,
        subtext=t("ltt_kpi_slow_steaming", current_lang)
    )

with m5:
    render_instrument_card(
        label=t("ltt_kpi_chokepoint_transit", current_lang),
        value=f"{kpis['at_risk_vessels']} Vessels",
        accent="red",
        delta="Hormuz / Red Sea",
        delta_is_positive_bad=True,
        subtext=t("ltt_kpi_war_risk", current_lang)
    )

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 4. PLAIN-ENGLISH EXPLORER: WHO IS CARRYING WHAT & WHERE ARE THEY GOING?
# -------------------------------------------------------------
vessel_options = [v["vessel_id"] for v in fleet] if fleet else []
vessel_map = {v["vessel_id"]: f"{v.get('flag_emoji', '🚢')} {v['name']} ({v.get('vessel_class', 'Tanker').split()[0]}) — {v.get('cargo_name', 'Petroleum')} ➔ {v.get('dest_port', 'Port').split()[0]}" for v in fleet}

with st.container(key="tanker_vessel_select_row"):
    col_sel, col_stats = st.columns([6, 4])
    with col_sel:
        selected_vessel_id = st.selectbox(
            t("ltt_select_vessel_label", current_lang),
            options=vessel_options,
            format_func=lambda x: vessel_map.get(x, x),
            index=0 if vessel_options else None,
            key="selected_vessel_tracker"
        )

    selected_vessel = next((v for v in fleet if v["vessel_id"] == selected_vessel_id), fleet[0] if fleet else None)

    with col_stats:
        if selected_vessel:
            rem_days_str = f"{selected_vessel['days_remaining']} {t('ltt_days_remaining', current_lang)}" if "days_remaining" in selected_vessel else "Live Satellite Tracking"
            render_html(f"""
            <div style="background: rgba(14, 21, 38, 0.85); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 8px; padding: 10px 14px; margin-top: 24px; display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <span style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">{t("ltt_current_speed_course", current_lang)}</span>
                    <div style="font-size: 16px; font-weight: 800; color: #38BDF8;">⚡ {selected_vessel['speed_knots']} Knots ({selected_vessel['speed_knots'] * 1.852:.1f} km/h) · {selected_vessel['heading_deg']}° COG</div>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">{t("ltt_arrival_timeline", current_lang)}</span>
                    <div style="font-size: 15px; font-weight: 800; color: #34D399;">⏱️ {rem_days_str}</div>
                </div>
            </div>
            """)

# Plain-English Executive Mission Callout for the Selected Vessel
if selected_vessel:
    sv = selected_vessel
    holding_summary = sv.get('cargo_summary_simple') or f"{sv.get('cargo_barrels', 750000):,} bbl {sv.get('cargo_name', 'Petroleum Feedstock')}"
    mission_text = sv.get('mission_purpose') or "Transporting commercial energy feedstock across international sea routes."
    v_class_tag = sv.get('vessel_class', 'Tanker').split()[0]
    rem_dist_val = f"{sv['remaining_distance_nm']:,} NM" if "remaining_distance_nm" in sv else "Underway"
    rem_days_val = f"{sv['days_remaining']} days left" if "days_remaining" in sv else "Active Voyage"
    current_basin_str = sv.get('current_basin') or f"Lat {sv['current_lat']:.2f}° N, Lon {sv['current_lon']:.2f}° E"
    render_html(f"""
    <div style="background: linear-gradient(135deg, rgba(245, 185, 66, 0.08) 0%, rgba(14, 21, 38, 0.95) 100%); border: 1px solid rgba(245, 185, 66, 0.35); border-radius: 10px; padding: 14px 18px; margin-bottom: 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.35);">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 6px;">
            <div style="font-size: 12px; font-weight: 800; color: #F5B942; text-transform: uppercase; letter-spacing: 0.06em; display: flex; align-items: center; gap: 8px;">
                {t("ltt_what_is_ship_carrying", current_lang)}
            </div>
            <span style="background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.3); font-size: 10.5px; font-weight: 700; padding: 2px 8px; border-radius: 4px;">
                {v_class_tag} TANKER
            </span>
        </div>
        <div class="fuelpulse-mission-grid">
            <div>
                <span style="color: #94A3B8; font-weight: 600; text-transform: uppercase; font-size: 10.5px;">{t("ltt_ship_holding_label", current_lang)}</span><br/>
                <strong style="color: #F8FAFC; font-size: 13.5px;">{sv.get('flag_emoji', '🚢')} {sv['name']}</strong> ({sv.get('flag', 'International')} Flag)<br/>
                <span style="color: #F5B942; font-weight: 700;">📦 Holding:</span> {holding_summary}
            </div>
            <div>
                <span style="color: #94A3B8; font-weight: 600; text-transform: uppercase; font-size: 10.5px;">{t("ltt_route_purpose_label", current_lang)}</span><br/>
                <strong style="color: #38BDF8;">⚓ {sv.get('origin_port', 'Open Ocean')} ({sv.get('origin_country', 'International')}) ➔ 🎯 {sv.get('dest_port', 'Port')} ({sv.get('dest_country', 'Terminal')})</strong><br/>
                <span style="color: #CBD5E1;">{mission_text}</span>
            </div>
            <div>
                <span style="color: #94A3B8; font-weight: 600; text-transform: uppercase; font-size: 10.5px;">{t("ltt_live_status_label", current_lang)}</span><br/>
                <strong style="color: #34D399;">📍 {current_basin_str}</strong><br/>
                <span style="color: #CBD5E1;">Cruising at <strong>{sv['speed_knots']} kts ({sv['speed_knots'] * 1.852:.1f} km/h)</strong> · <strong>{rem_dist_val}</strong> · <strong>{rem_days_val}</strong>.</span>
            </div>
        </div>
    </div>
    """)

# Interactive Fleet Overview Tabs
with st.expander(t("ltt_browse_summary_cards", current_lang), expanded=False):
    tab_ind, tab_glob = st.tabs([t("ltt_tab_india_corridor", current_lang), t("ltt_tab_global_corridor", current_lang)])

    with tab_ind:
        india_tankers = [v for v in fleet if v.get("in_india_corridor") or "India" in v.get("dest_country", "") or "India" in v.get("origin_country", "")]
        cols = st.columns(len(india_tankers) if india_tankers else 1)
        for i, iv in enumerate(india_tankers):
            with cols[i]:
                render_html(f"""
                <div style="background: #0D1527; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 8px; padding: 12px; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                            <strong style="font-size: 13px; color: #F8FAFC;">{iv['flag_emoji']} {iv['name']}</strong>
                            <span style="font-size: 10px; color: #F5B942; background: rgba(245, 185, 66, 0.12); padding: 1px 6px; border-radius: 4px;">{iv['vessel_class'].split()[0]}</span>
                        </div>
                        <div style="font-size: 11.5px; color: #38BDF8; font-weight: 700; margin-bottom: 6px;">🛢️ {iv['cargo_name']}</div>
                        <div style="font-size: 11px; color: #CBD5E1; margin-bottom: 6px;">
                            <strong>Route:</strong> {iv['origin_port']} ➔ <strong>{iv['dest_port'].split()[0]}</strong>
                        </div>
                        <div style="font-size: 10.5px; color: #94A3B8; line-height: 1.4; margin-bottom: 8px;">
                            {iv.get('mission_purpose', 'Energy transport corridor')}
                        </div>
                    </div>
                    <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 6px; display: flex; justify-content: space-between; font-size: 10.5px;">
                        <span style="color: #38BDF8;">⚡ {iv['speed_knots']} kts ({iv['speed_knots'] * 1.852:.0f} km/h)</span>
                        <span style="color: #34D399; font-weight: 700;">⏱️ {iv['days_remaining']}d left</span>
                    </div>
                </div>
                """)

    with tab_glob:
        global_tankers = [v for v in fleet if not (v.get("in_india_corridor") or "India" in v.get("dest_country", "") or "India" in v.get("origin_country", ""))]
        g_cols = st.columns(3)
        for i, gv in enumerate(global_tankers):
            with g_cols[i % 3]:
                gv_flag = gv.get("flag_emoji", "🌐")
                gv_name = gv.get("name", "Vessel")
                gv_class_short = (gv.get("vessel_class") or "Tanker").split()[0]
                gv_cargo = gv.get("cargo_name", "Petroleum Cargo")
                gv_bbl = gv.get("cargo_barrels", 500000) / 1e6
                gv_origin = gv.get("origin_port", "Open Sea")
                gv_dest_short = (gv.get("dest_port") or "Terminal").split()[0]
                gv_mission = gv.get("mission_purpose", "International strategic route")
                gv_speed = gv.get("speed_knots", 0.0)
                gv_days = gv.get("days_remaining", 1.0)
                render_html(f"""
                <div style="background: #0D1527; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 8px; padding: 12px; margin-bottom: 12px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                            <strong style="font-size: 13px; color: #F8FAFC;">{gv_flag} {gv_name}</strong>
                            <span style="font-size: 10px; color: #38BDF8; background: rgba(56, 189, 248, 0.12); padding: 1px 6px; border-radius: 4px;">{gv_class_short}</span>
                        </div>
                        <div style="font-size: 11.5px; color: #F5B942; font-weight: 700; margin-bottom: 6px;">🛢️ {gv_cargo} ({gv_bbl:.1f}M bbl)</div>
                        <div style="font-size: 11px; color: #CBD5E1; margin-bottom: 6px;">
                            <strong>Route:</strong> {gv_origin} ➔ <strong>{gv_dest_short}</strong>
                        </div>
                        <div style="font-size: 10.5px; color: #94A3B8; line-height: 1.4; margin-bottom: 8px;">
                            {gv_mission}
                        </div>
                    </div>
                    <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 6px; display: flex; justify-content: space-between; font-size: 10.5px;">
                        <span style="color: #38BDF8;">⚡ {gv_speed} kts ({gv_speed * 1.852:.0f} km/h)</span>
                        <span style="color: #34D399; font-weight: 700;">⏱️ {gv_days}d left</span>
                    </div>
                </div>
                """)

# -------------------------------------------------------------
# 5. REALISTIC INTERACTIVE GLOBAL MARITIME AIS SATELLITE MAP
# -------------------------------------------------------------
with st.container(key="tanker_map_header_row"):
    map_header_col1, map_header_col2, map_header_col3 = st.columns([5.2, 3.8, 3.0], vertical_alignment="bottom")
    with map_header_col1:
        st.subheader(t("ltt_map_title", current_lang))
    with map_header_col2:
        map_engine_options = [
            ("dark", t("ltt_opt_dark_ocean", current_lang)),
            ("vector_dark", t("ltt_opt_fast_vector", current_lang)),
            ("globe", t("ltt_opt_3d_globe", current_lang)),
            ("coastal", t("ltt_opt_coastal_chart", current_lang))
        ]
        map_style_key = st.selectbox(
            t("ltt_engine_label", current_lang),
            options=[m[0] for m in map_engine_options],
            format_func=lambda k: dict(map_engine_options).get(k, k),
            index=0,
            key="tanker_map_style_selector"
        )
    with map_header_col3:
        mouse_scroll_zoom = st.toggle(
            "🖱️ Mouse Wheel Zoom",
            value=st.session_state.get("tanker_mouse_zoom", False),
            key="tanker_mouse_zoom",
            help="Turn ON to zoom with mouse wheel/trackpad. Turn OFF to scroll page freely."
        )

# Region quick-focus buttons (Includes Americas & Atlantic)
rf_col1, rf_col2, rf_col3, rf_col4, rf_col5, rf_col6 = st.columns(6)
focus_region = st.session_state.get("tanker_map_focus", "all")

with rf_col1:
    if st.button(t("ltt_btn_global_view", current_lang), use_container_width=True, type="primary" if focus_region == "all" else "secondary"):
        st.session_state["tanker_map_focus"] = "all"
        st.rerun()
with rf_col2:
    if st.button(t("ltt_btn_india_view", current_lang), use_container_width=True, type="primary" if focus_region == "india" else "secondary"):
        st.session_state["tanker_map_focus"] = "india"
        st.rerun()
with rf_col3:
    if st.button(t("ltt_btn_hormuz_view", current_lang), use_container_width=True, type="primary" if focus_region == "hormuz" else "secondary"):
        st.session_state["tanker_map_focus"] = "hormuz"
        st.rerun()
with rf_col4:
    if st.button(t("ltt_btn_red_sea_view", current_lang), use_container_width=True, type="primary" if focus_region == "red_sea" else "secondary"):
        st.session_state["tanker_map_focus"] = "red_sea"
        st.rerun()
with rf_col5:
    if st.button(t("ltt_btn_malacca_view", current_lang), use_container_width=True, type="primary" if focus_region == "malacca" else "secondary"):
        st.session_state["tanker_map_focus"] = "malacca"
        st.rerun()
with rf_col6:
    if st.button(t("ltt_btn_americas_view", current_lang), use_container_width=True, type="primary" if focus_region == "americas" else "secondary"):
        st.session_state["tanker_map_focus"] = "americas"
        st.rerun()

# Set center, zoom & bounds based on selected focus (All countries visible in Global View)
bounds_dict = None
if focus_region == "india":
    c_lat, c_lon, zoom_level = 20.0, 68.0, 3.6
elif focus_region == "hormuz":
    c_lat, c_lon, zoom_level = 25.5, 55.5, 4.8
elif focus_region == "red_sea":
    c_lat, c_lon, zoom_level = 18.0, 42.0, 4.2
elif focus_region == "malacca":
    c_lat, c_lon, zoom_level = 4.0, 102.0, 4.2
elif focus_region == "americas":
    c_lat, c_lon, zoom_level = 15.0, -55.0, 1.8
else:
    # Full World Global View (All continents visible: Americas, Europe, Africa, Asia, Australia)
    c_lat, c_lon, zoom_level = 18.0, 12.0, 1.05

# Major Global Seaborne Shipping Corridors (Background Navigation Lanes)
SHIPPING_LANES = [
    # Persian Gulf to India & East Asia
    {"name": "Persian Gulf ➔ India Main Corridor", "lats": [26.6, 26.5, 24.5, 23.5, 22.4], "lons": [50.2, 56.3, 58.9, 64.0, 69.8]},
    # Persian Gulf to East Asia via Malacca
    {"name": "Persian Gulf ➔ Malacca ➔ China/East Asia", "lats": [24.5, 18.0, 8.0, 5.8, 1.4, 4.0, 14.0, 22.0, 30.0], "lons": [58.9, 64.0, 77.0, 96.0, 102.9, 107.0, 114.0, 120.0, 122.1]},
    # Middle East to Europe via Cape of Good Hope
    {"name": "Cape of Good Hope Mega-Route (Red Sea Bypass)", "lats": [25.0, 10.0, -5.0, -18.0, -28.5, -34.4, -15.0, 10.0, 38.0, 52.0], "lons": [57.0, 55.0, 45.0, 40.0, 33.2, 18.5, 5.0, -18.0, -10.0, 4.1]},
    # Transatlantic US Shale Corridor
    {"name": "US Gulf ➔ Northern Europe Transatlantic", "lats": [27.8, 25.0, 29.0, 38.0, 44.5, 49.0, 52.0], "lons": [-97.4, -85.0, -78.0, -50.0, -24.2, -8.0, 4.1]},
    # Russia Baltic to India via Cape
    {"name": "Baltic Sea ➔ Gujarat Route", "lats": [60.4, 55.0, 50.0, 35.0, -34.4, -10.0, 5.0, 16.2, 22.5], "lons": [28.6, 15.0, -2.0, -12.0, 18.5, 52.0, 64.0, 68.9, 69.7]},
    # Americas Pacific to Atlantic Corridor
    {"name": "Americas Pacific ➔ Atlantic Energy Canal", "lats": [33.7, 20.0, 9.0, 9.3, 15.0, 28.0], "lons": [-118.2, -105.0, -79.5, -79.8, -75.0, -85.0]},
    # Brazil Santos Basin to Asia/India Route
    {"name": "Brazil Santos Basin ➔ Cape ➔ India/China", "lats": [-24.0, -28.0, -34.4, -20.0, 5.0, 22.4], "lons": [-46.3, -30.0, 18.5, 55.0, 68.0, 69.8]}
]

fig_map = go.Figure()

is_tile_map = map_style_key in ["dark", "coastal"]
tile_style = "carto-darkmatter" if map_style_key == "dark" else "open-street-map"

if is_tile_map:
    # 1. Background Shipping Corridors (Vectorized single MultiLine trace for 10x rendering speed)
    all_lane_lats = []
    all_lane_lons = []
    for lane in SHIPPING_LANES:
        all_lane_lats.extend(lane["lats"])
        all_lane_lats.append(None)
        all_lane_lons.extend(lane["lons"])
        all_lane_lons.append(None)

    fig_map.add_trace(go.Scattermap(
        lat=all_lane_lats,
        lon=all_lane_lons,
        mode="lines",
        line=dict(width=1.8, color="rgba(96, 165, 250, 0.28)"),
        hoverinfo="none",
        name="Major Maritime Shipping Lanes",
        showlegend=False
    ))

    # 2. Strategic Chokepoint Danger Zones (Vectorized single trace)
    cp_lats = [cp["lat"] for cp in LiveTankerTracker.CHOKEPOINTS.values()]
    cp_lons = [cp["lon"] for cp in LiveTankerTracker.CHOKEPOINTS.values()]
    cp_colors = [cp["risk_color"] for cp in LiveTankerTracker.CHOKEPOINTS.values()]
    cp_texts = [f"🚨 {cp['name']}" for cp in LiveTankerTracker.CHOKEPOINTS.values()]
    cp_hovers = [
        f"<b>🚨 {cp['name']}</b><br>"
        f"Daily Vol: <b>{cp['daily_mbpd']}M bpd</b> · Status: <b>{cp['risk_level']}</b>"
        for cp in LiveTankerTracker.CHOKEPOINTS.values()
    ]

    fig_map.add_trace(go.Scattermap(
        lat=cp_lats,
        lon=cp_lons,
        mode="markers+text",
        marker=dict(size=18, color=cp_colors, opacity=0.9),
        text=cp_texts,
        textposition="top center",
        textfont=dict(family="Space Grotesk, sans-serif", size=11, color="#FFFFFF"),
        hoverinfo="text",
        hovertext=cp_hovers,
        name="Strategic Chokepoints",
        showlegend=False
    ))

    # 3. Background subtle trails for non-selected vessels (Combined into 1 trace for speed)
    bg_lats = []
    bg_lons = []
    for v in fleet:
        if selected_vessel and v["vessel_id"] == selected_vessel["vessel_id"]:
            continue
        wps = v.get("waypoints", [])
        if len(wps) >= 2:
            bg_lats.extend([pt[0] for pt in wps])
            bg_lats.append(None)
            bg_lons.extend([pt[1] for pt in wps])
            bg_lons.append(None)

    if bg_lats:
        fig_map.add_trace(go.Scattermap(
            lat=bg_lats,
            lon=bg_lons,
            mode="lines",
            line=dict(width=1.5, color="rgba(148, 163, 184, 0.35)"),
            hoverinfo="skip",
            showlegend=False
        ))

    # 4. Highlighted Active Passage for Selected Vessel with Glowing Trail
    if selected_vessel and "waypoints" in selected_vessel:
        wps = selected_vessel["waypoints"]
        lats = [pt[0] for pt in wps]
        lons = [pt[1] for pt in wps]
        fig_map.add_trace(go.Scattermap(
            lat=lats,
            lon=lons,
            mode="lines+markers",
            line=dict(width=4.0, color="#F5B942"),
            marker=dict(size=7, color="#F5B942"),
            hoverinfo="text",
            hovertext=f"<b>Active Voyage Passage:</b> {selected_vessel['origin_port']} ➔ {selected_vessel['dest_port']} ({selected_vessel['total_distance_nm']:,} NM)",
            name=f"Selected Route: {selected_vessel['name']}",
            showlegend=True
        ))

    # 5. Vessel Positions & Hover Dossiers
    for v in fleet:
        is_sel = selected_vessel and v["vessel_id"] == selected_vessel["vessel_id"]
        is_live = v.get("is_real_live_ais", False)

        if is_live:
            color = "#10B981"
            size = 18 if is_sel else 10
            hover_card = (
                f"<b>🛰️ {v['name']}</b> (IMO {v.get('imo', '~')})<br>"
                f"⚡ <b>{v['speed_knots']} kts</b> · 🛢️ {v.get('cargo_name', 'Petroleum')}<br>"
                f"🎯 ➔ <b>{v.get('dest_port', 'High Seas')}</b> · 🟢 Live AIS Ping"
            )
        else:
            color = "#F5B942" if v.get("cargo_type") == "crude" else ("#38BDF8" if v.get("cargo_type") == "product" else "#10B981")
            size = 22 if is_sel else (15 if "VLCC" in v.get("vessel_class", "") or "ULCC" in v.get("vessel_class", "") else 12)
            dest_short = v.get("dest_port", "").split()[0] if v.get("dest_port") else "Port"
            cargo_short = v.get("cargo_name", "Petroleum")
            dest_c = v.get("dest_country", "")
            rem_d = f"{v['days_remaining']}d left" if "days_remaining" in v else "Underway"
            hover_card = (
                f"<b>🚢 {v['name']} ({v.get('flag_emoji', '🚢')})</b><br>"
                f"⚡ <b>{v['speed_knots']} kts</b> · 🛢️ {cargo_short}<br>"
                f"🎯 ➔ <b>{dest_short}</b> ({dest_c}) · ⏱️ <b>{rem_d}</b>"
            )

        fig_map.add_trace(go.Scattermap(
            lat=[v["current_lat"]],
            lon=[v["current_lon"]],
            mode="markers+text",
            marker=dict(
                size=size,
                color=color,
                opacity=1.0
            ),
            text=[f"<b>{v['name']}</b> ({v['speed_knots']} kts)"] if is_sel else [""],
            textposition="bottom center",
            textfont=dict(family="Space Grotesk, sans-serif", size=12, color="#FFFFFF"),
            hoverinfo="text",
            hovertext=hover_card,
            name=f"{v['name']} ({v['speed_knots']} kts)",
            showlegend=False
        ))

    map_kwargs = dict(
        style=tile_style,
        center=dict(lat=c_lat, lon=c_lon),
        zoom=zoom_level
    )
    if bounds_dict:
        map_kwargs["bounds"] = bounds_dict

    fig_map.update_layout(
        map=map_kwargs,
        paper_bgcolor="#070A12",
        plot_bgcolor="#070A12",
        margin=dict(l=0, r=0, t=0, b=0),
        height=560,
        hoverlabel=dict(
            bgcolor="rgba(11, 17, 32, 0.95)",
            bordercolor="rgba(245, 185, 66, 0.7)",
            font_size=12,
            font_family="Space Grotesk, -apple-system, sans-serif"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="left",
            x=0,
            font=dict(color="#F8FAFC", size=11),
            bgcolor="rgba(14, 21, 38, 0.90)",
            bordercolor="rgba(255, 255, 255, 0.15)",
            borderwidth=1
        )
    )

else:
    # High-Performance Vector Radar / 3D Globe Projection (Zero External Tile Lag)
    proj_type = "orthographic" if map_style_key == "globe" else "natural earth"

    for cp_key, cp in LiveTankerTracker.CHOKEPOINTS.items():
        fig_map.add_trace(go.Scattergeo(
            lon=[cp["lon"]],
            lat=[cp["lat"]],
            mode="markers+text",
            marker=dict(size=16, color=cp["risk_color"], symbol="diamond", line=dict(color="#FFFFFF", width=1.5)),
            text=[f"🚨 {cp['name']}"],
            textposition="top center",
            textfont=dict(family="Space Grotesk, sans-serif", size=11, color="#F8FAFC"),
            hoverinfo="text",
            hovertext=f"<b>Chokepoint:</b> {cp['name']}<br><b>Throughput:</b> {cp['daily_mbpd']}M bpd<br><b>Risk:</b> {cp['risk_level']}",
            showlegend=False
        ))

    # Vectorized subtle trails for non-selected vessels
    bg_geo_lats = []
    bg_geo_lons = []
    for v in fleet:
        if selected_vessel and v["vessel_id"] == selected_vessel["vessel_id"]:
            continue
        wps = v.get("waypoints", [])
        if len(wps) >= 2:
            bg_geo_lats.extend([pt[0] for pt in wps] + [None])
            bg_geo_lons.extend([pt[1] for pt in wps] + [None])

    if bg_geo_lats:
        fig_map.add_trace(go.Scattergeo(
            lon=bg_geo_lons,
            lat=bg_geo_lats,
            mode="lines",
            line=dict(width=1.5, color="rgba(148, 163, 184, 0.35)", dash="dot"),
            hoverinfo="skip",
            showlegend=False
        ))

    if selected_vessel and "waypoints" in selected_vessel:
        wps = selected_vessel["waypoints"]
        fig_map.add_trace(go.Scattergeo(
            lon=[pt[1] for pt in wps],
            lat=[pt[0] for pt in wps],
            mode="lines+markers",
            line=dict(width=3.5, color="#F5B942"),
            marker=dict(size=6, color="#F5B942"),
            name=f"Passage: {selected_vessel['name']}"
        ))

    for v in fleet:
        is_sel = selected_vessel and v["vessel_id"] == selected_vessel["vessel_id"]
        is_live = v.get("is_real_live_ais", False)

        if is_live:
            color = "#10B981"
            size = 16 if is_sel else 9
            geo_hover = (
                f"<b>🛰️ {v['name']}</b> (IMO {v.get('imo', '~')})<br>"
                f"⚡ <b>{v['speed_knots']} kts</b> · 🛢️ {v.get('cargo_name', 'Petroleum')}<br>"
                f"🎯 ➔ <b>{v.get('dest_port', 'High Seas')}</b> · 🟢 Live AIS Ping"
            )
        else:
            color = "#F5B942" if v.get("cargo_type") == "crude" else ("#38BDF8" if v.get("cargo_type") == "product" else "#10B981")
            size = 20 if is_sel else 12
            dest_short = v.get("dest_port", "").split()[0] if v.get("dest_port") else "Port"
            cargo_short = v.get("cargo_name", "Petroleum")
            dest_c = v.get("dest_country", "")
            rem_d = f"{v['days_remaining']}d left" if "days_remaining" in v else "Underway"
            geo_hover = (
                f"<b>🚢 {v['name']} ({v.get('flag_emoji', '🚢')})</b><br>"
                f"⚡ <b>{v['speed_knots']} kts</b> · 🛢️ {cargo_short}<br>"
                f"🎯 ➔ <b>{dest_short}</b> ({dest_c}) · ⏱️ <b>{rem_d}</b>"
            )

        fig_map.add_trace(go.Scattergeo(
            lon=[v["current_lon"]],
            lat=[v["current_lat"]],
            mode="markers+text",
            marker=dict(size=size, color=color, symbol="triangle-up", line=dict(color="#FFFFFF" if is_sel else "#0B101E", width=2.0)),
            text=[f"<b>{v['name']}</b> ({v['speed_knots']} kts)"] if is_sel else [""],
            textposition="bottom center",
            textfont=dict(family="Space Grotesk, sans-serif", size=12, color="#F8FAFC"),
            hoverinfo="text",
            hovertext=geo_hover,
            name=f"{v['name']} ({v['speed_knots']} kts)",
            showlegend=False
        ))

    fig_map.update_geos(
        projection_type=proj_type,
        showocean=True,
        oceancolor="#070A12",
        showland=True,
        landcolor="#131B2E",
        showcountries=True,
        countrycolor="rgba(255, 255, 255, 0.22)",
        showcoastlines=True,
        coastlinecolor="rgba(245, 185, 66, 0.45)",
        resolution=110
    )
    fig_map.update_layout(
        paper_bgcolor="#070A12",
        plot_bgcolor="#070A12",
        margin=dict(l=0, r=0, t=10, b=0),
        height=560,
        hoverlabel=dict(
            bgcolor="rgba(11, 17, 32, 0.95)",
            bordercolor="rgba(245, 185, 66, 0.7)",
            font_size=12,
            font_family="Space Grotesk, -apple-system, sans-serif"
        ),
        legend=dict(orientation="h", y=1.02, x=0, font=dict(color="#F8FAFC", size=11))
    )

st.plotly_chart(
    fig_map,
    use_container_width=True,
    config={
        "scrollZoom": mouse_scroll_zoom,
        "doubleClick": "reset+autosize",
        "displayModeBar": True,
        "displaylogo": False,
        "modeBarButtonsToRemove": ["lasso2d", "select2d"],
        "modeBarButtonsToAdd": ["zoomIn2d", "zoomOut2d", "resetScale2d"],
    }
)

st.markdown("""
<div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 8px 14px; margin-top: 6px; font-size: 0.78rem; color: #94A3B8; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
    <div>
        💡 <b>Natural Page Scroll Protected:</b> Page scrolls down smoothly without stopping on map. To zoom the map with mouse wheel/trackpad, toggle <b>"🖱️ Mouse Wheel Zoom"</b> ON above, double-click anywhere to zoom in, or click <b>[+] [-]</b> in the top right map toolbar.
    </div>
    <div style="color: #38BDF8; font-weight: 600;">
        🌍 All Continents & Countries Active (Americas, Asia, Europe, Africa, Oceania)
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 6. VESSEL DEEP-DIVE DOSSIER & PHOTOGRAPHY (CLEAN HTML, NO LEAKAGE)
# -------------------------------------------------------------
if selected_vessel:
    v = selected_vessel
    st.markdown("---")
    dossier_hdr = t("ltt_dossier_title", current_lang)
    st.subheader(f"{dossier_hdr} {v['flag_emoji']} {v['name']} (IMO {v['imo']})")

    with st.container(key="tanker_dossier_row"):
        col_img, col_telemetry = st.columns([5, 7])

        with col_img:
            # High-Resolution Real Vessel Photography (Native Streamlit Media Manager)
            img_rel = v.get("asset_image", "assets/tankers/vlcc_supertanker.jpg")
            img_file = ROOT_DIR / img_rel
            if not img_file.exists():
                img_file = ROOT_DIR / "assets/tankers/vlcc_supertanker.jpg"

            st.image(
                str(img_file),
                use_container_width=True,
                caption=f"🛰️ AIS Satellite Recon: {v['name']} ({v['vessel_class'].split()[0]}) — {v['flag']} Registered"
            )

            dwt_lbl = t("ltt_deadweight", current_lang)
            lb_lbl = t("ltt_length_beam", current_lang)
            draft_lbl = t("ltt_laden_draft", current_lang)

            v_flag_emoji = v.get("flag_emoji", "🚢")
            v_built = v.get("built_year", 2020)
            v_class_full = v.get("vessel_class", "Tanker")
            v_flag_name = v.get("flag", "International")
            v_dwt = v.get("dwt", 115000)
            v_len = v.get("length_m", 250)
            v_beam = v.get("beam_m", 44)
            v_draft = v.get("draft_m", 12.5)

            spec_html = f"""
            <div style="background: #0D1527; border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 10px; padding: 14px 16px; margin-top: 4px; box-shadow: 0 6px 20px rgba(0,0,0,0.35);">
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <h4 style="margin: 0; font-size: 18px; font-weight: 800; color: #F8FAFC;">{v_flag_emoji} {v['name']}</h4>
                    <span style="font-size: 11px; color: #94A3B8; font-weight: 600;">BUILT {v_built}</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
                    <span style="font-size: 12px; color: #38BDF8; font-weight: 700;">{v_class_full}</span>
                    <span style="background: rgba(245, 185, 66, 0.15); color: #F5B942; border: 1px solid rgba(245, 185, 66, 0.3); font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px;">
                        {v_flag_name.upper()} REGISTERED
                    </span>
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 12px; padding-top: 10px; border-top: 1px solid rgba(255, 255, 255, 0.08); text-align: center;">
                    <div style="background: rgba(255,255,255,0.02); padding: 8px 4px; border-radius: 6px;">
                        <div style="font-size: 9.5px; color: #94A3B8; text-transform: uppercase;">{dwt_lbl}</div>
                        <div style="font-size: 12.5px; font-weight: 800; color: #F8FAFC;">{v_dwt:,} DWT</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.02); padding: 8px 4px; border-radius: 6px;">
                        <div style="font-size: 9.5px; color: #94A3B8; text-transform: uppercase;">{lb_lbl}</div>
                        <div style="font-size: 12.5px; font-weight: 800; color: #F8FAFC;">{v_len}m × {v_beam}m</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.02); padding: 8px 4px; border-radius: 6px;">
                        <div style="font-size: 9.5px; color: #94A3B8; text-transform: uppercase;">{draft_lbl}</div>
                        <div style="font-size: 12.5px; font-weight: 800; color: #34D399;">{v_draft} meters</div>
                    </div>
                </div>
            </div>
            """
            render_html(spec_html)

        with col_telemetry:
            # Dynamic ETA & Telemetry Dashboard Card (Rendered via clean render_html)
            v_basin = v.get("current_basin", f"Lat {v['current_lat']:.4f}° N, Lon {v['current_lon']:.4f}° E")
            v_orig_p = v.get("origin_port", "Open Ocean")
            v_orig_c = v.get("origin_country", "International")
            v_dest_c = v.get("dest_country", "Terminal")
            v_pct = v.get("progress_pct", 50.0)
            v_dep = v.get("departure_date", "Live Telemetry")
            v_sailed = v.get("sailed_distance_nm", 500)
            v_tot = v.get("total_distance_nm", 1000)
            v_days = f"{v['days_remaining']} <span style='font-size: 11px;'>Days</span>" if "days_remaining" in v else "Live Stream"
            v_hrs = f"~{v['hours_remaining']:,.0f} hours" if "hours_remaining" in v else "Streaming"
            v_rem_nm = f"{v['remaining_distance_nm']:,} <span style='font-size: 11px;'>NM</span>" if "remaining_distance_nm" in v else "AIS Ping"
            v_rem_km = f"{v['remaining_distance_nm'] * 1.852:,.0f} km" if "remaining_distance_nm" in v else "Real-Time Tracking"
            v_bbl = v.get("cargo_barrels", 750000)
            v_val_m = v.get("cargo_value_millions_usd", 38.0)
            v_sea = v.get("weather_sea_state", "Moderate (Wave 1.2m)")
            v_cp_col = v.get("chokepoint_color", "#38BDF8")
            v_cp_name = v.get("chokepoint_name", "Open Seaway")
            v_cp_dist = v.get("chokepoint_dist_nm", 250)
            v_cp_risk = v.get("chokepoint_risk", "Normal Traffic")

            telemetry_html = f"""
            <div style="background: #0D1527; border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 12px; padding: 18px 20px; box-shadow: 0 8px 30px rgba(0,0,0,0.5); display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <!-- Status & Sea Zone -->
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: #10B981; box-shadow: 0 0 8px #10B981;"></span>
                            <span style="font-size: 12px; font-weight: 800; color: #10B981; text-transform: uppercase; letter-spacing: 0.05em;">{v.get('nav_status', 'Underway')}</span>
                        </div>
                        <span style="font-size: 11px; color: #94A3B8; font-weight: 600;">IMO: {v['imo']} · MMSI: {v['mmsi']}</span>
                    </div>

                    <!-- Current Sea Basin -->
                    <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 10px 14px; margin-bottom: 12px;">
                        <div style="font-size: 10.5px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Current Maritime Basin & Coordinates</div>
                        <div style="font-size: 14.5px; font-weight: 700; color: #F8FAFC; margin-top: 2px;">📍 {v_basin}</div>
                        <div style="font-size: 12px; color: #38BDF8; font-family: monospace; margin-top: 2px;">{v['current_lat']:.4f}° N, {v['current_lon']:.4f}° E · Heading: {v['heading_deg']}° COG</div>
                    </div>

                    <!-- Voyage Progress Bar -->
                    <div style="margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 700; color: #F8FAFC; margin-bottom: 6px;">
                            <span>⚓ {v_orig_p} ({v_orig_c})</span>
                            <span style="color: #F5B942;">{v_pct}% SAILED</span>
                            <span>🎯 {v['dest_port']} ({v_dest_c})</span>
                        </div>
                        <div style="width: 100%; height: 8px; background: rgba(255, 255, 255, 0.1); border-radius: 999px; overflow: hidden;">
                            <div style="width: {v_pct}%; height: 100%; background: linear-gradient(90deg, #F5B942, #10B981); border-radius: 999px;"></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; font-size: 10.5px; color: #94A3B8; margin-top: 4px;">
                            <span>Departed: {v_dep}</span>
                            <span>{v_sailed:,} NM sailed of {v_tot:,} NM</span>
                        </div>
                    </div>

                    <!-- DYNAMIC ETA & SPEED SCORECARD ROW -->
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 12px;">
                        <div style="background: rgba(14, 165, 233, 0.1); border: 1px solid rgba(14, 165, 233, 0.3); border-radius: 8px; padding: 8px; text-align: center;">
                            <div style="font-size: 9.5px; color: #7DD3FC; font-weight: 700; text-transform: uppercase;">CURRENT SPEED (SOG)</div>
                            <div style="font-size: 18px; font-weight: 800; color: #38BDF8; margin: 2px 0;">{v['speed_knots']} <span style="font-size: 11px;">kts</span></div>
                            <div style="font-size: 10px; color: #BAE6FD;">{v['speed_knots'] * 1.852:.1f} km/h</div>
                        </div>
                        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 8px; text-align: center;">
                            <div style="font-size: 9.5px; color: #6EE7B7; font-weight: 700; text-transform: uppercase;">DAYS TO ARRIVAL (ETA)</div>
                            <div style="font-size: 18px; font-weight: 800; color: #34D399; margin: 2px 0;">{v_days}</div>
                            <div style="font-size: 10px; color: #A7F3D0;">{v_hrs}</div>
                        </div>
                        <div style="background: rgba(245, 185, 66, 0.1); border: 1px solid rgba(245, 185, 66, 0.3); border-radius: 8px; padding: 8px; text-align: center;">
                            <div style="font-size: 9.5px; color: #FCD34D; font-weight: 700; text-transform: uppercase;">DISTANCE REMAINING</div>
                            <div style="font-size: 18px; font-weight: 800; color: #F5B942; margin: 2px 0;">{v_rem_nm}</div>
                            <div style="font-size: 10px; color: #FDE68A;">{v_rem_km}</div>
                        </div>
                    </div>

                    <!-- CARGO SPECIFICATION & VALUE -->
                    <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 10px 12px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="font-size: 10px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Onboard Petroleum Cargo</span>
                                <div style="font-size: 13.5px; font-weight: 700; color: #F8FAFC;">🛢️ {v['cargo_name']} ({v_bbl:,} bbl)</div>
                            </div>
                            <div style="text-align: right;">
                                <span style="font-size: 10px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Cargo Market Valuation</span>
                                <div style="font-size: 15px; font-weight: 800; color: #F5B942;">${v_val_m}M USD</div>
                            </div>
                        </div>
                    </div>

                    <!-- PLAIN-ENGLISH MISSION BRIEFING -->
                    <div style="background: rgba(56, 189, 248, 0.05); border: 1px dashed rgba(56, 189, 248, 0.3); border-radius: 8px; padding: 9px 12px;">
                        <div style="font-size: 10px; font-weight: 700; color: #38BDF8; text-transform: uppercase;">🎯 Strategic Commercial Mission:</div>
                        <div style="font-size: 11.5px; color: #CBD5E1; margin-top: 2px; line-height: 1.4;">
                            {v.get('mission_purpose', 'Energy supply and commercial refinery feedstock delivery.')}
                        </div>
                    </div>
                </div>

                <!-- Chokepoint & Sea State Warning Footer -->
                <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; justify-content: space-between; align-items: center; font-size: 10.5px;">
                    <span style="color: #94A3B8;">🌊 <b>Sea State:</b> {v_sea}</span>
                    <span style="color: {v_cp_col}; font-weight: 700;">⚠️ {v_cp_name}: {v_cp_dist} NM away ({v_cp_risk})</span>
                </div>
            </div>
            """
            render_html(telemetry_html, container=col_telemetry)

# -------------------------------------------------------------
# 7. COMPLETE SEABORNE FLEET TELEMETRY MANIFEST TABLE
# -------------------------------------------------------------
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
st.subheader(t("ltt_manifest_title", current_lang))

table_data = []
for v in fleet:
    bbl_val = v.get("cargo_barrels", 750000)
    cargo_val_m = v.get("cargo_value_millions_usd") or (bbl_val * 80.0 / 1e6)
    days_arr = f"{v['days_remaining']} Days" if "days_remaining" in v else "Live Tracking"
    prog_str = f"{v['progress_pct']}%" if "progress_pct" in v else "Live GPS"
    table_data.append({
        t("tbl_vessel_name", current_lang): f"{v.get('flag_emoji', '🚢')} {v['name']}",
        t("tbl_vessel_class", current_lang): v.get("vessel_class", "Tanker").split()[0],
        "IMO": v.get("imo", "~"),
        t("tbl_carrying", current_lang): f"{v.get('cargo_name', 'Petroleum')} ({bbl_val / 1e6:.2f}M bbl)",
        t("tbl_cargo_val", current_lang): f"${cargo_val_m:.1f}M",
        t("tbl_speed", current_lang): f"{v.get('speed_knots', 0)} kts ({v.get('speed_knots', 0) * 1.852:.0f} km/h)",
        t("tbl_heading", current_lang): f"{v.get('heading_deg', 0)}°",
        t("tbl_current_loc", current_lang): v.get("current_basin", f"Lat {v['current_lat']:.2f}, Lon {v['current_lon']:.2f}"),
        t("tbl_origin", current_lang): v.get("origin_port", "Open Sea"),
        t("tbl_dest_port", current_lang): v.get("dest_port", "Port"),
        t("tbl_days_arrive", current_lang): days_arr,
        t("tbl_progress", current_lang): prog_str
    })

manifest_df = pd.DataFrame(table_data)
st.dataframe(manifest_df, use_container_width=True, hide_index=True)

# Technical CSV Export
render_csv_download(manifest_df, filename="global_tanker_ais_telemetry.csv", label=t("ltt_btn_export_csv", current_lang))

# -------------------------------------------------------------
# 8. PLAIN ENGLISH GUIDE: HOW MARITIME TANKER TELEMETRY WORKS
# -------------------------------------------------------------
st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

with st.expander(t("ltt_guide_title", current_lang), expanded=True):
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("""
        #### 🛰️ How are these tankers tracked?
        - **Satellite AIS (Automatic Identification System)**: Every commercial oil tanker is required by international maritime law (IMO SOLAS) to broadcast VHF transponder signals every 2 to 10 seconds.
        - **What they transmit**: Vessel GPS position, Speed Over Ground (SOG), Course Over Ground (COG), vessel draft (how deep the ship sits in water, which reveals if it is full of oil or empty), and destination port.
        - **Why knots?**: 1 Knot = **1 Nautical Mile per hour** = **1.852 km/h**. A supertanker traveling at **14 knots** moves at approximately **26 km/h**.

        #### ⏱️ How is "Days to Destination" (ETA) calculated?
        - If a supertanker has **1,340 Nautical Miles** left to sail and travels at **14 knots**:
          $$\\text{Hours} = \\frac{1,340 \\text{ NM}}{14 \\text{ knots}} = 95.7 \\text{ Hours} \\approx 4.0 \\text{ Days}$$
        - Our engine factors in real-time speed variations, port congestion waiting queues, and chokepoint transit delays.
        """)

    with col_g2:
        st.markdown("""
        #### 🐢 Why do massive supertankers sail at only 12–15 knots?
        - **Economic "Slow-Steaming"**: Tanker fuel (Heavy Fuel Oil / Marine Gasoil) consumption increases exponentially with speed.
        - Sailing a VLCC at **16 knots** burns almost **60% more bunker fuel** than sailing at **13 knots**, costing fleet operators an extra **$20,000+ per day**!
        
        #### 🚨 Geopolitical Diversion: The Cape of Good Hope Factor
        - When the **Bab el-Mandeb / Red Sea** corridor is disrupted by missile or pirate threats, tankers heading from the Middle East to Europe or the US cannot use the Suez Canal.
        - They must divert all the way around South Africa's **Cape of Good Hope**.
        - This adds **+3,500 Nautical Miles**, **+12 to 15 Days of transit time**, and over **$1,200,000 in extra fuel and charter costs** per voyage!
        """)

# Universal AI Assistant integration
render_universal_ai_assistant(context_page="Live Tanker Tracker", key_prefix="ltt")
