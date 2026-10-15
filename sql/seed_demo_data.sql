-- ==============================================================================
-- GLOBAL FUELPULSE AI — HIGH-FIDELITY SEED DEMO DATA
-- Realistic historical benchmark observations across 25+ global economies
-- ==============================================================================

-- 1. SEED DATA SOURCES
INSERT INTO data_sources (source_id, name, organization, homepage_url, api_docs_url, auth_type, update_frequency, license_terms) VALUES
('US_EIA', 'U.S. Energy Information Administration', 'U.S. Department of Energy', 'https://www.eia.gov/', 'https://www.eia.gov/opendata/', 'api_key', 'weekly', 'U.S. Public Domain'),
('UN_COMTRADE', 'United Nations Comtrade Database', 'UN Statistics Division', 'https://comtradeplus.un.org/', 'https://comtradedeveloper.un.org/', 'subscription_key', 'monthly', 'UN Terms of Use (Attribution required)'),
('INDIA_PPAC', 'Petroleum Planning & Analysis Cell', 'Ministry of Petroleum & Natural Gas, Govt of India', 'https://ppac.gov.in/', 'https://data.gov.in/', 'api_key', 'daily', 'Government Open Data License - India'),
('EC_OIL_BULLETIN', 'European Commission Weekly Oil Bulletin', 'Directorate-General for Energy', 'https://energy.ec.europa.eu/', 'https://ec.europa.eu/energy/observatory/reports/', 'none', 'weekly', 'European Commission Open Data'),
('GLOBAL_PETROL_PRICES', 'GlobalPetrolPrices.com', 'GlobalPetrolPrices Ltd', 'https://www.globalpetrolprices.com/', 'https://www.globalpetrolprices.com/data_feeds.php', 'xml_subscription', 'weekly', 'Proprietary Commercial License'),
('WORLD_BANK', 'World Bank Commodity Markets', 'World Bank Group', 'https://www.worldbank.org/', 'https://api.worldbank.org/v2/', 'none', 'monthly', 'Creative Commons Attribution 4.0')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 2. SEED DIMENSION COUNTRIES (25 Major Energy Players)
INSERT INTO dim_country (country_iso3, country_iso2, country_name, continent, region, income_group, currency_code, latitude, longitude, is_opec, is_opec_plus, is_major_net_importer) VALUES
('USA', 'US', 'United States', 'North America', 'Northern America', 'High income', 'USD', 37.0902, -95.7129, FALSE, FALSE, FALSE),
('SAU', 'SA', 'Saudi Arabia', 'Asia', 'Western Asia', 'High income', 'SAR', 23.8859, 45.0792, TRUE, TRUE, FALSE),
('RUS', 'RU', 'Russian Federation', 'Europe', 'Eastern Europe', 'Upper middle income', 'RUB', 61.5240, 105.3188, FALSE, TRUE, FALSE),
('IND', 'IN', 'India', 'Asia', 'Southern Asia', 'Lower middle income', 'INR', 20.5937, 78.9629, FALSE, FALSE, TRUE),
('CHN', 'CN', 'China', 'Asia', 'Eastern Asia', 'Upper middle income', 'CNY', 35.8617, 104.1954, FALSE, FALSE, TRUE),
('DEU', 'DE', 'Germany', 'Europe', 'Western Europe', 'High income', 'EUR', 51.1657, 10.4515, FALSE, FALSE, TRUE),
('GBR', 'GB', 'United Kingdom', 'Europe', 'Northern Europe', 'High income', 'GBP', 55.3781, -3.4360, FALSE, FALSE, TRUE),
('JPN', 'JP', 'Japan', 'Asia', 'Eastern Asia', 'High income', 'JPY', 36.2048, 138.2529, FALSE, FALSE, TRUE),
('KOR', 'KR', 'South Korea', 'Asia', 'Eastern Asia', 'High income', 'KRW', 35.9078, 127.7669, FALSE, FALSE, TRUE),
('CAN', 'CA', 'Canada', 'North America', 'Northern America', 'High income', 'CAD', 56.1304, -106.3468, FALSE, FALSE, FALSE),
('ARE', 'AE', 'United Arab Emirates', 'Asia', 'Western Asia', 'High income', 'AED', 23.4241, 53.8478, TRUE, TRUE, FALSE),
('IRQ', 'IQ', 'Iraq', 'Asia', 'Western Asia', 'Upper middle income', 'IQD', 33.2232, 43.6793, TRUE, TRUE, FALSE),
('KWT', 'KW', 'Kuwait', 'Asia', 'Western Asia', 'High income', 'KWD', 29.3117, 47.4818, TRUE, TRUE, FALSE),
('QAT', 'QA', 'Qatar', 'Asia', 'Western Asia', 'High income', 'QAR', 25.3548, 51.1839, FALSE, FALSE, FALSE),
('NOR', 'NO', 'Norway', 'Europe', 'Northern Europe', 'High income', 'NOK', 60.4720, 8.4689, FALSE, FALSE, FALSE),
('NGA', 'NG', 'Nigeria', 'Africa', 'Western Africa', 'Lower middle income', 'NGN', 9.0820, 8.6753, TRUE, TRUE, FALSE),
('BRA', 'BR', 'Brazil', 'South America', 'South America', 'Upper middle income', 'BRL', -14.2350, -51.9253, FALSE, FALSE, FALSE),
('FRA', 'FR', 'France', 'Europe', 'Western Europe', 'High income', 'EUR', 46.2276, 2.2137, FALSE, FALSE, TRUE),
('ITA', 'IT', 'Italy', 'Europe', 'Southern Europe', 'High income', 'EUR', 41.8719, 12.5674, FALSE, FALSE, TRUE),
('SGP', 'SG', 'Singapore', 'Asia', 'South-Eastern Asia', 'High income', 'SGD', 1.3521, 103.8198, FALSE, FALSE, TRUE),
('AUS', 'AU', 'Australia', 'Oceania', 'Australia and New Zealand', 'High income', 'AUD', -25.2744, 133.7751, FALSE, FALSE, FALSE),
('ZAF', 'ZA', 'South Africa', 'Africa', 'Southern Africa', 'Upper middle income', 'ZAR', -30.5595, 22.9375, FALSE, FALSE, TRUE),
('MEX', 'MX', 'Mexico', 'North America', 'Central America', 'Upper middle income', 'MXN', 23.6345, -102.5528, FALSE, TRUE, FALSE),
('IDN', 'ID', 'Indonesia', 'Asia', 'South-Eastern Asia', 'Upper middle income', 'IDR', -0.7893, 113.9213, FALSE, FALSE, TRUE),
('TUR', 'TR', 'Turkey', 'Asia', 'Western Asia', 'Upper middle income', 'TRY', 38.9637, 35.2433, FALSE, FALSE, TRUE)
ON DUPLICATE KEY UPDATE country_name=VALUES(country_name);

-- 3. SEED DIMENSION LOCATIONS
INSERT INTO dim_location (location_id, country_iso3, location_name, location_type, state_province, latitude, longitude) VALUES
('IND_DEL', 'IND', 'Delhi', 'city', 'Delhi NCT', 28.6139, 77.2090),
('IND_BOM', 'IND', 'Mumbai', 'city', 'Maharashtra', 19.0760, 72.8777),
('IND_CCU', 'IND', 'Kolkata', 'city', 'West Bengal', 22.5726, 88.3639),
('IND_MAA', 'IND', 'Chennai', 'city', 'Tamil Nadu', 13.0827, 80.2707),
('USA_NAT', 'USA', 'U.S. National Average', 'national', NULL, 37.0902, -95.7129),
('USA_PADD1', 'USA', 'East Coast (PADD 1)', 'padd_district', 'East Coast', 40.7128, -74.0060),
('USA_PADD3', 'USA', 'Gulf Coast (PADD 3)', 'padd_district', 'Gulf Coast', 29.7604, -95.3698),
('USA_PADD5', 'USA', 'West Coast (PADD 5)', 'padd_district', 'West Coast', 34.0522, -118.2437),
('DEU_BER', 'DEU', 'Berlin', 'city', 'Berlin', 52.5200, 13.4050),
('GBR_LON', 'GBR', 'London', 'city', 'Greater London', 51.5074, -0.1278),
('FRA_PAR', 'FRA', 'Paris', 'city', 'Ile-de-France', 48.8566, 2.3522),
('JPN_TYO', 'JPN', 'Tokyo', 'city', 'Kanto', 35.6762, 139.6503)
ON DUPLICATE KEY UPDATE location_name=VALUES(location_name);

-- 4. SEED FACT EXCHANGE RATES (Reference against USD)
INSERT INTO fact_exchange_rate (currency_code, rate_date, rate_to_usd, source_id) VALUES
('USD', '2025-01-01', 1.000000, 'US_EIA'),
('INR', '2025-01-01', 86.500000, 'INDIA_PPAC'),
('EUR', '2025-01-01', 0.960000, 'EC_OIL_BULLETIN'),
('GBP', '2025-01-01', 0.810000, 'GLOBAL_PETROL_PRICES'),
('SAR', '2025-01-01', 3.750000, 'GLOBAL_PETROL_PRICES'),
('RUB', '2025-01-01', 98.200000, 'GLOBAL_PETROL_PRICES'),
('CNY', '2025-01-01', 7.280000, 'GLOBAL_PETROL_PRICES'),
('JPY', '2025-01-01', 154.500000, 'GLOBAL_PETROL_PRICES'),
('CAD', '2025-01-01', 1.420000, 'US_EIA'),
('AUD', '2025-01-01', 1.580000, 'GLOBAL_PETROL_PRICES'),
('BRL', '2025-01-01', 6.100000, 'GLOBAL_PETROL_PRICES'),
('SGD', '2025-01-01', 1.350000, 'GLOBAL_PETROL_PRICES')
ON DUPLICATE KEY UPDATE rate_to_usd=VALUES(rate_to_usd);

-- 5. SEED FACT FUEL PRICES (Current and historical retail benchmark prices)
INSERT INTO fuel_prices (country_iso3, location_id, observation_date, fuel_type, price_local, currency_local, unit, price_usd_per_litre, tax_component_percent, source_id) VALUES
-- United States (EIA Weekly Data)
('USA', 'USA_NAT', '2025-01-06', 'petrol_regular', 3.0530, 'USD', 'gallon', 0.8065, 18.5, 'US_EIA'),
('USA', 'USA_NAT', '2025-01-13', 'petrol_regular', 3.0890, 'USD', 'gallon', 0.8160, 18.5, 'US_EIA'),
('USA', 'USA_NAT', '2025-01-20', 'petrol_regular', 3.1250, 'USD', 'gallon', 0.8255, 18.5, 'US_EIA'),
('USA', 'USA_NAT', '2025-01-06', 'diesel', 3.5120, 'USD', 'gallon', 0.9278, 22.0, 'US_EIA'),
('USA', 'USA_NAT', '2025-01-13', 'diesel', 3.5480, 'USD', 'gallon', 0.9373, 22.0, 'US_EIA'),
('USA', 'USA_NAT', '2025-01-20', 'diesel', 3.5790, 'USD', 'gallon', 0.9455, 22.0, 'US_EIA'),
-- India (PPAC Metro Daily Data)
('IND', 'IND_DEL', '2025-01-06', 'petrol_regular', 94.7200, 'INR', 'litre', 1.0950, 48.0, 'INDIA_PPAC'),
('IND', 'IND_DEL', '2025-01-13', 'petrol_regular', 94.7200, 'INR', 'litre', 1.0950, 48.0, 'INDIA_PPAC'),
('IND', 'IND_DEL', '2025-01-20', 'petrol_regular', 94.7200, 'INR', 'litre', 1.0950, 48.0, 'INDIA_PPAC'),
('IND', 'IND_DEL', '2025-01-06', 'diesel', 87.6200, 'INR', 'litre', 1.0130, 42.0, 'INDIA_PPAC'),
('IND', 'IND_DEL', '2025-01-13', 'diesel', 87.6200, 'INR', 'litre', 1.0130, 42.0, 'INDIA_PPAC'),
('IND', 'IND_DEL', '2025-01-20', 'diesel', 87.6200, 'INR', 'litre', 1.0130, 42.0, 'INDIA_PPAC'),
('IND', 'IND_BOM', '2025-01-20', 'petrol_regular', 104.2100, 'INR', 'litre', 1.2047, 51.0, 'INDIA_PPAC'),
('IND', 'IND_BOM', '2025-01-20', 'diesel', 92.1500, 'INR', 'litre', 1.0653, 44.0, 'INDIA_PPAC'),
-- Germany (EC Weekly Oil Bulletin)
('DEU', 'DEU_BER', '2025-01-06', 'petrol_regular', 1.7200, 'EUR', 'litre', 1.7917, 56.5, 'EC_OIL_BULLETIN'),
('DEU', 'DEU_BER', '2025-01-13', 'petrol_regular', 1.7450, 'EUR', 'litre', 1.8177, 56.5, 'EC_OIL_BULLETIN'),
('DEU', 'DEU_BER', '2025-01-20', 'petrol_regular', 1.7620, 'EUR', 'litre', 1.8354, 56.5, 'EC_OIL_BULLETIN'),
('DEU', 'DEU_BER', '2025-01-20', 'diesel', 1.6250, 'EUR', 'litre', 1.6927, 49.0, 'EC_OIL_BULLETIN'),
-- France (EC Weekly Oil Bulletin)
('FRA', 'FRA_PAR', '2025-01-20', 'petrol_regular', 1.8100, 'EUR', 'litre', 1.8854, 58.0, 'EC_OIL_BULLETIN'),
('FRA', 'FRA_PAR', '2025-01-20', 'diesel', 1.6900, 'EUR', 'litre', 1.7604, 52.0, 'EC_OIL_BULLETIN'),
-- United Kingdom (GlobalPetrolPrices)
('GBR', 'GBR_LON', '2025-01-20', 'petrol_regular', 1.4120, 'GBP', 'litre', 1.7432, 54.0, 'GLOBAL_PETROL_PRICES'),
('GBR', 'GBR_LON', '2025-01-20', 'diesel', 1.4890, 'GBP', 'litre', 1.8383, 53.0, 'GLOBAL_PETROL_PRICES'),
-- Saudi Arabia (Low retail price, domestic subsidies)
('SAU', NULL, '2025-01-20', 'petrol_regular', 2.1800, 'SAR', 'litre', 0.5813, 15.0, 'GLOBAL_PETROL_PRICES'),
('SAU', NULL, '2025-01-20', 'diesel', 1.1500, 'SAR', 'litre', 0.3067, 15.0, 'GLOBAL_PETROL_PRICES'),
-- UAE
('ARE', NULL, '2025-01-20', 'petrol_regular', 2.6100, 'AED', 'litre', 0.7107, 5.0, 'GLOBAL_PETROL_PRICES'),
('ARE', NULL, '2025-01-20', 'diesel', 2.6800, 'AED', 'litre', 0.7297, 5.0, 'GLOBAL_PETROL_PRICES'),
-- China
('CHN', NULL, '2025-01-20', 'petrol_regular', 7.9500, 'CNY', 'litre', 1.0920, 35.0, 'GLOBAL_PETROL_PRICES'),
('CHN', NULL, '2025-01-20', 'diesel', 7.5500, 'CNY', 'litre', 1.0371, 32.0, 'GLOBAL_PETROL_PRICES'),
-- Japan
('JPN', 'JPN_TYO', '2025-01-20', 'petrol_regular', 175.2000, 'JPY', 'litre', 1.1340, 42.0, 'GLOBAL_PETROL_PRICES'),
('JPN', 'JPN_TYO', '2025-01-20', 'diesel', 154.8000, 'JPY', 'litre', 1.0020, 36.0, 'GLOBAL_PETROL_PRICES'),
-- Canada
('CAN', NULL, '2025-01-20', 'petrol_regular', 1.5400, 'CAD', 'litre', 1.0845, 33.0, 'US_EIA'),
('CAN', NULL, '2025-01-20', 'diesel', 1.6200, 'CAD', 'litre', 1.1408, 30.0, 'US_EIA'),
-- Australia
('AUS', NULL, '2025-01-20', 'petrol_regular', 1.8200, 'AUD', 'litre', 1.1519, 38.0, 'GLOBAL_PETROL_PRICES'),
('AUS', NULL, '2025-01-20', 'diesel', 1.8900, 'AUD', 'litre', 1.1962, 38.0, 'GLOBAL_PETROL_PRICES'),
-- Norway (High fuel tax benchmark)
('NOR', NULL, '2025-01-20', 'petrol_regular', 21.4500, 'NOK', 'litre', 1.9500, 60.0, 'GLOBAL_PETROL_PRICES'),
('NOR', NULL, '2025-01-20', 'diesel', 20.1000, 'NOK', 'litre', 1.8273, 55.0, 'GLOBAL_PETROL_PRICES')
ON DUPLICATE KEY UPDATE price_local=VALUES(price_local), price_usd_per_litre=VALUES(price_usd_per_litre);

-- 6. SEED FACT PETROLEUM TRADE (UN Comtrade & EIA Official Annual Volumes 2023-2024)
INSERT INTO fact_petroleum_trade (reporting_period, reporting_year, exporter_iso3, importer_iso3, product_category, hs_code, trade_direction, quantity, quantity_unit, value_usd, source_id) VALUES
-- Bilateral Crude Flows (HS 2709) - Saudi Arabia Exporter
('2024', 2024, 'SAU', 'CHN', 'crude_oil', '2709', 'export', 1720000, 'barrels_per_day', 51500000000.00, 'UN_COMTRADE'),
('2024', 2024, 'SAU', 'IND', 'crude_oil', '2709', 'export', 840000, 'barrels_per_day', 25100000000.00, 'UN_COMTRADE'),
('2024', 2024, 'SAU', 'JPN', 'crude_oil', '2709', 'export', 910000, 'barrels_per_day', 27200000000.00, 'UN_COMTRADE'),
('2024', 2024, 'SAU', 'KOR', 'crude_oil', '2709', 'export', 820000, 'barrels_per_day', 24500000000.00, 'UN_COMTRADE'),
('2024', 2024, 'SAU', 'USA', 'crude_oil', '2709', 'export', 310000, 'barrels_per_day', 9250000000.00, 'US_EIA'),

-- Russia Exporter (Displaced to Asian buyers)
('2024', 2024, 'RUS', 'CHN', 'crude_oil', '2709', 'export', 2150000, 'barrels_per_day', 58200000000.00, 'UN_COMTRADE'),
('2024', 2024, 'RUS', 'IND', 'crude_oil', '2709', 'export', 1850000, 'barrels_per_day', 50100000000.00, 'INDIA_PPAC'),
('2024', 2024, 'RUS', 'TUR', 'crude_oil', '2709', 'export', 280000, 'barrels_per_day', 7600000000.00, 'UN_COMTRADE'),

-- Iraq Exporter
('2024', 2024, 'IRQ', 'IND', 'crude_oil', '2709', 'export', 980000, 'barrels_per_day', 29300000000.00, 'INDIA_PPAC'),
('2024', 2024, 'IRQ', 'CHN', 'crude_oil', '2709', 'export', 1100000, 'barrels_per_day', 32900000000.00, 'UN_COMTRADE'),
('2024', 2024, 'IRQ', 'USA', 'crude_oil', '2709', 'export', 220000, 'barrels_per_day', 6550000000.00, 'US_EIA'),

-- UAE Exporter
('2024', 2024, 'ARE', 'JPN', 'crude_oil', '2709', 'export', 1050000, 'barrels_per_day', 31400000000.00, 'UN_COMTRADE'),
('2024', 2024, 'ARE', 'IND', 'crude_oil', '2709', 'export', 450000, 'barrels_per_day', 13450000000.00, 'INDIA_PPAC'),

-- USA Exporter (Crude & Refined)
('2024', 2024, 'USA', 'CAN', 'crude_oil', '2709', 'export', 340000, 'barrels_per_day', 10150000000.00, 'US_EIA'),
('2024', 2024, 'USA', 'KOR', 'crude_oil', '2709', 'export', 410000, 'barrels_per_day', 12250000000.00, 'US_EIA'),
('2024', 2024, 'USA', 'MEX', 'refined_petroleum', '2710', 'export', 1180000, 'barrels_per_day', 41200000000.00, 'US_EIA'),
('2024', 2024, 'USA', 'CAN', 'refined_petroleum', '2710', 'export', 490000, 'barrels_per_day', 17100000000.00, 'US_EIA'),

-- Canada Exporter (Heavy crude to USA)
('2024', 2024, 'CAN', 'USA', 'crude_oil', '2709', 'export', 3950000, 'barrels_per_day', 106000000000.00, 'US_EIA'),

-- Importer flows matching totals
('2024', 2024, NULL, 'IND', 'crude_oil', '2709', 'import', 4650000, 'barrels_per_day', 138000000000.00, 'INDIA_PPAC'),
('2024', 2024, NULL, 'CHN', 'crude_oil', '2709', 'import', 11300000, 'barrels_per_day', 337000000000.00, 'UN_COMTRADE'),
('2024', 2024, NULL, 'USA', 'crude_oil', '2709', 'import', 6480000, 'barrels_per_day', 193000000000.00, 'US_EIA'),
('2024', 2024, NULL, 'JPN', 'crude_oil', '2709', 'import', 2420000, 'barrels_per_day', 72400000000.00, 'UN_COMTRADE'),
('2024', 2024, NULL, 'DEU', 'crude_oil', '2709', 'import', 1680000, 'barrels_per_day', 50200000000.00, 'UN_COMTRADE')
ON DUPLICATE KEY UPDATE quantity=VALUES(quantity), value_usd=VALUES(value_usd);

-- 7. SEED FACT AFFORDABILITY (2024 Benchmark GDP per Capita and % Daily Income)
INSERT INTO fact_affordability (country_iso3, reporting_year, gdp_per_capita_nominal_usd, gdp_per_capita_ppp_usd, daily_income_proxy_usd, petrol_litre_percent_daily_income, diesel_litre_percent_daily_income, affordability_tier, source_id) VALUES
('IND', 2024, 2730.00, 10120.00, 7.48, 14.64, 13.54, 'Severe', 'WORLD_BANK'),
('USA', 2024, 85370.00, 85370.00, 233.89, 0.35, 0.40, 'High', 'WORLD_BANK'),
('DEU', 2024, 54290.00, 69330.00, 148.74, 1.23, 1.14, 'High', 'WORLD_BANK'),
('GBR', 2024, 51070.00, 58910.00, 139.92, 1.25, 1.31, 'High', 'WORLD_BANK'),
('FRA', 2024, 47360.00, 61160.00, 129.75, 1.45, 1.36, 'High', 'WORLD_BANK'),
('JPN', 2024, 33140.00, 52120.00, 90.79, 1.25, 1.10, 'High', 'WORLD_BANK'),
('CHN', 2024, 13140.00, 25010.00, 36.00, 3.03, 2.88, 'Moderate', 'WORLD_BANK'),
('SAU', 2024, 33040.00, 70330.00, 90.52, 0.64, 0.34, 'High', 'WORLD_BANK'),
('ARE', 2024, 53920.00, 96850.00, 147.73, 0.48, 0.49, 'High', 'WORLD_BANK'),
('CAN', 2024, 54870.00, 60490.00, 150.33, 0.72, 0.76, 'High', 'WORLD_BANK'),
('NGA', 2024, 1110.00, 6310.00, 3.04, 23.40, 27.80, 'Critical', 'WORLD_BANK'),
('ZAF', 2024, 6190.00, 16370.00, 16.96, 7.80, 8.10, 'Moderate', 'WORLD_BANK'),
('BRA', 2024, 10290.00, 20340.00, 28.19, 3.90, 3.80, 'Moderate', 'WORLD_BANK')
ON DUPLICATE KEY UPDATE petrol_litre_percent_daily_income=VALUES(petrol_litre_percent_daily_income);

-- 8. SEED ETL RUN LOG
INSERT INTO etl_run_log (source_id, pipeline_name, status, rows_fetched, rows_inserted, rows_updated, rows_rejected, duplicate_count, duration_ms, started_at, completed_at) VALUES
('US_EIA', 'eia_retail_fuel_weekly', 'SUCCESS', 24, 24, 0, 0, 0, 1420, NOW() - INTERVAL 1 HOUR, NOW() - INTERVAL 1 HOUR + INTERVAL 2 SECOND),
('INDIA_PPAC', 'ppac_metro_fuel_daily', 'SUCCESS', 16, 16, 0, 0, 0, 850, NOW() - INTERVAL 2 HOUR, NOW() - INTERVAL 2 HOUR + INTERVAL 1 SECOND),
('EC_OIL_BULLETIN', 'ec_oil_bulletin_weekly', 'SUCCESS', 54, 54, 0, 0, 0, 2100, NOW() - INTERVAL 5 HOUR, NOW() - INTERVAL 5 HOUR + INTERVAL 3 SECOND),
('UN_COMTRADE', 'un_comtrade_petroleum_annual', 'SUCCESS', 85, 85, 0, 0, 0, 3450, NOW() - INTERVAL 1 DAY, NOW() - INTERVAL 1 DAY + INTERVAL 4 SECOND);

-- 9. SEED ANOMALY EVENTS
INSERT INTO anomaly_events (entity_type, country_iso3, product_category, observation_date, metric_name, observed_value, expected_baseline, deviation_percent, detection_method, severity, alert_description) VALUES
('fuel_price', 'USA', 'petrol_regular', '2025-01-20', 'price_usd_per_litre', 0.8255, 0.7800, 5.83, 'rolling_zscore', 'LOW', 'Mild upward deviation in national gasoline retail price due to seasonal refinery turnaround.'),
('trade_volume', 'RUS', 'crude_oil', '2024-12-01', 'export_bpd', 2150000.0000, 1650000.0000, 30.30, 'mad', 'MEDIUM', 'Significant diversion of seaborne crude trade flows to Asian refiners post-sanction reshuffling.');
