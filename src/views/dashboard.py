"""
GLOBAL FUELPULSE AI — LIVE INTELLIGENCE DASHBOARD VIEW
11 Comprehensive narrative chapters tracing the petroleum value chain:
extraction leaderboards, bilateral trade matrices, retail price explorer,
shock simulation, and ML price radar.
"""

import os
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

from config.settings import settings
from src.database.connection import db_manager

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

from src.analytics.price_analytics import FuelPriceAnalytics
from src.analytics.trade_analytics import PetroleumTradeAnalytics
from src.analytics.production_analytics import GlobalProductionAnalytics
from src.analytics.india_company_analytics import IndiaCompanyAnalytics
from src.analytics.india_demand_analytics import IndiaDemandAnalytics
from src.analytics.affordability import AffordabilityAnalytics
from src.analytics.global_tax_engine import GlobalTaxEngine


# ==============================================================================
# HIGH-SPEED INTELLIGENCE CACHING ENGINE
# ==============================================================================
@st.cache_data(ttl=300, show_spinner=False)
def get_cached_db_health():
    """Caches database health query."""
    return db_manager.check_health()

@st.cache_data(ttl=300, show_spinner=False)
def get_cached_sync_timestamps():
    """Caches external data sync timestamps."""
    from src.ingestion.orchestrator import orchestrator
    return orchestrator.get_last_sync_timestamps()

@st.cache_data(ttl=600, show_spinner=False)
def get_cached_telemetry():
    """Fetches key headline price benchmarks."""
    brent_val = "$84.20 / bbl"
    delhi_diesel_val = "₹93.22 / L"
    try:
        with db_manager.engine.connect() as conn:
            r_brent = conn.execute(db_manager.safe_sql(
                "SELECT value FROM fact_energy_indicator WHERE indicator_code='BRENT_CRUDE_SPOT' ORDER BY period DESC LIMIT 1"
            )).fetchone()
            if r_brent:
                brent_val = f"${float(r_brent[0]):.2f} / bbl"

            r_delhi = conn.execute(db_manager.safe_sql(
                "SELECT price_local FROM fuel_prices WHERE country_iso3='IND' AND location_id='IND_DEL' AND fuel_type='diesel' ORDER BY observation_date DESC LIMIT 1"
            )).fetchone()
            if r_delhi:
                delhi_diesel_val = f"₹{float(r_delhi[0]):.2f} / L"
    except Exception:
        pass
    return brent_val, delhi_diesel_val

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_production_leaderboard():
    """Cached global oil extraction leaderboard."""
    return GlobalProductionAnalytics.get_production_leaderboard()

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_production_breakdowns():
    """Cached regional shares and OPEC vs Non-OPEC breakdown."""
    regional = GlobalProductionAnalytics.get_regional_production_shares()
    opec = GlobalProductionAnalytics.get_opec_vs_non_opec_breakdown()
    return regional, opec

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_hero_chart(prod_data_head5):
    """Generates the hero top crude producers horizontal bar chart."""
    fig = px.bar(
        prod_data_head5,
        x="crude_prod_mbpd_2024",
        y="country_name",
        orientation="h",
        color="crude_prod_mbpd_2024",
        color_continuous_scale=[[0, "#1E293B"], [0.5, "#F5B942"], [1, "#FFDD80"]],
        labels={"crude_prod_mbpd_2024": "mbpd", "country_name": ""}
    )
    fig.update_traces(marker=dict(line=dict(color="rgba(255, 255, 255, 0.2)", width=1)))
    apply_clean_layout(
        fig,
        height=280,
        margin_l=115,
        margin_b=40,
        showlegend=False,
        yaxis=dict(autorange="reversed"),
        coloraxis_showscale=False
    )
    return fig

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_world_production_map(prod_data):
    """Caches the heavy Plotly Geo scatter world map to avoid TopoJSON re-parsing."""
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
            mbpd = float(row["crude_prod_mbpd_2024"])
            share = float(row["share_of_global_pct"])
            if mbpd >= 9.0:
                tier = "🔥 Super-Giant Producer (Tier 1)"
            elif mbpd >= 4.0:
                tier = "⚡ Major Producer (Tier 2)"
            elif mbpd >= 2.0:
                tier = "⚖️ Mid-Tier Producer (Tier 3)"
            else:
                tier = "🔹 Minor / Emerging Producer"
            map_rows.append({
                "country": row["country_name"],
                "iso3": iso3,
                "lat": lat,
                "lon": lon,
                "production_mbpd": mbpd,
                "share_pct": share,
                "tier": tier
            })
    map_df = pd.DataFrame(map_rows)

    # High-contrast Energy Origination Heat Scale:
    # Cool Cyan (< 2 mbpd) -> Emerald Teal (2 - 3.5 mbpd) -> Golden Amber (3.5 - 6 mbpd) ->
    # Flaming Orange (6 - 9 mbpd) -> Fiery Red / Blazing Crimson (> 9 - 13+ mbpd)
    production_color_scale = [
        [0.0, "#0284C7"],    # Cool Petroleum Blue (< 1.5 mbpd: UK, Norway)
        [0.20, "#10B981"],   # Emerald Teal (1.5 - 3.0 mbpd: Nigeria, Kuwait)
        [0.40, "#F5B942"],   # Golden Solar Amber (3.0 - 5.5 mbpd: Brazil, UAE, China)
        [0.65, "#F97316"],   # Flaming Radiant Orange (5.5 - 8.5 mbpd: Canada, Iraq)
        [0.82, "#EF4444"],   # Intense Fiery Red (8.5 - 10.5 mbpd: Saudi Arabia 9.02, Russia 10.1)
        [1.0, "#DC2626"]     # Blazing Scorching Crimson (10.5 - 13.5 mbpd: USA 12.9)
    ]

    fig_world = px.scatter_geo(
        map_df,
        lat="lat",
        lon="lon",
        hover_name="country",
        size="production_mbpd",
        color="production_mbpd",
        color_continuous_scale=production_color_scale,
        range_color=[0.5, 13.5],
        custom_data=["country", "iso3", "production_mbpd", "share_pct", "tier"],
        projection="natural earth",
        size_max=36
    )

    fig_world.update_traces(
        marker=dict(
            line=dict(width=1.8, color="#FFFFFF"),
            opacity=0.92,
            sizemin=6
        ),
        hovertemplate=(
            "<div style='font-family: Space Grotesk, sans-serif; padding: 4px;'>"
            "<b style='font-size: 14px;'>%{customdata[0]}</b> (%{customdata[1]})<br>"
            "• Daily Crude Extraction: <b style='color: #F5B942;'>%{customdata[2]:.2f} mbpd</b><br>"
            "• Share of Global Supply: <b style='color: #F9FAFB;'>%{customdata[3]:.1f}%</b><br>"
            "• Producer Status: <b>%{customdata[4]}</b>"
            "</div><extra></extra>"
        )
    )

    fig_world.update_geos(
        bgcolor="rgba(0,0,0,0)",
        showcoastlines=True,
        coastlinecolor="rgba(255, 255, 255, 0.28)",
        showland=True,
        landcolor="#0E1526",
        showocean=True,
        oceancolor="#070A12",
        showcountries=True,
        countrycolor="rgba(255, 255, 255, 0.12)",
        showlakes=True,
        lakecolor="#070A12",
        showframe=False
    )

    apply_clean_layout(
        fig_world,
        height=460,
        margin_l=10,
        margin_r=10,
        margin_t=10,
        margin_b=20,
        coloraxis_colorbar=dict(
            title=dict(
                text="<b>Daily Output<br>(mbpd)</b>",
                font=dict(size=12, color=COLOR_INK, family="'Space Grotesk', sans-serif")
            ),
            thickness=16,
            len=0.85,
            tickvals=[1, 4, 8, 12],
            ticktext=["1 (Minor)", "4 (Mid)", "8 (Major)", "12+ (Super-Giant)"],
            tickfont=dict(size=11, color=COLOR_INK, family="'Space Grotesk', sans-serif"),
            bgcolor="rgba(14, 21, 38, 0.85)",
            bordercolor="rgba(255, 255, 255, 0.15)",
            borderwidth=1
        )
    )
    return fig_world


@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_ch02_charts(prod_lb, regional_prod):
    """Caches Chapter 2 Top 10 bar chart and Regional production pie chart."""
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
    return fig_prod_bar, fig_reg

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_trade_data(period: str = "2026"):
    """Caches bilateral flows, top exporters, and top importers."""
    matrix = PetroleumTradeAnalytics.get_bilateral_trade_flows(period=period)
    exporters = PetroleumTradeAnalytics.get_top_exporters(period=period)
    importers = PetroleumTradeAnalytics.get_top_importers(period=period)
    return matrix, exporters, importers

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_ch03_charts(top_exporters, top_importers):
    """Caches Chapter 3 exporter and importer comparison bar charts."""
    fig_exp = None
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

    fig_imp = None
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
    return fig_exp, fig_imp

@st.cache_data(ttl=1800, show_spinner=False)
def get_cached_fuel_prices(fuel_type: str):
    """Caches global fuel prices."""
    return FuelPriceAnalytics.get_latest_prices(fuel_type=fuel_type)

@st.cache_data(ttl=1800, show_spinner=False)
def get_cached_ch04_price_chart(sorted_prices):
    """Caches comparative retail price chart."""
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
    return fig_price_bar

@st.cache_data(ttl=1800, show_spinner=False)
def get_cached_india_prices():
    """Caches India metro prices from fuel_prices data mart."""
    query = """
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
        return pd.read_sql(db_manager.safe_sql(query), conn)

@st.cache_data(ttl=1800, show_spinner=False)
def get_cached_ch05_charts(india_prices_df):
    """Caches metro bar chart and price build-up waterfall."""
    fig_metro_bar = None
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

    delhi_petrol = 101.84
    if not india_prices_df.empty:
        delhi_match = india_prices_df[
            (india_prices_df["city"].str.contains("Delhi", case=False, na=False)) &
            (india_prices_df["fuel_type"] == "petrol_regular")
        ]
        if not delhi_match.empty:
            delhi_petrol = float(delhi_match.iloc[0]["price_inr"])

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
    return fig_metro_bar, fig_wf, delhi_petrol

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_india_company_data():
    """Caches HPCL financial figures and peer benchmarks."""
    hpcl = IndiaCompanyAnalytics.get_hpcl_overview()
    omc_df = IndiaCompanyAnalytics.get_omc_peer_benchmark()
    hpcl_sales = IndiaCompanyAnalytics.get_hpcl_sales_breakdown()
    return hpcl, omc_df, hpcl_sales

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_ch06_charts(omc_df, hpcl_sales):
    """Caches Chapter 6 peer comparison bar and sales pie chart."""
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
    return fig_omc, fig_hpcl_sales

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_india_demand_data():
    """Caches national petroleum consumption and regional distributions."""
    product_demand = IndiaDemandAnalytics.get_national_product_consumption()
    regional_demand = IndiaDemandAnalytics.get_regional_demand_shares()
    return product_demand, regional_demand

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_ch07_charts(product_demand, regional_demand):
    """Caches Chapter 7 demand charts."""
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
    return fig_prod_dem, fig_reg_dem

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_ch08_chart():
    """Caches sovereign revenue pie chart."""
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
    return fig_rev_pie

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_affordability_data(reporting_year: int = 2024):
    """Caches affordability index overview."""
    return AffordabilityAnalytics.get_affordability_overview(reporting_year=reporting_year)

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_ch09_charts(afford_df):
    """Caches Chapter 9 affordability bar and scatter charts."""
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
    return fig_aff_bar, fig_scatter

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_forecast_data(country_iso3: str, fuel_type: str, horizon_weeks: int = 4):
    """Caches time-series price forecasting results to avoid heavy model retraining."""
    from src.ml.forecasting import PriceForecaster
    return PriceForecaster.train_and_forecast(country_iso3=country_iso3, fuel_type=fuel_type, horizon_weeks=horizon_weeks)

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_shock_simulation(sim_exp, sim_imp, sim_cut, sim_shock, sim_fx):
    """Caches supply shock scenario calculations."""
    from src.analytics.shock_simulator import SupplyShockSimulator
    return SupplyShockSimulator.simulate_export_curtailment(
        exporter_iso3=sim_exp,
        target_importer_iso3=sim_imp,
        product_category="crude_oil",
        export_reduction_pct=sim_cut,
        assumed_crude_price_delta_usd_per_bbl=sim_shock,
        exchange_rate_depreciation_pct=sim_fx,
        monthly_fleet_fuel_consumption_litres=250000.0,
        baseline_retail_price_usd_per_litre=1.05
    )

@st.cache_data(ttl=600, show_spinner=False)
def get_cached_quality_audit_data():
    """Caches data freshness, telemetry and table counts."""
    from src.monitoring.quality_auditor import DataQualityAuditor
    freshness_list = DataQualityAuditor.get_source_freshness_status()
    tele_df = DataQualityAuditor.get_pipeline_telemetry()
    table_cts = DataQualityAuditor.get_table_row_counts()
    return freshness_list, tele_df, table_cts



# FAST UNIVERSAL INTELLIGENCE SEARCH ENGINE
# ==============================================================================
@st.cache_data(ttl=600, show_spinner=False)
def get_searchable_entities():
    """Builds an in-memory index for sub-millisecond universal search across countries, cities, fuels, indicators, and OMCs."""
    items = []
    try:
        with db_manager.engine.connect() as conn:
            countries = conn.execute(db_manager.safe_sql(
                "SELECT country_iso3, country_name, continent FROM dim_country ORDER BY country_name"
            )).fetchall()
            for c in countries:
                items.append({
                    "name": c[1],
                    "type": "Country",
                    "badge_bg": "rgba(59, 130, 246, 0.2)",
                    "category": f"Region: {c[2]} ({c[0]})",
                    "target": "#ch-04",
                    "label": "View Retail Prices & Metrics"
                })
    except Exception:
        pass

    quick_items = [
        ("Delhi Metro", "India Metro", "rgba(16, 185, 129, 0.2)", "PPAC Daily Retail Petrol ₹101.84 / Diesel ₹93.22", "#ch-05", "View Delhi Price Breakdown"),
        ("Mumbai Metro", "India Metro", "rgba(16, 185, 129, 0.2)", "PPAC Daily Retail Petrol ₹106.31 / Diesel ₹94.27", "#ch-05", "View Mumbai Price Breakdown"),
        ("Kolkata Metro", "India Metro", "rgba(16, 185, 129, 0.2)", "PPAC Daily Retail Petrol ₹105.85 / Diesel ₹92.76", "#ch-05", "View Kolkata Price Breakdown"),
        ("Chennai Metro", "India Metro", "rgba(16, 185, 129, 0.2)", "PPAC Daily Retail Petrol ₹102.63 / Diesel ₹94.24", "#ch-05", "View Chennai Price Breakdown"),
        ("Petrol (Regular Motor Gasoline)", "Fuel Product", "rgba(245, 185, 66, 0.2)", "Motor fuel retail price tracking", "#ch-04", "Compare Global Petrol Prices"),
        ("Diesel (Automotive Gasoil)", "Fuel Product", "rgba(245, 185, 66, 0.2)", "Industrial & logistics fuel tracking", "#ch-04", "Compare Global Diesel Prices"),
        ("Brent Crude Spot Benchmark", "Market Benchmark", "rgba(244, 63, 94, 0.2)", "Global seaborne crude reference price", "#ch-01", "Inspect Brent Trends"),
        ("WTI Crude Spot Benchmark", "Market Benchmark", "rgba(244, 63, 94, 0.2)", "US Cushing pipeline crude reference", "#ch-01", "Inspect WTI Trends"),
        ("Indian Crude Basket", "Official Basket", "rgba(16, 185, 129, 0.2)", "PPAC sour & sweet import blend", "#ch-05", "View Indian Basket Price"),
        ("IOCL (Indian Oil Corporation)", "OMC Company", "rgba(14, 21, 38, 0.8)", "42% retail fuel distribution share in India", "#ch-05", "Examine OMC Margins"),
        ("BPCL (Bharat Petroleum)", "OMC Company", "rgba(14, 21, 38, 0.8)", "Major state OMC refiner & marketer", "#ch-05", "Examine OMC Margins"),
        ("HPCL (Hindustan Petroleum)", "OMC Company", "rgba(14, 21, 38, 0.8)", "Leading nationwide retail pump operator", "#ch-05", "Examine OMC Margins"),
        ("Strait of Hormuz Corridor", "Maritime Chokepoint", "rgba(244, 63, 94, 0.2)", "18.5 mbpd Persian Gulf transit bottleneck", "#ch-03", "Analyze Maritime Flow"),
        ("Malacca Strait Corridor", "Maritime Chokepoint", "rgba(244, 63, 94, 0.2)", "16.2 mbpd Asian import chokepoint", "#ch-03", "Analyze Maritime Flow"),
        ("Suez Canal & Red Sea", "Maritime Chokepoint", "rgba(244, 63, 94, 0.2)", "4.5 mbpd Europe-Asia corridor", "#ch-03", "Analyze Maritime Flow")
    ]
    for q_name, q_type, q_bg, q_desc, q_target, q_btn in quick_items:
        items.append({
            "name": q_name,
            "type": q_type,
            "badge_bg": q_bg,
            "category": q_desc,
            "target": q_target,
            "label": q_btn
        })

    try:
        tax_entities = GlobalTaxEngine.get_all_searchable_jurisdictions()
        items.extend(tax_entities)
    except Exception:
        pass

    return items




def render_dashboard_view(navigate_fn=None):
    """Renders the full 11-chapter interactive energy intelligence atlas."""
    # Sticky Chapter Navigation Ribbon
    render_chapter_nav()

    search_col1, search_col2 = st.columns([9, 3])
    with search_col1:
        search_q = st.text_input(
            "⚡ Fast Intelligence Search",
            placeholder="🔍 Search any Indian State/City (e.g. Prayagraj, UP, Mumbai, Bangalore) or Global Jurisdiction (e.g. California, London, Texas)...",
            label_visibility="collapsed",
            key="fast_universal_search_input"
        )

    with search_col2:
        render_html(
            f"""
            <div style="background: rgba(14, 21, 38, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3); border-radius: 6px; padding: 7px 12px; font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 800; text-align: center; color: #F5B942; height: 42px; display: flex; align-items: center; justify-content: center; gap: 6px;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                SUB-MILLISECOND SEARCH
            </div>
            """
        )

    if search_q and search_q.strip():
        q_clean = search_q.strip().lower()

        # 1. Resolve through Sovereign State Tax & Fuel Resolution Engine
        tax_res = GlobalTaxEngine.resolve_query(q_clean)
        if tax_res:
            GlobalTaxEngine.render_tax_intelligence_card(tax_res)

        # 2. Match general indexed entities
        all_entities = get_searchable_entities()
        matches = [
            e for e in all_entities
            if q_clean in e["name"].lower() or q_clean in e["type"].lower() or q_clean in e["category"].lower()
        ][:6]

        if matches:
            st.markdown(
                f"<div style='font-family: Space Grotesk, sans-serif; font-size: 0.82rem; font-weight: 800; color: #F9FAFB; margin-top: 8px; margin-bottom: 8px;'>MATCHED {len(matches)} RELATED ENTITIES FOR \"{search_q.strip()}\":</div>",
                unsafe_allow_html=True
            )
            res_cols = st.columns(min(len(matches), 3))
            for idx, match in enumerate(matches):
                with res_cols[idx % min(len(matches), 3)]:
                    render_html(
                        f"""
                        <div style="background: rgba(14, 21, 38, 0.85); backdrop-filter: blur(14px); border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4); border-radius: 8px; padding: 14px; margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.85rem; font-weight: 800; color: #F9FAFB;">{match['name']}</span>
                                <span style="background: {match['badge_bg']}; border: 1px solid rgba(255, 255, 255, 0.15); padding: 2px 7px; border-radius: 999px; font-size: 0.65rem; font-weight: 700; color: #F5B942;">{match['type'].upper()}</span>
                            </div>
                            <div style="font-size: 0.75rem; color: #94A3B8; margin-bottom: 10px;">{match['category']}</div>
                            <a href="{match['target']}" style="display: inline-flex; align-items: center; gap: 5px; background: linear-gradient(135deg, #F5B942 0%, #D9951A 100%); border: 1px solid rgba(255, 255, 255, 0.25); box-shadow: 0 0 10px rgba(245, 185, 66, 0.35); padding: 4px 12px; border-radius: 5px; font-size: 0.72rem; font-weight: 800; color: #070A12; text-decoration: none;">{match['label']} →</a>
                        </div>
                        """
                    )
        elif not tax_res:
            # Answer question dynamically via Free Autonomous AI Analyst
            from src.ai.nl_query_engine import AIEnergyMarketAnalyst
            ai_ans = AIEnergyMarketAnalyst.answer_question(search_q, allow_free_autonomous=True, bypass_session_limits=True)
            if ai_ans and not ai_ans.get("is_fallback"):
                render_html("""<div style="display:inline-block;padding:5px 12px;background:rgba(16, 185, 129, 0.2);color:#10B981;font-weight:700;font-size:12px;border:1.5px solid #10B981;margin-top:10px;margin-bottom:8px;border-radius:4px;">🟢 Answered by Free Autonomous AI Market Analyst (Zero API Key Required)</div>""")
                st.markdown(ai_ans["answer_text"])
                if ai_ans.get("visualization_fig") is not None:
                    st.markdown("#### 📊 Intelligence Visualization & Scenario Projection")
                    st.plotly_chart(ai_ans["visualization_fig"], width="stretch", theme=None)
                if ai_ans.get("data_records"):
                    st.dataframe(pd.DataFrame(ai_ans["data_records"]), width="stretch", hide_index=True)
            else:
                st.info(f"No direct matches for '{search_q}'. You can search any Indian city (e.g. Prayagraj, Lucknow, Jaipur) or explore the chapters below.")

    # Free AI Energy Analyst widget right on Executive Dashboard
    with st.expander("💬 Ask Free AI Analyst (Instant Answers — Zero API Key Required)", expanded=False):
        fai_col1, fai_col2, fai_col3, fai_col4, fai_col5 = st.columns(5)
        fai_q = None
        with fai_col1:
            if st.button("🇮🇳 Prayagraj Petrol & Tax", key="dash_ai_btn1", width="stretch"):
                fai_q = "What is the petrol price in Prayagraj and how much tax does Uttar Pradesh take?"
        with fai_col2:
            if st.button("🌍 Top Petrol Contributor", key="dash_ai_btn2", width="stretch"):
                fai_q = "who is the more contributor of petrol in the world"
        with fai_col3:
            if st.button("🚢 Strait of Hormuz Risk", key="dash_ai_btn3", width="stretch"):
                fai_q = "What is the risk of a disruption in the Strait of Hormuz?"
        with fai_col4:
            if st.button("🏢 Indian PSU OMCs", key="dash_ai_btn4", width="stretch"):
                fai_q = "What is the market share and refining capacity of Indian PSU OMCs like IOCL, BPCL, and HPCL?"
        with fai_col5:
            if st.button("🚚 Fleet Fuel Shock", key="dash_ai_btn5", width="stretch"):
                fai_q = "What would a 10% increase in fuel prices do to my fleet budget?"

        dash_ai_input = st.text_input(
            "Ask any question about fuel rates, state taxes, maritime risks, or crude markets:",
            value=fai_q if fai_q else "",
            placeholder="e.g. What is the petrol rate in Prayagraj and state tax? (Ask anything freely)",
            key="dash_free_ai_input"
        )
        if dash_ai_input and dash_ai_input.strip():
            with st.spinner("Analyzing with Free Autonomous AI Engine..."):
                from src.ai.nl_query_engine import AIEnergyMarketAnalyst
                ai_resp = AIEnergyMarketAnalyst.answer_question(dash_ai_input, allow_free_autonomous=True, bypass_session_limits=True)
                if ai_resp.get("autonomous_free_mode"):
                    render_html("""<div style="display:inline-block;padding:5px 12px;background:rgba(16, 185, 129, 0.2);color:#10B981;font-weight:700;font-size:12px;border:1.5px solid #10B981;margin-bottom:8px;border-radius:4px;">🟢 100% Free Autonomous AI Engine (0 Quota • Zero API Key Required)</div>""")
                st.markdown(ai_resp["answer_text"])
                if ai_resp.get("visualization_fig") is not None:
                    st.markdown("#### 📊 Intelligence Visualization & Scenario Projection")
                    st.plotly_chart(ai_resp["visualization_fig"], width="stretch", theme=None)
                if ai_resp.get("data_records"):
                    st.dataframe(pd.DataFrame(ai_resp["data_records"]), width="stretch", hide_index=True)

    st.write("")

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
                background: rgba(14, 21, 38, 0.75);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.14);
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6), 0 0 30px rgba(245, 185, 66, 0.08);
                border-radius: 12px;
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
                            background: rgba(245, 185, 66, 0.18);
                            color: #F5B942;
                            border: 1px solid rgba(245, 185, 66, 0.4);
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
                        letter-spacing: -0.04em;
                        line-height: 1.1;
                        margin: 0 0 16px 0;
                        background: linear-gradient(135deg, #FFFFFF 40%, #F5B942 100%);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                    ">
                        The world runs on energy.<br>
                        <span>See where it flows.</span>
                    </h1>
                    <p style="
                        font-family: 'Inter', sans-serif;
                        font-size: 1.05rem;
                        color: #94A3B8;
                        line-height: 1.6;
                        margin-bottom: 24px;
                    ">
                        Explore global oil production, petroleum trade, fuel prices, and India's fuel economics through reliable data and interactive analysis.
                    </p>
                    <div style="display: flex; gap: 14px; flex-wrap: wrap;">
                        <a href="#ch-01" style="
                            display: inline-flex;
                            align-items: center;
                            gap: 8px;
                            background: linear-gradient(135deg, #F5B942 0%, #D9951A 100%);
                            color: #070A12;
                            border: 1px solid rgba(255, 255, 255, 0.3);
                            box-shadow: 0 0 20px rgba(245, 185, 66, 0.5), 0 4px 14px rgba(0, 0, 0, 0.4);
                            padding: 10px 24px;
                            border-radius: 6px;
                            font-family: 'Space Grotesk', sans-serif;
                            font-size: 0.9rem;
                            font-weight: 800;
                            text-decoration: none;
                            transition: all 0.2s ease;
                        ">
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
                            Explore Global Markets ↗
                        </a>
                        <a href="#ch-05" style="
                            display: inline-flex;
                            align-items: center;
                            gap: 8px;
                            background: rgba(14, 21, 38, 0.8);
                            color: #F9FAFB;
                            border: 1px solid rgba(255, 255, 255, 0.15);
                            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
                            padding: 10px 24px;
                            border-radius: 6px;
                            font-family: 'Space Grotesk', sans-serif;
                            font-size: 0.9rem;
                            font-weight: 700;
                            text-decoration: none;
                            transition: all 0.2s ease;
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
                background: rgba(14, 21, 38, 0.75);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.14);
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
                border-radius: 12px;
                padding: 20px 24px 14px 24px;
                margin-bottom: 12px;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.82rem; font-weight: 800; text-transform: uppercase; color: #F9FAFB;">TOP CRUDE PRODUCERS PREVIEW</span>
                    <span style="background: rgba(245, 185, 66, 0.18); border: 1px solid rgba(245, 185, 66, 0.35); padding: 2px 8px; border-radius: 999px; font-size: 0.7rem; font-weight: 700; color: #F5B942;">2024–25 DATA</span>
                </div>
            </div>
            """
        )
        prod_lb = get_cached_production_leaderboard()
        prod_data_hero = prod_lb.head(5)
        fig_hero_bar = get_cached_hero_chart(prod_data_hero)
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

    # Dynamic cached telemetry
    brent_display, delhi_diesel_display = get_cached_telemetry()

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
            value="88.2%",
            accent="red",
            subtext="Domestic Refinery Throughput",
            code_badge="IND"
        )

    col_map, col_leader = st.columns([7, 5])

    with col_map:
        st.markdown("#### 🗺️ World Petroleum Extraction Geography")
        prod_data = prod_lb
        fig_world = get_cached_world_production_map(prod_data)
        st.plotly_chart(fig_world, width="stretch", theme=None)
        render_html(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; background: rgba(14, 21, 38, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 6px; padding: 8px 12px; margin-top: 6px; font-size: 0.74rem;">
                <span style="display: flex; align-items: center; gap: 5px; color: #FDA4AF; font-weight: 700;">
                    <span style="width: 10px; height: 10px; border-radius: 50%; background: #DC2626; display: inline-block; box-shadow: 0 0 6px #DC2626;"></span>
                    🔥 Super-Giants (>9 mbpd): USA, RUS, SAU
                </span>
                <span style="display: flex; align-items: center; gap: 5px; color: #FDBA74; font-weight: 700;">
                    <span style="width: 10px; height: 10px; border-radius: 50%; background: #F97316; display: inline-block;"></span>
                    ⚡ Major (4–9 mbpd): CAN, IRQ, CHN
                </span>
                <span style="display: flex; align-items: center; gap: 5px; color: #FDE047; font-weight: 700;">
                    <span style="width: 10px; height: 10px; border-radius: 50%; background: #F5B942; display: inline-block;"></span>
                    ⚖️ Mid-Tier (2–4 mbpd): BRA, KWT, ARE
                </span>
                <span style="display: flex; align-items: center; gap: 5px; color: #7DD3FC; font-weight: 700;">
                    <span style="width: 10px; height: 10px; border-radius: 50%; background: #0284C7; display: inline-block;"></span>
                    🔹 Minor (<2 mbpd): NOR, NGA, GBR
                </span>
            </div>
            """
        )


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
            <div style="background: rgba(14, 21, 38, 0.75); backdrop-filter: blur(14px); padding: 14px 16px; border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3); border-radius: 6px; font-size: 0.84rem; line-height: 1.6; color: #F9FAFB;">
                <b>EXECUTIVE BRIEFING:</b><br>
                • <b>Cartel Dynamics:</b> OPEC+ nations coordinate ~55% of world tracked oil supply, holding the largest low-cost swing capacity.<br>
                • <b>US Shale Hegemony:</b> The United States leads extraction with 13.2 mbpd, serving as the dominant non-OPEC pricing anchor.<br>
                • <b>India Geopolitics:</b> 88.2% foreign crude intake makes national fiscal balances sensitive to freight corridors and crude swings.
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

    prod_lb = get_cached_production_leaderboard()
    regional_prod, opec_split = get_cached_production_breakdowns()

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
    fig_prod_bar, fig_reg = get_cached_ch02_charts(prod_lb, regional_prod)

    with cp_chart1:
        st.markdown("#### 📊 Top 10 Crude Oil Producing Nations (2024 vs 2023)")
        st.plotly_chart(fig_prod_bar, width="stretch", theme=None)

    with cp_chart2:
        st.markdown("#### 🌐 Regional Production Shares")
        st.plotly_chart(fig_reg, width="stretch", theme=None)

    render_html(
        f"""
        <div style="background: rgba(14, 21, 38, 0.75); backdrop-filter: blur(14px); padding: 12px 16px; border-left: 3px solid {COLOR_AMBER}; border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3); border-radius: 4px; font-size: 0.84rem; color: #F9FAFB; margin-top: 6px; line-height: 1.5;">
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

    trade_matrix, top_exporters, top_importers = get_cached_trade_data(period="2026")
    fig_exp, fig_imp = get_cached_ch03_charts(top_exporters, top_importers)

    t_col1, t_col2 = st.columns([6, 6])

    with t_col1:
        st.markdown("#### 🚢 Top 5 Petroleum Exporters (Tracked Seaborne Flow)")
        if fig_exp is not None:
            st.plotly_chart(fig_exp, width="stretch", theme=None)

    with t_col2:
        st.markdown("#### 📥 Top 5 Petroleum Importers (Daily Intake)")
        if fig_imp is not None:
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

    prices_df = get_cached_fuel_prices(fuel_type=selected_story_fuel)

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
                subtext="₹101.84 / Litre (48% Tax Burden)",
                code_badge="IND"
            )

        # Comparative Bar Chart
        fig_price_bar = get_cached_ch04_price_chart(sorted_prices)
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

    # Fetch cached India Metro Data from fuel_prices
    india_prices_df = get_cached_india_prices()
    fig_metro_bar, fig_wf, delhi_petrol = get_cached_ch05_charts(india_prices_df)

    ind_c1, ind_c2 = st.columns([5, 7])

    with ind_c1:
        st.markdown("#### 🏙️ PPAC Metro Pricing Benchmark (₹ / Litre)")
        if fig_metro_bar is not None:
            st.plotly_chart(fig_metro_bar, width="stretch", theme=None)

    with ind_c2:
        ch5_state = st.selectbox(
            "Inspect State / City Price Anatomy",
            [
                "Delhi (NCT)",
                "Uttar Pradesh (Prayagraj / Lucknow)",
                "Maharashtra (Mumbai / Pune)",
                "Karnataka (Bengaluru)",
                "Tamil Nadu (Chennai)",
                "West Bengal (Kolkata)",
                "Rajasthan (Jaipur)",
                "Bihar (Patna)",
                "Gujarat (Ahmedabad)",
                "Telangana (Hyderabad)"
            ],
            key="ch05_state_selector"
        )
        ch5_res = GlobalTaxEngine.resolve_query(ch5_state.split("(")[0].strip()) or GlobalTaxEngine.resolve_query("Delhi")
        ch5_p_price = ch5_res["petrol_price"]
        st.markdown(f"#### 💰 Price Build-Up Anatomy ({ch5_res['jurisdiction_name']} Petrol ₹{ch5_p_price:.2f}/L)")

        # Build interactive waterfall for selected state
        steps = ch5_res.get("waterfall_steps", [])
        if steps:
            x_labels = [s["component"] for s in steps[:-1]] + ["Final Pump Price"]
            y_amounts = [s.get("amount_inr", 0.0) for s in steps[:-1]] + [0]
            text_labels = [f"₹{s.get('amount_inr', 0.0):.2f}" for s in steps[:-1]] + [f"₹{ch5_p_price:.2f}"]

            fig_ch5_wf = go.Figure(go.Waterfall(
                name="Cost Build-Up",
                orientation="v",
                measure=["relative"] * len(steps[:-1]) + ["total"],
                x=x_labels,
                y=y_amounts,
                text=text_labels,
                textposition="outside",
                connector={"line": {"color": "rgba(255, 255, 255, 0.25)"}},
                decreasing={"marker": {"color": "#F43F5E"}},
                increasing={"marker": {"color": COLOR_AMBER}},
                totals={"marker": {"color": "#60A5FA"}}
            ))
            apply_clean_layout(
                fig_ch5_wf,
                height=420,
                yaxis_title="Price (₹ / Litre)",
                margin_b=60
            )
            st.plotly_chart(fig_ch5_wf, width="stretch", theme=None)
            st.caption(f"State VAT: ₹{ch5_res['state_tax_amount']:.2f}/L ({ch5_res['state_tax_share_pump_pct']}% of pump price, +{ch5_res['state_tax_added_to_base_pct']}% over base). {ch5_res['statutory_note']}")
        else:
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

    hpcl, omc_df, hpcl_sales = get_cached_india_company_data()

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
    fig_omc, fig_hpcl_sales = get_cached_ch06_charts(omc_df, hpcl_sales)

    with hpcl_col1:
        st.markdown("#### ⚖️ OMC Peer Comparison (Throughput & Market Sales MMT)")
        st.plotly_chart(fig_omc, width="stretch", theme=None)

    with hpcl_col2:
        st.markdown("#### 📦 HPCL Product Sales Portfolio (46.82 MMT)")
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

    product_demand, regional_demand = get_cached_india_demand_data()
    fig_prod_dem, fig_reg_dem = get_cached_ch07_charts(product_demand, regional_demand)

    dem_c1, dem_c2 = st.columns([7, 5])

    with dem_c1:
        st.markdown("#### ⛽ Consumption by Petroleum Commodity (National Total ~233 MMT)")
        st.plotly_chart(fig_prod_dem, width="stretch", theme=None)

    with dem_c2:
        st.markdown("#### 🧭 Geographic Demand Distribution")
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
            <div style="background: rgba(14, 21, 38, 0.75); backdrop-filter: blur(14px); border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4); border-radius: 8px; padding: 22px 24px; height: 100%;">
                <div style="font-size: 0.82rem; font-weight: 800; text-transform: uppercase; color: #94A3B8; margin-bottom: 6px;">SOVEREIGN PETROLEUM FISCAL REVENUE</div>
                <div style="font-size: 2.2rem; font-weight: 800; color: #F9FAFB; line-height: 1.1;">₹4.82 Lakh Cr</div>
                <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 6px; margin-bottom: 16px;">Total Contribution to Central and State Exchequers (FY2023–24)</div>

                <div style="border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 12px; font-size: 0.85rem; line-height: 1.6; color: #E2E8F0;">
                    • <b>Central Exchequer:</b> ~₹2.81 Lakh Crore via Specific Central Excise Duty on Petrol & Diesel.<br>
                    • <b>State Exchequers:</b> ~₹2.01 Lakh Crore via State VAT, Sales Tax, and Local Cess.<br>
                    • <b>Non-GST Treatment:</b> Petrol, Diesel, and Crude Oil remain outside GST, preserving fiscal autonomy for Indian states.
                </div>
            </div>
            """
        )

    with rev_c2:
        st.markdown("#### 🏛️ Central vs. State Petroleum Revenue Composition")
        fig_rev_pie = get_cached_ch08_chart()
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

    afford_df = get_cached_affordability_data(reporting_year=2024)

    if not afford_df.empty:
        aff_c1, aff_c2 = st.columns([6, 6])
        fig_aff_bar, fig_scatter = get_cached_ch09_charts(afford_df)
        with aff_c1:
            st.markdown("#### ⚖️ % of Daily Income Spent per Litre of Petrol")
            st.plotly_chart(fig_aff_bar, width="stretch", theme=None)

        with aff_c2:
            st.markdown("#### 🔍 Nominal GDP per Capita vs. Fuel Burden (Log Scale)")
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
            fc_results = get_cached_forecast_data(country_iso3=fc_country, fuel_type=fc_fuel, horizon_weeks=4)

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

        sim_res = get_cached_shock_simulation(
            sim_exp=sim_exp,
            sim_imp=sim_imp,
            sim_cut=sim_cut,
            sim_shock=sim_shock,
            sim_fx=sim_fx
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

    freshness_list, tele_df, table_cts = get_cached_quality_audit_data()
    fresh_df = pd.DataFrame(freshness_list)

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
