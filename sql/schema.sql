-- ==============================================================================
-- GLOBAL FUELPULSE AI — MYSQL RELATIONAL SCHEMA DDL
-- Database: fuelx_db
-- Target: MySQL 8.0+ / 9.x
-- ==============================================================================

-- 1. DATA SOURCES REGISTRY
CREATE TABLE IF NOT EXISTS data_sources (
    source_id VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    organization VARCHAR(150),
    homepage_url VARCHAR(255),
    api_docs_url VARCHAR(255),
    auth_type VARCHAR(50) DEFAULT 'none',
    update_frequency VARCHAR(50) DEFAULT 'daily',
    license_terms TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. DIMENSION: COUNTRIES
CREATE TABLE IF NOT EXISTS dim_country (
    country_iso3 CHAR(3) NOT NULL PRIMARY KEY,
    country_iso2 CHAR(2) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    continent VARCHAR(50) NOT NULL,
    region VARCHAR(100),
    income_group VARCHAR(50),
    currency_code CHAR(3),
    latitude DECIMAL(9, 6),
    longitude DECIMAL(9, 6),
    is_opec BOOLEAN DEFAULT FALSE,
    is_opec_plus BOOLEAN DEFAULT FALSE,
    is_major_net_importer BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. DIMENSION: LOCATIONS (Sub-national regions, metro cities, ports)
CREATE TABLE IF NOT EXISTS dim_location (
    location_id VARCHAR(50) NOT NULL PRIMARY KEY,
    country_iso3 CHAR(3) NOT NULL,
    location_name VARCHAR(100) NOT NULL,
    location_type VARCHAR(50) DEFAULT 'city', -- city, state, padd_district, port
    state_province VARCHAR(100),
    latitude DECIMAL(9, 6),
    longitude DECIMAL(9, 6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_dim_location_country FOREIGN KEY (country_iso3) 
        REFERENCES dim_country(country_iso3) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. FACT: FUEL PRICES (Granular retail price observations)
CREATE TABLE IF NOT EXISTS fuel_prices (
    price_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    country_iso3 CHAR(3) NOT NULL,
    location_id VARCHAR(50) NULL,
    observation_date DATE NOT NULL,
    fuel_type VARCHAR(50) NOT NULL, -- petrol_regular, petrol_premium, diesel, lpg, kerosene
    price_local DECIMAL(12, 4) NOT NULL,
    currency_local CHAR(3) NOT NULL,
    unit VARCHAR(30) DEFAULT 'litre', -- litre, gallon
    price_usd_per_litre DECIMAL(10, 4) NOT NULL,
    tax_component_percent DECIMAL(5, 2) NULL,
    source_id VARCHAR(50) NOT NULL,
    source_updated_at TIMESTAMP NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_fuel_price_country FOREIGN KEY (country_iso3) 
        REFERENCES dim_country(country_iso3),
    CONSTRAINT fk_fuel_price_source FOREIGN KEY (source_id) 
        REFERENCES data_sources(source_id),
    CONSTRAINT uq_fuel_price_obs UNIQUE (country_iso3, location_id, observation_date, fuel_type, source_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. FACT: PETROLEUM TRADE (Crude oil & refined products import/export flows)
CREATE TABLE IF NOT EXISTS fact_petroleum_trade (
    trade_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    reporting_period VARCHAR(10) NOT NULL, -- YYYY or YYYY-MM
    reporting_year INT NOT NULL,
    exporter_iso3 CHAR(3) NULL,            -- Nullable for aggregate import flows
    importer_iso3 CHAR(3) NULL,            -- Nullable for aggregate export flows
    product_category VARCHAR(50) NOT NULL, -- crude_oil, refined_petroleum, gasoline, diesel, lpg, jet_fuel
    hs_code VARCHAR(10) NULL,              -- 2709 (Crude), 2710 (Refined), etc.
    trade_direction VARCHAR(10) NOT NULL,  -- export, import
    quantity DECIMAL(16, 4) NOT NULL,      -- Trade volume
    quantity_unit VARCHAR(30) NOT NULL,    -- barrels_per_day, thousand_metric_tonnes, barrels
    value_usd DECIMAL(18, 2) NULL,         -- Trade monetary value
    transport_mode VARCHAR(50) DEFAULT 'tanker_pipeline',
    source_id VARCHAR(50) NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_trade_exporter FOREIGN KEY (exporter_iso3) 
        REFERENCES dim_country(country_iso3),
    CONSTRAINT fk_trade_importer FOREIGN KEY (importer_iso3) 
        REFERENCES dim_country(country_iso3),
    CONSTRAINT fk_trade_source FOREIGN KEY (source_id) 
        REFERENCES data_sources(source_id),
    CONSTRAINT uq_petroleum_trade UNIQUE (reporting_period, exporter_iso3, importer_iso3, product_category, trade_direction, source_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. FACT: ENERGY INDICATORS (National production, refinery output, crude benchmarks)
CREATE TABLE IF NOT EXISTS fact_energy_indicator (
    indicator_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    country_iso3 CHAR(3) NULL,
    indicator_code VARCHAR(50) NOT NULL, -- crude_prod_bpd, refinery_capacity_bpd, consumption_bpd, crude_basket_price
    period VARCHAR(10) NOT NULL,
    value DECIMAL(16, 4) NOT NULL,
    unit VARCHAR(30) NOT NULL,
    source_id VARCHAR(50) NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_indicator_country FOREIGN KEY (country_iso3) 
        REFERENCES dim_country(country_iso3),
    CONSTRAINT fk_indicator_source FOREIGN KEY (source_id) 
        REFERENCES data_sources(source_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. FACT: EXCHANGE RATES
CREATE TABLE IF NOT EXISTS fact_exchange_rate (
    rate_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    currency_code CHAR(3) NOT NULL,
    rate_date DATE NOT NULL,
    rate_to_usd DECIMAL(14, 6) NOT NULL, -- 1 USD = X Local Currency
    source_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_exchange_rate UNIQUE (currency_code, rate_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. FACT: FUEL AFFORDABILITY & INCOME INDICATORS
CREATE TABLE IF NOT EXISTS fact_affordability (
    affordability_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    country_iso3 CHAR(3) NOT NULL,
    reporting_year INT NOT NULL,
    gdp_per_capita_nominal_usd DECIMAL(12, 2) NOT NULL,
    gdp_per_capita_ppp_usd DECIMAL(12, 2) NULL,
    daily_income_proxy_usd DECIMAL(10, 2) NOT NULL, -- GDP per capita / 365
    petrol_litre_percent_daily_income DECIMAL(6, 2) NOT NULL,
    diesel_litre_percent_daily_income DECIMAL(6, 2) NOT NULL,
    affordability_tier VARCHAR(30) NOT NULL, -- High, Moderate, Severe, Critical
    source_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_affordability_country FOREIGN KEY (country_iso3) 
        REFERENCES dim_country(country_iso3),
    CONSTRAINT uq_country_year_afford UNIQUE (country_iso3, reporting_year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. FACT: FLEET TRIPS (Logistics and enterprise fleet operations)
CREATE TABLE IF NOT EXISTS fact_fleet_trip (
    trip_id VARCHAR(50) NOT NULL PRIMARY KEY,
    country_iso3 CHAR(3) NOT NULL,
    vehicle_id VARCHAR(50) NOT NULL,
    vehicle_class VARCHAR(50) NOT NULL, -- Heavy Duty Truck, Medium Delivery Van, Light Commercial
    trip_date DATE NOT NULL,
    distance_km DECIMAL(10, 2) NOT NULL,
    fuel_consumed_litres DECIMAL(10, 2) NOT NULL,
    fuel_type VARCHAR(30) NOT NULL,
    origin_city VARCHAR(100),
    destination_city VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_trip_country FOREIGN KEY (country_iso3) 
        REFERENCES dim_country(country_iso3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. FACT: FLEET FUEL PURCHASES
CREATE TABLE IF NOT EXISTS fact_fuel_purchase (
    purchase_id VARCHAR(50) NOT NULL PRIMARY KEY,
    trip_id VARCHAR(50) NULL,
    country_iso3 CHAR(3) NOT NULL,
    purchase_date DATE NOT NULL,
    litres_purchased DECIMAL(10, 2) NOT NULL,
    price_per_litre_local DECIMAL(10, 4) NOT NULL,
    total_cost_local DECIMAL(12, 2) NOT NULL,
    total_cost_usd DECIMAL(12, 2) NOT NULL,
    fuel_type VARCHAR(30) NOT NULL,
    station_brand VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_purchase_country FOREIGN KEY (country_iso3) 
        REFERENCES dim_country(country_iso3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 11. ML: FORECAST PREDICTIONS
CREATE TABLE IF NOT EXISTS forecast_predictions (
    prediction_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    country_iso3 CHAR(3) NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    forecast_horizon_weeks INT NOT NULL,
    forecast_target_date DATE NOT NULL,
    predicted_price_usd DECIMAL(10, 4) NOT NULL,
    confidence_lower_usd DECIMAL(10, 4) NOT NULL,
    confidence_upper_usd DECIMAL(10, 4) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    train_mae DECIMAL(8, 4),
    train_rmse DECIMAL(8, 4),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_forecast_country FOREIGN KEY (country_iso3) 
        REFERENCES dim_country(country_iso3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 12. ML & AUDIT: ANOMALY EVENTS
CREATE TABLE IF NOT EXISTS anomaly_events (
    anomaly_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL, -- fuel_price, trade_volume, ingestion
    country_iso3 CHAR(3) NULL,
    product_category VARCHAR(50) NULL,
    observation_date DATE NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    observed_value DECIMAL(16, 4) NOT NULL,
    expected_baseline DECIMAL(16, 4) NOT NULL,
    deviation_percent DECIMAL(8, 2) NOT NULL,
    detection_method VARCHAR(50) NOT NULL, -- rolling_zscore, mad, iqr, freshness_gap
    severity VARCHAR(20) NOT NULL, -- LOW, MEDIUM, HIGH, CRITICAL
    alert_description TEXT NOT NULL,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_resolved BOOLEAN DEFAULT FALSE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 13. AUDIT & TELEMETRY: ETL RUN LOG
CREATE TABLE IF NOT EXISTS etl_run_log (
    run_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    source_id VARCHAR(50) NOT NULL,
    pipeline_name VARCHAR(100) NOT NULL,
    status VARCHAR(30) NOT NULL, -- SUCCESS, PARTIAL, FAILED, RUNNING
    rows_fetched INT DEFAULT 0,
    rows_inserted INT DEFAULT 0,
    rows_updated INT DEFAULT 0,
    rows_rejected INT DEFAULT 0,
    duplicate_count INT DEFAULT 0,
    duration_ms INT DEFAULT 0,
    error_message TEXT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
