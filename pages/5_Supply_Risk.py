"""
Page 5: Global Fuel Supply Risk Monitor.
Evaluates national petroleum import dependence, supplier concentration (HHI), and maritime chokepoints.
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
    COLOR_WHITE,
    COLOR_CREAM
)
from src.analytics.supply_risk import SupplyRiskMonitor, CHOKEPOINTS_REGISTRY

apply_theme()

render_page_header(
    title="GLOBAL FUEL SUPPLY RISK MONITOR",
    subtitle="Import Vulnerability, Supplier Concentration Exposure, and Strategic Maritime Chokepoints",
    source_tag="EIA Movements • UN Comtrade • Global Chokepoints Registry",
    observation_date="Strategic 2024–2025 Intelligence"
)

# Load Dependence Leaderboard
dep_df = SupplyRiskMonitor.get_import_dependence_leaderboard(period="2024")

# Top KPI Summary Cards
k1, k2, k3, k4 = st.columns(4)

with k1:
    render_instrument_card(
        label="Strategic Chokepoints",
        value=f"{len(CHOKEPOINTS_REGISTRY)} Critical Passages",
        accent="amber",
        subtext="Tracking 60%+ seaborne oil"
    )

with k2:
    hormuz_vol = CHOKEPOINTS_REGISTRY[0]["daily_transit_volume_mbpd"]
    render_instrument_card(
        label="Hormuz Daily Transit",
        value=f"{hormuz_vol:.1f} Million bpd",
        accent="red",
        subtext="Single largest global energy bottleneck",
        code_badge="HORMUZ"
    )

with k3:
    high_risk_importers = len(dep_df[dep_df["supplier_risk_tier"] == "High Concentration (High Exposure)"]) if not dep_df.empty else 4
    render_instrument_card(
        label="High Exposure Importers",
        value=f"{high_risk_importers} Economies",
        accent="copper",
        subtext="HHI > 2,500 supplier concentration"
    )

with k4:
    malacca_vol = CHOKEPOINTS_REGISTRY[1]["daily_transit_volume_mbpd"]
    render_instrument_card(
        label="Malacca Strait Transit",
        value=f"{malacca_vol:.1f} Million bpd",
        accent="teal",
        subtext="Primary Asia-Pacific supply artery",
        code_badge="MALACCA"
    )

st.write("")

# Strategic Chokepoint Map & Details
st.subheader("🗺️ Strategic Maritime Petroleum Shipping Chokepoints")
choke_col_map, choke_col_info = st.columns([7, 5])

with choke_col_map:
    choke_df = pd.DataFrame(CHOKEPOINTS_REGISTRY)
    choke_df["lat"] = [c["coordinates"][0] for c in CHOKEPOINTS_REGISTRY]
    choke_df["lon"] = [c["coordinates"][1] for c in CHOKEPOINTS_REGISTRY]

    fig_choke = px.scatter_geo(
        choke_df,
        lat="lat",
        lon="lon",
        hover_name="name",
        size="daily_transit_volume_mbpd",
        color="daily_transit_volume_mbpd",
        color_continuous_scale=[[0, COLOR_AMBER], [1, "#C53030"]],
        labels={"daily_transit_volume_mbpd": "Transit (Million bpd)"}
    )
    fig_choke.update_geos(
        showcoastlines=True, coastlinecolor=COLOR_INK,
        showland=True, landcolor="#EFEAD9",
        showocean=True, oceancolor=COLOR_WHITE,
        projection_type="natural earth",
        framecolor=COLOR_INK,
        framewidth=1.5
    )
    apply_clean_layout(
        fig_choke,
        height=480,
        margin_l=15,
        margin_b=20,
        coloraxis_colorbar=dict(title="Million bpd", thickness=14, title_font=dict(size=12, color=COLOR_INK), tickfont=dict(size=11, color=COLOR_INK))
    )
    st.plotly_chart(fig_choke, width="stretch", theme=None)

with choke_col_info:
    selected_chokepoint_name = st.selectbox("Select Chokepoint for Intelligence Profile:", [c["name"] for c in CHOKEPOINTS_REGISTRY])
    selected_cp = next(c for c in CHOKEPOINTS_REGISTRY if c["name"] == selected_chokepoint_name)

    st.markdown(f"### {selected_cp['name']}")
    st.markdown(f"**Region:** `{selected_cp['region']}`")
    st.markdown(f"**Transit Volume:** **{selected_cp['daily_transit_volume_mbpd']} Million bpd** ({selected_cp['share_of_global_seaborne_oil_pct']}% of global maritime oil)")
    st.markdown(f"**Primary Suppliers:** {', '.join(selected_cp['critical_suppliers'])}")
    st.markdown(f"**Destination Corridor:** {selected_cp['primary_destination_corridor']}")
    st.warning(f"**Vulnerability Notes:** {selected_cp['vulnerability_notes']}")

st.write("")

# Supplier Concentration & Import Exposure Table
st.subheader("📋 National Petroleum Import Vulnerability & Concentration Leaderboard")
if not dep_df.empty:
    display_dep = dep_df[[
        "country_name", "continent", "total_import_quantity",
        "global_import_share_percent", "hhi_concentration_index", "supplier_risk_tier"
    ]].rename(columns={
        "country_name": "Country", "continent": "Continent",
        "total_import_quantity": "Import Volume (bpd)", "global_import_share_percent": "Global Share %",
        "hhi_concentration_index": "HHI Concentration", "supplier_risk_tier": "Risk Tier"
    })
    st.dataframe(display_dep, width="stretch", hide_index=True)
    render_csv_download(display_dep, "fuelpulse_supply_risk_index.csv")

st.markdown("---")
st.info(
    """
    **Methodological Governance Note:**
    Trade concentration alone does not guarantee geopolitical disruption. The Herfindahl-Hirschman Index measures structural dependency on few trading partners. Geopolitical assessments should integrate strategic commercial stocks (SPR), bilateral diplomatic agreements, and alternative pipeline transit capacities.
    """
)
