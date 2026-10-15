# Global FuelPulse AI — Power BI Reporting Assets

This directory provides complete reporting specifications, tabular model blueprints, DAX calculations, and connectivity documentation to deploy the executive Power BI reporting layer for **Global FuelPulse AI**.

---

## 📑 Contents

1. [connection_guide.md](file:///Users/HAMZA/.gemini/antigravity/scratch/global-fuelpulse-ai/powerbi/connection_guide.md): Step-by-step setup for connecting Power BI Desktop to MySQL `fuelx_db`, Star-Schema relationships, and gateway refresh.
2. [dax_measures.md](file:///Users/HAMZA/.gemini/antigravity/scratch/global-fuelpulse-ai/powerbi/dax_measures.md): 25+ verified DAX measures covering retail prices, trade balances, HHI supplier risk, affordability proxies, and fleet operations.
3. [pbix_model_blueprint.json](file:///Users/HAMZA/.gemini/antigravity/scratch/global-fuelpulse-ai/powerbi/pbix_model_blueprint.json): Tabular Model Definition (TMDL/BIM) specifying dataset tables, columns, format strings, and relationship cardinalities.

---

## 📊 Dashboard Pages Architecture

The recommended Power BI executive report comprises 8 report tabs:
1. **Executive Overview:** High-level global map, unweighted average retail price, leading exporter and importer KPIs.
2. **Fuel Price Comparison:** Interactive country slicers, USD vs. local currency toggles, WoW and MoM price differentials.
3. **Petroleum Trade Flows:** Sankey/Bilateral corridor visuals, top 20 exporters/importers by volume and customs valuation.
4. **Fuel Affordability Index:** Scatter plot of GDP per capita vs. % daily income, affordability tiers.
5. **Country Supply Risk Monitor:** Import dependence matrix and Herfindahl-Hirschman Index (HHI) concentration scores.
6. **Commercial Fleet Analytics:** Fuel consumption, mileage, cost per kilometre, and monthly spend analysis.
7. **Forecast & Anomaly Monitoring:** Projected price corridors with 95% confidence intervals and historical actuals.
8. **Data Quality & Telemetry:** Ingestion run success rates, row counts, duplicate logs, and source observation latencies.
