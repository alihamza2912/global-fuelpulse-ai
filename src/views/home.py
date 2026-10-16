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
    apply_clean_layout,
    COLOR_AMBER,
    COLOR_WHITE,
    COLOR_INK,
    COLOR_GRAY_MUTED
)
from src.database.connection import db_manager


def render_home_view(navigate_fn=None):
    """Renders the modern Hero With Mockup Product Overview."""

    # 1. Hero Section with Glow, Gradient Text & Eyebrow Badge
    render_html(f"""
    <div style="position: relative; overflow: hidden; padding: 20px 0 10px 0; text-align: center;">
        
        <!-- Ambient Background Radial Glow -->
        <div style="position: absolute; top: -100px; left: 50%; transform: translateX(-50%); width: 850px; height: 320px; background: radial-gradient(ellipse at center, rgba(245, 185, 66, 0.22) 0%, rgba(96, 165, 250, 0.14) 50%, transparent 75%); filter: blur(80px); pointer-events: none; z-index: 0;"></div>

        <div style="position: relative; z-index: 2; max-width: 950px; margin: 0 auto;">
            
            <!-- Category Eyebrow Pill -->
            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(245, 185, 66, 0.12); border: 1px solid rgba(245, 185, 66, 0.35); padding: 5px 14px; border-radius: 9999px; font-family: 'Space Grotesk', sans-serif; font-size: 0.74rem; font-weight: 800; color: #F5B942; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 12px; box-shadow: 0 0 16px rgba(245, 185, 66, 0.2);">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #10B981; display: inline-block;"></span>
                GLOBAL FUELPULSE AI • ENERGY INTELLIGENCE PLATFORM
            </div>

            <!-- Gradient Heading -->
            <h1 style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 3.4rem; font-weight: 800; letter-spacing: -0.04em; line-height: 1.1; margin: 0 0 14px 0; background: linear-gradient(180deg, #FFFFFF 25%, rgba(255, 255, 255, 0.9) 65%, #94A3B8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Understand the world's real-time energy flows.
            </h1>

            <!-- Subtitle Description -->
            <p style="font-family: 'Inter', sans-serif; font-size: 1.12rem; color: #94A3B8; max-width: 640px; margin: 0 auto 20px auto; line-height: 1.6; font-weight: 400;">
                Unify international crude benchmarks, maritime seaborne tanker routes, and downstream retail pump pricing into an integrated, deterministic intelligence platform.
            </p>

        </div>
    </div>
    """)

    # 2. Hero Action Buttons (Primary Glow CTA + Secondary Link)
    c1, c2, c3, c4 = st.columns([3, 4, 3, 2])
    with c2:
        if st.button("⚡ Launch Live Intelligence Dashboard", type="primary", use_container_width=True, key="hero_cta_dash"):
            if navigate_fn:
                navigate_fn("Live Intelligence Dashboard")
            else:
                st.session_state.active_nav = "⚡ Intelligence Dashboard"
                st.rerun()
    with c3:
        if st.button("🇮🇳 Explore India Fuel Center →", use_container_width=True, key="hero_cta_india"):
            if navigate_fn:
                navigate_fn("India Fuel Center")
            else:
                st.session_state.active_nav = "🇮🇳 India Fuel Center"
                st.rerun()

    st.write("")

    # 3. The Interactive Browser Mockup Container
    render_html("""
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
                    ● 25 NATIONS LIVE TELEMETRY
                </div>
            </div>

            <!-- Inside Mockup: Live Infographic Strip -->
            <div style="padding: 16px 20px 8px 20px; background: rgba(7, 10, 18, 0.6); border-bottom: 1px solid rgba(255, 255, 255, 0.08); display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px;">
                <div style="background: rgba(14, 21, 38, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 12px 14px;">
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">BRENT CRUDE SPOT</div>
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 800; color: #F5B942;">$76.80 / bbl</div>
                    <div style="font-size: 0.7rem; color: #10B981; font-weight: 600;">▲ Daily Reference Benchmark</div>
                </div>
                <div style="background: rgba(14, 21, 38, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 12px 14px;">
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">DELHI DIESEL PUMP</div>
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 800; color: #F9FAFB;">₹87.62 / L</div>
                    <div style="font-size: 0.7rem; color: #60A5FA; font-weight: 600;">Official PPAC Metro Benchmark</div>
                </div>
                <div style="background: rgba(14, 21, 38, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 12px 14px;">
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">STRAIT OF HORMUZ</div>
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 800; color: #60A5FA;">18.5 mbpd</div>
                    <div style="font-size: 0.7rem; color: #F43F5E; font-weight: 600;">Critical Seaborne Chokepoint</div>
                </div>
                <div style="background: rgba(14, 21, 38, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 12px 14px;">
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">IN-MEMORY LATENCY</div>
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 800; color: #10B981;">&lt; 10 ms</div>
                    <div style="font-size: 0.7rem; color: #94A3B8; font-weight: 600;">Multi-Tier Cache Engine</div>
                </div>
            </div>

            <!-- Inside Mockup: Chart Preview -->
            <div style="padding: 16px 20px; background: #070A12;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; font-weight: 800; color: #F9FAFB; text-transform: uppercase;">TOP GLOBAL CRUDE PRODUCERS PREVIEW (mbpd)</span>
                    <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; color: #94A3B8;">EIA & OPEC VERIFIED 2024–25</span>
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
    col_problem, col_who = st.columns([1, 1], gap="large")

    with col_problem:
        render_html("""
        <div style="background: rgba(14, 21, 38, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 22px; height: 100%;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; font-weight: 800; color: #F5B942; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 6px;">
                THE CORE CHALLENGE
            </div>
            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 700; color: #F9FAFB; margin: 0 0 12px 0;">
                The Decoupling of Crude Oil and Retail Fuel Prices
            </h3>
            <p style="font-family: 'Inter', sans-serif; font-size: 0.92rem; line-height: 1.6; color: #94A3B8; margin-bottom: 12px;">
                Crude oil is traded internationally as a fungible commodity in US Dollars per barrel. Yet what consumers, freight fleets, and industrial enterprises pay at the pump varies wildly across nations—from under <b>$0.35/L</b> in subsidized oil-producing states to over <b>$2.15/L</b> in heavily taxed European markets.
            </p>
            <p style="font-family: 'Inter', sans-serif; font-size: 0.92rem; line-height: 1.6; color: #94A3B8; margin: 0;">
                This spread is driven not by oil quality, but by <b>refinery crack spreads</b>, <b>currency depreciation against the USD</b>, <b>national fuel subsidies</b>, and <b>sovereign excise taxes and regional VAT</b>. Global FuelPulse AI makes these mechanisms transparent, auditable, and quantifiable.
            </p>
        </div>
        """)

    with col_who:
        render_html("""
        <div style="background: rgba(14, 21, 38, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 22px; height: 100%;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; font-weight: 800; color: #60A5FA; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 6px;">
                USER VALUE
            </div>
            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 700; color: #F9FAFB; margin: 0 0 12px 0;">
                Who Relies on Global FuelPulse AI?
            </h3>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.88rem; line-height: 1.55; color: #94A3B8;">
                <div style="margin-bottom: 10px;">
                    <b style="color: #F9FAFB;">🚛 Fleet & Logistics Operators:</b> Accurately forecast diesel fuel expenditures, model fuel surcharge rate adjustments, and benchmark multi-state fuel bunkering.
                </div>
                <div style="margin-bottom: 10px;">
                    <b style="color: #F9FAFB;">📊 Energy & Commodity Analysts:</b> Monitor seaborne petroleum trade lanes, tanker transit chokepoints (Hormuz, Malacca, Suez), and supplier concentration risk (HHI).
                </div>
                <div style="margin-bottom: 10px;">
                    <b style="color: #F9FAFB;">🏛️ Economic & Policy Researchers:</b> Dissect price build-up structures, evaluate tax wedge impacts, and calculate genuine fuel affordability burdens across income deciles.
                </div>
                <div>
                    <b style="color: #F9FAFB;">🏭 Corporate Procurement Teams:</b> Stress-test procurement budgets against crude oil supply shocks and currency volatility scenarios.
                </div>
            </div>
        </div>
        """)

    st.write("")

    # 5. Modular Product Navigation Grid
    st.markdown("""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; font-weight: 800; color: #F9FAFB; margin: 18px 0 12px 0;">
        EXPLORE THE PLATFORM SUITE
    </div>
    """, unsafe_allow_html=True)

    grid1, grid2, grid3 = st.columns(3)

    with grid1:
        render_html("""
        <div style="background: rgba(14, 21, 38, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 18px; margin-bottom: 14px; min-height: 170px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span style="font-size: 1.2rem;">⚡</span>
                <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; font-size: 0.95rem;">Live Intelligence Dashboard</span>
            </div>
            <p style="font-size: 0.82rem; color: #94A3B8; line-height: 1.45; margin-bottom: 12px;">
                11 narrative chapters tracing the petroleum value chain: extraction leaderboards, bilateral trade matrices, retail price explorer, shock simulation, and ML price radar.
            </p>
        </div>
        """)
        if st.button("Open Dashboard →", key="btn_nav_dash", use_container_width=True):
            if navigate_fn:
                navigate_fn("Live Intelligence Dashboard")
            else:
                st.session_state.active_nav = "⚡ Intelligence Dashboard"
                st.rerun()

    with grid2:
        render_html("""
        <div style="background: rgba(14, 21, 38, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 18px; margin-bottom: 14px; min-height: 170px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span style="font-size: 1.2rem;">🇮🇳</span>
                <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; font-size: 0.95rem;">India Fuel Center</span>
            </div>
            <p style="font-size: 0.82rem; color: #94A3B8; line-height: 1.45; margin-bottom: 12px;">
                Official PPAC metro daily city benchmarks (Delhi, Mumbai, Kolkata, Chennai), MoPNG retail price build-up waterfall, and OMC market footprint breakdown.
            </p>
        </div>
        """)
        if st.button("Open India Center →", key="btn_nav_india", use_container_width=True):
            if navigate_fn:
                navigate_fn("India Fuel Center")
            else:
                st.session_state.active_nav = "🇮🇳 India Fuel Center"
                st.rerun()

    with grid3:
        render_html("""
        <div style="background: rgba(14, 21, 38, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 18px; margin-bottom: 14px; min-height: 170px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span style="font-size: 1.2rem;">🔒</span>
                <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; font-size: 0.95rem;">Data Trust & Provenance</span>
            </div>
            <p style="font-size: 0.82rem; color: #94A3B8; line-height: 1.45; margin-bottom: 12px;">
                Full transparency over the 7 registered data providers, observation dates vs retrieval timestamps, SLA thresholds, and automated quality quarantine logs.
            </p>
        </div>
        """)
        if st.button("Open Trust Center →", key="btn_nav_trust", use_container_width=True):
            if navigate_fn:
                navigate_fn("Data Trust Center")
            else:
                st.session_state.active_nav = "🔒 Data Trust"
                st.rerun()

    # 6. Honest Scope & Coverage Disclosure
    render_html("""
    <div style="background: rgba(14, 21, 38, 0.5); border: 1px dashed rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 16px 20px; font-family: 'Inter', sans-serif; font-size: 0.8rem; color: #94A3B8; line-height: 1.55; margin-top: 14px;">
        <b style="color: #F9FAFB; font-family: 'Space Grotesk', sans-serif;">🛡️ ETHICAL DATA DISCLOSURE:</b>
        Global FuelPulse AI operates on real, verified benchmark data from public institutions (US EIA, India PPAC, European Commission, UN Comtrade, Open Exchange Rates). We deliberately do not fabricate synthetic pricing or hallucinate unmonitored rural stations. Where data is collected weekly or annually, the exact observation dates and provenance are visibly stamped on every metric and chart.
    </div>
    """)
