"""
SQLAlchemy ORM Models for Global FuelPulse AI Platform.
Maps all dimensions, facts, ML, and auditing tables to the database.
"""

from datetime import datetime, date
from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    CHAR,
    Numeric,
    Date,
    DateTime,
    Boolean,
    Text,
    ForeignKey,
    UniqueConstraint,
    Index
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class DataSource(Base):
    __tablename__ = "data_sources"

    source_id = Column(String(50), primary_key=True)
    name = Column(String(150), nullable=False)
    organization = Column(String(150), nullable=True)
    homepage_url = Column(String(255), nullable=True)
    api_docs_url = Column(String(255), nullable=True)
    auth_type = Column(String(50), default="none")
    update_frequency = Column(String(50), default="daily")
    license_terms = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    fuel_prices = relationship("FuelPrice", back_populates="source")
    petroleum_trades = relationship("PetroleumTrade", back_populates="source")


class DimCountry(Base):
    __tablename__ = "dim_country"

    country_iso3 = Column(CHAR(3), primary_key=True)
    country_iso2 = Column(CHAR(2), nullable=False)
    country_name = Column(String(100), nullable=False)
    continent = Column(String(50), nullable=False)
    region = Column(String(100), nullable=True)
    income_group = Column(String(50), nullable=True)
    currency_code = Column(CHAR(3), nullable=True)
    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)
    is_opec = Column(Boolean, default=False)
    is_opec_plus = Column(Boolean, default=False)
    is_major_net_importer = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    locations = relationship("DimLocation", back_populates="country")
    fuel_prices = relationship("FuelPrice", back_populates="country")
    affordability_records = relationship("FactAffordability", back_populates="country")


class DimLocation(Base):
    __tablename__ = "dim_location"

    location_id = Column(String(50), primary_key=True)
    country_iso3 = Column(CHAR(3), ForeignKey("dim_country.country_iso3", ondelete="CASCADE"), nullable=False)
    location_name = Column(String(100), nullable=False)
    location_type = Column(String(50), default="city")
    state_province = Column(String(100), nullable=True)
    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    country = relationship("DimCountry", back_populates="locations")


class FuelPrice(Base):
    __tablename__ = "fuel_prices"

    price_id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    country_iso3 = Column(CHAR(3), ForeignKey("dim_country.country_iso3"), nullable=False)
    location_id = Column(String(50), nullable=True)
    observation_date = Column(Date, nullable=False)
    fuel_type = Column(String(50), nullable=False)
    price_local = Column(Numeric(12, 4), nullable=False)
    currency_local = Column(CHAR(3), nullable=False)
    unit = Column(String(30), default="litre")
    price_usd_per_litre = Column(Numeric(10, 4), nullable=False)
    tax_component_percent = Column(Numeric(5, 2), nullable=True)
    source_id = Column(String(50), ForeignKey("data_sources.source_id"), nullable=False)
    source_updated_at = Column(DateTime, nullable=True)
    ingested_at = Column(DateTime, default=datetime.utcnow)
    is_verified = Column(Boolean, default=True)

    country = relationship("DimCountry", back_populates="fuel_prices")
    source = relationship("DataSource", back_populates="fuel_prices")

    __table_args__ = (
        UniqueConstraint("country_iso3", "location_id", "observation_date", "fuel_type", "source_id", name="uq_fuel_price_obs"),
        Index("idx_fp_country_date", "country_iso3", "observation_date"),
        Index("idx_fp_fuel_date", "fuel_type", "observation_date"),
    )


class PetroleumTrade(Base):
    __tablename__ = "fact_petroleum_trade"

    trade_id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    reporting_period = Column(String(10), nullable=False)
    reporting_year = Column(Integer, nullable=False)
    exporter_iso3 = Column(CHAR(3), ForeignKey("dim_country.country_iso3"), nullable=True)
    importer_iso3 = Column(CHAR(3), ForeignKey("dim_country.country_iso3"), nullable=True)
    product_category = Column(String(50), nullable=False)
    hs_code = Column(String(10), nullable=True)
    trade_direction = Column(String(10), nullable=False)
    quantity = Column(Numeric(16, 4), nullable=False)
    quantity_unit = Column(String(30), nullable=False)
    value_usd = Column(Numeric(18, 2), nullable=True)
    transport_mode = Column(String(50), default="tanker_pipeline")
    source_id = Column(String(50), ForeignKey("data_sources.source_id"), nullable=False)
    ingested_at = Column(DateTime, default=datetime.utcnow)

    source = relationship("DataSource", back_populates="petroleum_trades")

    __table_args__ = (
        UniqueConstraint("reporting_period", "exporter_iso3", "importer_iso3", "product_category", "trade_direction", "source_id", name="uq_petroleum_trade"),
        Index("idx_trade_period_prod", "reporting_period", "product_category"),
        Index("idx_trade_exporter", "exporter_iso3", "reporting_year"),
        Index("idx_trade_importer", "importer_iso3", "reporting_year"),
    )


class FactEnergyIndicator(Base):
    __tablename__ = "fact_energy_indicator"

    indicator_id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    country_iso3 = Column(CHAR(3), ForeignKey("dim_country.country_iso3"), nullable=True)
    indicator_code = Column(String(50), nullable=False)
    period = Column(String(10), nullable=False)
    value = Column(Numeric(16, 4), nullable=False)
    unit = Column(String(30), nullable=False)
    source_id = Column(String(50), ForeignKey("data_sources.source_id"), nullable=False)
    ingested_at = Column(DateTime, default=datetime.utcnow)


class FactExchangeRate(Base):
    __tablename__ = "fact_exchange_rate"

    rate_id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    currency_code = Column(CHAR(3), nullable=False)
    rate_date = Column(Date, nullable=False)
    rate_to_usd = Column(Numeric(14, 6), nullable=False)
    source_id = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("currency_code", "rate_date", name="uq_exchange_rate"),
    )


class FactAffordability(Base):
    __tablename__ = "fact_affordability"

    affordability_id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    country_iso3 = Column(CHAR(3), ForeignKey("dim_country.country_iso3"), nullable=False)
    reporting_year = Column(Integer, nullable=False)
    gdp_per_capita_nominal_usd = Column(Numeric(12, 2), nullable=False)
    gdp_per_capita_ppp_usd = Column(Numeric(12, 2), nullable=True)
    daily_income_proxy_usd = Column(Numeric(10, 2), nullable=False)
    petrol_litre_percent_daily_income = Column(Numeric(6, 2), nullable=False)
    diesel_litre_percent_daily_income = Column(Numeric(6, 2), nullable=False)
    affordability_tier = Column(String(30), nullable=False)
    source_id = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    country = relationship("DimCountry", back_populates="affordability_records")

    __table_args__ = (
        UniqueConstraint("country_iso3", "reporting_year", name="uq_country_year_afford"),
    )


class FactFleetTrip(Base):
    __tablename__ = "fact_fleet_trip"

    trip_id = Column(String(50), primary_key=True)
    country_iso3 = Column(CHAR(3), ForeignKey("dim_country.country_iso3"), nullable=False)
    vehicle_id = Column(String(50), nullable=False)
    vehicle_class = Column(String(50), nullable=False)
    trip_date = Column(Date, nullable=False)
    distance_km = Column(Numeric(10, 2), nullable=False)
    fuel_consumed_litres = Column(Numeric(10, 2), nullable=False)
    fuel_type = Column(String(30), nullable=False)
    origin_city = Column(String(100), nullable=True)
    destination_city = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class FactFuelPurchase(Base):
    __tablename__ = "fact_fuel_purchase"

    purchase_id = Column(String(50), primary_key=True)
    trip_id = Column(String(50), nullable=True)
    country_iso3 = Column(CHAR(3), ForeignKey("dim_country.country_iso3"), nullable=False)
    purchase_date = Column(Date, nullable=False)
    litres_purchased = Column(Numeric(10, 2), nullable=False)
    price_per_litre_local = Column(Numeric(10, 4), nullable=False)
    total_cost_local = Column(Numeric(12, 2), nullable=False)
    total_cost_usd = Column(Numeric(12, 2), nullable=False)
    fuel_type = Column(String(30), nullable=False)
    station_brand = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ForecastPrediction(Base):
    __tablename__ = "forecast_predictions"

    prediction_id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    country_iso3 = Column(CHAR(3), ForeignKey("dim_country.country_iso3"), nullable=False)
    fuel_type = Column(String(50), nullable=False)
    forecast_horizon_weeks = Column(Integer, nullable=False)
    forecast_target_date = Column(Date, nullable=False)
    predicted_price_usd = Column(Numeric(10, 4), nullable=False)
    confidence_lower_usd = Column(Numeric(10, 4), nullable=False)
    confidence_upper_usd = Column(Numeric(10, 4), nullable=False)
    model_name = Column(String(100), nullable=False)
    model_version = Column(String(50), nullable=False)
    train_mae = Column(Numeric(8, 4), nullable=True)
    train_rmse = Column(Numeric(8, 4), nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)


class AnomalyEvent(Base):
    __tablename__ = "anomaly_events"

    anomaly_id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    entity_type = Column(String(50), nullable=False)
    country_iso3 = Column(CHAR(3), nullable=True)
    product_category = Column(String(50), nullable=True)
    observation_date = Column(Date, nullable=False)
    metric_name = Column(String(100), nullable=False)
    observed_value = Column(Numeric(16, 4), nullable=False)
    expected_baseline = Column(Numeric(16, 4), nullable=False)
    deviation_percent = Column(Numeric(8, 2), nullable=False)
    detection_method = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    alert_description = Column(Text, nullable=False)
    detected_at = Column(DateTime, default=datetime.utcnow)
    is_resolved = Column(Boolean, default=False)


class EtlRunLog(Base):
    __tablename__ = "etl_run_log"

    run_id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    source_id = Column(String(50), nullable=False)
    pipeline_name = Column(String(100), nullable=False)
    status = Column(String(30), nullable=False)
    rows_fetched = Column(Integer, default=0)
    rows_inserted = Column(Integer, default=0)
    rows_updated = Column(Integer, default=0)
    rows_rejected = Column(Integer, default=0)
    duplicate_count = Column(Integer, default=0)
    duration_ms = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class User(Base):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    ai_usages = relationship("AIQuestionUsage", back_populates="user", cascade="all, delete-orphan")


class UserSession(Base):
    __tablename__ = "user_sessions"

    session_token = Column(String(64), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="sessions")


class AIQuestionUsage(Base):
    __tablename__ = "ai_question_usages"

    usage_id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    question_hash = Column(String(64), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(String(20), default="completed", index=True)  # "completed", "failed", "pending"
    model_used = Column(String(50), nullable=True)
    tokens_used = Column(Integer, nullable=True)

    user = relationship("User", back_populates="ai_usages")
