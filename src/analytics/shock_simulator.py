"""
Supply Shock Simulator Engine.
Simulates hypothetical export curtailments, crude price shocks, and commercial fleet financial impacts.
Explicitly identifies assumptions and isolates scenarios from forecasts.
"""

from typing import Dict, Any, List
from src.database.connection import db_manager
from src.analytics.trade_analytics import PetroleumTradeAnalytics
from sqlalchemy import text


class SupplyShockSimulator:
    """Calculates exposure, replacement volumes, and fleet cost impacts under user-defined scenarios."""

    @staticmethod
    def simulate_export_curtailment(
        exporter_iso3: str,
        target_importer_iso3: str,
        product_category: str = "crude_oil",
        export_reduction_pct: float = 15.0,
        assumed_crude_price_delta_usd_per_bbl: float = 12.0,
        exchange_rate_depreciation_pct: float = 3.0,
        monthly_fleet_fuel_consumption_litres: float = 250000.0,
        baseline_retail_price_usd_per_litre: float = 1.05
    ) -> Dict[str, Any]:
        """
        Executes interactive multi-factor sensitivity simulation.
        """
        # 1. Retrieve baseline bilateral trade volume between exporter and target importer
        query = """
        SELECT quantity, quantity_unit, COALESCE(value_usd, 0) AS value_usd
        FROM fact_petroleum_trade
        WHERE exporter_iso3 = :exp
          AND importer_iso3 = :imp
          AND product_category = :prod
          AND trade_direction = 'export'
        ORDER BY reporting_period DESC
        LIMIT 1
        """
        with db_manager.engine.connect() as conn:
            result = conn.execute(text(query), {
                "exp": exporter_iso3,
                "imp": target_importer_iso3,
                "prod": product_category
            }).fetchone()

        if result:
            baseline_bilateral_bpd = float(result[0])
            baseline_annual_val = float(result[2]) if result[2] is not None else 15000000000.0
        else:
            # Aggregate or proxy fallback
            baseline_bilateral_bpd = 500000.0
            baseline_annual_val = 15000000000.0

        # 2. Volume Deficit Calculation
        reduction_fraction = export_reduction_pct / 100.0
        volume_deficit_bpd = baseline_bilateral_bpd * reduction_fraction
        scenario_remaining_supply_bpd = baseline_bilateral_bpd - volume_deficit_bpd
        annual_deficit_barrels = volume_deficit_bpd * 365.0

        # 3. Price Pass-Through Impact (1 barrel = 158.987 litres)
        # Assumed crude price delta per litre
        crude_delta_per_litre_usd = assumed_crude_price_delta_usd_per_bbl / 158.987295
        # Retail price under crude shock + FX depreciation
        scenario_retail_price_usd = (baseline_retail_price_usd_per_litre + crude_delta_per_litre_usd) * (1.0 + (exchange_rate_depreciation_pct / 100.0))
        price_diff_per_litre = scenario_retail_price_usd - baseline_retail_price_usd_per_litre
        price_pct_increase = ((scenario_retail_price_usd - baseline_retail_price_usd_per_litre) / baseline_retail_price_usd_per_litre) * 100.0

        # 4. Commercial Fleet Budget Impact
        baseline_monthly_fleet_spend_usd = monthly_fleet_fuel_consumption_litres * baseline_retail_price_usd_per_litre
        scenario_monthly_fleet_spend_usd = monthly_fleet_fuel_consumption_litres * scenario_retail_price_usd
        additional_monthly_fleet_cost_usd = scenario_monthly_fleet_spend_usd - baseline_monthly_fleet_spend_usd
        annualized_fleet_cost_increase_usd = additional_monthly_fleet_cost_usd * 12.0

        # 5. Sensitivity Matrix (Varying export cuts 5%, 10%, 15%, 20%, 25%)
        sensitivity_curve = []
        for cut in [5.0, 10.0, 15.0, 20.0, 25.0, 30.0]:
            cut_bpd = baseline_bilateral_bpd * (cut / 100.0)
            # Simulated crude escalation: elastic assumption ~ $0.80/bbl per 1% cut
            sim_crude_delta = cut * 0.80
            sim_price_usd = (baseline_retail_price_usd_per_litre + (sim_crude_delta / 158.987)) * (1.0 + (exchange_rate_depreciation_pct / 100.0))
            sim_fleet_monthly = monthly_fleet_fuel_consumption_litres * sim_price_usd
            sensitivity_curve.append({
                "export_cut_pct": cut,
                "deficit_bpd": round(cut_bpd, 0),
                "simulated_crude_delta_usd": round(sim_crude_delta, 2),
                "simulated_retail_price_usd": round(sim_price_usd, 4),
                "fleet_monthly_spend_usd": round(sim_fleet_monthly, 2),
                "additional_cost_usd": round(sim_fleet_monthly - baseline_monthly_fleet_spend_usd, 2)
            })

        return {
            "exporter_iso3": exporter_iso3,
            "target_importer_iso3": target_importer_iso3,
            "product_category": product_category,
            "baseline_bilateral_bpd": round(baseline_bilateral_bpd, 0),
            "export_reduction_pct": export_reduction_pct,
            "volume_deficit_bpd": round(volume_deficit_bpd, 0),
            "annual_deficit_barrels": round(annual_deficit_barrels, 0),
            "scenario_remaining_supply_bpd": round(scenario_remaining_supply_bpd, 0),
            "baseline_retail_price_usd": round(baseline_retail_price_usd_per_litre, 4),
            "scenario_retail_price_usd": round(scenario_retail_price_usd, 4),
            "retail_price_delta_usd": round(price_diff_per_litre, 4),
            "retail_price_pct_increase": round(price_pct_increase, 2),
            "baseline_monthly_fleet_spend_usd": round(baseline_monthly_fleet_spend_usd, 2),
            "scenario_monthly_fleet_spend_usd": round(scenario_monthly_fleet_spend_usd, 2),
            "additional_monthly_fleet_cost_usd": round(additional_monthly_fleet_cost_usd, 2),
            "annualized_fleet_cost_increase_usd": round(annualized_fleet_cost_increase_usd, 2),
            "sensitivity_curve": sensitivity_curve,
            "assumptions_disclaimer": "Scenario Simulation Disclaimer: This calculation tests user-defined hypotheses. It assumes immediate linear retail cost pass-through without accounting for commercial strategic petroleum reserve (SPR) releases, OPEC spare capacity activation, or fuel tax adjustments."
        }
