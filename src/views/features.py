"""
GLOBAL FUELPULSE AI — FEATURES CATALOG VIEW
Complete technical inventory of all 12 modules, their analytical models,
data requirements, and operational status.
"""

import streamlit as st
import pandas as pd
from src.ui_components import (
    render_html,
    get_fuel_client_logo_html,
    get_lucide_icon_svg,
    COLOR_AMBER,
    COLOR_WHITE,
    COLOR_INK,
    COLOR_GRAY_MUTED
)
from src.localization.i18n import t, get_current_language


def render_features_view(navigate_fn=None):
    """Renders the comprehensive Features & Analytical Capabilities Catalog."""
    cur_lang = get_current_language()

    render_html(f"""
    <div style="background: radial-gradient(circle at 10% 20%, rgba(245, 185, 66, 0.12) 0%, rgba(14, 21, 38, 0.95) 70%), #070A12; border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 12px; padding: 26px 30px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
            <div>
                {get_fuel_client_logo_html()}
                <h1 style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 2rem; font-weight: 800; color: #F9FAFB; margin: 6px 0 8px 0; letter-spacing: -0.02em;">
                    {t('features_hero_title', cur_lang)}
                </h1>
                <p style="font-family: 'Inter', sans-serif; font-size: 1rem; color: #94A3B8; margin: 0; max-width: 820px; line-height: 1.55;">
                    {t('features_hero_sub', cur_lang)}
                </p>
            </div>
        </div>
    </div>
    """)

    features = [
        {
            "id": "01",
            "name": "Global Crude Extraction Leaderboard",
            "category": "UPSTREAM INTELLIGENCE",
            "icon": "database",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Tracks daily and annual crude oil extraction volumes (in million barrels per day - mbpd) for the top 15 producing nations, contrasting OPEC vs Non-OPEC market power.",
            "why": "Identifies upstream market concentration and baseline global supply expansion or curtailment.",
            "data": "US EIA Table 11.1b, Official OPEC Annual Statistical Bulletins.",
            "action_text": "View in Dashboard Chapter 02",
            "nav_target": "Live Intelligence Dashboard"
        },
        {
            "id": "02",
            "name": "Bilateral Seaborne Trade Flow Matrix",
            "category": "MIDSTREAM LOGISTICS",
            "icon": "ship",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Origin-destination bilateral matrix capturing physical crude and product tanker flows between sovereign exporters and consuming hubs.",
            "why": "Reveals energy interdependence, export intensities, and sovereign trade surpluses/deficits.",
            "data": "UN Comtrade Petroleum Trade Mart (Harmonized System Codes 2709 & 2710).",
            "action_text": "View in Dashboard Chapter 03",
            "nav_target": "Live Intelligence Dashboard"
        },
        {
            "id": "03",
            "name": "International Retail Fuel Price Explorer",
            "category": "DOWNSTREAM PRICING",
            "icon": "fuel",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Multi-country comparative pricing for Regular Motor Gasoline (Petrol) and Automotive Gasoil (Diesel), harmonized into standardized USD per litre and local currencies.",
            "why": "Enables cross-border fleet routing, international price disparity tracking, and diesel-to-petrol ratio analysis.",
            "data": "US EIA, India PPAC, European Commission Oil Bulletin, Open Exchange Rates.",
            "action_text": "View in Dashboard Chapter 04",
            "nav_target": "Live Intelligence Dashboard"
        },
        {
            "id": "04",
            "name": "Price Build-Up & Tax Waterfall Analyzer",
            "category": "FISCAL DECOMPOSITION",
            "icon": "layers",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Decomposes consumer retail pump prices into upstream crude benchmark costs, refinery margin, central excise duty, dealer margin, and regional VAT.",
            "why": "Demystifies the exact sovereign tax wedge vs commodity cost within each litre of motor fuel.",
            "data": "Ministry of Petroleum & Natural Gas (MoPNG) Price Build-Up Circulars, PPAC.",
            "action_text": "View in India Fuel Center",
            "nav_target": "India Fuel Center"
        },
        {
            "id": "05",
            "name": "Energy Affordability Burden Index",
            "category": "SOCIOECONOMIC IMPACT",
            "icon": "activity",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Calculates the real economic burden of fuel by benchmarking a 50-litre tank against national GDP per capita and daily minimum wage levels.",
            "why": "Exposes why a $1.10/L fuel price in a developing nation represents a far greater economic burden than $1.85/L in a high-income nation.",
            "data": "World Bank Economic Indicators, ILO Minimum Wage Database.",
            "action_text": "View in Dashboard Chapter 06",
            "nav_target": "Live Intelligence Dashboard"
        },
        {
            "id": "06",
            "name": "Maritime Chokepoint & Supply Risk Radar",
            "category": "VULNERABILITY AUDITING",
            "icon": "shield-check",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Evaluates national dependency on high-risk maritime transit corridors (Strait of Hormuz, Malacca Strait, Suez/Red Sea) and calculates the Herfindahl-Hirschman Index (HHI).",
            "why": "Quantifies supply disruption vulnerability for nations heavily reliant on singular import routes.",
            "data": "Maritime transit throughput records, UN Comtrade bilateral import weights.",
            "action_text": "View in Dashboard Chapter 07",
            "nav_target": "Live Intelligence Dashboard"
        },
        {
            "id": "07",
            "name": "Macroeconomic Fuel Shock Simulator",
            "category": "DECISION SUPPORT & PLANNING",
            "icon": "zap",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Interactive sensitivity model allowing fleet managers and procurement leaders to simulate crude oil spikes (+$5 to +$50/bbl) and local currency depreciations (1% to 25%).",
            "why": "Accurately projects monthly fleet cost inflations and evaluates required fuel surcharge pass-through rates.",
            "data": "Empirical pass-through elasticities, user fleet size and monthly volume inputs.",
            "action_text": "View in Dashboard Chapter 08",
            "nav_target": "Live Intelligence Dashboard"
        },
        {
            "id": "08",
            "name": "SARIMAX & XGBoost Machine Learning Radar",
            "category": "PREDICTIVE MODELING",
            "icon": "sparkles",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Multi-horizon time-series forecasting engine generating 30-day and 90-day forward retail fuel price projections with 80% and 95% confidence intervals.",
            "why": "Provides quantitative forward price expectations incorporating seasonal demand patterns and crude spot lags.",
            "data": "Historical weekly fuel price time-series, Brent crude spot lag regressors.",
            "action_text": "View in Dashboard Chapter 10",
            "nav_target": "Live Intelligence Dashboard"
        },
        {
            "id": "09",
            "name": "AI Energy Market Analyst (LLM-Assisted)",
            "category": "SYNTHETIC REASONING",
            "icon": "bot",
            "status": "PRODUCTION / ACTIVE • 100% FREE AUTONOMOUS",
            "status_color": "#10B981",
            "what": "Natural-language query engine powered by Google Gemini and autonomous SQL synthesis, capable of translating plain-English questions into verified read-only SQL queries with zero quota limits and instant telemetry.",
            "why": "Allows executive stakeholders to extract instant answers without writing SQL queries or navigating multiple charts.",
            "data": "Full relational schema grounding, in-memory TTL query cache, MoPNG official circulars.",
            "action_text": "Open Full AI Analyst Studio",
            "nav_target": "AI_Analyst"
        },
        {
            "id": "10",
            "name": "India Metro Energy Center (PPAC Daily)",
            "category": "REGIONAL BENCHMARKING",
            "icon": "map-pinned",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Dedicated operational portal tracking verified daily retail pump prices for Delhi, Mumbai, Kolkata, and Chennai, plus Indian Crude Basket and OMC market shares.",
            "why": "Gives Indian fleet operators, shippers, and policy observers authoritative benchmark transparency.",
            "data": "Petroleum Planning & Analysis Cell (PPAC), MoPNG, IOCL/BPCL/HPCL public disclosures.",
            "action_text": "View India Fuel Center",
            "nav_target": "India Fuel Center"
        },
        {
            "id": "11",
            "name": "Automated Quality Auditor & Telemetry Mart",
            "category": "DATA GOVERNANCE",
            "icon": "shield-check",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Real-time auditing suite verifying observation latencies, data provenance, connector execution runtimes, and zero-tolerance quarantine logs.",
            "why": "Guarantees data integrity and alerts operators to stale feeds or upstream API format changes.",
            "data": "`etl_run_log` table, database schema inspection pragma.",
            "action_text": "View Data Trust Center",
            "nav_target": "Data Trust Center"
        },
        {
            "id": "12",
            "name": "Power BI & Multi-Format Data Export",
            "category": "ENTERPRISE INTEGRATION",
            "icon": "download",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Direct export capabilities for all underlying data marts in CSV format, alongside auto-generated Power BI `.pbids` enterprise connection files.",
            "why": "Allows enterprise teams to seamlessly ingest FuelPulse AI data directly into internal corporate BI dashboards.",
            "data": "Relational query exports across all database tables.",
            "action_text": "Export from Dashboard",
            "nav_target": "Live Intelligence Dashboard"
        }
    ]

    for f in features:
        icon_svg = get_lucide_icon_svg(f.get("icon", "sparkles"), size=18, color="#F5B942")
        render_html(f"""
        <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 20px; margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px; margin-bottom: 10px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    {icon_svg}
                    <div>
                        <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 800; color: #F5B942; letter-spacing: 0.06em;">FEATURE {f['id']} // {f['category']}</span>
                        <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; font-weight: 800; color: #F9FAFB; margin: 3px 0 0 0;">{f['name']}</h3>
                    </div>
                </div>
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem; font-weight: 800; color: {f['status_color']}; background: rgba(255, 255, 255, 0.05); border: 1px solid {f['status_color']}; padding: 3px 9px; border-radius: 999px;">
                    {f['status']}
                </span>
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.86rem; line-height: 1.55; color: #94A3B8; margin-bottom: 12px;">
                <p style="margin: 0 0 6px 0;"><b style="color: #F9FAFB;">What it does:</b> {f['what']}</p>
                <p style="margin: 0 0 6px 0;"><b style="color: #F9FAFB;">Why it matters:</b> {f['why']}</p>
                <p style="margin: 0;"><b style="color: #F9FAFB;">Input data sources:</b> {f['data']}</p>
            </div>
        </div>
        """)

        if f["id"] == "09":
            with st.container():
                render_html("""
                <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 8px; padding: 12px 16px; margin: -6px 0 14px 0;">
                    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 1.15rem;">🤖</span>
                            <b style="color: #34D399; font-family: 'Space Grotesk', sans-serif; font-size: 0.92rem;">Try Feature 09 Live Now — Free Autonomous Energy Intelligence</b>
                        </div>
                        <span style="background: rgba(16, 185, 129, 0.18); color: #34D399; font-size: 0.72rem; font-weight: 800; padding: 2px 8px; border-radius: 4px; border: 1px solid rgba(16, 185, 129, 0.4);">
                            🟢 3 FREE QUESTIONS/24H • ATTACH ANTIGRAVITY TOKEN FOR UNLIMITED
                        </span>
                    </div>
                    <p style="font-size: 0.78rem; color: #94A3B8; margin: 6px 0 0 0; line-height: 1.4;">
                        Select any suggested query chip below or ask any question to trigger autonomous SQL query synthesis and market analysis:
                    </p>
                </div>
                """)

                import uuid
                if "ai_session_id" not in st.session_state:
                    st.session_state.ai_session_id = str(uuid.uuid4())
                sess_id = st.session_state.ai_session_id

                from src.ai.nl_query_engine import AIEnergyMarketAnalyst, session_protector
                from config.settings import is_user_custom_key_configured
                from src.ai.gemini_client import gemini_client

                has_custom_key = is_user_custom_key_configured() or gemini_client.is_key_configured()
                sess_status = session_protector.get_session_status(sess_id, has_custom_key=has_custom_key, enforce_user_daily_limit=True)

                if sess_status.get("is_blocked"):
                    status_badge_html = '<div style="display:inline-block;padding:5px 12px;background:rgba(239, 68, 68, 0.2);color:#EF4444;font-weight:700;font-size:12px;border:1px solid #EF4444;border-radius:4px;margin-bottom:12px;">🚫 Security Violation: Session Terminated</div>'
                elif sess_status.get("is_daily_quota_finished"):
                    status_badge_html = f'<div style="display:inline-block;padding:5px 12px;background:rgba(245, 185, 66, 0.2);color:#F5B942;font-weight:700;font-size:12px;border:1px solid #F5B942;border-radius:4px;margin-bottom:12px;">⏳ Daily Quota Reached (3/3 Used) • Resets in {sess_status["reset_time_str"]}</div>'
                else:
                    status_badge_html = f'<div style="display:inline-block;padding:5px 12px;background:rgba(16, 185, 129, 0.2);color:#10B981;font-weight:700;font-size:12px;border:1px solid #10B981;border-radius:4px;margin-bottom:12px;">🟢 Antigravity AI Active • {sess_status["daily_questions_remaining"]} / 3 Questions Remaining Today (24h Quota)</div>'
                render_html(status_badge_html)

                f9_col1, f9_col2, f9_col3, f9_col4, f9_col5 = st.columns(5)
                f9_q = None
                with f9_col1:
                    if st.button("🇸🇦 Saudi Tax & Rates", key="feat_ai_btn_saudi", width="stretch", type="secondary"):
                        f9_q = "how much Saudi take tax from there people"
                with f9_col2:
                    if st.button("🇮🇳 Prayagraj Petrol & Tax", key="feat_ai_btn1", width="stretch", type="secondary"):
                        f9_q = "What is the petrol price in Prayagraj and how much tax does Uttar Pradesh take?"
                with f9_col3:
                    if st.button("🌍 Top Petrol Contributor", key="feat_ai_btn2", width="stretch", type="secondary"):
                        f9_q = "who is the more contributor of petrol in the world"
                with f9_col4:
                    if st.button("🚢 Strait of Hormuz Risk", key="feat_ai_btn3", width="stretch", type="secondary"):
                        f9_q = "What is the risk of a disruption in the Strait of Hormuz?"
                with f9_col5:
                    if st.button("🏢 Indian PSU OMCs", key="feat_ai_btn4", width="stretch", type="secondary"):
                        f9_q = "What is the market share and refining capacity of Indian PSU OMCs like IOCL, BPCL, and HPCL?"

                feat_ai_input = st.text_input(
                    "Ask any question about fuel rates, state taxes, maritime risks, or crude markets:",
                    value=f9_q if f9_q else "",
                    placeholder="e.g. how much Saudi take tax from there people, or What is petrol rate in Prayagraj?",
                    key="feat_f9_text_input"
                )
                if feat_ai_input and feat_ai_input.strip():
                    with st.spinner("Analyzing with AI Market Analyst Engine..."):
                        ai_resp = AIEnergyMarketAnalyst.answer_question(
                            feat_ai_input,
                            session_id=sess_id,
                            allow_free_autonomous=True,
                            enforce_user_daily_limit=True
                        )
                        if ai_resp.get("is_security_blocked") or "Security Violation" in ai_resp.get("topic", ""):
                            render_html("""<div style="display:inline-block;padding:7px 14px;background:rgba(239, 68, 68, 0.2);color:#EF4444;font-weight:700;font-size:12.5px;border:1.5px solid #EF4444;margin-bottom:8px;border-radius:4px;">🚫 Enterprise Security Alert: Malicious activity detected. Session terminated.</div>""")
                        elif "Daily Free Quota Finished" in ai_resp.get("topic", "") or "Daily Quota Limit Reached" in ai_resp.get("topic", ""):
                            render_html(f"""<div style="display:inline-block;padding:7px 14px;background:rgba(245, 185, 66, 0.2);color:#F5B942;font-weight:700;font-size:12.5px;border:1.5px solid #F5B942;margin-bottom:8px;border-radius:4px;">⏳ Daily Quota Reached (3/3 Questions Used) • Resets in {sess_status["reset_time_str"]}</div>""")
                        elif ai_resp.get("autonomous_free_mode"):
                            render_html("""<div style="display:inline-block;padding:5px 12px;background:rgba(16, 185, 129, 0.2);color:#10B981;font-weight:700;font-size:12px;border:1.5px solid #10B981;margin-bottom:8px;border-radius:4px;">🟢 Antigravity AI Engine (3 Questions / 24h Quota)</div>""")
                        st.markdown(ai_resp["answer_text"])
                        if ai_resp.get("visualization_fig") is not None:
                            st.plotly_chart(ai_resp["visualization_fig"], width="stretch", theme=None)
                        if ai_resp.get("data_records"):
                            st.dataframe(pd.DataFrame(ai_resp["data_records"]), width="stretch", hide_index=True)

                col_f9_studio, col_f9_dash = st.columns([1, 1])
                with col_f9_studio:
                    render_html("""
                    <a href="/AI_Analyst" target="_self" style="text-decoration: none; display: block;">
                        <div style="background: #EAB308; color: #070A12; font-family: 'Space Grotesk', sans-serif; font-size: 12.5px; font-weight: 700; height: 34px; line-height: 34px; text-align: center; border-radius: 6px; box-shadow: 0 2px 6px rgba(0,0,0,0.25); cursor: pointer; transition: all 0.15s ease;">
                            🤖 Open Full AI Analyst Studio (/AI_Analyst) →
                        </div>
                    </a>
                    """)
                with col_f9_dash:
                    if st.button("📊 View in Dashboard Chapter 09", key="feat_f9_dash_btn", width="stretch", type="secondary"):
                        if navigate_fn:
                            navigate_fn("Live Intelligence Dashboard")
                        else:
                            st.session_state.active_nav = "⚡ Intelligence Dashboard"
                            st.rerun()
                st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        else:
            col_btn, _ = st.columns([2.0, 3.0])
            with col_btn:
                if st.button(f"⚡ {f['action_text']} →", key=f"feat_btn_{f['id']}", width="stretch", type="secondary"):
                    if navigate_fn:
                        navigate_fn(f["nav_target"])
                    else:
                        st.session_state.active_nav = f["nav_target"]
                        st.rerun()
            st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
