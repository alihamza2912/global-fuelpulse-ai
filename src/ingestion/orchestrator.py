"""
Master Ingestion Pipeline Orchestrator for Global FuelPulse AI.
Executes external connectors, records pipeline telemetry, and updates analytical data marts.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from src.database.connection import db_manager
from src.ingestion.fuel_prices.eia_fuel_connector import EIAFuelPriceConnector
from src.ingestion.fuel_prices.ppac_india_connector import PPACIndiaConnector
from src.ingestion.fuel_prices.ec_oil_bulletin import ECOilBulletinConnector
from src.ingestion.fuel_prices.globalpetrolprices import GlobalPetrolPricesConnector
from src.ingestion.exchange_rates.open_er_connector import OpenExchangeRateConnector
from src.ingestion.petroleum_trade.un_comtrade_connector import UNComtradeConnector
from src.ingestion.petroleum_trade.eia_trade_connector import EIATradeConnector
from src.database.models import EtlRunLog

logger = logging.getLogger(__name__)


class IngestionOrchestrator:
    """Coordinates scheduled or manual execution of all data connectors."""

    def __init__(self):
        self.connectors = [
            OpenExchangeRateConnector(),
            EIAFuelPriceConnector(),
            PPACIndiaConnector(),
            ECOilBulletinConnector(),
            GlobalPetrolPricesConnector(),
            UNComtradeConnector(),
            EIATradeConnector()
        ]

    def run_all(self) -> List[Dict[str, Any]]:
        """Executes all registered connectors sequentially inside managed sessions."""
        summaries = []
        logger.info("Initiating full ingestion cycle across %d connectors...", len(self.connectors))

        for connector in self.connectors:
            try:
                with db_manager.get_session() as session:
                    summary = connector.run_pipeline(session)
                    summaries.append(summary)
            except Exception as e:
                logger.error("Connector [%s] run failed: %s", connector.pipeline_name, e)
                summaries.append({
                    "source_id": connector.source_id,
                    "pipeline_name": connector.pipeline_name,
                    "status": "FAILED",
                    "error_message": str(e)
                })

        return summaries

    def run_live_refresh(self) -> List[Dict[str, Any]]:
        """Executes live retail fuel prices, exchange rate synchronization, and international petroleum trade flows."""
        live_connectors = [
            OpenExchangeRateConnector(),
            EIAFuelPriceConnector(),
            PPACIndiaConnector(),
            ECOilBulletinConnector(),
            GlobalPetrolPricesConnector(),
            UNComtradeConnector(),
            EIATradeConnector()
        ]
        summaries = []
        logger.info("Triggering live data refresh across %d connectors...", len(live_connectors))
        for c in live_connectors:
            try:
                with db_manager.get_session() as session:
                    res = c.run_pipeline(session)
                    summaries.append(res)
            except Exception as e:
                logger.error("Live refresh connector [%s] error: %s", c.pipeline_name, e)
                summaries.append({
                    "source_id": c.source_id,
                    "pipeline_name": c.pipeline_name,
                    "status": "FAILED",
                    "error_message": str(e)
                })
        return summaries

    def run_fuel_prices_only(self) -> List[Dict[str, Any]]:
        """Executes only retail fuel price pipelines."""
        fuel_connectors = [
            EIAFuelPriceConnector(),
            PPACIndiaConnector(),
            ECOilBulletinConnector(),
            GlobalPetrolPricesConnector()
        ]
        summaries = []
        for c in fuel_connectors:
            with db_manager.get_session() as session:
                summaries.append(c.run_pipeline(session))
        return summaries

    def run_trade_only(self) -> List[Dict[str, Any]]:
        """Executes only international petroleum trade pipelines."""
        trade_connectors = [
            UNComtradeConnector(),
            EIATradeConnector()
        ]
        summaries = []
        for c in trade_connectors:
            with db_manager.get_session() as session:
                summaries.append(c.run_pipeline(session))
        return summaries

    def get_last_sync_timestamps(self) -> Dict[str, Optional[str]]:
        """Returns the most recent successful run timestamp per data source from etl_run_log."""
        result: Dict[str, Optional[str]] = {
            "US_EIA": None,
            "INDIA_PPAC": None,
            "EC_OIL_BULLETIN": None,
            "OPEN_ER_API": None,
            "GLOBAL_PETROL_PRICES": None,
            "UN_COMTRADE": None
        }
        try:
            with db_manager.get_session() as session:
                logs = session.query(EtlRunLog).filter_by(status="SUCCESS").order_by(EtlRunLog.completed_at.desc()).all()
                for log in logs:
                    if log.source_id in result and result[log.source_id] is None:
                        if log.completed_at:
                            result[log.source_id] = log.completed_at.strftime("%Y-%m-%d %H:%M UTC")
        except Exception as e:
            logger.warning("Could not query etl_run_log: %s", e)
        return result


# Global orchestrator singleton
orchestrator = IngestionOrchestrator()
