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
from src.localization.i18n import t, get_current_language


def render_how_it_works_view(navigate_fn=None):
    """Renders the comprehensive Architecture and Technical Blueprint."""
    cur_lang = get_current_language()

    render_html(f"""
    <div style="background: radial-gradient(circle at 10% 20%, rgba(16, 185, 129, 0.12) 0%, rgba(14, 21, 38, 0.95) 70%), #070A12; border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 12px; padding: 26px 30px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
            <div>
                {get_fuel_client_logo_html()}
                <h1 style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 2rem; font-weight: 800; color: #F9FAFB; margin: 6px 0 8px 0; letter-spacing: -0.02em;">
                    {t('how_hero_title', cur_lang)}
                </h1>
                <p style="font-family: 'Inter', sans-serif; font-size: 1rem; color: #94A3B8; margin: 0; max-width: 820px; line-height: 1.55;">
                    {t('how_hero_sub', cur_lang)}
                </p>
            </div>
        </div>
    </div>
    """)

    # 1. The 6-Stage End-to-End Pipeline
    st.markdown(f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 12px;">
        {t('how_sec1_title', cur_lang)}
    </div>
    """, unsafe_allow_html=True)

    stages = [
        ("01", t("how_stage_01_title", cur_lang), "#F5B942",
         t("how_stage_01_desc", cur_lang)),
        ("02", t("how_stage_02_title", cur_lang), "#60A5FA",
         t("how_stage_02_desc", cur_lang)),
        ("03", t("how_stage_03_title", cur_lang), "#34D399",
         t("how_stage_03_desc", cur_lang)),
        ("04", t("how_stage_04_title", cur_lang), "#F472B6",
         t("how_stage_04_desc", cur_lang)),
        ("05", t("how_stage_05_title", cur_lang), "#A78BFA",
         t("how_stage_05_desc", cur_lang)),
        ("06", t("how_stage_06_title", cur_lang), "#F87171",
         t("how_stage_06_desc", cur_lang))
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
    st.markdown(f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 12px;">
        {t('how_sec2_title', cur_lang)}
    </div>
    """, unsafe_allow_html=True)

    render_html('<div class="fuelpulse-suite-container">')
    c1, c2, c3 = st.columns(3)

    with c1:
        render_html(f"""
        <div style="background: rgba(14, 21, 38, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 16px; height: 100%;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.78rem; font-weight: 800; color: #F5B942; margin-bottom: 6px;">{t('how_tech_core_title', cur_lang)}</div>
            <ul style="font-family: 'Inter', sans-serif; font-size: 0.83rem; line-height: 1.6; color: #94A3B8; margin: 0; padding-left: 18px;">
                <li><b style="color: #F9FAFB;">Python 3.12+</b> (Async & Typing)</li>
                <li><b style="color: #F9FAFB;">SQLAlchemy 2.0</b> (Unified ORM)</li>
                <li><b style="color: #F9FAFB;">SQLite 3 / MySQL 8.0</b> (Dual Engine)</li>
                <li><b style="color: #F9FAFB;">Pandas 2.2 & NumPy 2.0</b> (Vector Math)</li>
            </ul>
        </div>
        """)

    with c2:
        render_html(f"""
        <div style="background: rgba(14, 21, 38, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 16px; height: 100%;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.78rem; font-weight: 800; color: #60A5FA; margin-bottom: 6px;">{t('how_tech_analytics_title', cur_lang)}</div>
            <ul style="font-family: 'Inter', sans-serif; font-size: 0.83rem; line-height: 1.6; color: #94A3B8; margin: 0; padding-left: 18px;">
                <li><b style="color: #F9FAFB;">Statsmodels</b> (SARIMAX Time-Series)</li>
                <li><b style="color: #F9FAFB;">Scikit-learn & XGBoost</b> (Regression)</li>
                <li><b style="color: #F9FAFB;">Google Gemini 1.5 Pro/Flash</b> (LLM Query)</li>
                <li><b style="color: #F9FAFB;">Prophet</b> (Seasonal Trend Modeling)</li>
            </ul>
        </div>
        """)

    with c3:
        render_html(f"""
        <div style="background: rgba(14, 21, 38, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 16px; height: 100%;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.78rem; font-weight: 800; color: #34D399; margin-bottom: 6px;">{t('how_tech_frontend_title', cur_lang)}</div>
            <ul style="font-family: 'Inter', sans-serif; font-size: 0.83rem; line-height: 1.6; color: #94A3B8; margin: 0; padding-left: 18px;">
                <li><b style="color: #F9FAFB;">Streamlit 1.40+</b> (Websocket Compr.)</li>
                <li><b style="color: #F9FAFB;">Plotly 5.24</b> (GPU WebGL Graphics)</li>
                <li><b style="color: #F9FAFB;">Pytest 9.0+</b> (85 Automated Tests)</li>
                <li><b style="color: #F9FAFB;">AppTest</b> (Headless UI Assurance)</li>
            </ul>
        </div>
        """)
    render_html('</div>')

    st.write("")

    # 3. Ingestion Orchestrator & Concurrency Safeguard
    st.markdown(f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 12px;">
        {t('how_sec3_title', cur_lang)}
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
