"""
GLOBAL FUELPULSE AI — ROADMAP & STATUS VIEW
Three-tier operational roadmap, engineering milestones,
and real-time system capability status.
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


def render_roadmap_view(navigate_fn=None):
    """Renders the comprehensive Product Roadmap and Platform Status."""
    cur_lang = get_current_language()

    render_html(f"""
    <div style="background: radial-gradient(circle at 10% 20%, rgba(52, 211, 153, 0.12) 0%, rgba(14, 21, 38, 0.95) 70%), #070A12; border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 12px; padding: 26px 30px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
            <div>
                {get_fuel_client_logo_html()}
                <h1 style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 2rem; font-weight: 800; color: #F9FAFB; margin: 6px 0 8px 0; letter-spacing: -0.02em;">
                    {t('roadmap_hero_title', cur_lang)}
                </h1>
                <p style="font-family: 'Inter', sans-serif; font-size: 1rem; color: #94A3B8; margin: 0; max-width: 820px; line-height: 1.55;">
                    {t('roadmap_hero_sub', cur_lang)}
                </p>
            </div>
        </div>
    </div>
    """)

    # 1. Real-Time System Status Board
    st.markdown(f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 8px;">
        {t('roadmap_sec1_title', cur_lang)}
    </div>
    """, unsafe_allow_html=True)

    status_items = [
        (t("rm_status_core", cur_lang), t("rm_status_core_sub", cur_lang), t("status_operational", cur_lang), "#10B981"),
        (t("rm_status_conn", cur_lang), t("rm_status_conn_sub", cur_lang), t("status_active", cur_lang), "#10B981"),
        (t("rm_status_cache", cur_lang), t("rm_status_cache_sub", cur_lang), t("status_operational", cur_lang), "#10B981"),
        (t("rm_status_ml", cur_lang), t("rm_status_ml_sub", cur_lang), t("status_operational", cur_lang), "#10B981"),
        (t("rm_status_ai", cur_lang), t("rm_status_ai_sub", cur_lang), t("status_online", cur_lang), "#60A5FA"),
        (t("rm_status_audit", cur_lang), t("rm_status_audit_sub", cur_lang), t("status_verified", cur_lang), "#10B981")
    ]

    render_html('<div class="fuelpulse-suite-container">')
    sc1, sc2, sc3 = st.columns(3)
    for idx, (svc, tech, st_text, st_col) in enumerate(status_items):
        target_col = [sc1, sc2, sc3][idx % 3]
        with target_col:
            render_html(f"""
            <div style="background: rgba(14, 21, 38, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 6px; padding: 12px 14px; margin-bottom: 10px; height: 100%;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.85rem; font-weight: 700; color: #F9FAFB;">{svc}</span>
                    <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.68rem; font-weight: 800; color: {st_col}; background: rgba(255, 255, 255, 0.05); border: 1px solid {st_col}; padding: 2px 6px; border-radius: 4px;">{st_text}</span>
                </div>
                <div style="font-size: 0.75rem; color: #94A3B8;">{tech}</div>
            </div>
            """)
    render_html('</div>')

    st.write("")

    # 2. Three-Tier Engineering Roadmap
    st.markdown(f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 8px;">
        {t('roadmap_sec2_title', cur_lang)}
    </div>
    """, unsafe_allow_html=True)

    # Tier 1
    render_html(f"""
    <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-left: 4px solid #10B981; border-radius: 8px; padding: 18px 22px; margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.95rem; font-weight: 800; color: #10B981;">{t('tier_1_title', cur_lang)}</span>
            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; color: #10B981; font-weight: 700; background: rgba(16, 185, 129, 0.15); padding: 2px 8px; border-radius: 4px;">{t('status_completed', cur_lang)}</span>
        </div>
        <ul style="font-family: 'Inter', sans-serif; font-size: 0.85rem; line-height: 1.6; color: #94A3B8; margin: 0; padding-left: 20px;">
            <li><b style="color: #F9FAFB;">{t('t1_b1_title', cur_lang)}</b> {t('t1_b1_desc', cur_lang)}</li>
            <li><b style="color: #F9FAFB;">{t('t1_b2_title', cur_lang)}</b> {t('t1_b2_desc', cur_lang)}</li>
            <li><b style="color: #F9FAFB;">{t('t1_b3_title', cur_lang)}</b> {t('t1_b3_desc', cur_lang)}</li>
            <li><b style="color: #F9FAFB;">{t('t1_b4_title', cur_lang)}</b> {t('t1_b4_desc', cur_lang)}</li>
            <li><b style="color: #F9FAFB;">{t('t1_b5_title', cur_lang)}</b> {t('t1_b5_desc', cur_lang)}</li>
        </ul>
    </div>
    """)

    # Tier 2
    render_html(f"""
    <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-left: 4px solid #F5B942; border-radius: 8px; padding: 18px 22px; margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.95rem; font-weight: 800; color: #F5B942;">{t('tier_2_title', cur_lang)}</span>
            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; color: #F5B942; font-weight: 700; background: rgba(245, 185, 66, 0.15); padding: 2px 8px; border-radius: 4px;">{t('status_in_progress', cur_lang)}</span>
        </div>
        <ul style="font-family: 'Inter', sans-serif; font-size: 0.85rem; line-height: 1.6; color: #94A3B8; margin: 0; padding-left: 20px;">
            <li><b style="color: #F9FAFB;">{t('t2_b1_title', cur_lang)}</b> {t('t2_b1_desc', cur_lang)}</li>
            <li><b style="color: #F9FAFB;">{t('t2_b2_title', cur_lang)}</b> {t('t2_b2_desc', cur_lang)}</li>
            <li><b style="color: #F9FAFB;">{t('t2_b3_title', cur_lang)}</b> {t('t2_b3_desc', cur_lang)}</li>
            <li><b style="color: #F9FAFB;">{t('t2_b4_title', cur_lang)}</b> {t('t2_b4_desc', cur_lang)}</li>
        </ul>
    </div>
    """)

    # Tier 3
    render_html(f"""
    <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-left: 4px solid #60A5FA; border-radius: 8px; padding: 18px 22px; margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.95rem; font-weight: 800; color: #60A5FA;">{t('tier_3_title', cur_lang)}</span>
            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; color: #60A5FA; font-weight: 700; background: rgba(59, 130, 246, 0.15); padding: 2px 8px; border-radius: 4px;">{t('status_planned', cur_lang)}</span>
        </div>
        <ul style="font-family: 'Inter', sans-serif; font-size: 0.85rem; line-height: 1.6; color: #94A3B8; margin: 0; padding-left: 20px;">
            <li><b style="color: #F9FAFB;">{t('t3_b1_title', cur_lang)}</b> {t('t3_b1_desc', cur_lang)}</li>
            <li><b style="color: #F9FAFB;">{t('t3_b2_title', cur_lang)}</b> {t('t3_b2_desc', cur_lang)}</li>
            <li><b style="color: #F9FAFB;">{t('t3_b3_title', cur_lang)}</b> {t('t3_b3_desc', cur_lang)}</li>
        </ul>
    </div>
    """)

