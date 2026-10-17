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
    st.markdown("""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 8px;">
        1. FREQUENTLY ASKED QUESTIONS (FAQ)
    </div>
    """, unsafe_allow_html=True)

    faqs = [
        ("01. Where does Global FuelPulse AI source its data?",
         "All datasets are ingested directly from official public institutions and governmental regulatory bodies: the U.S. Energy Information Administration (US EIA), the Petroleum Planning & Analysis Cell (PPAC) under the Indian Ministry of Petroleum & Natural Gas, the European Commission DG Energy Oil Bulletin, the United Nations Statistics Division (UN Comtrade), and Open Exchange Rates. We do not use hallucinated mock data or unverified third-party scrapers."),

        ("02. Why do petrol and diesel prices differ so widely between Indian cities?",
         "While the base price (refinery transfer price) and Central Excise Duty are identical nationwide, retail selling prices diverge due to state-specific Value Added Tax (VAT) rates (e.g. ~19.4% in Delhi vs ~25% in Maharashtra), local municipal entry cesses, and inland freight costs from the nearest bulk oil terminal depot."),

        ("03. How often are fuel prices and exchange rates refreshed?",
         "PPAC daily metro retail prices and Open Exchange Rates currency rates are polled daily. U.S. EIA crude inventories and European Commission member fuel prices are refreshed weekly on their official release days. Global bilateral trade flows (UN Comtrade) are updated annually."),

        ("04. Does the platform track private petrol pumps like Nayara, Jio-bp, and Shell?",
         "Yes. Public sector OMCs (IndianOil, BPCL, HPCL) account for ~89% of the retail pump footprint and operate under uniform pricing per municipal territory. Private retailers (Nayara, Reliance BP Mobility / Jio-bp, Shell India) account for ~11% and maintain pricing freedom; in major cities they price at OMC benchmark parity, while on highway corridors they may offer additive-differentiated fuels or slight discounts."),

        ("05. What is the Indian Crude Basket and how is it constructed?",
         "The Indian Crude Basket represents the weighted average cost of crude oil imported by Indian refiners. It is computed by PPAC with an official composition: approximately 75.6% Oman-Dubai sour grade and 24.4% Brent sweet grade."),

        ("06. How does the Macroeconomic Shock Simulator calculate fleet costs?",
         "The simulator utilizes empirical short-run pass-through elasticities (approximately 0.72 for crude spot movements and 0.85 for foreign exchange fluctuations against the USD). These coefficients are applied to baseline retail prices and multiplied by the monthly fleet consumption volume input by the user."),

        ("07. How are retail fuel price forecasts generated?",
         "We deploy Seasonal Auto-Regressive Integrated Moving Average (SARIMAX) models with Brent crude spot price lags as exogenous regressors, alongside XGBoost and Prophet models. All models undergo rolling-origin out-of-sample backtesting against holdout validation sets, tracking MAE, RMSE, and MAPE."),

        ("08. Can I export data for Microsoft Excel or Power BI?",
         "Yes. Every analytical table and chart includes one-click CSV export buttons. Furthermore, the platform automatically generates `.pbids` enterprise connection files for native one-click integration with Microsoft Power BI Desktop."),

        ("09. Why is the AI Energy Analyst quota-gated?",
         "The AI Energy Analyst uses Google Gemini with an in-memory TTL cache and strict quota budgeting. This guarantees sub-second response times for frequently requested queries while protecting against runaway API token consumption."),

        ("10. How can I contribute or report a data discrepancy?",
         "Global FuelPulse AI is open-source. You can submit pull requests, report data discrepancies, or request new data connector integrations via the official GitHub repository at `https://github.com/alihamza2912/global-fuelpulse-ai`.")
    ]

    for q, a in faqs:
        with st.expander(f"**{q}**"):
            st.markdown(f"<div style='font-family: Inter, sans-serif; font-size: 0.88rem; line-height: 1.6; color: #94A3B8;'>{a}</div>", unsafe_allow_html=True)

    st.write("")

    # 2. Developer Quickstart & Environment Reference
    st.markdown("""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 8px;">
        2. DEVELOPER QUICKSTART & ENVIRONMENT REFERENCE
    </div>
    """, unsafe_allow_html=True)

    render_html("""
    <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 20px; font-family: 'Inter', sans-serif; font-size: 0.88rem; line-height: 1.6; color: #94A3B8;">
        <p style="margin-top: 0;"><b style="color: #F9FAFB;">Local Setup in 3 Commands:</b></p>
        <pre style="background: #070A12; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 6px; padding: 12px; color: #F5B942; font-family: 'Courier New', monospace; font-size: 0.82rem; overflow-x: auto;">
git clone https://github.com/alihamza2912/global-fuelpulse-ai.git
cd global-fuelpulse-ai
pip install -r requirements.txt
streamlit run app.py</pre>

        <p><b style="color: #F9FAFB;">Running Automated Tests:</b></p>
        <pre style="background: #070A12; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 6px; padding: 12px; color: #34D399; font-family: 'Courier New', monospace; font-size: 0.82rem; overflow-x: auto;">
PYTHONPATH=. pytest tests/ -v</pre>

        <p><b style="color: #F9FAFB;">Environment Variables (<code>.env</code>):</b></p>
        <ul style="margin: 0; padding-left: 20px;">
            <li><code>DATABASE_URL</code>: SQLite (<code>sqlite:///fuelx_local.db</code>) or MySQL (<code>mysql+pymysql://user:pass@host/fuelx_db</code>)</li>
            <li><code>GEMINI_API_KEY</code>: Optional Google AI Studio key for AI Analyst</li>
            <li><code>EIA_API_KEY</code>: Optional U.S. EIA API v2 access key</li>
            <li><code>STREAMLIT_SERVER_PORT</code>: Port to bind (default 8501)</li>
        </ul>
    </div>
    """)
