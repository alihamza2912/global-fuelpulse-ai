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

    feature_configs = [
        {"id": "01", "icon": "database", "nav_target": "Live Intelligence Dashboard"},
        {"id": "02", "icon": "ship", "nav_target": "Live Intelligence Dashboard"},
        {"id": "03", "icon": "fuel", "nav_target": "Live Intelligence Dashboard"},
        {"id": "04", "icon": "layers", "nav_target": "India Fuel Center"},
        {"id": "05", "icon": "activity", "nav_target": "Live Intelligence Dashboard"},
        {"id": "06", "icon": "shield-check", "nav_target": "Live Intelligence Dashboard"},
        {"id": "07", "icon": "zap", "nav_target": "Live Intelligence Dashboard"},
        {"id": "08", "icon": "sparkles", "nav_target": "Live Intelligence Dashboard"},
        {"id": "09", "icon": "bot", "nav_target": "AI_Analyst"},
        {"id": "10", "icon": "map-pinned", "nav_target": "India Fuel Center"},
        {"id": "11", "icon": "shield-check", "nav_target": "Data Trust Center"},
        {"id": "12", "icon": "download", "nav_target": "Live Intelligence Dashboard"},
    ]

    features = []
    for cfg in feature_configs:
        fid = cfg["id"]
        is_f9 = (fid == "09")
        status_text = t("feat_lbl_active_f9", cur_lang) if is_f9 else t("feat_lbl_verified", cur_lang)
        features.append({
            "id": fid,
            "name": t(f"feat_{fid}_name", cur_lang),
            "category": t(f"feat_{fid}_cat", cur_lang),
            "icon": cfg["icon"],
            "status": status_text,
            "status_color": "#10B981",
            "what": t(f"feat_{fid}_what", cur_lang),
            "why": t(f"feat_{fid}_why", cur_lang),
            "data": t(f"feat_{fid}_data", cur_lang),
            "action_text": t(f"feat_{fid}_act", cur_lang),
            "nav_target": cfg["nav_target"]
        })

    for f in features:
        icon_svg = get_lucide_icon_svg(f.get("icon", "sparkles"), size=18, color="#F5B942")
        render_html(f"""
        <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 20px; margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px; margin-bottom: 10px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    {icon_svg}
                    <div>
                        <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 800; color: #F5B942; letter-spacing: 0.06em;">{t('feat_lbl_feature', cur_lang)} {f['id']} // {f['category']}</span>
                        <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; font-weight: 800; color: #F9FAFB; margin: 3px 0 0 0;">{f['name']}</h3>
                    </div>
                </div>
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem; font-weight: 800; color: {f['status_color']}; background: rgba(255, 255, 255, 0.05); border: 1px solid {f['status_color']}; padding: 3px 9px; border-radius: 999px;">
                    {f['status']}
                </span>
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.86rem; line-height: 1.55; color: #94A3B8; margin-bottom: 12px;">
                <p style="margin: 0 0 6px 0;"><b style="color: #F9FAFB;">{t('feat_lbl_what', cur_lang)}:</b> {f['what']}</p>
                <p style="margin: 0 0 6px 0;"><b style="color: #F9FAFB;">{t('feat_lbl_why', cur_lang)}:</b> {f['why']}</p>
                <p style="margin: 0;"><b style="color: #F9FAFB;">{t('feat_lbl_sources', cur_lang)}:</b> {f['data']}</p>
            </div>
        </div>
        """)

        if f["id"] == "09":
            with st.container():
                render_html(f"""
                <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 8px; padding: 12px 16px; margin: -6px 0 14px 0;">
                    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 1.15rem;">🤖</span>
                            <b style="color: #34D399; font-family: 'Space Grotesk', sans-serif; font-size: 0.92rem;">{t('feat_f9_try_title', cur_lang)}</b>
                        </div>
                        <span style="background: rgba(16, 185, 129, 0.18); color: #34D399; font-size: 0.72rem; font-weight: 800; padding: 2px 8px; border-radius: 4px; border: 1px solid rgba(16, 185, 129, 0.4);">
                            {t('feat_f9_try_badge', cur_lang)}
                        </span>
                    </div>
                    <p style="font-size: 0.78rem; color: #94A3B8; margin: 6px 0 0 0; line-height: 1.4;">
                        {t('feat_f9_try_desc', cur_lang)}
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
                from src.auth.quota_service import quota_service
                clean_uid_feat = sess_id.replace("usr_", "").replace("user_", "")
                q_sum = quota_service.get_quota_summary(clean_uid_feat, bypass_cache=True)
                used_feat = q_sum.get("used", 0)
                rem_feat = q_sum.get("remaining", max(0, 3 - used_feat))
                is_exh_feat = q_sum.get("quota_exhausted", (used_feat >= 3 or rem_feat <= 0))
                rst_feat = q_sum.get("reset_time_str", "24 hours")

                sess_status = session_protector.get_session_status(sess_id)
                if sess_status.get("is_blocked"):
                    status_badge_html = '<div style="display:inline-block;padding:5px 12px;background:rgba(239, 68, 68, 0.2);color:#EF4444;font-weight:700;font-size:12px;border:1px solid #EF4444;border-radius:4px;margin-bottom:12px;">🚫 Security Violation: Session Terminated</div>'
                elif is_exh_feat:
                    status_badge_html = f'<div style="display:inline-block;padding:5px 12px;background:rgba(245, 185, 66, 0.2);color:#F5B942;font-weight:700;font-size:12px;border:1px solid #F5B942;border-radius:4px;margin-bottom:12px;">⏳ Daily Quota Reached (3/3 used · 0 remaining · Quota exceeded) • Resets in {rst_feat}</div>'
                else:
                    status_badge_html = f'<div style="display:inline-block;padding:5px 12px;background:rgba(16, 185, 129, 0.2);color:#10B981;font-weight:700;font-size:12px;border:1px solid #10B981;border-radius:4px;margin-bottom:12px;">🟢 Antigravity AI Active • {used_feat}/3 used · {rem_feat} remaining</div>'
                render_html(status_badge_html)

                f9_col1, f9_col2, f9_col3, f9_col4, f9_col5 = st.columns(5)
                f9_q = None
                with f9_col1:
                    if st.button(f"🇸🇦 {t('feat_chip_saudi', cur_lang)}", key="feat_ai_btn_saudi", width="stretch", type="secondary"):
                        f9_q = "how much Saudi take tax from there people"
                with f9_col2:
                    if st.button(f"🇮🇳 {t('feat_chip_prayagraj', cur_lang)}", key="feat_ai_btn1", width="stretch", type="secondary"):
                        f9_q = "What is the petrol price in Prayagraj and how much tax does Uttar Pradesh take?"
                with f9_col3:
                    if st.button(f"🌍 {t('feat_chip_top_contrib', cur_lang)}", key="feat_ai_btn2", width="stretch", type="secondary"):
                        f9_q = "who is the more contributor of petrol in the world"
                with f9_col4:
                    if st.button(f"🚢 {t('feat_chip_hormuz', cur_lang)}", key="feat_ai_btn3", width="stretch", type="secondary"):
                        f9_q = "What is the risk of a disruption in the Strait of Hormuz?"
                with f9_col5:
                    if st.button(f"🏢 {t('feat_chip_psu', cur_lang)}", key="feat_ai_btn4", width="stretch", type="secondary"):
                        f9_q = "What is the market share and refining capacity of Indian PSU OMCs like IOCL, BPCL, and HPCL?"

                feat_ai_input = st.text_input(
                    t("feat_ai_input_label", cur_lang),
                    value=f9_q if f9_q else "",
                    placeholder=t("feat_ai_input_placeholder", cur_lang),
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
                            render_html(f"""<div style="display:inline-block;padding:7px 14px;background:rgba(245, 185, 66, 0.2);color:#F5B942;font-weight:700;font-size:12.5px;border:1.5px solid #F5B942;margin-bottom:8px;border-radius:4px;">⏳ Daily Quota Reached (3/3 used · 0 remaining · Quota exceeded) • Resets in {rst_feat}</div>""")
                        elif ai_resp.get("autonomous_free_mode"):
                            render_html("""<div style="display:inline-block;padding:5px 12px;background:rgba(16, 185, 129, 0.2);color:#10B981;font-weight:700;font-size:12px;border:1.5px solid #10B981;margin-bottom:8px;border-radius:4px;">🟢 Antigravity AI Engine (3 Questions / 24h Quota)</div>""")
                        st.markdown(ai_resp["answer_text"])
                        if ai_resp.get("visualization_fig") is not None:
                            st.plotly_chart(ai_resp["visualization_fig"], width="stretch", theme=None)
                        if ai_resp.get("data_records"):
                            st.dataframe(pd.DataFrame(ai_resp["data_records"]), width="stretch", hide_index=True)

                render_html('<div class="fuelpulse-f9-actions">')
                col_f9_studio, col_f9_dash = st.columns([1, 1])
                with col_f9_studio:
                    render_html(f"""
                    <a href="/AI_Analyst" target="_self" style="text-decoration: none; display: block;">
                        <div style="background: #EAB308; color: #070A12; font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 800; height: 42px; line-height: 42px; text-align: center; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.25); cursor: pointer; transition: all 0.15s ease;">
                            {t('home_btn_f9_studio', cur_lang)}
                        </div>
                    </a>
                    """)
                with col_f9_dash:
                    if st.button(f"{t('home_btn_f9_dash', cur_lang)}", key="feat_f9_dash_btn", width="stretch", type="secondary"):
                        if navigate_fn:
                            navigate_fn("Live Intelligence Dashboard")
                        else:
                            st.session_state.active_nav = "⚡ Intelligence Dashboard"
                            st.rerun()
                render_html('</div>')
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
