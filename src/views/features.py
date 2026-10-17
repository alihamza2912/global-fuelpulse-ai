"""
GLOBAL FUELPULSE AI — FEATURES CATALOG VIEW
Complete technical inventory of all 12 modules, their analytical models,
data requirements, and operational status.
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

    features = [
        {
            "id": "01",
            "name": "Global Crude Extraction Leaderboard",
            "category": "UPSTREAM INTELLIGENCE",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Tracks daily and annual crude oil extraction volumes (in million barrels per day - mbpd) for the top 15 producing nations, contrasting OPEC vs Non-OPEC market power.",
            "why": "Identifies upstream market concentration and baseline global supply expansion or curtailment.",
            "data": "US EIA Table 11.1b, Official OPEC Annual Statistical Bulletins.",
            "action_text": "View in Dashboard Chapter 02",
            "nav_target": "Live Intelligence Dashboard"
        },
        {
            "id": "02",
            "name": "Bilateral Seaborne Trade Flow Matrix",
            "category": "MIDSTREAM LOGISTICS",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Origin-destination bilateral matrix capturing physical crude and product tanker flows between sovereign exporters and consuming hubs.",
            "why": "Reveals energy interdependence, export intensities, and sovereign trade surpluses/deficits.",
            "data": "UN Comtrade Petroleum Trade Mart (Harmonized System Codes 2709 & 2710).",
            "action_text": "View in Dashboard Chapter 03",
            "nav_target": "Live Intelligence Dashboard"
        },
        {
            "id": "03",
            "name": "International Retail Fuel Price Explorer",
            "category": "DOWNSTREAM PRICING",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Multi-country comparative pricing for Regular Motor Gasoline (Petrol) and Automotive Gasoil (Diesel), harmonized into standardized USD per litre and local currencies.",
            "why": "Enables cross-border fleet routing, international price disparity tracking, and diesel-to-petrol ratio analysis.",
            "data": "US EIA, India PPAC, European Commission Oil Bulletin, Open Exchange Rates.",
            "action_text": "View in Dashboard Chapter 04",
            "nav_target": "Live Intelligence Dashboard"
        },
        {
            "id": "04",
            "name": "Price Build-Up & Tax Waterfall Analyzer",
            "category": "FISCAL DECOMPOSITION",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Decomposes consumer retail pump prices into upstream crude benchmark costs, refinery margin, central excise duty, dealer margin, and regional VAT.",
            "why": "Demystifies the exact sovereign tax wedge vs commodity cost within each litre of motor fuel.",
            "data": "Ministry of Petroleum & Natural Gas (MoPNG) Price Build-Up Circulars, PPAC.",
            "action_text": "View in India Fuel Center",
            "nav_target": "India Fuel Center"
        },
        {
            "id": "05",
            "name": "Energy Affordability Burden Index",
            "category": "SOCIOECONOMIC IMPACT",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Calculates the real economic burden of fuel by benchmarking a 50-litre tank against national GDP per capita and daily minimum wage levels.",
            "why": "Exposes why a $1.10/L fuel price in a developing nation represents a far greater economic burden than $1.85/L in a high-income nation.",
            "data": "World Bank Economic Indicators, ILO Minimum Wage Database.",
            "action_text": "View in Dashboard Chapter 06",
            "nav_target": "Live Intelligence Dashboard"
        },
        {
            "id": "06",
            "name": "Maritime Chokepoint & Supply Risk Radar",
            "category": "VULNERABILITY AUDITING",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Evaluates national dependency on high-risk maritime transit corridors (Strait of Hormuz, Malacca Strait, Suez/Red Sea) and calculates the Herfindahl-Hirschman Index (HHI).",
            "why": "Quantifies supply disruption vulnerability for nations heavily reliant on singular import routes.",
            "data": "Maritime transit throughput records, UN Comtrade bilateral import weights.",
            "action_text": "View in Dashboard Chapter 07",
            "nav_target": "Live Intelligence Dashboard"
        },
        {
            "id": "07",
            "name": "Macroeconomic Fuel Shock Simulator",
            "category": "DECISION SUPPORT & PLANNING",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Interactive sensitivity model allowing fleet managers and procurement leaders to simulate crude oil spikes (+$5 to +$50/bbl) and local currency depreciations (1% to 25%).",
            "why": "Accurately projects monthly fleet cost inflations and evaluates required fuel surcharge pass-through rates.",
            "data": "Empirical pass-through elasticities, user fleet size and monthly volume inputs.",
            "action_text": "View in Dashboard Chapter 08",
            "nav_target": "Live Intelligence Dashboard"
        },
        {
            "id": "08",
            "name": "SARIMAX & XGBoost Machine Learning Radar",
            "category": "PREDICTIVE MODELING",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Multi-horizon time-series forecasting engine generating 30-day and 90-day forward retail fuel price projections with 80% and 95% confidence intervals.",
            "why": "Provides quantitative forward price expectations incorporating seasonal demand patterns and crude spot lags.",
            "data": "Historical weekly fuel price time-series, Brent crude spot lag regressors.",
            "action_text": "View in Dashboard Chapter 10",
            "nav_target": "Live Intelligence Dashboard"
        },
        {
            "id": "09",
            "name": "AI Energy Market Analyst (LLM-Assisted)",
            "category": "SYNTHETIC REASONING",
            "status": "PRODUCTION / QUOTA-GATED",
            "status_color": "#60A5FA",
            "what": "Natural-language query engine powered by Google Gemini, capable of translating plain-English questions into verified read-only SQL queries with quota tracking.",
            "why": "Allows executive stakeholders to extract instant answers without writing SQL queries or navigating multiple charts.",
            "data": "Full relational schema grounding, in-memory TTL query cache.",
            "action_text": "View in Dashboard Chapter 09",
            "nav_target": "Live Intelligence Dashboard"
        },
        {
            "id": "10",
            "name": "India Metro Energy Center (PPAC Daily)",
            "category": "REGIONAL BENCHMARKING",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Dedicated operational portal tracking verified daily retail pump prices for Delhi, Mumbai, Kolkata, and Chennai, plus Indian Crude Basket and OMC market shares.",
            "why": "Gives Indian fleet operators, shippers, and policy observers authoritative benchmark transparency.",
            "data": "Petroleum Planning & Analysis Cell (PPAC), MoPNG, IOCL/BPCL/HPCL public disclosures.",
            "action_text": "View India Fuel Center",
            "nav_target": "India Fuel Center"
        },
        {
            "id": "11",
            "name": "Automated Quality Auditor & Telemetry Mart",
            "category": "DATA GOVERNANCE",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Real-time auditing suite verifying observation latencies, data provenance, connector execution runtimes, and zero-tolerance quarantine logs.",
            "why": "Guarantees data integrity and alerts operators to stale feeds or upstream API format changes.",
            "data": "`etl_run_log` table, database schema inspection pragma.",
            "action_text": "View Data Trust Center",
            "nav_target": "Data Trust Center"
        },
        {
            "id": "12",
            "name": "Power BI & Multi-Format Data Export",
            "category": "ENTERPRISE INTEGRATION",
            "status": "PRODUCTION / VERIFIED",
            "status_color": "#10B981",
            "what": "Direct export capabilities for all underlying data marts in CSV format, alongside auto-generated Power BI `.pbids` enterprise connection files.",
            "why": "Allows enterprise teams to seamlessly ingest FuelPulse AI data directly into internal corporate BI dashboards.",
            "data": "Relational query exports across all database tables.",
            "action_text": "Export from Dashboard",
            "nav_target": "Live Intelligence Dashboard"
        }
    ]

    for f in features:
        render_html(f"""
        <div style="background: rgba(14, 21, 38, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 10px; padding: 20px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px; margin-bottom: 10px;">
                <div>
                    <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 800; color: #F5B942; letter-spacing: 0.06em;">FEATURE {f['id']} // {f['category']}</span>
                    <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; font-weight: 800; color: #F9FAFB; margin: 3px 0 0 0;">{f['name']}</h3>
                </div>
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem; font-weight: 800; color: {f['status_color']}; background: rgba(255, 255, 255, 0.05); border: 1px solid {f['status_color']}; padding: 3px 9px; border-radius: 999px;">
                    {f['status']}
                </span>
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.86rem; line-height: 1.55; color: #94A3B8; margin-bottom: 12px;">
                <p style="margin: 0 0 6px 0;"><b style="color: #F9FAFB;">What it does:</b> {f['what']}</p>
                <p style="margin: 0 0 6px 0;"><b style="color: #F9FAFB;">Why it matters:</b> {f['why']}</p>
                <p style="margin: 0;"><b style="color: #F9FAFB;">Input data sources:</b> {f['data']}</p>
            </div>
        </div>
        """)
