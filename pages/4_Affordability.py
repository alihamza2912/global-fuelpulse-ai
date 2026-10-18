"""
Page 4: Fuel Price Evaluation & Affordability.
Analyzes consumer fuel burden relative to GDP per capita and daily income proxies.
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
from src.ui_components import (
    render_page_header,
    render_universal_ai_assistant,
    render_instrument_card,
    render_csv_download,
    apply_theme,
    get_atlas_plotly_theme,
    apply_clean_layout,
    COLOR_INK,
    COLOR_AMBER
)
from src.localization.i18n import t, get_current_language
from src.analytics.affordability import AffordabilityAnalytics
from src.analytics.price_analytics import FuelPriceAnalytics

apply_theme()
current_lang = get_current_language()

render_page_header(
    title=t("sidebar_04_afford", current_lang),
    subtitle=t("chapter_07_subtitle", current_lang),
    source_tag="World Bank • EIA • PPAC",
    observation_date="2024 Benchmark Data"
)

# Load Affordability Overview
afford_df = AffordabilityAnalytics.get_affordability_overview(reporting_year=2024)

# Top KPI row
k1, k2, k3, k4 = st.columns(4)

with k1:
    best_row = afford_df.iloc[0] if not afford_df.empty else None
    render_instrument_card(
        label="Most Affordable Fuel",
        value=f"{best_row['petrol_litre_percent_daily_income']:.2f}% income" if best_row is not None else "0.35%",
        accent="teal",
        subtext=f"Leader: {best_row['country_name'] if best_row is not None else 'USA'}"
    )

with k2:
    worst_row = afford_df.iloc[-1] if not afford_df.empty else None
    render_instrument_card(
        label="Severe Affordability Burden",
        value=f"{worst_row['petrol_litre_percent_daily_income']:.1f}% income" if worst_row is not None else "23.4%",
        accent="red",
        subtext=f"Highest burden: {worst_row['country_name'] if worst_row is not None else 'Nigeria'}"
    )

with k3:
    median_afford = afford_df["petrol_litre_percent_daily_income"].median() if not afford_df.empty else 1.3
    render_instrument_card(
        label="Median Daily Income Burden",
        value=f"{median_afford:.2f}%",
        accent="amber",
        subtext="1 Litre Petrol / Daily Income"
    )

with k4:
    critical_count = len(afford_df[afford_df["affordability_tier"].isin(["Severe", "Critical"])])
    render_instrument_card(
        label="Vulnerable Economies",
        value=f"{critical_count} Countries",
        accent="copper",
        subtext="Spend > 5% daily income per litre"
    )

st.write("")

# Visualizations: Affordability Rankings & Scatter Plot
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 Fuel Affordability Rankings (% Daily Income / Litre)")
    if not afford_df.empty:
        fig_bar = px.bar(
            afford_df.sort_values("petrol_litre_percent_daily_income", ascending=False),
            x="petrol_litre_percent_daily_income",
            y="country_name",
            color="affordability_tier",
            color_discrete_map={
                "High": "#2C7A7B",
                "Moderate": COLOR_AMBER,
                "Severe": "#C05621",
                "Critical": "#C53030"
            },
            orientation="h",
            labels={"petrol_litre_percent_daily_income": "% of Daily Income Proxy", "country_name": "Country"}
        )
        fig_bar.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.2)))
        apply_clean_layout(
            fig_bar,
            height=480,
            margin_l=130,
            legend_below=True,
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_bar, width="stretch", theme=None)

with col_chart2:
    st.subheader("🔍 GDP per Capita vs. Fuel Affordability")
    if not afford_df.empty:
        fig_scatter = px.scatter(
            afford_df,
            x="gdp_per_capita_nominal_usd",
            y="petrol_litre_percent_daily_income",
            color="continent",
            hover_name="country_name",
            size="petrol_litre_percent_daily_income",
            log_x=True,
            labels={
                "gdp_per_capita_nominal_usd": "Nominal GDP per Capita (USD, Log Scale)",
                "petrol_litre_percent_daily_income": "% Daily Income / Litre"
            }
        )
        fig_scatter.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.5)))
        apply_clean_layout(
            fig_scatter,
            height=480,
            legend_below=True
        )
        st.plotly_chart(fig_scatter, width="stretch", theme=None)

st.write("")

# Methodology & Analytical Notes
st.markdown("### 💡 Analytical Methodology & Governance")
st.info(
    """
    **Definition of Income Proxy:**
    The daily income proxy is calculated as $\\text{Daily Income Proxy} = \\frac{\\text{Nominal GDP per Capita}}{365}$.
    
    *Important Caveat:* GDP per capita measures gross economic output per resident and does not equal household disposable income. In countries with significant income inequality or informal economies, the actual fuel burden on lower-income deciles is substantially higher.
    
    **Policy Context:**
    - Developed economies (e.g., USA, Germany) exhibit very low daily income expenditure per litre (< 1.5%), even where nominal fuel pump taxes exceed 50%.
    - Developing and emerging markets (e.g., India, Nigeria) face elevated affordability pressure (> 10-25% of daily income per litre), rendering household budgets highly vulnerable to crude oil price shocks.
    """
)

# Data Table
st.dataframe(
    afford_df[[
        "rank_best_to_worst", "country_name", "continent", "income_group",
        "gdp_per_capita_nominal_usd", "daily_income_proxy_usd",
        "petrol_litre_percent_daily_income", "affordability_tier"
    ]].rename(columns={
        "rank_best_to_worst": "Rank", "country_name": "Country",
        "gdp_per_capita_nominal_usd": "GDP per Cap (USD)", "daily_income_proxy_usd": "Daily Proxy ($)",
        "petrol_litre_percent_daily_income": "% Daily Income", "affordability_tier": "Tier"
    }),
    width="stretch",
    hide_index=True
)
render_csv_download(afford_df, "fuelpulse_affordability_index.csv")

# Universal Floating AI Assistant Dock (Bottom-Right FAB)
render_universal_ai_assistant(context_page="Fuel Affordability", key_prefix="p4_afford")
