"""
Page 9: AI Energy Market Analyst.
Grounded natural language decision support answering queries via verified read-only SQL execution,
intelligent question caching, direct database routing, and Google Gemini free-tier AI with strict
quota and rate-limit protection.
"""

import uuid
from pathlib import Path
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Ensure .env is loaded using absolute path from project root
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE, override=True)

from src.ui_components import render_page_header, render_csv_download, apply_theme, render_html
from src.ai.nl_query_engine import AIEnergyMarketAnalyst
from src.ai.quota_manager import quota_manager
from src.ai.gemini_client import gemini_client
from config.settings import settings

apply_theme()

render_page_header(
    title="AI ENERGY MARKET ANALYST",
    subtitle="Grounded Natural Language Intelligence with Free-Tier Quota & Rate-Limit Protection",
    source_tag="Safe Read-Only SQL & Gemini Free-Tier",
    observation_date="Continuous Oct 2026 Grounding"
)

# Initialize unique session identifier for per-user rate limit & cooldown tracking
if "ai_session_id" not in st.session_state:
    st.session_state.ai_session_id = str(uuid.uuid4())

# Retrieve real-time shared quota status
q_status = quota_manager.get_quota_status()

# Status badge logic: Always online (Free Autonomous Mode active when no key is provided)
if q_status["is_finished"]:
    status_label = "Free Autonomous AI: Online"
    status_icon = "🟢"
    status_detail = f"Continuous access active • Daily quota resets at {q_status['reset_time_str']}"
    badge_bg = "#EBF7EE"
elif not gemini_client.is_key_configured():
    status_label = "Free AI Analyst: Online"
    status_icon = "🟢"
    status_detail = "100% Free Autonomous Mode Active • Zero API Key Required • Ask Anything"
    badge_bg = "#EBF7EE"
else:
    status_label = "AI Assistant: Connected"
    status_icon = "🟢"
    status_detail = f"Free questions left today: {q_status['calls_remaining']} / {q_status['max_calls_today']}"
    badge_bg = "#EBF7EE"

render_html(f"""<div style="display:inline-flex;align-items:center;gap:10px;padding:9px 18px;background:rgba(14, 21, 38, 0.85);backdrop-filter:blur(12px);color:#F9FAFB;font-weight:700;font-size:13px;border:1px solid rgba(255, 255, 255, 0.14);box-shadow:0 4px 14px rgba(0, 0, 0, 0.35);margin-bottom:16px;border-radius:6px;"><span>{status_icon} <strong style="color:#F5B942;">{status_label}</strong></span><span style="color:rgba(255, 255, 255, 0.2);font-weight:400;">•</span><span style="font-weight:500;font-size:12.5px;color:#94A3B8;">{status_detail}</span></div>""")

# Assistant Info Banner
st.info(
    f"""
    🛡️ **100% Free Autonomous Energy Intelligence:**
    - Mode: **Continuous Free AI Market Analyst** (Zero billing, zero API keys required).
    - Status: **{status_label}** ({status_detail}).
    - **Free Asking Capability**: Ask freely about any Indian city or state fuel price & tax decomposition (e.g. Prayagraj, UP, Delhi, Mumbai), global crude contributors, maritime chokepoints, PSU oil companies (IOCL, BPCL, HPCL), or macroeconomic inflation shocks.
    - **Direct Mathematical Precision**: Price breakdowns and tax calculations are resolved directly from official Ministry of Petroleum & Natural Gas (MoPNG) circulars and state VAT statutes.
    """
)

# Preset Query Buttons
st.subheader("💡 Suggested Intelligence Queries")
btn_col1, btn_col2, btn_col3, btn_col4, btn_col5 = st.columns(5)

preset_q = None
with btn_col1:
    if st.button("🇮🇳 Prayagraj Petrol & Tax", width="stretch"):
        preset_q = "What is the petrol price in Prayagraj and how much tax does Uttar Pradesh take?"

with btn_col2:
    if st.button("🌍 Top Petrol Contributor", width="stretch"):
        preset_q = "who is the more contributor of petrol in the world"

with btn_col3:
    if st.button("🚢 Strait of Hormuz Risk", width="stretch"):
        preset_q = "What is the risk of a disruption in the Strait of Hormuz?"

with btn_col4:
    if st.button("🏢 Indian PSU OMCs", width="stretch"):
        preset_q = "What is the market share and refining capacity of Indian PSU OMCs like IOCL, BPCL, and HPCL?"

with btn_col5:
    if st.button("🚚 Fleet Fuel Shock", width="stretch"):
        preset_q = "What would a 10% increase in fuel prices do to my fleet budget?"

# Natural Language Text Input
user_question = st.text_input(
    "Ask a market intelligence question freely:",
    value=preset_q if preset_q else "",
    placeholder="e.g. What is the petrol rate in Prayagraj and state tax? (Ask anything freely)"
)

if user_question:
    with st.spinner("Analyzing question, checking cache & energy data mart..."):
        response = AIEnergyMarketAnalyst.answer_question(
            question=user_question,
            session_id=st.session_state.ai_session_id,
            allow_free_autonomous=True
        )

    st.markdown("---")

    # Render quota/source badges
    if response.get("autonomous_free_mode"):
        render_html("""<div style="display:inline-block;padding:5px 12px;background:rgba(16, 185, 129, 0.2);color:#10B981;font-weight:700;font-size:12px;border:1.5px solid #10B981;margin-bottom:10px;border-radius:4px;">🟢 100% Free Autonomous AI Engine (0 Quota • Zero API Key Required)</div>""")
    elif response.get("served_from_db"):
        render_html("""<div style="display:inline-block;padding:4px 10px;background:#FFF3CD;color:#111111;font-weight:700;font-size:12px;border:1.5px solid #111111;margin-bottom:10px;border-radius:3px;">⚡ Direct Database Answer (0 AI quota used)</div>""")
    elif response.get("served_from_cache"):
        render_html("""<div style="display:inline-block;padding:4px 10px;background:#E2E3E5;color:#111111;font-weight:700;font-size:12px;border:1.5px solid #111111;margin-bottom:10px;border-radius:3px;">💾 Answered from Cache (0 AI quota used)</div>""")
    elif response.get("quota_used"):
        render_html(f"""<div style="display:inline-block;padding:4px 10px;background:#D1E7DD;color:#111111;font-weight:700;font-size:12px;border:1.5px solid #111111;margin-bottom:10px;border-radius:3px;">🤖 Generated by Gemini Free-Tier ({response.get('model_used', settings.api.ai_model)})</div>""")

    st.markdown(response["answer_text"])

    # If tabular data returned, render table
    if response.get("data_records"):
        st.markdown("#### 📑 Underlying Relational Database Records")
        rec_df = pd.DataFrame(response["data_records"])
        st.dataframe(rec_df, width="stretch", hide_index=True)
        render_csv_download(rec_df, "ai_analyst_grounded_records.csv")

    # Provenance tags
    if response.get("sources_cited"):
        st.caption(f"Verified Provenance: {', '.join(response['sources_cited'])}")
else:
    st.write("")
    st.write("Enter an energy market question above or click one of the suggested query buttons to generate a grounded briefing.")
