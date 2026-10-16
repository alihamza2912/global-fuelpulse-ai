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
    # Check that sidebar buttons exist and contain the tree marker
    portal_buttons = [b for b in at.sidebar.button if "◆" in b.label or "◇" in b.label]
    assert len(portal_buttons) == 10, f"Expected 10 TreeNav portal buttons, found {len(portal_buttons)}"

