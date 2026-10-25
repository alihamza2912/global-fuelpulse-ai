"""
Page 13: Live Maritime Oil Tanker Tracker & Satellite AIS Telemetry.
Visualizes real-time global crude supertankers (VLCC, ULCC, Suezmax, Aframax, Product Tankers, LNG)
with interactive ocean map, vessel photo dossiers, live speed in knots, heading, dynamic ETA to destination, and cargo valuations.
"""

import sys
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
    get_atlas_plotly_theme,
    apply_clean_layout,
    render_html,
    COLOR_INK,
    COLOR_AMBER,
    COLOR_WHITE
)
from src.localization.i18n import t, get_current_language
from src.analytics.live_tanker_tracker import LiveTankerTracker

# 1. Initialize Page Architecture
apply_theme()
current_lang = get_current_language()

render_page_header(
    title="13. 🚢 Live Maritime Fuel Tanker Tracker — AIS Telemetry",
    subtitle="Real-time ocean coordinate positioning, speed over ground (knots), heading, dynamic days-to-arrival (ETA), and cargo valuations for global crude and fuel supertankers.",
    source_tag="Satellite AIS • MarineTraffic Feeds • Lloyd's List Intelligence • Kpler Telemetry",
    observation_date="Live Ocean Telemetry 2026"
)

# -------------------------------------------------------------
# 2. CONTROL & FILTER CONSOLE
# -------------------------------------------------------------
st.markdown("""
<div style="background: #0D1527; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 12px; padding: 18px 22px; margin-bottom: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px;">
        <span style="font-size: 13px; font-weight: 800; color: #F5B942; text-transform: uppercase; letter-spacing: 0.08em; display: flex; align-items: center; gap: 8px;">
            📡 MARITIME SATELLITE RADAR & FLEET TELEMETRY CONSOLE
        </span>
        <span style="background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.35); font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 999px;">
            ● SATELLITE AIS LIVE LOCK
        </span>
    </div>
""", unsafe_allow_html=True)

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

st.markdown("</div>", unsafe_allow_html=True)

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
        delta=f"100% AIS Tracked",
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
# 4. INTERACTIVE GLOBAL MARITIME AIS SATELLITE MAP
# -------------------------------------------------------------
st.subheader("🗺️ Global Maritime Oil Artery Map — Live AIS Coordinates & Predicted Routes")

# Vessel Selection dropdown
vessel_options = [v["vessel_id"] for v in fleet] if fleet else []
vessel_map = {v["vessel_id"]: f"{v['flag_emoji']} {v['name']} ({v['vessel_class'].split()[0]}) — {v['cargo_name']} ➔ {v['dest_port'].split()[0]}" for v in fleet}

col_sel, col_stats = st.columns([6, 4])
with col_sel:
    selected_vessel_id = st.selectbox(
        "Select Tanker to Track Path & Telemetry Dossier",
        options=vessel_options,
        format_func=lambda x: vessel_map.get(x, x),
        index=0 if vessel_options else None,
        key="selected_vessel_tracker"
    )

selected_vessel = LiveTankerTracker.get_vessel_by_id(selected_vessel_id) if selected_vessel_id else (fleet[0] if fleet else None)

with col_stats:
    if selected_vessel:
        st.markdown(f"""
        <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 10px 14px; margin-top: 24px; display: flex; align-items: center; justify-content: space-between;">
            <div>
                <span style="font-size: 11px; color: #94A3B8; text-transform: uppercase;">Current SOG & Course:</span>
                <div style="font-size: 16px; font-weight: 800; color: #38BDF8;">⚡ {selected_vessel['speed_knots']} Knots · {selected_vessel['heading_deg']}° COG</div>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 11px; color: #94A3B8; text-transform: uppercase;">Destination ETA:</span>
                <div style="font-size: 15px; font-weight: 800; color: #34D399;">⏱️ {selected_vessel['days_remaining']} Days Remaining</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Build High-Contrast Ocean Map
fig_map = go.Figure()

# 1. Chokepoint Warning Hazard Circles
for cp_key, cp in LiveTankerTracker.CHOKEPOINTS.items():
    fig_map.add_trace(go.Scattergeo(
        lon=[cp["lon"]],
        lat=[cp["lat"]],
        mode="markers+text",
        marker=dict(
            size=18,
            color=cp["risk_color"],
            symbol="diamond",
            line=dict(color="#FFFFFF", width=1.5),
            opacity=0.85
        ),
        text=[f"🚨 {cp['name']}"],
        textposition="top center",
        textfont=dict(family="Space Grotesk, sans-serif", size=11, color="#F8FAFC"),
        hoverinfo="text",
        hovertext=(
            f"<b>Strategic Maritime Chokepoint</b><br>"
            f"<b>Name:</b> {cp['name']}<br>"
            f"<b>Daily Throughput:</b> {cp['daily_mbpd']} Million bpd<br>"
            f"<b>Security Level:</b> {cp['risk_level']}"
        ),
        name=f"Chokepoint: {cp['name']}",
        showlegend=False
    ))

# 2. Voyage Trails for all other vessels (Subtle background paths)
for v in fleet:
    if selected_vessel and v["vessel_id"] == selected_vessel["vessel_id"]:
        continue
    wps = v.get("waypoints", [])
    if len(wps) >= 2:
        lats = [pt[0] for pt in wps]
        lons = [pt[1] for pt in wps]
        fig_map.add_trace(go.Scattergeo(
            lon=lons,
            lat=lats,
            mode="lines",
            line=dict(width=1.5, color="rgba(148, 163, 184, 0.35)", dash="dot"),
            hoverinfo="skip",
            showlegend=False
        ))

# 3. Active Selected Vessel Voyage Trail (High-Contrast Solid Past & Dashed Future)
if selected_vessel and "waypoints" in selected_vessel:
    wps = selected_vessel["waypoints"]
    lats = [pt[0] for pt in wps]
    lons = [pt[1] for pt in wps]
    fig_map.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        mode="lines",
        line=dict(width=3.5, color="#F5B942"),
        hoverinfo="text",
        hovertext=f"<b>Planned Passage:</b> {selected_vessel['origin_port']} ➔ {selected_vessel['dest_port']} ({selected_vessel['total_distance_nm']:,} NM)",
        name=f"Active Passage: {selected_vessel['name']}",
        showlegend=True
    ))

# 4. Fleet Vessel Positions (Ship Markers)
for v in fleet:
    is_sel = selected_vessel and v["vessel_id"] == selected_vessel["vessel_id"]
    color = "#F5B942" if v["cargo_type"] == "crude" else ("#38BDF8" if v["cargo_type"] == "product" else "#10B981")
    size = 20 if is_sel else (14 if "VLCC" in v["vessel_class"] or "ULCC" in v["vessel_class"] else 11)
    
    hover_card = (
        f"<b>🚢 {v['name']} ({v['flag_emoji']} {v['flag']})</b><br>"
        f"<b>Class:</b> {v['vessel_class']}<br>"
        f"<b>IMO:</b> {v['imo']} · <b>MMSI:</b> {v['mmsi']}<br>"
        f"────────────────────────<br>"
        f"<b>Speed Over Ground:</b> {v['speed_knots']} Knots ({v['speed_knots'] * 1.852:.1f} km/h)<br>"
        f"<b>Heading:</b> {v['heading_deg']}° · <b>Draft:</b> {v['draft_m']}m<br>"
        f"<b>Location:</b> {v['current_basin']}<br>"
        f"<b>Coordinates:</b> {v['current_lat']:.4f}°N, {v['current_lon']:.4f}°E<br>"
        f"────────────────────────<br>"
        f"<b>Cargo:</b> {v['cargo_name']} ({v['cargo_barrels']:,} bbl)<br>"
        f"<b>Cargo Value:</b> ${v['cargo_value_millions_usd']}M USD<br>"
        f"<b>Route:</b> {v['origin_port']} ➔ {v['dest_port']}<br>"
        f"<b>ETA:</b> {v['eta_human']} ({v['remaining_distance_nm']:,} NM left · {v['progress_pct']}%)"
    )

    fig_map.add_trace(go.Scattergeo(
        lon=[v["current_lon"]],
        lat=[v["current_lat"]],
        mode="markers+text",
        marker=dict(
            size=size,
            color=color,
            symbol="triangle-up",
            line=dict(color="#FFFFFF" if is_sel else "#0B101E", width=2.5 if is_sel else 1.2),
            opacity=1.0
        ),
        text=[f"<b>{v['name']}</b> ({v['speed_knots']} kts)"] if is_sel else [""],
        textposition="bottom center",
        textfont=dict(family="Space Grotesk, sans-serif", size=12, color="#F8FAFC"),
        hoverinfo="text",
        hovertext=hover_card,
        name=f"{v['name']} ({v['speed_knots']} kts)"
    ))

fig_map.update_geos(
    projection_type="natural earth",
    showocean=True,
    oceancolor="#090E1C",
    showland=True,
    landcolor="#1A243B",
    showcountries=True,
    countrycolor="rgba(255, 255, 255, 0.2)",
    showlakes=True,
    lakecolor="#090E1C",
    showcoastlines=True,
    coastlinecolor="rgba(245, 185, 66, 0.4)",
    resolution=50,
    fitbounds="locations"
)

fig_map.update_layout(
    paper_bgcolor="#0D1527",
    plot_bgcolor="#090E1C",
    margin=dict(l=10, r=10, t=20, b=10),
    height=540,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(color="#94A3B8", size=11),
        bgcolor="rgba(13, 21, 39, 0.85)"
    )
)

st.plotly_chart(fig_map, use_container_width=True)

# -------------------------------------------------------------
# 5. VESSEL DEEP-DIVE DOSSIER & PHOTOGRAPHY
# -------------------------------------------------------------
if selected_vessel:
    v = selected_vessel
    st.markdown("---")
    st.subheader(f"🔍 Vessel Intelligence Dossier: {v['flag_emoji']} {v['name']} (IMO {v['imo']})")

    col_img, col_telemetry = st.columns([5, 7])

    with col_img:
        # Realistic Ship Photography Card
        st.markdown(f"""
        <div style="background: #0D1527; border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 12px; overflow: hidden; box-shadow: 0 8px 30px rgba(0,0,0,0.5);">
            <div style="position: relative; width: 100%; height: 260px; overflow: hidden; background: #070A12;">
                <img src="{v['image_url']}" style="width: 100%; height: 100%; object-fit: cover; filter: contrast(1.1) brightness(0.95);" alt="{v['name']} Supertanker" />
                <div style="position: absolute; bottom: 10px; left: 12px; background: rgba(11, 16, 30, 0.85); backdrop-filter: blur(8px); padding: 4px 10px; border-radius: 6px; border: 1px solid rgba(255, 255, 255, 0.15);">
                    <span style="font-size: 11px; font-weight: 700; color: #F8FAFC;">{v['flag_emoji']} {v['flag'].upper()} REGISTERED</span>
                </div>
                <div style="position: absolute; top: 10px; right: 12px; background: rgba(245, 185, 66, 0.9); color: #0B101E; font-size: 11px; font-weight: 800; padding: 3px 8px; border-radius: 4px;">
                    {v['vessel_class'].split()[0]}
                </div>
            </div>
            <div style="padding: 16px 18px;">
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <h3 style="margin: 0; font-size: 20px; font-weight: 800; color: #F8FAFC;">{v['name']}</h3>
                    <span style="font-size: 12px; color: #94A3B8; font-weight: 600;">BUILT {v['built_year']}</span>
                </div>
                <div style="font-size: 12px; color: #38BDF8; font-weight: 600; margin-top: 2px;">{v['vessel_class']}</div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(255, 255, 255, 0.08); text-align: center;">
                    <div>
                        <div style="font-size: 10px; color: #94A3B8; text-transform: uppercase;">Deadweight</div>
                        <div style="font-size: 13px; font-weight: 700; color: #F8FAFC;">{v['dwt']:,} DWT</div>
                    </div>
                    <div>
                        <div style="font-size: 10px; color: #94A3B8; text-transform: uppercase;">Length / Beam</div>
                        <div style="font-size: 13px; font-weight: 700; color: #F8FAFC;">{v['length_m']}m × {v['beam_m']}m</div>
                    </div>
                    <div>
                        <div style="font-size: 10px; color: #94A3B8; text-transform: uppercase;">Laden Draft</div>
                        <div style="font-size: 13px; font-weight: 700; color: #F8FAFC;">{v['draft_m']} meters</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_telemetry:
        # Dynamic ETA & Telemetry Dashboard Card
        st.markdown(f"""
        <div style="background: #0D1527; border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 12px; padding: 20px 22px; box-shadow: 0 8px 30px rgba(0,0,0,0.5); height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <!-- Status & Sea Zone -->
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #10B981; box-shadow: 0 0 8px #10B981;"></span>
                        <span style="font-size: 12px; font-weight: 700; color: #10B981; text-transform: uppercase; letter-spacing: 0.05em;">{v['nav_status']}</span>
                    </div>
                    <span style="font-size: 11px; color: #94A3B8; font-weight: 600;">IMO: {v['imo']} · MMSI: {v['mmsi']}</span>
                </div>

                <!-- Current Sea Basin -->
                <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 10px 14px; margin-bottom: 14px;">
                    <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Current Maritime Basin & Coordinates</div>
                    <div style="font-size: 15px; font-weight: 700; color: #F8FAFC; margin-top: 2px;">📍 {v['current_basin']}</div>
                    <div style="font-size: 12px; color: #38BDF8; font-family: 'JetBrains Mono', monospace; margin-top: 2px;">{v['current_lat']:.4f}° N, {v['current_lon']:.4f}° E · Heading: {v['heading_deg']}° COG</div>
                </div>

                <!-- Voyage Progress Bar -->
                <div style="margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 700; color: #F8FAFC; margin-bottom: 6px;">
                        <span>⚓ {v['origin_port']} ({v['origin_country']})</span>
                        <span style="color: #F5B942;">{v['progress_pct']}% SAILED</span>
                        <span>🎯 {v['dest_port']} ({v['dest_country']})</span>
                    </div>
                    <div style="width: 100%; height: 8px; background: rgba(255, 255, 255, 0.1); border-radius: 999px; overflow: hidden;">
                        <div style="width: {v['progress_pct']}%; height: 100%; background: linear-gradient(90deg, #F5B942, #10B981); border-radius: 999px;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; color: #94A3B8; margin-top: 4px;">
                        <span>Departed: {v['departure_date']}</span>
                        <span>{v['sailed_distance_nm']:,} NM sailed of {v['total_distance_nm']:,} NM</span>
                    </div>
                </div>

                <!-- DYNAMIC ETA & SPEED SCORECARD ROW -->
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 14px;">
                    <div style="background: rgba(14, 165, 233, 0.1); border: 1px solid rgba(14, 165, 233, 0.3); border-radius: 8px; padding: 10px; text-align: center;">
                        <div style="font-size: 10px; color: #7DD3FC; font-weight: 700; text-transform: uppercase;">CURRENT SPEED (SOG)</div>
                        <div style="font-size: 20px; font-weight: 800; color: #38BDF8; margin: 2px 0;">{v['speed_knots']} <span style="font-size: 12px;">kts</span></div>
                        <div style="font-size: 10px; color: #BAE6FD;">{v['speed_knots'] * 1.852:.1f} km/h</div>
                    </div>
                    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 10px; text-align: center;">
                        <div style="font-size: 10px; color: #6EE7B7; font-weight: 700; text-transform: uppercase;">ESTIMATED TIME TO ARRIVAL</div>
                        <div style="font-size: 20px; font-weight: 800; color: #34D399; margin: 2px 0;">{v['days_remaining']} <span style="font-size: 12px;">Days</span></div>
                        <div style="font-size: 10px; color: #A7F3D0;">~{v['hours_remaining']:,.0f} hours</div>
                    </div>
                    <div style="background: rgba(245, 185, 66, 0.1); border: 1px solid rgba(245, 185, 66, 0.3); border-radius: 8px; padding: 10px; text-align: center;">
                        <div style="font-size: 10px; color: #FCD34D; font-weight: 700; text-transform: uppercase;">DISTANCE REMAINING</div>
                        <div style="font-size: 20px; font-weight: 800; color: #F5B942; margin: 2px 0;">{v['remaining_distance_nm']:,} <span style="font-size: 12px;">NM</span></div>
                        <div style="font-size: 10px; color: #FDE68A;">{v['remaining_distance_nm'] * 1.852:,.0f} km</div>
                    </div>
                </div>

                <!-- CARGO SPECIFICATION & VALUE -->
                <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 10px 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 10.5px; color: #94A3B8; text-transform: uppercase;">Onboard Petroleum Cargo</span>
                            <div style="font-size: 14px; font-weight: 700; color: #F8FAFC;">🛢️ {v['cargo_name']} ({v['cargo_barrels']:,} bbl)</div>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 10.5px; color: #94A3B8; text-transform: uppercase;">Cargo Market Valuation</span>
                            <div style="font-size: 15px; font-weight: 800; color: #F5B942;">${v['cargo_value_millions_usd']}M USD</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Chokepoint & Sea State Warning Footer -->
            <div style="margin-top: 14px; padding-top: 10px; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; justify-content: space-between; align-items: center; font-size: 11px;">
                <span style="color: #94A3B8;">🌊 <b>Sea State:</b> {v['weather_sea_state']}</span>
                <span style="color: {v['chokepoint_color']}; font-weight: 700;">⚠️ {v['chokepoint_name']}: {v['chokepoint_dist_nm']} NM away ({v['chokepoint_risk']})</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 6. COMPLETE SEABORNE FLEET TELEMETRY MANIFEST TABLE
# -------------------------------------------------------------
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
st.subheader("📋 Active Global Petroleum Fleet Telemetry Manifest")

table_data = []
for v in fleet:
    table_data.append({
        "Vessel Name": f"{v['flag_emoji']} {v['name']}",
        "Class": v["vessel_class"].split()[0],
        "IMO": v["imo"],
        "Cargo": v["cargo_name"],
        "Barrels": f"{v['cargo_barrels']:,} bbl",
        "Valuation ($M)": f"${v['cargo_value_millions_usd']}M",
        "Speed": f"{v['speed_knots']} kts",
        "Heading": f"{v['heading_deg']}°",
        "Current Sea Basin": v["current_basin"],
        "Origin": v["origin_port"],
        "Destination": v["dest_port"],
        "Remaining (NM)": f"{v['remaining_distance_nm']:,} NM",
        "ETA to Destination": v["eta_human"],
        "Progress": f"{v['progress_pct']}%"
    })

manifest_df = pd.DataFrame(table_data)
st.dataframe(manifest_df, use_container_width=True, hide_index=True)

# Technical CSV Export
render_csv_download(manifest_df, filename="global_tanker_ais_telemetry.csv", label="📥 EXPORT SEABORNE TANKER FLEET TELEMETRY (CSV)")

# -------------------------------------------------------------
# 7. PLAIN ENGLISH GUIDE: HOW MARITIME TANKER TELEMETRY WORKS
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
