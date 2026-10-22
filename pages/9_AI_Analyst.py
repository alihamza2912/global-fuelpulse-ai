"""
Page 9: AI Assistant & Energy Market Analyst.
Integrates:
- Official OpenAI Responses API with real-time web search tool.
- Database-backed authenticated user identity (persisting across page reloads and devices).
- Atomic rolling 24-hour quota management (3 free questions per user per 24 hours).
- Responsive conversational chat interface with full history, loading state, and clickable source citations.
- Enterprise security shield preventing prompt injections and unauthorized data access.
"""

import uuid
import sys
import time
from pathlib import Path
from datetime import datetime, timezone
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Ensure project root AND src directory are in sys.path
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
    load_dotenv(dotenv_path=ENV_FILE, override=False)

from src.ui_components import render_page_header, render_csv_download, apply_theme, render_html
from src.localization.i18n import t, get_current_language
from src.auth.auth_service import AuthService, DEFAULT_DEMO_USERNAME, DEFAULT_DEMO_EMAIL
from src.ai.openai_client import (
    openai_client,
    OpenAIQuotaExhaustedError,
    OpenAIMissingKeyError,
    OpenAIServiceError
)
from src.ai.openai_quota_manager import openai_quota_manager
from src.ai.chat_service import chat_endpoint, get_user_quota_endpoint
from src.ai.gemini_client import gemini_client
from config.settings import settings

apply_theme()
current_lang = get_current_language()

# Ensure default database tables and default demo analyst exist
AuthService.ensure_default_demo_user()

# Retrieve active authenticated user (strict gate: users MUST sign in to ask questions)
current_user = AuthService.get_active_user()

if not current_user:
    st.markdown("""
    <div style="background: rgba(245, 185, 66, 0.08); border: 1.5px solid rgba(245, 185, 66, 0.35); border-radius: 12px; padding: 20px 24px; margin: 16px 0 20px 0; text-align: center;">
        <div style="font-size: 2.2rem; margin-bottom: 8px;">🔐</div>
        <h3 style="margin: 0 0 6px 0; color: #F9FAFB; font-family: 'Space Grotesk', sans-serif;">Sign In Required to Ask Questions</h3>
        <p style="margin: 0 auto; color: #94A3B8; font-size: 0.92rem; line-height: 1.5; max-width: 620px;">
            Every registered user receives <b>3 free questions every 24 hours</b>. Unauthenticated visitors cannot ask questions.<br>
            Please sign in or create an account to start asking questions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_in, tab_reg = st.tabs(["Sign In", "Create Account"])
    with tab_in:
        with st.form("page9_gate_signin", clear_on_submit=False):
            in_email = st.text_input("Email", placeholder="you@company.com", key="p9_gate_signin_email")
            in_pwd = st.text_input("Password", type="password", placeholder="••••••••", key="p9_gate_signin_pwd")
            submit_in = st.form_submit_button("Sign In & Unlock 3 Questions", type="primary", use_container_width=True)
        if submit_in:
            ok, msg, token, udict = AuthService.login_user(in_email, in_pwd)
            if ok and udict:
                st.session_state["auth_user"] = udict
                st.session_state["auth_token"] = token
                st.success("Signed in successfully! Your 3 free questions are active.")
                st.rerun()
            else:
                st.error(msg)
    with tab_reg:
        with st.form("page9_gate_register", clear_on_submit=False):
            reg_name = st.text_input("Full Name", placeholder="e.g. Alexander Vance", key="p9_gate_reg_name")
            reg_user = st.text_input("Username", placeholder="e.g. avance", key="p9_gate_reg_user")
            reg_email = st.text_input("Email", placeholder="you@company.com", key="p9_gate_reg_email")
            reg_pwd = st.text_input("Password", type="password", placeholder="At least 6 characters", key="p9_gate_reg_pwd")
            submit_reg = st.form_submit_button("Create Account & Get 3 Free Questions", type="primary", use_container_width=True)
        if submit_reg:
            ok, msg, new_u = AuthService.register_user(reg_user, reg_email, reg_pwd, reg_name)
            if ok:
                _, _, token, udict = AuthService.login_user(reg_email, reg_pwd)
                if udict:
                    st.session_state["auth_user"] = udict
                    st.session_state["auth_token"] = token
                    st.success("Account created and signed in! 3 free questions unlocked.")
                    st.rerun()
            else:
                st.error(msg)
    st.stop()

user_id = current_user.get("user_id")

# Fetch persistent database quota status for this user from QuotaService
from src.auth.quota_service import quota_service
quota_status = quota_service.get_quota_summary(user_id, bypass_cache=True)
used_q = quota_status.get("used", 0)
remaining_q = quota_status.get("remaining", max(0, 3 - used_q))
is_exhausted = quota_status.get("quota_exhausted", (used_q >= 3 or remaining_q <= 0))
reset_time_str = quota_status.get("reset_time_str", "24 hours")

# Initialize conversation history in session state
if "openai_chat_history" not in st.session_state:
    st.session_state["openai_chat_history"] = []

render_page_header(
    title=t("sidebar_09_ai", current_lang),
    subtitle="OpenAI Responses API & Web Search • 3 Free Questions / Rolling 24 Hours • Authenticated Identity",
    source_tag="OpenAI GPT-4o & Live Search Grounding",
    observation_date=datetime.now(timezone.utc).strftime("%B %Y")
)

# 1. Authenticated User & Quota Status Badge
def _render_quota_pill(user_info, q_status):
    u_name = user_info.get("full_name") or user_info.get("username") or "Analyst"
    u_email = user_info.get("email", "")
    used = q_status.get("used", 0)
    rem = q_status.get("remaining", max(0, 3 - used))
    exhausted = q_status.get("quota_exhausted", (used >= 3 or rem <= 0))
    r_time = q_status.get("reset_time_str", "24 hours")

    has_openai = openai_client.is_key_configured()
    has_gemini = gemini_client.is_key_configured()

    if has_openai:
        engine_name = "OpenAI GPT"
        model_name = settings.api.openai_model
    elif has_gemini:
        engine_name = "Google Gemini"
        model_name = settings.api.ai_model
    else:
        engine_name = "AI Engine"
        model_name = "No Key"

    if exhausted or rem <= 0 or used >= 3:
        status_icon = "⏳"
        status_color = "#F5B942"
        status_label = "3/3 used · 0 remaining · Quota exceeded"
        status_detail = f"Resets in {r_time} • 3 questions allowed per rolling 24 hours"
    else:
        status_icon = "🟢"
        status_color = "#10B981"
        status_label = f"{used}/3 used · {rem} remaining"
        status_detail = f"Rolling 24-hour quota • Account: {u_name} ({u_email})"

    return f"""
    <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;padding:12px 18px;background:rgba(14, 21, 38, 0.85);backdrop-filter:blur(12px);color:#F9FAFB;font-size:13px;border:1px solid rgba(255, 255, 255, 0.14);box-shadow:0 4px 14px rgba(0, 0, 0, 0.35);margin-bottom:16px;border-radius:8px;">
        <div style="display:flex;align-items:center;gap:10px;">
            <span>{status_icon} <strong style="color:{status_color};">{status_label}</strong></span>
            <span style="color:rgba(255, 255, 255, 0.2);font-weight:400;">•</span>
            <span style="color:#94A3B8;font-weight:500;">{status_detail}</span>
        </div>
        <div style="display:flex;align-items:center;gap:8px;">
            <span style="background:rgba(255, 255, 255, 0.08);padding:3px 8px;border-radius:4px;font-size:11.5px;color:#CBD5E1;">Model: <strong>{model_name}</strong></span>
            <span style="background:rgba(255, 255, 255, 0.08);padding:3px 8px;border-radius:4px;font-size:11.5px;color:#CBD5E1;">Research: <strong>Active</strong></span>
        </div>
    </div>
    """

quota_pill_slot = st.empty()
quota_pill_slot.markdown(_render_quota_pill(current_user, quota_status), unsafe_allow_html=True)

# 2. Suggested Quick Inquiries
st.subheader("💡 Suggested Intelligence Queries")
btn_col0, btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(5)
preset_q = None
with btn_col0:
    if st.button("⚡ Jio Fuel Competitors", use_container_width=True, type="primary"):
        preset_q = "Which company can easily compete with Jio-bp fuel in India?"
with btn_col1:
    if st.button("🇸🇦 Saudi Fuel Supplier", use_container_width=True, type="secondary"):
        preset_q = "Who is the main supplier of fuel from Saudi Arabia and how is crude exported?"
with btn_col2:
    if st.button("🇮🇳 Prayagraj Petrol & Tax", use_container_width=True, type="secondary"):
        preset_q = "What is the petrol price in Prayagraj and how much tax does Uttar Pradesh take?"
with btn_col3:
    if st.button("🌍 Top Petrol Contributor", use_container_width=True, type="secondary"):
        preset_q = "Who is the top contributor of petroleum and petrol in the world currently?"
with btn_col4:
    if st.button("🚢 Strait of Hormuz Risk", use_container_width=True, type="secondary"):
        preset_q = "What are the latest developments and geopolitical risks in the Strait of Hormuz?"

# 3. Conversation History View
chat_container = st.container()
with chat_container:
    if not st.session_state["openai_chat_history"]:
        st.markdown(
            """
            <div style="text-align:center;padding:32px 20px;background:rgba(255, 255, 255, 0.02);border:1px dashed rgba(255, 255, 255, 0.12);border-radius:8px;margin-bottom:16px;">
                <div style="font-size:2rem;margin-bottom:8px;">🤖</div>
                <div style="font-weight:700;font-size:1.05rem;color:#F9FAFB;">OpenAI Assistant Ready</div>
                <div style="font-size:0.85rem;color:#94A3B8;max-width:560px;margin:6px auto 0 auto;">
                    Ask any question — general knowledge, programming, technical, business, or current energy intelligence.
                    The assistant retrieves live facts and source citations automatically via OpenAI Web Search.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        for msg in st.session_state["openai_chat_history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg.get("sources"):
                    st.markdown("##### 🔗 Verified Citations")
                    for src in msg["sources"]:
                        st.markdown(f"- [{src.get('title', 'Web Source')}]({src.get('url', '#')})")

# 4. Message Input: Typing + Voice Input
tab_type, tab_voice, tab_account = st.tabs([
    t("ai_tab_type", current_lang),
    t("ai_tab_voice", current_lang),
    "👤 Account & OpenAI Settings"
])

submitted_question = None

with tab_type:
    with st.form(key="openai_chat_form", clear_on_submit=True, border=False):
        c_in, c_btn, c_clear = st.columns([5.0, 1.2, 0.8], gap="small", vertical_alignment="center")
        with c_in:
            text_input_val = st.text_input(
                "Ask a question:",
                value=preset_q if preset_q else "",
                placeholder="Ask anything (general knowledge, technical, markets, news)...",
                label_visibility="collapsed"
            )
        with c_btn:
            send_btn = st.form_submit_button("Send ➔", use_container_width=True, type="primary")
        with c_clear:
            clear_btn = st.form_submit_button("Clear", use_container_width=True)

        if send_btn and text_input_val.strip():
            submitted_question = text_input_val.strip()
        elif clear_btn:
            st.session_state["openai_chat_history"] = []
            st.rerun()

with tab_voice:
    st.markdown(f"<div style='font-size:0.82rem; color:#94A3B8; margin-bottom:8px;'>{t('ai_voice_subtext', current_lang)}</div>", unsafe_allow_html=True)
    voice_audio = st.audio_input(t("ai_record_voice_label", current_lang), key="openai_voice_input")
    if voice_audio is not None:
        import io
        import speech_recognition as sr
        try:
            r = sr.Recognizer()
            with sr.AudioFile(io.BytesIO(voice_audio.read())) as source:
                audio_data = r.record(source)
                voice_transcribed = r.recognize_google(audio_data)
                st.success(f"🗣️ Transcribed Voice Note: **\"{voice_transcribed}\"**")
                if st.button("Ask Voice Question", key="openai_submit_voice", type="primary"):
                    submitted_question = voice_transcribed.strip()
        except sr.UnknownValueError:
            st.info("💡 Audio captured. You can also type your question directly in the Type Question tab.")
        except Exception:
            st.info("💡 Audio captured. If faint, you can type your question directly.")

with tab_account:
    st.markdown("#### 👤 Authenticated User & Limits")
    st.markdown(
        f"""
        - **Current User**: **{current_user.get('full_name')}** (`{current_user.get('email')}`)
        - **Stable User ID**: `{user_id}`
        - **24-Hour Allowance**: **3 questions per user per rolling 24 hours** (persists in database across devices & refreshes).
        - **Questions Remaining**: **{remaining_q} / 3**
        """
    )

    st.markdown("---")
    st.markdown("#### ⚙️ AI Engine & API Credentials")
    cfg_col1, cfg_col2 = st.columns([3.5, 2.5])
    with cfg_col1:
        # Gemini / Antigravity Key
        gem_k = st.session_state.get("gemini_api_key") or st.session_state.get("user_api_key") or settings.api.gemini_api_key
        has_gem = bool(gem_k and len(gem_k) > 10)
        gem_status = "🟢 Connected" if has_gem else "⚪ Not Set"
        st.markdown(f"**Google Gemini API Key**: `{gem_status}`")
        new_gem_input = st.text_input(
            "GEMINI_API_KEY (Session Override):",
            value=st.session_state.get("gemini_api_key", ""),
            type="password",
            placeholder="AQ... or AIza...",
            help="Free-tier Google Gemini key from Google AI Studio. Used for live energy research."
        )
        if st.button("Update Gemini Key", key="save_gemini_key_btn"):
            if new_gem_input.strip():
                st.session_state["gemini_api_key"] = new_gem_input.strip()
                st.session_state["user_api_key"] = new_gem_input.strip()
                st.success("Session Gemini API Key updated.")
            else:
                st.session_state.pop("gemini_api_key", None)
                st.session_state.pop("user_api_key", None)
                st.info("Session Gemini key reset to default.")
            st.rerun()

        st.markdown("<br/>", unsafe_allow_html=True)

        # OpenAI Key
        oai_k = st.session_state.get("openai_api_key") or settings.api.openai_api_key
        has_oai = bool(oai_k and len(oai_k) > 10 and not oai_k.startswith("sk-placeholder"))
        oai_status = "🟢 Connected" if has_oai else "⚪ Not Set"
        st.markdown(f"**OpenAI API Key**: `{oai_status}`")
        custom_key_input = st.text_input(
            "OPENAI_API_KEY (Session Override):",
            value=st.session_state.get("openai_api_key", ""),
            type="password",
            placeholder="sk-proj-...",
            help="Server-side key loads from .env by default. You can override it for your session here."
        )
        if st.button("Update OpenAI Key", key="save_openai_key_btn"):
            if custom_key_input.strip():
                st.session_state["openai_api_key"] = custom_key_input.strip()
                st.success("Session OpenAI API Key updated.")
            else:
                st.session_state.pop("openai_api_key", None)
                st.info("Session OpenAI key reset to default.")
            st.rerun()

    with cfg_col2:
        st.markdown("**Engine Settings**")
        st.info(
            f"**Active Model**: `{settings.api.ai_model if not openai_client.is_key_configured() else settings.api.openai_model}`\n\n"
            f"**Autonomous Deep Research**: `Enabled`\n\n"
            f"**Diagram Generator**: `Mermaid SVG & Flowcharts`\n\n"
            f"**Token Usage**: Bounded to fast, crisp 600-token analytical outputs."
        )

    st.markdown("---")
    # Quick Switch / Register Account
    with st.expander("🔐 Switch User or Register Account", expanded=False):
        auth_tab_in, auth_tab_reg = st.tabs(["Sign In", "Register New User"])
        with auth_tab_in:
            in_user = st.text_input("Username or Email", key="auth_in_user")
            in_pass = st.text_input("Password", type="password", key="auth_in_pass")
            if st.button("Sign In", key="auth_btn_signin", type="primary"):
                ok, msg, token, u_dict = AuthService.login_user(in_user, in_pass)
                if ok and token:
                    st.session_state["auth_session_token"] = token
                    st.session_state["auth_user"] = u_dict
                    st.success("Signed in successfully!")
                    st.rerun()
                else:
                    st.error(msg)

        with auth_tab_reg:
            reg_user = st.text_input("Username (3+ chars)", key="auth_reg_user")
            reg_email = st.text_input("Email", key="auth_reg_email")
            reg_name = st.text_input("Full Name (optional)", key="auth_reg_name")
            reg_pass = st.text_input("Password (6+ chars)", type="password", key="auth_reg_pass")
            if st.button("Register Account", key="auth_btn_register", type="primary"):
                ok, msg, new_u = AuthService.register_user(reg_user, reg_email, reg_pass, reg_name)
                if ok:
                    # Auto login
                    _, _, tok, u_dict = AuthService.login_user(reg_user, reg_pass)
                    st.session_state["auth_session_token"] = tok
                    st.session_state["auth_user"] = u_dict
                    st.success(f"Registered and logged in as {reg_user}!")
                    st.rerun()
                else:
                    st.error(msg)

# 5. Process Question Submission
if submitted_question:
    # Append user question to history
    st.session_state["openai_chat_history"].append({
        "role": "user",
        "content": submitted_question,
        "timestamp": datetime.utcnow().isoformat()
    })

    with st.spinner("Connecting to OpenAI Responses API, analyzing query & retrieving citations..."):
        response = chat_endpoint(
            question=submitted_question,
            user_id=user_id,
            enable_search=True
        )

    # Handle Errors
    if response.get("status_code") == 429:
        st.error(
            f"⏳ **HTTP 429: 24-Hour Free Quota Finished**\n\n"
            f"{response.get('message')}\n\n"
            f"Every registered user receives **3 free questions per rolling 24-hour period**. "
            f"Your quota will unlock automatically in **{response.get('reset_time_str')}**."
        )
    elif response.get("status_code") == 401:
        st.warning(
            f"🔑 **OpenAI API Key Notice**\n\n"
            f"{response.get('message')}\n\n"
            f"To enable real outbound queries, please set `OPENAI_API_KEY` in your `.env` file or in the **Account & OpenAI Settings** tab above."
        )
    elif response.get("status") == "error":
        st.error(f"⚠️ {response.get('message')}")
    else:
        # Successful response: append assistant message to conversation history
        st.session_state["openai_chat_history"].append({
            "role": "assistant",
            "content": response.get("answer_text", ""),
            "sources": response.get("sources", []),
            "model": response.get("model_used", settings.api.openai_model),
            "timestamp": datetime.utcnow().isoformat()
        })

    # Refresh user quota pill
    quota_service.invalidate_cache(user_id)
    updated_quota = quota_service.get_quota_summary(user_id, bypass_cache=True)
    quota_pill_slot.markdown(_render_quota_pill(current_user, updated_quota), unsafe_allow_html=True)
    st.rerun()
