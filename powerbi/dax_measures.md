# Global FuelPulse AI — Power BI DAX Measures Reference

This document provides verified, production-grade **DAX (Data Analysis Expressions)** formulas designed for the **Global FuelPulse AI Power BI Executive Dashboard** connected to the MySQL `fuelx_db` database.

---

## 1. Core Retail Price Measures

### 1.1 Latest Retail Petrol Price (USD / Litre)
```dax
Latest Petrol Price USD = 
CALCULATE(
    MAX(fuel_prices[price_usd_per_litre]),
    fuel_prices[fuel_type] = "petrol_regular",
    LASTDATE(fuel_prices[observation_date])
)
```

### 1.2 Latest Retail Diesel Price (USD / Litre)
```dax
Latest Diesel Price USD = 
CALCULATE(
    MAX(fuel_prices[price_usd_per_litre]),
    fuel_prices[fuel_type] = "diesel",
    LASTDATE(fuel_prices[observation_date])
)
```

### 1.3 Prior Period Price (USD / Litre)
```dax
Prior Period Price USD = 
CALCULATE(
    [Latest Petrol Price USD],
    DATEADD('DimDate'[Date], -7, DAY)
)
```

### 1.4 Price WoW Absolute Change
```dax
Price WoW Absolute Change = 
IF(
    NOT ISBLANK([Prior Period Price USD]),
    [Latest Petrol Price USD] - [Prior Period Price USD],
    BLANK()
)
```

### 1.5 Price WoW Percentage Change
```dax
Price WoW % Change = 
DIVIDE(
    [Price WoW Absolute Change],
    [Prior Period Price USD],
    0
)
```

### 1.6 Global Unweighted Average Petrol Price
```dax
Global Avg Petrol Price USD = 
CALCULATE(
    AVERAGE(fuel_prices[price_usd_per_litre]),
    fuel_prices[fuel_type] = "petrol_regular"
)
```

---

## 2. Petroleum Trade & Market Share Measures

### 2.1 Total Petroleum Export Volume (Barrels / Day)
```dax
Total Export Volume (bpd) = 
CALCULATE(
    SUM(fact_petroleum_trade[quantity]),
    fact_petroleum_trade[trade_direction] = "export"
)
```

### 2.2 Total Petroleum Import Volume (Barrels / Day)
```dax
Total Import Volume (bpd) = 
CALCULATE(
    SUM(fact_petroleum_trade[quantity]),
    fact_petroleum_trade[trade_direction] = "import"
)
```

### 2.3 Net Petroleum Trade Balance (bpd)
```dax
Net Petroleum Trade Balance = 
[Total Export Volume (bpd)] - [Total Import Volume (bpd)]
```

### 2.4 Petroleum Export Market Share (%)
```dax
Export Market Share % = 
DIVIDE(
    [Total Export Volume (bpd)],
    CALCULATE([Total Export Volume (bpd)], ALL(dim_country)),
    0
) * 100
```

### 2.5 Total Petroleum Trade Value (USD)
```dax
Total Export Value USD = 
CALCULATE(
    SUM(fact_petroleum_trade[value_usd]),
    fact_petroleum_trade[trade_direction] = "export"
)
```

---

## 3. Supplier Concentration (HHI) Measures

### 3.1 Bilateral Supplier Share (%)
```dax
Supplier Market Share % = 
VAR TotalImported = 
    CALCULATE(
        SUM(fact_petroleum_trade[quantity]),
        ALLEXCEPT(fact_petroleum_trade, fact_petroleum_trade[importer_iso3], fact_petroleum_trade[reporting_period])
    )
RETURN
    DIVIDE(SUM(fact_petroleum_trade[quantity]), TotalImported, 0) * 100
```

### 3.2 Herfindahl-Hirschman Index (HHI)
```dax
HHI Concentration Score = 
SUMX(
    VALUES(fact_petroleum_trade[exporter_iso3]),
    POWER([Supplier Market Share %], 2)
)
```

### 3.3 HHI Risk Classification Tier
```dax
HHI Risk Tier = 
SWITCH(
    TRUE(),
    [HHI Concentration Score] < 1500, "Low Concentration (Diverse)",
    [HHI Concentration Score] <= 2500, "Moderate Concentration",
    [HHI Concentration Score] > 2500, "High Concentration (Vulnerable)",
    "Unclassified"
)
```

---

## 4. Affordability & Macroeconomic Measures

### 4.1 Daily Income Proxy (USD)
```dax
Daily Income Proxy USD = 
DIVIDE(
    MAX(fact_affordability[gdp_per_capita_nominal_usd]),
    365,
    0
)
```

### 4.2 Fuel Spend as % of Daily Income
```dax
Fuel Spend % Daily Income = 
DIVIDE(
    [Latest Petrol Price USD],
    [Daily Income Proxy USD],
    0
) * 100
```

### 4.3 Affordability Tier Description
```dax
Affordability Classification = 
SWITCH(
    TRUE(),
    [Fuel Spend % Daily Income] < 1.0, "High Affordability",
    [Fuel Spend % Daily Income] <= 5.0, "Moderate Affordability",
    [Fuel Spend % Daily Income] <= 15.0, "Severe Burden",
    [Fuel Spend % Daily Income] > 15.0, "Critical Affordability Crisis",
    "No Data"
)
```

---

## 5. Commercial Fleet Fuel Cost Measures

### 5.1 Total Fleet Distance Travelled (km)
```dax
Total Fleet Mileage (km) = 
SUM(fact_fleet_trip[distance_km])
```

### 5.2 Total Fleet Fuel Consumed (Litres)
```dax
Total Fuel Consumed (Litres) = 
SUM(fact_fleet_trip[fuel_consumed_litres])
```

### 5.3 Fleet Fuel Economy (km / Litre)
```dax
Fleet Fuel Efficiency = 
DIVIDE(
    [Total Fleet Mileage (km)],
    [Total Fuel Consumed (Litres)],
    0
)
```

### 5.4 Total Fleet Fuel Cost (USD)
```dax
Total Fleet Fuel Cost USD = 
SUM(fact_fuel_purchase[total_cost_usd])
```

### 5.5 Average Fleet Cost per Litre (USD)
```dax
Avg Fleet Cost per Litre = 
DIVIDE(
    [Total Fleet Fuel Cost USD],
    SUM(fact_fuel_purchase[litres_purchased]),
    0
)
```

---

## 6. Dynamic Rank & Formatting Helper Measures

### 6.1 Country Price Rank (Lowest to Highest)
```dax
Country Price Rank = 
IF(
    NOT ISBLANK([Latest Petrol Price USD]),
    RANKX(
        ALLSELECTED(dim_country[country_name]),
        [Latest Petrol Price USD],
        ,
        ASC,
        Dense
    ),
    BLANK()
)
```

### 6.2 Data Freshness Indicator
```dax
Days Since Last Observation = 
DATEDIFF(
    MAX(fuel_prices[observation_date]),
    TODAY(),
    DAY
)
```
