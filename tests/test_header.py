import pytest
from src.ui_components import render_app_header_brand_html

def test_app_header_brand_html_structure():
    """Verifies that the brand title, AI badge, subtitle, and status indicators are strictly separated."""
    html = render_app_header_brand_html("en", "SQLITE VERIFIED", "LIVE 2026")
    
    # Check Brand Name prominence
    assert "GLOBAL FUELPULSE" in html
    assert "fuelpulse-brand-title" in html
    
    # Check Yellow AI Badge
    assert "fuelpulse-brand-ai-badge" in html
    assert "AI" in html
    
    # Check Subtitle
    assert "fuelpulse-brand-sub" in html
    
    # Check Vertical Divider separating Brand and Status Indicators
    assert "fuelpulse-header-v-divider" in html
    
    # Check Dedicated Status Cluster and Pills
    assert "fuelpulse-header-status-cluster" in html
    assert "fuelpulse-status-emerald" in html
    assert "SQLITE VERIFIED" in html
    assert "fuelpulse-status-amber" in html
    assert "LIVE 2026" in html
    
    # Ensure status indicators are not embedded inside subtitle row
    sub_row_idx = html.find("fuelpulse-header-sub-row")
    v_div_idx = html.find("fuelpulse-header-v-divider")
    status_idx = html.find("fuelpulse-header-status-cluster")
    
    assert sub_row_idx < v_div_idx < status_idx, "Layout order must be Sub-row -> Divider -> Status Cluster"
