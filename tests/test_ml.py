"""
Unit Tests for Machine Learning Forecasting and Anomaly Detection.
Verifies time-ordered train/test splits, MAE/RMSE calculations, and anomaly flagging.
"""

import pytest
from src.ml.forecasting import PriceForecaster
from src.ml.anomaly_detection import AnomalyDetector


def test_time_series_forecasting_evaluation():
    """Verifies that model generates projections, metrics, and confidence intervals."""
    results = PriceForecaster.train_and_forecast(
        country_iso3="USA",
        fuel_type="petrol_regular",
        horizon_weeks=4
    )
    assert "mae" in results
    assert "rmse" in results
    assert results["mae"] >= 0.0
    assert results["rmse"] >= 0.0
    assert len(results["forecasts"]) == 4

    # Verify that prediction interval lower bound <= predicted <= upper bound
    for fc in results["forecasts"]:
        assert fc["lower_bound_usd"] <= fc["predicted_price_usd"]
        assert fc["predicted_price_usd"] <= fc["upper_bound_usd"]


def test_anomaly_detector_methods():
    """Verifies that statistical anomaly detection identifies deviations."""
    price_anoms = AnomalyDetector.detect_price_anomalies(threshold_zscore=1.5)
    assert isinstance(price_anoms, list)

    trade_anoms = AnomalyDetector.detect_trade_volume_anomalies()
    assert isinstance(trade_anoms, list)

    for a in price_anoms + trade_anoms:
        assert "observed_value" in a
        assert "expected_baseline" in a
        assert "severity" in a
        assert a["severity"] in ("LOW", "MEDIUM", "HIGH", "CRITICAL")


def test_forecast_predictions_db_persistence():
    """Verifies that generated forecasts are saved into forecast_predictions table."""
    from src.database.connection import db_manager
    from src.database.models import ForecastPrediction

    res = PriceForecaster.train_and_forecast("USA", "diesel", horizon_weeks=4)
    assert len(res["forecasts"]) == 4

    with db_manager.get_session() as session:
        preds = session.query(ForecastPrediction).filter_by(
            country_iso3="USA",
            fuel_type="diesel"
        ).all()
        assert len(preds) == 4
        for p in preds:
            assert p.predicted_price_usd > 0
            assert p.confidence_lower_usd <= p.predicted_price_usd
            assert p.predicted_price_usd <= p.confidence_upper_usd
            assert p.train_mae is not None

