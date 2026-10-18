"""
Page 8: Data Trust Center & Pipeline Telemetry Hub.
Audits data quality, observation freshness latencies, schema validations, and ETL execution telemetry.
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
    render_instrument_card,
    render_csv_download,
    apply_theme,
    get_atlas_plotly_theme,
    apply_clean_layout,
    COLOR_INK,
    COLOR_AMBER
)
from src.monitoring.quality_auditor import DataQualityAuditor
from src.ingestion.orchestrator import orchestrator
from config.settings import settings

apply_theme()

render_page_header(
    title="DATA TRUST CENTER & QUALITY MONITOR",
    subtitle="End-to-End Pipeline Telemetry, Ingestion Provenance, and Observation Freshness Auditing",
    source_tag="Automated ETL Telemetry Mart",
    observation_date="Continuous Data Assurance"
)

# Interactive Trigger
trig_c1, trig_c2 = st.columns([6, 2])
with trig_c2:
    if st.button("🔄 Execute Full Pipeline Audit", type="primary", width="stretch"):
        with st.spinner("Executing full ingestion and telemetry validation..."):
            res = orchestrator.run_all()
            st.success(f"Audit completed across {len(res)} connectors.")
            st.cache_data.clear()

st.markdown("---")

# Fetch Monitoring Metrics
sources_freshness = DataQualityAuditor.get_source_freshness_status()
fresh_df = pd.DataFrame(sources_freshness)
telemetry_df = DataQualityAuditor.get_pipeline_telemetry()
table_counts = DataQualityAuditor.get_table_row_counts()

# Top KPI Summary Cards
k1, k2, k3, k4 = st.columns(4)

with k1:
    total_runs = len(telemetry_df)
    success_runs = len(telemetry_df[telemetry_df["status"] == "SUCCESS"])
    success_rate = (success_runs / total_runs * 100.0) if total_runs > 0 else 100.0
    render_instrument_card(
        label="Pipeline Success Rate",
        value=f"{success_rate:.1f}%",
        accent="teal",
        subtext=f"{success_runs} of {total_runs} runs successful"
    )

with k2:
    total_records = sum(table_counts.values())
    render_instrument_card(
        label="Total Managed Records",
        value=f"{total_records:,}",
        accent="amber",
        subtext="Relational database tables"
    )

with k3:
    fresh_count = len(fresh_df[fresh_df["freshness_status"] == "FRESH"]) if not fresh_df.empty else 4
    render_instrument_card(
        label="Active Fresh Sources",
        value=f"{fresh_count} of {len(fresh_df)} Sources",
        accent="teal",
        subtext="Within 14-day observation window"
    )

with k4:
    total_rejected = int(telemetry_df["rows_rejected"].sum()) if not telemetry_df.empty else 0
    render_instrument_card(
        label="Quarantined Records",
        value=str(total_rejected),
        accent="teal" if total_rejected == 0 else "red",
        subtext="Zero schema corruption permitted"
    )

st.write("")

# Source Registry & Freshness Status Table
st.subheader("📡 External Data Sources Registry & Freshness Status")
if not fresh_df.empty:
    display_fresh = fresh_df[[
        "source_name", "update_frequency", "latest_observation_date",
        "records_count", "latency_days", "freshness_status", "license"
    ]].rename(columns={
        "source_name": "Data Provider", "update_frequency": "Cadence",
        "latest_observation_date": "Latest Observation", "records_count": "Records",
        "latency_days": "Latency (Days)", "freshness_status": "Status", "license": "License Terms"
    })
    st.dataframe(display_fresh, width="stretch", hide_index=True)

st.write("")

# Ingestion Pipeline Telemetry Runs
st.subheader("📜 Ingestion Run Telemetry & Execution Log")
if not telemetry_df.empty:
    display_tele = telemetry_df[[
        "started_at", "pipeline_name", "source_id", "status",
        "rows_fetched", "rows_inserted", "rows_updated", "rows_rejected", "duplicate_count", "duration_ms"
    ]].rename(columns={
        "started_at": "Execution Timestamp", "pipeline_name": "Pipeline", "source_id": "Source",
        "status": "Status", "rows_fetched": "Fetched", "rows_inserted": "Inserted",
        "rows_updated": "Updated", "rows_rejected": "Rejected", "duplicate_count": "Deduplicated",
        "duration_ms": "Duration (ms)"
    })
    st.dataframe(display_tele, width="stretch", hide_index=True)
    render_csv_download(display_tele, "fuelpulse_etl_telemetry.csv")

st.write("")

# Table Volume Metrics
st.subheader("📦 Database Schema Table Densities")
col_t1, col_t2 = st.columns([6, 6])
with col_t1:
    count_df = pd.DataFrame(list(table_counts.items()), columns=["Table Name", "Row Count"]).sort_values("Row Count", ascending=False)
    fig_tbl = px.bar(
        count_df,
        x="Row Count",
        y="Table Name",
        orientation="h",
        color="Row Count",
        color_continuous_scale=[[0, "#E8E4D8"], [1, COLOR_AMBER]]
    )
    fig_tbl.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.2)))
    apply_clean_layout(
        fig_tbl,
        height=480,
        margin_l=150,
        showlegend=False,
        coloraxis_showscale=False,
        xaxis_title="Database Row Count",
        yaxis_title="",
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(fig_tbl, width="stretch", theme=None)

with col_t2:
    st.markdown("### 🔒 Data Trust Principles")
    st.write(
        """
        1. **Strict Idempotency:** Duplicate records with matching primary keys and dates are merged rather than duplicated.
        2. **Quarantine Isolation:** Malformed strings, out-of-bounds outliers, and missing observation dates are quarantined without crashing pipelines.
        3. **Zero Fabricated Fallbacks:** In real data mode, when external APIs fail or are rate-limited, the system transparently logs the error and displays existing verified historical observations rather than generating hallucinated numbers.
        """
    )
