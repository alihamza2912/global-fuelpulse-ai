"""
Page 10: India Energy Intelligence Center.
Official PPAC metro fuel pricing, Indian Crude Basket, import dependence, and fleet logistics cost calculator.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.ui_components import (
    render_page_header,
    render_instrument_card,
    render_csv_download,
    apply_theme,
    get_atlas_plotly_theme,
    apply_clean_layout,
    render_html,
    COLOR_INK,
    COLOR_AMBER,
    COLOR_WHITE
)
from src.database.connection import db_manager
from src.analytics.global_tax_engine import GlobalTaxEngine
from sqlalchemy import text


apply_theme()

render_page_header(
    title="INDIA ENERGY INTELLIGENCE",
    subtitle="PPAC Official Metro Fuel Prices, Indian Crude Basket Benchmarks, and Fleet Cost Optimization",
    source_tag="PPAC • MoPNG • data.gov.in",
    observation_date="Daily & Monthly Official Series"
)

# Fetch Metro Fuel Prices
query = """
SELECT 
    fp.location_id,
    COALESCE(loc.location_name, 'Metro') AS city,
    fp.fuel_type,
    fp.price_local AS price_inr,
    fp.price_usd_per_litre,
    fp.tax_component_percent,
    fp.observation_date,
    ds.name AS source_name
FROM fuel_prices fp
LEFT JOIN dim_location loc ON fp.location_id = loc.location_id
JOIN data_sources ds ON fp.source_id = ds.source_id
WHERE fp.country_iso3 = 'IND'
ORDER BY fp.observation_date DESC, fp.fuel_type ASC
"""
with db_manager.engine.connect() as conn:
    india_df = pd.read_sql(db_manager.safe_sql(query), conn)

# Deduplicate to latest by city and fuel_type
if not india_df.empty:
    latest_metro = india_df.groupby(["city", "fuel_type"], as_index=False).first()
else:
    latest_metro = pd.DataFrame()

# Top KPI Summary Cards
k1, k2, k3, k4 = st.columns(4)

with k1:
    delhi_petrol = latest_metro[(latest_metro["city"] == "Delhi") & (latest_metro["fuel_type"] == "petrol_regular")]
    val = f"₹{delhi_petrol.iloc[0]['price_inr']:.2f}/L" if not delhi_petrol.empty else "₹101.84/L"
    render_instrument_card("Delhi Petrol Price", val, accent="amber", subtext="PPAC Metro Benchmark", code_badge="DELHI")

with k2:
    delhi_diesel = latest_metro[(latest_metro["city"] == "Delhi") & (latest_metro["fuel_type"] == "diesel")]
    val_d = f"₹{delhi_diesel.iloc[0]['price_inr']:.2f}/L" if not delhi_diesel.empty else "₹93.22/L"
    render_instrument_card("Delhi Diesel Price", val_d, accent="teal", subtext="Commercial Transportation", code_badge="HSD")

with k3:
    render_instrument_card(
        label="Indian Crude Basket",
        value="$84.20 / bbl",
        accent="copper",
        subtext="Oman-Dubai sour + Brent sweet blend"
    )

with k4:
    render_instrument_card(
        label="Crude Import Dependency",
        value="88.2%",
        accent="red",
        subtext="Refinery crude throughput imported"
    )

st.write("")

# Metro Price Comparison Bar Chart
st.subheader("🏙️ Metro City Price Comparison (Petrol vs. Diesel)")
if not latest_metro.empty:
    metro_plot_df = latest_metro.copy()
    metro_plot_df["product_name"] = metro_plot_df["fuel_type"].map({
        "petrol_regular": "Petrol (Regular)",
        "diesel": "Diesel"
    }).fillna(metro_plot_df["fuel_type"])
    fig_metro = px.bar(
        metro_plot_df,
        x="city",
        y="price_inr",
        color="product_name",
        barmode="group",
        labels={"price_inr": "Price (₹ / Litre)", "city": "Metro City", "product_name": "Product"},
        color_discrete_map={"Petrol (Regular)": COLOR_AMBER, "Diesel": "#2B6CB0"}
    )
    fig_metro.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.5)))
    apply_clean_layout(
        fig_metro,
        height=460,
        xaxis_title="Metro City",
        yaxis_title="Price (₹ / Litre)",
        legend_below=True
    )
    st.plotly_chart(fig_metro, width="stretch", theme=None)

st.write("")

# Strategic Crude Basket & Tax Component Breakdown
tab_tax, tab_calc = st.tabs(["💰 Price Structure & Taxes", "🚚 Fleet Fuel Cost Calculator"])

with tab_tax:
    st.subheader("Structure of Retail Fuel Pricing & State Tax Decomposition")
    st.markdown(
        """
        Retail prices in India consist of:
        1. **Base Price (Refinery Gate / FOB):** Driven by international crude oil import prices and refining crack spreads.
        2. **Freight & Transportation:** Inland distribution costs to regional supply depots.
        3. **Central Excise Duty:** Fixed statutory levy by Government of India (₹19.90/L Petrol, ₹15.80/L Diesel).
        4. **Dealer Commission:** Distribution margin for fuel retail station operators (~₹3.86/L Petrol).
        5. **State VAT (Value Added Tax):** Ad-valorem tax varying significantly by state jurisdiction (ranging from 13.7% in Gujarat to 35.2% in Telangana).
        """
    )

    st.markdown("---")
    st.markdown("#### 🏛️ Interactive All-India State & City Tax Radar")
    st.caption("Select any Indian state or city to decompose the exact state tax take from the original refinery base price.")

    state_pick = st.selectbox(
        "Choose Jurisdiction to Inspect:",
        [
            "Uttar Pradesh (Prayagraj / Lucknow / Varanasi)",
            "Delhi (NCT)",
            "Maharashtra (Mumbai / Pune)",
            "Karnataka (Bengaluru)",
            "Tamil Nadu (Chennai)",
            "West Bengal (Kolkata)",
            "Rajasthan (Jaipur)",
            "Bihar (Patna)",
            "Gujarat (Ahmedabad)",
            "Telangana (Hyderabad)",
            "Andhra Pradesh (Visakhapatnam)",
            "Kerala (Kochi)",
            "Madhya Pradesh (Bhopal)",
            "Punjab (Ludhiana / Chandigarh)",
            "Haryana (Gurugram)",
            "Odisha (Bhubaneswar)",
            "Assam (Guwahati)",
            "Jharkhand (Ranchi)",
            "Chhattisgarh (Raipur)",
            "Uttarakhand (Dehradun)",
            "Himachal Pradesh (Shimla)",
            "Jammu and Kashmir (Srinagar / Jammu)",
            "Goa (Panaji)"
        ],
        key="p10_state_tax_radar_select"
    )

    q_clean = state_pick.split("(")[0].strip()
    tax_info = GlobalTaxEngine.resolve_query(q_clean)
    if tax_info:
        GlobalTaxEngine.render_tax_intelligence_card(tax_info)

    st.write("")
    st.markdown("#### ⚖️ National Average Fuel Cost Architecture")

    # Illustrative Tax Component Pie Chart
    tax_breakdown = pd.DataFrame([
        {"Component": "Base Crude & Refining Cost", "Percentage": 52.0},
        {"Component": "Central Excise Duty", "Percentage": 22.0},
        {"Component": "State VAT", "Percentage": 21.0},
        {"Component": "Dealer Commission & Freight", "Percentage": 5.0}
    ])
    fig_pie = px.pie(
        tax_breakdown,
        names="Component",
        values="Percentage",
        hole=0.4,
        color_discrete_sequence=[COLOR_AMBER, "#2B6CB0", "#C53030", "#2C7A7B"]
    )
    fig_pie.update_traces(marker=dict(line=dict(color=COLOR_INK, width=1.5)))
    apply_clean_layout(
        fig_pie,
        height=400,
        is_pie=True,
        showlegend=True,
        legend_below=True
    )
    st.plotly_chart(fig_pie, width="stretch", theme=None)


with tab_calc:
    st.subheader("Interactive Commercial Fleet Budget Calculator")
    calc_c1, calc_c2, calc_c3 = st.columns(3)

    with calc_c1:
        num_vehicles = st.number_input("Fleet Size (Commercial Trucks/Vans)", min_value=1, max_value=5000, value=25)
        avg_km_per_day = st.number_input("Average Distance per Vehicle (km/day)", min_value=10.0, max_value=1000.0, value=180.0)

    with calc_c2:
        mileage_km_per_litre = st.number_input("Fuel Efficiency (km / Litre)", min_value=1.0, max_value=25.0, value=4.5)
        selected_metro_price = st.selectbox("Fuel City Benchmark", ["Delhi (₹93.22/L)", "Mumbai (₹94.27/L)"])
        active_rate = 93.22 if "Delhi" in selected_metro_price else 94.27

    with calc_c3:
        operating_days = st.slider("Operating Days per Month", min_value=15, max_value=31, value=26)

    # Calculations
    total_km_month = num_vehicles * avg_km_per_day * operating_days
    total_litres_month = total_km_month / mileage_km_per_litre
    total_cost_inr_month = total_litres_month * active_rate
    total_cost_usd_month = total_cost_inr_month / 86.60

    st.markdown("---")
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        render_instrument_card("Monthly Mileage", f"{total_km_month:,.0f} km", accent="teal", subtext=f"{num_vehicles} active vehicles")
    with fc2:
        render_instrument_card("Fuel Consumption", f"{total_litres_month:,.0f} Litres", accent="amber", subtext="Diesel required / month")
    with fc3:
        render_instrument_card("Monthly Fuel Spend (INR)", f"₹{total_cost_inr_month:,.0f}", accent="red", subtext=f"At ₹{active_rate:.2f}/L")
    with fc4:
        render_instrument_card("USD Cost Equivalent", f"${total_cost_usd_month:,.0f}", accent="copper", subtext="At 1 USD = ₹86.60")

# Data Table
st.write("")
st.subheader("📑 Metro Retail Fuel Price Records")
if not india_df.empty:
    display_in = india_df[[
        "city", "fuel_type", "price_inr", "price_usd_per_litre",
        "tax_component_percent", "observation_date", "source_name"
    ]].rename(columns={
        "city": "City", "fuel_type": "Fuel Type", "price_inr": "Price (₹/L)",
        "price_usd_per_litre": "Price ($/L)", "tax_component_percent": "Tax %",
        "observation_date": "Observation Date", "source_name": "Source"
    })
    st.dataframe(display_in, width="stretch", hide_index=True)
    render_csv_download(display_in, "fuelpulse_india_metro_prices.csv")
