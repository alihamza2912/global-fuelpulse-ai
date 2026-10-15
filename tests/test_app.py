"""
End-to-End Headless AppTest for Streamlit Global FuelPulse AI.
Verifies that app.py loads, connects to database marts, renders charts, and executes without runtime errors.
"""

import pytest
from streamlit.testing.v1 import AppTest


def test_streamlit_app_renders_without_exceptions():
    """Runs app.py headlessly and verifies zero exceptions occurred during render."""
    at = AppTest.from_file("app.py", default_timeout=30)
    at.run()
    assert len(at.exception) == 0, f"App execution raised exceptions: {at.exception}"


def test_ai_analyst_page_renders_without_exceptions():
    """Runs pages/9_AI_Analyst.py headlessly and verifies zero exceptions occurred."""
    at = AppTest.from_file("pages/9_AI_Analyst.py", default_timeout=30)
    at.run()
    assert len(at.exception) == 0, f"AI Analyst page execution raised exceptions: {at.exception}"

