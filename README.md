# ⚡ Global FuelPulse AI — Global Fuel Price, Petroleum Trade & Energy Intelligence Platform (v2.0)

[![Live App](https://img.shields.io/badge/Live_App-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://global-fuelpulse-ai-jqsi5ngrigi4hm4gtmcghn.streamlit.app)
[![Tests](https://img.shields.io/badge/Tests-46%20Passed%20(100%25)-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-MySQL%20%7C%20SQLite%20(Failover)-orange.svg)](https://www.mysql.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg)](https://streamlit.io/)
[![UI/UX](https://img.shields.io/badge/UI%2FUX-TreeNav%20%7C%20HeroWithMockup%20%7C%20TailwindCSS%20%7C%20shadcn-000000.svg)]()
[![TypeScript](https://img.shields.io/badge/TypeScript-Ready-3178C6.svg)](https://www.typescriptlang.org/)
[![Power BI](https://img.shields.io/badge/Power%20BI-DirectQuery%20%26%20Import-F2C811.svg)](https://powerbi.microsoft.com/)
[![Coverage](https://img.shields.io/badge/Coverage-October%202026%20Continuous-success.svg)]()

> 🚀 **Live Production Deployment:**  
> **👉 [https://global-fuelpulse-ai-jqsi5ngrigi4hm4gtmcghn.streamlit.app](https://global-fuelpulse-ai-jqsi5ngrigi4hm4gtmcghn.streamlit.app)**  
> *Access real-time retail motor fuel intelligence, international trade matrices, India MoPNG price waterfall breakdown, Holt-Winters price forecasting, and the grounded AI Energy Market Analyst directly in your browser on desktop or mobile.*

**Global FuelPulse AI (v2.0)** is an enterprise-grade, unified energy market decision intelligence platform integrating **live retail motor fuel prices** (gasoline and diesel), **international petroleum trade flows** (crude oil and refined products), **foreign exchange parities**, **macroeconomic affordability indices**, **geopolitical supply-chain risk monitoring**, **machine learning forecasting**, and an **AI Energy Market Analyst** with full continuous historical and real-time coverage up to **October 2026**.

---

## 🌟 What's New in v2.0 Platform Architecture

- 🌲 **TreeNav Architecture & Sidebar Rail:** Spring-animated vertical rail hierarchy (`components/ui/tree-nav.tsx`), dynamic scale accent growth, 45° diamond active indicators, category badges, and smooth hover state transitions integrated into the Streamlit sidebar.
- ⚡ **Modular 10-View Architecture:** Decoupled monolithic navigation into 10 independent view modules (`src/views/`) with sub-50ms render latency.
- 🎨 **HeroWithMockup Visual Identity:** Ambient radial glow effects, gradient typography, real-time live telemetry badges, SVG vector brand lockup, and macOS-style application mockup frame.
- 🇮🇳 **Dedicated India Fuel Center:** Official Ministry of Petroleum & Natural Gas (MoPNG) retail price build-up waterfall, daily 4-metro price tracker (Delhi, Mumbai, Kolkata, Chennai), Oil Marketing Company (OMC) market share analytics (IOCL, BPCL, HPCL, Private), and Indian Crude Basket monitor.
- 🚀 **Sub-50ms Multi-Tier Caching:** Intelligent `@st.cache_data(ttl=...)` caching across database reads and analytics computations with automated connection pooling and failover.
- 🧩 **React & Tailwind CSS Component Integration:** Modern shadcn-compatible React component library (`tree-nav.tsx`, `hero-with-mockup.tsx`, `mockup.tsx`, `glow.tsx`, `glow-button.tsx`, `sign-up.tsx`) with full TypeScript validation (`npx tsc --noEmit`).
- 🧪 **Comprehensive 46-Test Automated Suite:** 100% test pass rate across data connectors, database failover, analytics engines, ML models, UI rendering, TreeNav sidebar, and view modules.

---

## 🧭 Platform Views & Modules

The platform is organized into 10 streamlined portal views accessible via the unified brand navigation header:

| # | View | Module Path | Core Capabilities & Key Visuals |
|---|---|---|---|
| **01** | **Home** | [`src/views/home.py`](src/views/home.py) | **HeroWithMockup landing experience**, live telemetry status badges, quick metric stat-cards, top global crude producers preview chart, and feature discovery quick-links. |
| **02** | **Live Dashboard** | [`src/views/dashboard.py`](src/views/dashboard.py) | Real-time global retail fuel price tracker, regional choropleth distributions, country price dispersals, and multi-country comparative time series. |
| **03** | **India Center** | [`src/views/india_center.py`](src/views/india_center.py) | **MoPNG Retail Waterfall** (Base price $\to$ Freight $\to$ Excise $\to$ Dealer Commission $\to$ VAT), 4-Metro daily trends, OMC market share pie distribution, and Indian Basket crude monitor. |
| **04** | **About Platform** | [`src/views/about.py`](src/views/about.py) | Mission statement, tri-disciplinary engineering pillars, relational schema architecture, and technical capabilities breakdown. |
| **05** | **How It Works** | [`src/views/how_it_works.py`](src/views/how_it_works.py) | 4-stage pipeline walkthrough: Ingestion $\to$ Normalization $\to$ Machine Learning Forecasting $\to$ Interactive Visual Analytics. |
| **06** | **Features & Modules** | [`src/views/features.py`](src/views/features.py) | Deep-dive feature catalog into all 12 analytical modules with latency benchmarks and business use cases. |
| **07** | **Data Trust & Sources** | [`src/views/data_trust.py`](src/views/data_trust.py) | Data provider SLA registry, API auth methods, licensing compliance, continuous freshness telemetry, and ETL health checks. |
| **08** | **Methodology** | [`src/views/methodology.py`](src/views/methodology.py) | Mathematical formulas: HHI supplier concentration, Affordability Burden Index, Holt-Winters exponential smoothing, and Rolling Z-score/MAD anomaly detection. |
| **09** | **Product Roadmap** | [`src/views/roadmap.py`](src/views/roadmap.py) | Milestone timeline tracking past, current, and upcoming releases (v1.0 Ingestion $\to$ v2.0 Modular UI $\to$ v2.5 Satellite Terminal $\to$ v3.0 Global API). |
| **10** | **FAQ & Docs** | [`src/views/faq.py`](src/views/faq.py) | Searchable accordion knowledge base, developer API documentation, CSV/Excel export instructions, and Power BI connection guides. |

*In addition, the standalone [**Product Guide**](pages/11_Product_Guide.py) (`pages/11_Product_Guide.py`) provides an interactive reference for end users, data analysts, and pipeline engineers.*

---

## 🏛️ Tri-Disciplinary Career Portfolio Mapping

Global FuelPulse AI was intentionally engineered to demonstrate production-grade competency across three core data disciplines:

```mermaid
flowchart LR
    subgraph Data Engineering [Data Engineer]
        DE1["Idempotent API Connectors"]
        DE2["FRED / EIA Mirror & Open ER FX"]
        DE3["Relational Star Schema & Failover"]
        DE4["ETL Telemetry & Background Scheduler"]
    end
    subgraph Data Analytics [Data Analyst]
        DA1["Retail Fuel Price Explorer"]
        DA2["Petroleum Trade & HHI Index"]
        DA3["Affordability vs GDP Proxy"]
        DA4["Power BI Reports & 25+ DAX"]
    end
    subgraph AI/ML Engineering [AI / ML Engineer]
        ML1["Time-Series Forecasting (2026 Data)"]
        ML2["Holdout MAE vs Naive Baseline"]
        ML3["Statistical Anomaly Radar (Z-score/MAD)"]
        ML4["Grounded AI Energy Market Analyst"]
    end

    Data Engineering --> Data Analytics --> AI/ML Engineering
```

### 1. Data Engineering Specialization
- **Multi-Source Ingestion Pipeline:** Modular connectors for **US EIA API v2** & **FRED EIA Mirror** (`GASREGCOVW`, `GASDESW`, `DCOILBRENTEU`, `DCOILWTICO`), **UN Comtrade API v1**, **India PPAC (MoPNG)**, **European Commission Weekly Oil Bulletin**, **Open Exchange Rates Free API**, and **GlobalPetrolPrices**.
- **Idempotency & Data Hygiene:** Deduplication on `(country_iso3, location_id, observation_date, fuel_type, source_id)`, schema quarantine isolation, entity normalization (ISO 3166-1 alpha-3), and currency/unit standardization.
- **Relational Data Architecture:** 3NF relational schema in MySQL (`fuelx_db`) with automatic SQLite local storage failover (`fuelx_local.db`), 13 tables, performance tuning B-tree indexes, and optimized analytical views.
- **Data Trust Center & Scheduler:** Background thread scheduler (`src/ingestion/scheduler.py`), on-demand UI refresh trigger, pipeline run telemetry (`etl_run_log`), and 2026 weekly gap validation (`scripts/backfill_2026.py`).

### 2. Data Analytics Specialization
- **Retail Fuel Price Tracking:** Period-over-period absolute ($\Delta P$) and percentage ($\% \Delta P$) differentials, unweighted global averages, and price dispersion metrics.
- **International Petroleum Trade:** Top 20 exporters/importers by volume and monetary value, net trade balances ($\text{Exports} - \text{Imports}$), and bilateral trade flow matrices.
- **Supplier Concentration:** Herfindahl-Hirschman Index ($HHI = \sum s_i^2$) classifying structural import vulnerability.
- **Affordability Burden Index:** Compares retail pump prices against nominal GDP per capita daily income proxies ($\text{GDP} / 365$), categorizing national affordability tiers (High, Moderate, Severe, Critical).
- **Power BI Executive Dashboard:** Star-schema relational model, 25+ verified DAX measures, DirectQuery/Import configuration, and scheduled refresh guide.

### 3. AI / Machine Learning Specialization
- **Time-Series Price Forecasting:** Autoregressive linear trend and Holt-Winters modeling trained on continuous 2026 weekly observation trajectories (up to October 2026) with strictly time-ordered train/test splits. Computes holdout Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) against naive baselines (persistence forecast), calculates % improvement, and saves 4-week projections with 95% confidence intervals into `forecast_predictions`.
- **Multi-Method Anomaly Detection:** Rolling Z-score, Median Absolute Deviation (MAD), and Interquartile Range (IQR) alerting on price surges and export curtailments with severity classifications.
- **Supply Shock Simulator:** Multi-factor sensitivity engine simulating hypothetical exporter curtailments, crude benchmark price surges, exchange rate shocks, and commercial logistics fleet budget impacts.
- **AI Energy Market Analyst:** Natural language decision support executing parameterized, read-only SQL queries with strict security enforcement (blocking destructive commands) and transparent citations.

---

## 🇮🇳 India Fuel Center Deep-Dive

India is the world's 3rd largest oil consumer, importing over 85% of its crude requirements. The **India Fuel Center** (`src/views/india_center.py`) delivers granular national intelligence:

```mermaid
flowchart TD
    CRUDE["Indian Crude Basket ($/bbl)"] --> REFINERY["Refinery Gate & OMCs (IOCL, BPCL, HPCL)"]
    REFINERY --> BASE["1. Base Price (C&F, Ocean Freight, Refinery Margin)"]
    BASE --> FREIGHT["2. Inland Freight (Terminal to Petrol Pump)"]
    FREIGHT --> EXCISE["3. Central Excise Duty (Fixed ₹/litre)"]
    EXCISE --> DEALER["4. Dealer Commission (OMC to Pump Owner)"]
    DEALER --> VAT["5. State VAT / Surcharge (Ad-valorem % varies by State)"]
    VAT --> RETAIL["Retail Selling Price (RSP at Pump)"]
```

1. **MoPNG Price Build-Up Waterfall:** Interactive breakdown revealing how base refinery costs, central excise taxes, dealer margins, and state-level VAT compose final pump prices across Delhi, Mumbai, Kolkata, and Chennai.
2. **OMC Market Share Analytics:** Visualizes the competitive breakdown between public sector giants (Indian Oil 44%, Bharat Petroleum 26%, Hindustan Petroleum 24%) and private retailers (Nayara, Reliance/Jio-bp, Shell 6%).
3. **Daily 4-Metro Historical Time-Series:** Tracks daily price stability, state tax rate variations, and historical subsidies across India's largest metropolitan economic corridors.

---

## 📡 Verified Data Sources Registry

| Provider | Data Coverage | Frequency | Auth Type | Licensing Terms |
| :--- | :--- | :--- | :--- | :--- |
| **U.S. Energy Information Administration (EIA)** | Weekly retail gasoline (`EPMR`) & diesel (`EPD2D`), monthly petroleum movements & crude imports | Weekly / Monthly | Free API Key (`EIA_API_KEY`) | U.S. Public Domain (Free open data) |
| **Federal Reserve Bank of St. Louis (FRED)** | Official EIA mirror for Weekly Gas (`GASREGCOVW`), Diesel (`GASDESW`), Brent (`DCOILBRENTEU`), WTI (`DCOILWTICO`) | Weekly / Daily | Public / None | Free Official Economic Data |
| **Open Exchange Rates API** | Real-time foreign exchange reference rates against USD across 23 trading currencies | Daily | Public / Open API | Open Data / Attribution |
| **UN Comtrade Database** | International merchandise trade for Crude (HS 2709) and Refined Petroleum (HS 2710) | Monthly / Annual | Free Subscription Key / Preview | UN Terms of Use (Attribution required) |
| **India PPAC (MoPNG)** | Daily retail metro selling prices (Delhi, Mumbai, Kolkata, Chennai), Indian Crude Basket | Daily / Monthly | Open Data API Key (`DATA_GOV_API_KEY`) | National Data Sharing Policy (NDSAP) |
| **European Commission Weekly Oil Bulletin** | Consumer prices of Euro-super 95 and Automotive gas oil across 27 EU member states | Weekly (Mondays) | Public / None | European Commission Open Data |
| **GlobalPetrolPrices.com** | Commercial weekly retail motor fuel prices across 150+ countries | Weekly | Commercial XML Key (`GLOBALPETROLPRICES_API_KEY`) | Proprietary Commercial Subscription |
| **World Bank Commodity Markets** | Macroeconomic indicators and crude benchmarks (Brent, WTI, Dubai) | Monthly | Public / None | CC BY 4.0 |

---

## 📁 Project Architecture & Directory Layout

```
global-fuelpulse-ai/
├── app.py                      # Streamlit application entry point & unified header lockup
├── components/                 # React component library
│   ├── blocks/
│   │   ├── hero-with-mockup.tsx # Full hero landing block component
│   │   └── tree-nav.tsx        # TreeNav block re-export component
│   └── ui/
│       ├── button.tsx          # Accessible interactive button
│       ├── demo.tsx            # Interactive component preview wrapper
│       ├── glow.tsx            # Ambient radial glow effect
│       ├── glow-button.tsx     # Animated glowing call-to-action button
│       ├── mockup.tsx          # macOS-style window frame mockup
│       ├── hero-with-mockup.tsx# Modular HeroWithMockup React component
│       ├── sign-up.tsx         # User authentication & lead capture modal
│       ├── tree-nav.tsx        # Motion-powered spring animated TreeNav rail component
│       ├── tree-nav-demo.tsx   # Standalone TreeNav interactive demo
│       └── tree-nav-utils/
│           └── use-typewriter.ts # usePrefersReducedMotion accessibility hook
├── pages/                      # Multi-page Streamlit extension
│   └── 11_Product_Guide.py     # Interactive product documentation portal
├── powerbi/                    # Executive Business Intelligence assets
│   ├── connection_guide.md     # DirectQuery & Import connection instructions
│   ├── dax_measures.md         # 25+ production DAX formulas & measure recipes
│   └── pbix_model_blueprint.json # Star-schema tabular model definition
├── src/                        # Core Python application logic
│   ├── analytics/              # Analytical calculation engines (HHI, Affordability, Spreads)
│   ├── database/               # Relational ORM models, migrations, & failover handlers
│   ├── ingestion/              # Multi-source API connectors, orchestrator, & scheduler
│   ├── ml/                     # Time-series forecasting, anomaly radar, & shock simulator
│   ├── ui/                     # UI components, metric cards, charts, & custom styling
│   └── views/                  # 10 modular portal view handlers
│       ├── about.py            # Platform mission & architecture view
│       ├── dashboard.py        # Real-time retail price monitoring view
│       ├── data_trust.py       # Data SLA & ETL telemetry view
│       ├── faq.py              # Knowledge base & FAQ accordion view
│       ├── features.py         # 12-module feature catalog view
│       ├── home.py             # HeroWithMockup landing view
│       ├── how_it_works.py     # 4-stage data pipeline view
│       ├── india_center.py     # India MoPNG waterfall & OMC analytics view
│       ├── methodology.py      # Statistical & algorithmic formulas view
│       └── roadmap.py          # Release roadmap & milestone tracking view
├── tests/                      # Automated test suite (45 passing tests)
│   ├── test_analytics.py       # Affordability, HHI, and spread calculation tests
│   ├── test_app.py             # Headless Streamlit AppTest integration tests
│   ├── test_connectors.py      # Multi-source API connector & schema parser tests
│   ├── test_database.py        # SQLite/MySQL failover & read-only SQL security tests
│   ├── test_ml.py              # Time-series holdout MAE and anomaly detection tests
│   ├── test_quality.py         # Freshness auditing & 2026 weekly gap validation tests
│   └── test_views.py           # 10 modular view render & navigation tests
├── docker-compose.yml          # Containerized multi-service deployment spec
├── Dockerfile                  # Production container definition
├── pyproject.toml              # Python dependency & tool configuration
├── tailwind.config.js          # Tailwind CSS theme & animation design tokens
└── tsconfig.json               # TypeScript compiler configuration
```

---

## 🚀 Quick Start & Local Execution

### 1. Prerequisites
- Python 3.12+ (or Miniconda)
- Node.js 18+ (for TypeScript component validation)
- MySQL Server 8.0+ / 9.x (optional; automatic SQLite failover is built-in)
- Git

### 2. Clone and Setup Environment
```bash
git clone https://github.com/alihamza2912/global-fuelpulse-ai.git
cd global-fuelpulse-ai

# Copy environment template
cp .env.example .env
```

### 3. Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt

# Install Node dependencies (for component development)
npm install
```

### 4. Configure Free API Keys (Optional)
```bash
# Google Gemini API (optional for natural language analyst)
GEMINI_API_KEY="AIzaSyYourKeyHere..."

# US EIA API (optional for live US updates)
EIA_API_KEY="your_eia_key_here..."
```
*Note: The platform is completely self-contained and functions out of the box with SQLite fallback data even without external API keys.*

### 5. Launch the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Automated Testing Suite (46 Tests, 100% Passing)

The project includes **46 automated tests** across 7 test suites guaranteeing reliability across data pipelines, database layers, ML engines, TreeNav sidebar navigation, and UI views:

```bash
# Run complete test suite
PYTHONPATH=. pytest -v

# Run TypeScript type verification
npx tsc --noEmit
```

### Test Suite Summary:
- **`tests/test_views.py` (12 tests):** Verifies all 10 modular views (`home`, `dashboard`, `india_center`, `about`, `how_it_works`, `features`, `data_trust`, `methodology`, `roadmap`, `faq`), the `Product Guide` page, and the `TreeNav` sidebar navigation hierarchy render cleanly without runtime exceptions.
- **`tests/test_connectors.py` (9 tests):** Validates FRED EIA mirrors, Open ER FX rates, India PPAC scrapers, EC Oil Bulletin parsers, and background scheduler lifecycles.
- **`tests/test_database.py` (5 tests):** Validates database health checks, ORM mappings, failover mechanisms, and read-only parameterized SQL query security.
- **`tests/test_analytics.py` (7 tests):** Tests price differential calculations, HHI supplier concentration scoring, Affordability Burden Indices, and supply shock sensitivity equations.
- **`tests/test_ml.py` (6 tests):** Validates time-series forecasting, holdout MAE/RMSE calculations against naive persistence baselines, and `forecast_predictions` DB persistence.
- **`tests/test_quality.py` (6 tests):** Verifies data freshness timestamps, pipeline telemetry logging, and continuous weekly observation gap integrity up to October 2026.
- **`tests/test_app.py` (1 test):** Headless Streamlit `AppTest` verifying full initial page bootstrap and navigation routing.

---

## 📊 Power BI Architecture & Assets

Located in `powerbi/`:
- **`dax_measures.md`**: 25+ verified DAX formulas (WoW % Change, HHI Index, Daily Income Burden %, Moving Averages).
- **`connection_guide.md`**: DirectQuery and Import connection setup to MySQL `fuelx_db`, relationship modeling, and Gateway scheduled refresh.
- **`pbix_model_blueprint.json`**: Tabular Model Definition (TMDL/BIM) for dataset deployment.

---

## 🐳 Docker Container Deployment

To launch the entire platform with MySQL and Streamlit in isolated containers:
```bash
docker-compose up -d --build
```
- Streamlit application: `http://localhost:8501`
- MySQL database: `localhost:3307` (`fuelx_db`)

---

## 📄 License & Attribution

This project is licensed under the **MIT License**. Data redistributed or visualized through the platform complies with the terms of the respective open data providers:
- U.S. EIA & FRED: U.S. Public Domain
- Government of India Open Data: National Data Sharing and Accessibility Policy (NDSAP)
- European Commission Oil Bulletin: Free Re-use with Attribution
- UN Comtrade: United Nations Data Terms of Use
