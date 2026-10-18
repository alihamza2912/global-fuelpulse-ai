"""
GLOBAL FUELPULSE AI — FAQ & DEVELOPER GUIDE VIEW
Comprehensive answers to key energy market questions, technical troubleshooting,
and local developer setup instructions.
"""

import streamlit as st
from src.ui_components import (
    render_html,
    get_fuel_client_logo_html,
    COLOR_AMBER,
    COLOR_WHITE,
    COLOR_INK,
    COLOR_GRAY_MUTED
)
from src.localization.i18n import t, get_current_language


def render_faq_view(navigate_fn=None):
    """Renders the comprehensive Documentation, Developer Guide, and FAQ."""
    cur_lang = get_current_language()

    render_html(f"""
    <div style="background: radial-gradient(circle at 10% 20%, rgba(244, 63, 94, 0.12) 0%, rgba(14, 21, 38, 0.95) 70%), #070A12; border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 12px; padding: 26px 30px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
            <div>
                {get_fuel_client_logo_html()}
                <h1 style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 2rem; font-weight: 800; color: #F9FAFB; margin: 6px 0 8px 0; letter-spacing: -0.02em;">
                    {t('faq_hero_title', cur_lang)}
                </h1>
                <p style="font-family: 'Inter', sans-serif; font-size: 1rem; color: #94A3B8; margin: 0; max-width: 820px; line-height: 1.55;">
                    {t('faq_hero_sub', cur_lang)}
                </p>
            </div>
        </div>
    </div>
    """)

    # 1. 10 Essential Frequently Asked Questions
    st.markdown(f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 8px;">
        {t('faq_sec1_title', cur_lang)}
    </div>
    """, unsafe_allow_html=True)

    faqs = [
        (t("faq_q01", cur_lang), t("faq_a01", cur_lang)),
        (t("faq_q02", cur_lang), t("faq_a02", cur_lang)),
        (t("faq_q03", cur_lang), t("faq_a03", cur_lang)),
        (t("faq_q04", cur_lang), t("faq_a04", cur_lang)),
        (t("faq_q05", cur_lang), t("faq_a05", cur_lang)),
        (t("faq_q06", cur_lang), t("faq_a06", cur_lang)),
        (t("faq_q07", cur_lang), t("faq_a07", cur_lang)),
        (t("faq_q08", cur_lang), t("faq_a08", cur_lang)),
        (t("faq_q09", cur_lang), t("faq_a09", cur_lang)),
        (t("faq_q10", cur_lang), t("faq_a10", cur_lang)),
    ]

    for q, a in faqs:
        with st.expander(f"**{q}**"):
            st.markdown(f"<div style='font-family: Inter, sans-serif; font-size: 0.88rem; line-height: 1.6; color: #94A3B8;'>{a}</div>", unsafe_allow_html=True)

    st.write("")

    # 2. Developer Quickstart & Environment Reference
    st.markdown(f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 8px;">
        {t('faq_sec2_title', cur_lang)}
    </div>
    """, unsafe_allow_html=True)

    render_html(f"""
    <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 20px; font-family: 'Inter', sans-serif; font-size: 0.88rem; line-height: 1.6; color: #94A3B8;">
        <p style="margin-top: 0;"><b style="color: #F9FAFB;">{t('faq_local_setup', cur_lang)}</b></p>
        <pre style="background: #070A12; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 6px; padding: 12px; color: #F5B942; font-family: 'Courier New', monospace; font-size: 0.82rem; overflow-x: auto;">
git clone https://github.com/alihamza2912/global-fuelpulse-ai.git
cd global-fuelpulse-ai
pip install -r requirements.txt
streamlit run app.py</pre>

        <p><b style="color: #F9FAFB;">{t('faq_run_tests', cur_lang)}</b></p>
        <pre style="background: #070A12; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 6px; padding: 12px; color: #34D399; font-family: 'Courier New', monospace; font-size: 0.82rem; overflow-x: auto;">
PYTHONPATH=. pytest tests/ -v</pre>

        <p><b style="color: #F9FAFB;">{t('faq_env_vars', cur_lang)}</b></p>
        <ul style="margin: 0; padding-left: 20px;">
            <li><code>DATABASE_URL</code>: SQLite (<code>sqlite:///fuelx_local.db</code>) or MySQL (<code>mysql+pymysql://user:pass@host/fuelx_db</code>)</li>
            <li><code>GEMINI_API_KEY</code>: Optional Google AI Studio key for AI Analyst</li>
            <li><code>EIA_API_KEY</code>: Optional U.S. EIA API v2 access key</li>
            <li><code>STREAMLIT_SERVER_PORT</code>: Port to bind (default 8501)</li>
        </ul>
    </div>
    """)

