"""
Page 7: Machine Learning Forecasting & Anomaly Detection Center.
Evaluates time-series predictive models with MAE/RMSE and detects statistical anomalies across prices and trade.
"""

import sys
from pathlib import Path

# Ensure project root AND src directory are in sys.path and remove conflicting parent mount
ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"

parent_mount = ROOT_DIR.parent
sys.path = [p for p in sys.path if Path(p).resolve() != parent_mount and Path(p).resolve() != parent_mount.parent]

for d in [str(ROOT_DIR), str(SRC_DIR)]:
    while d in sys.path:
        sys.path.remove(d)
    sys.path.insert(0, d)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.ui_components import (
    render_page_header,
    render_instrument_card,
    render_csv_download,
    apply_theme,
    get_atlas_plotly_theme,
    apply_clean_layout,
    COLOR_INK,
    COLOR_AMBER,
    COLOR_WHITE
)
from src.ml.forecasting import PriceForecaster
from src.ml.anomaly_detection import AnomalyDetector
from src.analytics.price_analytics import FuelPriceAnalytics

apply_theme()

render_page_header(
    title="FORECASTING & ANOMALY DETECTION",
    subtitle="Predictive Retail Fuel Price Modeling, Train/Test Validation, and Statistical Outlier Monitoring",
    source_tag="Statsmodels • Scikit-Learn • Rolling MAD / Z-Score",
    observation_date="Weekly Projections"
)

# Tabs: Forecasting & Anomaly Detection
tab_fc, tab_anom = st.tabs(["📈 ML Fuel Price Forecasting", "🚨 Energy Market Anomaly Radar"])

with tab_fc:
    st.subheader("🤖 Trend-Augmented Autoregressive Price Projection")
    
    # Country & Fuel Selection
    f_c1, f_c2, f_c3 = st.columns(3)
    with f_c1:
        target_country = st.selectbox("Forecast Target Country", ["USA", "IND", "DEU", "FRA", "GBR", "SAU"], format_func=lambda x: {
            "USA": "United States", "IND": "India", "DEU": "Germany",
            "FRA": "France", "GBR": "United Kingdom", "SAU": "Saudi Arabia"
        }.get(x, x))
    with f_c2:
        target_fuel = st.selectbox("Fuel Product", ["petrol_regular", "diesel"], format_func=lambda x: "Regular Gasoline / Petrol" if x == "petrol_regular" else "Diesel")
    with f_c3:
        horizon_wks = st.slider("Forecast Horizon (Weeks Ahead)", min_value=1, max_value=8, value=4)

    # Train model and generate projections
    fc_results = PriceForecaster.train_and_forecast(
        country_iso3=target_country,
        fuel_type=target_fuel,
        horizon_weeks=horizon_wks
    )

    # Performance KPI Cards
    mk1, mk2, mk3, mk4 = st.columns(4)
    with mk1:
        render_instrument_card(
            label="Model MAE (Holdout Test)",
            value=f"${fc_results['mae']:.4f}/L",
            accent="teal",
            subtext=f"Baseline MAE: ${fc_results.get('baseline_mae', 0.0):.4f}/L"
        )
    with mk2:
        render_instrument_card(
            label="Model RMSE",
            value=f"${fc_results['rmse']:.4f}/L",
            accent="teal",
            subtext=f"Evaluated on {fc_results.get('test_observations', 2)} holdout periods"
        )
    with mk3:
        beats_baseline = fc_results.get("model_beats_baseline", True)
        render_instrument_card(
            label="Model Validation vs Naive",
            value="SUPERIOR" if beats_baseline else "BASELINE PARITY",
            accent="amber" if beats_baseline else "copper",
            subtext="Lower forecast error" if beats_baseline else "Within noise margin"
        )
    with mk4:
        imp_val = fc_results.get("improvement_pct", 0.0)
        imp_sign = "+" if imp_val > 0 else ""
        render_instrument_card(
            label="Holdout Improvement vs Naive",
            value=f"{imp_sign}{imp_val:.1f}%",
            accent="green" if imp_val >= 0 else "amber",
            subtext=f"Trained: {fc_results.get('train_window', '2024–2026')}"
        )

    st.write("")

    # Forecast Plot: Historical actuals + Future trajectory with confidence bounds
    st.subheader(f"📊 Projected Price Trajectory: {target_country} ({target_fuel})")
    
    forecasts = fc_results.get("forecasts", [])
    hist_dates = fc_results.get("historical_dates", [])
    hist_prices = fc_results.get("historical_prices", [])

    fig_fc = go.Figure()

    # Historical line
    if hist_dates and hist_prices:
        fig_fc.add_trace(go.Scatter(
            x=hist_dates,
            y=hist_prices,
            mode="lines+markers",
            name="Historical Actual Price",
            line=dict(color=COLOR_INK, width=2.5),
            marker=dict(size=7, color=COLOR_INK)
        ))

    # Forecast line
    if forecasts:
        fc_dates = [f["target_date"] for f in forecasts]
        fc_preds = [f["predicted_price_usd"] for f in forecasts]
        fc_lower = [f.get("lower_bound_usd", f.get("confidence_lower_usd", f["predicted_price_usd"])) for f in forecasts]
        fc_upper = [f.get("upper_bound_usd", f.get("confidence_upper_usd", f["predicted_price_usd"])) for f in forecasts]

        # Connect last historical point to first forecast
        if hist_dates:
            plot_dates = [hist_dates[-1]] + fc_dates
            plot_preds = [hist_prices[-1]] + fc_preds
            plot_lower = [hist_prices[-1]] + fc_lower
            plot_upper = [hist_prices[-1]] + fc_upper
        else:
            plot_dates = fc_dates
            plot_preds = fc_preds
            plot_lower = fc_lower
            plot_upper = fc_upper

        # Confidence bounds shaded area
        fig_fc.add_trace(go.Scatter(
            x=plot_dates + plot_dates[::-1],
            y=plot_upper + plot_lower[::-1],
            fill="toself",
            fillcolor="rgba(245, 185, 66, 0.25)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            showlegend=True,
            name="95% Confidence Interval"
        ))

        # Prediction trace
        fig_fc.add_trace(go.Scatter(
            x=plot_dates,
            y=plot_preds,
            mode="lines+markers",
            name="Predicted Horizon",
            line=dict(color=COLOR_AMBER, width=3, dash="dash"),
            marker=dict(size=8, symbol="diamond", color=COLOR_AMBER, line=dict(color=COLOR_INK, width=1.5))
        ))

    apply_clean_layout(
        fig_fc,
        height=460,
        xaxis_title="Timeline",
        yaxis_title="Price (USD / Litre)",
        legend_below=True
    )
    st.plotly_chart(fig_fc, width="stretch", theme=None)

    # Forecast Projection Table
    if forecasts:
        fc_table = pd.DataFrame(forecasts).rename(columns={
            "week": "Week Ahead", "target_date": "Target Date",
            "predicted_price_usd": "Predicted (USD/L)",
            "lower_bound_usd": "Lower 95% Bound", "upper_bound_usd": "Upper 95% Bound",
            "method": "Algorithm"
        })
        st.dataframe(fc_table, width="stretch", hide_index=True)
        render_csv_download(fc_table, f"fuelpulse_{target_country}_{target_fuel}_forecast.csv")

with tab_anom:
    st.subheader("🚨 Statistical Anomaly Detection Radar")
    st.markdown(
        """
        The anomaly engine continuously evaluates price deviations using **Rolling Z-Scores**, **Median Absolute Deviation (MAD)**, and **Interquartile Range (IQR)** to detect sudden price spikes or export trade interruptions.
        """
    )

    detected_price_anoms = AnomalyDetector.detect_price_anomalies(threshold_zscore=2.0)
    detected_trade_anoms = AnomalyDetector.detect_trade_volume_anomalies()
    all_anomalies = detected_price_anoms + detected_trade_anoms

    if all_anomalies:
        anom_df = pd.DataFrame(all_anomalies)

        # Alert Breakdown Cards
        ak1, ak2, ak3 = st.columns(3)
        with ak1:
            render_instrument_card("Total Anomalies Flagged", str(len(all_anomalies)), accent="amber", subtext="Outliers exceeding statistical bounds")
        with ak2:
            crit_count = len(anom_df[anom_df["severity"] == "CRITICAL"])
            render_instrument_card("Critical Severity Events", str(crit_count), accent="red", subtext="Deviation > 25% from baseline")
        with ak3:
            render_instrument_card("Active Detection Methods", "Rolling Z-Score & MAD", accent="teal", subtext="Robust non-parametric models")

        st.write("")

        # Plotly Deviation Bar Chart
        fig_anom = px.bar(
            anom_df,
            x="country_name",
            y="deviation_percent",
            color="severity",
            color_discrete_map={"LOW": "#3b82f6", "MEDIUM": COLOR_AMBER, "HIGH": "#f97316", "CRITICAL": "#ef4444"},
            hover_name="description",
            labels={"deviation_percent": "Deviation from Baseline (%)", "country_name": "Country"}
        )
        fig_anom.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.5)))
        apply_clean_layout(
            fig_anom,
            height=480,
            xaxis_title="Country",
            yaxis_title="Deviation from Baseline (%)",
            legend_below=True
        )
        st.plotly_chart(fig_anom, width="stretch", theme=None)

        # Anomaly Log Table
        display_anom = anom_df[[
            "severity", "entity_type", "country_name", "product_category",
            "observation_date", "observed_value", "expected_baseline", "deviation_percent", "description"
        ]].rename(columns={
            "severity": "Severity", "entity_type": "Category", "country_name": "Country",
            "product_category": "Product", "observation_date": "Date",
            "observed_value": "Observed", "expected_baseline": "Baseline",
            "deviation_percent": "Dev %", "description": "Alert Detail"
        })
        st.dataframe(display_anom, width="stretch", hide_index=True)
    else:
        st.success("✅ No anomalous price movements or trade volume disruptions detected in current window.")
