"""
Entity Normalization and Unit Standardization for Global FuelPulse AI.
Standardizes country codes (ISO-3), units of volume/mass, and currency parities.
"""

from typing import Optional, Dict

# Country ISO-3 reference dictionary mapping names, aliases, and ISO-2 codes
COUNTRY_LOOKUP: Dict[str, str] = {
    # Americas
    "UNITED STATES": "USA", "UNITED STATES OF AMERICA": "USA", "USA": "USA", "US": "USA", "U.S.": "USA", "U.S.A.": "USA",
    "CANADA": "CAN", "CAN": "CAN", "CA": "CAN",
    "MEXICO": "MEX", "MEX": "MEX", "MX": "MEX",
    "BRAZIL": "BRA", "BRA": "BRA", "BR": "BRA",
    "ARGENTINA": "ARG", "ARG": "ARG", "AR": "ARG",
    "COLOMBIA": "COL", "COL": "COL", "CO": "COL",
    "VENEZUELA": "VEN", "VEN": "VEN", "VE": "VEN",
    
    # Europe
    "GERMANY": "DEU", "DEU": "DEU", "DE": "DEU", "GER": "DEU",
    "FRANCE": "FRA", "FRA": "FRA", "FR": "FRA",
    "UNITED KINGDOM": "GBR", "GBR": "GBR", "GB": "GBR", "UK": "GBR", "GREAT BRITAIN": "GBR",
    "ITALY": "ITA", "ITA": "ITA", "IT": "ITA",
    "SPAIN": "ESP", "ESP": "ESP", "ES": "ESP",
    "NETHERLANDS": "NLD", "NLD": "NLD", "NL": "NLD",
    "NORWAY": "NOR", "NOR": "NOR", "NO": "NOR",
    "POLAND": "POL", "POL": "POL", "PL": "POL",
    "BELGIUM": "BEL", "BEL": "BEL", "BE": "BEL",
    "SWEDEN": "SWE", "SWE": "SWE", "SE": "SWE",
    "SWITZERLAND": "CHE", "CHE": "CHE", "CH": "CHE",
    "RUSSIA": "RUS", "RUSSIAN FEDERATION": "RUS", "RUS": "RUS", "RU": "RUS",
    "TURKEY": "TUR", "TURKIYE": "TUR", "TUR": "TUR", "TR": "TUR",

    # Asia & Middle East
    "INDIA": "IND", "IND": "IND", "IN": "IND",
    "CHINA": "CHN", "CHINA, PEOPLE'S REPUBLIC OF": "CHN", "CHN": "CHN", "CN": "CHN",
    "JAPAN": "JPN", "JPN": "JPN", "JP": "JPN",
    "SOUTH KOREA": "KOR", "KOREA, REPUBLIC OF": "KOR", "KOR": "KOR", "KR": "KOR",
    "SAUDI ARABIA": "SAU", "SAU": "SAU", "SA": "SAU", "KSA": "SAU",
    "UNITED ARAB EMIRATES": "ARE", "UAE": "ARE", "ARE": "ARE", "AE": "ARE",
    "IRAQ": "IRQ", "IRQ": "IRQ", "IQ": "IRQ",
    "IRAN": "IRN", "IRN": "IRN", "IR": "IRN",
    "KUWAIT": "KWT", "KWT": "KWT", "KW": "KWT",
    "QATAR": "QAT", "QAT": "QAT", "QA": "QAT",
    "SINGAPORE": "SGP", "SGP": "SGP", "SG": "SGP",
    "INDONESIA": "IDN", "IDN": "IDN", "ID": "IDN",
    "MALAYSIA": "MYS", "MYS": "MYS", "MY": "MYS",
    "THAILAND": "THA", "THA": "THA", "TH": "THA",
    "VIETNAM": "VNM", "VIET NAM": "VNM", "VNM": "VNM", "VN": "VNM",
    "PAKISTAN": "PAK", "PAK": "PAK", "PK": "PAK",

    # Africa
    "NIGERIA": "NGA", "NGA": "NGA", "NG": "NGA",
    "SOUTH AFRICA": "ZAF", "ZAF": "ZAF", "ZA": "ZAF",
    "ANGOLA": "AGO", "AGO": "AGO", "AO": "AGO",
    "ALGERIA": "DZA", "DZA": "DZA", "DZ": "DZA",
    "EGYPT": "EGY", "EGY": "EGY", "EG": "EGY",
    "LIBYA": "LBY", "LBY": "LBY", "LY": "LBY",

    # Oceania
    "AUSTRALIA": "AUS", "AUS": "AUS", "AU": "AUS",
    "NEW ZEALAND": "NZL", "NZL": "NZL", "NZ": "NZL"
}

# Standard Conversion Constants
LITRES_PER_US_GALLON = 3.785411784
LITRES_PER_BARREL = 158.987295
BARRELS_PER_METRIC_TONNE_CRUDE = 7.33  # Average API ~32 degrees crude conversion

# Reference exchange rates relative to USD (1 USD = X local currency)
# Updated to active official baseline parities
DEFAULT_EXCHANGE_RATES: Dict[str, float] = {
    "USD": 1.0,
    "EUR": 0.955,
    "GBP": 0.805,
    "INR": 86.60,
    "SAR": 3.75,
    "AED": 3.6725,
    "RUB": 97.50,
    "CNY": 7.28,
    "JPY": 154.20,
    "KRW": 1420.0,
    "CAD": 1.425,
    "AUD": 1.585,
    "BRL": 6.12,
    "SGD": 1.352,
    "NOK": 11.05,
    "TRY": 35.40,
    "IDR": 16250.0,
    "ZAR": 18.50,
    "NGN": 1520.0,
    "IQD": 1310.0,
    "KWD": 0.308,
    "QAR": 3.64
}


def normalize_country_iso3(raw_name: Optional[str]) -> Optional[str]:
    """Resolves arbitrary country name strings or codes to ISO 3166-1 alpha-3."""
    if not raw_name:
        return None
    cleaned = str(raw_name).strip().upper()
    return COUNTRY_LOOKUP.get(cleaned, None)


def convert_fuel_price_to_usd_per_litre(
    price_local: float,
    currency: str,
    unit: str = "litre",
    exchange_rates: Optional[Dict[str, float]] = None
) -> float:
    """
    Standardizes fuel retail price to USD per Litre.
    Handles gallons, litres, barrels, and currency conversion.
    """
    if price_local <= 0:
        return 0.0

    fx_table = exchange_rates or DEFAULT_EXCHANGE_RATES
    fx_rate = fx_table.get(currency.upper(), 1.0)
    if fx_rate <= 0:
        fx_rate = 1.0

    # 1. Convert local currency to USD
    price_usd_in_unit = price_local / fx_rate

    # 2. Normalize unit to per litre
    unit_lower = unit.lower().strip()
    if unit_lower in ("gallon", "us_gallon", "gal"):
        price_usd_per_litre = price_usd_in_unit / LITRES_PER_US_GALLON
    elif unit_lower in ("barrel", "bbl"):
        price_usd_per_litre = price_usd_in_unit / LITRES_PER_BARREL
    else:  # already per litre
        price_usd_per_litre = price_usd_in_unit

    return round(price_usd_per_litre, 4)


def convert_trade_quantity_to_bpd(quantity: float, unit: str) -> float:
    """Standardizes trade quantity to Barrels Per Day (BPD)."""
    unit_lower = unit.lower().strip()
    if unit_lower in ("barrels_per_day", "bpd", "barrel/day"):
        return quantity
    elif unit_lower in ("thousand_metric_tonnes_per_year", "tmt_per_year"):
        # 1 TMT = 1,000 tonnes * 7.33 bbl = 7,330 bbl / 365 days
        return (quantity * 1000.0 * BARRELS_PER_METRIC_TONNE_CRUDE) / 365.0
    elif unit_lower in ("barrels", "bbl"):
        # Assuming annual reporting period
        return quantity / 365.0
    return quantity
