"""
Page 6: Supply Shock Simulator.
Allows users to test hypothetical exporter supply cuts, crude price shocks, and commercial fleet budget impacts.
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
from src.analytics.shock_simulator import SupplyShockSimulator
from src.analytics.trade_analytics import PetroleumTradeAnalytics

apply_theme()
current_lang = get_current_language()

render_page_header(
    title=t("sidebar_06_shock", current_lang),
    subtitle=t("chapter_09_subtitle", current_lang),
    source_tag="Interactive Sensitivity Engine",
    observation_date="Simulation Sandbox"
)

# User Interactive Controls
st.subheader("⚙️ Scenario Simulation Parameters")
sim_c1, sim_c2, sim_c3 = st.columns(3)

with sim_c1:
    exporter_options = ["SAU", "RUS", "IRQ", "ARE", "CAN", "USA"]
    exporter_names = {
        "SAU": "Saudi Arabia", "RUS": "Russia", "IRQ": "Iraq",
        "ARE": "United Arab Emirates", "CAN": "Canada", "USA": "United States"
    }
    sel_exp = st.selectbox("Hypothetical Disrupted Exporter", exporter_options, format_func=lambda x: exporter_names.get(x, x))
    product_cat = st.selectbox("Affected Commodity", ["crude_oil", "refined_petroleum"], format_func=lambda x: "Crude Oil" if x == "crude_oil" else "Refined Products")

with sim_c2:
    importer_options = ["IND", "CHN", "USA", "JPN", "DEU"]
    importer_names = {"IND": "India", "CHN": "China", "USA": "United States", "JPN": "Japan", "DEU": "Germany"}
    sel_imp = st.selectbox("Target Importing Economy / Fleet Base", importer_options, format_func=lambda x: importer_names.get(x, x))
    supply_cut_pct = st.slider("Exporter Supply Reduction (%)", min_value=5.0, max_value=40.0, value=15.0, step=5.0)

with sim_c3:
    crude_delta = st.number_input("Assumed Global Crude Price Shock (+$/bbl)", min_value=0.0, max_value=60.0, value=12.0, step=2.0)
    fx_depreciation = st.slider("Domestic Currency Depreciation (% vs USD)", min_value=0.0, max_value=20.0, value=2.5, step=0.5)

# Fleet Parameters Expander
with st.expander("🚚 Commercial Fleet Fleet Budget Parameters (Optional Customization)", expanded=False):
    fl_col1, fl_col2 = st.columns(2)
    with fl_col1:
        fleet_litres = st.number_input("Monthly Commercial Fleet Consumption (Litres)", min_value=1000.0, max_value=5000000.0, value=250000.0, step=10000.0)
    with fl_col2:
        baseline_price = st.number_input("Baseline Retail Price (USD / Litre)", min_value=0.20, max_value=3.50, value=1.05, step=0.05)

# Execute Simulation
sim_results = SupplyShockSimulator.simulate_export_curtailment(
    exporter_iso3=sel_exp,
    target_importer_iso3=sel_imp,
    product_category=product_cat,
    export_reduction_pct=supply_cut_pct,
    assumed_crude_price_delta_usd_per_bbl=crude_delta,
    exchange_rate_depreciation_pct=fx_depreciation,
    monthly_fleet_fuel_consumption_litres=fleet_litres,
    baseline_retail_price_usd_per_litre=baseline_price
)

st.markdown("---")

# KPI Summary
st.subheader("📊 Scenario Impact Assessment")
sk1, sk2, sk3, sk4, sk5 = st.columns(5)

with sk1:
    render_instrument_card(
        label="Volume Deficit",
        value=f"{sim_results['volume_deficit_bpd']:,.0f} bpd",
        accent="red",
        delta=f"-{sim_results['export_reduction_pct']:.1f}%",
        delta_is_positive_bad=True,
        subtext=f"Cut from {exporter_names.get(sel_exp, sel_exp)}"
    )

with sk2:
    base_flow = sim_results['baseline_bilateral_bpd']
    pct_rem = (sim_results['scenario_remaining_supply_bpd'] / max(1.0, float(base_flow))) * 100.0
    render_instrument_card(
        label="Remaining Supply",
        value=f"{sim_results['scenario_remaining_supply_bpd']:,.0f} bpd",
        accent="amber",
        delta=f"{pct_rem:.1f}% flow kept",
        delta_is_positive_bad=False,
        subtext=f"Baseline: {base_flow:,.0f} bpd"
    )

with sk3:
    render_instrument_card(
        label="Simulated Retail Price",
        value=f"${sim_results['scenario_retail_price_usd']:.4f}/L",
        accent="red",
        delta=f"+{sim_results['retail_price_pct_increase']:.1f}%",
        delta_is_positive_bad=True,
        subtext=f"Baseline: ${sim_results['baseline_retail_price_usd']:.4f}/L"
    )

with sk4:
    render_instrument_card(
        label="Monthly Fleet Deficit",
        value=f"+${sim_results['additional_monthly_fleet_cost_usd']:,.0f}",
        accent="red",
        delta=f"+${sim_results['additional_monthly_fleet_cost_usd']:,.0f}",
        delta_is_positive_bad=True,
        subtext="Additional monthly expenditure"
    )

with sk5:
    render_instrument_card(
        label="Annualized Cost Surge",
        value=f"+${sim_results['annualized_fleet_cost_increase_usd']:,.0f}",
        accent="copper",
        delta="12-Mo Horizon",
        delta_is_positive_bad=True,
        subtext="Cumulative yearly budget risk"
    )

st.write("")

# Sensitivity Analysis Plot & Table
sc_col1, sc_col2 = st.columns([7, 5])

with sc_col1:
    st.subheader("📈 Multi-Factor Sensitivity Curve")
    sens_df = pd.DataFrame(sim_results["sensitivity_curve"])
    fig_sens = px.line(
        sens_df,
        x="export_cut_pct",
        y="additional_cost_usd",
        markers=True,
        labels={"export_cut_pct": "Export Curtailment (%)", "additional_cost_usd": "Additional Monthly Fleet Spend ($)"},
        color_discrete_sequence=["#C53030"]
    )
    fig_sens.update_traces(line=dict(width=2.5), marker=dict(size=7, line=dict(color=COLOR_INK, width=1.5)))
    apply_clean_layout(
        fig_sens,
        height=460,
        showlegend=False,
        xaxis_title="Export Curtailment (%)",
        yaxis_title="Additional Monthly Spend ($)"
    )
    st.plotly_chart(fig_sens, width="stretch", theme=None)

with sc_col2:
    st.subheader("📋 Sensitivity Matrix")
    display_sens = sens_df[[
        "export_cut_pct", "deficit_bpd", "simulated_retail_price_usd", "additional_cost_usd"
    ]].rename(columns={
        "export_cut_pct": "Cut %", "deficit_bpd": "Deficit (bpd)",
        "simulated_retail_price_usd": "Sim Price ($/L)", "additional_cost_usd": "Monthly Added Cost ($)"
    })
    st.dataframe(display_sens, width="stretch", hide_index=True)

st.markdown("---")
st.warning(f"**Methodological Note:** {sim_results['assumptions_disclaimer']}")

# Universal Floating AI Assistant Dock (Bottom-Right FAB)
render_universal_ai_assistant(context_page="Supply Shock Simulator", key_prefix="p6_shock")
