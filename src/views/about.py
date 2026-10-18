"""
GLOBAL FUELPULSE AI — ABOUT THE PROJECT VIEW
Comprehensive exploration of energy market forces, geological vs tax drivers,
petroleum pass-through mechanics, and system design philosophy.
"""

import streamlit as st
from src.ui_components import (
    render_html,
    render_instrument_card,
    get_fuel_client_logo_html,
    get_lucide_icon_svg,
    COLOR_AMBER,
    COLOR_WHITE,
    COLOR_INK,
    COLOR_GRAY_MUTED
)
from src.localization.i18n import t, get_current_language


def render_about_view(navigate_fn=None):
    """Renders the About the Project dossier."""
    cur_lang = get_current_language()

    render_html(f"""
    <div style="background: radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.12) 0%, rgba(14, 21, 38, 0.95) 70%), #070A12; border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 12px; padding: 26px 30px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
            <div>
                {get_fuel_client_logo_html()}
                <h1 style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 2rem; font-weight: 800; color: #F9FAFB; margin: 6px 0 8px 0; letter-spacing: -0.02em;">
                    {t('about_hero_title', cur_lang)}
                </h1>
                <p style="font-family: 'Inter', sans-serif; font-size: 1rem; color: #94A3B8; margin: 0; max-width: 820px; line-height: 1.55;">
                    {t('about_hero_sub', cur_lang)}
                </p>
            </div>
        </div>
    </div>
    """)

    # 1. Mission and Core Purpose
    st.markdown(f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 12px;">
        {t('about_sec1_title', cur_lang)}
    </div>
    """, unsafe_allow_html=True)

    render_html("""
    <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 22px; margin-bottom: 24px; font-family: 'Inter', sans-serif; font-size: 0.92rem; line-height: 1.65; color: #94A3B8;">
        <p style="margin-top: 0;">
            Energy is the invisible substrate of modern civilization. Every freight container moving across oceans, every haulage truck delivering goods between cities, and every agricultural tractor tilling fields operates on refined petroleum distillates. Yet public understanding of fuel pricing remains distorted by political rhetoric and oversimplified headlines.
        </p>
        <p style="margin-bottom: 0;">
            <b>Global FuelPulse AI</b> was engineered to replace guesswork with empirical, deterministic market intelligence. We track physical oil from the wellhead to seaborne tankers, through complex refinery hydrocrackers, past sovereign fiscal tax tollgates, and into the commercial fuel pump. By integrating real-world datasets across 25 sovereign economies and Indian metro centers, we give decision-makers an auditable lens into energy economics.
        </p>
    </div>
    """)

    # 2. Geological Reality vs Sovereign Tax Regimes
    st.markdown(f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 12px;">
        {t('about_sec2_title', cur_lang)}
    </div>
    """, unsafe_allow_html=True)

    col_geo, col_tax = st.columns(2, gap="medium")
    with col_geo:
        render_html(f"""
        <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 20px; height: 100%;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                {get_lucide_icon_svg("globe", size=20, color="#F5B942")}
                <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; color: #F5B942; font-size: 1rem;">{t('about_geo_title', cur_lang)}</span>
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.88rem; line-height: 1.55; color: #94A3B8;">
                <p>{t('about_geo_intro', cur_lang)}</p>
                <ul style="margin: 0; padding-left: 20px;">
                    <li>{t('about_geo_b1', cur_lang)}</li>
                    <li>{t('about_geo_b2', cur_lang)}</li>
                    <li>{t('about_geo_b3', cur_lang)}</li>
                </ul>
            </div>
        </div>
        """)

    with col_tax:
        render_html(f"""
        <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 20px; height: 100%;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                {get_lucide_icon_svg("landmark", size=20, color="#60A5FA")}
                <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; color: #60A5FA; font-size: 1rem;">{t('about_tax_title', cur_lang)}</span>
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.88rem; line-height: 1.55; color: #94A3B8;">
                <p>{t('about_tax_intro', cur_lang)}</p>
                <ul style="margin: 0; padding-left: 20px;">
                    <li>{t('about_tax_b1', cur_lang)}</li>
                    <li>{t('about_tax_b2', cur_lang)}</li>
                    <li>{t('about_tax_b3', cur_lang)}</li>
                </ul>
            </div>
        </div>
        """)

    st.write("")

    # 3. The 5-Step Refined Product Pass-Through Chain
    st.markdown(f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 12px;">
        {t('about_sec3_title', cur_lang)}
    </div>
    """, unsafe_allow_html=True)

    render_html(f"""
    <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 22px; margin-bottom: 24px;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px;">
            <div style="background: rgba(7, 10, 18, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 14px;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 800; color: #F5B942; margin-bottom: 4px;">STAGE 01</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; margin-bottom: 6px;">{t('about_stage1_title', cur_lang)}</div>
                <div style="font-size: 0.8rem; color: #94A3B8; line-height: 1.45;">{t('about_stage1_desc', cur_lang)}</div>
            </div>
            <div style="background: rgba(7, 10, 18, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 14px;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 800; color: #60A5FA; margin-bottom: 4px;">STAGE 02</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; margin-bottom: 6px;">{t('about_stage2_title', cur_lang)}</div>
                <div style="font-size: 0.8rem; color: #94A3B8; line-height: 1.45;">{t('about_stage2_desc', cur_lang)}</div>
            </div>
            <div style="background: rgba(7, 10, 18, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 14px;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 800; color: #34D399; margin-bottom: 4px;">STAGE 03</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; margin-bottom: 6px;">{t('about_stage3_title', cur_lang)}</div>
                <div style="font-size: 0.8rem; color: #94A3B8; line-height: 1.45;">{t('about_stage3_desc', cur_lang)}</div>
            </div>
            <div style="background: rgba(7, 10, 18, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 14px;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 800; color: #F472B6; margin-bottom: 4px;">STAGE 04</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; margin-bottom: 6px;">{t('about_stage4_title', cur_lang)}</div>
                <div style="font-size: 0.8rem; color: #94A3B8; line-height: 1.45;">{t('about_stage4_desc', cur_lang)}</div>
            </div>
            <div style="background: rgba(7, 10, 18, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 14px;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 800; color: #A78BFA; margin-bottom: 4px;">STAGE 05</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; margin-bottom: 6px;">{t('about_stage5_title', cur_lang)}</div>
                <div style="font-size: 0.8rem; color: #94A3B8; line-height: 1.45;">{t('about_stage5_desc', cur_lang)}</div>
            </div>
        </div>
    </div>
    """)

    # 4. System Design Philosophy
    st.markdown(f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 12px;">
        {t('about_sec4_title', cur_lang)}
    </div>
    """, unsafe_allow_html=True)

    render_html(f"""
    <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 22px; font-family: 'Inter', sans-serif; font-size: 0.9rem; line-height: 1.6; color: #94A3B8;">
        <div style="margin-bottom: 12px;">
            <b style="color: #F9FAFB;">{t('about_phil1_title', cur_lang)}</b> {t('about_phil1_desc', cur_lang)}
        </div>
        <div style="margin-bottom: 12px;">
            <b style="color: #F9FAFB;">{t('about_phil2_title', cur_lang)}</b> {t('about_phil2_desc', cur_lang)}
        </div>
        <div>
            <b style="color: #F9FAFB;">{t('about_phil3_title', cur_lang)}</b> {t('about_phil3_desc', cur_lang)}
        </div>
    </div>
    """)
