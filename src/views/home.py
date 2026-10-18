"""
GLOBAL FUELPULSE AI — HOME / PRODUCT OVERVIEW VIEW
Modern Hero With Mockup design inspired by 21st.dev / shadcn:
Gradient typography, ambient glow backdrop, device browser mockup frame,
and seamless drill-down navigation.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.ui_components import (
    render_html,
    render_instrument_card,
    get_brand_logo_svg,
    get_fuel_client_logo_html,
    get_lucide_icon_svg,
    apply_clean_layout,
    COLOR_AMBER,
    COLOR_WHITE,
    COLOR_INK,
    COLOR_GRAY_MUTED
)
from src.database.connection import db_manager
from src.localization.i18n import t, get_current_language


def render_home_view(navigate_fn=None):
    """Renders the modern Hero With Mockup Product Overview."""
    cur_lang = get_current_language()

    # 1. Hero Section with Glow, Gradient Text & Eyebrow Badge
    render_html(f"""
    <div style="position: relative; overflow: hidden; padding: 20px 0 10px 0; text-align: center;">
        
        <!-- Ambient Background Radial Glow -->
        <div style="position: absolute; top: -100px; left: 50%; transform: translateX(-50%); width: 850px; height: 320px; background: radial-gradient(ellipse at center, rgba(245, 185, 66, 0.22) 0%, rgba(96, 165, 250, 0.14) 50%, transparent 75%); filter: blur(80px); pointer-events: none; z-index: 0;"></div>

        <div style="position: relative; z-index: 2; max-width: 950px; margin: 0 auto;">
            
            <!-- Category Eyebrow Pill -->
            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(245, 185, 66, 0.12); border: 1px solid rgba(245, 185, 66, 0.35); padding: 5px 14px; border-radius: 9999px; font-family: 'Space Grotesk', sans-serif; font-size: 0.74rem; font-weight: 800; color: #F5B942; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 12px; box-shadow: 0 0 16px rgba(245, 185, 66, 0.2);">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #10B981; display: inline-block;"></span>
                {t('home_eyebrow', cur_lang)}
            </div>

            <!-- Gradient Heading -->
            <h1 class="fuelpulse-hero-title" style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 3.4rem; font-weight: 800; letter-spacing: -0.04em; line-height: 1.1; margin: 0 0 14px 0; background: linear-gradient(180deg, #FFFFFF 25%, rgba(255, 255, 255, 0.9) 65%, #94A3B8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {t('home_hero_title', cur_lang)}
            </h1>

            <!-- Subtitle Description -->
            <p class="fuelpulse-hero-desc" style="font-family: 'Inter', sans-serif; font-size: 1.12rem; color: #94A3B8; max-width: 640px; margin: 0 auto 20px auto; line-height: 1.6; font-weight: 400;">
                {t('home_hero_subtitle', cur_lang)}
            </p>

        </div>
    </div>
    """)

    # 2. Hero Action Buttons (Balanced 2-CTA Grid)
    render_html('<div class="fuelpulse-hero-actions">')
    c2, c3 = st.columns([1, 1], gap="medium")
    with c2:
        if st.button(t('home_cta_dashboard', cur_lang), type="primary", use_container_width=True, key="hero_cta_dash"):
            if navigate_fn:
                navigate_fn("Live Intelligence Dashboard")
            else:
                st.session_state.active_nav = "⚡ Intelligence Dashboard"
                st.rerun()
    with c3:
        if st.button(t('home_cta_india', cur_lang), type="primary", use_container_width=True, key="hero_cta_india"):
            if navigate_fn:
                navigate_fn("India Fuel Center")
            else:
                st.session_state.active_nav = "🇮🇳 India Fuel Center"
                st.rerun()
    render_html('</div>')

    st.write("")

    # Fetch live headline benchmarks from database with current benchmarks
    brent_val = "$84.20 / bbl"
    delhi_diesel_val = "₹95.20 / L"
    try:
        with db_manager.engine.connect() as conn:
            r_brent = conn.execute(db_manager.safe_sql(
                "SELECT value FROM fact_energy_indicator WHERE indicator_code='BRENT_CRUDE_SPOT' ORDER BY period DESC LIMIT 1"
            )).fetchone()
            if r_brent:
                brent_val = f"${float(r_brent[0]):.2f} / bbl"

            r_delhi = conn.execute(db_manager.safe_sql(
                "SELECT price_local FROM fuel_prices WHERE country_iso3='IND' AND location_id='IND_DEL' AND fuel_type='diesel' ORDER BY observation_date DESC LIMIT 1"
            )).fetchone()
            if r_delhi:
                delhi_diesel_val = f"₹{float(r_delhi[0]):.2f} / L"
    except Exception:
        pass

    # 3. The Interactive Browser Mockup Container
    render_html(f"""
    <div style="position: relative; max-width: 1100px; margin: 8px auto 28px auto; z-index: 10;">
        <div style="background: rgba(14, 21, 38, 0.95); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.16); box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7), 0 0 40px rgba(245, 185, 66, 0.15); border-radius: 12px; overflow: hidden;">
            
            <!-- MacOS Window Header -->
            <div style="background: #151F38; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding: 10px 18px; display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="width: 11px; height: 11px; border-radius: 50%; background: #F43F5E; display: inline-block;"></span>
                    <span style="width: 11px; height: 11px; border-radius: 50%; background: #F5B942; display: inline-block;"></span>
                    <span style="width: 11px; height: 11px; border-radius: 50%; background: #10B981; display: inline-block;"></span>
                    <span style="font-family: 'Space Grotesk', monospace; font-size: 0.75rem; color: #94A3B8; margin-left: 12px;">global-fuelpulse-ai.streamlit.app</span>
                </div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; font-weight: 800; color: #F5B942; background: rgba(245, 185, 66, 0.15); border: 1px solid rgba(245, 185, 66, 0.3); padding: 3px 9px; border-radius: 4px;">
                    ● {t('home_mockup_telemetry', cur_lang)}
                </div>
            </div>

            <!-- Inside Mockup: Live Infographic Strip -->
            <div class="fuelpulse-mockup-strip" style="padding: 16px 20px 8px 20px; background: rgba(7, 10, 18, 0.6); border-bottom: 1px solid rgba(255, 255, 255, 0.08); display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px;">
                <div style="background: rgba(14, 21, 38, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 12px 14px;">
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">{t('home_brent_spot', cur_lang)}</div>
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 800; color: #F5B942;">{brent_val}</div>
                    <div style="font-size: 0.7rem; color: #10B981; font-weight: 600;">▲ {t('home_brent_sub', cur_lang)}</div>
                </div>
                <div style="background: rgba(14, 21, 38, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 12px 14px;">
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">{t('home_delhi_diesel', cur_lang)}</div>
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 800; color: #F9FAFB;">{delhi_diesel_val}</div>
                    <div style="font-size: 0.7rem; color: #60A5FA; font-weight: 600;">{t('home_delhi_sub', cur_lang)}</div>
                </div>
                <div style="background: rgba(14, 21, 38, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 12px 14px;">
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">{t('home_hormuz_title', cur_lang)}</div>
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 800; color: #60A5FA;">18.5 mbpd</div>
                    <div style="font-size: 0.7rem; color: #F43F5E; font-weight: 600;">{t('home_hormuz_sub', cur_lang)}</div>
                </div>
                <div style="background: rgba(14, 21, 38, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 12px 14px;">
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">{t('home_latency_title', cur_lang)}</div>
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 800; color: #10B981;">&lt; 10 ms</div>
                    <div style="font-size: 0.7rem; color: #94A3B8; font-weight: 600;">{t('home_latency_sub', cur_lang)}</div>
                </div>
            </div>

            <!-- Inside Mockup: Chart Preview -->
            <div style="padding: 16px 20px; background: #070A12;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; font-weight: 800; color: #F9FAFB; text-transform: uppercase;">{t('home_chart_title', cur_lang)}</span>
                    <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; color: #94A3B8;">{t('home_chart_sub', cur_lang)}</span>
                </div>
            </div>
        </div>
    </div>
    """)

    # Top Producers Preview Bar Chart rendered right inside the mockup space
    preview_df = pd.DataFrame([
        {"Country": "United States", "Production": 13.2},
        {"Country": "Saudi Arabia", "Production": 9.0},
        {"Country": "Russia", "Production": 9.1},
        {"Country": "Canada", "Production": 4.9},
        {"Country": "Iraq", "Production": 4.3}
    ])
    fig_mockup = px.bar(
        preview_df,
        x="Production",
        y="Country",
        orientation="h",
        color="Production",
        color_continuous_scale=[[0, "#1E293B"], [0.5, "#F5B942"], [1, "#FFDD80"]],
        labels={"Production": "mbpd", "Country": ""}
    )
    fig_mockup.update_traces(marker=dict(line=dict(color="rgba(255, 255, 255, 0.2)", width=1)))
    apply_clean_layout(
        fig_mockup,
        height=220,
        margin_l=120,
        margin_b=30,
        showlegend=False,
        yaxis=dict(autorange="reversed"),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_mockup, use_container_width=True, key="fig_home_mockup_chart")

    st.write("")

    # 4. Problem Solved & Executive Perspective
    render_html(f"""
    <div class="fuelpulse-perspective-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; align-items: stretch; width: 100%; box-sizing: border-box;">
        <div style="background: rgba(14, 21, 38, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 22px; display: flex; flex-direction: column; justify-content: flex-start; height: 100%; box-sizing: border-box;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; font-weight: 800; color: #F5B942; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 6px;">
                {t('home_challenge_eyebrow', cur_lang)}
            </div>
            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 700; color: #F9FAFB; margin: 0 0 12px 0;">
                {t('home_challenge_title', cur_lang)}
            </h3>
            <p style="font-family: 'Inter', sans-serif; font-size: 0.92rem; line-height: 1.6; color: #94A3B8; margin-bottom: 12px;">
                {t('home_challenge_p1', cur_lang)}
            </p>
            <p style="font-family: 'Inter', sans-serif; font-size: 0.92rem; line-height: 1.6; color: #94A3B8; margin: 0;">
                {t('home_challenge_p2', cur_lang)}
            </p>
        </div>
        <div style="background: rgba(14, 21, 38, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 22px; display: flex; flex-direction: column; justify-content: flex-start; height: 100%; box-sizing: border-box;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; font-weight: 800; color: #60A5FA; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 6px;">
                {t('home_value_eyebrow', cur_lang)}
            </div>
            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 700; color: #F9FAFB; margin: 0 0 12px 0;">
                {t('home_value_title', cur_lang)}
            </h3>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.88rem; line-height: 1.55; color: #94A3B8;">
                <div style="margin-bottom: 10px;">
                    <b style="color: #F9FAFB;">{t('home_val_fleet_title', cur_lang)}:</b> {t('home_val_fleet_desc', cur_lang)}
                </div>
                <div style="margin-bottom: 10px;">
                    <b style="color: #F9FAFB;">{t('home_val_analyst_title', cur_lang)}:</b> {t('home_val_analyst_desc', cur_lang)}
                </div>
                <div style="margin-bottom: 10px;">
                    <b style="color: #F9FAFB;">{t('home_val_policy_title', cur_lang)}:</b> {t('home_val_policy_desc', cur_lang)}
                </div>
                <div>
                    <b style="color: #F9FAFB;">{t('home_val_corp_title', cur_lang)}:</b> {t('home_val_corp_desc', cur_lang)}
                </div>
            </div>
        </div>
    </div>
    """)

    st.write("")

    # 5. Modular Product Navigation Grid
    st.markdown(f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; font-weight: 800; color: #F9FAFB; margin: 18px 0 12px 0;">
        {t('home_suite_title', cur_lang)}
    </div>
    """, unsafe_allow_html=True)

    render_html('<div class="fuelpulse-suite-container">')
    grid1, grid2, grid3 = st.columns(3)

    with grid1:
        render_html(f"""
        <div class="fuelpulse-product-card" style="background: rgba(14, 21, 38, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 18px; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                {get_lucide_icon_svg("chart-no-axes-combined", size=20, color="#F5B942")}
                <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; font-size: 0.95rem;">{t('home_card_dash_title', cur_lang)}</span>
            </div>
            <p style="font-size: 0.82rem; color: #94A3B8; line-height: 1.45; margin: 0;">
                {t('home_card_dash_desc', cur_lang)}
            </p>
        </div>
        """)
        if st.button(t('home_btn_open_dash', cur_lang), type="primary", key="btn_nav_dash", use_container_width=True):
            if navigate_fn:
                navigate_fn("Live Intelligence Dashboard")
            else:
                st.session_state.active_nav = "⚡ Intelligence Dashboard"
                st.rerun()

    with grid2:
        render_html(f"""
        <div class="fuelpulse-product-card" style="background: rgba(14, 21, 38, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 18px; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                {get_lucide_icon_svg("map-pinned", size=20, color="#60A5FA")}
                <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; font-size: 0.95rem;">{t('home_card_india_title', cur_lang)}</span>
            </div>
            <p style="font-size: 0.82rem; color: #94A3B8; line-height: 1.45; margin: 0;">
                {t('home_card_india_desc', cur_lang)}
            </p>
        </div>
        """)
        if st.button(t('home_btn_open_india', cur_lang), type="primary", key="btn_nav_india", use_container_width=True):
            if navigate_fn:
                navigate_fn("India Fuel Center")
            else:
                st.session_state.active_nav = "🇮🇳 India Fuel Center"
                st.rerun()

    with grid3:
        render_html(f"""
        <div class="fuelpulse-product-card" style="background: rgba(14, 21, 38, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 18px; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                {get_lucide_icon_svg("shield-check", size=20, color="#34D399")}
                <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; font-size: 0.95rem;">{t('home_card_trust_title', cur_lang)}</span>
            </div>
            <p style="font-size: 0.82rem; color: #94A3B8; line-height: 1.45; margin: 0;">
                {t('home_card_trust_desc', cur_lang)}
            </p>
        </div>
        """)
        if st.button(t('home_btn_open_trust', cur_lang), type="primary", key="btn_nav_trust", use_container_width=True):
            if navigate_fn:
                navigate_fn("Data Trust Center")
            else:
                st.session_state.active_nav = "🔒 Data Trust"
                st.rerun()
    render_html('</div>')

    # 5b. Feature 09: AI Energy Market Analyst Spotlight
    render_html(f"""
    <div style="background: radial-gradient(circle at 10% 20%, rgba(245, 185, 66, 0.12) 0%, rgba(14, 21, 38, 0.95) 70%), #070A12; border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 12px; padding: 22px 26px; margin: 22px 0 18px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                {get_lucide_icon_svg("bot", size=24, color="#F5B942")}
                <div>
                    <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem; font-weight: 800; color: #F5B942; letter-spacing: 0.08em; text-transform: uppercase;">{t('home_f9_category', cur_lang)}</span>
                    <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.22rem; font-weight: 800; color: #F9FAFB; margin: 2px 0 0 0;">{t('home_f9_title', cur_lang)}</h3>
                </div>
            </div>
            <span style="background: rgba(16, 185, 129, 0.18); color: #34D399; font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem; font-weight: 800; padding: 4px 12px; border-radius: 999px; border: 1px solid rgba(16, 185, 129, 0.4);">
                {t('home_f9_badge', cur_lang)}
            </span>
        </div>
        <p style="font-family: 'Inter', sans-serif; font-size: 0.9rem; color: #94A3B8; margin: 0 0 16px 0; line-height: 1.6;">
            {t('home_f9_desc', cur_lang)}
        </p>
    </div>
    """)

    col_h_studio, col_h_dash = st.columns([1, 1], gap="medium")
    with col_h_studio:
        st.link_button(
            t('home_btn_f9_studio', cur_lang),
            url="/AI_Analyst",
            use_container_width=True,
            type="primary"
        )
    with col_h_dash:
        if st.button(t('home_btn_f9_dash', cur_lang), key="home_btn_ai_dash", use_container_width=True, type="secondary"):
            if navigate_fn:
                navigate_fn("Live Intelligence Dashboard")
            else:
                st.session_state.active_nav = "⚡ Intelligence Dashboard"
                st.rerun()

    # 6. Honest Scope & Coverage Disclosure
    render_html(f"""
    <div style="background: rgba(14, 21, 38, 0.5); border: 1px dashed rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 16px 20px; font-family: 'Inter', sans-serif; font-size: 0.8rem; color: #94A3B8; line-height: 1.55; margin-top: 14px;">
        <b style="color: #F9FAFB; font-family: 'Space Grotesk', sans-serif;">{t('home_disclosure_title', cur_lang)}</b>
        {t('home_disclosure_desc', cur_lang)}
    </div>
    """)
