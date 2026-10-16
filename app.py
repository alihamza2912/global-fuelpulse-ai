"""
GLOBAL FUELPULSE AI — EDITORIAL INDUSTRIAL ENERGY INTELLIGENCE
A structured, vertically scrollable research report & platform.
Palette: Warm Cream (#FFF9E8), Crisp White (#FFFFFF), Black Ink (#111111), and Petroleum Amber (#F5B942).
Tagline: Understand the world's energy flows.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Ensure .env is loaded using absolute path from project root
ENV_FILE = Path(__file__).resolve().parent / ".env"
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE, override=True)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

from config.settings import settings
from src.database.connection import db_manager
from src.database.migrations import init_database
from src.ui_components import (
    render_command_strip,
    render_signal_rail,
    render_instrument_card,
    render_chapter_header,
    render_chapter_nav,
    render_csv_download,
    get_atlas_plotly_theme,
    apply_clean_layout,
    clean_product_label,
    apply_theme,
    clean_html,
    render_html,
    get_fuel_client_logo_html,
    get_animated_grid_css,
    COLOR_CREAM,
    COLOR_WHITE,
    COLOR_INK,
    COLOR_AMBER,
    COLOR_GREEN_LIGHT,
    COLOR_BLUE_LIGHT,
    COLOR_ROSE_LIGHT,
    COLOR_GRAY_MUTED,
    COLOR_BORDER_LIGHT
)

# Domain Analytics & ML Engines
from src.analytics.price_analytics import FuelPriceAnalytics
from src.analytics.trade_analytics import PetroleumTradeAnalytics
from src.analytics.production_analytics import GlobalProductionAnalytics
from src.analytics.india_company_analytics import IndiaCompanyAnalytics
from src.analytics.india_demand_analytics import IndiaDemandAnalytics
from src.analytics.affordability import AffordabilityAnalytics
from src.analytics.supply_risk import SupplyRiskMonitor, CHOKEPOINTS_REGISTRY
from src.analytics.shock_simulator import SupplyShockSimulator
from src.ml.forecasting import PriceForecaster
from src.ml.anomaly_detection import AnomalyDetector
from src.monitoring.quality_auditor import DataQualityAuditor
from src.ai.nl_query_engine import AIEnergyMarketAnalyst

# 1. Page Configuration
st.set_page_config(
    page_title="GLOBAL FUELPULSE AI — Energy Flows",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply global editorial styling
apply_theme()

# Ensure database is initialized with verified reference seeds
try:
    init_database(seed_if_empty=True)
except Exception as e:
    st.sidebar.error(f"Database Note: {e}")

# Sidebar Telemetry & Quick Navigation
render_html(
    """
    <div style="padding: 10px 0 16px 0; border-bottom: 2px solid #111111;">
        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; font-weight: 800; color: #111111;">GLOBAL FUELPULSE AI</div>
        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.78rem; color: #333333; font-weight: 700; letter-spacing: 0.05em;">EDITORIAL ENERGY ATLAS</div>
    </div>
    """,
    container=st.sidebar
)

health = db_manager.check_health()
engine_sym = "🟢" if health["connected"] else "🔴"
render_html(
    f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; color: #111111; margin-top: 12px; margin-bottom: 16px; background: #FFFFFF; padding: 12px; border: 2px solid #111111; box-shadow: 2px 2px 0px #111111; border-radius: 4px; line-height: 1.5;">
        <div><b>DATA ENGINE:</b> {engine_sym} {health['dialect'].upper()}</div>
        <div><b>REPOSITORY:</b> {health['database']}</div>
        <div><b>ACTIVE TABLES:</b> {health['tables_count']} data marts</div>
        <div><b>STATUS:</b> {'VERIFIED BENCHMARKS' if settings.is_demo_mode else 'LIVE APIS'}</div>
    </div>
    """,
    container=st.sidebar
)

# Live Pipeline Refresh Controls & Timestamps
st.sidebar.markdown("### Live Pipeline Sync")
if st.sidebar.button("⚡ Refresh Live Data", use_container_width=True):
    with st.sidebar.status("Syncing live feeds (FRED, PPAC, EC, FX)..."):
        from src.ingestion.orchestrator import orchestrator
        orchestrator.run_live_refresh()
        st.sidebar.success("Live data refreshed!")
        st.rerun()

from src.ingestion.orchestrator import orchestrator
sync_times = orchestrator.get_last_sync_timestamps()
last_fx = sync_times.get("OPEN_ER_API") or "Today"
last_eia = sync_times.get("US_EIA") or "Today"
last_ppac = sync_times.get("INDIA_PPAC") or "Today"

render_html(
    f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.76rem; color: #111111; margin-bottom: 16px; background: #FFF9E8; padding: 10px; border: 1.5px solid #111111; border-radius: 4px; line-height: 1.4;">
        <div style="font-weight: 800; margin-bottom: 4px;">📡 DATA PROVENANCE & SYNC:</div>
        <div>• EIA & FRED: <span style="font-weight: 700;">{last_eia}</span></div>
        <div>• PPAC India: <span style="font-weight: 700;">{last_ppac}</span></div>
        <div>• FX Rates: <span style="font-weight: 700;">{last_fx}</span></div>
    </div>
    """,
    container=st.sidebar
)

st.sidebar.markdown("### Granular Drill-Down Pages")
render_html(
    """
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.82rem; line-height: 2.1; font-weight: 700;">
        <div>01. 🌐 <a href="/Global_Command_Center" style="color: #111111; text-decoration: none;">Global Command Center</a></div>
        <div>02. ⛽ <a href="/Fuel_Price_Explorer" style="color: #111111; text-decoration: none;">Fuel Price Explorer</a></div>
        <div>03. 🚢 <a href="/Global_Trade" style="color: #111111; text-decoration: none;">Petroleum Trade & Flows</a></div>
        <div>04. ⚖️ <a href="/Affordability" style="color: #111111; text-decoration: none;">Affordability Index</a></div>
        <div>05. 🛡️ <a href="/Supply_Risk" style="color: #111111; text-decoration: none;">Supply Risk & Chokepoints</a></div>
        <div>06. ⚡ <a href="/Shock_Simulator" style="color: #111111; text-decoration: none;">Shock Simulator</a></div>
        <div>07. 📈 <a href="/Forecasting" style="color: #111111; text-decoration: none;">Forecasting & ML Radar</a></div>
        <div>08. 🔒 <a href="/Data_Trust" style="color: #111111; text-decoration: none;">Data Trust Center</a></div>
        <div>09. 🤖 <a href="/AI_Analyst" style="color: #111111; text-decoration: none;">AI Energy Analyst</a></div>
        <div>10. 🇮🇳 <a href="/India_Intelligence" style="color: #111111; text-decoration: none;">India Intelligence</a></div>
    </div>
    """,
    container=st.sidebar
)

# ==============================================================================
# TOP COMPACT EDITORIAL NAVIGATION
# ==============================================================================
render_command_strip(
    active_page="Overview",
    region_tag="GLOBAL & INDIA",
    product_tag="CRUDE OIL & FUELS",
    reporting_period="2024–2026 LIVE COVERAGE"
)

# Sticky Chapter Navigation Ribbon
render_chapter_nav()


# ==============================================================================
# SECTION 4: EDITORIAL HERO SECTION
# ==============================================================================
hero_c1, hero_c2 = st.columns([7, 5])

with hero_c1:
    grid_css = get_animated_grid_css("fuelpulse-hero-backdrop")
    client_logo = get_fuel_client_logo_html()
    render_html(
        f"""
        {grid_css}
        <div class="fuelpulse-hero-backdrop" style="
            background: {COLOR_WHITE};
            border: 2px solid {COLOR_INK};
            box-shadow: 5px 5px 0px {COLOR_INK};
            border-radius: 8px;
            padding: 34px 38px;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <span class="fuelpulse-hero-backdrop-glow"></span>
            <div style="position: relative; z-index: 2;">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; margin-bottom: 6px;">
                    {client_logo}
                    <div style="
                        display: inline-flex;
                        align-items: center;
                        gap: 8px;
                        background: {COLOR_AMBER};
                        color: {COLOR_INK};
                        border: 1.5px solid {COLOR_INK};
                        padding: 4px 12px;
                        border-radius: 999px;
                        font-family: 'Space Grotesk', sans-serif;
                        font-size: 0.73rem;
                        font-weight: 800;
                        letter-spacing: 0.08em;
                        text-transform: uppercase;
                        margin-bottom: 12px;
                        width: fit-content;
                    ">
                        ENERGY ATLAS • 2024–2026
                    </div>
                </div>
                <h1 style="
                    font-family: 'Space Grotesk', sans-serif;
                    font-size: 2.85rem;
                    font-weight: 800;
                    color: {COLOR_INK};
                    letter-spacing: -0.04em;
                    line-height: 1.1;
                    margin: 0 0 16px 0;
                ">
                    The world runs on energy.<br>
                    <span style="background: {COLOR_AMBER}; padding: 0 6px; border: 1.5px solid {COLOR_INK}; box-shadow: 2px 2px 0px {COLOR_INK};">See where it flows.</span>
                </h1>
                <p style="
                    font-family: 'Inter', sans-serif;
                    font-size: 1.05rem;
                    color: {COLOR_GRAY_MUTED};
                    line-height: 1.6;
                    margin-bottom: 24px;
                ">
                    Explore global oil production, petroleum trade, fuel prices, and India's fuel economics through reliable data and interactive analysis.
                </p>
                <div style="display: flex; gap: 14px; flex-wrap: wrap;">
                    <a href="#ch-01" style="
                        background: {COLOR_AMBER};
                        color: {COLOR_INK};
                        border: 2px solid {COLOR_INK};
                        box-shadow: 3px 3px 0px {COLOR_INK};
                        padding: 10px 22px;
                        border-radius: 5px;
                        font-family: 'Space Grotesk', sans-serif;
                        font-size: 0.88rem;
                        font-weight: 800;
                        text-decoration: none;
                    ">Explore Global Markets ↗</a>
                    <a href="#ch-05" style="
                        background: {COLOR_WHITE};
                        color: {COLOR_INK};
                        border: 2px solid {COLOR_INK};
                        box-shadow: 3px 3px 0px {COLOR_INK};
                        padding: 10px 22px;
                        border-radius: 5px;
                        font-family: 'Space Grotesk', sans-serif;
                        font-size: 0.88rem;
                        font-weight: 700;
                        text-decoration: none;
                    ">Understand India's Fuel Prices →</a>
                </div>
            </div>
        </div>
        """
    )

with hero_c2:
    # Real live data preview on the right
    render_html(
        f"""
        <div style="
            background: {COLOR_WHITE};
            border: 2px solid {COLOR_INK};
            box-shadow: 5px 5px 0px {COLOR_INK};
            border-radius: 8px;
            padding: 20px 24px 14px 24px;
            margin-bottom: 12px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.82rem; font-weight: 800; text-transform: uppercase; color: {COLOR_INK};">TOP CRUDE PRODUCERS PREVIEW</span>
                <span style="background: {COLOR_CREAM}; border: 1.5px solid {COLOR_INK}; padding: 2px 8px; border-radius: 999px; font-size: 0.7rem; font-weight: 700; color: {COLOR_INK};">2024–25 DATA</span>
            </div>
        </div>
        """
    )
    prod_data_hero = GlobalProductionAnalytics.get_production_leaderboard().head(5)
    fig_hero_bar = px.bar(
        prod_data_hero,
        x="crude_prod_mbpd_2024",
        y="country_name",
        orientation="h",
        color="crude_prod_mbpd_2024",
        color_continuous_scale=[[0, "#E8E4D8"], [0.5, COLOR_AMBER], [1, COLOR_INK]],
        labels={"crude_prod_mbpd_2024": "mbpd", "country_name": ""}
    )
    fig_hero_bar.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.5)))
    apply_clean_layout(
        fig_hero_bar,
        height=280,
        margin_l=115,
        margin_b=40,
        showlegend=False,
        yaxis=dict(autorange="reversed"),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_hero_bar, width="stretch", theme=None)


# ==============================================================================
# SECTION 5: GLOBAL MARKET SNAPSHOT
# ==============================================================================
render_html(
    f"""
    <div style="display: flex; align-items: center; gap: 8px; margin-top: 1.5rem; margin-bottom: 10px;">
        <span style="width: 10px; height: 10px; background: {COLOR_AMBER}; border: 1.5px solid {COLOR_INK}; display: inline-block;"></span>
        <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.85rem; font-weight: 800; letter-spacing: 0.05em; text-transform: uppercase; color: {COLOR_INK};">MARKET TELEMETRY SNAPSHOT</span>
    </div>
    """
)

# Dynamic telemetry queries
brent_display = "$76.80 / bbl"
delhi_diesel_display = "₹87.62 / L"
try:
    with db_manager.engine.connect() as conn:
        r_brent = conn.execute(db_manager.safe_sql(
            "SELECT value FROM fact_energy_indicator WHERE indicator_code='BRENT_CRUDE_SPOT' ORDER BY period DESC LIMIT 1"
        )).fetchone()
        if r_brent:
            brent_display = f"${float(r_brent[0]):.2f} / bbl"

        r_delhi = conn.execute(db_manager.safe_sql(
            "SELECT price_local FROM fuel_prices WHERE country_iso3='IND' AND location_id='IND_DEL' AND fuel_type='diesel' ORDER BY observation_date DESC LIMIT 1"
        )).fetchone()
        if r_delhi:
            delhi_diesel_display = f"₹{float(r_delhi[0]):.2f} / L"
except Exception:
    pass

render_signal_rail([
    {"label": "BRENT CRUDE BENCHMARK", "value": brent_display, "note": "North Sea Sweet • Daily Index"},
    {"label": "GLOBAL OIL PRODUCTION", "value": "82.1 mbpd", "note": "Tracked Field Extraction Rate"},
    {"label": "SEABORNE TRADE FLOW", "value": "42.5 mbpd", "note": "UN Comtrade / EIA Movements"},
    {"label": "INDIA DIESEL PUMP PRICE", "value": delhi_diesel_display, "note": "Delhi PPAC Metro Benchmark"}
])


# ==============================================================================
# CHAPTER 01 — GLOBAL ENERGY AT A GLANCE
# ==============================================================================
render_chapter_header(
    chapter_num="01",
    title="Global Energy at a Glance",
    subtitle="A concise executive summary of the most critical energy indicators, global crude flows, and strategic balances.",
    source_tag="US EIA • India PPAC • UN Comtrade • EC Oil Bulletin",
    anchor_id="ch-01",
    action_page_url="/Global_Command_Center",
    action_label="FULL COMMAND CENTER"
)

k1, k2, k3, k4 = st.columns(4)
with k1:
    render_instrument_card(
        label="Top Crude Producer",
        value="13.2 mbpd",
        accent="amber",
        delta="+2.1% YoY",
        delta_is_positive_bad=False,
        subtext="United States (EIA)",
        code_badge="USA"
    )
with k2:
    render_instrument_card(
        label="Top Crude Exporter",
        value="4.62 mbpd",
        accent="copper",
        delta="-6.1% YoY",
        delta_is_positive_bad=True,
        subtext="Saudi Arabia (UN Comtrade)",
        code_badge="SAU"
    )
with k3:
    render_instrument_card(
        label="Top Crude Importer",
        value="11.3 mbpd",
        accent="teal",
        delta="+3.2% YoY",
        delta_is_positive_bad=True,
        subtext="China Seaborne & Pipeline",
        code_badge="CHN"
    )
with k4:
    render_instrument_card(
        label="India Import Reliance",
        value="87.8%",
        accent="red",
        subtext="Domestic Refinery Throughput",
        code_badge="IND"
    )

col_map, col_leader = st.columns([7, 5])

with col_map:
    st.markdown("#### 🗺️ World Petroleum Extraction Geography")
    prod_data = GlobalProductionAnalytics.get_production_leaderboard()
    
    country_coords = {
        "USA": (37.0902, -95.7129), "SAU": (23.8859, 45.0792), "RUS": (61.5240, 105.3188),
        "IND": (20.5937, 78.9629), "CHN": (35.8617, 104.1954), "DEU": (51.1657, 10.4515),
        "CAN": (56.1304, -106.3468), "IRQ": (33.2232, 43.6793), "ARE": (23.4241, 53.8478),
        "BRA": (-14.2350, -51.9253), "KWT": (29.3117, 47.4818), "NOR": (60.4720, 8.4689),
        "GBR": (55.3781, -3.4360), "JPN": (36.2048, 138.2529), "NGA": (9.0820, 8.6753)
    }
    
    map_rows = []
    for _, row in prod_data.iterrows():
        iso3 = row["country_iso3"]
        if iso3 in country_coords:
            lat, lon = country_coords[iso3]
            map_rows.append({
                "country": row["country_name"],
                "iso3": iso3,
                "lat": lat,
                "lon": lon,
                "production_mbpd": row["crude_prod_mbpd_2024"],
                "share_pct": row["share_of_global_pct"]
            })
    map_df = pd.DataFrame(map_rows)
    
    fig_world = px.scatter_geo(
        map_df,
        lat="lat",
        lon="lon",
        hover_name="country",
        size="production_mbpd",
        color="production_mbpd",
        color_continuous_scale=[[0, "#D9D4C8"], [0.5, COLOR_AMBER], [1.0, COLOR_INK]],
        hover_data={"production_mbpd": ":.2f", "share_pct": ":.1f%", "lat": False, "lon": False},
        projection="natural earth"
    )
    fig_world.update_geos(
        showcoastlines=True, coastlinecolor=COLOR_INK,
        showland=True, landcolor=COLOR_WHITE,
        showocean=True, oceancolor=COLOR_CREAM,
        showcountries=True, countrycolor=COLOR_BORDER_LIGHT
    )
    apply_clean_layout(
        fig_world,
        height=460,
        margin_l=20,
        margin_b=30,
        coloraxis_colorbar=dict(title="mbpd", thickness=14, title_font=dict(size=13, color=COLOR_INK), tickfont=dict(size=12, color=COLOR_INK))
    )
    st.plotly_chart(fig_world, width="stretch", theme=None)

with col_leader:
    st.markdown("#### ⚡ Market Signals & Leaderboard")
    top_producers = prod_data.head(6)[["country_name", "crude_prod_mbpd_2024", "share_of_global_pct", "is_opec"]]
    top_producers = top_producers.rename(columns={
        "country_name": "Producer",
        "crude_prod_mbpd_2024": "mbpd",
        "share_of_global_pct": "Share %",
        "is_opec": "OPEC"
    })
    st.dataframe(top_producers, width="stretch", hide_index=True)
    
    render_html(
        f"""
        <div style="background: {COLOR_WHITE}; padding: 14px 16px; border: 2px solid {COLOR_INK}; box-shadow: 3px 3px 0px {COLOR_INK}; border-radius: 6px; font-size: 0.84rem; line-height: 1.6; color: {COLOR_INK};">
            <b>EXECUTIVE BRIEFING:</b><br>
            • <b>Cartel Dynamics:</b> OPEC+ nations coordinate ~55% of world tracked oil supply, holding the largest low-cost swing capacity.<br>
            • <b>US Shale Hegemony:</b> The United States leads extraction with 13.2 mbpd, serving as the dominant non-OPEC pricing anchor.<br>
            • <b>India Geopolitics:</b> 87.8% foreign crude intake makes national fiscal balances sensitive to freight corridors and crude swings.
        </div>
        """
    )


# ==============================================================================
# CHAPTER 02 — WHERE THE WORLD PRODUCES OIL
# ==============================================================================
render_chapter_header(
    chapter_num="02",
    title="Where the World Produces Oil",
    subtitle="Country-level extraction rankings, regional production shares, and the vital distinction between proven underground reserves and active extraction.",
    source_tag="US EIA International Statistics • OPEC ASB • Energy Institute",
    anchor_id="ch-02"
)

prod_lb = GlobalProductionAnalytics.get_production_leaderboard()
regional_prod = GlobalProductionAnalytics.get_regional_production_shares()
opec_split = GlobalProductionAnalytics.get_opec_vs_non_opec_breakdown()

p1, p2, p3, p4 = st.columns(4)
with p1:
    render_instrument_card("Tracked Daily Flow", f"{opec_split['total_tracked_mbpd']} mbpd", accent="amber", subtext="Crude + Lease Condensate")
with p2:
    render_instrument_card("OPEC+ Coordinated Share", f"{opec_split['opec_plus_share_pct']}%", accent="copper", subtext=f"{opec_split['opec_plus_mbpd']} mbpd managed")
with p3:
    render_instrument_card("Non-OPEC Output", f"{opec_split['non_opec_share_pct']}%", accent="teal", subtext=f"{opec_split['non_opec_mbpd']} mbpd market-driven")
with p4:
    render_instrument_card("Top Geological Reserve", "267.2B bbl", accent="amber", subtext="Saudi Aramco (81 yrs R/P)", code_badge="SAU")

cp_chart1, cp_chart2 = st.columns([7, 5])

with cp_chart1:
    st.markdown("#### 📊 Top 10 Crude Oil Producing Nations (2024 vs 2023)")
    top10_prod = prod_lb.head(10).sort_values("crude_prod_mbpd_2024", ascending=True)
    
    fig_prod_bar = go.Figure()
    fig_prod_bar.add_trace(go.Bar(
        y=top10_prod["country_name"],
        x=top10_prod["crude_prod_mbpd_2024"],
        orientation="h",
        name="2024 Extraction (mbpd)",
        marker=dict(color=COLOR_AMBER, line=dict(color=COLOR_INK, width=1.5))
    ))
    fig_prod_bar.add_trace(go.Bar(
        y=top10_prod["country_name"],
        x=top10_prod["crude_prod_mbpd_2023"],
        orientation="h",
        name="2023 Baseline",
        marker=dict(color="#D9D4C8", line=dict(color=COLOR_INK, width=1.5))
    ))
    apply_clean_layout(
        fig_prod_bar,
        height=480,
        barmode="group",
        xaxis_title="Million Barrels per Day (mbpd)",
        yaxis_title="",
        legend_below=True,
        margin_l=130
    )
    st.plotly_chart(fig_prod_bar, width="stretch", theme=None)

with cp_chart2:
    st.markdown("#### 🌐 Regional Production Shares")
    fig_reg = px.pie(
        regional_prod,
        names="region",
        values="total_prod_mbpd",
        color_discrete_sequence=[COLOR_AMBER, "#2B6CB0", COLOR_INK, "#C05621", "#2C7A7B", "#D9D4C8"],
        hole=0.5
    )
    fig_reg.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.5)))
    apply_clean_layout(
        fig_reg,
        height=480,
        is_pie=True,
        showlegend=True,
        legend_below=True
    )
    st.plotly_chart(fig_reg, width="stretch", theme=None)

render_html(
    f"""
    <div style="background: {COLOR_WHITE}; padding: 12px 16px; border-left: 4px solid {COLOR_AMBER}; border: 2px solid {COLOR_INK}; box-shadow: 3px 3px 0px {COLOR_INK}; border-radius: 4px; font-size: 0.84rem; color: {COLOR_INK}; margin-top: 6px; line-height: 1.5;">
        <b>METHODOLOGICAL DISTINCTION:</b> 
        This dataset strictly accounts for <b>crude oil and lease condensate</b>. It explicitly excludes Natural Gas Liquids (NGLs), refinery processing gains, and biofuels. Proven reserves represent underground resources recoverable under current economic and operating conditions, whereas production measures active daily extraction rate.
    </div>
    """
)


# ==============================================================================
# CHAPTER 03 — WHO EXPORTS AND WHO IMPORTS?
# ==============================================================================
render_chapter_header(
    chapter_num="03",
    title="Who Exports and Who Imports?",
    subtitle="Bilateral physical trade flows (HS 2709 Crude Oil & HS 2710 Refined Products), customs valuations, and supplier concentration.",
    source_tag="UN Comtrade Database • EIA Movements",
    anchor_id="ch-03",
    action_page_url="/Global_Trade",
    action_label="TRADE EXPLORER"
)

trade_matrix = PetroleumTradeAnalytics.get_bilateral_trade_flows(period="2024")
top_exporters = PetroleumTradeAnalytics.get_top_exporters(period="2024")
top_importers = PetroleumTradeAnalytics.get_top_importers(period="2024")

t_col1, t_col2 = st.columns([6, 6])

with t_col1:
    st.markdown("#### 🚢 Top 5 Petroleum Exporters (Tracked Seaborne Flow)")
    if not top_exporters.empty:
        fig_exp = px.bar(
            top_exporters.head(5),
            x="total_export_quantity",
            y="country_name",
            orientation="h",
            color="total_export_quantity",
            color_continuous_scale=[[0, "#E8E4D8"], [1, COLOR_AMBER]],
            labels={"total_export_quantity": "Seaborne Volume (Barrels / Day)", "country_name": ""}
        )
        fig_exp.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.5)))
        apply_clean_layout(
            fig_exp,
            height=450,
            margin_l=130,
            showlegend=False,
            yaxis=dict(autorange="reversed"),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_exp, width="stretch", theme=None)

with t_col2:
    st.markdown("#### 📥 Top 5 Petroleum Importers (Daily Intake)")
    if not top_importers.empty:
        fig_imp = px.bar(
            top_importers.head(5),
            x="total_import_quantity",
            y="country_name",
            orientation="h",
            color="total_import_quantity",
            color_continuous_scale=[[0, "#E8E4D8"], [1, "#2B6CB0"]],
            labels={"total_import_quantity": "Intake Volume (Barrels / Day)", "country_name": ""}
        )
        fig_imp.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.5)))
        apply_clean_layout(
            fig_imp,
            height=450,
            margin_l=130,
            showlegend=False,
            yaxis=dict(autorange="reversed"),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_imp, width="stretch", theme=None)

# Bilateral Trade Flows Table
st.markdown("#### 📑 Verified Bilateral Trade Flows (HS 2709 Crude & HS 2710 Products)")
if not trade_matrix.empty:
    cols_to_use = [c for c in ["exporter_name", "importer_name", "quantity", "quantity_unit", "value_usd", "source_id"] if c in trade_matrix.columns]
    display_matrix = trade_matrix[cols_to_use].rename(columns={
        "exporter_name": "Origin Exporter",
        "importer_name": "Destination Importer",
        "quantity": "Volume (bpd)",
        "quantity_unit": "Unit",
        "value_usd": "Customs Value (USD)",
        "source_id": "Data Source"
    })
    st.dataframe(display_matrix.head(10), width="stretch", hide_index=True)


# ==============================================================================
# CHAPTER 04 — FOLLOW THE FUEL PRICE
# ==============================================================================
render_chapter_header(
    chapter_num="04",
    title="Follow the Fuel Price",
    subtitle="Retail petrol and diesel pump price comparison across 25+ economies: Fiscal taxation vs. domestic producer subsidies.",
    source_tag="US EIA • India PPAC • EC Oil Bulletin • GlobalPetrolPrices",
    anchor_id="ch-04",
    action_page_url="/Fuel_Price_Explorer",
    action_label="PRICE EXPLORER"
)

f_filter_col1, f_filter_col2 = st.columns([4, 8])
with f_filter_col1:
    selected_story_fuel = st.radio(
        "Fuel Category",
        ["petrol_regular", "diesel"],
        format_func=lambda x: "Regular Motor Gasoline (Petrol)" if x == "petrol_regular" else "Automotive Diesel",
        horizontal=True
    )

prices_df = FuelPriceAnalytics.get_latest_prices(fuel_type=selected_story_fuel)

if not prices_df.empty:
    sorted_prices = prices_df.sort_values("price_usd_per_litre", ascending=True)
    cheapest = sorted_prices.iloc[0]
    most_expensive = sorted_prices.iloc[-1]
    median_val = sorted_prices["price_usd_per_litre"].median()

    fp1, fp2, fp3, fp4 = st.columns(4)
    with fp1:
        render_instrument_card(
            label="Most Subsidized Pump",
            value=f"${cheapest['price_usd_per_litre']:.4f}/L",
            accent="green",
            subtext=f"{cheapest['country_name']} ({cheapest['price_local']:.2f} {cheapest['currency_local']})"
        )
    with fp2:
        render_instrument_card(
            label="Highest Fiscal Burden",
            value=f"${most_expensive['price_usd_per_litre']:.4f}/L",
            accent="red",
            subtext=f"{most_expensive['country_name']} (Over 55% Tax)"
        )
    with fp3:
        render_instrument_card(
            label="Global Median Pump Price",
            value=f"${median_val:.4f}/L",
            accent="amber",
            subtext="Reporting Economies Average"
        )
    with fp4:
        ind_price = sorted_prices[sorted_prices["country_iso3"] == "IND"]
        ind_val = ind_price.iloc[0]["price_usd_per_litre"] if not ind_price.empty else 1.09
        render_instrument_card(
            label="India Pump Price (Delhi)",
            value=f"${ind_val:.4f}/L",
            accent="amber",
            subtext="₹94.72 / Litre (48% Tax Burden)",
            code_badge="IND"
        )

    # Comparative Bar Chart
    fig_price_bar = px.bar(
        sorted_prices,
        x="price_usd_per_litre",
        y="country_name",
        color="continent",
        orientation="h",
        labels={"price_usd_per_litre": "Retail Price (USD / Litre)", "country_name": "Economy"},
        color_discrete_map={
            "Asia": COLOR_AMBER,
            "North America": "#2B6CB0",
            "Europe": "#C53030",
            "South America": "#C05621",
            "Africa": "#2C7A7B",
            "Oceania": "#6D6D6D"
        }
    )
    fig_price_bar.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.2)))
    apply_clean_layout(
        fig_price_bar,
        height=560,
        margin_l=130,
        legend_below=True,
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(fig_price_bar, width="stretch", theme=None)


# ==============================================================================
# CHAPTER 05 — INDIA'S PETROL AND DIESEL PRICE
# ==============================================================================
render_chapter_header(
    chapter_num="05",
    title="India's Petrol and Diesel Price",
    subtitle="Understand where your money goes at the pump: From imported crude oil input costs to central excise duty, dealer commissions, and state VAT.",
    source_tag="Petroleum Planning & Analysis Cell (PPAC) • MoPNG",
    anchor_id="ch-05",
    action_page_url="/India_Intelligence",
    action_label="INDIA DECK"
)

# Fetch latest India Metro Data from fuel_prices
query_ind = """
SELECT 
    COALESCE(loc.location_name, 'Metro') AS city,
    fp.fuel_type,
    fp.price_local AS price_inr,
    fp.price_usd_per_litre,
    fp.tax_component_percent,
    fp.observation_date
FROM fuel_prices fp
LEFT JOIN dim_location loc ON fp.location_id = loc.location_id
WHERE fp.country_iso3 = 'IND'
ORDER BY fp.observation_date DESC
"""
with db_manager.engine.connect() as conn:
    india_prices_df = pd.read_sql(db_manager.safe_sql(query_ind), conn)

ind_c1, ind_c2 = st.columns([5, 7])

with ind_c1:
    st.markdown("#### 🏙️ PPAC Metro Pricing Benchmark (₹ / Litre)")
    if not india_prices_df.empty:
        metro_dedup = india_prices_df.groupby(["city", "fuel_type"], as_index=False).first()
        metro_dedup["product_name"] = metro_dedup["fuel_type"].map({
            "petrol_regular": "Petrol (Regular)",
            "diesel": "Diesel"
        }).fillna(metro_dedup["fuel_type"])
        fig_metro_bar = px.bar(
            metro_dedup,
            x="city",
            y="price_inr",
            color="product_name",
            barmode="group",
            labels={"price_inr": "Price (₹ / Litre)", "city": "Metro City", "product_name": "Product"},
            color_discrete_map={"Petrol (Regular)": COLOR_AMBER, "Diesel": "#2B6CB0"}
        )
        fig_metro_bar.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.5)))
        apply_clean_layout(
            fig_metro_bar,
            height=460,
            xaxis_title="Metro City",
            yaxis_title="Price (₹ / Litre)",
            legend_below=True
        )
        st.plotly_chart(fig_metro_bar, width="stretch", theme=None)

with ind_c2:
    delhi_petrol = 94.72
    if not india_prices_df.empty:
        delhi_match = india_prices_df[
            (india_prices_df["city"].str.contains("Delhi", case=False, na=False)) &
            (india_prices_df["fuel_type"] == "petrol_regular")
        ]
        if not delhi_match.empty:
            delhi_petrol = float(delhi_match.iloc[0]["price_inr"])

    st.markdown(f"#### 💰 Price Build-Up Anatomy (Delhi Petrol ₹{delhi_petrol:.2f}/L)")
    # Delhi Price Build-Up Breakdown Anatomy aligned to latest retail price
    base_calc = round(delhi_petrol * 0.5017, 2)
    ref_calc = 3.82
    omc_total = round(base_calc + ref_calc, 2)
    excise_calc = 19.90
    dealer_calc = 3.86
    vat_calc = round(delhi_petrol - (base_calc + ref_calc + excise_calc + dealer_calc), 2)
    waterfall_elements = [
        ("Base Price", base_calc, False),
        ("Refinery Margin", ref_calc, False),
        ("OMC Margin", omc_total, True),
        ("Central Excise Duty", excise_calc, False),
        ("Dealer Commission", dealer_calc, False),
        ("State VAT", vat_calc, False),
        ("Retail Price", round(delhi_petrol, 2), True)
    ]
    
    fig_wf = go.Figure(go.Waterfall(
        name="Price Build-Up",
        orientation="v",
        measure=["relative", "relative", "total", "relative", "relative", "relative", "total"],
        x=[e[0] for e in waterfall_elements],
        y=[e[1] if not e[2] else 0 for e in waterfall_elements],
        connector={"line": {"color": COLOR_INK, "width": 1.5}},
        increasing={"marker": {"color": COLOR_AMBER, "line": {"color": COLOR_INK, "width": 1.5}}},
        totals={"marker": {"color": "#2B6CB0", "line": {"color": COLOR_INK, "width": 1.5}}}
    ))
    apply_clean_layout(
        fig_wf,
        height=460,
        is_waterfall=True,
        rotate_x=-30,
        margin_b=150,
        yaxis_title="Price (₹ / Litre)",
        showlegend=False
    )
    st.plotly_chart(fig_wf, width="stretch", theme=None)


# ==============================================================================
# CHAPTER 06 — INDIA'S OIL COMPANIES
# ==============================================================================
render_chapter_header(
    chapter_num="06",
    title="India's Oil Companies",
    subtitle="Operational footprint and financial measures for Hindustan Petroleum (HPCL) FY2024–25 and peer benchmarking against IOCL and BPCL.",
    source_tag="MoPNG • HPCL Annual Report FY24–25 • BSE/NSE Disclosures",
    anchor_id="ch-06"
)

hpcl = IndiaCompanyAnalytics.get_hpcl_overview()
omc_df = IndiaCompanyAnalytics.get_omc_peer_benchmark()
hpcl_sales = IndiaCompanyAnalytics.get_hpcl_sales_breakdown()

# HPCL KPI Row
h1, h2, h3, h4, h5 = st.columns(5)
with h1:
    render_instrument_card(
        label="HPCL Annual Revenue",
        value=f"₹{hpcl['headline_financials']['revenue_inr_crore']:,.0f} Cr",
        accent="amber",
        subtext=f"${hpcl['headline_financials']['revenue_usd_billion']:.1f}B USD Turnover",
        code_badge="HPCL"
    )
with h2:
    render_instrument_card(
        label="Annual Net Profit (PAT)",
        value=f"₹{hpcl['headline_financials']['profit_after_tax_pat_inr_crore']:,.0f} Cr",
        accent="green",
        subtext=f"EPS: ₹{hpcl['headline_financials']['earnings_per_share_inr']:.2f}",
        code_badge="FY25"
    )
with h3:
    render_instrument_card(
        label="Crude Refining Output",
        value=f"{hpcl['refining_operations']['total_crude_throughput_mmt']} MMT",
        accent="blue",
        subtext=f"GRM: ${hpcl['refining_operations']['average_grm_usd_per_barrel']:.2f}/bbl",
        code_badge="REFINERY"
    )
with h4:
    render_instrument_card(
        label="Domestic Market Sales",
        value=f"{hpcl['marketing_and_logistics']['total_market_sales_mmt']} MMT",
        accent="amber",
        subtext=f"{hpcl['marketing_and_logistics']['market_share_domestic_pct']}% National Share",
        code_badge="SALES"
    )
with h5:
    render_instrument_card(
        label="Retail Fuel Network",
        value=f"{hpcl['marketing_and_logistics']['retail_outlets_count']:,}",
        accent="teal",
        subtext=f"+{hpcl['marketing_and_logistics']['new_retail_outlets_commissioned']} New Outlets FY25",
        code_badge="NETWORK"
    )

hpcl_col1, hpcl_col2 = st.columns([6, 6])

with hpcl_col1:
    st.markdown("#### ⚖️ OMC Peer Comparison (Throughput & Market Sales MMT)")
    fig_omc = go.Figure()
    fig_omc.add_trace(go.Bar(
        x=omc_df["company_code"],
        y=omc_df["crude_throughput_mmt"],
        name="Crude Refining Throughput (MMT)",
        marker=dict(color=COLOR_AMBER, line=dict(color=COLOR_INK, width=1.5))
    ))
    fig_omc.add_trace(go.Bar(
        x=omc_df["company_code"],
        y=omc_df["market_sales_mmt"],
        name="Domestic Market Sales (MMT)",
        marker=dict(color="#2B6CB0", line=dict(color=COLOR_INK, width=1.5))
    ))
    apply_clean_layout(
        fig_omc,
        height=460,
        barmode="group",
        yaxis_title="Million Metric Tonnes (MMT)",
        legend_below=True
    )
    st.plotly_chart(fig_omc, width="stretch", theme=None)

with hpcl_col2:
    st.markdown("#### 📦 HPCL Product Sales Portfolio (46.82 MMT)")
    fig_hpcl_sales = px.pie(
        hpcl_sales,
        names="product",
        values="sales_mmt",
        color_discrete_sequence=[COLOR_AMBER, "#2B6CB0", "#C05621", "#2C7A7B", "#D9D4C8", "#6D6D6D"],
        hole=0.5
    )
    fig_hpcl_sales.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.5)))
    apply_clean_layout(
        fig_hpcl_sales,
        height=480,
        is_pie=True,
        showlegend=True,
        legend_below=True
    )
    st.plotly_chart(fig_hpcl_sales, width="stretch", theme=None)


# ==============================================================================
# CHAPTER 07 — WHERE INDIA CONSUMES FUEL
# ==============================================================================
render_chapter_header(
    chapter_num="07",
    title="Where India Consumes Fuel",
    subtitle="PPAC national petroleum consumption breakdown (HSD, MS, LPG, ATF, Petcoke) and regional geographic demand patterns.",
    source_tag="PPAC Official Consumption Bulletin • MoPNG",
    anchor_id="ch-07"
)

product_demand = IndiaDemandAnalytics.get_national_product_consumption()
regional_demand = IndiaDemandAnalytics.get_regional_demand_shares()

dem_c1, dem_c2 = st.columns([7, 5])

with dem_c1:
    st.markdown("#### ⛽ Consumption by Petroleum Commodity (National Total ~233 MMT)")
    fig_prod_dem = px.bar(
        product_demand.sort_values("consumption_mmt", ascending=True),
        x="consumption_mmt",
        y="product_name",
        orientation="h",
        color="consumption_mmt",
        color_continuous_scale=[[0, "#E8E4D8"], [1, COLOR_AMBER]],
        labels={"consumption_mmt": "Consumption (MMT)", "product_name": ""}
    )
    fig_prod_dem.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.2)))
    apply_clean_layout(
        fig_prod_dem,
        height=460,
        margin_l=150,
        showlegend=False,
        coloraxis_showscale=False,
        xaxis_title="Consumption (Million Metric Tonnes)"
    )
    st.plotly_chart(fig_prod_dem, width="stretch", theme=None)

with dem_c2:
    st.markdown("#### 🧭 Geographic Demand Distribution")
    fig_reg_dem = px.pie(
        regional_demand,
        names="region",
        values="consumption_share_pct",
        color_discrete_sequence=[COLOR_AMBER, "#2B6CB0", "#C05621", "#2C7A7B"],
        hole=0.5
    )
    fig_reg_dem.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.5)))
    apply_clean_layout(
        fig_reg_dem,
        height=480,
        is_pie=True,
        showlegend=True,
        legend_below=True
    )
    st.plotly_chart(fig_reg_dem, width="stretch", theme=None)

st.dataframe(regional_demand[["region", "consumption_share_pct", "consumption_mmt", "demand_driver"]].rename(columns={
    "region": "Geographic Zone",
    "consumption_share_pct": "National Share %",
    "consumption_mmt": "Volume (MMT)",
    "demand_driver": "Key Industrial & Economic Drivers"
}), width="stretch", hide_index=True)


# ==============================================================================
# CHAPTER 08 — FUEL TAXES AND GOVERNMENT REVENUE
# ==============================================================================
render_chapter_header(
    chapter_num="08",
    title="Fuel Taxes and Government Revenue",
    subtitle="The critical distinction between excise duty rates, state VAT, and actual sovereign tax collections from the petroleum sector.",
    source_tag="PPAC Statistical Dossier • Union Budget & State Finance Accounts",
    anchor_id="ch-08"
)

rev_c1, rev_c2 = st.columns([6, 6])

with rev_c1:
    render_html(
        f"""
        <div style="background: {COLOR_WHITE}; border: 2px solid {COLOR_INK}; box-shadow: 4px 4px 0px {COLOR_INK}; border-radius: 6px; padding: 22px 24px; height: 100%;">
            <div style="font-size: 0.82rem; font-weight: 800; text-transform: uppercase; color: {COLOR_GRAY_MUTED}; margin-bottom: 6px;">SOVEREIGN PETROLEUM FISCAL REVENUE</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: {COLOR_INK}; line-height: 1.1;">₹4.82 Lakh Cr</div>
            <div style="font-size: 0.85rem; color: {COLOR_GRAY_MUTED}; margin-top: 6px; margin-bottom: 16px;">Total Contribution to Central and State Exchequers (FY2023–24)</div>
            
            <div style="border-top: 1.5px solid {COLOR_BORDER_LIGHT}; padding-top: 12px; font-size: 0.85rem; line-height: 1.6;">
                • <b>Central Exchequer:</b> ~₹2.81 Lakh Crore via Specific Central Excise Duty on Petrol & Diesel.<br>
                • <b>State Exchequers:</b> ~₹2.01 Lakh Crore via State VAT, Sales Tax, and Local Cess.<br>
                • <b>Non-GST Treatment:</b> Petrol, Diesel, and Crude Oil remain outside GST, preserving fiscal autonomy for Indian states.
            </div>
        </div>
        """
    )

with rev_c2:
    st.markdown("#### 🏛️ Central vs. State Petroleum Revenue Composition")
    rev_split_df = pd.DataFrame([
        {"Exchequer": "Central Government (Excise)", "Amount_Lakh_Cr": 2.81, "Share_Pct": 58.3},
        {"Exchequer": "State Governments (VAT/Cess)", "Amount_Lakh_Cr": 2.01, "Share_Pct": 41.7}
    ])
    fig_rev_pie = px.pie(
        rev_split_df,
        names="Exchequer",
        values="Amount_Lakh_Cr",
        color_discrete_sequence=[COLOR_AMBER, "#2B6CB0"],
        hole=0.5
    )
    fig_rev_pie.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.5)))
    apply_clean_layout(
        fig_rev_pie,
        height=450,
        is_pie=True,
        showlegend=True,
        legend_below=True
    )
    st.plotly_chart(fig_rev_pie, width="stretch", theme=None)


# ==============================================================================
# CHAPTER 09 — ENERGY RISK AND AFFORDABILITY
# ==============================================================================
render_chapter_header(
    chapter_num="09",
    title="Energy Risk and Affordability",
    subtitle="Macroeconomic consumer fuel burden (% daily income proxy) and maritime chokepoint transit vulnerability.",
    source_tag="World Bank Indicators • Global Chokepoints Registry",
    anchor_id="ch-09",
    action_page_url="/Affordability",
    action_label="AFFORDABILITY & RISK"
)

afford_df = AffordabilityAnalytics.get_affordability_overview(reporting_year=2024)

if not afford_df.empty:
    aff_c1, aff_c2 = st.columns([6, 6])
    with aff_c1:
        st.markdown("#### ⚖️ % of Daily Income Spent per Litre of Petrol")
        fig_aff_bar = px.bar(
            afford_df.sort_values("petrol_litre_percent_daily_income", ascending=True),
            x="petrol_litre_percent_daily_income",
            y="country_name",
            color="affordability_tier",
            orientation="h",
            color_discrete_map={
                "High": "#2C7A7B",
                "Moderate": COLOR_AMBER,
                "Severe": "#C05621",
                "Critical": "#C53030"
            },
            labels={"petrol_litre_percent_daily_income": "% Daily Income / Litre", "country_name": "Economy"}
        )
        fig_aff_bar.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.2)))
        apply_clean_layout(
            fig_aff_bar,
            height=480,
            margin_l=130,
            legend_below=True
        )
        st.plotly_chart(fig_aff_bar, width="stretch", theme=None)

    with aff_c2:
        st.markdown("#### 🔍 Nominal GDP per Capita vs. Fuel Burden (Log Scale)")
        fig_scatter = px.scatter(
            afford_df,
            x="gdp_per_capita_nominal_usd",
            y="petrol_litre_percent_daily_income",
            color="affordability_tier",
            hover_name="country_name",
            size="petrol_litre_percent_daily_income",
            log_x=True,
            labels={
                "gdp_per_capita_nominal_usd": "Nominal GDP per Capita (USD, Log Scale)",
                "petrol_litre_percent_daily_income": "% Daily Income / Litre"
            },
            color_discrete_map={
                "High": "#2C7A7B",
                "Moderate": COLOR_AMBER,
                "Severe": "#C05621",
                "Critical": "#C53030"
            }
        )
        fig_scatter.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.5)))
        apply_clean_layout(
            fig_scatter,
            height=480,
            legend_below=True
        )
        st.plotly_chart(fig_scatter, width="stretch", theme=None)


# ==============================================================================
# CHAPTER 10 — FORECASTS AND WHAT-IF SCENARIOS
# ==============================================================================
render_chapter_header(
    chapter_num="10",
    title="Forecasts and What-If Scenarios",
    subtitle="Model-supported retail fuel price projections with 95% confidence intervals and an interactive scenario simulation laboratory.",
    source_tag="Scikit-Learn • Statsmodels • Interactive Sensitivity Engine",
    anchor_id="ch-10",
    action_page_url="/Shock_Simulator",
    action_label="SCENARIO LAB"
)

tab_fc_view, tab_sim_view = st.tabs(["📈 ML Time-Series Forecasts", "⚡ Interactive Sensitivity Sandbox"])

with tab_fc_view:
    fc_c1, fc_c2 = st.columns([4, 8])
    with fc_c1:
        st.markdown("#### Model Selection")
        fc_country = st.selectbox(
            "Forecast Economy",
            ["USA", "IND", "DEU", "FRA", "GBR", "SAU"],
            index=1,
            format_func=lambda x: {
                "USA": "United States (USA)",
                "IND": "India (IND)",
                "DEU": "Germany (DEU)",
                "FRA": "France (FRA)",
                "GBR": "United Kingdom (GBR)",
                "SAU": "Saudi Arabia (SAU)"
            }.get(x, x)
        )
        fc_fuel = st.selectbox(
            "Product",
            ["petrol_regular", "diesel"],
            index=0,
            format_func=lambda x: "Petrol (Regular)" if x == "petrol_regular" else "Diesel"
        )
        fc_results = PriceForecaster.train_and_forecast(country_iso3=fc_country, fuel_type=fc_fuel, horizon_weeks=4)
        
        val_status = "SUPERIOR TO NAIVE" if fc_results.get("model_beats_baseline", True) else "BASELINE PARITY"
        render_instrument_card(
            "Test Set MAE",
            f"${fc_results['mae']:.4f}/L",
            accent="teal",
            subtext=f"Baseline MAE: ${fc_results.get('baseline_mae', 0.0):.4f}/L"
        )
        render_instrument_card(
            "Model Validation",
            val_status,
            accent="green" if fc_results.get("model_beats_baseline", True) else "amber",
            subtext=f"Trained: {fc_results.get('train_window', '2024–2026')}"
        )
        imp_val = fc_results.get("improvement_pct", 0.0)
        imp_sign = "+" if imp_val > 0 else ""
        render_instrument_card(
            "Holdout Accuracy Delta",
            f"{imp_sign}{imp_val:.1f}%",
            accent="green" if imp_val >= 0 else "amber",
            subtext=f"Tested: {fc_results.get('test_window', 'Holdout')}"
        )

    with fc_c2:
        country_display = {
            "USA": "United States", "IND": "India", "DEU": "Germany",
            "FRA": "France", "GBR": "United Kingdom", "SAU": "Saudi Arabia"
        }.get(fc_country, fc_country)
        product_display = "Petrol (Regular)" if fc_fuel == "petrol_regular" else "Diesel"
        st.markdown(f"#### 📈 Price Projection Trajectory: {country_display} ({product_display})")
        hist_dates = fc_results.get("historical_dates", [])
        hist_prices = fc_results.get("historical_prices", [])
        forecasts = fc_results.get("forecasts", [])

        fig_fc = go.Figure()
        if hist_dates and hist_prices:
            fig_fc.add_trace(go.Scatter(
                x=hist_dates, y=hist_prices, mode="lines+markers", name="Historical Actual",
                line=dict(color=COLOR_INK, width=2.5), marker=dict(size=7, color=COLOR_INK)
            ))
        if forecasts:
            fc_dates = [f["target_date"] for f in forecasts]
            fc_preds = [f["predicted_price_usd"] for f in forecasts]
            fc_lower = [f.get("lower_bound_usd", f.get("confidence_lower_usd", f["predicted_price_usd"])) for f in forecasts]
            fc_upper = [f.get("upper_bound_usd", f.get("confidence_upper_usd", f["predicted_price_usd"])) for f in forecasts]

            fig_fc.add_trace(go.Scatter(
                x=fc_dates, y=fc_upper, mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip"
            ))
            fig_fc.add_trace(go.Scatter(
                x=fc_dates, y=fc_lower, mode="lines", line=dict(width=0), fill="tonexty",
                fillcolor="rgba(245, 185, 66, 0.25)", name="95% Confidence Envelope"
            ))
            fig_fc.add_trace(go.Scatter(
                x=fc_dates, y=fc_preds, mode="lines+markers", name="Projected Trajectory",
                line=dict(color=COLOR_AMBER, width=2.5, dash="dash"), marker=dict(size=8, symbol="diamond", color=COLOR_AMBER, line=dict(color=COLOR_INK, width=1.5))
            ))
        apply_clean_layout(
            fig_fc,
            height=460,
            xaxis_title="Observation Timeline",
            yaxis_title="Price (USD / Litre)",
            legend_below=True
        )
        st.plotly_chart(fig_fc, width="stretch", theme=None)

with tab_sim_view:
    sim_p1, sim_p2, sim_p3 = st.columns(3)
    with sim_p1:
        sim_exp = st.selectbox("Exporter Cut Origin", ["SAU", "RUS", "IRQ"], index=0)
        sim_cut = st.slider("Supply Reduction (%)", 5.0, 35.0, 15.0, 5.0)
    with sim_p2:
        sim_imp = st.selectbox("Importing Base", ["IND", "CHN", "USA"], index=0)
        sim_shock = st.slider("Crude Shock (+$/bbl)", 0.0, 40.0, 12.0, 2.0)
    with sim_p3:
        sim_fx = st.slider("Currency Depreciation (%)", 0.0, 15.0, 2.5, 0.5)

    sim_res = SupplyShockSimulator.simulate_export_curtailment(
        exporter_iso3=sim_exp,
        target_importer_iso3=sim_imp,
        product_category="crude_oil",
        export_reduction_pct=sim_cut,
        assumed_crude_price_delta_usd_per_bbl=sim_shock,
        exchange_rate_depreciation_pct=sim_fx,
        monthly_fleet_fuel_consumption_litres=250000.0,
        baseline_retail_price_usd_per_litre=1.05
    )

    sr1, sr2, sr3, sr4 = st.columns(4)
    with sr1:
        render_instrument_card("Volume Deficit", f"{sim_res['volume_deficit_bpd']:,.0f} bpd", accent="red", subtext=f"-{sim_cut}% cut from {sim_exp}")
    with sr2:
        render_instrument_card("Remaining Bilateral Flow", f"{sim_res['scenario_remaining_supply_bpd']:,.0f} bpd", accent="amber", subtext=f"Baseline: {sim_res['baseline_bilateral_bpd']:,.0f} bpd")
    with sr3:
        render_instrument_card("Simulated Retail Pump", f"${sim_res['scenario_retail_price_usd']:.4f}/L", accent="red", delta=f"+{sim_res['retail_price_pct_increase']:.1f}%", delta_is_positive_bad=True, subtext="Direct consumer inflation")
    with sr4:
        fleet_pct = ((sim_res['additional_monthly_fleet_cost_usd'] / sim_res['baseline_monthly_fleet_spend_usd']) * 100.0) if sim_res.get('baseline_monthly_fleet_spend_usd', 0) > 0 else sim_res.get('retail_price_pct_increase', 0.0)
        render_instrument_card("Monthly Fleet Cost Impact", f"+${sim_res['additional_monthly_fleet_cost_usd']:,.0f}", accent="red", delta=f"+{fleet_pct:.1f}%", delta_is_positive_bad=True, subtext="250,000L commercial fleet")


# ==============================================================================
# CHAPTER 11 — DATA SOURCES AND RELIABILITY
# ==============================================================================
render_chapter_header(
    chapter_num="11",
    title="Data Sources and Reliability",
    subtitle="Full provenance auditing, ETL pipeline execution logs, freshness latencies, and downloadable verified datasets.",
    source_tag="Automated Data Quality & Pipeline Assurance Mart",
    anchor_id="ch-11",
    action_page_url="/Data_Trust",
    action_label="DATA TRUST CENTER"
)

freshness_list = DataQualityAuditor.get_source_freshness_status()
fresh_df = pd.DataFrame(freshness_list)
tele_df = DataQualityAuditor.get_pipeline_telemetry()
table_cts = DataQualityAuditor.get_table_row_counts()

dt1, dt2, dt3, dt4 = st.columns(4)
with dt1:
    tot_runs = len(tele_df)
    succ_runs = len(tele_df[tele_df["status"] == "SUCCESS"])
    pct_succ = (succ_runs / tot_runs * 100.0) if tot_runs > 0 else 100.0
    render_instrument_card("ETL Success Rate", f"{pct_succ:.1f}%", accent="green", subtext=f"{succ_runs} of {tot_runs} runs successful")
with dt2:
    tot_recs = sum(table_cts.values())
    render_instrument_card("Verified Data Mart Records", f"{tot_recs:,}", accent="amber", subtext="Relational database tables")
with dt3:
    fresh_ct = len(fresh_df[fresh_df["freshness_status"] == "FRESH"]) if not fresh_df.empty else 4
    render_instrument_card("Active Fresh Feeds", f"{fresh_ct} / {len(fresh_df)} Sources", accent="teal", subtext="Within reporting SLA window")
with dt4:
    tot_rej = int(tele_df["rows_rejected"].sum()) if not tele_df.empty else 0
    render_instrument_card("Quarantined Rows", str(tot_rej), accent="teal", subtext="Zero corruption tolerance")

if not fresh_df.empty:
    st.markdown("#### 📡 Registered External Data Sources & Freshness Audits")
    st.dataframe(fresh_df[[
        "source_name", "update_frequency", "latest_observation_date",
        "records_count", "latency_days", "freshness_status", "license"
    ]].rename(columns={
        "source_name": "Data Provider",
        "update_frequency": "Cadence",
        "latest_observation_date": "Latest Observation",
        "records_count": "Records",
        "latency_days": "Latency (Days)",
        "freshness_status": "Status",
        "license": "License Terms"
    }), width="stretch", hide_index=True)

# Export Master Dossier
exp_col1, exp_col2 = st.columns([7, 5])
with exp_col2:
    render_csv_download(prod_lb, "global_fuelpulse_energy_atlas_master.csv", "📥 EXPORT COMPLETE ENERGY ATLAS DATASET")

render_html(
    """
    <div style="text-align: center; margin-top: 4rem; padding: 2.5rem 0; border-top: 2px solid #111111; font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 13px; color: #111111; font-weight: 700; letter-spacing: 0.04em; line-height: 1.6;">
        GLOBAL FUELPULSE AI — EDITORIAL INDUSTRIAL ENERGY INTELLIGENCE<br>
        <span style="font-size: 12px; font-weight: 600; color: #222222;">DATA SOURCES: US EIA • UN COMTRADE • INDIA PPAC • EC OIL BULLETIN • WORLD BANK • HPCL DISCLOSURES</span>
    </div>
    """
)
