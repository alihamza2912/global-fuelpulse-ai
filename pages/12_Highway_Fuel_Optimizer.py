"""
Page 12: Highway Fuel Trip & Cross-Border Arbitrage Optimizer.
Calculates optimal refueling waypoints, state/country border price differentials,
and net commercial savings across India, Saudi Arabia, Dubai / UAE, and Middle East GCC corridors.
"""

import sys
from pathlib import Path

# Ensure project root AND src directory are in sys.path
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
import plotly.express as px
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
from src.analytics.highway_fuel_optimizer import HighwayFuelOptimizer

# Initialize Page
apply_theme()
current_lang = get_current_language()

# Page Header (internally orchestrates universal navigation, sidebar, and theme)
render_page_header(
    title="12. 🛣️ Highway Fuel Trip & Arbitrage Optimizer",
    subtitle="Interstate VAT disparity, cross-border freight corridor routing, and AI refueling optimization for India, Saudi Arabia, Dubai/UAE, and the Middle East.",
    source_tag="PPAC • MoPNG • Saudi Aramco • UAE Fuel Committee",
    observation_date="Live Corridor Telemetry 2026"
)

# -------------------------------------------------------------
# 1. CONTROL CONSOLE: REGION, ROUTE, VEHICLE & FUEL
# -------------------------------------------------------------
st.markdown("""
<div style="background: #0D1527; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 12px; padding: 18px 22px; margin-bottom: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.2rem;">🗺️</span>
            <div>
                <div style="font-weight: 700; color: #F8FAFC; font-size: 1.05rem; letter-spacing: 0.02em;">CORRIDOR ROUTE & VEHICLE CONFIGURATION</div>
                <div style="font-size: 0.78rem; color: #94A3B8;">Select freight region, origin-destination nodes, and fleet vehicle parameters.</div>
            </div>
        </div>
        <span style="background: rgba(245, 185, 66, 0.15); border: 1px solid rgba(245, 185, 66, 0.35); color: #F5B942; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 20px;">
            AI ARBITRAGE ACTIVE
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

col_reg, col_mode, col_corridor = st.columns([1.2, 1.0, 1.8])

with col_reg:
    region_choice = st.selectbox(
        "Geographic Freight Region",
        options=[
            ("india", "🇮🇳 India (28 States & UTs)"),
            ("saudi", "🇸🇦 Saudi Arabia (Aramco Corridors)"),
            ("uae", "🇦🇪 Dubai & UAE (Emirates Freight)"),
            ("gcc_cross_border", "🌐 GCC Cross-Border (UAE, KSA, Oman, Qatar)")
        ],
        format_func=lambda x: x[1],
        index=0,
        key="opt_region"
    )[0]

with col_mode:
    route_mode = st.radio(
        "Routing Mode",
        options=["Preset Freight Artery", "Custom Hubs"],
        horizontal=True,
        key="opt_route_mode"
    )

corridors = HighwayFuelOptimizer.get_corridors_for_region(region_choice)
selected_corridor_id = None
custom_origin = None
custom_dest = None

if route_mode == "Preset Freight Artery":
    with col_corridor:
        corridor_options = [(c["id"], c["name"]) for c in corridors]
        selected_corridor_id = st.selectbox(
            "Primary Arterial Corridor",
            options=corridor_options,
            format_func=lambda x: x[1],
            key="opt_preset_corridor"
        )[0]
else:
    # Custom origin / destination dropdowns
    if region_choice == "india":
        all_nodes = sorted(list(HighwayFuelOptimizer.INDIA_NODES.keys()))
    elif region_choice == "saudi":
        all_nodes = sorted(list(HighwayFuelOptimizer.SAUDI_NODES.keys()))
    elif region_choice == "uae":
        all_nodes = sorted(list(HighwayFuelOptimizer.UAE_NODES.keys()))
    else:
        all_nodes = sorted(list(HighwayFuelOptimizer.GCC_CROSS_BORDER_NODES.keys()))

    with col_corridor:
        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            custom_origin = st.selectbox("Origin Hub", options=all_nodes, index=0, key="opt_custom_origin")
        with sub_c2:
            custom_dest = st.selectbox("Destination Hub", options=all_nodes, index=min(1, len(all_nodes)-1), key="opt_custom_dest")

# Vehicle & Fuel Selection
col_veh, col_fuel, col_custom = st.columns([1.5, 1.2, 1.3])

with col_veh:
    veh_keys = list(HighwayFuelOptimizer.VEHICLE_PROFILES.keys())
    vehicle_type = st.selectbox(
        "Fleet / Vehicle Class",
        options=veh_keys,
        format_func=lambda k: f"{HighwayFuelOptimizer.VEHICLE_PROFILES[k]['icon']} {HighwayFuelOptimizer.VEHICLE_PROFILES[k]['name']}",
        index=0,
        key="opt_vehicle_type"
    )

with col_fuel:
    if region_choice == "india":
        fuel_opts = [("diesel", "⛽ Diesel (High Freight Volume)"), ("petrol", "🟢 Petrol (Motor Spirit)")]
    elif region_choice == "saudi":
        fuel_opts = [("diesel", "⛽ Diesel (1.15 SAR/L)"), ("petrol_91", "🟢 Premium 91 (2.18 SAR/L)"), ("petrol_95", "🔴 Super 95 (2.33 SAR/L)")]
    elif region_choice == "uae":
        fuel_opts = [("diesel", "⛽ Diesel (3.10 AED/L)"), ("petrol_95", "🟢 Special 95 (2.93 AED/L)"), ("petrol_98", "🔴 Super 98 (3.05 AED/L)")]
    else:
        fuel_opts = [("diesel", "⛽ Diesel (Cross-Border Arbitrage)"), ("petrol", "🟢 Petrol (Cross-Border)")]

    fuel_type = st.selectbox(
        "Fuel Specification",
        options=fuel_opts,
        format_func=lambda x: x[1],
        index=0,
        key="opt_fuel_type"
    )[0]

with col_custom:
    v_def = HighwayFuelOptimizer.VEHICLE_PROFILES[vehicle_type]
    exp = st.expander(f"⚙️ Tank & Mileage ({v_def['tank_capacity_l']}L • {v_def['consumption_kml']} km/L)", expanded=False)
    with exp:
        override_tank = st.number_input("Custom Tank Capacity (Liters)", min_value=10.0, max_value=1200.0, value=float(v_def["tank_capacity_l"]), step=10.0)
        override_kml = st.number_input("Fuel Efficiency (km/L)", min_value=1.0, max_value=40.0, value=float(v_def["consumption_kml"]), step=0.5)

# -------------------------------------------------------------
# 2. RUN OPTIMIZATION ALGORITHM
# -------------------------------------------------------------
result = HighwayFuelOptimizer.optimize_trip(
    region=region_choice,
    origin=custom_origin or "Delhi",
    destination=custom_dest or "Maharashtra",
    vehicle_type=vehicle_type,
    fuel_type=fuel_type,
    custom_tank_l=override_tank,
    custom_kml=override_kml,
    selected_corridor_id=selected_corridor_id
)

fin = result["financial_summary"]
sym = result["currency_symbol"]
code = result["currency_code"]
p_met = result["price_metrics"]

# -------------------------------------------------------------
# 3. EXECUTIVE FINANCIAL & TELEMETRY SCORECARD
# -------------------------------------------------------------
st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    st.markdown(f"""
    <div style="background: #0D1527; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 14px; text-align: center;">
        <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 600; text-transform: uppercase;">Total Distance</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: #F8FAFC; margin: 4px 0;">{result['total_distance_km']:,.0f} <span style="font-size: 0.85rem; color: #94A3B8;">km</span></div>
        <div style="font-size: 0.75rem; color: #38BDF8;">⏱️ ~{result['est_transit_hours']} hrs transit</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div style="background: #0D1527; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 14px; text-align: center;">
        <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 600; text-transform: uppercase;">Fuel Consumption</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: #F5B942; margin: 4px 0;">{result['total_fuel_needed_l']:,.1f} <span style="font-size: 0.85rem; color: #94A3B8;">L</span></div>
        <div style="font-size: 0.75rem; color: #94A3B8;">Range: {result['tank_range_km']:,.0f} km/tank</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div style="background: #0D1527; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 14px; text-align: center;">
        <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 600; text-transform: uppercase;">Unplanned Cost</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: #F43F5E; margin: 4px 0;">{sym}{fin['unoptimized_cost']:,.0f}</div>
        <div style="font-size: 0.75rem; color: #FDA4AF;">Naive random fills</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div style="background: #0D1527; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 14px; text-align: center;">
        <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 600; text-transform: uppercase;">Optimized Cost</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: #10B981; margin: 4px 0;">{sym}{fin['optimized_cost']:,.0f}</div>
        <div style="font-size: 0.75rem; color: #6EE7B7;">{sym}{fin['cost_per_km']:.2f} / km</div>
    </div>
    """, unsafe_allow_html=True)

with m5:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(13, 21, 39, 0.95) 100%); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 10px; padding: 14px; text-align: center; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.15);">
        <div style="font-size: 0.72rem; color: #6EE7B7; font-weight: 700; text-transform: uppercase;">NET CASH SAVINGS</div>
        <div style="font-size: 1.5rem; font-weight: 900; color: #34D399; margin: 4px 0;">{sym}{fin['net_savings']:,.0f}</div>
        <div style="font-size: 0.75rem; color: #A7F3D0; font-weight: 600;">💰 {fin['savings_pct']}% ROI on Strategy</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 4. VISUALIZATION: HIGHWAY PRICE PROFILE & ARBITRAGE CHARTS
# -------------------------------------------------------------
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

col_chart_route, col_chart_tax = st.columns([1.6, 1.4])

# Plotly High-Contrast styling template
chart_paper_bg = "#0D1527"
chart_plot_bg = "#090E1C"

with col_chart_route:
    st.markdown("""
    <div style="font-size: 0.95rem; font-weight: 700; color: #F8FAFC; margin-bottom: 8px;">
        📈 Highway Corridor Fuel Price Trajectory & Waypoint Arbitrage
    </div>
    """, unsafe_allow_html=True)

    wp_df = pd.DataFrame(result["waypoints"])
    fig_route = go.Figure()

    # Route line
    fig_route.add_trace(go.Scatter(
        x=wp_df["cumulative_km"],
        y=wp_df["fuel_price"],
        mode="lines+markers+text",
        text=wp_df["node"],
        textposition="top center",
        line=dict(color="#F5B942", width=3, shape="spline"),
        marker=dict(size=10, color="#F5B942", line=dict(color="#090E1C", width=2)),
        name="Pump Price"
    ))

    # Benchmark Average
    fig_route.add_hline(
        y=p_met["avg_price"],
        line_dash="dot",
        line_color="rgba(148, 163, 184, 0.6)",
        annotation_text=f"Corridor Avg: {sym}{p_met['avg_price']:.2f}",
        annotation_position="bottom right"
    )

    fig_route.update_layout(
        paper_bgcolor=chart_paper_bg,
        plot_bgcolor=chart_plot_bg,
        font=dict(color="#94A3B8", family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto"),
        margin=dict(l=40, r=30, t=25, b=40),
        height=320,
        xaxis=dict(
            title="Cumulative Transit Distance (km)",
            gridcolor="rgba(255, 255, 255, 0.06)",
            zeroline=False
        ),
        yaxis=dict(
            title=f"Price ({code} / Litre)",
            gridcolor="rgba(255, 255, 255, 0.06)",
            zeroline=False
        ),
        showlegend=False
    )
    st.plotly_chart(fig_route, use_container_width=True)

with col_chart_tax:
    st.markdown("""
    <div style="font-size: 0.95rem; font-weight: 700; color: #F8FAFC; margin-bottom: 8px;">
        🏛️ Interstate VAT & Local Tax Disparity (% Spread)
    </div>
    """, unsafe_allow_html=True)

    # Bar chart for VAT and prices
    fig_tax = go.Figure()
    
    colors = ["#10B981" if w in p_met["cheapest_hubs"] else ("#F43F5E" if w in p_met["expensive_hubs"] else "#38BDF8") for w in wp_df["node"]]
    
    fig_tax.add_trace(go.Bar(
        x=wp_df["node"],
        y=wp_df["fuel_price"],
        marker_color=colors,
        text=[f"{sym}{p:.2f}<br>({v}%)" for p, v in zip(wp_df["fuel_price"], wp_df["vat_pct"])],
        textposition="auto",
        name="Price / L"
    ))

    fig_tax.update_layout(
        paper_bgcolor=chart_paper_bg,
        plot_bgcolor=chart_plot_bg,
        font=dict(color="#94A3B8", family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto"),
        margin=dict(l=40, r=30, t=25, b=40),
        height=320,
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            zeroline=False
        ),
        yaxis=dict(
            title=f"Price ({code} / Litre)",
            gridcolor="rgba(255, 255, 255, 0.06)",
            zeroline=False
        ),
        showlegend=False
    )
    st.plotly_chart(fig_tax, use_container_width=True)

# -------------------------------------------------------------
# 5. STEP-BY-STEP REFUELING MANIFEST & AI TACTICAL ADVICE
# -------------------------------------------------------------
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
    <div>
        <div style="font-weight: 700; color: #F8FAFC; font-size: 1.1rem; letter-spacing: 0.02em;">
            📋 STEP-BY-STEP AI REFUELING STRATEGY & MANIFEST
        </div>
        <div style="font-size: 0.8rem; color: #94A3B8;">
            Strategic waypoints: follow these stop instructions to achieve the guaranteed {sym}{fin['net_savings']:,.0f} savings.
        </div>
    </div>
    <div style="display: flex; gap: 8px;">
        <span style="font-size: 0.72rem; padding: 3px 8px; border-radius: 6px; background: rgba(16, 185, 129, 0.15); color: #34D399; font-weight: 700;">⭐ MAX REFUEL</span>
        <span style="font-size: 0.72rem; padding: 3px 8px; border-radius: 6px; background: rgba(244, 63, 94, 0.15); color: #FB7185; font-weight: 700;">🛑 AVOID REFUEL</span>
    </div>
</div>
""", unsafe_allow_html=True)

sched_df = pd.DataFrame(result["refuel_schedule"])

for _, row in sched_df.iterrows():
    action = row["action"]
    if "MAX REFUEL" in action:
        border_col = "rgba(16, 185, 129, 0.5)"
        badge_bg = "rgba(16, 185, 129, 0.15)"
        badge_text = "#34D399"
        card_bg = "linear-gradient(90deg, rgba(16, 185, 129, 0.08) 0%, #0D1527 100%)"
    elif "DO NOT REFUEL" in action:
        border_col = "rgba(244, 63, 94, 0.4)"
        badge_bg = "rgba(244, 63, 94, 0.15)"
        badge_text = "#FB7185"
        card_bg = "linear-gradient(90deg, rgba(244, 63, 94, 0.06) 0%, #0D1527 100%)"
    elif "Full Tank" in action:
        border_col = "rgba(245, 185, 66, 0.4)"
        badge_bg = "rgba(245, 185, 66, 0.15)"
        badge_text = "#F5B942"
        card_bg = "#0D1527"
    else:
        border_col = "rgba(255, 255, 255, 0.10)"
        badge_bg = "rgba(148, 163, 184, 0.12)"
        badge_text = "#94A3B8"
        card_bg = "#0D1527"

    fill_detail = f"Fill <b>{row['liters_filled']} L</b> ({sym}{row['cost']:,.2f})" if row['liters_filled'] > 0 else "0 Liters"

    st.markdown(f"""
    <div style="background: {card_bg}; border: 1px solid {border_col}; border-radius: 10px; padding: 12px 18px; margin-bottom: 8px;">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.15); display: flex; align-items: center; justify-content: center; font-weight: 700; color: #F8FAFC; font-size: 0.82rem;">
                    {row['step']}
                </div>
                <div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-weight: 700; color: #F8FAFC; font-size: 0.95rem;">{row['location']}</span>
                        <span style="font-size: 0.75rem; color: #94A3B8;">({row['jurisdiction']})</span>
                    </div>
                    <div style="font-size: 0.75rem; color: #64748B;">
                        Km Marker: <b>{row['km_mark']} km</b> • Pump Price: <b style="color: #F8FAFC;">{sym}{row['price']:.2f}/L</b> • Tax: <b>{row['vat_pct']}%</b>
                    </div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="text-align: right;">
                    <span style="display: inline-block; padding: 3px 10px; border-radius: 6px; background: {badge_bg}; color: {badge_text}; font-size: 0.78rem; font-weight: 700;">
                        {row['action']}
                    </span>
                    <div style="font-size: 0.75rem; color: #E2E8F0; margin-top: 3px;">{fill_detail}</div>
                </div>
            </div>
        </div>
        <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.05); font-size: 0.8rem; color: #CBD5E1;">
            💡 <b>Tactical Dispatch:</b> {row['reason']}
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 6. EXPORT MANIFEST (CSV)
# -------------------------------------------------------------
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
col_dl1, col_dl2 = st.columns([1.5, 3.5])

with col_dl1:
    csv_bytes = sched_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Export Trip Manifest (CSV)",
        data=csv_bytes,
        file_name=f"fuel_trip_manifest_{result['origin']}_{result['destination']}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col_dl2:
    st.markdown("""
    <div style="font-size: 0.75rem; color: #64748B; padding-top: 8px;">
        * Manifest ready for commercial dispatchers, fleet telematics management, or long-distance inter-city drivers.
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 7. UNIVERSAL AI ASSISTANT
# -------------------------------------------------------------
render_universal_ai_assistant(
    context_page="Highway Fuel Optimizer",
    key_prefix="hfo"
)
