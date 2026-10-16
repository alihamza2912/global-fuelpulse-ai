"""
GLOBAL FUELPULSE AI — HOW IT WORKS & ARCHITECTURE VIEW
Detailed architectural breakdown of the 6-stage data lifecycle,
technology stack specifications, and pipeline orchestration.
"""

import streamlit as st
from src.ui_components import (
    render_html,
    render_instrument_card,
    get_fuel_client_logo_html,
    COLOR_AMBER,
    COLOR_WHITE,
    COLOR_INK,
    COLOR_GRAY_MUTED
)


def render_how_it_works_view(navigate_fn=None):
    """Renders the comprehensive Architecture and Technical Blueprint."""

    render_html(f"""
    <div style="background: radial-gradient(circle at 10% 20%, rgba(16, 185, 129, 0.12) 0%, rgba(14, 21, 38, 0.95) 70%), #070A12; border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 12px; padding: 26px 30px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
            <div>
                {get_fuel_client_logo_html()}
                <h1 style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 2rem; font-weight: 800; color: #F9FAFB; margin: 6px 0 8px 0; letter-spacing: -0.02em;">
                    How It Works & System Architecture
                </h1>
                <p style="font-family: 'Inter', sans-serif; font-size: 1rem; color: #94A3B8; margin: 0; max-width: 820px; line-height: 1.55;">
                    The 6-stage data engineering lifecycle, deterministic validation rules, caching hierarchy, and production technology stack.
                </p>
            </div>
        </div>
    </div>
    """)

    # 1. The 6-Stage End-to-End Pipeline
    st.markdown("""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 12px;">
        1. THE 6-STAGE DATA PIPELINE
    </div>
    """, unsafe_allow_html=True)

    stages = [
        ("01", "INGESTION & CONNECTOR POOL", "#F5B942",
         "Automated ETL connectors poll registered APIs and published bulletins: US EIA (crude spot benchmarks, inventory stocks), India PPAC (metro pump prices, Indian Crude Basket), European Commission Oil Bulletin (weekly EU member prices), and Open Exchange Rates (live daily FX conversions)."),
        ("02", "SCHEMA VALIDATION & ISOLATION", "#60A5FA",
         "Strict domain integrity checks enforce boundary constraints (e.g. retail price between $0.10 and $4.50/L, non-negative refinery volumes, valid ISO-3 country codes). Anomalous or corrupted records are isolated into a quarantine log rather than polluting reporting tables."),
        ("03", "RELATIONAL MODELING & STORAGE", "#34D399",
         "Data is stored in high-performance relational tables adhering to star schema principles: dimension tables (`dim_country`, `dim_location`, `data_sources`) and partitioned fact tables (`fuel_prices`, `fact_energy_indicator`, `petroleum_trade_flows`, `etl_run_log`). Supports both embedded SQLite and enterprise MySQL."),
        ("04", "ANALYTICAL & ML COMPUTATION", "#F472B6",
         "Vectorized analytical engines calculate real-time indicators: the Herfindahl-Hirschman Index (HHI) for maritime chokepoints, currency pass-through regressions, affordability burdens against GDP per capita, and multi-horizon SARIMAX / XGBoost retail price forecasts."),
        ("05", "MULTI-TIER CACHING HIERARCHY", "#A78BFA",
         "A tiered caching engine with automatic TTL invalidation guarantees sub-50ms user responsiveness. Heavy TopoJSON geographic scatter layers, SQL aggregates, and ML model instances are kept warm in memory, preventing redundant recomputations on UI reruns."),
        ("06", "PRESENTATION & EXPORT INTERFACES", "#F87171",
         "Visual rendering is handled via Streamlit 1.40+ and Plotly, styled in an Editorial Dark design language. Interactive controls support instant drill-downs, CSV data exports, and direct integration with corporate Power BI reporting pipelines.")
    ]

    for num, title, color, desc in stages:
        render_html(f"""
        <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-left: 4px solid {color}; border-radius: 6px; padding: 14px 18px; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; font-weight: 800; color: {color};">{num} //</span>
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.95rem; font-weight: 800; color: #F9FAFB;">{title}</span>
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.85rem; line-height: 1.5; color: #94A3B8;">
                {desc}
            </div>
        </div>
        """)

    st.write("")

    # 2. Production Technology Stack
    st.markdown("""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 12px;">
        2. VERIFIED PRODUCTION TECHNOLOGY STACK
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        render_html("""
        <div style="background: rgba(14, 21, 38, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 16px; height: 100%;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.78rem; font-weight: 800; color: #F5B942; margin-bottom: 6px;">CORE & DATABASE</div>
            <ul style="font-family: 'Inter', sans-serif; font-size: 0.83rem; line-height: 1.6; color: #94A3B8; margin: 0; padding-left: 18px;">
                <li><b style="color: #F9FAFB;">Python 3.12+</b> (Async & Typing)</li>
                <li><b style="color: #F9FAFB;">SQLAlchemy 2.0</b> (Unified ORM)</li>
                <li><b style="color: #F9FAFB;">SQLite 3 / MySQL 8.0</b> (Dual Engine)</li>
                <li><b style="color: #F9FAFB;">Pandas 2.2 & NumPy 2.0</b> (Vector Math)</li>
            </ul>
        </div>
        """)

    with c2:
        render_html("""
        <div style="background: rgba(14, 21, 38, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 16px; height: 100%;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.78rem; font-weight: 800; color: #60A5FA; margin-bottom: 6px;">ANALYTICS & ML</div>
            <ul style="font-family: 'Inter', sans-serif; font-size: 0.83rem; line-height: 1.6; color: #94A3B8; margin: 0; padding-left: 18px;">
                <li><b style="color: #F9FAFB;">Statsmodels</b> (SARIMAX Time-Series)</li>
                <li><b style="color: #F9FAFB;">Scikit-learn & XGBoost</b> (Regression)</li>
                <li><b style="color: #F9FAFB;">Google Gemini 1.5 Pro/Flash</b> (LLM Query)</li>
                <li><b style="color: #F9FAFB;">Prophet</b> (Seasonal Trend Modeling)</li>
            </ul>
        </div>
        """)

    with c3:
        render_html("""
        <div style="background: rgba(14, 21, 38, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 16px; height: 100%;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.78rem; font-weight: 800; color: #34D399; margin-bottom: 6px;">FRONTEND & TESTING</div>
            <ul style="font-family: 'Inter', sans-serif; font-size: 0.83rem; line-height: 1.6; color: #94A3B8; margin: 0; padding-left: 18px;">
                <li><b style="color: #F9FAFB;">Streamlit 1.40+</b> (Websocket Compr.)</li>
                <li><b style="color: #F9FAFB;">Plotly 5.24</b> (GPU WebGL Graphics)</li>
                <li><b style="color: #F9FAFB;">Pytest 9.0+</b> (39 Automated Tests)</li>
                <li><b style="color: #F9FAFB;">AppTest</b> (Headless UI Assurance)</li>
            </ul>
        </div>
        """)

    st.write("")

    # 3. Ingestion Orchestrator & Concurrency Safeguard
    st.markdown("""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 12px;">
        3. PIPELINE ORCHESTRATION & THREAD SAFETY
    </div>
    """, unsafe_allow_html=True)

    render_html("""
    <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 20px; font-family: 'Inter', sans-serif; font-size: 0.88rem; line-height: 1.6; color: #94A3B8;">
        <p style="margin-top: 0;">
            The central <code>PipelineOrchestrator</code> utilizes a non-blocking mutex lock (<code>threading.Lock()</code>). When a user clicks <b>⚡ Refresh Live Data</b> or an automated scheduler trigger fires, the pipeline verifies whether another sync process is already active. If active, concurrent duplicate executions are gracefully refused, preventing database write-lock contention and redundant API quota consumption.
        </p>
        <p style="margin-bottom: 0;">
            Every ingestion step records execution telemetry into <code>etl_run_log</code>: connector name, start timestamp, completion duration (milliseconds), row count fetched, row count committed, and error exceptions (if any). This telemetry is openly displayed in the <b>Data Trust Center</b> for full operational transparency.
        </p>
    </div>
    """)
