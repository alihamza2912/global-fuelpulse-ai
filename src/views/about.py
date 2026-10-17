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
    st.markdown("""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 12px;">
        1. THE MISSION: DEMYSTIFYING THE ENERGY VALUE CHAIN
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
    st.markdown("""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 12px;">
        2. GEOLOGICAL DRIVERS VS. SOVEREIGN FISCAL POLICY
    </div>
    """, unsafe_allow_html=True)

    col_geo, col_tax = st.columns(2, gap="medium")
    with col_geo:
        render_html(f"""
        <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 20px; height: 100%;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                {get_lucide_icon_svg("globe", size=20, color="#F5B942")}
                <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; color: #F5B942; font-size: 1rem;">Geological & Upstream Drivers</span>
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.88rem; line-height: 1.55; color: #94A3B8;">
                <p>Upstream crude extraction economics are governed by geology:</p>
                <ul style="margin: 0; padding-left: 20px;">
                    <li><b>Lifting Costs:</b> Arabian light crude can be extracted for under <b>$10–$15/barrel</b> in conventional onshore fields, whereas Canadian oil sands or deepwater offshore can exceed <b>$45–$55/barrel</b>.</li>
                    <li><b>Crude Quality & Gravity:</b> Sweet crude (low sulfur, e.g. Brent, WTI) trades at a premium because it requires less desulfurization refining than heavy sour blends (e.g. Dubai, Maya).</li>
                    <li><b>Geopolitical Bottlenecks:</b> Over 60% of seaborne crude transits through just three chokepoints: Hormuz, Malacca, and Bab el-Mandeb/Suez.</li>
                </ul>
            </div>
        </div>
        """)

    with col_tax:
        render_html(f"""
        <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 20px; height: 100%;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                {get_lucide_icon_svg("landmark", size=20, color="#60A5FA")}
                <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; color: #60A5FA; font-size: 1rem;">Sovereign Fiscal & Tax Regimes</span>
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.88rem; line-height: 1.55; color: #94A3B8;">
                <p>Taxes and state policy account for up to <b>65%</b> of consumer fuel prices:</p>
                <ul style="margin: 0; padding-left: 20px;">
                    <li><b>Resource Subsidies:</b> Net exporters (Saudi Arabia, Kuwait) view fuel subsidies as direct citizen dividend distribution, pegging prices far below global export value.</li>
                    <li><b>Environmental Decarbonization:</b> European nations (Norway, Italy, Germany) impose heavy carbon taxes and excise duties (> $1.10/L) to disincentivize fossil fuel consumption.</li>
                    <li><b>Fiscal Revenue Shield:</b> Major importers (India) levy central excise and state VAT as critical non-repayable tax revenue, adjusting rates counter-cyclically to cushion government deficits.</li>
                </ul>
            </div>
        </div>
        """)

    st.write("")

    # 3. The 5-Step Refined Product Pass-Through Chain
    st.markdown("""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 12px;">
        3. THE 5-STAGE VALUE ADDED CHAIN (FROM WELLHEAD TO NOZZLE)
    </div>
    """, unsafe_allow_html=True)

    render_html("""
    <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 22px; margin-bottom: 24px;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px;">
            <div style="background: rgba(7, 10, 18, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 14px;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 800; color: #F5B942; margin-bottom: 4px;">STAGE 01</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; margin-bottom: 6px;">Crude Extraction</div>
                <div style="font-size: 0.8rem; color: #94A3B8; line-height: 1.45;">Wellhead drilling, separation of associated gas, and field gathering systems. Priced in USD/bbl.</div>
            </div>
            <div style="background: rgba(7, 10, 18, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 14px;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 800; color: #60A5FA; margin-bottom: 4px;">STAGE 02</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; margin-bottom: 6px;">Maritime Tanker Transit</div>
                <div style="font-size: 0.8rem; color: #94A3B8; line-height: 1.45;">VLCC and Suezmax chartering, bunker fuel costs, marine insurance, and chokepoint transit tariffs.</div>
            </div>
            <div style="background: rgba(7, 10, 18, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 14px;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 800; color: #34D399; margin-bottom: 4px;">STAGE 03</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; margin-bottom: 6px;">Refining & Cracking</div>
                <div style="font-size: 0.8rem; color: #94A3B8; line-height: 1.45;">Atmospheric distillation, catalytic cracking, and hydrotreating. Refiner margins determined by the 3:2:1 crack spread.</div>
            </div>
            <div style="background: rgba(7, 10, 18, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 14px;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 800; color: #F472B6; margin-bottom: 4px;">STAGE 04</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; margin-bottom: 6px;">Tax & Duty Tollgate</div>
                <div style="font-size: 0.8rem; color: #94A3B8; line-height: 1.45;">Customs tariffs, central excise levies, environmental surcharges, and state-level ad-valorem Value Added Tax.</div>
            </div>
            <div style="background: rgba(7, 10, 18, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 14px;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 800; color: #A78BFA; margin-bottom: 4px;">STAGE 05</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #F9FAFB; margin-bottom: 6px;">Inland Depot & Pump</div>
                <div style="font-size: 0.8rem; color: #94A3B8; line-height: 1.45;">Pipeline transportation to regional terminals, road tanker carriage, dealer commission, and final dispensing.</div>
            </div>
        </div>
    </div>
    """)

    # 4. System Design Philosophy
    st.markdown("""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 12px;">
        4. DESIGN PHILOSOPHY & PRINCIPLES
    </div>
    """, unsafe_allow_html=True)

    render_html("""
    <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 22px; font-family: 'Inter', sans-serif; font-size: 0.9rem; line-height: 1.6; color: #94A3B8;">
        <div style="margin-bottom: 12px;">
            <b style="color: #F9FAFB;">Zero Fabricated Telemetry:</b> In financial and commodity intelligence, hallucinated mock data is worse than no data. If a specific city or country does not publish daily retail prices, Global FuelPulse AI honestly presents the latest official observation timestamp rather than inventing synthetic numbers.
        </div>
        <div style="margin-bottom: 12px;">
            <b style="color: #F9FAFB;">Sub-Second Interactive Performance:</b> By employing aggressive multi-tier caching (SQLAlchemy connection pooling, pre-computed TopoJSON geographic layers, in-memory query indexes), the platform renders analytical chapters in under 50 milliseconds.
        </div>
        <div>
            <b style="color: #F9FAFB;">Reproducible Open Architecture:</b> All analytics formulas—from the Herfindahl-Hirschman supplier concentration index to the price build-up waterfall—are fully documented with LaTeX math and backed by open-source automated unit tests.
        </div>
    </div>
    """)
