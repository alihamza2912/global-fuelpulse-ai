"""
GLOBAL FUELPULSE AI — EDITORIAL DESIGN SYSTEM & UI COMPONENTS
Premium Modern Energy Intelligence & Glassmorphic Layout Language.
Visual identity: Deep Obsidian (#070A12), Dark Glass (#0E1526),
Crisp White Typography (#F9FAFB), and Petroleum Amber (#F5B942).
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
# 1. COLOR PALETTE CONSTANTS (DARK OBSIDIAN & GLASSMORPHIC DIRECTION)
# ==============================================================================
COLOR_CREAM = "#070A12"          # Dark obsidian global canvas
COLOR_WHITE = "#0E1526"          # Dark glass card surface
COLOR_INK = "#F9FAFB"            # Solid luminous white typography
COLOR_AMBER = "#F5B942"          # Petroleum amber-yellow accent
COLOR_GREEN_LIGHT = "rgba(16, 185, 129, 0.22)"  # Soft emerald glass badge
COLOR_BLUE_LIGHT = "rgba(59, 130, 246, 0.22)"   # Soft sapphire glass badge
COLOR_ROSE_LIGHT = "rgba(244, 63, 94, 0.22)"    # Soft rose glass badge
COLOR_GRAY_MUTED = "#94A3B8"     # Slate secondary text
COLOR_BORDER_LIGHT = "rgba(255, 255, 255, 0.12)" # Subtle hairline translucent borders

# Backward-compatible aliases for legacy modules
COLOR_GRAPHITE = COLOR_CREAM
COLOR_OBSIDIAN = COLOR_WHITE
COLOR_SURFACE_ALT = COLOR_WHITE
COLOR_BORDER = "rgba(255, 255, 255, 0.14)"
COLOR_TEXT_PRIMARY = COLOR_INK
COLOR_TEXT_MUTED = COLOR_GRAY_MUTED
COLOR_TEXT_FAINT = "#64748B"
COLOR_COPPER = "#F59E0B"
COLOR_TEAL = "#14B8A6"
COLOR_RED = "#F43F5E"

# Modern luminous Plotly colorway
EDITORIAL_COLORWAY = [COLOR_AMBER, "#60A5FA", "#34D399", "#F472B6", "#A78BFA", "#F87171"]
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
def get_logo_mark_svg(size: int = 36) -> str:
    """Returns the standalone compact petroleum droplet, trade-route orbit, and energy pulse mark."""
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="36" height="36" rx="8" fill="#0E1526" stroke="rgba(255, 255, 255, 0.15)" stroke-width="1.2"/>
  <!-- Orbital Global Trade Route Curve -->
  <ellipse cx="18" cy="18" rx="14.5" ry="6.2" transform="rotate(-26 18 18)" stroke="#60A5FA" stroke-width="1.4" stroke-dasharray="3 2" opacity="0.85"/>
  <circle cx="28.5" cy="12.5" r="1.8" fill="#F5B942"/>
  <!-- Petroleum Fuel Droplet -->
  <path d="M18 7 C18 7 11.5 15.5 11.5 20.5 A6.5 6.5 0 0 0 24.5 20.5 C24.5 15.5 18 7 18 7 Z" fill="url(#gfp_drop_grad)" stroke="#F5B942" stroke-width="1.3"/>
  <!-- Energy Frequency Pulse Waveform -->
  <path d="M12 20.5 L15 20.5 L16.8 16.5 L19.5 24.5 L21.2 20.5 L24 20.5" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  <defs>
    <linearGradient id="gfp_drop_grad" x1="18" y1="7" x2="18" y2="27" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F5B942"/>
      <stop offset="65%" stop-color="#D97706"/>
      <stop offset="100%" stop-color="#0E1526"/>
    </linearGradient>
  </defs>
</svg>"""


def get_brand_logo_svg(width: int = 340, height: int = 54) -> str:
    """Returns the full brand lockup: distinctive vector trade emblem + Global FuelPulse AI typography."""
    return f"""<svg width="{width}" height="{height}" viewBox="0 0 340 54" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Droplet & Trade Route Orbit Emblem -->
  <g transform="translate(4, 6)">
    <rect width="42" height="42" rx="9" fill="#0E1526" stroke="rgba(255, 255, 255, 0.16)" stroke-width="1.3"/>
    <ellipse cx="21" cy="21" rx="17" ry="7.2" transform="rotate(-26 21 21)" stroke="#60A5FA" stroke-width="1.5" stroke-dasharray="3.5 2" opacity="0.9"/>
    <circle cx="33" cy="14.5" r="2.1" fill="#F5B942"/>
    <path d="M21 8 C21 8 13.5 18 13.5 24 A7.5 7.5 0 0 0 28.5 24 C28.5 18 21 8 21 8 Z" fill="url(#gfp_brand_drop)" stroke="#F5B942" stroke-width="1.4"/>
    <path d="M14 24 L17.5 24 L19.6 19 L22.8 28.5 L24.8 24 L28 24" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <defs>
    <linearGradient id="gfp_brand_drop" x1="21" y1="8" x2="21" y2="31" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F5B942"/>
      <stop offset="65%" stop-color="#D97706"/>
      <stop offset="100%" stop-color="#0E1526"/>
    </linearGradient>
  </defs>
  <!-- Typography Lockup -->
  <text x="56" y="27" fill="#F9FAFB" font-family="'Space Grotesk', -apple-system, sans-serif" font-weight="800" font-size="18" letter-spacing="0.04em">GLOBAL FUELPULSE</text>
  <rect x="256" y="13" width="28" height="18" rx="4" fill="rgba(245, 185, 66, 0.22)" stroke="#F5B942" stroke-width="1.2"/>
  <text x="270" y="26" fill="#F5B942" font-family="'Space Grotesk', sans-serif" font-weight="800" font-size="11.5" text-anchor="middle">AI</text>
  <text x="56" y="44" fill="#94A3B8" font-family="'Inter', sans-serif" font-weight="700" font-size="11.5" letter-spacing="0.05em">ENERGY INTELLIGENCE PLATFORM</text>
</svg>"""


def get_fuel_client_logo_html() -> str:
    """Returns a client-facing badge with the distinctive fuel trade logo."""
    return f"""
    <div style="
        display: inline-flex;
        align-items: center;
        gap: 9px;
        background: rgba(14, 21, 38, 0.85);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4);
        padding: 5px 14px;
        border-radius: 9999px;
        margin-bottom: 12px;
        width: fit-content;
        position: relative;
        z-index: 5;
    ">
        {get_logo_mark_svg(20)}
        <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; color: #F9FAFB; text-transform: uppercase;">
            GLOBAL FUELPULSE <span style="background: rgba(245, 185, 66, 0.2); color: #F5B942; padding: 2px 8px; border-radius: 999px; font-weight: 800; border: 1px solid rgba(245, 185, 66, 0.4); margin-left: 6px;">INTELLIGENCE</span>
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
  0%, 100% {{ transform: scale(1); opacity: 0.6; }}
  50%      {{ transform: scale(1.1); opacity: 0.95; }}
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
    linear-gradient(to right, rgba(255, 255, 255, 0.05) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
  background-size: 36px 36px;
  opacity: 0.65;
  animation: fp-grid-drift 26s linear infinite;
  will-change: background-position;
}}
.{container_class}::after {{
  background-image:
    linear-gradient(to right, rgba(245, 185, 66, 0.2) 1.2px, transparent 1.2px),
    linear-gradient(to bottom, rgba(245, 185, 66, 0.2) 1.2px, transparent 1.2px);
  background-size: 144px 144px;
  opacity: 0.55;
  animation: fp-grid-drift 26s linear infinite;
  will-change: background-position;
}}
.{container_class}-glow {{
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: radial-gradient(45% 45% at 50% 42%, rgba(245, 185, 66, 0.16), transparent 70%);
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
    """Injects high-contrast modern dark obsidian and glassmorphic styling."""
    custom_css = f"""<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700&family=Space+Grotesk:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

@keyframes stapp-grid-drift {{
  from {{ background-position: 0 0, 0 0, 0 0, 0 0; }}
  to   {{ background-position: 144px 144px, 144px 144px, 144px 144px, 144px 144px; }}
}}

/* 1. Global page canvas with dark animated grid backdrop */
.stApp {{
  background-color: #070A12 !important;
  background-image:
    radial-gradient(at 0% 0%, rgba(245, 185, 66, 0.08) 0px, transparent 50%),
    radial-gradient(at 100% 0%, rgba(59, 130, 246, 0.08) 0px, transparent 50%),
    linear-gradient(to right, rgba(255, 255, 255, 0.035) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(255, 255, 255, 0.035) 1px, transparent 1px) !important;
  background-size: 100% 100%, 100% 100%, 48px 48px, 48px 48px !important;
  color: #F9FAFB !important;
  font-family: 'Space Grotesk', 'Inter', -apple-system, sans-serif;
}}
@media (prefers-reduced-motion: reduce) {{
  .stApp {{ animation: none !important; }}
}}

/* 2. Global typography scale */
h1 {{
  font-family: 'Space Grotesk', -apple-system, sans-serif !important;
  font-size: 30px !important;
  color: #F9FAFB !important;
  font-weight: 800 !important;
  letter-spacing: -0.03em !important;
  line-height: 1.2 !important;
}}
h2 {{
  font-family: 'Space Grotesk', -apple-system, sans-serif !important;
  font-size: 24px !important;
  color: #F9FAFB !important;
  font-weight: 800 !important;
  letter-spacing: -0.02em !important;
  line-height: 1.25 !important;
}}
h3, h4 {{
  font-family: 'Space Grotesk', -apple-system, sans-serif !important;
  font-size: 19px !important;
  color: #F9FAFB !important;
  font-weight: 700 !important;
  letter-spacing: -0.01em !important;
  line-height: 1.3 !important;
}}
h5, h6 {{
  font-family: 'Space Grotesk', -apple-system, sans-serif !important;
  font-size: 16px !important;
  color: #F9FAFB !important;
  font-weight: 700 !important;
}}
p, span, label {{
  color: #E2E8F0;
  font-size: 14px;
  line-height: 1.5;
}}

/* 3. Sidebar Styling */
section[data-testid="stSidebar"] {{
  background-color: #0B101E !important;
  border-right: 1px solid rgba(255, 255, 255, 0.10) !important;
}}
section[data-testid="stSidebar"] * {{
  color: #F9FAFB !important;
}}

/* 4. BaseWeb Popover & Dropdown Portals (Selectbox, Menus) */
div[data-baseweb="popover"], div[data-baseweb="popover"] > div, div[data-baseweb="menu"], ul[data-baseweb="menu"], ul[role="listbox"] {{
  background-color: #0E1526 !important;
  color: #F9FAFB !important;
  border: 1px solid rgba(255, 255, 255, 0.16) !important;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.6) !important;
  border-radius: 8px !important;
}}

/* Dropdown list items and options */
li[role="option"], div[role="option"], ul[role="listbox"] li, ul[data-baseweb="menu"] li {{
  background-color: #0E1526 !important;
  color: #F9FAFB !important;
  font-family: 'Space Grotesk', -apple-system, sans-serif !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  padding: 9px 14px !important;
  transition: background-color 0.15s ease !important;
}}

/* Dropdown Option Hover State */
li[role="option"]:hover, li[role="option"][aria-selected="true"]:hover, li[data-highlighted="true"], ul[role="listbox"] li:hover, ul[data-baseweb="menu"] li:hover {{
  background-color: rgba(245, 185, 66, 0.15) !important;
  color: #F5B942 !important;
}}

/* Dropdown Option Selected State */
li[role="option"][aria-selected="true"], ul[role="listbox"] li[aria-selected="true"] {{
  background-color: rgba(245, 185, 66, 0.25) !important;
  color: #F5B942 !important;
  font-weight: 800 !important;
}}

/* Disabled Items */
li[aria-disabled="true"], li[aria-disabled="true"] * {{
  color: #64748B !important;
  background-color: #0B101E !important;
  cursor: not-allowed !important;
}}

/* Selectbox Input Box (Trigger container displaying selected value) */
div[data-baseweb="select"] > div {{
  background-color: #0E1526 !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  border-radius: 6px !important;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
  color: #F9FAFB !important;
}}
div[data-baseweb="select"] * {{
  color: #F9FAFB !important;
}}
div[data-baseweb="select"] svg {{
  fill: #F5B942 !important;
  color: #F5B942 !important;
}}

/* Multiselect Tags */
div[data-baseweb="tag"], span[data-baseweb="tag"] {{
  background-color: rgba(245, 185, 66, 0.2) !important;
  color: #F5B942 !important;
  border: 1px solid rgba(245, 185, 66, 0.4) !important;
  border-radius: 4px !important;
  font-weight: 700 !important;
  font-size: 13px !important;
  padding: 2px 8px !important;
}}
div[data-baseweb="tag"] * {{
  color: #F5B942 !important;
  fill: #F5B942 !important;
}}

/* 5. Text and Number Inputs */
div[data-baseweb="input"] {{
  background-color: #0E1526 !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  border-radius: 6px !important;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
}}
div[data-baseweb="input"] input {{
  background-color: transparent !important;
  color: #F9FAFB !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 14px !important;
}}
input::placeholder, textarea::placeholder {{
  color: #64748B !important;
  opacity: 1 !important;
}}

/* 6. Date Picker & Calendar Pop-up */
div[data-baseweb="calendar"] {{
  background-color: #0E1526 !important;
  border: 1px solid rgba(255, 255, 255, 0.16) !important;
  border-radius: 8px !important;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.6) !important;
  color: #F9FAFB !important;
}}
div[data-baseweb="calendar"] * {{
  color: #F9FAFB !important;
}}
div[data-baseweb="calendar"] button:hover {{
  background-color: rgba(245, 185, 66, 0.15) !important;
  color: #F5B942 !important;
}}
div[data-baseweb="calendar"] button[aria-selected="true"] {{
  background-color: #F5B942 !important;
  color: #070A12 !important;
  font-weight: 800 !important;
}}

/* 7. Tooltips & Help Icons */
div[role="tooltip"], div[data-baseweb="tooltip"] {{
  background-color: #151F38 !important;
  color: #F9FAFB !important;
  border: 1px solid rgba(255, 255, 255, 0.16) !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5) !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  border-radius: 6px !important;
  padding: 8px 12px !important;
}}
div[role="tooltip"] * {{
  color: #F9FAFB !important;
}}
svg[data-testid="stTooltipIcon"] {{
  fill: #F5B942 !important;
  color: #F5B942 !important;
}}

/* 8. Dataframe Container & Column Menu Pop-ups */
div[data-testid="stDataFrame"] {{
  background-color: #0E1526 !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
  border-radius: 8px !important;
  overflow: hidden !important;
}}
div[data-testid="stDataFrameColumnMenu"], div[data-testid="stDataFrame"] div[role="menu"], div[data-testid="column-menu-popover"] {{
  background-color: #0E1526 !important;
  color: #F9FAFB !important;
  border: 1px solid rgba(255, 255, 255, 0.16) !important;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5) !important;
  border-radius: 6px !important;
}}
div[data-testid="stDataFrameColumnMenu"] *, div[data-testid="stDataFrame"] div[role="menu"] * {{
  color: #F9FAFB !important;
}}
div[data-testid="stDataFrameColumnMenu"] button:hover, div[data-testid="stDataFrame"] div[role="menu"] button:hover {{
  background-color: rgba(245, 185, 66, 0.15) !important;
  color: #F5B942 !important;
}}

/* 9. HTML and Markdown Tables */
table {{
  width: 100% !important;
  border-collapse: collapse !important;
  background-color: #0E1526 !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35) !important;
  border-radius: 8px !important;
  overflow: hidden !important;
  margin-bottom: 16px !important;
}}
th {{
  background-color: #151F38 !important;
  color: #F9FAFB !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-weight: 700 !important;
  font-size: 13px !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.12) !important;
  padding: 10px 14px !important;
  text-align: left !important;
}}
td {{
  background-color: #0E1526 !important;
  color: #E2E8F0 !important;
  font-size: 13px !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
  padding: 9px 14px !important;
}}
tr:nth-child(even) td {{
  background-color: #111B30 !important;
}}
tr:hover td {{
  background-color: rgba(245, 185, 66, 0.08) !important;
}}

/* 10. Tabs */
button[data-baseweb="tab"] {{
  background-color: rgba(14, 21, 38, 0.75) !important;
  color: #FFFFFF !important;
  -webkit-text-fill-color: #FFFFFF !important;
  border: 1px solid rgba(255, 255, 255, 0.16) !important;
  border-bottom: none !important;
  border-radius: 6px 6px 0px 0px !important;
  font-weight: 700 !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 14px !important;
  padding: 9px 20px !important;
  margin-right: 4px !important;
}}
button[data-baseweb="tab"] * {{
  color: #FFFFFF !important;
  -webkit-text-fill-color: #FFFFFF !important;
  font-weight: 700 !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
  background-color: #0E1526 !important;
  color: #FACC15 !important;
  -webkit-text-fill-color: #FACC15 !important;
  font-weight: 800 !important;
  border-top: 2.5px solid #EAB308 !important;
  border-bottom: 2px solid #0E1526 !important;
}}
button[data-baseweb="tab"][aria-selected="true"] * {{
  color: #FACC15 !important;
  -webkit-text-fill-color: #FACC15 !important;
  font-weight: 800 !important;
}}
button[data-baseweb="tab"]:hover {{
  color: #FACC15 !important;
  -webkit-text-fill-color: #FACC15 !important;
  background-color: #151F38 !important;
}}
button[data-baseweb="tab"]:hover * {{
  color: #FACC15 !important;
  -webkit-text-fill-color: #FACC15 !important;
}}
div[data-baseweb="tab-highlight"] {{
  background-color: #EAB308 !important;
}}
div[data-baseweb="tab-border"] {{
  background-color: rgba(255, 255, 255, 0.16) !important;
  height: 2px !important;
}}

/* 11. Radio & Checkbox */
label[data-baseweb="radio"], label[data-baseweb="checkbox"] {{
  color: #F9FAFB !important;
  font-size: 14px !important;
  font-weight: 600 !important;
}}
label[data-baseweb="radio"] *, label[data-baseweb="checkbox"] * {{
  color: #F9FAFB !important;
}}

/* 12. Sliders */
div[data-baseweb="slider"] div[role="slider"] {{
  background-color: #F5B942 !important;
  border: 2px solid #070A12 !important;
  box-shadow: 0 0 10px rgba(245, 185, 66, 0.6) !important;
}}
div[data-testid="stSliderTickBar"], div[data-testid="stSlider"] [data-testid="stThumbValue"], div[data-testid="stSlider"] * {{
  color: #F9FAFB !important;
  font-weight: 700 !important;
  font-family: 'Space Grotesk', sans-serif !important;
}}

/* 13. Expanders */
div[data-testid="stExpander"] {{
  background-color: #0E1526 !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  border-radius: 8px !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
  margin-bottom: 14px !important;
}}
div[data-testid="stExpander"] summary {{
  color: #F9FAFB !important;
  font-weight: 700 !important;
  font-size: 15px !important;
  font-family: 'Space Grotesk', sans-serif !important;
}}
div[data-testid="stExpander"] summary:hover {{
  background-color: rgba(245, 185, 66, 0.08) !important;
}}
div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {{
  color: #E2E8F0 !important;
  background-color: #0E1526 !important;
}}

/* 14. Alerts, Toasts, and Callouts */
div[data-testid="stAlert"] {{
  background-color: rgba(14, 21, 38, 0.9) !important;
  color: #F9FAFB !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35) !important;
  border-radius: 8px !important;
}}
div[data-testid="stAlert"] * {{
  color: #F9FAFB !important;
}}
div[data-testid="stToast"] {{
  background-color: #0E1526 !important;
  color: #F9FAFB !important;
  border: 1px solid rgba(255, 255, 255, 0.16) !important;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5) !important;
}}
div[data-testid="stToast"] * {{
  color: #F9FAFB !important;
}}

/* 15. File Uploader & Secondary / Download Buttons */
div[data-testid="stFileUploader"] {{
  background-color: #0E1526 !important;
  border: 2px dashed rgba(255, 255, 255, 0.18) !important;
  border-radius: 8px !important;
  padding: 14px !important;
}}
div[data-testid="stFileUploader"] * {{
  color: #F9FAFB !important;
}}


/* 16. Header bar and action menu */
header[data-testid="stHeader"] {{
  background-color: rgba(7, 10, 18, 0.85) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
}}
header[data-testid="stHeader"] button, header[data-testid="stHeader"] svg {{
  color: #F9FAFB !important;
  fill: #F9FAFB !important;
}}
ul[role="menu"], div[role="menu"] {{
  background-color: #0E1526 !important;
  color: #F9FAFB !important;
  border: 1px solid rgba(255, 255, 255, 0.16) !important;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.6) !important;
  border-radius: 8px !important;
}}
li[role="menuitem"], div[role="menuitem"] {{
  color: #F9FAFB !important;
  background-color: #0E1526 !important;
  font-size: 14px !important;
  font-weight: 600 !important;
}}
li[role="menuitem"]:hover, div[role="menuitem"]:hover {{
  background-color: rgba(245, 185, 66, 0.15) !important;
  color: #F5B942 !important;
}}

/* 17. Universal Action Buttons (Matte Yellow with Bold Jet Black Text) */
div.stButton > button,
div.stDownloadButton > button,
div.stFormSubmitButton > button,
div[data-testid="stPopover"] > button,
div[data-testid="stPopoverButton"] > button,
div:not([data-testid="stButtonGroup"]):not([data-baseweb="button-group"]):not([data-testid="stPills"]) > button[kind="primary"],
div:not([data-testid="stButtonGroup"]):not([data-baseweb="button-group"]):not([data-testid="stPills"]) > button[kind="secondary"]:not([role="radio"]):not([role="checkbox"]):not([data-testid*="Active"]),
div:not([data-testid="stButtonGroup"]):not([data-baseweb="button-group"]):not([data-testid="stPills"]) > button[data-testid="stBaseButton-primary"],
div:not([data-testid="stButtonGroup"]):not([data-baseweb="button-group"]):not([data-testid="stPills"]) > button[data-testid="stBaseButton-secondary"]:not([role="radio"]):not([role="checkbox"]):not([data-testid*="Active"]) {{
  background: #EAB308 !important;
  background-color: #EAB308 !important;
  color: #070A12 !important;
  -webkit-text-fill-color: #070A12 !important;
  border: 1.5px solid #CA8A04 !important;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.25) !important;
  border-radius: 6px !important;
  font-weight: 800 !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 13.5px !important;
  padding: 8px 20px !important;
  transition: all 0.15s ease-in-out !important;
  cursor: pointer !important;
}}

/* Force all inner elements of standard action buttons to be crisp, bold jet-black */
div.stButton > button *,
div.stButton > button p,
div.stButton > button span,
div.stButton > button div,
div.stButton > button strong,
div.stButton > button b,
div.stDownloadButton > button *,
div.stDownloadButton > button p,
div.stDownloadButton > button span,
div.stDownloadButton > button div,
div.stFormSubmitButton > button *,
div.stFormSubmitButton > button p,
div.stFormSubmitButton > button span,
div.stFormSubmitButton > button div,
div[data-testid="stPopover"] > button *,
div[data-testid="stPopover"] > button p,
div[data-testid="stPopover"] > button span,
div[data-testid="stPopover"] > button div,
div[data-testid="stPopoverButton"] > button *,
div:not([data-testid="stButtonGroup"]):not([data-baseweb="button-group"]):not([data-testid="stPills"]) > button[kind="primary"] *,
div:not([data-testid="stButtonGroup"]):not([data-baseweb="button-group"]):not([data-testid="stPills"]) > button[kind="secondary"]:not([role="radio"]):not([role="checkbox"]):not([data-testid*="Active"]) *,
div:not([data-testid="stButtonGroup"]):not([data-baseweb="button-group"]):not([data-testid="stPills"]) > button[data-testid="stBaseButton-primary"] *,
div:not([data-testid="stButtonGroup"]):not([data-baseweb="button-group"]):not([data-testid="stPills"]) > button[data-testid="stBaseButton-secondary"]:not([role="radio"]):not([role="checkbox"]):not([data-testid*="Active"]) * {{
  color: #070A12 !important;
  -webkit-text-fill-color: #070A12 !important;
  font-weight: 800 !important;
  fill: #070A12 !important;
}}

/* Button Hover State - Vibrant Matte Lift */
div.stButton > button:hover,
div.stDownloadButton > button:hover,
div.stFormSubmitButton > button:hover,
div[data-testid="stPopover"] > button:hover,
div[data-testid="stPopoverButton"] > button:hover,
div:not([data-testid="stButtonGroup"]):not([data-baseweb="button-group"]):not([data-testid="stPills"]) > button[kind="primary"]:hover,
div:not([data-testid="stButtonGroup"]):not([data-baseweb="button-group"]):not([data-testid="stPills"]) > button[kind="secondary"]:not([role="radio"]):not([role="checkbox"]):hover {{
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3) !important;
  background: #FACC15 !important;
  background-color: #FACC15 !important;
  border-color: #CA8A04 !important;
}}

div.stButton > button:hover *,
div.stDownloadButton > button:hover *,
div.stFormSubmitButton > button:hover *,
div[data-testid="stPopover"] > button:hover *,
div[data-testid="stPopoverButton"] > button:hover *,
div:not([data-testid="stButtonGroup"]):not([data-baseweb="button-group"]):not([data-testid="stPills"]) > button[kind="primary"]:hover *,
div:not([data-testid="stButtonGroup"]):not([data-baseweb="button-group"]):not([data-testid="stPills"]) > button[kind="secondary"]:not([role="radio"]):not([role="checkbox"]):hover * {{
  color: #070A12 !important;
  -webkit-text-fill-color: #070A12 !important;
}}

/* Button Active / Clicked State */
div.stButton > button:active,
div.stDownloadButton > button:active,
div.stFormSubmitButton > button:active,
div[data-testid="stPopover"] > button:active,
div[data-testid="stPopoverButton"] > button:active,
div:not([data-testid="stButtonGroup"]):not([data-baseweb="button-group"]):not([data-testid="stPills"]) > button[kind="primary"]:active,
div:not([data-testid="stButtonGroup"]):not([data-baseweb="button-group"]):not([data-testid="stPills"]) > button[kind="secondary"]:not([role="radio"]):not([role="checkbox"]):active {{
  transform: translateY(1px) !important;
  background: #CA8A04 !important;
  background-color: #CA8A04 !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
}}

/* 17b. Equal Dimensions & No-Wrap for Top Bar Action Popovers (Classic 38px Height) */
div[data-testid="stPopover"],
div[data-testid="stPopoverButton"] {{
  display: flex !important;
  align-items: center !important;
  width: 100% !important;
}}

div[data-testid="stPopover"] > button,
div[data-testid="stPopoverButton"] > button {{
  height: 38px !important;
  min-height: 38px !important;
  max-height: 38px !important;
  line-height: 38px !important;
  width: 100% !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 14px !important;
  box-sizing: border-box !important;
  margin: 0 !important;
  border-radius: 6px !important;
}}

div[data-testid="stPopover"] > button *,
div[data-testid="stPopover"] > button p,
div[data-testid="stPopover"] > button span,
div[data-testid="stPopover"] > button div,
div[data-testid="stPopoverButton"] > button *,
div[data-testid="stPopoverButton"] > button p,
div[data-testid="stPopoverButton"] > button span,
div[data-testid="stPopoverButton"] > button div {{
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  line-height: 1 !important;
  font-size: 13px !important;
  font-weight: 800 !important;
  margin: 0 !important;
  padding: 0 !important;
}}

/* 17c. Sleek, Compact Slate-Grey Buttons inside Popover Menus (Original Website Dropdown Format) */
div[data-testid="stPopoverBody"] div.stButton > button,
div[data-baseweb="popover"] div.stButton > button,
div[data-testid="stPopoverContent"] div.stButton > button,
div[data-testid="stPopoverBody"] button[kind="secondary"],
div[data-testid="stPopoverBody"] button[kind="primary"],
div[data-baseweb="popover"] button[kind="secondary"],
div[data-baseweb="popover"] button[kind="primary"] {{
  background: #1E293B !important;
  background-color: #1E293B !important;
  color: #F1F5F9 !important;
  -webkit-text-fill-color: #F1F5F9 !important;
  border: 1px solid rgba(255, 255, 255, 0.09) !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25) !important;
  border-radius: 6px !important;
  height: 34px !important;
  min-height: 34px !important;
  max-height: 34px !important;
  line-height: 34px !important;
  padding: 0 12px !important;
  margin: 3px 0 !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  text-align: left !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  transition: all 0.15s ease-in-out !important;
  cursor: pointer !important;
  width: 100% !important;
}}

/* Inner text and icons of popover buttons */
div[data-testid="stPopoverBody"] div.stButton > button *,
div[data-testid="stPopoverBody"] div.stButton > button p,
div[data-testid="stPopoverBody"] div.stButton > button span,
div[data-testid="stPopoverBody"] div.stButton > button div,
div[data-baseweb="popover"] div.stButton > button *,
div[data-baseweb="popover"] div.stButton > button p,
div[data-baseweb="popover"] div.stButton > button span,
div[data-baseweb="popover"] div.stButton > button div {{
  color: #F1F5F9 !important;
  -webkit-text-fill-color: #F1F5F9 !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  text-align: left !important;
  justify-content: flex-start !important;
  line-height: 1 !important;
}}

/* Hover state for popover dropdown buttons */
div[data-testid="stPopoverBody"] div.stButton > button:hover,
div[data-baseweb="popover"] div.stButton > button:hover,
div[data-testid="stPopoverContent"] div.stButton > button:hover {{
  background: #334155 !important;
  background-color: #334155 !important;
  border-color: rgba(255, 255, 255, 0.25) !important;
  color: #FFFFFF !important;
  -webkit-text-fill-color: #FFFFFF !important;
  transform: none !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35) !important;
}}

div[data-testid="stPopoverBody"] div.stButton > button:hover *,
div[data-testid="stPopoverBody"] div.stButton > button:hover p,
div[data-testid="stPopoverBody"] div.stButton > button:hover span,
div[data-baseweb="popover"] div.stButton > button:hover * {{
  color: #FFFFFF !important;
  -webkit-text-fill-color: #FFFFFF !important;
}}

/* Selected/Active Language Button in Popover (Kind=Primary) */
div[data-testid="stPopoverBody"] div.stButton > button[kind="primary"],
div[data-testid="stPopoverBody"] div.stButton > button[data-testid="stBaseButton-primary"],
div[data-baseweb="popover"] div.stButton > button[kind="primary"],
div[data-baseweb="popover"] div.stButton > button[data-testid="stBaseButton-primary"] {{
  background: rgba(234, 179, 8, 0.14) !important;
  background-color: rgba(234, 179, 8, 0.14) !important;
  border: 1.5px solid #EAB308 !important;
  color: #FACC15 !important;
  -webkit-text-fill-color: #FACC15 !important;
  font-weight: 700 !important;
}}

div[data-testid="stPopoverBody"] div.stButton > button[kind="primary"] *,
div[data-testid="stPopoverBody"] div.stButton > button[kind="primary"] p,
div[data-testid="stPopoverBody"] div.stButton > button[kind="primary"] span,
div[data-baseweb="popover"] div.stButton > button[kind="primary"] * {{
  color: #FACC15 !important;
  -webkit-text-fill-color: #FACC15 !important;
  font-weight: 700 !important;
}}

/* Ensure the popover popup background is deep dark slate with subtle glassmorphic border */
div[data-testid="stPopoverBody"],
div[data-baseweb="popover"] {{
  background: #0B1120 !important;
  border: 1px solid rgba(255, 255, 255, 0.14) !important;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.65) !important;
  border-radius: 8px !important;
  padding: 12px 14px !important;
}}

/* 18. Modern Glassmorphic Cards */
.editorial-card, .instrument-card {{
  background: rgba(14, 21, 38, 0.75);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
  border-radius: 8px;
  padding: 16px 18px;
  position: relative;
  margin-bottom: 14px;
  min-height: 140px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-sizing: border-box;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}}
.editorial-card:hover, .instrument-card:hover {{
  transform: translateY(-2px);
  border-color: rgba(245, 185, 66, 0.45);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.55), 0 0 16px rgba(245, 185, 66, 0.2);
}}

.instrument-tag {{
  font-family: 'Space Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #94A3B8;
  margin-bottom: 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}}
.instrument-val {{
  font-family: 'Space Grotesk', sans-serif;
  font-size: 26px;
  font-weight: 800;
  color: #F9FAFB;
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
  color: #94A3B8;
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  word-break: break-word;
}}

/* Delta badges */
.delta-pill-bad {{
  background: rgba(244, 63, 94, 0.2);
  color: #FB7185;
  border: 1px solid rgba(244, 63, 94, 0.4);
  padding: 2px 8px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 12px;
}}
.delta-pill-good {{
  background: rgba(16, 185, 129, 0.2);
  color: #34D399;
  border: 1px solid rgba(16, 185, 129, 0.4);
  padding: 2px 8px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 12px;
}}
.delta-pill-neutral {{
  background: rgba(245, 185, 66, 0.2);
  color: #F5B942;
  border: 1px solid rgba(245, 185, 66, 0.4);
  padding: 2px 8px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 12px;
}}

/* 18. Enlarged Editorial Topic Ribbon & Navigation (High-Contrast Universal Visibility) */
div[data-testid="stButtonGroup"],
div.stButtonGroup,
div[data-baseweb="button-group"],
div[data-testid="stPills"],
div[role="radiogroup"] {{
  gap: 10px !important;
  margin-top: 8px !important;
  margin-bottom: 22px !important;
  display: flex !important;
  flex-wrap: wrap !important;
  align-items: center !important;
}}

/* Unselected Navigation Pills - Crystal Clear Pure White on Dark Glass Card */
div[data-testid="stButtonGroup"] button,
div[data-testid="stButtonGroup"] button[aria-checked="false"],
div[data-testid="stButtonGroup"] button:not([aria-checked="true"]):not([data-testid*="Active"]),
div.stButtonGroup button,
div[data-baseweb="button-group"] button,
div[data-testid="stPills"] button,
div[role="radiogroup"] button,
button[data-testid*="stBaseButton-pills"] {{
  background: rgba(15, 23, 42, 0.95) !important;
  background-color: rgba(15, 23, 42, 0.95) !important;
  color: #FFFFFF !important;
  -webkit-text-fill-color: #FFFFFF !important;
  border: 1.5px solid rgba(255, 255, 255, 0.28) !important;
  border-radius: 8px !important;
  font-family: 'Space Grotesk', -apple-system, sans-serif !important;
  font-size: 15px !important;
  font-weight: 700 !important;
  padding: 10px 20px !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
  transition: all 0.18s ease-in-out !important;
  cursor: pointer !important;
  opacity: 1 !important;
}}

/* Force ALL inner elements, text, spans, divs of unselected pills to be Pure White (#FFFFFF) */
div[data-testid="stButtonGroup"] button *,
div[data-testid="stButtonGroup"] button p,
div[data-testid="stButtonGroup"] button span,
div[data-testid="stButtonGroup"] button div,
div[data-testid="stButtonGroup"] button[aria-checked="false"] *,
div[data-testid="stButtonGroup"] button[aria-checked="false"] p,
div[data-testid="stButtonGroup"] button[aria-checked="false"] span,
div[data-testid="stButtonGroup"] button[aria-checked="false"] div,
div.stButtonGroup button *,
div.stButtonGroup button p,
div.stButtonGroup button span,
div.stButtonGroup button div,
div[data-baseweb="button-group"] button *,
div[data-baseweb="button-group"] button p,
div[data-baseweb="button-group"] button span,
div[data-baseweb="button-group"] button div,
div[data-testid="stPills"] button *,
div[data-testid="stPills"] button p,
div[data-testid="stPills"] button span,
div[data-testid="stPills"] button div,
div[role="radiogroup"] button *,
div[role="radiogroup"] button p,
div[role="radiogroup"] button span,
div[role="radiogroup"] button div,
button[data-testid*="stBaseButton-pills"] *,
button[data-testid*="stBaseButton-pills"] p,
button[data-testid*="stBaseButton-pills"] span,
button[data-testid*="stBaseButton-pills"] div {{
  color: #FFFFFF !important;
  -webkit-text-fill-color: #FFFFFF !important;
  font-family: 'Space Grotesk', -apple-system, sans-serif !important;
  font-weight: 700 !important;
  font-size: 15px !important;
  opacity: 1 !important;
}}

/* Hover State on Navigation Pills - Vibrant Matte Yellow Border & Text */
div[data-testid="stButtonGroup"] button:hover,
div.stButtonGroup button:hover,
div[data-baseweb="button-group"] button:hover,
div[data-testid="stPills"] button:hover,
div[role="radiogroup"] button:hover {{
  background: rgba(234, 179, 8, 0.22) !important;
  background-color: rgba(234, 179, 8, 0.22) !important;
  border-color: #EAB308 !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 14px rgba(234, 179, 8, 0.35) !important;
}}

div[data-testid="stButtonGroup"] button:hover *,
div[data-testid="stButtonGroup"] button:hover p,
div[data-testid="stButtonGroup"] button:hover span,
div.stButtonGroup button:hover *,
div[data-baseweb="button-group"] button:hover *,
div[data-testid="stPills"] button:hover *,
div[role="radiogroup"] button:hover * {{
  color: #FACC15 !important;
  -webkit-text-fill-color: #FACC15 !important;
  font-weight: 800 !important;
}}

/* Active / Selected Pill - Solid Matte Yellow with Bold Jet Black Text */
div[data-testid="stButtonGroup"] button[aria-checked="true"],
div[data-testid="stButtonGroup"] button[data-testid*="Active"],
div[data-testid="stButtonGroup"] button[kind*="Active"],
div[data-testid="stButtonGroup"] button[aria-selected="true"],
div[data-testid="stButtonGroup"] button[data-selected="true"],
div.stButtonGroup button[aria-checked="true"],
div.stButtonGroup button[data-testid*="Active"],
div.stButtonGroup button[kind*="Active"],
div[data-baseweb="button-group"] button[aria-checked="true"],
div[data-baseweb="button-group"] button[data-testid*="Active"],
div[data-baseweb="button-group"] button[kind*="Active"],
div[role="radiogroup"] button[aria-checked="true"],
div[role="radiogroup"] button[data-testid*="Active"],
div[role="radiogroup"] button[kind*="Active"],
div[data-testid="stPills"] button[aria-selected="true"],
div[data-testid="stPills"] button[data-selected="true"],
button[data-testid*="stBaseButton-pills"][aria-selected="true"],
button[data-testid*="pillsActive"],
button[data-testid*="secondaryActive"],
button[data-testid*="primaryActive"] {{
  background: #EAB308 !important;
  background-color: #EAB308 !important;
  color: #070A12 !important;
  -webkit-text-fill-color: #070A12 !important;
  border: 2px solid #CA8A04 !important;
  font-weight: 800 !important;
  box-shadow: 0 4px 16px rgba(234, 179, 8, 0.45) !important;
  transform: translateY(-1px) !important;
}}

/* Force all inner elements of active/selected pill to bold jet-black */
div[data-testid="stButtonGroup"] button[aria-checked="true"] *,
div[data-testid="stButtonGroup"] button[aria-checked="true"] p,
div[data-testid="stButtonGroup"] button[aria-checked="true"] span,
div[data-testid="stButtonGroup"] button[aria-checked="true"] div,
div[data-testid="stButtonGroup"] button[data-testid*="Active"] *,
div[data-testid="stButtonGroup"] button[data-testid*="Active"] p,
div[data-testid="stButtonGroup"] button[data-testid*="Active"] span,
div[data-testid="stButtonGroup"] button[data-testid*="Active"] div,
div[data-testid="stButtonGroup"] button[kind*="Active"] *,
div.stButtonGroup button[aria-checked="true"] *,
div.stButtonGroup button[data-testid*="Active"] *,
div.stButtonGroup button[kind*="Active"] *,
div[data-baseweb="button-group"] button[aria-checked="true"] *,
div[data-baseweb="button-group"] button[data-testid*="Active"] *,
div[data-baseweb="button-group"] button[kind*="Active"] *,
div[role="radiogroup"] button[aria-checked="true"] *,
div[role="radiogroup"] button[aria-checked="true"] p,
div[role="radiogroup"] button[aria-checked="true"] span,
div[role="radiogroup"] button[aria-checked="true"] div,
div[role="radiogroup"] button[data-testid*="Active"] *,
div[role="radiogroup"] button[kind*="Active"] *,
div[data-testid="stPills"] button[aria-selected="true"] *,
div[data-testid="stPills"] button[data-selected="true"] *,
button[data-testid*="stBaseButton-pills"][aria-selected="true"] *,
button[data-testid*="pillsActive"] *,
button[data-testid*="secondaryActive"] *,
button[data-testid*="primaryActive"] * {{
  color: #070A12 !important;
  -webkit-text-fill-color: #070A12 !important;
  font-weight: 800 !important;
  font-size: 15px !important;
  fill: #070A12 !important;
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
    """Renders the top navigation bar with brand, links, and status in dark glassmorphism."""
    apply_theme()
    health = db_manager.check_health()
    engine_name = "MYSQL 8.4" if health["dialect"] == "mysql" else "LOCAL CACHE"
    logo_svg = get_brand_logo_svg(width=290, height=48)

    nav_html = f"""<div style="background: rgba(14, 21, 38, 0.85); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); border-radius: 10px; padding: 12px 20px; margin: -0.5rem 0 1.75rem 0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
<div style="display: flex; align-items: center; gap: 14px;">{logo_svg}</div>
<div style="display: flex; align-items: center; gap: 8px; font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 700; flex-wrap: wrap;">
<a href="#ch-01" style="color: #F9FAFB; text-decoration: none; padding: 4px 8px; border-radius: 4px; transition: color 0.15s ease;">Overview</a>
<span style="color: rgba(255, 255, 255, 0.2);">•</span>
<a href="#ch-02" style="color: #F9FAFB; text-decoration: none; padding: 4px 8px; border-radius: 4px;">Production</a>
<span style="color: rgba(255, 255, 255, 0.2);">•</span>
<a href="#ch-03" style="color: #F9FAFB; text-decoration: none; padding: 4px 8px; border-radius: 4px;">Trade</a>
<span style="color: rgba(255, 255, 255, 0.2);">•</span>
<a href="#ch-04" style="color: #F9FAFB; text-decoration: none; padding: 4px 8px; border-radius: 4px;">Fuel Prices</a>
<span style="color: rgba(255, 255, 255, 0.2);">•</span>
<a href="#ch-05" style="color: #F9FAFB; text-decoration: none; padding: 4px 8px; border-radius: 4px;">India Fuel</a>
<span style="color: rgba(255, 255, 255, 0.2);">•</span>
<a href="#ch-06" style="color: #F9FAFB; text-decoration: none; padding: 4px 8px; border-radius: 4px;">Companies</a>
<span style="color: rgba(255, 255, 255, 0.2);">•</span>
<a href="#ch-11" style="color: #F9FAFB; text-decoration: none; padding: 4px 8px; border-radius: 4px;">Data Trust</a>
</div>
<div style="display: flex; align-items: center; gap: 12px;">
<span style="background: rgba(16, 185, 129, 0.18); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 4px 12px; border-radius: 999px; font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 700;">● {engine_name} VERIFIED</span>
<a href="#ch-05" style="background: #EAB308; color: #070A12; border: 1px solid #CA8A04; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.25); padding: 6px 14px; border-radius: 6px; font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 800; text-decoration: none;">EXPLORE MARKETS ↗</a>
</div>
</div>"""
    render_html(nav_html)


# ==============================================================================
# 6. GLOBAL SIGNAL RAIL (HORIZONTAL EDITORIAL STRIP)
# ==============================================================================
def render_signal_rail(signals: List[Dict[str, str]]):
    """Renders a modern dark glass horizontal strip."""
    html_items = []
    for s in signals:
        html_items.append(
            f"""<div style="flex: 1; min-width: 170px; padding: 10px 14px; border-right: 1px solid rgba(255, 255, 255, 0.1); display: flex; flex-direction: column;">
<span style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">{s.get('label', '')}</span>
<span style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 800; color: #F9FAFB; margin-top: 3px;">{s.get('value', '')}</span>
<span style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; color: #64748B; margin-top: 2px;">{s.get('note', '')}</span>
</div>"""
        )
    rail_html = f"""<div style="background: rgba(14, 21, 38, 0.75); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4); border-radius: 8px; padding: 6px 12px; margin-bottom: 1.5rem; display: flex; flex-wrap: wrap; align-items: center;">
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
    """Renders a modern dark glassmorphic card with subtle glow and wrapping text."""
    delta_html = ""
    if delta:
        is_pos = not delta.startswith("-") and delta != "0.0%" and delta != "0.00"
        pill_class = "delta-pill-bad" if (is_pos and delta_is_positive_bad) else ("delta-pill-good" if not is_pos else "delta-pill-neutral")
        arrow = "▲" if is_pos else ("▼" if delta.startswith("-") else "")
        delta_html = f'<span class="{pill_class}">{arrow} {delta}</span>'

    badge_html = f'<span style="background: rgba(245, 185, 66, 0.15); border: 1px solid rgba(245, 185, 66, 0.35); color: {COLOR_AMBER}; font-weight: 800; padding: 1px 7px; border-radius: 4px; font-size: 12px;">{code_badge}</span>' if code_badge else ""
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
    """Renders a modern dark chapter banner with clear numbering, divider, and metadata."""
    action_html = ""
    if action_page_url:
        action_html = f"""<a href="{action_page_url}" style="display: inline-flex; align-items: center; gap: 6px; background: #EAB308; color: #070A12; border: 1px solid #CA8A04; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.25); padding: 6px 14px; border-radius: 6px; font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 800; text-decoration: none; letter-spacing: 0.04em;"><span>{action_label}</span> ↗</a>"""

    header_html = f"""<div id="{anchor_id}" style="margin-top: 3.5rem; margin-bottom: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255, 255, 255, 0.12);">
<div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 14px;">
<div>
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
<span style="background: rgba(245, 185, 66, 0.18); color: #F5B942; border: 1px solid rgba(245, 185, 66, 0.4); padding: 2px 10px; border-radius: 999px; font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase;">CHAPTER {chapter_num}</span>
</div>
<h2 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 800; color: #F9FAFB; letter-spacing: -0.03em; margin: 0; line-height: 1.2;">{title}</h2>
<div style="font-family: 'Space Grotesk', sans-serif; font-size: 14px; color: #94A3B8; margin-top: 6px; max-width: 820px; line-height: 1.5;">{subtitle}</div>
</div>
<div style="display: flex; flex-direction: column; align-items: flex-end; gap: 8px;">
{action_html}
<div style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 700; color: #94A3B8; background: #0E1526; padding: 4px 10px; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 4px;">DATA: {source_tag}</div>
</div>
</div>
</div>"""
    render_html(header_html)


def render_chapter_nav(lang=None):
    """Renders a floating Tubelight horizontal navigation bar for the 11 analytical chapters."""
    from src.localization.i18n import t, get_current_language
    cur_lang = lang or get_current_language()
    chapters = [
        ("01", t("chapter_01_title", cur_lang), "#ch-01"),
        ("02", t("chapter_02_title", cur_lang), "#ch-02"),
        ("03", t("chapter_03_title", cur_lang), "#ch-03"),
        ("04", t("chapter_04_title", cur_lang), "#ch-04"),
        ("05", t("chapter_05_title", cur_lang), "#ch-05"),
        ("06", t("chapter_06_title", cur_lang), "#ch-06"),
        ("07", t("chapter_07_title", cur_lang), "#ch-07"),
        ("08", t("chapter_08_title", cur_lang), "#ch-08"),
        ("09", t("chapter_09_title", cur_lang), "#ch-09"),
        ("10", t("chapter_10_title", cur_lang), "#ch-10"),
        ("11", t("chapter_11_title", cur_lang), "#ch-11")
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
    background: rgba(14, 21, 38, 0.85);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6), 0 0 20px rgba(0, 0, 0, 0.4);
    border-radius: 9999px;
    padding: 6px 12px;
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
    color: #F5B942;
    letter-spacing: 0.05em;
    padding: 6px 12px;
    background: rgba(245, 185, 66, 0.15);
    border: 1px solid rgba(245, 185, 66, 0.35);
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
    color: #94A3B8;
    text-decoration: none;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    background: transparent;
}}
.tubelight-nav-item .ch-badge {{
    background: rgba(255, 255, 255, 0.1);
    color: #F9FAFB;
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
    background: #F5B942;
    border-radius: 9999px;
    transition: all 0.25s ease-out;
    opacity: 0;
}}
.tubelight-nav-item:hover {{
    background: rgba(245, 185, 66, 0.15);
    color: #F9FAFB;
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
    """Returns layout dictionary for Plotly charts matching modern dark glassmorphic styling."""
    theme = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="'Space Grotesk', 'Inter', -apple-system, sans-serif",
            color="#F9FAFB",
            size=13
        ),
        margin=dict(l=20, r=20, t=35, b=20),
        height=height,
        colorway=EDITORIAL_COLORWAY,
        title=dict(
            font=dict(color="#F9FAFB", family="'Space Grotesk', sans-serif", size=16)
        ),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.08)",
            zerolinecolor="rgba(255, 255, 255, 0.12)",
            tickfont=dict(color="#94A3B8", family="'Space Grotesk', sans-serif", size=13),
            title=dict(font=dict(color="#F9FAFB", family="'Space Grotesk', sans-serif", size=14))
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.08)",
            zerolinecolor="rgba(255, 255, 255, 0.12)",
            tickfont=dict(color="#94A3B8", family="'Space Grotesk', sans-serif", size=13),
            title=dict(font=dict(color="#F9FAFB", family="'Space Grotesk', sans-serif", size=14))
        ),
        legend=dict(
            bgcolor="rgba(14, 21, 38, 0.8)",
            bordercolor="rgba(255, 255, 255, 0.12)",
            borderwidth=1,
            font=dict(color="#F9FAFB", family="'Space Grotesk', sans-serif", size=13)
        ),
        hoverlabel=dict(
            bgcolor="#0E1526",
            bordercolor="rgba(255, 255, 255, 0.2)",
            font=dict(color="#F9FAFB", family="'Space Grotesk', sans-serif", size=13)
        )
    )
    return deep_merge(theme, overrides)


def apply_atlas_theme(fig, height: int = 460, **kwargs):
    """Safely applies dark styling to a Plotly figure without duplicate keyword collisions."""
    return apply_clean_layout(fig, height=height, **kwargs)


def render_page_header(title: str, subtitle: str, source_tag: str, observation_date: str):
    """Renders a modern dark glass page banner for drill-down pages."""
    apply_theme()
    header_html = f"""<div style="background: rgba(14, 21, 38, 0.8); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4); border-radius: 8px; padding: 22px 26px; margin-bottom: 24px;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
<div>
<h1 style="font-size: 30px; margin: 0; color: #F9FAFB;">{title}</h1>
<p style="font-size: 14px; color: #94A3B8; margin-top: 4px; margin-bottom: 0;">{subtitle}</p>
</div>
<div style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; color: #94A3B8; text-align: right;">
<div><b style="color: #F9FAFB;">SOURCE:</b> {source_tag}</div>
<div><b style="color: #F9FAFB;">OBSERVED:</b> {observation_date}</div>
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
