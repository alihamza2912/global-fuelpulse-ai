"""
GLOBAL FUELPULSE AI — EDITORIAL DESIGN SYSTEM & UI COMPONENTS
Premium Editorial Industrial Intelligence & Neo-Brutalist Layout Language.
Distinctive visual identity: Warm Cream (#FFF9E8), Crisp White (#FFFFFF),
Sharp Black Ink (#111111), Petroleum Amber (#F5B942), and Offset Black Shadows.
"""

import streamlit as st
import pandas as pd
import textwrap
from typing import Optional, Dict, Any, List
from datetime import datetime
from config.settings import settings
from src.database.connection import db_manager
from src.utils.chart_style import apply_clean_layout, clean_product_label

# ==============================================================================
# 1. COLOR PALETTE CONSTANTS (PREPZII EDITORIAL DIRECTION)
# ==============================================================================
COLOR_CREAM = "#FFF9E8"          # Warm cream global canvas
COLOR_WHITE = "#FFFFFF"          # Crisp white surfaces
COLOR_INK = "#111111"            # Solid black ink typography & outlines
COLOR_AMBER = "#F5B942"          # Petroleum amber-yellow accent
COLOR_GREEN_LIGHT = "#D9F4D8"    # Soft green (subsidized / positive delta)
COLOR_BLUE_LIGHT = "#DFEBFA"     # Soft blue (trade & seaborne flows)
COLOR_ROSE_LIGHT = "#F7E1E6"     # Soft rose (high fiscal burden / risk alert)
COLOR_GRAY_MUTED = "#222222"     # High-contrast secondary text (pure dark)
COLOR_BORDER_LIGHT = "#D9D4C8"   # Subtle hairline borders

# Backward-compatible aliases for legacy modules
COLOR_GRAPHITE = COLOR_CREAM
COLOR_OBSIDIAN = COLOR_WHITE
COLOR_SURFACE_ALT = COLOR_WHITE
COLOR_BORDER = COLOR_INK
COLOR_TEXT_PRIMARY = COLOR_INK
COLOR_TEXT_MUTED = COLOR_GRAY_MUTED
COLOR_TEXT_FAINT = "#333333"
COLOR_COPPER = "#C05621"
COLOR_TEAL = "#2C7A7B"
COLOR_RED = "#C53030"

# High-contrast editorial Plotly colorway
EDITORIAL_COLORWAY = [COLOR_AMBER, COLOR_INK, "#2B6CB0", "#C05621", "#2C7A7B", "#C53030"]
ATLAS_COLORWAY = EDITORIAL_COLORWAY


# ==============================================================================
# 2. HTML CLEANING HELPER (PREVENTS MARKDOWN CODE-BLOCK LEAKAGE)
# ==============================================================================
def clean_html(html_str: str) -> str:
    """Removes all leading indentation and empty lines from HTML strings so Markdown never interprets them as code blocks."""
    if not html_str:
        return ""
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    return "\n".join(lines)


def render_html(html_str: str, container=None):
    """Safely renders HTML into Streamlit without raw code block leakage."""
    target = container or st
    target.markdown(clean_html(html_str), unsafe_allow_html=True)



# ==============================================================================
# 3. BRAND LOGO (CLEAN EDITORIAL SVG EMBED)
# ==============================================================================
def get_brand_logo_svg(width: int = 280, height: int = 50) -> str:
    """Returns the custom editorial Global FuelPulse AI emblem and typography."""
    return f"""<svg width="{width}" height="{height}" viewBox="0 0 320 54" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="6" y="6" width="42" height="42" rx="4" fill="#111111"/>
<rect x="3" y="3" width="42" height="42" rx="4" fill="#F5B942" stroke="#111111" stroke-width="2.5"/>
<circle cx="24" cy="24" r="11" fill="#111111"/>
<circle cx="24" cy="24" r="5.5" fill="#FFF9E8"/>
<path d="M24 13 L24 18 M24 30 L24 35 M13 24 L18 24 M30 24 L35 24" stroke="#F5B942" stroke-width="2.5" stroke-linecap="round"/>
<text x="56" y="24" fill="#111111" font-family="'Space Grotesk', -apple-system, sans-serif" font-weight="800" font-size="16" letter-spacing="0.06em">GLOBAL FUELPULSE AI</text>
<text x="56" y="41" fill="#111111" font-family="'Space Grotesk', -apple-system, sans-serif" font-weight="600" font-size="12" letter-spacing="0.02em">Understand the world's energy flows.</text>
</svg>"""


def get_fuel_client_logo_html() -> str:
    """Returns a client-facing small fuel logo badge with an industrial fuel pump and energy flame."""
    return """
    <div style="
        display: inline-flex;
        align-items: center;
        gap: 9px;
        background: #FFFFFF;
        border: 1.5px solid #111111;
        box-shadow: 2px 2px 0px #111111;
        padding: 5px 12px;
        border-radius: 9999px;
        margin-bottom: 12px;
        width: fit-content;
        position: relative;
        z-index: 5;
    ">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#111111" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 22V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v17"/>
            <path d="M15 10h2a2 2 0 0 1 2 2v2a2 2 0 0 0 2 2 2 2 0 0 0 2-2V9.83a2 2 0 0 0-.59-1.42L19.4 5.4"/>
            <path d="M3 22h12"/>
            <path d="M7 9h4"/>
            <circle cx="9" cy="6" r="1.3" fill="#F5B942"/>
        </svg>
        <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; color: #111111; text-transform: uppercase;">
            FUELPULSE AI <span style="background: #F5B942; color: #111111; padding: 1px 7px; border-radius: 3px; font-weight: 800; border: 1px solid #111111; margin-left: 4px;">CLIENT PORTAL</span>
        </span>
    </div>
    """


def get_animated_grid_css(container_class: str = "fuelpulse-hero-backdrop") -> str:
    """Generates layered, CSS-only animated grid backdrop styles matching animated-grid.tsx."""
    return f"""
<style>
@keyframes fp-grid-drift {{
  from {{ background-position: 0 0, 0 0; }}
  to   {{ background-position: 144px 144px, 144px 144px; }}
}}
@keyframes fp-grid-pulse {{
  0%, 100% {{ transform: scale(1); opacity: 0.7; }}
  50%      {{ transform: scale(1.12); opacity: 1; }}
}}
.{container_class} {{
  position: relative !important;
  overflow: hidden !important;
}}
.{container_class}::before,
.{container_class}::after {{
  content: "";
  position: absolute;
  inset: -144px;
  pointer-events: none;
}}
.{container_class}::before {{
  background-image:
    linear-gradient(to right, #dce4ef 1px, transparent 1px),
    linear-gradient(to bottom, #dce4ef 1px, transparent 1px);
  background-size: 36px 36px;
  opacity: 0.45;
  animation: fp-grid-drift 26s linear infinite;
  will-change: background-position;
}}
.{container_class}::after {{
  background-image:
    linear-gradient(to right, rgba(245, 185, 66, 0.55) 1.2px, transparent 1.2px),
    linear-gradient(to bottom, rgba(245, 185, 66, 0.55) 1.2px, transparent 1.2px);
  background-size: 144px 144px;
  opacity: 0.38;
  animation: fp-grid-drift 26s linear infinite;
  will-change: background-position;
}}
.{container_class}-glow {{
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: radial-gradient(45% 45% at 50% 42%, rgba(245, 185, 66, 0.22), transparent 70%);
  animation: fp-grid-pulse 9s ease-in-out infinite;
  will-change: transform, opacity;
}}
@media (prefers-reduced-motion: reduce) {{
  .{container_class}::before, .{container_class}::after, .{container_class}-glow {{
    animation: none !important;
  }}
}}
</style>
"""



# ==============================================================================
# 4. EDITORIAL THEME INJECTOR
# ==============================================================================
def apply_theme():
    """Injects high-contrast editorial CSS: warm cream canvas, black ink, offset shadows, and complete BaseWeb portal light styling."""
    custom_css = f"""<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700&family=Space+Grotesk:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

/* 1. Global page canvas */
.stApp {{
background-color: {COLOR_CREAM} !important;
color: {COLOR_INK} !important;
font-family: 'Space Grotesk', 'Inter', -apple-system, sans-serif;
}}

/* 2. Global typography scale */
h1 {{
font-family: 'Space Grotesk', -apple-system, sans-serif !important;
font-size: 30px !important;
color: {COLOR_INK} !important;
font-weight: 800 !important;
letter-spacing: -0.03em !important;
line-height: 1.2 !important;
}}
h2 {{
font-family: 'Space Grotesk', -apple-system, sans-serif !important;
font-size: 24px !important;
color: {COLOR_INK} !important;
font-weight: 800 !important;
letter-spacing: -0.02em !important;
line-height: 1.25 !important;
}}
h3, h4 {{
font-family: 'Space Grotesk', -apple-system, sans-serif !important;
font-size: 19px !important;
color: {COLOR_INK} !important;
font-weight: 700 !important;
letter-spacing: -0.01em !important;
line-height: 1.3 !important;
}}
h5, h6 {{
font-family: 'Space Grotesk', -apple-system, sans-serif !important;
font-size: 16px !important;
color: {COLOR_INK} !important;
font-weight: 700 !important;
}}
p, span, label {{
color: {COLOR_INK};
font-size: 14px;
line-height: 1.5;
}}

/* 3. Sidebar Styling */
section[data-testid="stSidebar"] {{
background-color: {COLOR_WHITE} !important;
border-right: 2px solid {COLOR_INK} !important;
}}
section[data-testid="stSidebar"] * {{
color: {COLOR_INK} !important;
}}

/* 4. BaseWeb Popover & Dropdown Portals (Selectbox, Menus) */
div[data-baseweb="popover"], div[data-baseweb="popover"] > div, div[data-baseweb="menu"], ul[data-baseweb="menu"], ul[role="listbox"] {{
background-color: #FFFFFF !important;
color: #000000 !important;
border: 2px solid #111111 !important;
box-shadow: 4px 4px 0px #111111 !important;
border-radius: 4px !important;
}}

/* Dropdown list items and options */
li[role="option"], div[role="option"], ul[role="listbox"] li, ul[data-baseweb="menu"] li {{
background-color: #FFFFFF !important;
color: #000000 !important;
font-family: 'Space Grotesk', -apple-system, sans-serif !important;
font-size: 14px !important;
font-weight: 500 !important;
padding: 9px 14px !important;
transition: background-color 0.1s ease !important;
}}

/* Dropdown Option Hover State */
li[role="option"]:hover, li[role="option"][aria-selected="true"]:hover, li[data-highlighted="true"], ul[role="listbox"] li:hover, ul[data-baseweb="menu"] li:hover {{
background-color: #FFE58A !important;
color: #000000 !important;
}}

/* Dropdown Option Selected State */
li[role="option"][aria-selected="true"], ul[role="listbox"] li[aria-selected="true"] {{
background-color: #F5B942 !important;
color: #000000 !important;
font-weight: 800 !important;
}}

/* Disabled Items */
li[aria-disabled="true"], li[aria-disabled="true"] * {{
color: #555555 !important;
background-color: #F8F7F4 !important;
cursor: not-allowed !important;
}}

/* Selectbox Input Box (Trigger container displaying selected value) */
div[data-baseweb="select"] > div {{
background-color: #FFFFFF !important;
border: 2px solid #111111 !important;
border-radius: 4px !important;
box-shadow: 2px 2px 0px #111111 !important;
color: #000000 !important;
}}
div[data-baseweb="select"] * {{
color: #000000 !important;
}}
div[data-baseweb="select"] svg {{
fill: #000000 !important;
color: #000000 !important;
}}

/* Multiselect Tags */
div[data-baseweb="tag"], span[data-baseweb="tag"] {{
background-color: #FFE58A !important;
color: #000000 !important;
border: 1.5px solid #111111 !important;
border-radius: 4px !important;
font-weight: 700 !important;
font-size: 13px !important;
padding: 2px 8px !important;
}}
div[data-baseweb="tag"] * {{
color: #000000 !important;
fill: #000000 !important;
}}

/* 5. Text and Number Inputs */
div[data-baseweb="input"] {{
background-color: #FFFFFF !important;
border: 2px solid #111111 !important;
border-radius: 4px !important;
box-shadow: 2px 2px 0px #111111 !important;
}}
div[data-baseweb="input"] input {{
background-color: #FFFFFF !important;
color: #000000 !important;
font-family: 'Space Grotesk', sans-serif !important;
font-size: 14px !important;
}}
input::placeholder, textarea::placeholder {{
color: #444444 !important;
opacity: 1 !important;
}}

/* 6. Date Picker & Calendar Pop-up */
div[data-baseweb="calendar"] {{
background-color: #FFFFFF !important;
border: 2px solid #111111 !important;
border-radius: 6px !important;
box-shadow: 4px 4px 0px #111111 !important;
color: #000000 !important;
}}
div[data-baseweb="calendar"] * {{
color: #000000 !important;
}}
div[data-baseweb="calendar"] button:hover {{
background-color: #FFE58A !important;
}}
div[data-baseweb="calendar"] button[aria-selected="true"] {{
background-color: #F5B942 !important;
color: #000000 !important;
font-weight: 800 !important;
}}

/* 7. Tooltips & Help Icons */
div[role="tooltip"], div[data-baseweb="tooltip"] {{
background-color: #FFFFFF !important;
color: #000000 !important;
border: 2px solid #111111 !important;
box-shadow: 3px 3px 0px #111111 !important;
font-size: 13px !important;
font-weight: 600 !important;
border-radius: 4px !important;
padding: 8px 12px !important;
}}
div[role="tooltip"] * {{
color: #000000 !important;
}}
svg[data-testid="stTooltipIcon"] {{
fill: #111111 !important;
color: #111111 !important;
}}

/* 8. Dataframe Container & Column Menu Pop-ups */
div[data-testid="stDataFrame"] {{
background-color: #FFFFFF !important;
border: 2px solid #111111 !important;
box-shadow: 4px 4px 0px #111111 !important;
border-radius: 6px !important;
overflow: hidden !important;
}}
div[data-testid="stDataFrameColumnMenu"], div[data-testid="stDataFrame"] div[role="menu"], div[data-testid="column-menu-popover"] {{
background-color: #FFFFFF !important;
color: #000000 !important;
border: 2px solid #111111 !important;
box-shadow: 4px 4px 0px #111111 !important;
border-radius: 4px !important;
}}
div[data-testid="stDataFrameColumnMenu"] *, div[data-testid="stDataFrame"] div[role="menu"] * {{
color: #000000 !important;
}}
div[data-testid="stDataFrameColumnMenu"] button:hover, div[data-testid="stDataFrame"] div[role="menu"] button:hover {{
background-color: #FFE58A !important;
color: #000000 !important;
}}

/* 9. HTML and Markdown Tables */
table {{
width: 100% !important;
border-collapse: collapse !important;
background-color: #FFFFFF !important;
border: 2px solid #111111 !important;
box-shadow: 3px 3px 0px #111111 !important;
border-radius: 4px !important;
margin-bottom: 16px !important;
}}
th {{
background-color: #F2EFE9 !important;
color: #000000 !important;
font-family: 'Space Grotesk', sans-serif !important;
font-weight: 800 !important;
font-size: 13px !important;
border: 1px solid #D9D4C8 !important;
padding: 10px 14px !important;
text-align: left !important;
}}
td {{
background-color: #FFFFFF !important;
color: #111111 !important;
font-size: 13px !important;
border: 1px solid #E8E4D8 !important;
padding: 9px 14px !important;
}}
tr:nth-child(even) td {{
background-color: #FAF8F2 !important;
}}
tr:hover td {{
background-color: #FFF2CC !important;
}}

/* 10. Tabs */
button[data-baseweb="tab"] {{
background-color: #FFFFFF !important;
color: #111111 !important;
border: 1.5px solid #111111 !important;
border-radius: 4px 4px 0px 0px !important;
font-weight: 700 !important;
font-family: 'Space Grotesk', sans-serif !important;
font-size: 14px !important;
padding: 8px 18px !important;
margin-right: 4px !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
background-color: #F5B942 !important;
color: #111111 !important;
font-weight: 800 !important;
border-bottom: 2px solid #F5B942 !important;
}}
button[data-baseweb="tab"]:hover {{
background-color: #FFE58A !important;
color: #111111 !important;
}}
div[data-baseweb="tab-highlight"] {{
background-color: #111111 !important;
}}
div[data-baseweb="tab-border"] {{
background-color: #111111 !important;
height: 2px !important;
}}

/* 11. Radio & Checkbox */
label[data-baseweb="radio"], label[data-baseweb="checkbox"] {{
color: #111111 !important;
font-size: 14px !important;
font-weight: 600 !important;
}}
label[data-baseweb="radio"] *, label[data-baseweb="checkbox"] * {{
color: #111111 !important;
}}

/* 12. Sliders */
div[data-baseweb="slider"] div[role="slider"] {{
background-color: #F5B942 !important;
border: 2px solid #111111 !important;
box-shadow: 2px 2px 0px #111111 !important;
}}
div[data-testid="stSliderTickBar"], div[data-testid="stSlider"] [data-testid="stThumbValue"], div[data-testid="stSlider"] * {{
color: #111111 !important;
font-weight: 700 !important;
font-family: 'Space Grotesk', sans-serif !important;
}}

/* 13. Expanders */
div[data-testid="stExpander"] {{
background-color: #FFFFFF !important;
border: 2px solid #111111 !important;
border-radius: 6px !important;
box-shadow: 3px 3px 0px #111111 !important;
margin-bottom: 14px !important;
}}
div[data-testid="stExpander"] summary {{
color: #111111 !important;
font-weight: 700 !important;
font-size: 15px !important;
font-family: 'Space Grotesk', sans-serif !important;
}}
div[data-testid="stExpander"] summary:hover {{
background-color: #FFF9E8 !important;
}}
div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {{
color: #111111 !important;
background-color: #FFFFFF !important;
}}

/* 14. Alerts, Toasts, and Callouts */
div[data-testid="stAlert"] {{
background-color: #FFFFFF !important;
color: #111111 !important;
border: 2px solid #111111 !important;
box-shadow: 3px 3px 0px #111111 !important;
border-radius: 6px !important;
}}
div[data-testid="stAlert"] * {{
color: #111111 !important;
}}
div[data-testid="stToast"] {{
background-color: #FFFFFF !important;
color: #111111 !important;
border: 2px solid #111111 !important;
box-shadow: 4px 4px 0px #111111 !important;
}}
div[data-testid="stToast"] * {{
color: #111111 !important;
}}

/* 15. File Uploader & Secondary / Download Buttons */
div[data-testid="stFileUploader"] {{
background-color: #FFFFFF !important;
border: 2px dashed #111111 !important;
border-radius: 6px !important;
padding: 14px !important;
}}
div[data-testid="stFileUploader"] * {{
color: #111111 !important;
}}
button[data-testid="stBaseButton-secondary"], div.stDownloadButton > button {{
background-color: #FFFFFF !important;
color: #111111 !important;
border: 2px solid #111111 !important;
box-shadow: 3px 3px 0px #111111 !important;
border-radius: 4px !important;
font-weight: 700 !important;
font-family: 'Space Grotesk', sans-serif !important;
font-size: 13px !important;
padding: 8px 18px !important;
transition: all 0.15s ease !important;
}}
button[data-testid="stBaseButton-secondary"]:hover, div.stDownloadButton > button:hover {{
background-color: #FFE58A !important;
color: #111111 !important;
transform: translate(-1px, -1px) !important;
box-shadow: 4px 4px 0px #111111 !important;
}}

/* 16. Header bar and action menu */
header[data-testid="stHeader"] {{
background-color: #FFF9E8 !important;
border-bottom: 2px solid #111111 !important;
}}
header[data-testid="stHeader"] button, header[data-testid="stHeader"] svg {{
color: #111111 !important;
fill: #111111 !important;
}}
ul[role="menu"], div[role="menu"] {{
background-color: #FFFFFF !important;
color: #111111 !important;
border: 2px solid #111111 !important;
box-shadow: 4px 4px 0px #111111 !important;
border-radius: 4px !important;
}}
li[role="menuitem"], div[role="menuitem"] {{
color: #111111 !important;
background-color: #FFFFFF !important;
font-size: 14px !important;
font-weight: 600 !important;
}}
li[role="menuitem"]:hover, div[role="menuitem"]:hover {{
background-color: #FFE58A !important;
color: #111111 !important;
}}

/* 17. Buttons in Neo-Brutalist Editorial Style */
button[kind="primary"], div.stButton > button:first-child {{
background-color: {COLOR_AMBER} !important;
color: {COLOR_INK} !important;
border: 2px solid {COLOR_INK} !important;
box-shadow: 3px 3px 0px {COLOR_INK} !important;
border-radius: 4px !important;
font-weight: 700 !important;
font-family: 'Space Grotesk', sans-serif !important;
font-size: 13px !important;
padding: 8px 18px !important;
transition: all 0.15s ease !important;
}}
button[kind="primary"]:hover, div.stButton > button:first-child:hover {{
transform: translate(-1px, -1px) !important;
box-shadow: 4px 4px 0px {COLOR_INK} !important;
background-color: #E2A633 !important;
}}
button[kind="secondary"] {{
background-color: {COLOR_WHITE} !important;
color: {COLOR_INK} !important;
border: 2px solid {COLOR_INK} !important;
box-shadow: 3px 3px 0px {COLOR_INK} !important;
border-radius: 4px !important;
font-weight: 600 !important;
font-family: 'Space Grotesk', sans-serif !important;
font-size: 13px !important;
}}

/* 18. Editorial Cards */
.editorial-card, .instrument-card {{
background: {COLOR_WHITE};
border: 2px solid {COLOR_INK};
box-shadow: 4px 4px 0px {COLOR_INK};
border-radius: 6px;
padding: 16px 18px;
position: relative;
margin-bottom: 14px;
min-height: 140px;
display: flex;
flex-direction: column;
justify-content: space-between;
box-sizing: border-box;
transition: transform 0.15s ease, box-shadow 0.15s ease;
}}
.editorial-card:hover, .instrument-card:hover {{
transform: translate(-1px, -1px);
box-shadow: 5px 5px 0px {COLOR_INK};
}}

.instrument-tag {{
font-family: 'Space Grotesk', sans-serif;
font-size: 13px;
font-weight: 700;
text-transform: uppercase;
letter-spacing: 0.05em;
color: {COLOR_INK};
margin-bottom: 6px;
display: flex;
justify-content: space-between;
align-items: center;
}}
.instrument-val {{
font-family: 'Space Grotesk', sans-serif;
font-size: 26px;
font-weight: 800;
color: {COLOR_INK};
line-height: 1.2;
letter-spacing: -0.02em;
word-wrap: break-word;
overflow-wrap: break-word;
white-space: normal;
font-variant-numeric: tabular-nums;
}}
.instrument-sub {{
font-family: 'Space Grotesk', sans-serif;
font-size: 13px;
color: {COLOR_INK};
margin-top: 6px;
display: flex;
align-items: center;
gap: 8px;
flex-wrap: wrap;
word-break: break-word;
}}

/* Delta badges */
.delta-pill-bad {{
background: {COLOR_ROSE_LIGHT};
color: #9B1C1C;
border: 1.5px solid {COLOR_INK};
padding: 2px 8px;
border-radius: 999px;
font-weight: 700;
font-size: 12px;
}}
.delta-pill-good {{
background: {COLOR_GREEN_LIGHT};
color: #03543F;
border: 1.5px solid {COLOR_INK};
padding: 2px 8px;
border-radius: 999px;
font-weight: 700;
font-size: 12px;
}}
.delta-pill-neutral {{
background: {COLOR_AMBER};
color: {COLOR_INK};
border: 1.5px solid {COLOR_INK};
padding: 2px 8px;
border-radius: 999px;
font-weight: 700;
font-size: 12px;
}}
</style>"""
    render_html(custom_css)


# ==============================================================================
# 5. COMPACT EDITORIAL TOP NAVIGATION
# ==============================================================================
def render_command_strip(
    active_page: str = "Overview",
    region_tag: str = "GLOBAL",
    product_tag: str = "CRUDE & REFINED",
    reporting_period: str = "2024–2025"
):
    """Renders the top editorial navigation bar with brand, links, and status."""
    apply_theme()
    health = db_manager.check_health()
    engine_name = "MYSQL 8.4" if health["dialect"] == "mysql" else "LOCAL CACHE"
    logo_svg = get_brand_logo_svg(width=290, height=48)

    nav_html = f"""<div style="background: {COLOR_WHITE}; border: 2px solid {COLOR_INK}; box-shadow: 4px 4px 0px {COLOR_INK}; border-radius: 6px; padding: 12px 20px; margin: -0.5rem 0 1.75rem 0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
<div style="display: flex; align-items: center; gap: 14px;">{logo_svg}</div>
<div style="display: flex; align-items: center; gap: 8px; font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 700; flex-wrap: wrap;">
<a href="#ch-01" style="color: {COLOR_INK}; text-decoration: none; padding: 4px 8px; border-radius: 3px;">Overview</a>
<span style="color: {COLOR_BORDER_LIGHT};">•</span>
<a href="#ch-02" style="color: {COLOR_INK}; text-decoration: none; padding: 4px 8px; border-radius: 3px;">Production</a>
<span style="color: {COLOR_BORDER_LIGHT};">•</span>
<a href="#ch-03" style="color: {COLOR_INK}; text-decoration: none; padding: 4px 8px; border-radius: 3px;">Trade</a>
<span style="color: {COLOR_BORDER_LIGHT};">•</span>
<a href="#ch-04" style="color: {COLOR_INK}; text-decoration: none; padding: 4px 8px; border-radius: 3px;">Fuel Prices</a>
<span style="color: {COLOR_BORDER_LIGHT};">•</span>
<a href="#ch-05" style="color: {COLOR_INK}; text-decoration: none; padding: 4px 8px; border-radius: 3px;">India Fuel</a>
<span style="color: {COLOR_BORDER_LIGHT};">•</span>
<a href="#ch-06" style="color: {COLOR_INK}; text-decoration: none; padding: 4px 8px; border-radius: 3px;">Companies</a>
<span style="color: {COLOR_BORDER_LIGHT};">•</span>
<a href="#ch-11" style="color: {COLOR_INK}; text-decoration: none; padding: 4px 8px; border-radius: 3px;">Data Trust</a>
</div>
<div style="display: flex; align-items: center; gap: 12px;">
<span style="background: {COLOR_GREEN_LIGHT}; color: #03543F; border: 1.5px solid {COLOR_INK}; padding: 4px 10px; border-radius: 999px; font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 700;">● {engine_name} VERIFIED</span>
<a href="#ch-05" style="background: {COLOR_AMBER}; color: {COLOR_INK}; border: 2px solid {COLOR_INK}; box-shadow: 2px 2px 0px {COLOR_INK}; padding: 6px 14px; border-radius: 4px; font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 800; text-decoration: none;">EXPLORE MARKETS ↗</a>
</div>
</div>"""
    render_html(nav_html)


# ==============================================================================
# 6. GLOBAL SIGNAL RAIL (HORIZONTAL EDITORIAL STRIP)
# ==============================================================================
def render_signal_rail(signals: List[Dict[str, str]]):
    """Renders a clean horizontal editorial strip with black borders and offset shadows."""
    html_items = []
    for s in signals:
        html_items.append(
            f"""<div style="flex: 1; min-width: 170px; padding: 10px 14px; border-right: 1.5px solid {COLOR_BORDER_LIGHT}; display: flex; flex-direction: column;">
<span style="font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 700; color: {COLOR_INK}; text-transform: uppercase; letter-spacing: 0.05em;">{s.get('label', '')}</span>
<span style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 800; color: {COLOR_INK}; margin-top: 3px;">{s.get('value', '')}</span>
<span style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; color: #222222; margin-top: 2px;">{s.get('note', '')}</span>
</div>"""
        )
    rail_html = f"""<div style="background: {COLOR_WHITE}; border: 2px solid {COLOR_INK}; box-shadow: 4px 4px 0px {COLOR_INK}; border-radius: 6px; padding: 6px 12px; margin-bottom: 1.5rem; display: flex; flex-wrap: wrap; align-items: center;">
{''.join(html_items)}
</div>"""
    render_html(rail_html)


# ==============================================================================
# 7. EDITORIAL INSTRUMENT CARD COMPONENT
# ==============================================================================
def render_instrument_card(
    label: str,
    value: str,
    accent: str = "amber",
    delta: Optional[str] = None,
    delta_is_positive_bad: bool = True,
    subtext: Optional[str] = None,
    code_badge: Optional[str] = None
):
    """Renders an editorial card with solid black border, 4px offset shadow, and wrapping text."""
    delta_html = ""
    if delta:
        is_pos = not delta.startswith("-") and delta != "0.0%" and delta != "0.00"
        pill_class = "delta-pill-bad" if (is_pos and delta_is_positive_bad) else ("delta-pill-good" if not is_pos else "delta-pill-neutral")
        arrow = "▲" if is_pos else ("▼" if delta.startswith("-") else "")
        delta_html = f'<span class="{pill_class}">{arrow} {delta}</span>'

    badge_html = f'<span style="background: {COLOR_CREAM}; border: 1.5px solid {COLOR_INK}; color: {COLOR_INK}; font-weight: 800; padding: 1px 7px; border-radius: 4px; font-size: 12px;">{code_badge}</span>' if code_badge else ""
    sub_span = f'<span>{subtext}</span>' if subtext else ""

    card_html = f"""<div class="editorial-card">
<div class="instrument-tag"><span>{label}</span>{badge_html}</div>
<div class="instrument-val">{value}</div>
<div class="instrument-sub">{delta_html}{sub_span}</div>
</div>"""
    render_html(card_html)


# ==============================================================================
# 8. CHAPTER HEADER & PERSISTENT CHAPTER NAVIGATION
# ==============================================================================
def render_chapter_header(
    chapter_num: str,
    title: str,
    subtitle: str,
    source_tag: str,
    anchor_id: str,
    action_page_url: Optional[str] = None,
    action_label: Optional[str] = "EXPLORE DRILL-DOWN"
):
    """Renders an editorial chapter banner with clear numbering, divider, and metadata."""
    action_html = ""
    if action_page_url:
        action_html = f"""<a href="{action_page_url}" style="display: inline-flex; align-items: center; gap: 6px; background: {COLOR_AMBER}; color: {COLOR_INK}; border: 2px solid {COLOR_INK}; box-shadow: 2px 2px 0px {COLOR_INK}; padding: 6px 14px; border-radius: 4px; font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 800; text-decoration: none; letter-spacing: 0.04em;"><span>{action_label}</span> ↗</a>"""

    header_html = f"""<div id="{anchor_id}" style="margin-top: 3.5rem; margin-bottom: 1.5rem; padding-top: 1.5rem; border-top: 3px solid {COLOR_INK};">
<div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 14px;">
<div>
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
<span style="background: {COLOR_AMBER}; color: {COLOR_INK}; border: 1.5px solid {COLOR_INK}; padding: 2px 10px; border-radius: 999px; font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase;">CHAPTER {chapter_num}</span>
</div>
<h2 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 800; color: {COLOR_INK}; letter-spacing: -0.03em; margin: 0; line-height: 1.2;">{title}</h2>
<div style="font-family: 'Space Grotesk', sans-serif; font-size: 14px; color: #222222; margin-top: 6px; max-width: 820px; line-height: 1.5;">{subtitle}</div>
</div>
<div style="display: flex; flex-direction: column; align-items: flex-end; gap: 8px;">
{action_html}
<div style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 700; color: {COLOR_INK}; background: {COLOR_WHITE}; padding: 4px 10px; border: 1.5px solid {COLOR_BORDER_LIGHT}; border-radius: 4px;">DATA: {source_tag}</div>
</div>
</div>
</div>"""
    render_html(header_html)


def render_chapter_nav():
    """Renders a floating Tubelight horizontal navigation bar for the 11 analytical chapters."""
    chapters = [
        ("01", "At a Glance", "#ch-01"),
        ("02", "Production", "#ch-02"),
        ("03", "Trade Flows", "#ch-03"),
        ("04", "Fuel Prices", "#ch-04"),
        ("05", "India Price", "#ch-05"),
        ("06", "Oil Companies", "#ch-06"),
        ("07", "Consumption", "#ch-07"),
        ("08", "Taxes & Revenue", "#ch-08"),
        ("09", "Risk & Security", "#ch-09"),
        ("10", "Forecasts & Lab", "#ch-10"),
        ("11", "Data Sources", "#ch-11")
    ]

    nav_links = "".join([
        f'<a href="{anchor}" class="tubelight-nav-item"><span class="tubelight-lamp"></span><span class="ch-badge">{num}</span><span>{name}</span></a>'
        for num, name, anchor in chapters
    ])

    css_and_nav = f"""<style>
.tubelight-nav-wrapper {{
    display: flex;
    justify-content: center;
    position: sticky;
    top: 12px;
    z-index: 999;
    margin: 0 auto 2rem auto;
    width: 100%;
}}
.tubelight-nav-container {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255, 255, 255, 0.94);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 2px solid {COLOR_INK};
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08), 4px 4px 0px {COLOR_INK};
    border-radius: 9999px;
    padding: 6px 10px;
    max-width: 98%;
    overflow-x: auto;
    scrollbar-width: none;
    -ms-overflow-style: none;
    white-space: nowrap;
}}
.tubelight-nav-container::-webkit-scrollbar {{
    display: none;
}}
.tubelight-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 800;
    color: {COLOR_INK};
    letter-spacing: 0.05em;
    padding: 6px 12px;
    background: {COLOR_CREAM};
    border: 1.5px solid {COLOR_INK};
    border-radius: 9999px;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    margin-right: 4px;
}}
.tubelight-nav-item {{
    position: relative;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 7px 14px;
    border-radius: 9999px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 12.5px;
    font-weight: 700;
    color: {COLOR_INK};
    text-decoration: none;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    background: transparent;
}}
.tubelight-nav-item .ch-badge {{
    background: {COLOR_INK};
    color: {COLOR_WHITE};
    font-size: 10.5px;
    font-weight: 800;
    padding: 1px 6px;
    border-radius: 9999px;
}}
.tubelight-nav-item .tubelight-lamp {{
    position: absolute;
    top: -2px;
    left: 50%;
    transform: translateX(-50%);
    width: 0px;
    height: 3px;
    background: {COLOR_AMBER};
    border-radius: 9999px;
    transition: all 0.25s ease-out;
    opacity: 0;
}}
.tubelight-nav-item:hover {{
    background: rgba(245, 185, 66, 0.15);
    color: #000000;
    transform: translateY(-2px);
}}
.tubelight-nav-item:hover .tubelight-lamp {{
    width: 28px;
    opacity: 1;
    box-shadow: 0 0 12px 3px rgba(245, 185, 66, 0.85), 0 0 24px 6px rgba(245, 185, 66, 0.45);
}}
</style>
<div class="tubelight-nav-wrapper">
<div class="tubelight-nav-container">
<div class="tubelight-title">⚡ CHAPTERS</div>
{nav_links}
</div>
</div>"""
    render_html(css_and_nav)


# ==============================================================================
# 9. HIGH-CONTRAST EDITORIAL PLOTLY THEME
# ==============================================================================
def deep_merge(base: dict, update: dict) -> dict:
    """Recursively merges two dictionaries so nested styling keys are never clobbered."""
    merged = base.copy()
    for k, v in update.items():
        if isinstance(v, dict) and k in merged and isinstance(merged[k], dict):
            merged[k] = deep_merge(merged[k], v)
        else:
            merged[k] = v
    return merged


def get_atlas_plotly_theme(height: int = 420, **overrides) -> Dict[str, Any]:
    """Returns layout dictionary for Plotly charts matching the clean Editorial aesthetic with pure black legend text."""
    theme = dict(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="'Space Grotesk', 'Inter', -apple-system, sans-serif",
            color="#111111",
            size=13
        ),
        margin=dict(l=20, r=20, t=35, b=20),
        height=height,
        colorway=EDITORIAL_COLORWAY,
        title=dict(
            font=dict(color="#111111", family="'Space Grotesk', sans-serif", size=16)
        ),
        xaxis=dict(
            gridcolor="#E8E4D8",
            zerolinecolor="#E8E4D8",
            tickfont=dict(color="#111111", family="'Space Grotesk', sans-serif", size=13),
            title=dict(font=dict(color="#111111", family="'Space Grotesk', sans-serif", size=14))
        ),
        yaxis=dict(
            gridcolor="#E8E4D8",
            zerolinecolor="#E8E4D8",
            tickfont=dict(color="#111111", family="'Space Grotesk', sans-serif", size=13),
            title=dict(font=dict(color="#111111", family="'Space Grotesk', sans-serif", size=14))
        ),
        legend=dict(
            bgcolor="#FFFFFF",
            bordercolor="#111111",
            borderwidth=1.5,
            font=dict(color="#000000", family="'Space Grotesk', sans-serif", size=13)
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#111111",
            font=dict(color="#000000", family="'Space Grotesk', sans-serif", size=13)
        )
    )
    return deep_merge(theme, overrides)


def apply_atlas_theme(fig, height: int = 460, **kwargs):
    """Safely applies Editorial styling to a Plotly figure without duplicate keyword collisions."""
    return apply_clean_layout(fig, height=height, **kwargs)


def render_page_header(title: str, subtitle: str, source_tag: str, observation_date: str):
    """Renders a clean editorial page banner for drill-down pages."""
    apply_theme()
    header_html = f"""<div style="background: {COLOR_WHITE}; border: 2px solid {COLOR_INK}; box-shadow: 4px 4px 0px {COLOR_INK}; border-radius: 6px; padding: 22px 26px; margin-bottom: 24px;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
<div>
<h1 style="font-size: 30px; margin: 0; color: {COLOR_INK};">{title}</h1>
<p style="font-size: 14px; color: #222222; margin-top: 4px; margin-bottom: 0;">{subtitle}</p>
</div>
<div style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; color: {COLOR_INK}; text-align: right;">
<div><b>SOURCE:</b> {source_tag}</div>
<div><b>OBSERVED:</b> {observation_date}</div>
</div>
</div>
</div>"""
    render_html(header_html)


def render_csv_download(df: pd.DataFrame, filename: str, label: str = "📥 EXPORT CSV DATASET"):
    """Provides a technical export button in editorial styling."""
    if df.empty:
        return
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=label,
        data=csv,
        file_name=filename,
        mime="text/csv"
    )
