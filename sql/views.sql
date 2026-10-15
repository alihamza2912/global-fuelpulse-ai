-- ==============================================================================
-- GLOBAL FUELPULSE AI — ANALYTICAL SQL VIEWS
-- Optimized for High-Performance BI Dashboards & Streamlit Metrics
-- ==============================================================================

-- 1. LATEST AVAILABLE FUEL PRICES PER COUNTRY & FUEL TYPE
CREATE OR REPLACE VIEW vw_latest_fuel_prices AS
WITH ranked_prices AS (
    SELECT 
        fp.price_id,
        fp.country_iso3,
        c.country_name,
        c.continent,
        c.region,
        fp.location_id,
        loc.location_name,
        fp.observation_date,
        fp.fuel_type,
        fp.price_local,
        fp.currency_local,
        fp.unit,
        fp.price_usd_per_litre,
        fp.tax_component_percent,
        fp.source_id,
        ds.name AS source_name,
        fp.source_updated_at,
        fp.ingested_at,
        ROW_NUMBER() OVER (
            PARTITION BY fp.country_iso3, fp.fuel_type, COALESCE(fp.location_id, 'NATIONAL') 
            ORDER BY fp.observation_date DESC, fp.ingested_at DESC
        ) as rn
    FROM fuel_prices fp
    JOIN dim_country c ON fp.country_iso3 = c.country_iso3
    LEFT JOIN dim_location loc ON fp.location_id = loc.location_id
    JOIN data_sources ds ON fp.source_id = ds.source_id
)
SELECT 
    price_id,
    country_iso3,
    country_name,
    continent,
    region,
    location_id,
    location_name,
    observation_date,
    fuel_type,
    price_local,
    currency_local,
    unit,
    price_usd_per_litre,
    tax_component_percent,
    source_id,
    source_name,
    source_updated_at,
    ingested_at
FROM ranked_prices
WHERE rn = 1;

-- 2. HISTORICAL PRICE CHANGES (Current vs Previous Observation Period)
CREATE OR REPLACE VIEW vw_price_changes_weekly_monthly AS
WITH lagged_prices AS (
    SELECT 
        country_iso3,
        fuel_type,
        COALESCE(location_id, 'NATIONAL') as loc_id,
        observation_date,
        price_usd_per_litre,
        price_local,
        currency_local,
        LAG(price_usd_per_litre, 1) OVER (
            PARTITION BY country_iso3, fuel_type, COALESCE(location_id, 'NATIONAL') 
            ORDER BY observation_date ASC
        ) as prev_price_usd,
        LAG(observation_date, 1) OVER (
            PARTITION BY country_iso3, fuel_type, COALESCE(location_id, 'NATIONAL') 
            ORDER BY observation_date ASC
        ) as prev_observation_date
    FROM fuel_prices
)
SELECT 
    lp.country_iso3,
    c.country_name,
    c.continent,
    lp.fuel_type,
    lp.loc_id,
    lp.observation_date AS current_date,
    lp.prev_observation_date,
    lp.price_usd_per_litre AS current_price_usd,
    lp.prev_price_usd,
    (lp.price_usd_per_litre - lp.prev_price_usd) AS absolute_change_usd,
    CASE 
        WHEN lp.prev_price_usd > 0 
        THEN ROUND(((lp.price_usd_per_litre - lp.prev_price_usd) / lp.prev_price_usd) * 100, 2)
        ELSE NULL 
    END AS pct_change_usd
FROM lagged_prices lp
JOIN dim_country c ON lp.country_iso3 = c.country_iso3
WHERE lp.prev_price_usd IS NOT NULL;

-- 3. TOP PETROLEUM EXPORTERS BY PRODUCT & PERIOD
CREATE OR REPLACE VIEW vw_top_petroleum_exporters AS
SELECT 
    t.reporting_period,
    t.reporting_year,
    t.product_category,
    t.exporter_iso3,
    c.country_name AS exporter_country,
    c.continent,
    c.is_opec,
    c.is_opec_plus,
    t.quantity_unit,
    SUM(t.quantity) AS total_export_quantity,
    SUM(COALESCE(t.value_usd, 0)) AS total_export_value_usd,
    t.source_id
FROM fact_petroleum_trade t
JOIN dim_country c ON t.exporter_iso3 = c.country_iso3
WHERE t.trade_direction = 'export'
GROUP BY 
    t.reporting_period, 
    t.reporting_year, 
    t.product_category, 
    t.exporter_iso3, 
    c.country_name, 
    c.continent, 
    c.is_opec, 
    c.is_opec_plus, 
    t.quantity_unit, 
    t.source_id;

-- 4. TOP PETROLEUM IMPORTERS BY PRODUCT & PERIOD
CREATE OR REPLACE VIEW vw_top_petroleum_importers AS
SELECT 
    t.reporting_period,
    t.reporting_year,
    t.product_category,
    t.importer_iso3,
    c.country_name AS importer_country,
    c.continent,
    c.income_group,
    t.quantity_unit,
    SUM(t.quantity) AS total_import_quantity,
    SUM(COALESCE(t.value_usd, 0)) AS total_import_value_usd,
    t.source_id
FROM fact_petroleum_trade t
JOIN dim_country c ON t.importer_iso3 = c.country_iso3
WHERE t.trade_direction = 'import'
GROUP BY 
    t.reporting_period, 
    t.reporting_year, 
    t.product_category, 
    t.importer_iso3, 
    c.country_name, 
    c.continent, 
    c.income_group, 
    t.quantity_unit, 
    t.source_id;

-- 5. PETROLEUM TRADE BALANCE (EXPORTS - IMPORTS)
CREATE OR REPLACE VIEW vw_petroleum_trade_balance AS
WITH exports_agg AS (
    SELECT 
        reporting_period,
        reporting_year,
        exporter_iso3 AS country_iso3,
        product_category,
        quantity_unit,
        SUM(quantity) AS export_qty,
        SUM(COALESCE(value_usd, 0)) AS export_val_usd
    FROM fact_petroleum_trade
    WHERE trade_direction = 'export'
    GROUP BY reporting_period, reporting_year, exporter_iso3, product_category, quantity_unit
),
imports_agg AS (
    SELECT 
        reporting_period,
        reporting_year,
        importer_iso3 AS country_iso3,
        product_category,
        quantity_unit,
        SUM(quantity) AS import_qty,
        SUM(COALESCE(value_usd, 0)) AS import_val_usd
    FROM fact_petroleum_trade
    WHERE trade_direction = 'import'
    GROUP BY reporting_period, reporting_year, importer_iso3, product_category, quantity_unit
)
SELECT 
    COALESCE(e.reporting_period, i.reporting_period) AS reporting_period,
    COALESCE(e.reporting_year, i.reporting_year) AS reporting_year,
    COALESCE(e.country_iso3, i.country_iso3) AS country_iso3,
    c.country_name,
    c.continent,
    COALESCE(e.product_category, i.product_category) AS product_category,
    COALESCE(e.quantity_unit, i.quantity_unit) AS quantity_unit,
    COALESCE(e.export_qty, 0) AS export_quantity,
    COALESCE(i.import_qty, 0) AS import_quantity,
    (COALESCE(e.export_qty, 0) - COALESCE(i.import_qty, 0)) AS net_export_quantity,
    COALESCE(e.export_val_usd, 0) AS export_value_usd,
    COALESCE(i.import_val_usd, 0) AS import_value_usd,
    (COALESCE(e.export_val_usd, 0) - COALESCE(i.import_val_usd, 0)) AS trade_balance_usd,
    CASE 
        WHEN (COALESCE(e.export_qty, 0) - COALESCE(i.import_qty, 0)) > 0 THEN 'Net Exporter'
        WHEN (COALESCE(e.export_qty, 0) - COALESCE(i.import_qty, 0)) < 0 THEN 'Net Importer'
        ELSE 'Balanced'
    END AS trade_status
FROM exports_agg e
FULL OUTER JOIN imports_agg i 
    ON e.reporting_period = i.reporting_period 
    AND e.country_iso3 = i.country_iso3 
    AND e.product_category = i.product_category 
    AND e.quantity_unit = i.quantity_unit
JOIN dim_country c ON COALESCE(e.country_iso3, i.country_iso3) = c.country_iso3;

-- 6. SUPPLIER CONCENTRATION INDEX (HERFINDAHL-HIRSCHMAN INDEX - HHI)
CREATE OR REPLACE VIEW vw_supplier_concentration_hhi AS
WITH bilateral_totals AS (
    SELECT 
        reporting_period,
        reporting_year,
        importer_iso3,
        product_category,
        quantity_unit,
        SUM(quantity) AS total_imported
    FROM fact_petroleum_trade
    WHERE trade_direction = 'import' AND exporter_iso3 IS NOT NULL
    GROUP BY reporting_period, reporting_year, importer_iso3, product_category, quantity_unit
),
supplier_shares AS (
    SELECT 
        t.reporting_period,
        t.reporting_year,
        t.importer_iso3,
        t.exporter_iso3,
        t.product_category,
        t.quantity,
        bt.total_imported,
        (t.quantity / NULLIF(bt.total_imported, 0)) * 100 AS market_share_percent,
        POWER((t.quantity / NULLIF(bt.total_imported, 0)) * 100, 2) AS squared_market_share
    FROM fact_petroleum_trade t
    JOIN bilateral_totals bt 
        ON t.reporting_period = bt.reporting_period 
        AND t.importer_iso3 = bt.importer_iso3 
        AND t.product_category = bt.product_category
    WHERE t.trade_direction = 'import' AND t.exporter_iso3 IS NOT NULL
)
SELECT 
    ss.reporting_period,
    ss.reporting_year,
    ss.importer_iso3,
    c.country_name AS importer_country,
    ss.product_category,
    COUNT(DISTINCT ss.exporter_iso3) AS active_supplier_count,
    ROUND(SUM(ss.squared_market_share), 2) AS hhi_index,
    CASE 
        WHEN SUM(ss.squared_market_share) < 1500 THEN 'Low Concentration (Diverse)'
        WHEN SUM(ss.squared_market_share) BETWEEN 1500 AND 2500 THEN 'Moderate Concentration'
        ELSE 'High Concentration (Vulnerable)'
    END AS concentration_risk_tier
FROM supplier_shares ss
JOIN dim_country c ON ss.importer_iso3 = c.country_iso3
GROUP BY ss.reporting_period, ss.reporting_year, ss.importer_iso3, c.country_name, ss.product_category;

-- 7. FUEL AFFORDABILITY RANKINGS
CREATE OR REPLACE VIEW vw_fuel_affordability_ranking AS
SELECT 
    fa.affordability_id,
    fa.country_iso3,
    c.country_name,
    c.continent,
    c.income_group,
    fa.reporting_year,
    fa.gdp_per_capita_nominal_usd,
    fa.daily_income_proxy_usd,
    fa.petrol_litre_percent_daily_income,
    fa.diesel_litre_percent_daily_income,
    fa.affordability_tier,
    DENSE_RANK() OVER (ORDER BY fa.petrol_litre_percent_daily_income ASC) as affordability_rank_best_to_worst
FROM fact_affordability fa
JOIN dim_country c ON fa.country_iso3 = c.country_iso3;

-- 8. FLEET OPERATIONAL FUEL COSTS
CREATE OR REPLACE VIEW vw_fleet_fuel_costs AS
SELECT 
    fp.country_iso3,
    c.country_name,
    fp.fuel_type,
    DATE_FORMAT(fp.purchase_date, '%Y-%m') AS purchase_month,
    COUNT(fp.purchase_id) AS total_fuel_transactions,
    SUM(fp.litres_purchased) AS total_litres_purchased,
    SUM(fp.total_cost_usd) AS total_spend_usd,
    ROUND(SUM(fp.total_cost_usd) / NULLIF(SUM(fp.litres_purchased), 0), 4) AS avg_cost_per_litre_usd
FROM fact_fuel_purchase fp
JOIN dim_country c ON fp.country_iso3 = c.country_iso3
GROUP BY fp.country_iso3, c.country_name, fp.fuel_type, DATE_FORMAT(fp.purchase_date, '%Y-%m');

-- 9. DATA QUALITY & PIPELINE HEALTH MONITOR
CREATE OR REPLACE VIEW vw_data_quality_summary AS
SELECT 
    source_id,
    pipeline_name,
    status,
    COUNT(*) AS total_pipeline_runs,
    SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) AS successful_runs,
    ROUND((SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 1) AS success_rate_percent,
    SUM(rows_fetched) AS total_rows_fetched,
    SUM(rows_inserted) AS total_rows_inserted,
    SUM(rows_updated) AS total_rows_updated,
    SUM(rows_rejected) AS total_rows_rejected,
    SUM(duplicate_count) AS total_duplicates_detected,
    MAX(started_at) AS last_run_timestamp,
    AVG(duration_ms) AS avg_execution_duration_ms
FROM etl_run_log
GROUP BY source_id, pipeline_name, status;
