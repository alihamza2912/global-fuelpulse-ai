import pytest
from src.ui_components import (
    render_app_header_brand_html,
    get_logo_mark_svg,
    get_brand_logo_svg,
    get_news_globe_icon_svg,
    get_lucide_icon_svg,
    apply_theme
)

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


def test_brand_logo_and_news_globe_svg():
    """Verifies brand vector marks and News globe SVG generation."""
    mark = get_logo_mark_svg(36)
    assert "<svg" in mark
    assert "viewBox=\"0 0 36 36\"" in mark
    assert "gfp_drop_grad" in mark

    brand = get_brand_logo_svg(340, 54, "en")
    assert "GLOBAL FUELPULSE" in brand
    assert "AI" in brand

    globe = get_news_globe_icon_svg(24, "en")
    assert "NEWS" in globe
    assert "<circle" in globe


def test_lucide_icon_system():
    """Verifies pure-SVG Lucide vector icons render correctly."""
    icons_to_test = ["database", "activity", "bot", "fuel", "languages", "newspaper", "sparkles"]
    for icon_name in icons_to_test:
        svg = get_lucide_icon_svg(icon_name, size=20, color="#F5B942")
        assert "<svg" in svg
        assert "viewBox=\"0 0 24 24\"" in svg
        assert "stroke=\"#F5B942\"" in svg


def test_apply_theme_runs_safely():
    """Verifies that apply_theme executes without exception in standalone environment."""
    apply_theme()

