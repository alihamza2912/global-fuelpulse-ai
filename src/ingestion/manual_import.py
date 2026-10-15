"""
Manual File Import Pipeline for Official Statistical Reports (CSV/XLSX).
Allows users to upload or ingest official datasets that lack automated REST APIs.
"""

import io
import logging
import pandas as pd
from typing import Dict, Any, Tuple
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.database.connection import db_manager
from src.transformations.normalizers import normalize_country_iso3, convert_fuel_price_to_usd_per_litre
from src.transformations.validators import validate_fuel_price_record, validate_trade_record
from src.database.models import FuelPrice, PetroleumTrade, EtlRunLog

logger = logging.getLogger(__name__)


def import_fuel_prices_from_dataframe(df: pd.DataFrame, source_id: str, session: Session) -> Dict[str, Any]:
    """
    Ingests fuel price observations from a pandas DataFrame.
    Expected columns: country, observation_date, fuel_type, price_local, currency, unit, [location]
    """
    start_time = datetime.now(timezone.utc)
    inserted = 0
    updated = 0
    rejected = 0
    duplicates = 0
    rejection_reasons = []

    # Standardize column headers
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    for idx, row in df.iterrows():
        country_raw = str(row.get("country", row.get("country_name", "")))
        iso3 = normalize_country_iso3(country_raw)
        if not iso3:
            rejected += 1
            rejection_reasons.append(f"Row {idx}: Unrecognized country '{country_raw}'")
            continue

        fuel_type = str(row.get("fuel_type", "petrol_regular")).lower().strip()
        price_local = float(row.get("price_local", row.get("price", 0)))
        currency = str(row.get("currency", "USD")).upper().strip()
        unit = str(row.get("unit", "litre")).lower().strip()
        location_id = str(row.get("location_id", f"{iso3}_NAT"))

        # Date parsing
        raw_date = row.get("observation_date", row.get("date"))
        try:
            if isinstance(raw_date, datetime):
                obs_date = raw_date.date()
            elif isinstance(raw_date, str):
                obs_date = datetime.strptime(raw_date[:10], "%Y-%m-%d").date()
            else:
                obs_date = datetime.now(timezone.utc).date()
        except Exception:
            rejected += 1
            rejection_reasons.append(f"Row {idx}: Invalid date format '{raw_date}'")
            continue

        usd_litre = convert_fuel_price_to_usd_per_litre(price_local, currency, unit)

        record = {
            "country_iso3": iso3,
            "location_id": location_id,
            "observation_date": obs_date,
            "fuel_type": fuel_type,
            "price_local": price_local,
            "currency_local": currency,
            "unit": unit,
            "price_usd_per_litre": usd_litre,
            "tax_component_percent": row.get("tax_component_percent"),
            "source_id": source_id,
            "source_updated_at": datetime.now(timezone.utc)
        }

        is_valid, reason = validate_fuel_price_record(record)
        if not is_valid:
            rejected += 1
            rejection_reasons.append(f"Row {idx}: {reason}")
            continue

        # Database upsert
        existing = session.query(FuelPrice).filter_by(
            country_iso3=iso3,
            location_id=location_id,
            observation_date=obs_date,
            fuel_type=fuel_type,
            source_id=source_id
        ).first()

        if existing:
            if float(existing.price_local) != price_local:
                existing.price_local = price_local
                existing.price_usd_per_litre = usd_litre
                updated += 1
            else:
                duplicates += 1
        else:
            new_p = FuelPrice(
                country_iso3=iso3,
                location_id=location_id,
                observation_date=obs_date,
                fuel_type=fuel_type,
                price_local=price_local,
                currency_local=currency,
                unit=unit,
                price_usd_per_litre=usd_litre,
                tax_component_percent=row.get("tax_component_percent"),
                source_id=source_id,
                source_updated_at=datetime.now(timezone.utc)
            )
            session.add(new_p)
            inserted += 1

    session.flush()

    # Record telemetry
    log_entry = EtlRunLog(
        source_id=source_id,
        pipeline_name="manual_csv_fuel_price_import",
        status="SUCCESS" if rejected == 0 else "PARTIAL",
        rows_fetched=len(df),
        rows_inserted=inserted,
        rows_updated=updated,
        rows_rejected=rejected,
        duplicate_count=duplicates,
        duration_ms=int((datetime.now(timezone.utc) - start_time).total_seconds() * 1000),
        started_at=start_time,
        completed_at=datetime.now(timezone.utc)
    )
    session.add(log_entry)
    session.commit()

    return {
        "rows_total": len(df),
        "inserted": inserted,
        "updated": updated,
        "duplicates": duplicates,
        "rejected": rejected,
        "rejection_reasons": rejection_reasons[:10]
    }
