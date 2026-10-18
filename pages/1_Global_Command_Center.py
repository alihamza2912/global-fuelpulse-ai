"""
THE ENERGY ATLAS — GLOBAL COMMAND CENTER
Signature Asymmetric Intelligence Console: World Map Anchor, Global Signal Rail & Market Movements.
"""

import sys
from pathlib import Path

# Ensure project root AND src directory are in sys.path and remove conflicting parent mount
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
    render_command_strip,
    render_universal_ai_assistant,
    render_signal_rail,
    render_instrument_card,
    render_csv_download,
    apply_theme,
    get_atlas_plotly_theme,
    apply_clean_layout,
    clean_html,
    render_html,
    COLOR_GRAPHITE,
    COLOR_OBSIDIAN,
    COLOR_BORDER,
    COLOR_AMBER,
    COLOR_TEAL,
    COLOR_COPPER,
    COLOR_RED,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    COLOR_INK,
    COLOR_WHITE,
    COLOR_CREAM
)
from src.localization.i18n import t, get_current_language
from src.analytics.price_analytics import FuelPriceAnalytics
from src.analytics.trade_analytics import PetroleumTradeAnalytics
from src.monitoring.quality_auditor import DataQualityAuditor

apply_theme()
current_lang = get_current_language()

# 1. Top Enterprise Command Strip with Synchronized Universal Header
render_command_strip(
    active_page="Global Command Center",
    region_tag="WORLDWIDE REPOSITORY",
    product_tag="MOTOR FUELS & CRUDE",
    reporting_period="LATEST 2024–2025"
)

# 1b. Integrated Universal AI Assistant Dock
render_universal_ai_assistant(context_page="Global Command Center", key_prefix="p1_cmd")

# 2. Interactive Analytical Controls Filter Bar
render_html(f'<div class="atlas-section-title">{t("sidebar_01_command", current_lang)} — CONTROL TERMINAL & PARAMETERS</div>')
ctrl_c1, ctrl_c2, ctrl_c3, ctrl_c4 = st.columns([3, 3, 4, 2])

with ctrl_c1:
    selected_fuel = st.selectbox(
        "COMMODITY SPECIFICATION",
        ["petrol_regular", "diesel"],
        format_func=lambda x: "Regular Motor Gasoline (Petrol)" if x == "petrol_regular" else "On-Highway Diesel Fuel"
    )

with ctrl_c2:
    selected_continent = st.selectbox(
        "CONTINENTAL SECTOR",
        ["All Sectors", "Asia", "Europe", "North America", "South America", "Africa", "Oceania"]
    )
    continent_filter = None if selected_continent == "All Sectors" else selected_continent

with ctrl_c3:
    all_prices = FuelPriceAnalytics.get_latest_prices(fuel_type=selected_fuel, continent=continent_filter)
    country_list = ["Global Focus (All)"] + sorted(all_prices["country_name"].unique().tolist())
    selected_country = st.selectbox("SOVEREIGN ECONOMY DEEP-DIVE", country_list)
    country_filter = None if selected_country == "Global Focus (All)" else selected_country

with ctrl_c4:
    st.write("")
    st.write("")
    if st.button("⚡ RE-QUERY", type="primary", width="stretch", help="Re-queries active data store for latest observations"):
        st.cache_data.clear()
        st.rerun()

# 3. Global Signal Rail
summary = FuelPriceAnalytics.get_global_price_summary(selected_fuel)
top_exp = PetroleumTradeAnalytics.get_top_exporters("crude_oil", "2024", limit=1)
top_imp = PetroleumTradeAnalytics.get_top_importers("crude_oil", "2024", limit=1)

render_signal_rail([
    {
        "label": f"LATEST {selected_fuel.replace('_', ' ').upper()} MEAN",
        "value": f"${summary['unweighted_avg_usd']:.4f} / L",
        "note": "Unweighted sovereign mean"
    },
    {
        "label": "MINIMUM OBSERVATION",
        "value": f"${summary['min_price_usd']:.4f} / L",
        "note": f"{summary.get('min_country', 'N/A')}"
    },
    {
        "label": "MAXIMUM OBSERVATION",
        "value": f"${summary['max_price_usd']:.4f} / L",
        "note": f"{summary.get('max_country', 'N/A')}"
    },
    {
        "label": "CRUDE EXPORT LEADER",
        "value": top_exp.iloc[0]["country_name"] if not top_exp.empty else "Saudi Arabia",
        "note": f"{top_exp.iloc[0]['total_export_quantity']:,.0f} bpd" if not top_exp.empty else "4.29M bpd"
    },
    {
        "label": "CRUDE IMPORT LEADER",
        "value": top_imp.iloc[0]["country_name"] if not top_imp.empty else "China",
        "note": f"{top_imp.iloc[0]['total_import_quantity']:,.0f} bpd" if not top_imp.empty else "11.3M bpd"
    }
])

st.write("")

# 4. Asymmetric Analytical Composition: World Map Anchor (Left) & Instrument Rail (Right)
map_col, inst_col = st.columns([8, 4])

with map_col:
    render_html('<div class="atlas-section-title">THE ENERGY ATLAS — GLOBAL RETAIL FUEL PRICE TOPOGRAPHY</div>')
    if not all_prices.empty:
        # Create Custom Continuous Color Scale (Cream to Amber to Ink)
        price_heat_scale = [
            [0.0, "#10B981"],   # Emerald (Low / Subsidized: < $0.70/L)
            [0.35, "#F5B942"],  # Amber (Moderate: $0.70 - $1.20/L)
            [0.70, "#F97316"],  # Orange (High: $1.20 - $1.60/L)
            [1.0, "#EF4444"]    # Crimson Red (Heavy Tax: > $1.70/L)
        ]

        fig_map = px.choropleth(
            all_prices,
            locations="country_iso3",
            color="price_usd_per_litre",
            hover_name="country_name",
            hover_data={
                "price_usd_per_litre": ":$.4f",
                "price_local": ":.2f",
                "currency_local": True,
                "observation_date": True,
                "source_name": True,
                "country_iso3": False
            },
            color_continuous_scale=price_heat_scale,
            labels={"price_usd_per_litre": "USD / Litre"}
        )

        fig_map.update_geos(
            bgcolor="rgba(0,0,0,0)",
            showcoastlines=True,
            coastlinecolor="rgba(255, 255, 255, 0.28)",
            showland=True,
            landcolor="#0E1526",
            showocean=True,
            oceancolor="#070A12",
            showlakes=True,
            lakecolor="#070A12",
            showcountries=True,
            countrycolor="rgba(255, 255, 255, 0.12)",
            countrywidth=0.8,
            projection_type="natural earth",
            showframe=False
        )


        apply_clean_layout(
            fig_map,
            height=520,
            margin_l=15,
            margin_b=20,
            coloraxis_colorbar=dict(
                title=dict(text="USD / LITRE"),
                thickness=14,
                len=0.75,
                title_font=dict(size=12, color=COLOR_INK),
                tickfont=dict(size=11, color=COLOR_INK)
            )
        )
        st.plotly_chart(fig_map, width="stretch", theme=None)
    else:
        st.warning("No price observations match the active filter criteria.")

with inst_col:
    render_html('<div class="atlas-section-title">ACTIVE SECTOR TELEMETRY</div>')
    
    # Check if a specific country is focused
    if country_filter and country_filter != "Global Focus (All)":
        c_row = all_prices[all_prices["country_name"] == country_filter]
        if not c_row.empty:
            iso3 = c_row.iloc[0]["country_iso3"]
            chg = FuelPriceAnalytics.calculate_price_change_metrics(iso3, selected_fuel)
            render_instrument_card(
                label=f"{country_filter.upper()} CURRENT QUOTE",
                value=f"${chg['current_price_usd']:.4f} / L",
                accent="amber",
                delta=f"{chg['percentage_change']:+.2f}%" if chg["has_previous"] else None,
                subtext=f"{chg.get('current_price_local', 0.0):.2f} {chg.get('currency', 'USD')}/L",
                code_badge=iso3
            )
            st.write("")
            render_instrument_card(
                label="PRIOR PERIOD OBSERVATION",
                value=f"${chg['previous_price_usd']:.4f} / L" if chg['has_previous'] else "NO PRIOR RECORD",
                accent="teal",
                subtext=f"Observed: {chg.get('previous_date', 'N/A')}",
                code_badge="LAG-1"
            )
            st.write("")
            render_instrument_card(
                label="ABSOLUTE VARIANCE",
                value=f"{chg['absolute_change_usd']:+.4f} USD",
                accent="red" if chg['absolute_change_usd'] > 0 else "teal",
                subtext="Period-over-period delta",
                code_badge="ABS"
            )
    else:
        # Global Focus Telemetry Cards
        render_instrument_card(
            label="TRACKED SOVEREIGN ECONOMIES",
            value=f"{len(all_prices)} Nations",
            accent="teal",
            subtext="Active reporting jurisdictions",
            code_badge="COV"
        )
        st.write("")
        render_instrument_card(
            label="SOVEREIGN SPREAD (MAX - MIN)",
            value=f"${(summary['max_price_usd'] - summary['min_price_usd']):.4f} / L",
            accent="amber",
            subtext="Global retail price disparity",
            code_badge="SPREAD"
        )
        st.write("")
        render_instrument_card(
            label="ANNUAL CRUDE TRADE MONITORED",
            value=f"${(top_exp['total_export_value_usd'].sum() if not top_exp.empty else 5.15e10) / 1e9:.1f}B USD",
            accent="copper",
            subtext="Customs commodity valuation",
            code_badge="VALUE"
        )

st.write("")

# 5. Market Movement Panel (Large Instrument Chart)
render_html('<div class="atlas-section-title">MARKET MOVEMENT INSTRUMENT — PRICE DISPERSION & COUNTRY RANKINGS</div>')
chart_col_rank, chart_col_dist = st.columns([7, 5])

with chart_col_rank:
    if not all_prices.empty:
        sorted_p = all_prices.sort_values("price_usd_per_litre", ascending=True)
        fig_rank = px.bar(
            sorted_p.head(14),
            x="price_usd_per_litre",
            y="country_name",
            orientation="h",
            labels={"price_usd_per_litre": "USD / Litre", "country_name": "Economy"},
            color="price_usd_per_litre",
            color_continuous_scale=[[0.0, "#E8E4D8"], [1.0, COLOR_AMBER]]
        )
        fig_rank.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.2)))
        apply_clean_layout(
            fig_rank,
            height=480,
            margin_l=130,
            showlegend=False,
            coloraxis_showscale=False,
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_rank, width="stretch", theme=None)

with chart_col_dist:
    if not all_prices.empty:
        fig_hist = px.histogram(
            all_prices,
            x="price_usd_per_litre",
            nbins=12,
            marginal="box",
            labels={"price_usd_per_litre": "USD / Litre"},
            color_discrete_sequence=[COLOR_AMBER]
        )
        fig_hist.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.2)))
        apply_clean_layout(
            fig_hist,
            height=480,
            showlegend=False,
            xaxis_title="USD / Litre",
            bargap=0.1
        )
        st.plotly_chart(fig_hist, width="stretch", theme=None)

st.write("")

# 6. Detailed Sovereign Energy Observation Table
render_html('<div class="atlas-section-title">VERIFIED OBSERVATION AUDIT TRAIL & PROVENANCE</div>')
audit_table = all_prices[[
    "country_name", "continent", "location_name", "fuel_type", "price_local",
    "currency_local", "price_usd_per_litre", "tax_component_percent", "observation_date", "source_name"
]].rename(columns={
    "country_name": "Economy", "location_name": "Sub-National Point", "fuel_type": "Commodity",
    "price_local": "Local Quote", "currency_local": "Currency", "price_usd_per_litre": "Price (USD/L)",
    "tax_component_percent": "Tax %", "observation_date": "Observation Date", "source_name": "Verified Source"
})
st.dataframe(audit_table, width="stretch", hide_index=True)
render_csv_download(audit_table, f"atlas_{selected_fuel}_command_center.csv")
