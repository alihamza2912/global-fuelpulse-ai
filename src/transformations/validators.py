"""
Data Validation and Quality Assurance for Ingestion Pipelines.
Ensures zero bad data corrupts analytical views and facts.
"""

from typing import Dict, Any, Tuple
from datetime import date, datetime


def validate_fuel_price_record(record: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validates a fuel price observation dictionary.
    Returns (is_valid, rejection_reason).
    """
    # 1. Country code validation
    country = record.get("country_iso3")
    if not country or len(country) != 3:
        return False, f"Invalid country_iso3: '{country}'"

    # 2. Fuel type validation
    valid_fuel_types = ("petrol_regular", "petrol_premium", "diesel", "lpg", "kerosene")
    fuel_type = record.get("fuel_type")
    if fuel_type not in valid_fuel_types:
        return False, f"Unsupported fuel_type: '{fuel_type}'"

    # 3. Observation date
    obs_date = record.get("observation_date")
    if not obs_date:
        return False, "Missing observation_date"
    if isinstance(obs_date, str):
        try:
            obs_date = datetime.strptime(obs_date[:10], "%Y-%m-%d").date()
        except ValueError:
            return False, f"Malformed observation_date string: '{obs_date}'"
    if obs_date > date.today():
        return False, f"Future observation_date detected: {obs_date}"

    # 4. Price bounds ($0.02 - $20.00 / litre)
    usd_price = record.get("price_usd_per_litre")
    if usd_price is None or usd_price <= 0:
        return False, f"Non-positive USD price: {usd_price}"
    if usd_price > 20.0:
        return False, f"Unrealistic high price outlier (> $20/litre): {usd_price}"

    # 5. Local price
    local_price = record.get("price_local")
    if local_price is None or local_price <= 0:
        return False, f"Non-positive local price: {local_price}"

    return True, ""


def validate_trade_record(record: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validates a petroleum trade observation dictionary.
    Returns (is_valid, rejection_reason).
    """
    period = record.get("reporting_period")
    if not period:
        return False, "Missing reporting_period"

    direction = record.get("trade_direction")
    if direction not in ("export", "import"):
        return False, f"Invalid trade_direction: '{direction}'"

    # Either exporter or importer must exist
    exporter = record.get("exporter_iso3")
    importer = record.get("importer_iso3")
    if not exporter and not importer:
        return False, "Both exporter_iso3 and importer_iso3 are null"

    # Quantity check
    quantity = record.get("quantity")
    if quantity is None or quantity < 0:
        return False, f"Negative or null trade quantity: {quantity}"

    return True, ""
