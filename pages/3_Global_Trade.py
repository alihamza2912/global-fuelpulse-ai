"""
THE ENERGY ATLAS — GLOBAL PETROLEUM TRADE & LOGISTICS INTELLIGENCE
Global maritime trade corridors, bilateral crude flows, customs valuations, and HHI concentration risk.
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
    COLOR_COPPER,
    COLOR_TEAL,
    COLOR_RED,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    COLOR_INK,
    COLOR_WHITE,
    COLOR_CREAM
)
from src.localization.i18n import t, get_current_language
from src.analytics.trade_analytics import PetroleumTradeAnalytics
from src.transformations.normalizers import normalize_country_iso3

apply_theme()
current_lang = get_current_language()

# 1. Top Enterprise Command Strip with Synchronized Universal Header
render_command_strip(
    active_page="Petroleum Logistics Intelligence",
    region_tag="MARITIME CORRIDORS & PORTS",
    product_tag="CRUDE (HS 2709) & REFINED (HS 2710)",
    reporting_period="2025–2026 LIVE CUSTOMS RADAR"
)

# 1b. Integrated Universal AI Assistant Dock
render_universal_ai_assistant(context_page="Global Petroleum Trade", key_prefix="p3_trade")

# 2. Controls & Parameter Bar
render_html(f'<div class="atlas-section-title">{t("sidebar_03_trade", current_lang)} — LOGISTICS RADAR CONTROLS</div>')
tr_c1, tr_c2, tr_c3, tr_c4 = st.columns([3, 2, 3, 2])

with tr_c1:
    product_cat = st.selectbox(
        "COMMODITY HS CLASSIFICATION",
        ["crude_oil", "refined_petroleum"],
        format_func=lambda x: "Crude Petroleum (HS 2709)" if x == "crude_oil" else "Refined Motor Products (HS 2710)"
    )

with tr_c2:
    period_choice = st.selectbox(
        "CUSTOMS AUDIT PERIOD",
        ["2026 (Live Customs)", "2025 (Annual Series)", "2024 (Historical Benchmark)"]
    )
    reporting_period = "2026" if "2026" in period_choice else ("2025" if "2025" in period_choice else "2024")

with tr_c3:
    all_exporters = PetroleumTradeAnalytics.get_top_exporters(product_cat, reporting_period, limit=30)
    all_importers = PetroleumTradeAnalytics.get_top_importers(product_cat, reporting_period, limit=30)
    country_choices = sorted(list(set(
        all_exporters["country_name"].tolist() + all_importers["country_name"].tolist()
    ))) if not all_exporters.empty else ["Saudi Arabia", "United States", "China", "India"]
    selected_country = st.selectbox("SOVEREIGN TRADE DOSSIER", country_choices)

with tr_c4:
    trade_metric_view = st.radio("ANALYSIS METRIC", ["Volume (bpd)", "Valuation (USD)"], horizontal=True)

# 3. Global Signal Rail
total_volume = all_exporters["total_export_quantity"].sum() if not all_exporters.empty else 0
total_val_usd = all_exporters["total_export_value_usd"].sum() if not all_exporters.empty else 0
top_exp = all_exporters.iloc[0] if not all_exporters.empty else None
top_imp = all_importers.iloc[0] if not all_importers.empty else None

render_signal_rail([
    {
        "label": "TRACKED GLOBAL SEABORNE TRADE",
        "value": f"{total_volume:,.0f} bpd",
        "note": f"{product_cat.replace('_', ' ').title()}"
    },
    {
        "label": "TOTAL CUSTOMS VALUATION",
        "value": f"${total_val_usd / 1e9:.1f} Billion USD",
        "note": "Official customs valuation"
    },
    {
        "label": "LEADING EXPORTER MARKET SHARE",
        "value": f"{top_exp['country_name']} ({top_exp['global_market_share_percent']:.1f}%)" if top_exp is not None else "Saudi Arabia",
        "note": f"{top_exp['total_export_quantity']:,.0f} bpd" if top_exp is not None else ""
    },
    {
        "label": "LEADING IMPORTER MARKET SHARE",
        "value": f"{top_imp['country_name']} ({top_imp['global_import_share_percent']:.1f}%)" if top_imp is not None else "China",
        "note": f"{top_imp['total_import_quantity']:,.0f} bpd" if top_imp is not None else ""
    },
    {
        "label": "TRADE ARCHITECTURE",
        "value": "BILATERAL CORRIDORS",
        "note": "UN Comtrade • EIA Movements"
    }
])

st.write("")

# 4. Bilateral Trade Corridors Map (Copper & Amber Arcs)
render_html('<div class="atlas-section-title">PETROLEUM ARTERY RADAR — BILATERAL SEABORNE CORRIDORS</div>')
flows_df = PetroleumTradeAnalytics.get_bilateral_trade_flows(product_cat, reporting_period)

if not flows_df.empty:
    fig_flow_map = go.Figure()

    for _, row in flows_df.iterrows():
        if pd.notnull(row["exp_lat"]) and pd.notnull(row["imp_lat"]):
            # Calculate arc curve midpoint
            mid_lat = (row["exp_lat"] + row["imp_lat"]) / 2.0 + 4.0
            mid_lon = (row["exp_lon"] + row["imp_lon"]) / 2.0
            
            # Flow width based on volume
            line_width = max(1.8, min(7.5, row["quantity"] / 350000.0))
            
            # Color: Oxidized copper for primary flows, Amber for top tier
            arc_color = COLOR_AMBER if row["quantity"] >= 1500000 else COLOR_COPPER

            fig_flow_map.add_trace(go.Scattergeo(
                lat=[row["exp_lat"], mid_lat, row["imp_lat"]],
                lon=[row["exp_lon"], mid_lon, row["imp_lon"]],
                mode="lines",
                line=dict(width=line_width, color=arc_color),
                opacity=0.82,
                name=f"{row['exporter_name']} ➔ {row['importer_name']}",
                hoverinfo="text",
                text=(
                    f"<b>CORRIDOR:</b> {row['exporter_name']} ➔ {row['importer_name']}<br>"
                    f"<b>COMMODITY:</b> {product_cat.replace('_', ' ').title()}<br>"
                    f"<b>VOLUME:</b> {row['quantity']:,.0f} bpd<br>"
                    f"<b>VALUATION:</b> ${row['value_usd']:,.0f} USD<br>"
                    f"<b>PROVENANCE:</b> {row['source_id']}"
                )
            ))

            # Exporter origin node
            fig_flow_map.add_trace(go.Scattergeo(
                lat=[row["exp_lat"]],
                lon=[row["exp_lon"]],
                mode="markers",
                marker=dict(size=6, color=COLOR_AMBER, symbol="circle"),
                hoverinfo="none",
                showlegend=False
            ))
            # Importer destination node
            fig_flow_map.add_trace(go.Scattergeo(
                lat=[row["imp_lat"]],
                lon=[row["imp_lon"]],
                mode="markers",
                marker=dict(size=6, color=COLOR_TEAL, symbol="square"),
                hoverinfo="none",
                showlegend=False
            ))

    fig_flow_map.update_geos(
        showcoastlines=True,
        coastlinecolor=COLOR_INK,
        showland=True,
        landcolor="#EFEAD9",
        showocean=True,
        oceancolor=COLOR_WHITE,
        showcountries=True,
        countrycolor="#D9D4C8",
        countrywidth=0.8,
        projection_type="natural earth",
        framecolor=COLOR_INK,
        framewidth=1.5
    )

    apply_clean_layout(
        fig_flow_map,
        height=520,
        margin_l=15,
        margin_b=20,
        showlegend=False
    )
    st.plotly_chart(fig_flow_map, width="stretch", theme=None)
else:
    st.info("No bilateral observations recorded for selected category.")

st.write("")

# 5. Leaderboards & Country Deep-Dive
tab_lead, tab_dossier = st.tabs(["🏆 COMMODITY LEADERBOARDS", "🔍 SOVEREIGN TRADE DOSSIER & HHI CONCENTRATION"])

with tab_lead:
    render_html('<div class="atlas-section-title">GLOBAL EXPORT & IMPORT MATRIX</div>')
    lead_c1, lead_c2 = st.columns(2)

    with lead_c1:
        st.markdown(f"#### 🚢 Top Exporters: {product_cat.replace('_', ' ').title()}")
        if not all_exporters.empty:
            metric_col = "total_export_quantity" if trade_metric_view == "Volume (bpd)" else "total_export_value_usd"
            label_col = "Volume (bpd)" if trade_metric_view == "Volume (bpd)" else "Customs Value (USD)"
            fig_exp = px.bar(
                all_exporters.head(12),
                x=metric_col,
                y="country_name",
                orientation="h",
                color="global_market_share_percent",
                color_continuous_scale=[[0.0, "#E8E4D8"], [1.0, COLOR_AMBER]],
                labels={metric_col: label_col, "country_name": "Exporter"}
            )
            fig_exp.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.2)))
            apply_clean_layout(
                fig_exp,
                height=480,
                margin_l=130,
                showlegend=False,
                coloraxis_showscale=False,
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig_exp, width="stretch", theme=None)

    with lead_c2:
        st.markdown(f"#### 📥 Top Importers: {product_cat.replace('_', ' ').title()}")
        if not all_importers.empty:
            metric_col_i = "total_import_quantity" if trade_metric_view == "Volume (bpd)" else "total_import_value_usd"
            label_col_i = "Volume (bpd)" if trade_metric_view == "Volume (bpd)" else "Customs Value (USD)"
            fig_imp = px.bar(
                all_importers.head(12),
                x=metric_col_i,
                y="country_name",
                orientation="h",
                color="global_import_share_percent",
                color_continuous_scale=[[0.0, "#E8E4D8"], [1.0, "#2B6CB0"]],
                labels={metric_col_i: label_col_i, "country_name": "Importer"}
            )
            fig_imp.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.2)))
            apply_clean_layout(
                fig_imp,
                height=480,
                margin_l=130,
                showlegend=False,
                coloraxis_showscale=False,
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig_imp, width="stretch", theme=None)

with tab_dossier:
    render_html(f'<div class="atlas-section-title">SOVEREIGN TRADE DOSSIER: {selected_country.upper()}</div>')
    target_iso = normalize_country_iso3(selected_country)
    hhi_info = PetroleumTradeAnalytics.calculate_supplier_concentration_hhi(target_iso, product_cat, reporting_period)

    dos_c1, dos_c2 = st.columns([5, 7])
    with dos_c1:
        render_instrument_card(
            label="HHI CONCENTRATION SCORE",
            value=f"{hhi_info['hhi_score']:.1f}",
            accent="red" if hhi_info['hhi_score'] > 2500 else ("amber" if hhi_info['hhi_score'] >= 1500 else "teal"),
            subtext=f"Tier: {hhi_info['risk_tier']}",
            code_badge=target_iso
        )
        st.write("")
        st.markdown(f"**Supplier Fragmentation ({hhi_info['supplier_count']} Identified Suppliers):**")
        if hhi_info["suppliers"]:
            sup_df = pd.DataFrame(hhi_info["suppliers"])
            fig_donut = px.pie(
                sup_df,
                names="exporter_name",
                values="quantity",
                hole=0.55,
                color_discrete_sequence=[COLOR_AMBER, COLOR_COPPER, COLOR_TEAL, "#2B6CB0", "#C53030"]
            )
            fig_donut.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.5)))
            apply_clean_layout(
                fig_donut,
                height=450,
                is_pie=True,
                showlegend=True,
                legend_below=True
            )
            st.plotly_chart(fig_donut, width="stretch", theme=None)
        else:
            st.info("No bilateral supplier records available for this sovereign entity.")

    with dos_c2:
        exp_vol = all_exporters[all_exporters["exporter_iso3"] == target_iso]["total_export_quantity"].sum() if not all_exporters.empty else 0
        imp_vol = all_importers[all_importers["importer_iso3"] == target_iso]["total_import_quantity"].sum() if not all_importers.empty else 0
        net_pos = exp_vol - imp_vol

        render_instrument_card(
            label="NET STRATEGIC TRADE BALANCE",
            value=f"{net_pos:+,.0f} bpd",
            accent="teal" if net_pos > 0 else "red",
            subtext="Net Exporter" if net_pos > 0 else ("Net Importer" if net_pos < 0 else "Balanced"),
            code_badge="BAL"
        )
        st.write("")
        render_html(
            f"""
            <div style="background: rgba(14, 21, 38, 0.75); backdrop-filter: blur(14px); border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3); padding: 14px; border-radius: 6px; font-family: 'Space Grotesk', sans-serif; font-size: 0.85rem; line-height: 1.8; color: #F9FAFB;">
                <div><b>GROSS EXPORTS:</b> <span>{exp_vol:,.0f} bpd</span></div>
                <div><b>GROSS IMPORTS:</b> <span>{imp_vol:,.0f} bpd</span></div>
                <div><b>COMMODITY CATEGORY:</b> <span style="background: rgba(245, 185, 66, 0.2); color: #F5B942; padding: 2px 8px; border-radius: 4px; border: 1px solid rgba(245, 185, 66, 0.4); font-weight: 700;">{product_cat.upper()}</span></div>
                <div><b>REPORTING CADENCE:</b> <span>ANNUAL CUSTOMS (UN COMTRADE)</span></div>
            </div>
            """
        )

st.write("")

# 6. Customs Flow Audit Table
render_html('<div class="atlas-section-title">SEABORNE LOGISTICS OBSERVATIONS & PROVENANCE TABLE</div>')
if not flows_df.empty:
    display_flows = flows_df[[
        "exporter_name", "importer_name", "quantity", "quantity_unit", "value_usd", "source_id"
    ]].rename(columns={
        "exporter_name": "Sovereign Exporter", "importer_name": "Sovereign Importer",
        "quantity": "Volume (bpd)", "quantity_unit": "Unit", "value_usd": "Customs Value (USD)", "source_id": "Data Source"
    })
    st.dataframe(display_flows, width="stretch", hide_index=True)
    render_csv_download(display_flows, f"atlas_trade_flows_{product_cat}_{reporting_period}.csv")
