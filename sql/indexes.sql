-- ==============================================================================
-- GLOBAL FUELPULSE AI — DATABASE PERFORMANCE INDEXES
-- Optimizes filtered queries on date ranges, countries, products, and sources
-- ==============================================================================

-- fuel_prices indexes
CREATE INDEX idx_fp_country_date ON fuel_prices(country_iso3, observation_date);
CREATE INDEX idx_fp_fuel_date ON fuel_prices(fuel_type, observation_date);
CREATE INDEX idx_fp_source_date ON fuel_prices(source_id, observation_date);
CREATE INDEX idx_fp_usd_price ON fuel_prices(price_usd_per_litre);

-- fact_petroleum_trade indexes
CREATE INDEX idx_trade_period_prod ON fact_petroleum_trade(reporting_period, product_category);
CREATE INDEX idx_trade_exporter ON fact_petroleum_trade(exporter_iso3, reporting_year);
CREATE INDEX idx_trade_importer ON fact_petroleum_trade(importer_iso3, reporting_year);
CREATE INDEX idx_trade_direction ON fact_petroleum_trade(trade_direction, reporting_year);

-- fact_affordability indexes
CREATE INDEX idx_afford_country_year ON fact_affordability(country_iso3, reporting_year);

-- fact_exchange_rate indexes
CREATE INDEX idx_fx_curr_date ON fact_exchange_rate(currency_code, rate_date);

-- anomaly_events indexes
CREATE INDEX idx_anomaly_date_severity ON anomaly_events(observation_date, severity);
CREATE INDEX idx_anomaly_entity ON anomaly_events(entity_type, country_iso3);

-- etl_run_log indexes
CREATE INDEX idx_etl_source_status ON etl_run_log(source_id, status);
CREATE INDEX idx_etl_started ON etl_run_log(started_at);
