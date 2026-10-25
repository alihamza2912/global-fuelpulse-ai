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
    title="11. 🚢 Live Maritime Fuel Tanker Tracker — AIS Telemetry",
    subtitle="Real-time ocean coordinate positioning, speed over ground (knots), heading, dynamic days-to-arrival (ETA), and cargo valuations for global crude and fuel supertankers.",
    source_tag="Satellite AIS • MarineTraffic Feeds • Lloyd's List Intelligence • Kpler Telemetry",
    observation_date="Live Ocean Telemetry 2026"
)

# -------------------------------------------------------------
# 2. CONTROL & FILTER CONSOLE
# -------------------------------------------------------------
render_html("""
<div style="background: #0D1527; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 12px; padding: 14px 20px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: space-between;">
    <span style="font-size: 13px; font-weight: 800; color: #F5B942; text-transform: uppercase; letter-spacing: 0.08em; display: flex; align-items: center; gap: 8px;">
        📡 MARITIME SATELLITE RADAR & FLEET TELEMETRY CONSOLE
    </span>
    <span style="background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.35); font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 999px;">
        ● SATELLITE AIS LIVE LOCK
    </span>
</div>
""")

col_f1, col_f2, col_f3 = st.columns([2, 2, 3])

with col_f1:
    cargo_choice = st.selectbox(
        "Commodity Type",
        options=[("all", "🌐 All Commodities"), ("crude", "🛢️ Crude Oil (VLCC/Suezmax)"), ("product", "⛽ Refined Products (Diesel/Jet)"), ("lng", "❄️ LNG Carriers (Q-Max)")],
        format_func=lambda x: x[1],
        index=0,
        key="tanker_filter_cargo"
    )[0]

with col_f2:
    class_choice = st.selectbox(
        "Vessel Classification",
        options=["all", "VLCC", "ULCC", "Suezmax", "Aframax", "LR2", "LR1", "Q-Max"],
        format_func=lambda x: "All Vessel Classes" if x == "all" else f"Class: {x}",
        index=0,
        key="tanker_filter_class"
    )

with col_f3:
    search_query = st.text_input(
        "Search Fleet (Name, IMO, Port, or Flag)",
        placeholder="e.g. Maran Canopus, Ras Tanura, 9784532, India...",
        key="tanker_search_query"
    )

# -------------------------------------------------------------
# 3. COMPUTE FLEET TELEMETRY & SUMMARY METRICS
# -------------------------------------------------------------
fleet = LiveTankerTracker.get_fleet_telemetry(
    cargo_filter=cargo_choice,
    vessel_class_filter=class_choice,
    search_query=search_query
)
kpis = LiveTankerTracker.get_summary_kpis(fleet)

# Elevated Midnight Scorecards (Universal 195px Equal-Height Standard)
m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    render_instrument_card(
        label="Active Fleet at Sea",
        value=f"{kpis['active_vessels']} Vessels",
        accent="amber",
        delta="100% AIS Tracked",
        delta_is_positive_bad=False,
        subtext="Laden international voyages"
    )

with m2:
    render_instrument_card(
        label="Seaborne Barrels",
        value=f"{kpis['total_barrels_at_sea'] / 1e6:,.1f}M bbl",
        accent="amber",
        delta="Crude & Refined",
        delta_is_positive_bad=False,
        subtext="In transit across oceans"
    )

with m3:
    render_instrument_card(
        label="Customs Cargo Value",
        value=f"${kpis['total_cargo_value_usd'] / 1e9:.2f}B USD",
        accent="copper",
        delta=f"₹{kpis['total_cargo_value_usd'] * 83.2 / 1e7:,.0f} Cr",
        delta_is_positive_bad=False,
        subtext="Spot commercial valuation"
    )

with m4:
    render_instrument_card(
        label="Average Speed (SOG)",
        value=f"{kpis['avg_fleet_speed_knots']:.1f} Knots",
        accent="teal",
        delta=f"{kpis['avg_fleet_speed_knots'] * 1.852:.1f} km/h",
        delta_is_positive_bad=False,
        subtext="Economic slow-steaming"
    )

with m5:
    render_instrument_card(
        label="At-Risk Chokepoint Transit",
        value=f"{kpis['at_risk_vessels']} Vessels",
        accent="red",
        delta="Hormuz / Red Sea",
        delta_is_positive_bad=True,
        subtext="Within 500 NM war-risk zone"
    )

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 4. PLAIN-ENGLISH EXPLORER: WHO IS CARRYING WHAT & WHERE ARE THEY GOING?
# -------------------------------------------------------------
vessel_options = [v["vessel_id"] for v in fleet] if fleet else []
vessel_map = {v["vessel_id"]: f"{v['flag_emoji']} {v['name']} ({v['vessel_class'].split()[0]}) — {v['cargo_name']} ➔ {v['dest_port'].split()[0]}" for v in fleet}

col_sel, col_stats = st.columns([6, 4])
with col_sel:
    selected_vessel_id = st.selectbox(
        "🎯 Select Supertanker to Inspect Voyage Mission & AIS Telemetry",
        options=vessel_options,
        format_func=lambda x: vessel_map.get(x, x),
        index=0 if vessel_options else None,
        key="selected_vessel_tracker"
    )

selected_vessel = LiveTankerTracker.get_vessel_by_id(selected_vessel_id) if selected_vessel_id else (fleet[0] if fleet else None)

with col_stats:
    if selected_vessel:
        render_html(f"""
        <div style="background: rgba(14, 21, 38, 0.85); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 8px; padding: 10px 14px; margin-top: 24px; display: flex; align-items: center; justify-content: space-between;">
            <div>
                <span style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Current Speed & Course</span>
                <div style="font-size: 16px; font-weight: 800; color: #38BDF8;">⚡ {selected_vessel['speed_knots']} Knots ({selected_vessel['speed_knots'] * 1.852:.1f} km/h) · {selected_vessel['heading_deg']}° COG</div>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Arrival Timeline</span>
                <div style="font-size: 15px; font-weight: 800; color: #34D399;">⏱️ {selected_vessel['days_remaining']} Days Remaining</div>
            </div>
        </div>
        """)

# Plain-English Executive Mission Callout for the Selected Vessel
if selected_vessel:
    sv = selected_vessel
    holding_summary = sv.get('cargo_summary_simple') or f"{sv['cargo_barrels']:,} bbl {sv['cargo_name']}"
    mission_text = sv.get('mission_purpose') or "Transporting commercial energy feedstock across international sea routes."
    v_class_tag = sv['vessel_class'].split()[0]
    render_html(f"""
    <div style="background: linear-gradient(135deg, rgba(245, 185, 66, 0.08) 0%, rgba(14, 21, 38, 0.95) 100%); border: 1px solid rgba(245, 185, 66, 0.35); border-radius: 10px; padding: 14px 18px; margin-bottom: 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.35);">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 6px;">
            <div style="font-size: 12px; font-weight: 800; color: #F5B942; text-transform: uppercase; letter-spacing: 0.06em; display: flex; align-items: center; gap: 8px;">
                📦 What is the Ship Carrying?
            </div>
            <span style="background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.3); font-size: 10.5px; font-weight: 700; padding: 2px 8px; border-radius: 4px;">
                {v_class_tag} TANKER
            </span>
        </div>
        <div style="display: grid; grid-template-columns: 1.2fr 1.3fr 1.1fr; gap: 14px; font-size: 12px; line-height: 1.5;">
            <div>
                <span style="color: #94A3B8; font-weight: 600; text-transform: uppercase; font-size: 10.5px;">🚢 Ship & Cargo Holding:</span><br/>
                <strong style="color: #F8FAFC; font-size: 13.5px;">{sv['flag_emoji']} {sv['name']}</strong> ({sv['flag']} Flag)<br/>
                <span style="color: #F5B942; font-weight: 700;">📦 Holding:</span> {holding_summary}
            </div>
            <div>
                <span style="color: #94A3B8; font-weight: 600; text-transform: uppercase; font-size: 10.5px;">📍 Route & Commercial Purpose:</span><br/>
                <strong style="color: #38BDF8;">⚓ {sv['origin_port']} ({sv['origin_country']}) ➔ 🎯 {sv['dest_port']} ({sv['dest_country']})</strong><br/>
                <span style="color: #CBD5E1;">{mission_text}</span>
            </div>
            <div>
                <span style="color: #94A3B8; font-weight: 600; text-transform: uppercase; font-size: 10.5px;">⏱️ Live Status & ETA:</span><br/>
                <strong style="color: #34D399;">📍 {sv['current_basin']}</strong><br/>
                <span style="color: #CBD5E1;">Cruising at <strong>{sv['speed_knots']} kts ({sv['speed_knots'] * 1.852:.1f} km/h)</strong> · <strong>{sv['remaining_distance_nm']:,} NM</strong> to go · <strong>{sv['days_remaining']} days</strong> left to destination.</span>
            </div>
        </div>
    </div>
    """)

# Interactive Fleet Overview Tabs
with st.expander("🚢 **Browse All 10 Tankers: What Each Ship is Carrying (Quick Summary Cards)**", expanded=False):
    tab_ind, tab_glob = st.tabs(["🇮🇳 India Energy Lifelines (4 Tankers)", "🌏 Asia-Pacific & European Supertankers (6 Tankers)"])

    with tab_ind:
        india_tankers = [v for v in fleet if v.get("in_india_corridor") or "India" in v["dest_country"] or "India" in v["origin_country"]]
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
        global_tankers = [v for v in fleet if not (v.get("in_india_corridor") or "India" in v["dest_country"] or "India" in v["origin_country"])]
        g_cols = st.columns(3)
        for i, gv in enumerate(global_tankers):
            with g_cols[i % 3]:
                render_html(f"""
                <div style="background: #0D1527; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 8px; padding: 12px; margin-bottom: 12px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                            <strong style="font-size: 13px; color: #F8FAFC;">{gv['flag_emoji']} {gv['name']}</strong>
                            <span style="font-size: 10px; color: #38BDF8; background: rgba(56, 189, 248, 0.12); padding: 1px 6px; border-radius: 4px;">{gv['vessel_class'].split()[0]}</span>
                        </div>
                        <div style="font-size: 11.5px; color: #F5B942; font-weight: 700; margin-bottom: 6px;">🛢️ {gv['cargo_name']} ({gv['cargo_barrels'] / 1e6:.1f}M bbl)</div>
                        <div style="font-size: 11px; color: #CBD5E1; margin-bottom: 6px;">
                            <strong>Route:</strong> {gv['origin_port']} ➔ <strong>{gv['dest_port'].split()[0]}</strong>
                        </div>
                        <div style="font-size: 10.5px; color: #94A3B8; line-height: 1.4; margin-bottom: 8px;">
                            {gv.get('mission_purpose', 'International strategic route')}
                        </div>
                    </div>
                    <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 6px; display: flex; justify-content: space-between; font-size: 10.5px;">
                        <span style="color: #38BDF8;">⚡ {gv['speed_knots']} kts ({gv['speed_knots'] * 1.852:.0f} km/h)</span>
                        <span style="color: #34D399; font-weight: 700;">⏱️ {gv['days_remaining']}d left</span>
                    </div>
                </div>
                """)

# -------------------------------------------------------------
# 5. REALISTIC INTERACTIVE GLOBAL MARITIME AIS SATELLITE MAP
# -------------------------------------------------------------
map_header_col1, map_header_col2 = st.columns([6, 4])
with map_header_col1:
    st.subheader("🗺️ Realistic Global Maritime Ocean Map — Live AIS Coordinates & Shipping Corridors")
with map_header_col2:
    map_style_choice = st.radio(
        "Map Display Engine",
        options=["🌑 Realistic Dark Oceanic", "🗺️ Coastal Navigation Chart", "🌐 3D Global Globe"],
        index=0,
        horizontal=True,
        key="tanker_map_style_selector"
    )

# Region quick-focus buttons
rf_col1, rf_col2, rf_col3, rf_col4, rf_col5 = st.columns(5)
focus_region = st.session_state.get("tanker_map_focus", "all")

with rf_col1:
    if st.button("🌐 Global Fleet View", use_container_width=True, type="primary" if focus_region == "all" else "secondary"):
        st.session_state["tanker_map_focus"] = "all"
        st.rerun()
with rf_col2:
    if st.button("🇮🇳 Indian Ocean & Gujarat", use_container_width=True, type="primary" if focus_region == "india" else "secondary"):
        st.session_state["tanker_map_focus"] = "india"
        st.rerun()
with rf_col3:
    if st.button("⚡ Persian Gulf & Hormuz", use_container_width=True, type="primary" if focus_region == "hormuz" else "secondary"):
        st.session_state["tanker_map_focus"] = "hormuz"
        st.rerun()
with rf_col4:
    if st.button("🚨 Red Sea & Bab el-Mandeb", use_container_width=True, type="primary" if focus_region == "red_sea" else "secondary"):
        st.session_state["tanker_map_focus"] = "red_sea"
        st.rerun()
with rf_col5:
    if st.button("🚢 Malacca Strait Corridor", use_container_width=True, type="primary" if focus_region == "malacca" else "secondary"):
        st.session_state["tanker_map_focus"] = "malacca"
        st.rerun()

# Set center, zoom & bounds based on selected focus (Guarantees single-world view, no duplicate countries)
if focus_region == "india":
    c_lat, c_lon, zoom_level = 20.0, 68.0, 3.8
    bounds_dict = dict(west=45, east=95, south=-5, north=32)
elif focus_region == "hormuz":
    c_lat, c_lon, zoom_level = 25.5, 55.5, 5.2
    bounds_dict = dict(west=46, east=62, south=20, north=31)
elif focus_region == "red_sea":
    c_lat, c_lon, zoom_level = 18.0, 42.0, 4.4
    bounds_dict = dict(west=32, east=52, south=10, north=30)
elif focus_region == "malacca":
    c_lat, c_lon, zoom_level = 4.0, 102.0, 4.5
    bounds_dict = dict(west=92, east=110, south=-5, north=15)
else:
    # Single-world global focus (Never repeats countries across width)
    if selected_vessel and selected_vessel.get("in_india_corridor"):
        c_lat, c_lon, zoom_level = 20.0, 66.0, 3.0
    elif selected_vessel:
        c_lat = selected_vessel["current_lat"]
        c_lon = selected_vessel["current_lon"]
        zoom_level = 2.8
    else:
        c_lat, c_lon, zoom_level = 18.0, 62.0, 2.7
    bounds_dict = dict(west=-35, east=145, south=-38, north=65)

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
    {"name": "Baltic Sea ➔ Gujarat Route", "lats": [60.4, 55.0, 50.0, 35.0, -34.4, -10.0, 5.0, 16.2, 22.5], "lons": [28.6, 15.0, -2.0, -12.0, 18.5, 52.0, 64.0, 68.9, 69.7]}
]

fig_map = go.Figure()

is_tile_map = "Realistic" in map_style_choice or "Coastal" in map_style_choice
tile_style = "carto-darkmatter" if "Realistic" in map_style_choice else "open-street-map"

if is_tile_map:
    # 1. Background Shipping Corridors
    for lane in SHIPPING_LANES:
        fig_map.add_trace(go.Scattermap(
            lat=lane["lats"],
            lon=lane["lons"],
            mode="lines",
            line=dict(width=1.8, color="rgba(96, 165, 250, 0.28)"),
            hoverinfo="text",
            hovertext=f"<b>Primary Seaborne Artery:</b> {lane['name']}",
            name="Major Maritime Shipping Lanes",
            showlegend=False
        ))

    # 2. Strategic Chokepoint Danger Zones
    for cp_key, cp in LiveTankerTracker.CHOKEPOINTS.items():
        fig_map.add_trace(go.Scattermap(
            lat=[cp["lat"]],
            lon=[cp["lon"]],
            mode="markers+text",
            marker=dict(
                size=18,
                color=cp["risk_color"],
                opacity=0.9
            ),
            text=[f"🚨 {cp['name']}"],
            textposition="top center",
            textfont=dict(family="Space Grotesk, sans-serif", size=11, color="#FFFFFF"),
            hoverinfo="text",
            hovertext=(
                f"<b>🚨 Strategic Maritime Chokepoint</b><br>"
                f"<b>Name:</b> {cp['name']}<br>"
                f"<b>Daily Volume:</b> {cp['daily_mbpd']} Million bpd<br>"
                f"<b>Status:</b> {cp['risk_level']}"
            ),
            name=f"Chokepoint: {cp['name']}",
            showlegend=False
        ))

    # 3. Background subtle trails for non-selected vessels
    for v in fleet:
        if selected_vessel and v["vessel_id"] == selected_vessel["vessel_id"]:
            continue
        wps = v.get("waypoints", [])
        if len(wps) >= 2:
            lats = [pt[0] for pt in wps]
            lons = [pt[1] for pt in wps]
            fig_map.add_trace(go.Scattermap(
                lat=lats,
                lon=lons,
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
        color = "#F5B942" if v["cargo_type"] == "crude" else ("#38BDF8" if v["cargo_type"] == "product" else "#10B981")
        size = 22 if is_sel else (15 if "VLCC" in v["vessel_class"] or "ULCC" in v["vessel_class"] else 12)

        hover_card = (
            f"<b>🚢 {v['name']} ({v['flag_emoji']} {v['flag']})</b><br>"
            f"<b>Class:</b> {v['vessel_class']}<br>"
            f"<b>IMO:</b> {v['imo']} · <b>MMSI:</b> {v['mmsi']}<br>"
            f"────────────────────────<br>"
            f"<b>Speed Over Ground:</b> {v['speed_knots']} Knots ({v['speed_knots'] * 1.852:.1f} km/h)<br>"
            f"<b>Heading:</b> {v['heading_deg']}° · <b>Draft:</b> {v['draft_m']}m<br>"
            f"<b>Current Location:</b> {v['current_basin']}<br>"
            f"<b>Coordinates:</b> {v['current_lat']:.4f}°N, {v['current_lon']:.4f}°E<br>"
            f"────────────────────────<br>"
            f"<b>Cargo:</b> {v['cargo_name']} ({v['cargo_barrels']:,} bbl)<br>"
            f"<b>Cargo Value:</b> ${v['cargo_value_millions_usd']}M USD<br>"
            f"<b>Route:</b> {v['origin_port']} ➔ {v['dest_port']}<br>"
            f"<b>Mission:</b> {v.get('mission_purpose', 'Energy Delivery')}<br>"
            f"<b>ETA:</b> {v['eta_human']} ({v['remaining_distance_nm']:,} NM left · {v['progress_pct']}%)"
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
            name=f"{v['name']} ({v['speed_knots']} kts · {v['cargo_name'].split()[0]})"
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
        height=580,
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
    # 3D High-Contrast Global Orthographic Projection
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

    for v in fleet:
        if selected_vessel and v["vessel_id"] == selected_vessel["vessel_id"]:
            continue
        wps = v.get("waypoints", [])
        if len(wps) >= 2:
            fig_map.add_trace(go.Scattergeo(
                lon=[pt[1] for pt in wps],
                lat=[pt[0] for pt in wps],
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
        color = "#F5B942" if v["cargo_type"] == "crude" else ("#38BDF8" if v["cargo_type"] == "product" else "#10B981")
        size = 20 if is_sel else 12
        fig_map.add_trace(go.Scattergeo(
            lon=[v["current_lon"]],
            lat=[v["current_lat"]],
            mode="markers+text",
            marker=dict(size=size, color=color, symbol="triangle-up", line=dict(color="#FFFFFF" if is_sel else "#0B101E", width=2.0)),
            text=[f"<b>{v['name']}</b> ({v['speed_knots']} kts)"] if is_sel else [""],
            textposition="bottom center",
            textfont=dict(family="Space Grotesk, sans-serif", size=12, color="#F8FAFC"),
            name=f"{v['name']} ({v['speed_knots']} kts)"
        ))

    fig_map.update_geos(
        projection_type="orthographic",
        showocean=True,
        oceancolor="#070A12",
        showland=True,
        landcolor="#18233C",
        showcountries=True,
        countrycolor="rgba(255, 255, 255, 0.25)",
        showcoastlines=True,
        coastlinecolor="rgba(245, 185, 66, 0.5)",
        resolution=50
    )
    fig_map.update_layout(
        paper_bgcolor="#070A12",
        plot_bgcolor="#070A12",
        margin=dict(l=0, r=0, t=10, b=0),
        height=580,
        legend=dict(orientation="h", y=1.02, x=0, font=dict(color="#F8FAFC", size=11))
    )

st.plotly_chart(
    fig_map,
    use_container_width=True,
    config={
        "scrollZoom": False,
        "displayModeBar": True,
        "displaylogo": False,
        "modeBarButtonsToRemove": ["lasso2d", "select2d"],
        "modeBarButtonsToAdd": ["zoomIn2d", "zoomOut2d", "resetScale2d"],
    }
)

# -------------------------------------------------------------
# 6. VESSEL DEEP-DIVE DOSSIER & PHOTOGRAPHY (CLEAN HTML, NO LEAKAGE)
# -------------------------------------------------------------
if selected_vessel:
    v = selected_vessel
    st.markdown("---")
    st.subheader(f"🔍 Vessel Intelligence Dossier: {v['flag_emoji']} {v['name']} (IMO {v['imo']})")

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

        spec_html = f"""
        <div style="background: #0D1527; border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 10px; padding: 14px 16px; margin-top: 4px; box-shadow: 0 6px 20px rgba(0,0,0,0.35);">
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
                <h4 style="margin: 0; font-size: 18px; font-weight: 800; color: #F8FAFC;">{v['flag_emoji']} {v['name']}</h4>
                <span style="font-size: 11px; color: #94A3B8; font-weight: 600;">BUILT {v['built_year']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
                <span style="font-size: 12px; color: #38BDF8; font-weight: 700;">{v['vessel_class']}</span>
                <span style="background: rgba(245, 185, 66, 0.15); color: #F5B942; border: 1px solid rgba(245, 185, 66, 0.3); font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px;">
                    {v['flag'].upper()} REGISTERED
                </span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 12px; padding-top: 10px; border-top: 1px solid rgba(255, 255, 255, 0.08); text-align: center;">
                <div style="background: rgba(255,255,255,0.02); padding: 8px 4px; border-radius: 6px;">
                    <div style="font-size: 9.5px; color: #94A3B8; text-transform: uppercase;">Deadweight</div>
                    <div style="font-size: 12.5px; font-weight: 800; color: #F8FAFC;">{v['dwt']:,} DWT</div>
                </div>
                <div style="background: rgba(255,255,255,0.02); padding: 8px 4px; border-radius: 6px;">
                    <div style="font-size: 9.5px; color: #94A3B8; text-transform: uppercase;">Length × Beam</div>
                    <div style="font-size: 12.5px; font-weight: 800; color: #F8FAFC;">{v['length_m']}m × {v['beam_m']}m</div>
                </div>
                <div style="background: rgba(255,255,255,0.02); padding: 8px 4px; border-radius: 6px;">
                    <div style="font-size: 9.5px; color: #94A3B8; text-transform: uppercase;">Laden Draft</div>
                    <div style="font-size: 12.5px; font-weight: 800; color: #34D399;">{v['draft_m']} meters</div>
                </div>
            </div>
        </div>
        """
        render_html(spec_html)

    with col_telemetry:
        # Dynamic ETA & Telemetry Dashboard Card (Rendered via clean render_html)
        telemetry_html = f"""
        <div style="background: #0D1527; border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 12px; padding: 18px 20px; box-shadow: 0 8px 30px rgba(0,0,0,0.5); display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <!-- Status & Sea Zone -->
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: #10B981; box-shadow: 0 0 8px #10B981;"></span>
                        <span style="font-size: 12px; font-weight: 800; color: #10B981; text-transform: uppercase; letter-spacing: 0.05em;">{v['nav_status']}</span>
                    </div>
                    <span style="font-size: 11px; color: #94A3B8; font-weight: 600;">IMO: {v['imo']} · MMSI: {v['mmsi']}</span>
                </div>

                <!-- Current Sea Basin -->
                <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 10px 14px; margin-bottom: 12px;">
                    <div style="font-size: 10.5px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Current Maritime Basin & Coordinates</div>
                    <div style="font-size: 14.5px; font-weight: 700; color: #F8FAFC; margin-top: 2px;">📍 {v['current_basin']}</div>
                    <div style="font-size: 12px; color: #38BDF8; font-family: monospace; margin-top: 2px;">{v['current_lat']:.4f}° N, {v['current_lon']:.4f}° E · Heading: {v['heading_deg']}° COG</div>
                </div>

                <!-- Voyage Progress Bar -->
                <div style="margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 700; color: #F8FAFC; margin-bottom: 6px;">
                        <span>⚓ {v['origin_port']} ({v['origin_country']})</span>
                        <span style="color: #F5B942;">{v['progress_pct']}% SAILED</span>
                        <span>🎯 {v['dest_port']} ({v['dest_country']})</span>
                    </div>
                    <div style="width: 100%; height: 8px; background: rgba(255, 255, 255, 0.1); border-radius: 999px; overflow: hidden;">
                        <div style="width: {v['progress_pct']}%; height: 100%; background: linear-gradient(90deg, #F5B942, #10B981); border-radius: 999px;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 10.5px; color: #94A3B8; margin-top: 4px;">
                        <span>Departed: {v['departure_date']}</span>
                        <span>{v['sailed_distance_nm']:,} NM sailed of {v['total_distance_nm']:,} NM</span>
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
                        <div style="font-size: 18px; font-weight: 800; color: #34D399; margin: 2px 0;">{v['days_remaining']} <span style="font-size: 11px;">Days</span></div>
                        <div style="font-size: 10px; color: #A7F3D0;">~{v['hours_remaining']:,.0f} hours</div>
                    </div>
                    <div style="background: rgba(245, 185, 66, 0.1); border: 1px solid rgba(245, 185, 66, 0.3); border-radius: 8px; padding: 8px; text-align: center;">
                        <div style="font-size: 9.5px; color: #FCD34D; font-weight: 700; text-transform: uppercase;">DISTANCE REMAINING</div>
                        <div style="font-size: 18px; font-weight: 800; color: #F5B942; margin: 2px 0;">{v['remaining_distance_nm']:,} <span style="font-size: 11px;">NM</span></div>
                        <div style="font-size: 10px; color: #FDE68A;">{v['remaining_distance_nm'] * 1.852:,.0f} km</div>
                    </div>
                </div>

                <!-- CARGO SPECIFICATION & VALUE -->
                <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 10px 12px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 10px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Onboard Petroleum Cargo</span>
                            <div style="font-size: 13.5px; font-weight: 700; color: #F8FAFC;">🛢️ {v['cargo_name']} ({v['cargo_barrels']:,} bbl)</div>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 10px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Cargo Market Valuation</span>
                            <div style="font-size: 15px; font-weight: 800; color: #F5B942;">${v['cargo_value_millions_usd']}M USD</div>
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
                <span style="color: #94A3B8;">🌊 <b>Sea State:</b> {v['weather_sea_state']}</span>
                <span style="color: {v['chokepoint_color']}; font-weight: 700;">⚠️ {v['chokepoint_name']}: {v['chokepoint_dist_nm']} NM away ({v['chokepoint_risk']})</span>
            </div>
        </div>
        """
        render_html(telemetry_html, container=col_telemetry)

# -------------------------------------------------------------
# 7. COMPLETE SEABORNE FLEET TELEMETRY MANIFEST TABLE
# -------------------------------------------------------------
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
st.subheader("📋 Active Global Petroleum Fleet Telemetry Manifest")

table_data = []
for v in fleet:
    table_data.append({
        "Vessel Name": f"{v['flag_emoji']} {v['name']}",
        "Class": v["vessel_class"].split()[0],
        "IMO": v["imo"],
        "What It's Carrying": f"{v['cargo_name']} ({v['cargo_barrels'] / 1e6:.2f}M bbl)",
        "Cargo Value ($M)": f"${v['cargo_value_millions_usd']}M",
        "Speed": f"{v['speed_knots']} kts ({v['speed_knots'] * 1.852:.0f} km/h)",
        "Heading": f"{v['heading_deg']}°",
        "Current Location": v["current_basin"],
        "Origin": v["origin_port"],
        "Destination Port": v["dest_port"],
        "Days to Arrive": f"{v['days_remaining']} Days",
        "Progress": f"{v['progress_pct']}%"
    })

manifest_df = pd.DataFrame(table_data)
st.dataframe(manifest_df, use_container_width=True, hide_index=True)

# Technical CSV Export
render_csv_download(manifest_df, filename="global_tanker_ais_telemetry.csv", label="📥 EXPORT SEABORNE TANKER FLEET TELEMETRY (CSV)")

# -------------------------------------------------------------
# 8. PLAIN ENGLISH GUIDE: HOW MARITIME TANKER TELEMETRY WORKS
# -------------------------------------------------------------
st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

with st.expander("📖 **Plain-English Guide: How does live tanker tracking work and what do knots/ETA mean?**", expanded=True):
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
