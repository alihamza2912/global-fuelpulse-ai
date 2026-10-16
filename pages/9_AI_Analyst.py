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

# Small readable status line: "AI assistant: connected", "AI key not found", or "Free quota finished"
if q_status["is_finished"]:
    status_label = "Free quota finished"
    status_icon = "🔴"
    status_detail = f"Available again after {q_status['reset_time_str']}"
    badge_bg = "#FFEBEA"
elif not gemini_client.is_key_configured():
    status_label = "AI key not found"
    status_icon = "🟡"
    status_detail = "Add GEMINI_API_KEY in .env file to enable live AI briefings"
    badge_bg = "#FFF8E1"
else:
    status_label = "AI assistant: connected"
    status_icon = "🟢"
    status_detail = f"Free questions left today: {q_status['calls_remaining']} / {q_status['max_calls_today']}"
    badge_bg = "#EBF7EE"

render_html(f"""<div style="display:inline-flex;align-items:center;gap:10px;padding:9px 18px;background:rgba(14, 21, 38, 0.85);backdrop-filter:blur(12px);color:#F9FAFB;font-weight:700;font-size:13px;border:1px solid rgba(255, 255, 255, 0.14);box-shadow:0 4px 14px rgba(0, 0, 0, 0.35);margin-bottom:16px;border-radius:6px;"><span>{status_icon} <strong style="color:#F5B942;">{status_label}</strong></span><span style="color:rgba(255, 255, 255, 0.2);font-weight:400;">•</span><span style="font-weight:500;font-size:12.5px;color:#94A3B8;">{status_detail}</span></div>""")

# Assistant Info Banner
st.info(
    f"""
    🛡️ **Free-Tier Protection & Grounded Data Engine:**
    - Model: **{settings.api.ai_model}** (Free tier only, zero billing-enabled options).
    - Status: **{status_label}** ({status_detail}).
    - Quota resets daily at **midnight Pacific Time ({q_status['reset_time_str']})**.
    - **Zero Quota Usage**: Simple fuel price queries, global contributor benchmarks, and repeated questions are answered directly from our verified energy database and local cache without consuming daily AI calls.
    - **Session Protections**: Maximum 500 characters, 3-second cooldown between questions, and 15 questions per hour.
    """
)

# Preset Query Buttons
st.subheader("💡 Suggested Intelligence Queries")
btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)

preset_q = None
with btn_col1:
    if st.button("🚢 Top Crude Exporters", width="stretch"):
        preset_q = "Which countries exported the most crude oil in the latest available reporting year?"

with btn_col2:
    if st.button("⛽ Compare Key Pump Prices", width="stretch"):
        preset_q = "Compare petrol prices in India, Germany and the United States."

with btn_col3:
    if st.button("🌍 Top Petrol Contributor", width="stretch"):
        preset_q = "who is the more contributor of petrol in the world"

with btn_col4:
    if st.button("🚚 Fleet Fuel Budget Shock", width="stretch"):
        preset_q = "What would a 10% increase in fuel prices do to my fleet budget?"

# Natural Language Text Input
user_question = st.text_input(
    "Ask a market intelligence question:",
    value=preset_q if preset_q else "",
    placeholder="e.g. who is the more contributor of petrol in the world (max 500 characters)"
)

if user_question:
    with st.spinner("Analyzing question, checking cache & energy data mart..."):
        response = AIEnergyMarketAnalyst.answer_question(
            question=user_question,
            session_id=st.session_state.ai_session_id
        )

    st.markdown("---")

    # Render quota/source badges
    if response.get("served_from_db"):
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
