"""
Comprehensive Test Suite for Global FuelPulse AI Modular Views and Navigation.
Verifies that all 10 product sections, navigation states, and page guides render cleanly without exception.
"""

import pytest
from streamlit.testing.v1 import AppTest


def test_product_guide_page_renders_without_exceptions():
    """Verifies that pages/11_Product_Guide.py runs headlessly without exceptions."""
    at = AppTest.from_file("pages/11_Product_Guide.py", default_timeout=30)
    at.run()
    assert len(at.exception) == 0, f"Product Guide raised exceptions: {at.exception}"


def test_app_home_view_renders_cleanly():
    """Verifies that default app.py landing page loads and displays key product elements."""
    at = AppTest.from_file("app.py", default_timeout=30)
    at.run()
    assert len(at.exception) == 0, f"App execution raised exceptions: {at.exception}"


def test_app_dashboard_navigation_renders_cleanly():
    """Verifies that app.py with ?tab=dashboard renders the 11-chapter dashboard."""
    at = AppTest.from_file("app.py", default_timeout=30)
    at.query_params["tab"] = "dashboard"
    at.run()
    assert len(at.exception) == 0, f"Dashboard view raised exceptions: {at.exception}"


def test_app_india_center_navigation_renders_cleanly():
    """Verifies that app.py with ?tab=india renders India Fuel Center."""
    at = AppTest.from_file("app.py", default_timeout=30)
    at.query_params["tab"] = "india"
    at.run()
    assert len(at.exception) == 0, f"India Center view raised exceptions: {at.exception}"


def test_app_data_trust_navigation_renders_cleanly():
    """Verifies that app.py with ?tab=trust renders Data Trust Center."""
    at = AppTest.from_file("app.py", default_timeout=30)
    at.query_params["tab"] = "trust"
    at.run()
    assert len(at.exception) == 0, f"Data Trust view raised exceptions: {at.exception}"


def test_app_methodology_navigation_renders_cleanly():
    """Verifies that app.py with ?tab=methodology renders Methodology & Formulas."""
    at = AppTest.from_file("app.py", default_timeout=30)
    at.query_params["tab"] = "methodology"
    at.run()
    assert len(at.exception) == 0, f"Methodology view raised exceptions: {at.exception}"


def test_app_tree_nav_sidebar_renders_cleanly():
    """Verifies that the TreeNav sidebar with connected rail and diamond indicators renders cleanly."""
    at = AppTest.from_file("app.py", default_timeout=30)
    at.run()
    assert len(at.exception) == 0, f"App TreeNav sidebar raised exceptions: {at.exception}"
    # Verify Tree Nav component rendered in sidebar and live refresh button exists
    assert any("Tree Nav" in str(m.value) for m in at.sidebar.markdown), "Tree Nav component not found in sidebar"
    assert any("Refresh Live Data" in b.label for b in at.sidebar.button), "Live refresh button not found in sidebar"


def test_home_platform_suite_buttons_navigate_correctly():
    """Verifies that clicking 'Open Dashboard →' navigates cleanly to the Intelligence Dashboard."""
    at = AppTest.from_file("app.py", default_timeout=30)
    at.run()
    assert at.session_state["active_nav"] == "🏠 Overview"

    dash_btns = [b for b in at.button if "Open Dashboard" in b.label]
    assert len(dash_btns) > 0, "Open Dashboard button not found on home view"
    dash_btns[0].click().run()

    assert at.session_state["active_nav"] == "⚡ Intelligence Dashboard"
    assert at.query_params.get("tab") == "dashboard" or at.query_params.get("tab") == ["dashboard"]
    assert len(at.exception) == 0, f"Dashboard navigation raised exception: {at.exception}"


def test_dashboard_search_prayagraj_and_global_tax():
    """Verifies that searching for 'prayagraj' and 'california' in the dashboard renders without exceptions."""
    at = AppTest.from_file("app.py", default_timeout=35)
    at.query_params["tab"] = "dashboard"
    at.run()
    assert len(at.exception) == 0, f"Dashboard initial load exception: {at.exception}"

    # Search for prayagraj
    search_inputs = [ti for ti in at.text_input if ti.key == "fast_universal_search_input"]
    assert len(search_inputs) > 0, "fast_universal_search_input not found"
    search_inputs[0].input("prayagraj").run()
    assert len(at.exception) == 0, f"Prayagraj search raised exception: {at.exception}"

    # Search for california
    search_inputs = [ti for ti in at.text_input if ti.key == "fast_universal_search_input"]
    assert len(search_inputs) > 0
    search_inputs[0].input("california").run()
    assert len(at.exception) == 0, f"California search raised exception: {at.exception}"


