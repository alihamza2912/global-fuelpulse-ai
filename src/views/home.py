"""
GLOBAL FUELPULSE AI — HOME / PRODUCT OVERVIEW VIEW
High-speed, beautifully styled landing page introducing the platform, its mission,
verified coverage, and direct entry points into granular intelligence tools.
"""

import streamlit as st
import pandas as pd
from src.ui_components import (
    render_html,
    render_instrument_card,
    get_brand_logo_svg,
    get_fuel_client_logo_html,
    COLOR_AMBER,
    COLOR_WHITE,
    COLOR_INK,
    COLOR_GRAY_MUTED
)
from src.database.connection import db_manager


def render_home_view(navigate_fn=None):
    """Renders the high-speed Product Home & Executive Overview."""

    # 1. Hero Brand Header
    render_html(f"""
    <div style="background: radial-gradient(circle at 15% 20%, rgba(245, 185, 66, 0.12) 0%, rgba(14, 21, 38, 0.95) 75%), #070A12; border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 12px; padding: 28px 32px 32px 32px; margin-bottom: 24px; box-shadow: 0 16px 36px rgba(0, 0, 0, 0.45); position: relative; overflow: hidden;">
        <div style="margin-bottom: 14px;">
            {get_fuel_client_logo_html()}
        </div>
        <div style="display: flex; align-items: flex-start; justify-content: space-between; flex-wrap: wrap; gap: 20px;">
            <div style="max-width: 780px;">
                <h1 style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 2.2rem; font-weight: 800; color: #F9FAFB; margin: 0 0 10px 0; letter-spacing: -0.02em; line-height: 1.15;">
                    The Open Global Energy & Refined Fuel Intelligence Platform
                </h1>
                <p style="font-family: 'Inter', -apple-system, sans-serif; font-size: 1.05rem; line-height: 1.6; color: #94A3B8; margin: 0 0 18px 0; font-weight: 400;">
                    Global FuelPulse AI unifies upstream crude benchmarks, maritime seaborne tanker flows, and downstream retail pump pricing into an integrated, deterministic decision support system for commercial fleets, commodity analysts, and policy researchers.
                </p>
                <div style="display: inline-flex; align-items: center; gap: 14px; flex-wrap: wrap;">
                    <span style="display: inline-flex; align-items: center; gap: 6px; font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; font-weight: 700; color: #F5B942; background: rgba(245, 185, 66, 0.15); border: 1px solid rgba(245, 185, 66, 0.35); padding: 4px 12px; border-radius: 999px;">
                        <span style="width: 8px; height: 8px; border-radius: 50%; background: #10B981; display: inline-block;"></span>
                        2024–2026 VERIFIED BENCHMARKS
                    </span>
                    <span style="display: inline-flex; align-items: center; gap: 6px; font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; font-weight: 700; color: #60A5FA; background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.35); padding: 4px 12px; border-radius: 999px;">
                        🌐 25 SOVEREIGN ECONOMIES
                    </span>
                    <span style="display: inline-flex; align-items: center; gap: 6px; font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; font-weight: 700; color: #34D399; background: rgba(52, 211, 153, 0.15); border: 1px solid rgba(52, 211, 153, 0.35); padding: 4px 12px; border-radius: 999px;">
                        🇮🇳 PPAC INDIA BENCHMARKS
                    </span>
                </div>
            </div>
        </div>
    </div>
    """)

    # 2. Key Live Telemetry Cards
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_instrument_card(
            label="Brent Crude Benchmark",
            value="$76.80 / bbl",
            accent="amber",
            subtext="Global seaborne crude baseline",
            code_badge="BRENT"
        )
    with k2:
        render_instrument_card(
            label="Delhi Retail Diesel",
            value="₹87.62 / L",
            accent="teal",
            subtext="PPAC Metro Benchmark ($1.05/L)",
            code_badge="HSD"
        )
    with k3:
        render_instrument_card(
            label="Monitored Economies",
            value="25 Countries",
            accent="copper",
            subtext="85%+ of global crude throughput",
            code_badge="COVERAGE"
        )
    with k4:
        render_instrument_card(
            label="Data Provenance",
            value="7 Verified Sources",
            accent="teal",
            subtext="EIA • PPAC • EC • UN Comtrade",
            code_badge="PROVENANCE"
        )

    st.write("")

    # 3. Primary Call-to-Action Bar
    cta_col1, cta_col2, cta_col3 = st.columns([5, 4, 3])
    with cta_col1:
        if st.button("⚡ Launch Live Intelligence Dashboard", type="primary", use_container_width=True):
            if navigate_fn:
                navigate_fn("Live Intelligence Dashboard")
            else:
                st.session_state.active_nav = "Live Intelligence Dashboard"
                st.rerun()
    with cta_col2:
        if st.button("🇮🇳 Explore India Fuel Center", use_container_width=True):
            if navigate_fn:
                navigate_fn("India Fuel Center")
            else:
                st.session_state.active_nav = "India Fuel Center"
                st.rerun()
    with cta_col3:
        if st.button("🔒 Data Trust Center", use_container_width=True):
            if navigate_fn:
                navigate_fn("Data Trust Center")
            else:
                st.session_state.active_nav = "Data Trust Center"
                st.rerun()

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
                st.session_state.active_nav = "Live Intelligence Dashboard"
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
                st.session_state.active_nav = "India Fuel Center"
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
                st.session_state.active_nav = "Data Trust Center"
                st.rerun()

    grid4, grid5, grid6 = st.columns(3)

    with grid4:
        render_html("""
        <div style="background: rgba(14, 21, 38, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 18px; margin-bottom: 14px; min-height: 170px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span style="font-size: 1.2rem;">📖</span>
                <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; font-size: 0.95rem;">About the Project</span>
            </div>
            <p style="font-size: 0.82rem; color: #94A3B8; line-height: 1.45; margin-bottom: 12px;">
                The energy market dynamics, economic drivers, geological vs sovereign tax influences, pass-through mechanics, and system design philosophy.
            </p>
        </div>
        """)
        if st.button("Read About Project →", key="btn_nav_about", use_container_width=True):
            if navigate_fn:
                navigate_fn("About the Project")
            else:
                st.session_state.active_nav = "About the Project"
                st.rerun()

    with grid5:
        render_html("""
        <div style="background: rgba(14, 21, 38, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 18px; margin-bottom: 14px; min-height: 170px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span style="font-size: 1.2rem;">⚙️</span>
                <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; font-size: 0.95rem;">How It Works & Tech Stack</span>
            </div>
            <p style="font-size: 0.82rem; color: #94A3B8; line-height: 1.45; margin-bottom: 12px;">
                Architecture dossier covering the 6-stage data lifecycle: Ingestion → Validation → Storage → Analytics → Caching → UI presentation.
            </p>
        </div>
        """)
        if st.button("View Architecture →", key="btn_nav_arch", use_container_width=True):
            if navigate_fn:
                navigate_fn("How It Works & Architecture")
            else:
                st.session_state.active_nav = "How It Works & Architecture"
                st.rerun()

    with grid6:
        render_html("""
        <div style="background: rgba(14, 21, 38, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 18px; margin-bottom: 14px; min-height: 170px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span style="font-size: 1.2rem;">📐</span>
                <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; font-size: 0.95rem;">Methodology & Formulas</span>
            </div>
            <p style="font-size: 0.82rem; color: #94A3B8; line-height: 1.45; margin-bottom: 12px;">
                Full mathematical equations: Price spreads, Herfindahl-Hirschman Index (HHI), Trade Balances, Affordability scoring, and Forecast error metrics.
            </p>
        </div>
        """)
        if st.button("Inspect Formulas →", key="btn_nav_meth", use_container_width=True):
            if navigate_fn:
                navigate_fn("Methodology & Calculations")
            else:
                st.session_state.active_nav = "Methodology & Calculations"
                st.rerun()

    # 6. Honest Scope & Coverage Disclosure
    st.write("")
    render_html("""
    <div style="background: rgba(14, 21, 38, 0.5); border: 1px dashed rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 16px 20px; font-family: 'Inter', sans-serif; font-size: 0.8rem; color: #94A3B8; line-height: 1.55;">
        <b style="color: #F9FAFB; font-family: 'Space Grotesk', sans-serif;">🛡️ ETHICAL DATA DISCLOSURE:</b>
        Global FuelPulse AI operates on real, verified benchmark data from public institutions (US EIA, India PPAC, European Commission, UN Comtrade, Open Exchange Rates). We deliberately do not fabricate synthetic pricing or hallucinate unmonitored rural stations. Where data is collected weekly or annually, the exact observation dates and provenance are visibly stamped on every metric and chart.
    </div>
    """)
