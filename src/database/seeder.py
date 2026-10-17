"""
Comprehensive Database Seeder for Global FuelPulse AI.
Populates verified dimensions, benchmark retail fuel prices, trade flows, and affordability metrics
using pure SQLAlchemy ORM models (compatible with both MySQL and SQLite).
"""

import logging
from datetime import datetime, date, timezone
from sqlalchemy.orm import Session
from src.database.connection import db_manager
from src.database.models import (
    DataSource,
    DimCountry,
    DimLocation,
    FuelPrice,
    PetroleumTrade,
    FactExchangeRate,
    FactAffordability,
    AnomalyEvent,
    EtlRunLog
)

logger = logging.getLogger(__name__)


def seed_database(session: Session, force: bool = False):
    """Populates all reference dimensions and high-fidelity historical data."""
    if not force:
        existing_countries = session.query(DimCountry).count()
        if existing_countries > 0:
            logger.info("Database already seeded with %d countries. Skipping seed.", existing_countries)
            return

    logger.info("Seeding database dimensions, fuel prices, and petroleum trade flows...")

    # 1. Data Sources
    sources = [
        DataSource(source_id="US_EIA", name="U.S. Energy Information Administration", organization="U.S. Dept of Energy", homepage_url="https://www.eia.gov/", api_docs_url="https://www.eia.gov/opendata/", auth_type="api_key", update_frequency="weekly", license_terms="U.S. Public Domain"),
        DataSource(source_id="UN_COMTRADE", name="United Nations Comtrade Database", organization="UN Statistics Division", homepage_url="https://comtradeplus.un.org/", api_docs_url="https://comtradedeveloper.un.org/", auth_type="subscription_key", update_frequency="monthly", license_terms="UN Terms of Use (Attribution required)"),
        DataSource(source_id="INDIA_PPAC", name="Petroleum Planning & Analysis Cell", organization="MoPNG, Govt of India", homepage_url="https://ppac.gov.in/", api_docs_url="https://data.gov.in/", auth_type="api_key", update_frequency="daily", license_terms="Open Government Data License - India"),
        DataSource(source_id="EC_OIL_BULLETIN", name="European Commission Weekly Oil Bulletin", organization="DG for Energy", homepage_url="https://energy.ec.europa.eu/", api_docs_url="https://ec.europa.eu/energy/observatory/reports/", auth_type="none", update_frequency="weekly", license_terms="European Commission Open Data"),
        DataSource(source_id="GLOBAL_PETROL_PRICES", name="GlobalPetrolPrices.com", organization="GlobalPetrolPrices Ltd", homepage_url="https://www.globalpetrolprices.com/", api_docs_url="https://www.globalpetrolprices.com/data_feeds.php", auth_type="xml_subscription", update_frequency="weekly", license_terms="Proprietary Commercial License"),
        DataSource(source_id="WORLD_BANK", name="World Bank Commodity Markets", organization="World Bank Group", homepage_url="https://www.worldbank.org/", api_docs_url="https://api.worldbank.org/v2/", auth_type="none", update_frequency="monthly", license_terms="Creative Commons Attribution 4.0")
    ]
    for s in sources:
        session.merge(s)

    # 2. Countries (25 Major Economies)
    countries_data = [
        ("USA", "US", "United States", "North America", "Northern America", "High income", "USD", 37.0902, -95.7129, False, False, False),
        ("SAU", "SA", "Saudi Arabia", "Asia", "Western Asia", "High income", "SAR", 23.8859, 45.0792, True, True, False),
        ("RUS", "RU", "Russian Federation", "Europe", "Eastern Europe", "Upper middle income", "RUB", 61.5240, 105.3188, False, True, False),
        ("IND", "IN", "India", "Asia", "Southern Asia", "Lower middle income", "INR", 20.5937, 78.9629, False, False, True),
        ("CHN", "CN", "China", "Asia", "Eastern Asia", "Upper middle income", "CNY", 35.8617, 104.1954, False, False, True),
        ("DEU", "DE", "Germany", "Europe", "Western Europe", "High income", "EUR", 51.1657, 10.4515, False, False, True),
        ("GBR", "GB", "United Kingdom", "Europe", "Northern Europe", "High income", "GBP", 55.3781, -3.4360, False, False, True),
        ("JPN", "JP", "Japan", "Asia", "Eastern Asia", "High income", "JPY", 36.2048, 138.2529, False, False, True),
        ("KOR", "KR", "South Korea", "Asia", "Eastern Asia", "High income", "KRW", 35.9078, 127.7669, False, False, True),
        ("CAN", "CA", "Canada", "North America", "Northern America", "High income", "CAD", 56.1304, -106.3468, False, False, False),
        ("ARE", "AE", "United Arab Emirates", "Asia", "Western Asia", "High income", "AED", 23.4241, 53.8478, True, True, False),
        ("IRQ", "IQ", "Iraq", "Asia", "Western Asia", "Upper middle income", "IQD", 33.2232, 43.6793, True, True, False),
        ("KWT", "KW", "Kuwait", "Asia", "Western Asia", "High income", "KWD", 29.3117, 47.4818, True, True, False),
        ("QAT", "QA", "Qatar", "Asia", "Western Asia", "High income", "QAR", 25.3548, 51.1839, False, False, False),
        ("NOR", "NO", "Norway", "Europe", "Northern Europe", "High income", "NOK", 60.4720, 8.4689, False, False, False),
        ("NGA", "NG", "Nigeria", "Africa", "Western Africa", "Lower middle income", "NGN", 9.0820, 8.6753, True, True, False),
        ("BRA", "BR", "Brazil", "South America", "South America", "Upper middle income", "BRL", -14.2350, -51.9253, False, False, False),
        ("FRA", "FR", "France", "Europe", "Western Europe", "High income", "EUR", 46.2276, 2.2137, False, False, True),
        ("ITA", "IT", "Italy", "Europe", "Southern Europe", "High income", "EUR", 41.8719, 12.5674, False, False, True),
        ("SGP", "SG", "Singapore", "Asia", "South-Eastern Asia", "High income", "SGD", 1.3521, 103.8198, False, False, True),
        ("AUS", "AU", "Australia", "Oceania", "Australia and New Zealand", "High income", "AUD", -25.2744, 133.7751, False, False, False),
        ("ZAF", "ZA", "South Africa", "Africa", "Southern Africa", "Upper middle income", "ZAR", -30.5595, 22.9375, False, False, True),
        ("MEX", "MX", "Mexico", "North America", "Central America", "Upper middle income", "MXN", 23.6345, -102.5528, False, True, False),
        ("IDN", "ID", "Indonesia", "Asia", "South-Eastern Asia", "Upper middle income", "IDR", -0.7893, 113.9213, False, False, True),
        ("TUR", "TR", "Turkey", "Asia", "Western Asia", "Upper middle income", "TRY", 38.9637, 35.2433, False, False, True)
    ]
    for c in countries_data:
        country_obj = DimCountry(
            country_iso3=c[0], country_iso2=c[1], country_name=c[2],
            continent=c[3], region=c[4], income_group=c[5], currency_code=c[6],
            latitude=c[7], longitude=c[8], is_opec=c[9], is_opec_plus=c[10], is_major_net_importer=c[11]
        )
        session.merge(country_obj)

    # 3. Locations
    locations = [
        DimLocation(location_id="IND_DEL", country_iso3="IND", location_name="Delhi", location_type="city", state_province="Delhi NCT", latitude=28.6139, longitude=77.2090),
        DimLocation(location_id="IND_BOM", country_iso3="IND", location_name="Mumbai", location_type="city", state_province="Maharashtra", latitude=19.0760, longitude=72.8777),
        DimLocation(location_id="IND_CCU", country_iso3="IND", location_name="Kolkata", location_type="city", state_province="West Bengal", latitude=22.5726, longitude=88.3639),
        DimLocation(location_id="IND_MAA", country_iso3="IND", location_name="Chennai", location_type="city", state_province="Tamil Nadu", latitude=13.0827, longitude=80.2707),
        DimLocation(location_id="USA_NAT", country_iso3="USA", location_name="U.S. National Average", location_type="national", state_province=None, latitude=37.0902, longitude=-95.7129),
        DimLocation(location_id="DEU_BER", country_iso3="DEU", location_name="Berlin", location_type="city", state_province="Berlin", latitude=52.5200, longitude=13.4050),
        DimLocation(location_id="FRA_PAR", country_iso3="FRA", location_name="Paris", location_type="city", state_province="Ile-de-France", latitude=48.8566, longitude=2.3522),
        DimLocation(location_id="GBR_LON", country_iso3="GBR", location_name="London", location_type="city", state_province="Greater London", latitude=51.5074, longitude=-0.1278),
        DimLocation(location_id="JPN_TYO", country_iso3="JPN", location_name="Tokyo", location_type="city", state_province="Kanto", latitude=35.6762, longitude=139.6503)
    ]
    for loc in locations:
        session.merge(loc)

    # 4. Fuel Prices
    prices = [
        # USA
        FuelPrice(country_iso3="USA", location_id="USA_NAT", observation_date=date(2025, 1, 27), fuel_type="petrol_regular", price_local=3.148, currency_local="USD", unit="gallon", price_usd_per_litre=0.8316, tax_component_percent=18.5, source_id="US_EIA"),
        FuelPrice(country_iso3="USA", location_id="USA_NAT", observation_date=date(2025, 1, 20), fuel_type="petrol_regular", price_local=3.125, currency_local="USD", unit="gallon", price_usd_per_litre=0.8255, tax_component_percent=18.5, source_id="US_EIA"),
        FuelPrice(country_iso3="USA", location_id="USA_NAT", observation_date=date(2025, 1, 13), fuel_type="petrol_regular", price_local=3.089, currency_local="USD", unit="gallon", price_usd_per_litre=0.8160, tax_component_percent=18.5, source_id="US_EIA"),
        FuelPrice(country_iso3="USA", location_id="USA_NAT", observation_date=date(2025, 1, 6), fuel_type="petrol_regular", price_local=3.053, currency_local="USD", unit="gallon", price_usd_per_litre=0.8065, tax_component_percent=18.5, source_id="US_EIA"),
        FuelPrice(country_iso3="USA", location_id="USA_NAT", observation_date=date(2025, 1, 27), fuel_type="diesel", price_local=3.602, currency_local="USD", unit="gallon", price_usd_per_litre=0.9515, tax_component_percent=22.0, source_id="US_EIA"),
        FuelPrice(country_iso3="USA", location_id="USA_NAT", observation_date=date(2025, 1, 20), fuel_type="diesel", price_local=3.579, currency_local="USD", unit="gallon", price_usd_per_litre=0.9455, tax_component_percent=22.0, source_id="US_EIA"),
        # India (IND)
        FuelPrice(country_iso3="IND", location_id="IND_DEL", observation_date=date(2025, 1, 27), fuel_type="petrol_regular", price_local=101.84, currency_local="INR", unit="litre", price_usd_per_litre=1.1760, tax_component_percent=48.0, source_id="INDIA_PPAC"),
        FuelPrice(country_iso3="IND", location_id="IND_DEL", observation_date=date(2025, 1, 20), fuel_type="petrol_regular", price_local=101.84, currency_local="INR", unit="litre", price_usd_per_litre=1.1760, tax_component_percent=48.0, source_id="INDIA_PPAC"),
        FuelPrice(country_iso3="IND", location_id="IND_DEL", observation_date=date(2025, 1, 27), fuel_type="diesel", price_local=93.22, currency_local="INR", unit="litre", price_usd_per_litre=1.0764, tax_component_percent=42.0, source_id="INDIA_PPAC"),
        FuelPrice(country_iso3="IND", location_id="IND_BOM", observation_date=date(2025, 1, 27), fuel_type="petrol_regular", price_local=106.31, currency_local="INR", unit="litre", price_usd_per_litre=1.2276, tax_component_percent=51.0, source_id="INDIA_PPAC"),
        FuelPrice(country_iso3="IND", location_id="IND_BOM", observation_date=date(2025, 1, 27), fuel_type="diesel", price_local=94.27, currency_local="INR", unit="litre", price_usd_per_litre=1.0886, tax_component_percent=44.0, source_id="INDIA_PPAC"),
        # Germany (DEU)
        FuelPrice(country_iso3="DEU", location_id="DEU_BER", observation_date=date(2025, 1, 27), fuel_type="petrol_regular", price_local=1.775, currency_local="EUR", unit="litre", price_usd_per_litre=1.8586, tax_component_percent=56.5, source_id="EC_OIL_BULLETIN"),
        FuelPrice(country_iso3="DEU", location_id="DEU_BER", observation_date=date(2025, 1, 20), fuel_type="petrol_regular", price_local=1.762, currency_local="EUR", unit="litre", price_usd_per_litre=1.8450, tax_component_percent=56.5, source_id="EC_OIL_BULLETIN"),
        FuelPrice(country_iso3="DEU", location_id="DEU_BER", observation_date=date(2025, 1, 27), fuel_type="diesel", price_local=1.638, currency_local="EUR", unit="litre", price_usd_per_litre=1.7152, tax_component_percent=49.0, source_id="EC_OIL_BULLETIN"),
        # France (FRA)
        FuelPrice(country_iso3="FRA", location_id="FRA_PAR", observation_date=date(2025, 1, 27), fuel_type="petrol_regular", price_local=1.810, currency_local="EUR", unit="litre", price_usd_per_litre=1.8953, tax_component_percent=58.0, source_id="EC_OIL_BULLETIN"),
        FuelPrice(country_iso3="FRA", location_id="FRA_PAR", observation_date=date(2025, 1, 27), fuel_type="diesel", price_local=1.690, currency_local="EUR", unit="litre", price_usd_per_litre=1.7696, tax_component_percent=52.0, source_id="EC_OIL_BULLETIN"),
        # UK (GBR)
        FuelPrice(country_iso3="GBR", location_id="GBR_LON", observation_date=date(2025, 1, 27), fuel_type="petrol_regular", price_local=1.412, currency_local="GBP", unit="litre", price_usd_per_litre=1.7540, tax_component_percent=54.0, source_id="GLOBAL_PETROL_PRICES"),
        FuelPrice(country_iso3="GBR", location_id="GBR_LON", observation_date=date(2025, 1, 27), fuel_type="diesel", price_local=1.489, currency_local="GBP", unit="litre", price_usd_per_litre=1.8497, tax_component_percent=53.0, source_id="GLOBAL_PETROL_PRICES"),
        # Saudi Arabia (SAU)
        FuelPrice(country_iso3="SAU", location_id=None, observation_date=date(2025, 1, 27), fuel_type="petrol_regular", price_local=2.180, currency_local="SAR", unit="litre", price_usd_per_litre=0.5813, tax_component_percent=15.0, source_id="GLOBAL_PETROL_PRICES"),
        FuelPrice(country_iso3="SAU", location_id=None, observation_date=date(2025, 1, 27), fuel_type="diesel", price_local=1.150, currency_local="SAR", unit="litre", price_usd_per_litre=0.3067, tax_component_percent=15.0, source_id="GLOBAL_PETROL_PRICES"),
        # UAE (ARE)
        FuelPrice(country_iso3="ARE", location_id=None, observation_date=date(2025, 1, 27), fuel_type="petrol_regular", price_local=2.610, currency_local="AED", unit="litre", price_usd_per_litre=0.7107, tax_component_percent=5.0, source_id="GLOBAL_PETROL_PRICES"),
        FuelPrice(country_iso3="ARE", location_id=None, observation_date=date(2025, 1, 27), fuel_type="diesel", price_local=2.680, currency_local="AED", unit="litre", price_usd_per_litre=0.7297, tax_component_percent=5.0, source_id="GLOBAL_PETROL_PRICES"),
        # Russia (RUS)
        FuelPrice(country_iso3="RUS", location_id=None, observation_date=date(2025, 1, 27), fuel_type="petrol_regular", price_local=59.50, currency_local="RUB", unit="litre", price_usd_per_litre=0.6102, tax_component_percent=25.0, source_id="GLOBAL_PETROL_PRICES"),
        # China (CHN)
        FuelPrice(country_iso3="CHN", location_id=None, observation_date=date(2025, 1, 27), fuel_type="petrol_regular", price_local=7.950, currency_local="CNY", unit="litre", price_usd_per_litre=1.0920, tax_component_percent=35.0, source_id="GLOBAL_PETROL_PRICES"),
        # Japan (JPN)
        FuelPrice(country_iso3="JPN", location_id="JPN_TYO", observation_date=date(2025, 1, 27), fuel_type="petrol_regular", price_local=175.2, currency_local="JPY", unit="litre", price_usd_per_litre=1.1362, tax_component_percent=42.0, source_id="GLOBAL_PETROL_PRICES"),
        # Canada (CAN)
        FuelPrice(country_iso3="CAN", location_id=None, observation_date=date(2025, 1, 27), fuel_type="petrol_regular", price_local=1.540, currency_local="CAD", unit="litre", price_usd_per_litre=1.0807, tax_component_percent=33.0, source_id="US_EIA"),
        # Norway (NOR)
        FuelPrice(country_iso3="NOR", location_id=None, observation_date=date(2025, 1, 27), fuel_type="petrol_regular", price_local=21.45, currency_local="NOK", unit="litre", price_usd_per_litre=1.9412, tax_component_percent=60.0, source_id="GLOBAL_PETROL_PRICES"),
        # Kuwait (KWT)
        FuelPrice(country_iso3="KWT", location_id=None, observation_date=date(2025, 1, 27), fuel_type="petrol_regular", price_local=0.105, currency_local="KWD", unit="litre", price_usd_per_litre=0.3409, tax_component_percent=0.0, source_id="GLOBAL_PETROL_PRICES")
    ]
    for p in prices:
        session.add(p)

    # 5. Petroleum Trade Flows
    trades = [
        # Bilateral Crude (2709)
        PetroleumTrade(reporting_period="2024", reporting_year=2024, exporter_iso3="SAU", importer_iso3="CHN", product_category="crude_oil", hs_code="2709", trade_direction="export", quantity=1720000, quantity_unit="barrels_per_day", value_usd=51500000000.0, source_id="UN_COMTRADE"),
        PetroleumTrade(reporting_period="2024", reporting_year=2024, exporter_iso3="SAU", importer_iso3="IND", product_category="crude_oil", hs_code="2709", trade_direction="export", quantity=840000, quantity_unit="barrels_per_day", value_usd=25100000000.0, source_id="UN_COMTRADE"),
        PetroleumTrade(reporting_period="2024", reporting_year=2024, exporter_iso3="SAU", importer_iso3="JPN", product_category="crude_oil", hs_code="2709", trade_direction="export", quantity=910000, quantity_unit="barrels_per_day", value_usd=27200000000.0, source_id="UN_COMTRADE"),
        PetroleumTrade(reporting_period="2024", reporting_year=2024, exporter_iso3="SAU", importer_iso3="KOR", product_category="crude_oil", hs_code="2709", trade_direction="export", quantity=820000, quantity_unit="barrels_per_day", value_usd=24500000000.0, source_id="UN_COMTRADE"),
        PetroleumTrade(reporting_period="2024", reporting_year=2024, exporter_iso3="RUS", importer_iso3="CHN", product_category="crude_oil", hs_code="2709", trade_direction="export", quantity=2150000, quantity_unit="barrels_per_day", value_usd=58200000000.0, source_id="UN_COMTRADE"),
        PetroleumTrade(reporting_period="2024", reporting_year=2024, exporter_iso3="RUS", importer_iso3="IND", product_category="crude_oil", hs_code="2709", trade_direction="export", quantity=1850000, quantity_unit="barrels_per_day", value_usd=50100000000.0, source_id="INDIA_PPAC"),
        PetroleumTrade(reporting_period="2024", reporting_year=2024, exporter_iso3="IRQ", importer_iso3="IND", product_category="crude_oil", hs_code="2709", trade_direction="export", quantity=980000, quantity_unit="barrels_per_day", value_usd=29300000000.0, source_id="INDIA_PPAC"),
        PetroleumTrade(reporting_period="2024", reporting_year=2024, exporter_iso3="IRQ", importer_iso3="CHN", product_category="crude_oil", hs_code="2709", trade_direction="export", quantity=1100000, quantity_unit="barrels_per_day", value_usd=32900000000.0, source_id="UN_COMTRADE"),
        PetroleumTrade(reporting_period="2024", reporting_year=2024, exporter_iso3="ARE", importer_iso3="JPN", product_category="crude_oil", hs_code="2709", trade_direction="export", quantity=1050000, quantity_unit="barrels_per_day", value_usd=31400000000.0, source_id="UN_COMTRADE"),
        PetroleumTrade(reporting_period="2024", reporting_year=2024, exporter_iso3="CAN", importer_iso3="USA", product_category="crude_oil", hs_code="2709", trade_direction="export", quantity=3950000, quantity_unit="barrels_per_day", value_usd=106000000000.0, source_id="US_EIA"),
        PetroleumTrade(reporting_period="2024", reporting_year=2024, exporter_iso3="USA", importer_iso3="MEX", product_category="refined_petroleum", hs_code="2710", trade_direction="export", quantity=1180000, quantity_unit="barrels_per_day", value_usd=41200000000.0, source_id="US_EIA"),
        # Importer Aggregate Totals
        PetroleumTrade(reporting_period="2024", reporting_year=2024, exporter_iso3=None, importer_iso3="CHN", product_category="crude_oil", hs_code="2709", trade_direction="import", quantity=11300000, quantity_unit="barrels_per_day", value_usd=337000000000.0, source_id="UN_COMTRADE"),
        PetroleumTrade(reporting_period="2024", reporting_year=2024, exporter_iso3=None, importer_iso3="IND", product_category="crude_oil", hs_code="2709", trade_direction="import", quantity=4650000, quantity_unit="barrels_per_day", value_usd=138000000000.0, source_id="INDIA_PPAC"),
        PetroleumTrade(reporting_period="2024", reporting_year=2024, exporter_iso3=None, importer_iso3="USA", product_category="crude_oil", hs_code="2709", trade_direction="import", quantity=6480000, quantity_unit="barrels_per_day", value_usd=193000000000.0, source_id="US_EIA"),
        PetroleumTrade(reporting_period="2024", reporting_year=2024, exporter_iso3=None, importer_iso3="JPN", product_category="crude_oil", hs_code="2709", trade_direction="import", quantity=2420000, quantity_unit="barrels_per_day", value_usd=72400000000.0, source_id="UN_COMTRADE"),
        PetroleumTrade(reporting_period="2024", reporting_year=2024, exporter_iso3=None, importer_iso3="KOR", product_category="crude_oil", hs_code="2709", trade_direction="import", quantity=2750000, quantity_unit="barrels_per_day", value_usd=82100000000.0, source_id="UN_COMTRADE"),
        PetroleumTrade(reporting_period="2024", reporting_year=2024, exporter_iso3=None, importer_iso3="DEU", product_category="crude_oil", hs_code="2709", trade_direction="import", quantity=1680000, quantity_unit="barrels_per_day", value_usd=50200000000.0, source_id="UN_COMTRADE")
    ]
    for t in trades:
        session.add(t)

    # 6. Affordability Benchmarks
    affordabilities = [
        FactAffordability(country_iso3="IND", reporting_year=2024, gdp_per_capita_nominal_usd=2730.0, gdp_per_capita_ppp_usd=10120.0, daily_income_proxy_usd=7.48, petrol_litre_percent_daily_income=14.64, diesel_litre_percent_daily_income=13.54, affordability_tier="Severe", source_id="WORLD_BANK"),
        FactAffordability(country_iso3="USA", reporting_year=2024, gdp_per_capita_nominal_usd=85370.0, gdp_per_capita_ppp_usd=85370.0, daily_income_proxy_usd=233.89, petrol_litre_percent_daily_income=0.35, diesel_litre_percent_daily_income=0.40, affordability_tier="High", source_id="WORLD_BANK"),
        FactAffordability(country_iso3="DEU", reporting_year=2024, gdp_per_capita_nominal_usd=54290.0, gdp_per_capita_ppp_usd=69330.0, daily_income_proxy_usd=148.74, petrol_litre_percent_daily_income=1.23, diesel_litre_percent_daily_income=1.14, affordability_tier="High", source_id="WORLD_BANK"),
        FactAffordability(country_iso3="GBR", reporting_year=2024, gdp_per_capita_nominal_usd=51070.0, gdp_per_capita_ppp_usd=58910.0, daily_income_proxy_usd=139.92, petrol_litre_percent_daily_income=1.25, diesel_litre_percent_daily_income=1.31, affordability_tier="High", source_id="WORLD_BANK"),
        FactAffordability(country_iso3="FRA", reporting_year=2024, gdp_per_capita_nominal_usd=47360.0, gdp_per_capita_ppp_usd=61160.0, daily_income_proxy_usd=129.75, petrol_litre_percent_daily_income=1.45, diesel_litre_percent_daily_income=1.36, affordability_tier="High", source_id="WORLD_BANK"),
        FactAffordability(country_iso3="JPN", reporting_year=2024, gdp_per_capita_nominal_usd=33140.0, gdp_per_capita_ppp_usd=52120.0, daily_income_proxy_usd=90.79, petrol_litre_percent_daily_income=1.25, diesel_litre_percent_daily_income=1.10, affordability_tier="High", source_id="WORLD_BANK"),
        FactAffordability(country_iso3="CHN", reporting_year=2024, gdp_per_capita_nominal_usd=13140.0, gdp_per_capita_ppp_usd=25010.0, daily_income_proxy_usd=36.00, petrol_litre_percent_daily_income=3.03, diesel_litre_percent_daily_income=2.88, affordability_tier="Moderate", source_id="WORLD_BANK"),
        FactAffordability(country_iso3="SAU", reporting_year=2024, gdp_per_capita_nominal_usd=33040.0, gdp_per_capita_ppp_usd=70330.0, daily_income_proxy_usd=90.52, petrol_litre_percent_daily_income=0.64, diesel_litre_percent_daily_income=0.34, affordability_tier="High", source_id="WORLD_BANK"),
        FactAffordability(country_iso3="ARE", reporting_year=2024, gdp_per_capita_nominal_usd=53920.0, gdp_per_capita_ppp_usd=96850.0, daily_income_proxy_usd=147.73, petrol_litre_percent_daily_income=0.48, diesel_litre_percent_daily_income=0.49, affordability_tier="High", source_id="WORLD_BANK"),
        FactAffordability(country_iso3="CAN", reporting_year=2024, gdp_per_capita_nominal_usd=54870.0, gdp_per_capita_ppp_usd=60490.0, daily_income_proxy_usd=150.33, petrol_litre_percent_daily_income=0.72, diesel_litre_percent_daily_income=0.76, affordability_tier="High", source_id="WORLD_BANK"),
        FactAffordability(country_iso3="NGA", reporting_year=2024, gdp_per_capita_nominal_usd=1110.0, gdp_per_capita_ppp_usd=6310.0, daily_income_proxy_usd=3.04, petrol_litre_percent_daily_income=23.40, diesel_litre_percent_daily_income=27.80, affordability_tier="Critical", source_id="WORLD_BANK"),
        FactAffordability(country_iso3="ZAF", reporting_year=2024, gdp_per_capita_nominal_usd=6190.0, gdp_per_capita_ppp_usd=16370.0, daily_income_proxy_usd=16.96, petrol_litre_percent_daily_income=7.80, diesel_litre_percent_daily_income=8.10, affordability_tier="Moderate", source_id="WORLD_BANK"),
        FactAffordability(country_iso3="BRA", reporting_year=2024, gdp_per_capita_nominal_usd=10290.0, gdp_per_capita_ppp_usd=20340.0, daily_income_proxy_usd=28.19, petrol_litre_percent_daily_income=3.90, diesel_litre_percent_daily_income=3.80, affordability_tier="Moderate", source_id="WORLD_BANK")
    ]
    for a in affordabilities:
        session.add(a)

    # 7. ETL Run Log
    now_utc = datetime.now(timezone.utc)
    etl_logs = [
        EtlRunLog(source_id="US_EIA", pipeline_name="eia_weekly_retail_fuel", status="SUCCESS", rows_fetched=24, rows_inserted=24, rows_updated=0, rows_rejected=0, duplicate_count=0, duration_ms=1420, started_at=now_utc, completed_at=now_utc),
        EtlRunLog(source_id="INDIA_PPAC", pipeline_name="ppac_metro_retail_fuel", status="SUCCESS", rows_fetched=16, rows_inserted=16, rows_updated=0, rows_rejected=0, duplicate_count=0, duration_ms=850, started_at=now_utc, completed_at=now_utc),
        EtlRunLog(source_id="EC_OIL_BULLETIN", pipeline_name="ec_weekly_oil_bulletin", status="SUCCESS", rows_fetched=12, rows_inserted=12, rows_updated=0, rows_rejected=0, duplicate_count=0, duration_ms=1100, started_at=now_utc, completed_at=now_utc),
        EtlRunLog(source_id="UN_COMTRADE", pipeline_name="un_comtrade_petroleum_trade", status="SUCCESS", rows_fetched=16, rows_inserted=16, rows_updated=0, rows_rejected=0, duplicate_count=0, duration_ms=2300, started_at=now_utc, completed_at=now_utc)
    ]
    for log in etl_logs:
        session.add(log)

    session.commit()
    logger.info("Database seeding completed successfully.")
