"""
GLOBAL FUELPULSE AI — METHODOLOGY & CALCULATIONS VIEW
Formal mathematical equations, econometric pass-through formulas,
and statistical error evaluation frameworks.
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


def render_methodology_view(navigate_fn=None):
    """Renders the comprehensive Methodology, Mathematical Formulations, and Calculations guide."""
    cur_lang = get_current_language()

    render_html(f"""
    <div style="background: radial-gradient(circle at 10% 20%, rgba(245, 185, 66, 0.12) 0%, rgba(14, 21, 38, 0.95) 70%), #070A12; border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 12px; padding: 26px 30px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
            <div>
                {get_fuel_client_logo_html()}
                <h1 style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 2rem; font-weight: 800; color: #F9FAFB; margin: 6px 0 8px 0; letter-spacing: -0.02em;">
                    {t('method_hero_title', cur_lang)}
                </h1>
                <p style="font-family: 'Inter', sans-serif; font-size: 1rem; color: #94A3B8; margin: 0; max-width: 820px; line-height: 1.55;">
                    {t('method_hero_sub', cur_lang)}
                </p>
            </div>
        </div>
    </div>
    """)

    # 1. Price Variation & Delta Calculations
    st.markdown(f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 8px;">
        {t('meth_sec1_title', cur_lang)}
    </div>
    """, unsafe_allow_html=True)

    render_html("""
    <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 20px; margin-bottom: 20px; font-family: 'Inter', sans-serif; font-size: 0.88rem; line-height: 1.6; color: #94A3B8;">
        <p style="margin-top: 0;">
            To calculate genuine price movement over time without contamination from cross-city geographic variance, all observations are partitioned strictly by the tuple <code>(country_iso3, location_id, fuel_type, brand_name)</code>.
        </p>
    </div>
    """)

    st.latex(r"""
    \Delta P_t = P_t - P_{t-1}
    """)
    st.latex(r"""
    \% \Delta P_t = \left( \frac{P_t - P_{t-1}}{P_{t-1}} \right) \times 100\%
    """)

    st.write("")

    # 2. Herfindahl-Hirschman Index (HHI) for Import Concentration
    st.markdown(f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 8px;">
        {t('meth_sec2_title', cur_lang)}
    </div>
    """, unsafe_allow_html=True)

    render_html("""
    <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 20px; margin-bottom: 20px; font-family: 'Inter', sans-serif; font-size: 0.88rem; line-height: 1.6; color: #94A3B8;">
        <p style="margin-top: 0;">
            We employ the Herfindahl-Hirschman Index (HHI) to quantify import reliance on sovereign supplier nations. Let $s_i$ be the percentage share of crude oil imported from supplier $i$:
        </p>
    </div>
    """)

    st.latex(r"""
    HHI = \sum_{i=1}^N \left( s_i \right)^2 \quad \text{where} \quad s_i = \left( \frac{\text{Import Volume}_i}{\sum_{j=1}^N \text{Import Volume}_j} \right) \times 100\%
    """)

    render_html(f"""
    <div style="background: rgba(14, 21, 38, 0.5); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 6px; padding: 12px 16px; margin-bottom: 20px; font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; color: #F9FAFB;">
        <div>{t('meth_hhi_resilient', cur_lang)}</div>
        <div>{t('meth_hhi_guarded', cur_lang)}</div>
        <div>{t('meth_hhi_elevated', cur_lang)}</div>
    </div>
    """)

    st.write("")

    # 3. Energy Affordability Burden Index
    st.markdown(f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 8px;">
        {t('meth_sec3_title', cur_lang)}
    </div>
    """, unsafe_allow_html=True)

    render_html("""
    <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 20px; margin-bottom: 20px; font-family: 'Inter', sans-serif; font-size: 0.88rem; line-height: 1.6; color: #94A3B8;">
        <p style="margin-top: 0;">
            Raw price per litre ($/L) fails to reflect socioeconomic purchasing power. A $1.10/L price in an emerging economy poses a vastly higher financial strain than $1.80/L in Western Europe. We compute the <b>50-Litre Fill-Up Burden</b> against daily income:
        </p>
    </div>
    """)

    st.latex(r"""
    \text{Affordability Burden (\%)} = \frac{50 \times P_{\text{fuel, USD}}}{\left( \frac{\text{GDP per Capita}_{\text{USD}}}{365} \right)} \times 100\%
    """)

    st.write("")

    # 4. Macroeconomic Shock Simulator Elasticity Model
    st.markdown(f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 8px;">
        {t('meth_sec4_shock_title', cur_lang)}
    </div>
    """, unsafe_allow_html=True)

    render_html(r"""
    <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 20px; margin-bottom: 20px; font-family: 'Inter', sans-serif; font-size: 0.88rem; line-height: 1.6; color: #94A3B8;">
        <p style="margin-top: 0;">
            The interactive shock simulator models the impact of an exogenous crude oil supply shock ($\Delta C$ in USD/bbl) and local currency depreciation ($\% \Delta FX$) on fleet operating budgets:
        </p>
    </div>
    """)

    st.latex(r"""
    P_{\text{simulated}} = P_{\text{baseline}} \times \left( 1 + \beta_{\text{crude}} \cdot \frac{\Delta C}{C_{\text{baseline}}} + \beta_{\text{FX}} \cdot \frac{\% \Delta FX}{100} \right)
    """)
    st.latex(r"""
    \Delta \text{Expenditure}_{\text{monthly}} = V_{\text{fleet}} \times \left( P_{\text{simulated}} - P_{\text{baseline}} \right)
    """)

    render_html(r"""
    <div style="background: rgba(14, 21, 38, 0.5); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 6px; padding: 12px 16px; margin-bottom: 20px; font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; color: #94A3B8;">
        Where $\beta_{\text{crude}} \approx 0.72$ (empirical short-run pass-through coefficient) and $\beta_{\text{FX}} \approx 0.85$ (imported commodity currency elasticity).
    </div>
    """)

    st.write("")

    # 5. Forecast Error Evaluation Metrics
    st.markdown(f"""
    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; margin-bottom: 8px;">
        {t('meth_sec5_error_title', cur_lang)}
    </div>
    """, unsafe_allow_html=True)

    render_html("""
    <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 20px; margin-bottom: 20px; font-family: 'Inter', sans-serif; font-size: 0.88rem; line-height: 1.6; color: #94A3B8;">
        <p style="margin-top: 0;">
            All machine learning and econometric price projections (SARIMAX, XGBoost, Prophet) undergo out-of-sample backtesting across a 12-week holdout validation window using three standard error metrics:
        </p>
    </div>
    """)

    st.latex(r"""
    \text{Mean Absolute Error (MAE)} = \frac{1}{n} \sum_{i=1}^n |y_i - \hat{y}_i|
    """)
    st.latex(r"""
    \text{Root Mean Squared Error (RMSE)} = \sqrt{\frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2}
    """)
    st.latex(r"""
    \text{Mean Absolute Percentage Error (MAPE)} = \frac{100\%}{n} \sum_{i=1}^n \left| \frac{y_i - \hat{y}_i}{y_i} \right|
    """)
