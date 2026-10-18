"""
Page 9: AI Energy Market Analyst.
Grounded natural language decision support answering queries via verified read-only SQL execution,
intelligent question caching, direct database routing, Google Gemini AI, and strict 24-hour rate-limit
and anti-abuse security protection.
"""

import uuid
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Ensure project root AND src directory are in sys.path and remove conflicting parent mount
ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"

parent_mount = ROOT_DIR.parent
sys.path = [p for p in sys.path if Path(p).resolve() != parent_mount and Path(p).resolve() != parent_mount.parent]

for d in [str(ROOT_DIR), str(SRC_DIR)]:
    while d in sys.path:
        sys.path.remove(d)
    sys.path.insert(0, d)

# Ensure .env is loaded using absolute path from project root
ENV_FILE = ROOT_DIR / ".env"
if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE, override=True)

from src.ui_components import render_page_header, render_csv_download, apply_theme, render_html
from src.localization.i18n import t, get_current_language
from src.ai.nl_query_engine import AIEnergyMarketAnalyst, session_protector
from src.ai.quota_manager import quota_manager
from src.ai.gemini_client import gemini_client, sanitize_sensitive_text
from config.settings import settings, set_user_api_key, is_user_custom_key_configured, get_system_antigravity_token

apply_theme()
current_lang = get_current_language()

render_page_header(
    title=t("sidebar_09_ai", current_lang),
    subtitle="Grounded Natural Language Intelligence • Strict 24h Quota & Enterprise Security Shield",
    source_tag="Safe Read-Only SQL & Antigravity / Gemini Intelligence",
    observation_date="Continuous Oct 2026 Grounding"
)

# Initialize unique session identifier for per-user rate limit & quota tracking
if "ai_session_id" not in st.session_state:
    st.session_state.ai_session_id = str(uuid.uuid4())

sess_id = st.session_state.ai_session_id
has_custom_key = is_user_custom_key_configured() or gemini_client.is_key_configured()
sess_status = session_protector.get_session_status(sess_id, has_custom_key=has_custom_key, enforce_user_daily_limit=True)

# Determine live status badge
if sess_status.get("is_blocked"):
    status_label = "🚫 Security Alert: Access Terminated"
    status_icon = "🔴"
    status_detail = "Session permanently blocked due to illegal/malicious activity detection"
elif sess_status.get("is_daily_quota_finished"):
    status_label = "Daily Quota Reached (3/3 Used)"
    status_icon = "⏳"
    status_detail = f"Resets in {sess_status['reset_time_str']} (after 24 hours) • 3 questions allowed per 24 hours"
else:
    status_label = "Antigravity AI Connected"
    status_icon = "🟢"
    status_detail = f"Questions remaining today: {sess_status['daily_questions_remaining']} / 3 (Resets in 24 hours)"

render_html(f"""<div style="display:inline-flex;align-items:center;gap:10px;padding:9px 18px;background:rgba(14, 21, 38, 0.85);backdrop-filter:blur(12px);color:#F9FAFB;font-weight:700;font-size:13px;border:1px solid rgba(255, 255, 255, 0.14);box-shadow:0 4px 14px rgba(0, 0, 0, 0.35);margin-bottom:16px;border-radius:6px;"><span>{status_icon} <strong style="color:#F5B942;">{status_label}</strong></span><span style="color:rgba(255, 255, 255, 0.2);font-weight:400;">•</span><span style="font-weight:500;font-size:12.5px;color:#94A3B8;">{status_detail}</span></div>""")

# Assistant Info Banner
st.info(
    f"""
    🛡️ **Enterprise AI Energy Market Analyst (Powered by Antigravity AI):**
    - **Status**: **{status_label}** ({status_detail}).
    - **Integrated Antigravity Tokens**: Automatically connected behind the scenes. Zero manual configuration required.
    - **24-Hour Allowance**: Anyone can ask **up to 3 questions in 24 hours**. After 3 questions, your quota resets automatically after 24 hours.
    - **Clear Plain Language & Visual Flowcharts**: Every answer delivers intuitive analysis accompanied by visual diagrams and flowcharts for effortless comprehension.
    - **Multi-Country Precision**: Accurately analyzes sovereign suppliers (e.g. Saudi Aramco, ADNOC), sovereign tax structures (Saudi Arabia 15% VAT & 0% income tax, India GST/VAT), OPEC quotas, crude contributors, and shipping corridors.
    - **Security & Integrity Shield**: Real-time protection against malicious queries or system tampering.
    """
)

# Preset Query Buttons
st.subheader("💡 Suggested Intelligence Queries")
btn_col0, btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(5)

preset_q = None
with btn_col0:
    if st.button("⚡ Jio Fuel Competitors", use_container_width=True, type="primary"):
        preset_q = "which company can easily compete jio fuel"

with btn_col1:
    if st.button("🇸🇦 Saudi Fuel Supplier", use_container_width=True, type="secondary"):
        preset_q = "who is the main supplier of fuel from saudi"

with btn_col2:
    if st.button("🇮🇳 Prayagraj Petrol & Tax", use_container_width=True, type="secondary"):
        preset_q = "What is the petrol price in Prayagraj and how much tax does Uttar Pradesh take?"

with btn_col3:
    if st.button("🌍 Top Petrol Contributor", use_container_width=True, type="secondary"):
        preset_q = "who is the more contributor of petrol in the world"

with btn_col4:
    if st.button("🚢 Strait of Hormuz Risk", use_container_width=True, type="secondary"):
        preset_q = "What is the risk of a disruption in the Strait of Hormuz?"

# WhatsApp-Style Dual Input: Typing + Voice Recording
tab_type, tab_voice = st.tabs(["💬 Type Question", "🎙️ WhatsApp Voice Note"])
with tab_type:
    text_q = st.text_input(
        "Ask a market intelligence question freely:",
        value=preset_q if preset_q else "",
        placeholder="e.g. which company can easily compete jio fuel, or What is the petrol rate in Prayagraj?"
    )

voice_q = None
with tab_voice:
    st.markdown("<div style='font-size:0.82rem; color:#94A3B8; margin-bottom:8px;'>🎙️ <b>WhatsApp Voice Note:</b> Record your question directly using your microphone. Our speech recognizer transcribes it automatically:</div>", unsafe_allow_html=True)
    voice_audio = st.audio_input("Record Voice Question", key="page9_voice_recorder")
    if voice_audio is not None:
        import io
        import speech_recognition as sr
        try:
            r = sr.Recognizer()
            with sr.AudioFile(io.BytesIO(voice_audio.read())) as source:
                audio_data = r.record(source)
                voice_transcribed = r.recognize_google(audio_data)
                st.success(f"🗣️ Transcribed Voice Note: **\"{voice_transcribed}\"**")
                if st.button("Submit Voice Question ⚡", key="page9_submit_voice", type="primary"):
                    voice_q = voice_transcribed
        except sr.UnknownValueError:
            st.info("💡 Audio captured. If speech was faint, you can type your question directly in the Type Question tab.")
        except Exception:
            st.info("💡 Audio captured. You can also type your question directly in the Type Question tab.")

user_question = voice_q or text_q

if user_question:
    with st.spinner("Analyzing question, checking cache & energy data mart..."):
        response = AIEnergyMarketAnalyst.answer_question(
            question=user_question,
            session_id=sess_id,
            allow_free_autonomous=True,
            enforce_user_daily_limit=True
        )

    st.markdown("---")

    # Render quota/source badges
    if response.get("is_security_blocked") or "Security Violation" in response.get("topic", ""):
        render_html("""<div style="display:inline-block;padding:7px 14px;background:rgba(239, 68, 68, 0.2);color:#EF4444;font-weight:700;font-size:12.5px;border:1.5px solid #EF4444;margin-bottom:10px;border-radius:4px;">🚫 Enterprise Security Alert • Session Terminated</div>""")
    elif "Daily Free Quota Finished" in response.get("topic", "") or "Daily Quota Limit Reached" in response.get("topic", ""):
        render_html("""<div style="display:inline-block;padding:7px 14px;background:rgba(245, 185, 66, 0.2);color:#F5B942;font-weight:700;font-size:12.5px;border:1.5px solid #F5B942;margin-bottom:10px;border-radius:4px;">⏳ Daily Quota Reached (3/3 Questions Used) • Resets After 24 Hours</div>""")
    elif response.get("autonomous_free_mode"):
        render_html("""<div style="display:inline-block;padding:5px 12px;background:rgba(16, 185, 129, 0.2);color:#10B981;font-weight:700;font-size:12px;border:1.5px solid #10B981;margin-bottom:10px;border-radius:4px;">🟢 Antigravity AI Engine (3 Questions / 24h Quota)</div>""")
    elif response.get("served_from_db"):
        render_html("""<div style="display:inline-block;padding:4px 10px;background:#FFF3CD;color:#111111;font-weight:700;font-size:12px;border:1.5px solid #111111;margin-bottom:10px;border-radius:3px;">⚡ Direct Database Answer (0 AI quota used)</div>""")
    elif response.get("served_from_cache"):
        render_html("""<div style="display:inline-block;padding:4px 10px;background:#E2E3E5;color:#111111;font-weight:700;font-size:12px;border:1.5px solid #111111;margin-bottom:10px;border-radius:3px;">💾 Answered from Cache (0 AI quota used)</div>""")
    elif response.get("quota_used"):
        render_html(f"""<div style="display:inline-block;padding:4px 10px;background:#D1E7DD;color:#111111;font-weight:700;font-size:12px;border:1.5px solid #111111;margin-bottom:10px;border-radius:3px;">🤖 Generated by Antigravity / Gemini ({response.get('model_used', settings.api.ai_model)})</div>""")

    st.markdown(response["answer_text"])

    # If visualization returned, render interactive chart
    if response.get("visualization_fig") is not None:
        st.markdown("#### 📊 Interactive Scenario Projection & Intelligence Visualization")
        st.plotly_chart(response["visualization_fig"], width="stretch", theme=None)

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
