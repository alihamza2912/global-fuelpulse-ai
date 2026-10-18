"""
Page 2: Live Global Fuel Price Explorer.
Priority Module A: Interactive retail petrol and diesel price tracker across global economies.
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
    render_page_header,
    render_instrument_card,
    render_csv_download,
    apply_theme,
    get_atlas_plotly_theme,
    apply_clean_layout,
    COLOR_INK,
    COLOR_AMBER,
    COLOR_WHITE
)
from src.analytics.price_analytics import FuelPriceAnalytics
from src.ingestion.orchestrator import orchestrator
from config.settings import settings

apply_theme()

render_page_header(
    title="LIVE GLOBAL FUEL PRICE EXPLORER",
    subtitle="Retail Gasoline & Diesel Price Benchmarking, Trends, and Currency Conversions",
    source_tag="US EIA • India PPAC • EC Oil Bulletin • GlobalPetrolPrices",
    observation_date="Weekly & Daily Reporting Intervals"
)

# Interactive Filters
f_col1, f_col2, f_col3, f_col4 = st.columns([2, 2, 2, 2])

with f_col1:
    continent = st.selectbox("Continent / Region", ["All", "Asia", "Europe", "North America", "South America", "Africa", "Oceania"])

with f_col2:
    fuel_type = st.selectbox(
        "Fuel Category",
        ["petrol_regular", "diesel"],
        format_func=lambda x: "Regular Motor Gasoline (Petrol)" if x == "petrol_regular" else "Automotive Diesel"
    )

with f_col3:
    all_prices = FuelPriceAnalytics.get_latest_prices(fuel_type=fuel_type, continent=continent)
    countries = sorted(all_prices["country_name"].unique().tolist()) if not all_prices.empty else ["United States"]
    primary_country = st.selectbox("Focus Country", countries, index=0)

with f_col4:
    display_currency = st.radio("Display Parity", ["USD per Litre", "Local Currency"], horizontal=True)

# Authorized Refresh Button
refresh_col1, refresh_col2 = st.columns([6, 2])
with refresh_col2:
    if st.button("⚡ Ingest / Re-query Fuel Feeds", type="primary", width="stretch"):
        with st.spinner("Connecting to external authorized fuel data pipelines..."):
            summary = orchestrator.run_fuel_prices_only()
            st.success(f"Ingested {len(summary)} pipelines successfully.")
            st.cache_data.clear()

st.markdown("---")

# Metrics for Selected Country
c_data = all_prices[all_prices["country_name"] == primary_country]
if not c_data.empty:
    country_iso3 = c_data.iloc[0]["country_iso3"]
    change_metrics = FuelPriceAnalytics.calculate_price_change_metrics(country_iso3, fuel_type)

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        usd_val = change_metrics["current_price_usd"]
        loc_val = change_metrics.get("current_price_local")
        curr_code = change_metrics.get("currency", "USD")
        val_str = f"${usd_val:.4f}/L" if display_currency == "USD per Litre" else f"{loc_val:.2f} {curr_code}/L"
        render_instrument_card(
            label=f"Current {primary_country} Price",
            value=val_str,
            accent="amber",
            delta=f"{change_metrics['percentage_change']:+.2f}%" if change_metrics["has_previous"] else None,
            delta_is_positive_bad=True,
            subtext=f"Observed: {change_metrics['current_date']}"
        )

    with m2:
        prev_usd = change_metrics.get("previous_price_usd")
        prev_str = f"${prev_usd:.4f}/L" if prev_usd else "No Prior Record"
        render_instrument_card(
            label="Previous Period Price",
            value=prev_str,
            accent="teal",
            subtext=f"Date: {change_metrics.get('previous_date', 'N/A')}"
        )

    with m3:
        abs_diff = change_metrics["absolute_change_usd"]
        diff_str = f"{abs_diff:+.4f} USD" if abs_diff != 0 else "0.0000 USD"
        render_instrument_card(
            label="Absolute Price Delta",
            value=diff_str,
            accent="copper",
            subtext="Period-over-period change"
        )

    with m4:
        pct_diff = change_metrics["percentage_change"]
        render_instrument_card(
            label="Percentage Movement",
            value=f"{pct_diff:+.2f}%",
            accent="red" if pct_diff > 0 else "teal",
            delta=f"{pct_diff:+.2f}%",
            delta_is_positive_bad=True,
            subtext="Relative price change"
        )

    with m5:
        source_name = c_data.iloc[0]["source_name"]
        render_instrument_card(
            label="Data Provenance",
            value=source_name[:15] + "..." if len(source_name) > 15 else source_name,
            accent="amber",
            subtext="Official verified feed"
        )
else:
    st.info("Select a country with available records to view metrics.")

st.write("")

# Historical Trend Chart & Multi-Country Comparison
trend_col, comp_col = st.columns([7, 5])

with trend_col:
    st.subheader(f"📈 Historical Price Trend: {primary_country}")
    # Retrieve historical observations
    query = """
    SELECT observation_date, price_usd_per_litre, price_local, currency_local, source_id
    FROM fuel_prices
    WHERE country_iso3 = :iso3 AND fuel_type = :fuel
    ORDER BY observation_date ASC
    """
    from src.database.connection import db_manager
    from sqlalchemy import text
    with db_manager.engine.connect() as conn:
        hist_df = pd.read_sql(text(query), conn, params={"iso3": country_iso3, "fuel": fuel_type})

    if not hist_df.empty:
        fig_trend = px.line(
            hist_df,
            x="observation_date",
            y="price_usd_per_litre" if display_currency == "USD per Litre" else "price_local",
            markers=True,
            labels={
                "observation_date": "Observation Date",
                "price_usd_per_litre": "USD / Litre",
                "price_local": f"Local Price ({c_data.iloc[0]['currency_local']})"
            },
            color_discrete_sequence=[COLOR_AMBER]
        )
        fig_trend.update_traces(line=dict(width=2.5), marker=dict(size=7, line=dict(color=COLOR_INK, width=1.5)))
        apply_clean_layout(
            fig_trend,
            height=460,
            showlegend=False,
            xaxis_title="Observation Date",
            yaxis_title="Price"
        )
        st.plotly_chart(fig_trend, width="stretch", theme=None)
    else:
        st.warning("Insufficient historical series for selected country.")

with comp_col:
    st.subheader("⚖️ Multi-Country Price Comparison")
    comp_countries = st.multiselect(
        "Compare Countries (Up to 5):",
        options=sorted(all_prices["country_name"].unique().tolist()),
        default=[c for c in ["United States", "India", "Germany", "Saudi Arabia"] if c in all_prices["country_name"].values][:4]
    )
    if comp_countries:
        comp_df = all_prices[all_prices["country_name"].isin(comp_countries)].sort_values("price_usd_per_litre")
        fig_comp = px.bar(
            comp_df,
            x="price_usd_per_litre",
            y="country_name",
            color="continent",
            orientation="h",
            labels={"price_usd_per_litre": "Price (USD / Litre)", "country_name": "Country"}
        )
        fig_comp.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.2)))
        apply_clean_layout(
            fig_comp,
            height=480,
            margin_l=130,
            legend_below=True,
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_comp, width="stretch", theme=None)

st.write("")

# Price Distribution Across All Reporting Economies
st.subheader(f"📊 Global Retail Price Distribution ({fuel_type.replace('_', ' ').title()})")
dist_col1, dist_col2 = st.columns([7, 5])

with dist_col1:
    fig_hist = px.histogram(
        all_prices,
        x="price_usd_per_litre",
        nbins=15,
        marginal="box",
        color_discrete_sequence=[COLOR_AMBER],
        labels={"price_usd_per_litre": "Price (USD / Litre)"}
    )
    fig_hist.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.2)))
    apply_clean_layout(
        fig_hist,
        height=460,
        showlegend=False,
        xaxis_title="Price (USD / Litre)"
    )
    st.plotly_chart(fig_hist, width="stretch", theme=None)

with dist_col2:
    st.markdown("### 📌 Pricing Insights & Benchmarks")
    st.write(
        """
        - **Subsidized Major Exporters:** Countries such as *Saudi Arabia*, *Kuwait*, and *UAE* exhibit the lowest retail fuel prices due to direct domestic producer subsidies.
        - **High-Tax European Economies:** Countries including *Norway*, *Germany*, *France*, and *Italy* demonstrate the highest consumer prices, where duties, carbon taxation, and VAT constitute over 50% of the pump price.
        - **Retail vs. Crude Distinction:** Retail fuel prices incorporate crude procurement, refining margins, distribution, dealer commissions, and excise taxes, differing substantially from spot crude benchmarks ($/barrel).
        """
    )

st.write("")

# Searchable Data Table
st.subheader("📑 Global Retail Fuel Price Records")
table_view = all_prices[[
    "country_name", "continent", "location_name", "fuel_type", "price_local",
    "currency_local", "price_usd_per_litre", "tax_component_percent", "observation_date", "source_name"
]].rename(columns={
    "country_name": "Country", "location_name": "Location", "price_local": "Local Price",
    "currency_local": "Currency", "price_usd_per_litre": "Price (USD/L)",
    "tax_component_percent": "Tax %", "observation_date": "Obs Date", "source_name": "Source"
})
st.dataframe(table_view, width="stretch", hide_index=True)
render_csv_download(table_view, f"fuelpulse_{fuel_type}_prices.csv")
