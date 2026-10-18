"""
GLOBAL FUELPULSE AI — EDITORIAL DESIGN SYSTEM & UI COMPONENTS
Premium Modern Energy Intelligence & Glassmorphic Layout Language.
Visual identity: Deep Obsidian (#070A12), Dark Glass (#0E1526),
Crisp White Typography (#F9FAFB), and Petroleum Amber (#F5B942).
"""

import streamlit as st
import pandas as pd
import textwrap
import urllib.parse
from typing import Optional, Dict, Any, List, Tuple
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


# ==============================================================================
# 3b. NEWS GLOBE ICON (BROADCAST-STYLE VECTOR EMBLEM)
# ==============================================================================
def get_news_globe_icon_svg(size: int = 24) -> str:
    """
    Returns the vector News Globe icon: vibrant cyan/sky-blue globe sphere with crisp
    white coordinate grid lines and a horizontal red banner labeled 'NEWS' with folded
    crimson 3D tails. Matches the international broadcast news emblem aesthetic.
    """
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Left Ribbon Back Fold -->
  <path d="M 10 50 C 10 59 18 64 22 64 L 22 52 Z" fill="#9F1239" />
  <!-- Right Ribbon Back Fold -->
  <path d="M 90 50 C 90 59 82 64 78 64 L 78 52 Z" fill="#9F1239" />

  <!-- Globe Sphere -->
  <circle cx="50" cy="50" r="34" fill="#38BDF8" />

  <!-- Globe Coordinate Grid Lines -->
  <line x1="50" y1="16" x2="50" y2="84" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round" />
  <line x1="16" y1="50" x2="84" y2="50" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round" />
  <path d="M 23 34 Q 50 42 77 34" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" />
  <path d="M 23 66 Q 50 58 77 66" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" />
  <path d="M 50 16 C 34 16 28 32 28 50 C 28 68 34 84 50 84" fill="none" stroke="#FFFFFF" stroke-width="2.2" />
  <path d="M 50 16 C 66 16 72 32 72 50 C 72 68 66 84 50 84" fill="none" stroke="#FFFFFF" stroke-width="2.2" />
  <circle cx="50" cy="50" r="34" fill="none" stroke="#0284C7" stroke-width="1.8" />

  <!-- Ribbon Side Folds Under (Dark Crimson) -->
  <path d="M 16 58 C 14 62 16 66 22 66 L 22 58 Z" fill="#881337" />
  <path d="M 84 58 C 86 62 84 66 78 66 L 78 58 Z" fill="#881337" />

  <!-- Central Red NEWS Banner -->
  <rect x="14" y="37" width="72" height="26" rx="4" fill="#EF4444" />

  <!-- Text: NEWS -->
  <text x="50" y="55.5" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-weight="900" font-size="16" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">NEWS</text>
</svg>"""


def get_news_globe_icon_data_uri(size: int = 36) -> str:
    """Returns an optimized URL-encoded data URI of the News Globe SVG icon for CSS pseudo-elements."""
    svg = get_news_globe_icon_svg(size)
    compact_svg = " ".join(line.strip() for line in svg.splitlines() if line.strip())
    return "data:image/svg+xml," + urllib.parse.quote(compact_svg)


# ==============================================================================
# 3c. COHESIVE LUCIDE VECTOR ICON SYSTEM
# ==============================================================================
LUCIDE_ICON_PATHS: Dict[str, str] = {
    "layout-dashboard": '<rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>',
    "chart-no-axes-combined": '<path d="M12 16v5"/><path d="M16 14v7"/><path d="M20 10v11"/><path d="m22 3-8.646 8.646a.5.5 0 0 1-.708 0L9.354 8.354a.5.5 0 0 0-.707 0L2 15"/><path d="M4 18v3"/><path d="M8 14v7"/>',
    "map-pinned": '<path d="M18 8c0 4.5-6 9-6 9s-6-4.5-6-9a6 6 0 0 1 12 0"/><circle cx="12" cy="8" r="2"/><path d="M8.835 14H5a1 1 0 0 0-.9.56l-1.9 3.8A1 1 0 0 0 3.1 20h17.8a1 1 0 0 0 .9-1.64l-1.9-3.8a1 1 0 0 0-.9-.56h-3.835"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "workflow": '<rect width="8" height="8" x="3" y="3" rx="2"/><path d="M7 11v4a2 2 0 0 0 2 2h4"/><rect width="8" height="8" x="13" y="13" rx="2"/>',
    "layers": '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
    "shield-check": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "flask-conical": '<path d="M10 2v7.527a2 2 0 0 1-.211.896L4.72 20.55a1 1 0 0 0 .9 1.45h12.76a1 1 0 0 0 .9-1.45l-5.069-10.127A2 2 0 0 1 14 9.527V2"/><path d="M8.5 2h7"/><path d="M7 16h10"/>',
    "route": '<circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/>',
    "book-open": '<path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/>',
    "languages": '<path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/>',
    "newspaper": '<path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/><path d="M18 14h-8"/><path d="M15 18h-5"/><path d="M10 6h8v4h-8V6Z"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/><path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"/>',
    "activity": '<path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.48 12H2"/>',
    "sparkles": '<path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>',
    "droplet": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "refresh-cw": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "external-link": '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
    "landmark": '<line x1="3" x2="21" y1="22" y2="22"/><line x1="6" x2="6" y1="18" y2="11"/><line x1="10" x2="10" y1="18" y2="11"/><line x1="14" x2="14" y1="18" y2="11"/><line x1="18" x2="18" y1="18" y2="11"/><polygon points="12 2 20 7 4 7"/>',
    "bot": '<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/>',
    "fuel": '<line x1="3" x2="15" y1="22" y2="22"/><line x1="4" x2="14" y1="9" y2="9"/><path d="M14 22V4a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v18"/><path d="M14 13h2a2 2 0 0 1 2 2v2a2 2 0 0 0 2 2a2 2 0 0 0 2-2V9.83a2 2 0 0 0-.59-1.42L18 5"/>',
    "ship": '<path d="M2 21c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1 .6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M19.38 20A11.6 11.6 0 0 0 21 14l-9-4-9 4c0 2.9.94 5.34 2.81 7.76"/><path d="M19 13V7a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v6"/><line x1="12" x2="12" y1="2" y2="5"/>',
    "brain": '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"/><path d="M12 18v-5"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>'
}


def get_lucide_icon_svg(
    name: str,
    size: int = 18,
    color: str = "currentColor",
    stroke_width: float = 2.0,
    class_name: str = ""
) -> str:
    """Returns an accessible, pure-SVG vector element matching Lucide React icons."""
    clean_name = name.lower().strip().replace("_", "-")
    path_data = LUCIDE_ICON_PATHS.get(clean_name, LUCIDE_ICON_PATHS.get("activity", ""))
    cls_attr = f' class="{class_name}"' if class_name else ''
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" '
        f'stroke-linejoin="round"{cls_attr} style="vertical-align: -2px; display: inline-block; flex-shrink: 0;">'
        f'{path_data}</svg>'
    )


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


def render_app_header_brand_html(current_lang: str, engine_name: str, live_text: str) -> str:
    """Renders the balanced, unified top application header bar with Lucide vector icons."""
    from src.localization.i18n import t
    brand_sub = t('brand_subtitle', current_lang)
    db_icon = get_lucide_icon_svg("database", size=13, color="#34D399")
    act_icon = get_lucide_icon_svg("activity", size=13, color="#F5B942")
    logo_svg = get_logo_mark_svg(size=38)
    return f"""
    <div class="fuelpulse-header-bar">
        <div style="display: flex; align-items: center; gap: 12px; flex-shrink: 0;">
            {logo_svg}
            <div>
                <div style="display: flex; align-items: center; gap: 8px; line-height: 1.25;">
                    <span style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 1.22rem; font-weight: 800; letter-spacing: -0.01em; color: #FFFFFF; text-transform: uppercase; white-space: nowrap;">
                        GLOBAL FUELPULSE
                    </span>
                    <span style="background: #EAB308; color: #070A12; font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem; font-weight: 900; padding: 2px 7px; border-radius: 4px; letter-spacing: 0.05em; display: inline-block;">
                        AI
                    </span>
                </div>
                <div style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 0.65rem; font-weight: 700; color: #94A3B8; letter-spacing: 0.12em; text-transform: uppercase; margin-top: 3px; white-space: nowrap;">
                    {brand_sub}
                </div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 8px; flex-shrink: 0;">
            <span class="fuelpulse-status-pill fuelpulse-status-emerald">
                {db_icon}
                <span>{engine_name}</span>
            </span>
            <span class="fuelpulse-status-pill fuelpulse-status-amber">
                {act_icon}
                <span>{live_text}</span>
            </span>
        </div>
    </div>
    """


def render_two_tier_nav_html(current_lang: str, active_canonical: str) -> str:
    """Renders the structured two-tier navigation system with Lucide vector icons."""
    from src.localization.i18n import get_clean_nav_label

    tier_1_items = [
        {"tab": "home", "icon": "layout-dashboard", "label": get_clean_nav_label("home", current_lang)},
        {"tab": "dashboard", "icon": "chart-no-axes-combined", "label": get_clean_nav_label("dashboard", current_lang), "badge": "Live"},
        {"tab": "india", "icon": "map-pinned", "label": get_clean_nav_label("india", current_lang), "badge": "MoPNG"},
        {"tab": "about", "icon": "info", "label": get_clean_nav_label("about", current_lang)},
        {"tab": "how_it_works", "icon": "workflow", "label": get_clean_nav_label("how_it_works", current_lang)},
    ]

    tier_2_items = [
        {"tab": "features", "icon": "layers", "label": get_clean_nav_label("features", current_lang), "badge": "12 Mod"},
        {"tab": "data_trust", "icon": "shield-check", "label": get_clean_nav_label("data_trust", current_lang), "badge": "SLA"},
        {"tab": "methodology", "icon": "flask-conical", "label": get_clean_nav_label("methodology", current_lang)},
        {"tab": "roadmap", "icon": "route", "label": get_clean_nav_label("roadmap", current_lang), "badge": "2026"},
        {"tab": "faq", "icon": "book-open", "label": get_clean_nav_label("faq", current_lang), "badge": "Docs"},
    ]

    def render_tier_bar(items, tier_title):
        links = []
        for it in items:
            is_active = (it["tab"] == active_canonical)
            active_cls = " active" if is_active else ""
            icon_color = "#F5B942" if is_active else "#94A3B8"
            icon_svg = get_lucide_icon_svg(it["icon"], size=15, color=icon_color)
            badge_html = f'<span class="fuelpulse-nav-badge">{it["badge"]}</span>' if it.get("badge") else ''
            links.append(
                f'<a href="?tab={it["tab"]}&lang={current_lang}" target="_self" class="fuelpulse-nav-link{active_cls}">'
                f'{icon_svg}<span>{it["label"]}</span>{badge_html}</a>'
            )
        return (
            f'<div class="fuelpulse-nav-tier">'
            f'<span class="fuelpulse-nav-tier-label">{tier_title}</span>'
            f'{"".join(links)}'
            f'</div>'
        )

    t1 = render_tier_bar(tier_1_items, "CORE")
    t2 = render_tier_bar(tier_2_items, "SPECS")
    return f'<div class="fuelpulse-nav-shell">{t1}{t2}</div>'



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

/* 0. Responsive Centered Layout Container (1360px max-width, zero horizontal overflow) */
.block-container {{
  max-width: 1360px !important;
  margin-left: auto !important;
  margin-right: auto !important;
  padding-top: 1.25rem !important;
  padding-bottom: 2.5rem !important;
  padding-left: 24px !important;
  padding-right: 24px !important;
  box-sizing: border-box !important;
}}

@media (max-width: 1024px) {{
  .block-container {{
    padding-left: 18px !important;
    padding-right: 18px !important;
    padding-top: 1.15rem !important;
  }}
}}

@media (max-width: 768px) {{
  .block-container {{
    padding-left: 12px !important;
    padding-right: 12px !important;
    padding-top: 1.0rem !important;
  }}
}}

/* Universal Pinned Floating Action Button (FAB) */
div[class*="global_fuelpulse_fab"] button,
div[data-testid*="global_fuelpulse_fab"] button {{
  position: fixed !important;
  bottom: 24px !important;
  right: 24px !important;
  z-index: 999999 !important;
  width: 58px !important;
  height: 58px !important;
  min-width: 58px !important;
  max-width: 58px !important;
  min-height: 58px !important;
  max-height: 58px !important;
  border-radius: 50% !important;
  padding: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: linear-gradient(135deg, #F5B942 0%, #D97706 100%) !important;
  color: #0F172A !important;
  border: 2px solid rgba(255, 255, 255, 0.75) !important;
  box-shadow: 0 8px 24px rgba(245, 185, 66, 0.45), 0 4px 12px rgba(0, 0, 0, 0.6) !important;
  font-size: 26px !important;
  line-height: 1 !important;
  cursor: pointer !important;
  transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.25s ease !important;
}}

div[class*="global_fuelpulse_fab"] button:hover,
div[data-testid*="global_fuelpulse_fab"] button:hover {{
  transform: scale(1.12) !important;
  box-shadow: 0 12px 32px rgba(245, 185, 66, 0.65), 0 6px 16px rgba(0, 0, 0, 0.8) !important;
}}

div[class*="global_fuelpulse_fab"] button:active,
div[data-testid*="global_fuelpulse_fab"] button:active {{
  transform: scale(0.94) !important;
}}

@media (max-width: 768px) {{
  div[class*="global_fuelpulse_fab"] button,
  div[data-testid*="global_fuelpulse_fab"] button {{
    bottom: 18px !important;
    right: 18px !important;
  }}
}}

/* Universal Header & Action Bar Container */
.fuelpulse-header-bar {{
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  background: rgba(14, 21, 38, 0.90) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  border-radius: 10px !important;
  padding: 8px 16px !important;
  margin-top: 0 !important;
  margin-bottom: 12px !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
  gap: 14px !important;
  flex-wrap: nowrap !important;
  overflow: visible !important;
  box-sizing: border-box !important;
}}

.fuelpulse-status-pill {{
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  padding: 3px 9px !important;
  border-radius: 999px !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  letter-spacing: 0.04em !important;
  line-height: 1 !important;
}}

.fuelpulse-status-emerald {{
  background: rgba(16, 185, 129, 0.16) !important;
  color: #34D399 !important;
  border: 1px solid rgba(16, 185, 129, 0.35) !important;
}}

.fuelpulse-status-amber {{
  background: rgba(245, 185, 66, 0.16) !important;
  color: #F5B942 !important;
  border: 1px solid rgba(245, 185, 66, 0.35) !important;
}}

/* Structured Two-Tier Navigation System */
.fuelpulse-nav-shell {{
  display: flex !important;
  flex-direction: column !important;
  gap: 5px !important;
  margin-bottom: 16px !important;
  width: 100% !important;
}}

.fuelpulse-nav-tier {{
  display: flex !important;
  align-items: center !important;
  gap: 4px !important;
  flex-wrap: nowrap !important;
  overflow-x: auto !important;
  scrollbar-width: none !important;
  -ms-overflow-style: none !important;
  background: rgba(11, 17, 32, 0.75) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 8px !important;
  padding: 3px 6px !important;
}}

.fuelpulse-nav-tier::-webkit-scrollbar {{
  display: none !important;
}}

.fuelpulse-nav-link {{
  display: inline-flex !important;
  align-items: center !important;
  gap: 5px !important;
  height: 30px !important;
  padding: 0 9px !important;
  border-radius: 5px !important;
  font-family: 'Space Grotesk', -apple-system, sans-serif !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  color: #94A3B8 !important;
  text-decoration: none !important;
  transition: all 0.15s ease-in-out !important;
  border: 1px solid transparent !important;
  white-space: nowrap !important;
  cursor: pointer !important;
}}

.fuelpulse-nav-link:hover {{
  background: rgba(255, 255, 255, 0.06) !important;
  color: #F9FAFB !important;
  border-color: rgba(255, 255, 255, 0.12) !important;
}}

.fuelpulse-nav-link.active {{
  background: rgba(234, 179, 8, 0.12) !important;
  color: #F5B942 !important;
  border-color: rgba(234, 179, 8, 0.45) !important;
  font-weight: 700 !important;
  box-shadow: 0 0 10px rgba(234, 179, 8, 0.12) !important;
}}

.fuelpulse-nav-tier-label {{
  font-size: 9px !important;
  font-weight: 800 !important;
  color: #64748B !important;
  text-transform: uppercase !important;
  letter-spacing: 0.06em !important;
  padding: 0 6px !important;
  user-select: none !important;
  opacity: 0.8 !important;
}}

.fuelpulse-nav-badge {{
  display: inline-flex !important;
  align-items: center !important;
  height: 15px !important;
  padding: 0 4px !important;
  border-radius: 3px !important;
  font-size: 9.5px !important;
  font-weight: 700 !important;
  background: rgba(234, 179, 8, 0.16) !important;
  color: #F5B942 !important;
  border: 1px solid rgba(234, 179, 8, 0.32) !important;
  margin-left: 3px !important;
  line-height: 1 !important;
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
div[data-testid="stDecoration"] {{
  display: none !important;
}}
header[data-testid="stHeader"] {{
  height: 2.875rem !important;
  min-height: 2.875rem !important;
  max-height: 2.875rem !important;
  padding: 0 1rem !important;
  margin: 0 !important;
  top: 0 !important;
  background: transparent !important;
  background-color: transparent !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  border-bottom: none !important;
  pointer-events: none !important;
  z-index: 999990 !important;
}}
header[data-testid="stHeader"] * {{
  pointer-events: auto !important;
}}
header[data-testid="stHeader"] [data-testid="stToolbar"] {{
  top: 0 !important;
  right: 1rem !important;
  height: 2.875rem !important;
  display: flex !important;
  align-items: center !important;
  visibility: visible !important;
  opacity: 1 !important;
  overflow: visible !important;
}}
header[data-testid="stHeader"] button,
header[data-testid="stHeader"] svg,
header[data-testid="stHeader"] [data-testid="stToolbar"],
header[data-testid="stHeader"] [data-testid="stSidebarCollapsedControl"],
header[data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] {{
  pointer-events: auto !important;
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

/* 17. Professional SaaS Button & Popover Design System */

/* A. Popover Trigger Buttons (Header: Language & Live News) */
div[data-testid="stPopover"],
div[data-testid="stPopoverButton"] {{
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 100% !important;
  background: transparent !important;
  background-color: transparent !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
  padding: 0 !important;
  margin: 0 !important;
}}

div[data-testid="stPopover"] > button,
div[data-testid="stPopoverButton"] > button,
button[key*="top_ai_assistant_btn"],
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button,
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopover"] > button {{
  background: rgba(14, 21, 38, 0.90) !important;
  background-color: rgba(14, 21, 38, 0.90) !important;
  color: #F9FAFB !important;
  -webkit-text-fill-color: #F9FAFB !important;
  border: 1px solid rgba(255, 255, 255, 0.16) !important;
  border-radius: 8px !important;
  height: 38px !important;
  min-height: 38px !important;
  max-height: 38px !important;
  line-height: 38px !important;
  padding: 0 10px !important;
  font-family: 'Space Grotesk', -apple-system, sans-serif !important;
  font-size: 12px !important;
  font-weight: 700 !important;
  white-space: nowrap !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 6px !important;
  transition: all 0.15s ease-in-out !important;
  cursor: pointer !important;
  width: 100% !important;
  box-sizing: border-box !important;
}}

div[data-testid="stPopover"] > button *,
div[data-testid="stPopover"] > button p,
div[data-testid="stPopover"] > button span,
div[data-testid="stPopoverButton"] > button *,
div[data-testid="stPopoverButton"] > button p,
div[data-testid="stPopoverButton"] > button span,
button[key*="top_ai_assistant_btn"] *,
button[key*="top_ai_assistant_btn"] p,
button[key*="top_ai_assistant_btn"] span {{
  color: #F9FAFB !important;
  -webkit-text-fill-color: #F9FAFB !important;
  font-size: 12px !important;
  font-weight: 700 !important;
  white-space: nowrap !important;
  line-height: 1 !important;
  margin: 0 !important;
  padding: 0 !important;
}}

/* AI Assistant Header Button: Subtle golden border and glowing indicator matching popover form */
button[key*="top_ai_assistant_btn"] {{
  border: 1px solid rgba(245, 185, 66, 0.45) !important;
  background: rgba(245, 185, 66, 0.08) !important;
  color: #F5B942 !important;
  -webkit-text-fill-color: #F5B942 !important;
}}

button[key*="top_ai_assistant_btn"] *,
button[key*="top_ai_assistant_btn"] p,
button[key*="top_ai_assistant_btn"] span {{
  color: #F5B942 !important;
  -webkit-text-fill-color: #F5B942 !important;
}}

div[data-testid="stPopover"] > button:hover,
div[data-testid="stPopoverButton"] > button:hover,
button[key*="top_ai_assistant_btn"]:hover,
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button:hover {{
  background: rgba(245, 185, 66, 0.14) !important;
  background-color: rgba(245, 185, 66, 0.14) !important;
  border-color: rgba(245, 185, 66, 0.6) !important;
  color: #F5B942 !important;
  -webkit-text-fill-color: #F5B942 !important;
  transform: translateY(-1px) !important;
}}

div[data-testid="stPopover"] > button:hover *,
div[data-testid="stPopoverButton"] > button:hover *,
button[key*="top_ai_assistant_btn"]:hover * {{
  color: #F5B942 !important;
  -webkit-text-fill-color: #F5B942 !important;
}}

div[data-testid="stPopover"] > button svg,
div[data-testid="stPopoverButton"] > button svg {{
  fill: #F5B942 !important;
  color: #F5B942 !important;
}}

/* B. Popover Dropdown Container & Menu Items (Language selector & News Wire) */
div[data-testid="stPopoverBody"],
div[data-baseweb="popover"],
div[data-testid="stPopoverContent"] {{
  background: #0B1120 !important;
  border: 1px solid rgba(255, 255, 255, 0.14) !important;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.65) !important;
  border-radius: 8px !important;
}}

div[data-testid="stPopoverBody"] div.stButton > button,
div[data-baseweb="popover"] div.stButton > button,
div[data-testid="stPopoverContent"] div.stButton > button {{
  background: #111A2E !important;
  background-color: #111A2E !important;
  color: #E2E8F0 !important;
  -webkit-text-fill-color: #E2E8F0 !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 5px !important;
  height: 32px !important;
  min-height: 32px !important;
  max-height: 32px !important;
  line-height: 32px !important;
  padding: 0 10px !important;
  margin: 2px 0 !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  font-family: 'Space Grotesk', -apple-system, sans-serif !important;
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  text-align: left !important;
  white-space: nowrap !important;
  box-shadow: none !important;
  transition: all 0.12s ease !important;
  width: 100% !important;
  cursor: pointer !important;
}}

div[data-testid="stPopoverBody"] div.stButton > button *,
div[data-baseweb="popover"] div.stButton > button *,
div[data-testid="stPopoverContent"] div.stButton > button * {{
  color: #E2E8F0 !important;
  -webkit-text-fill-color: #E2E8F0 !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  white-space: nowrap !important;
  line-height: 1 !important;
}}

div[data-testid="stPopoverBody"] div.stButton > button:hover,
div[data-baseweb="popover"] div.stButton > button:hover,
div[data-testid="stPopoverContent"] div.stButton > button:hover {{
  background: rgba(245, 185, 66, 0.14) !important;
  background-color: rgba(245, 185, 66, 0.14) !important;
  border-color: rgba(245, 185, 66, 0.4) !important;
  color: #F5B942 !important;
  -webkit-text-fill-color: #F5B942 !important;
  transform: none !important;
}}

div[data-testid="stPopoverBody"] div.stButton > button:hover *,
div[data-baseweb="popover"] div.stButton > button:hover *,
div[data-testid="stPopoverContent"] div.stButton > button:hover * {{
  color: #F5B942 !important;
  -webkit-text-fill-color: #F5B942 !important;
}}

div[data-testid="stPopoverBody"] div.stButton > button[kind="primary"],
div[data-baseweb="popover"] div.stButton > button[kind="primary"],
div[data-testid="stPopoverContent"] div.stButton > button[kind="primary"] {{
  background: rgba(245, 185, 66, 0.22) !important;
  background-color: rgba(245, 185, 66, 0.22) !important;
  border: 1px solid rgba(245, 185, 66, 0.5) !important;
  color: #F5B942 !important;
  -webkit-text-fill-color: #F5B942 !important;
  font-weight: 700 !important;
}}

div[data-testid="stPopoverBody"] div.stButton > button[kind="primary"] *,
div[data-baseweb="popover"] div.stButton > button[kind="primary"] *,
div[data-testid="stPopoverContent"] div.stButton > button[kind="primary"] * {{
  color: #F5B942 !important;
  -webkit-text-fill-color: #F5B942 !important;
  font-weight: 700 !important;
}}

/* C. Secondary Action Buttons & Suggested Query Chips */
div:not([data-testid="stPopoverBody"]):not([data-baseweb="popover"]):not([data-testid="stPopoverContent"]) > div.stButton > button[kind="secondary"],
div:not([data-testid="stPopoverBody"]):not([data-baseweb="popover"]):not([data-testid="stPopoverContent"]) > div.stButton > button[data-testid="stBaseButton-secondary"]:not([role="radio"]):not([role="checkbox"]):not([data-testid*="Active"]),
button[kind="secondary"]:not([data-testid="stBaseButton-primary"]):not([role="radio"]):not([role="checkbox"]) {{
  background: rgba(14, 21, 38, 0.75) !important;
  background-color: rgba(14, 21, 38, 0.75) !important;
  color: #E2E8F0 !important;
  -webkit-text-fill-color: #E2E8F0 !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  border-radius: 6px !important;
  font-family: 'Space Grotesk', -apple-system, sans-serif !important;
  font-size: 11.5px !important;
  font-weight: 600 !important;
  height: 32px !important;
  min-height: 32px !important;
  padding: 0 10px !important;
  white-space: nowrap !important;
  text-overflow: ellipsis !important;
  overflow: hidden !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25) !important;
  transition: all 0.15s ease-in-out !important;
  cursor: pointer !important;
}}

div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[kind="secondary"] *,
div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[data-testid="stBaseButton-secondary"] * {{
  color: #E2E8F0 !important;
  -webkit-text-fill-color: #E2E8F0 !important;
  font-size: 11.5px !important;
  font-weight: 600 !important;
  white-space: nowrap !important;
}}

div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[kind="secondary"]:hover,
div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[data-testid="stBaseButton-secondary"]:hover {{
  background: rgba(245, 185, 66, 0.12) !important;
  background-color: rgba(245, 185, 66, 0.12) !important;
  border-color: rgba(245, 185, 66, 0.45) !important;
  color: #F5B942 !important;
  -webkit-text-fill-color: #F5B942 !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.35) !important;
}}

div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[kind="secondary"]:hover *,
div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[data-testid="stBaseButton-secondary"]:hover * {{
  color: #F5B942 !important;
  -webkit-text-fill-color: #F5B942 !important;
}}

/* D. Primary Action Buttons (Key CTA & Ingestion Trigger Buttons) */
div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[kind="primary"],
div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[data-testid="stBaseButton-primary"],
div.stDownloadButton > button,
div.stFormSubmitButton > button {{
  background: #EAB308 !important;
  background-color: #EAB308 !important;
  color: #070A12 !important;
  -webkit-text-fill-color: #070A12 !important;
  border: 1px solid #CA8A04 !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25) !important;
  border-radius: 6px !important;
  font-weight: 700 !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 12.5px !important;
  height: 34px !important;
  min-height: 34px !important;
  padding: 0 14px !important;
  transition: all 0.15s ease-in-out !important;
  cursor: pointer !important;
  white-space: nowrap !important;
}}

div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[kind="primary"] *,
div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[data-testid="stBaseButton-primary"] *,
div.stDownloadButton > button *,
div.stFormSubmitButton > button * {{
  color: #070A12 !important;
  -webkit-text-fill-color: #070A12 !important;
  font-weight: 700 !important;
  font-size: 12.5px !important;
  white-space: nowrap !important;
}}

div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[kind="primary"]:hover,
div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[data-testid="stBaseButton-primary"]:hover,
div.stDownloadButton > button:hover,
div.stFormSubmitButton > button:hover {{
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3) !important;
  background: #FACC15 !important;
  background-color: #FACC15 !important;
  border-color: #CA8A04 !important;
}}

div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[kind="primary"]:active,
div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[data-testid="stBaseButton-primary"]:active {{
  transform: translateY(1px) !important;
  background: #CA8A04 !important;
  background-color: #CA8A04 !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
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

/* ==============================================================================
   19. COMPREHENSIVE MOBILE RESPONSIVE ENGINE (<= 768px & <= 480px, Desktop Untouched)
   ============================================================================== */
@media (max-width: 768px) {{
  /* A. Mobile Container & Typography Scaling */
  .block-container {{
    padding-left: 10px !important;
    padding-right: 10px !important;
    padding-top: 2.2rem !important;
    padding-bottom: 2rem !important;
  }}

  h1 {{ font-size: 22px !important; line-height: 1.2 !important; }}
  h2 {{ font-size: 18px !important; line-height: 1.25 !important; }}
  h3, h4 {{ font-size: 15px !important; line-height: 1.3 !important; }}
  p, span, label {{ font-size: 13px !important; }}

  /* B. Universal 2-Column Responsive Grid for Multi-Column Blocks */
  [data-testid="stHorizontalBlock"] {{
    display: grid !important;
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    gap: 8px !important;
    width: 100% !important;
  }}

  [data-testid="stHorizontalBlock"] > [data-testid="column"],
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
    width: 100% !important;
    min-width: 0 !important;
    flex: unset !important;
  }}

  /* C. Hide Empty Centering / Spacer Columns on Mobile */
  [data-testid="column"]:empty,
  [data-testid="stColumn"]:empty {{
    display: none !important;
  }}

  /* D. Odd Last Column Foundation Span (e.g. 3rd card or 5th AI query button) */
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child:nth-child(odd):not(:first-child),
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child:nth-child(odd):not(:first-child) {{
    grid-column: 1 / -1 !important;
  }}

  /* E. Charts, Dataframes, Tables, and Heavy Visuals Span Full Width */
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:has(.js-plotly-plot),
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:has(.js-plotly-plot),
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:has([data-testid="stPlotlyChart"]),
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:has([data-testid="stPlotlyChart"]),
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:has([data-testid="stDataFrame"]),
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:has([data-testid="stDataFrame"]),
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:has(table),
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:has(table),
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:has(iframe),
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:has(iframe),
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:has(form),
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:has(form),
  [data-testid="stHorizontalBlock"] > [data-testid="column"]:has(.fuelpulse-hero-backdrop),
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:has(.fuelpulse-hero-backdrop) {{
    grid-column: 1 / -1 !important;
  }}

  /* F. Top Header Bar: 3-column mobile grid: Brand full width on Row 1, AI, Language & News side-by-side on Row 2 */
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) {{
    display: grid !important;
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    gap: 6px !important;
    width: 100% !important;
  }}

  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) > [data-testid="column"]:first-child,
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) > [data-testid="stColumn"]:first-child {{
    grid-column: 1 / -1 !important;
  }}

  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) > [data-testid="column"]:not(:first-child),
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) > [data-testid="stColumn"]:not(:first-child) {{
    grid-column: span 1 !important;
    width: 100% !important;
    min-width: 0 !important;
  }}

  .fuelpulse-header-bar {{
    padding: 8px 10px !important;
    gap: 8px !important;
    margin-bottom: 6px !important;
  }}

  /* Compact button dimensions and font sizes on mobile to guarantee 1-line fit */
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button,
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopover"] > button,
  button[key*="top_ai_assistant_btn"] {{
    min-height: 35px !important;
    max-height: 35px !important;
    line-height: 35px !important;
    padding: 0 4px !important;
    font-size: 11px !important;
    border-radius: 7px !important;
  }}

  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button *,
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopover"] > button *,
  button[key*="top_ai_assistant_btn"] * {{
    font-size: 11px !important;
  }}

  /* G. Compact Metric & Instrument Cards */
  .editorial-card, .instrument-card {{
    min-height: 84px !important;
    padding: 10px 12px !important;
    margin-bottom: 6px !important;
  }}

  .instrument-tag {{
    font-size: 10.5px !important;
    margin-bottom: 4px !important;
  }}

  .instrument-val {{
    font-size: 19px !important;
    line-height: 1.15 !important;
  }}

  .instrument-sub {{
    font-size: 10.5px !important;
    margin-top: 4px !important;
    gap: 4px !important;
  }}

  /* H. Global Signal Rail Grid Transformation */
  .fuelpulse-signal-rail {{
    display: grid !important;
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    gap: 8px !important;
    padding: 8px 10px !important;
    margin-bottom: 1rem !important;
  }}

  .fuelpulse-signal-item {{
    min-width: 0 !important;
    flex: unset !important;
    border-right: none !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding: 6px 8px !important;
    background: rgba(255, 255, 255, 0.02) !important;
    border-radius: 6px !important;
  }}

  .fuelpulse-signal-val {{
    font-size: 18px !important;
  }}

  /* I. Mockup Live Benchmark Strip Grid */
  .fuelpulse-mockup-strip {{
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    gap: 8px !important;
    padding: 10px 12px 6px 12px !important;
  }}

  .fuelpulse-mockup-strip > div {{
    padding: 8px 10px !important;
  }}

  /* J. Touch-Friendly Compact Secondary & Action Buttons */
  div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[kind="secondary"],
  div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[data-testid="stBaseButton-secondary"]:not([role="radio"]):not([role="checkbox"]):not([data-testid*="Active"]),
  button[kind="secondary"]:not([data-testid="stBaseButton-primary"]):not([role="radio"]):not([role="checkbox"]) {{
    height: 36px !important;
    min-height: 36px !important;
    font-size: 11px !important;
    padding: 0 8px !important;
    white-space: normal !important;
    text-align: center !important;
    line-height: 1.2 !important;
  }}

  div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[kind="primary"],
  div:not([data-testid*="Popover"]):not([data-baseweb="popover"]) > div.stButton > button[data-testid="stBaseButton-primary"],
  div.stDownloadButton > button,
  div.stFormSubmitButton > button {{
    height: 36px !important;
    min-height: 36px !important;
    font-size: 12px !important;
    padding: 0 10px !important;
  }}

  /* K. Navigation Shell Scaling */
  .fuelpulse-nav-shell {{
    gap: 4px !important;
    margin-bottom: 12px !important;
  }}

  .fuelpulse-nav-tier {{
    padding: 2px 4px !important;
  }}

  .fuelpulse-nav-link {{
    height: 28px !important;
    padding: 0 7px !important;
    font-size: 11px !important;
    gap: 4px !important;
  }}

  .fuelpulse-nav-tier-label {{
    font-size: 8px !important;
    padding: 0 4px !important;
  }}

  /* L. Tubelight Navigation on Mobile */
  .tubelight-nav-wrapper {{
    top: 6px !important;
    margin-bottom: 1rem !important;
  }}

  .tubelight-nav-container {{
    padding: 4px 8px !important;
    gap: 4px !important;
  }}

  .tubelight-nav-item {{
    padding: 5px 10px !important;
    font-size: 11px !important;
  }}

  .tubelight-title {{
    padding: 4px 8px !important;
    font-size: 10px !important;
  }}

  /* M. Chapter Header Banners */
  .fuelpulse-chapter-header {{
    margin-top: 2rem !important;
    margin-bottom: 1rem !important;
    padding-top: 1rem !important;
  }}

  .fuelpulse-chapter-header h2 {{
    font-size: 18px !important;
  }}

  /* N. Popovers & Menus Max Viewport Fit */
  div[data-baseweb="popover"] {{
    max-width: 95vw !important;
  }}

  /* O. Hero Mockup & Typography */
  .fuelpulse-hero-title {{
    font-size: 2.1rem !important;
    line-height: 1.15 !important;
  }}

  .fuelpulse-hero-desc {{
    font-size: 0.92rem !important;
    line-height: 1.45 !important;
    margin-bottom: 14px !important;
  }}

  .fuelpulse-product-card {{
    padding: 12px 14px !important;
    min-height: auto !important;
    margin-bottom: 8px !important;
  }}
}}

@media (max-width: 480px) {{
  .block-container {{
    padding-left: 8px !important;
    padding-right: 8px !important;
    padding-top: 2.0rem !important;
  }}

  .fuelpulse-hero-title {{
    font-size: 1.7rem !important;
    line-height: 1.2 !important;
  }}

  .fuelpulse-header-bar {{
    flex-wrap: wrap !important;
    padding: 6px 8px !important;
  }}

  .fuelpulse-header-bar .fuelpulse-status-pill {{
    font-size: 9.5px !important;
    padding: 2px 6px !important;
  }}

  .instrument-val {{
    font-size: 17px !important;
  }}

  .editorial-card, .instrument-card {{
    min-height: 76px !important;
    padding: 8px 10px !important;
  }}

  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) {{
    gap: 4px !important;
  }}

  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button,
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopover"] > button,
  button[key*="top_ai_assistant_btn"] {{
    min-height: 32px !important;
    max-height: 32px !important;
    line-height: 32px !important;
    padding: 0 2px !important;
    font-size: 10px !important;
    letter-spacing: -0.01em !important;
  }}

  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button *,
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopover"] > button *,
  button[key*="top_ai_assistant_btn"] * {{
    font-size: 10px !important;
  }}
}}
</style>"""
    render_html(custom_css)


# ==============================================================================
# 5. UNIVERSAL TOP HEADER & SYNCHRONIZED MULTI-LANGUAGE NAVIGATION
# ==============================================================================
def render_universal_top_header(active_page_name: str = "Overview", key_prefix: str = ""):
    """
    Renders the universal, synchronized top application header across all views and drill-down pages:
    - Vector Brand lockup with live database engine verification badge
    - Universal Language Selector Popover (synchronizes app_language and URL query params site-wide)
    - Live News Wire & Maritime Alert Center Popover
    """
    from src.localization.i18n import (
        t,
        get_current_language,
        set_language,
        get_available_languages,
    )
    from src.analytics.global_news_engine import GlobalNewsEngine

    apply_theme()
    current_lang = get_current_language()
    health = db_manager.check_health()
    engine_name = "MYSQL 8.4" if health["dialect"] == "mysql" else "SQLITE VERIFIED"
    
    pfx = (key_prefix or active_page_name or "nav").lower().replace(" ", "_").replace(".", "_").replace("•", "_")

    from src.ai.nl_query_engine import session_protector
    if "ai_session_id" not in st.session_state:
        import uuid
        st.session_state.ai_session_id = str(uuid.uuid4())
    sess_id = st.session_state.ai_session_id
    sess_status = session_protector.get_session_status(sess_id, has_custom_key=True, enforce_user_daily_limit=True)
    rem_q = sess_status.get("daily_questions_remaining", 3)

    col_brand, col_ai, col_lang, col_news = st.columns([6.1, 1.3, 1.3, 1.3], gap="small", vertical_alignment="center")
    with col_brand:
        render_html(render_app_header_brand_html(current_lang, engine_name, t('live_indicator', current_lang)))

    with col_ai:
        ai_btn_label = f"🤖 AI ({rem_q}/3)"
        if st.button(
            ai_btn_label,
            key=f"{pfx}_top_ai_assistant_btn",
            use_container_width=True,
            type="secondary",
            help="Ask Antigravity AI Assistant (Text & WhatsApp Voice Note)"
        ):
            _show_ai_assistant_dialog(context_page=active_page_name)

    with col_lang:
        all_langs = get_available_languages()
        cur_data = all_langs.get(current_lang, all_langs.get("en", {"flag": "🌐", "native": "English", "name": "English"}))
        cur_flag = cur_data.get("flag", "🌐")
        lang_btn_label = f"🌐 Lang ({cur_flag})"
        with st.popover(lang_btn_label, use_container_width=True):
            st.markdown(f"#### 🌐 {t('select_language', current_lang)} ({len(all_langs)} World Languages)")
            st.caption("Select and activate your language across the entire platform:")
            with st.container(height=340):
                for code, data in all_langs.items():
                    is_selected = (code == current_lang)
                    active_mark = "✓ " if is_selected else ""
                    item_label = f"{active_mark}{data['flag']}  {data['native']}  ({data['name']})"
                    if st.button(
                        item_label,
                        key=f"{pfx}_lang_btn_{code}",
                        use_container_width=True,
                        type="primary" if is_selected else "secondary"
                    ):
                        if code != current_lang:
                            set_language(code)
                            st.rerun()

    with col_news:
        alerts_count = GlobalNewsEngine.get_active_alerts_count()
        news_btn_label = f"📰 News ({alerts_count})"
        with st.popover(news_btn_label, use_container_width=True):
            render_html(f"""
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid rgba(255, 255, 255, 0.12);">
                {get_news_globe_icon_svg(size=36)}
                <div>
                    <div style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 1.15rem; font-weight: 800; color: #F9FAFB; letter-spacing: -0.01em;">
                        {t('brand_title', current_lang)} — Global Wire
                    </div>
                    <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 2px;">
                        Real-Time Maritime Intelligence & Energy Wire
                    </div>
                </div>
            </div>
            """)
            
            render_html(f"""
            <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 6px; padding: 7px 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #10B981; box-shadow: 0 0 6px #10B981;"></span>
                    <span style="font-size: 0.76rem; font-weight: 700; color: #34D399;">🟢 Live News: Auto-Synchronized</span>
                </div>
                <div style="font-size: 0.70rem; color: #94A3B8; font-family: monospace;">{GlobalNewsEngine.get_last_refresh_timestamp()}</div>
            </div>
            """)

            tab_hormuz, tab_trade, tab_rates, tab_all = st.tabs([
                f"🚨 {t('nav_trade', current_lang)}",
                f"🚢 {t('chapter_03_title', current_lang)}",
                f"⛽ {t('chapter_05_title', current_lang)}",
                f"📰 {t('live_news_button', current_lang)}"
            ])
            
            with tab_hormuz:
                st.markdown("#### 🔴 Maritime Transit Risk Monitor")
                for chk in GlobalNewsEngine.get_chokepoint_telemetry(current_lang):
                    st.markdown(f"""
                    <div style="background: rgba(14, 21, 38, 0.9); border: 1px solid rgba(255, 255, 255, 0.12); border-left: 4px solid {chk['status_color']}; border-radius: 6px; padding: 10px 12px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <b style="color: #F9FAFB; font-size: 0.9rem;">{chk['name']}</b>
                            <span style="background: rgba(239, 68, 68, 0.2); color: {chk['status_color']}; font-size: 0.7rem; font-weight: 800; padding: 2px 6px; border-radius: 4px;">{chk['status']}</span>
                        </div>
                        <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 4px;">Throughput: <b style="color: #F5B942;">{chk['throughput']}</b> ({chk['global_share']})</div>
                        <div style="font-size: 0.74rem; color: #CBD5E1; margin-top: 4px;"><b>Risk:</b> {chk['key_risk']}</div>
                        <div style="font-size: 0.72rem; color: #34D399; margin-top: 3px;"><b>Contingency:</b> {chk['contingency']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
            with tab_trade:
                st.markdown("#### 🚢 Global Petroleum Import & Export")
                for item in GlobalNewsEngine.get_live_news_feed(category="TRADE_FLOWS", lang=current_lang):
                    metrics_html = " ".join([f"<span style='background: rgba(59,130,246,0.18); color: #60A5FA; padding: 2px 6px; border-radius: 4px; font-size: 0.68rem;'><b>{k}:</b> {v}</span>" for k, v in item['metrics'].items()])
                    st.markdown(f"""
                    <div style="background: rgba(14, 21, 38, 0.9); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 6px; padding: 10px 12px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <b style="color: #F9FAFB; font-size: 0.85rem;">{item['headline']}</b>
                        </div>
                        <div style="font-size: 0.74rem; color: #94A3B8; margin: 4px 0;">{item['timestamp']} • Source: <i>{item['source']}</i></div>
                        <p style="font-size: 0.78rem; color: #CBD5E1; line-height: 1.4; margin-bottom: 6px;">{item['summary']}</p>
                        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                            {metrics_html}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
            with tab_rates:
                st.markdown("#### ⛽ Verified Live Retail Rates Today (17 Oct 2026)")
                benchmarks = GlobalNewsEngine.get_live_delhi_and_metro_benchmarks()
                d = benchmarks["delhi"]
                st.markdown(f"""
                <div style="background: rgba(234, 179, 8, 0.12); border: 1.5px solid #CA8A04; border-radius: 8px; padding: 12px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 800; color: #EAB308; font-size: 0.92rem;">🇮🇳 DELHI (LIVE TODAY)</span>
                        <span style="background: #EAB308; color: #070A12; font-weight: 800; font-size: 0.68rem; padding: 2px 6px; border-radius: 4px;">PPAC VERIFIED</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px;">
                        <div style="background: rgba(0,0,0,0.4); padding: 8px; border-radius: 6px;">
                            <div style="font-size: 0.72rem; color: #94A3B8;">Petrol RSP</div>
                            <div style="font-size: 1.25rem; font-weight: 800; color: #F9FAFB;">₹{d['petrol']:.2f}/L</div>
                        </div>
                        <div style="background: rgba(0,0,0,0.4); padding: 8px; border-radius: 6px;">
                            <div style="font-size: 0.72rem; color: #94A3B8;">Diesel RSP</div>
                            <div style="font-size: 1.25rem; font-weight: 800; color: #F9FAFB;">₹{d['diesel']:.2f}/L</div>
                        </div>
                    </div>
                    <div style="font-size: 0.74rem; color: #CBD5E1; margin-top: 8px; line-height: 1.4;">
                        • <b>Base Refinery Transfer:</b> ₹{d['base_petrol']:.2f}/L<br/>
                        • <b>Central Excise:</b> ₹{d['central_tax']:.2f}/L<br/>
                        • <b>Delhi State VAT (19.40%):</b> ₹{d['state_vat']:.2f}/L<br/>
                        • <b>Combined Tax Wedge:</b> ₹40.40/L ({d['tax_share_pct']}% of pump price)
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("**Other Indian Metros & Global:**")
                m = benchmarks["mumbai"]
                c = benchmarks["kolkata"]
                ch = benchmarks["chennai"]
                st.markdown(f"""
                <div style="font-size: 0.78rem; color: #94A3B8; line-height: 1.6;">
                    • <b>Mumbai:</b> Petrol ₹{m['petrol']:.2f}/L | Diesel ₹{m['diesel']:.2f}/L (Tax: {m['tax_share_pct']}%)<br/>
                    • <b>Kolkata:</b> Petrol ₹{c['petrol']:.2f}/L | Diesel ₹{c['diesel']:.2f}/L (Tax: {c['tax_share_pct']}%)<br/>
                    • <b>Chennai:</b> Petrol ₹{ch['petrol']:.2f}/L | Diesel ₹{ch['diesel']:.2f}/L (Tax: {ch['tax_share_pct']}%)<br/>
                    • <b>United States:</b> $3.24 / gal ($0.86/L)<br/>
                    • <b>Germany (EU):</b> €1.78 / L ($1.94/L)<br/>
                    • <b>United Kingdom:</b> £1.42 / L ($1.85/L)<br/>
                    • <b>UAE:</b> AED 3.03 / L ($0.82/L)
                </div>
                """, unsafe_allow_html=True)
                
            with tab_all:
                st.markdown("#### 📰 Complete Real-Time Intelligence Chronology")
                for item in GlobalNewsEngine.get_live_news_feed(lang=current_lang):
                    st.markdown(f"""
                    <div style="background: rgba(14, 21, 38, 0.9); border: 1px solid rgba(255, 255, 255, 0.12); border-left: 3px solid {item['impact_color']}; border-radius: 6px; padding: 10px 12px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 0.7rem; font-weight: 700; color: #F5B942;">{item['category_label']}</span>
                            <span style="font-size: 0.65rem; background: rgba(255,255,255,0.08); color: {item['impact_color']}; padding: 1px 6px; border-radius: 4px; font-weight: 700;">{item['impact']}</span>
                        </div>
                        <b style="color: #F9FAFB; font-size: 0.84rem; display: block; margin: 4px 0;">{item['headline']}</b>
                        <div style="font-size: 0.72rem; color: #94A3B8; margin-bottom: 4px;">{item['timestamp']} • <i>{item['source']}</i></div>
                        <p style="font-size: 0.76rem; color: #CBD5E1; line-height: 1.4; margin-bottom: 6px;">{item['summary']}</p>
                    </div>
                    """, unsafe_allow_html=True)


# ==============================================================================
# 5b. UNIVERSAL FLOATING AI ASSISTANT (FAB + DIALOG DRAWER)
# ==============================================================================
def _get_contextual_ai_suggestions(context_page: str) -> List[Tuple[str, str]]:
    """Returns tailored prompt chips based on the active page context."""
    c_lower = (context_page or "").lower()
    if "trade" in c_lower:
        return [
            ("🇸🇦 Saudi Fuel Supplier", "who is the main supplier of fuel from saudi"),
            ("🇮🇳 India Import Sourcing", "what are India petroleum import sourcing partners"),
            ("🇦🇪 Dubai & UAE Exports", "what are Dubai petroleum export destinations"),
            ("🇷🇺 Russian Crude Flows", "what are Russia petroleum export destinations")
        ]
    elif "price" in c_lower or "explorer" in c_lower:
        return [
            ("🇮🇳 Prayagraj Petrol & Tax", "What is the petrol price in Prayagraj and how much tax does Uttar Pradesh take?"),
            ("⛽ Delhi Pump Breakdown", "What is the fuel price in Delhi and its tax breakdown?"),
            ("🌐 US vs Germany Comparison", "Compare petrol retail prices in USA and Germany"),
            ("🇸🇦 Saudi Fuel Supplier", "who is the main supplier of fuel from saudi")
        ]
    elif "india" in c_lower:
        return [
            ("⚡ Jio Fuel Competitors", "which company can easily compete jio fuel"),
            ("🇮🇳 Prayagraj Petrol & Tax", "What is the petrol price in Prayagraj and how much tax does Uttar Pradesh take?"),
            ("⛽ Indian OMCs (IOCL/BPCL)", "Who are the major fuel retailers and OMCs in India?"),
            ("📊 Delhi Tax Wedge", "What is the fuel price in Delhi and its tax breakdown?")
        ]
    elif "afford" in c_lower:
        return [
            ("⚖️ Highest Fuel Burden", "Which country has the highest fuel burden as % of daily income?"),
            ("🇮🇳 India vs Global Burden", "How affordable is petrol in India compared to Europe?"),
            ("🇸🇦 Saudi Fuel Supplier", "who is the main supplier of fuel from saudi")
        ]
    elif "risk" in c_lower:
        return [
            ("🚢 Hormuz Chokepoint Risk", "What is the risk of a disruption in the Strait of Hormuz?"),
            ("🛡️ HHI Supply Concentration", "Which countries face the highest oil import concentration risk?"),
            ("🇸🇦 Saudi Fuel Supplier", "who is the main supplier of fuel from saudi")
        ]
    elif "shock" in c_lower:
        return [
            ("🚚 Fleet Fuel Shock (10%)", "What would a 10% increase in fuel prices do to my fleet budget?"),
            ("⚡ Crude Surge +$20/bbl", "What happens to retail prices if crude spikes by $20/bbl?"),
            ("🇸🇦 Saudi Fuel Supplier", "who is the main supplier of fuel from saudi")
        ]
    elif "forecast" in c_lower:
        return [
            ("📈 60-Day Price Radar", "What is the 60-day price forecast for petrol in India?"),
            ("🛢️ Brent Crude Trajectory", "What is the projected price trend for Brent crude?"),
            ("🇸🇦 Saudi Fuel Supplier", "who is the main supplier of fuel from saudi")
        ]
    elif "trust" in c_lower:
        return [
            ("🔒 PPAC & EIA Provenance", "Where does the fuel price data come from and how often is it updated?"),
            ("🛡️ Hallucination Safeguard", "How does Antigravity AI verify relational database records?"),
            ("🇸🇦 Saudi Fuel Supplier", "who is the main supplier of fuel from saudi")
        ]
    else:
        return [
            ("⚡ Jio Fuel Competitors", "which company can easily compete jio fuel"),
            ("🇸🇦 Saudi Fuel Supplier", "who is the main supplier of fuel from saudi"),
            ("🌍 World Oil Leader", "who is the more contributor of petrol in the world"),
            ("🇮🇳 Prayagraj Petrol & Tax", "What is the petrol price in Prayagraj and how much tax does Uttar Pradesh take?")
        ]


@st.dialog("🤖 Antigravity AI — Energy Market Intelligence", width="large")
def _show_ai_assistant_dialog(context_page: str = "Overview"):
    """
    Renders the responsive modal AI Assistant dialog.
    - Zero meta-labels like 'Simple English Explanation'
    - Answers the exact question asked with grounded energy intelligence
    - Enforces 24-hour daily quota (3 questions/24h per user) with tamper-resistant server persistence
    - WhatsApp-style dual input: Text typing + Voice note recording with automatic speech transcription
    - Renders visual Mermaid diagrams and Plotly figures (dragmode=False)
    """
    import uuid
    from src.ai.nl_query_engine import AIEnergyMarketAnalyst, session_protector
    from src.localization.i18n import get_current_language

    current_lang = get_current_language()
    pfx = ("dlg_" + context_page).lower().replace(" ", "_").replace(".", "_").replace("•", "_")

    if "ai_session_id" not in st.session_state:
        st.session_state.ai_session_id = str(uuid.uuid4())
    sess_id = st.session_state.ai_session_id

    sess_status = session_protector.get_session_status(sess_id, has_custom_key=True, enforce_user_daily_limit=True)
    rem_q = sess_status.get("daily_questions_remaining", 3)
    reset_str = sess_status.get("reset_time_str", "24 hours")
    is_blocked = sess_status.get("is_blocked", False)
    is_quota_finished = sess_status.get("is_daily_quota_finished", False)

    if is_blocked:
        status_text = "🚫 Access Blocked • Security Violation"
        status_color = "#EF4444"
    elif is_quota_finished:
        status_text = f"⏳ Daily Quota Reached (3/3 Used) • Resets in {reset_str}"
        status_color = "#F5B942"
    else:
        status_text = f"🟢 Antigravity AI Active • {rem_q}/3 Questions Today (24h Quota)"
        status_color = "#34D399"

    # Dialog Header Card
    st.markdown(f"""
    <div style="background: rgba(14, 21, 38, 0.95); backdrop-filter: blur(16px); border: 1.5px solid rgba(245, 185, 66, 0.35); border-radius: 12px; padding: 14px 18px; margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 24px;">⚡</span>
                <div>
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.05rem; font-weight: 800; color: #F9FAFB;">
                        GLOBAL FUELPULSE AI INTELLIGENCE
                    </div>
                    <div style="font-size: 0.74rem; color: #94A3B8; font-weight: 600;">
                        Context: <b style="color: #F5B942;">{context_page}</b> • Direct Grounded Analysis & Visual Projections
                    </div>
                </div>
            </div>
            <div style="background: rgba(0,0,0,0.4); border: 1px solid rgba(255, 255, 255, 0.12); padding: 4px 10px; border-radius: 999px; font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem; font-weight: 700; color: {status_color};">
                {status_text}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Contextual Suggested Chips
    suggested = _get_contextual_ai_suggestions(context_page)
    st.markdown("<div style='font-family: \"Space Grotesk\", sans-serif; font-size: 0.78rem; font-weight: 700; color: #CBD5E1; margin-bottom: 6px;'>💡 Suggested Intelligence Queries:</div>", unsafe_allow_html=True)
    chip_cols = st.columns(len(suggested))
    selected_query = None
    for idx, (label, query_str) in enumerate(suggested):
        with chip_cols[idx]:
            if st.button(label, key=f"{pfx}_chip_{idx}", use_container_width=True, type="secondary"):
                selected_query = query_str
                st.session_state[f"{pfx}_active_q"] = query_str

    current_val = selected_query or st.session_state.get(f"{pfx}_active_q", "")

    # WhatsApp-Style Dual Input: Typing + Voice Recording
    tab_type, tab_voice = st.tabs(["💬 Type Question", "🎙️ WhatsApp Voice Note"])
    user_input = ""
    ask_clicked = False

    with tab_type:
        c_in, c_btn = st.columns([5, 1], gap="small", vertical_alignment="center")
        with c_in:
            user_input = st.text_input(
                "Ask any energy question (taxes, suppliers, prices, shipping, quotas):",
                value=current_val,
                placeholder="e.g. which company can easily compete jio fuel, or who is main supplier of fuel from saudi?",
                key=f"{pfx}_input",
                label_visibility="collapsed"
            )
        with c_btn:
            ask_clicked = st.button("Ask AI ⚡", key=f"{pfx}_submit_btn", use_container_width=True, type="primary")

    with tab_voice:
        st.markdown("<div style='font-size:0.8rem; color:#94A3B8; margin-bottom:8px;'>🎙️ <b>WhatsApp Voice Note:</b> Record your question directly using your microphone. Our integrated speech engine transcribes it automatically:</div>", unsafe_allow_html=True)
        voice_audio = st.audio_input("Record Voice Question", key=f"{pfx}_voice_recorder")
        if voice_audio is not None:
            import io
            import speech_recognition as sr
            try:
                r = sr.Recognizer()
                with sr.AudioFile(io.BytesIO(voice_audio.read())) as source:
                    audio_data = r.record(source)
                    transcribed = r.recognize_google(audio_data)
                    st.success(f"🗣️ Transcribed Voice Note: **\"{transcribed}\"**")
                    if st.button("Submit Voice Question ⚡", key=f"{pfx}_voice_submit_btn", type="primary", use_container_width=True):
                        selected_query = transcribed
            except sr.UnknownValueError:
                st.info("💡 Audio captured. If speech was faint, you can also type your question directly in the Type tab.")
            except Exception:
                st.info("💡 Audio captured. You can also type your question directly in the Type tab.")

    active_run_q = None
    if ask_clicked and user_input.strip():
        active_run_q = user_input.strip()
    elif selected_query:
        active_run_q = selected_query

    resp_key = f"{pfx}_resp_cache"
    if active_run_q:
        with st.spinner("Analyzing energy intelligence marts & running Antigravity AI..."):
            ans = AIEnergyMarketAnalyst.answer_question(
                question=active_run_q,
                session_id=sess_id,
                allow_free_autonomous=True,
                enforce_user_daily_limit=True
            )
            st.session_state[resp_key] = ans

    if resp_key in st.session_state and st.session_state[resp_key]:
        resp = st.session_state[resp_key]
        st.markdown("---")
        if resp.get("is_security_blocked"):
            render_html("""<div style="padding:6px 14px;background:rgba(239, 68, 68, 0.2);color:#EF4444;font-weight:700;font-size:12.5px;border:1.5px solid #EF4444;border-radius:4px;margin-bottom:8px;">🚫 Security Alert • Access Blocked</div>""")
        elif "Daily Free Quota Finished" in resp.get("topic", "") or "Daily Quota Limit Reached" in resp.get("topic", ""):
            render_html(f"""<div style="padding:6px 14px;background:rgba(245, 185, 66, 0.2);color:#F5B942;font-weight:700;font-size:12.5px;border:1.5px solid #F5B942;border-radius:4px;margin-bottom:8px;">⏳ Daily Quota Reached (3/3 Used) • Resets in {sess_status["reset_time_str"]}</div>""")
        else:
            render_html("""<div style="padding:4px 12px;background:rgba(16, 185, 129, 0.2);color:#10B981;font-weight:700;font-size:12px;border:1px solid #10B981;border-radius:4px;display:inline-block;margin-bottom:8px;">🟢 Antigravity AI Engine Verified Response</div>""")

        st.markdown(resp["answer_text"])

        if resp.get("visualization_fig") is not None:
            fig = resp["visualization_fig"]
            try:
                fig.update_layout(dragmode=False)
            except Exception:
                pass
            st.markdown("#### 📊 Grounded Scenario & Visual Intelligence Projection")
            st.plotly_chart(fig, width="stretch", theme=None, config={"scrollZoom": False, "displayModeBar": True})

        if resp.get("data_records"):
            with st.expander("📑 Underlying Verified Relational Mart Records", expanded=False):
                rec_df = pd.DataFrame(resp["data_records"])
                st.dataframe(rec_df, width="stretch", hide_index=True)
                render_csv_download(rec_df, f"ai_grounded_{pfx}.csv")

        if resp.get("sources_cited"):
            st.caption(f"Verified Provenance: {', '.join(resp['sources_cited'])}")


def render_floating_ai_assistant(context_page: str = "Overview", key_prefix: str = ""):
    """
    Positioned natively in the upper top header across all pages.
    Bottom floating button is retired to keep the viewport clean and completely eliminate overlap.
    """
    pass


def render_universal_ai_assistant(context_page: str = "Overview", key_prefix: str = ""):
    """Maintains backward compatibility across all views by rendering the universal floating FAB."""
    render_floating_ai_assistant(context_page=context_page, key_prefix=key_prefix)


# ==============================================================================
# 5c. COMPACT EDITORIAL TOP NAVIGATION
# ==============================================================================
def render_command_strip(
    active_page: str = "Overview",
    region_tag: str = "GLOBAL",
    product_tag: str = "CRUDE & REFINED",
    reporting_period: str = "2024–2025",
    show_universal_header: bool = True
):
    """Renders the top navigation bar with brand, links, and status in dark glassmorphism."""
    apply_theme()
    if show_universal_header:
        render_universal_top_header(active_page_name=active_page, key_prefix=f"cs_{active_page}")

    from src.localization.i18n import t, get_current_language
    current_lang = get_current_language()

    health = db_manager.check_health()
    engine_name = "MYSQL 8.4" if health["dialect"] == "mysql" else "LOCAL CACHE"
    logo_svg = get_brand_logo_svg(width=290, height=48)

    nav_html = f"""<div style="background: rgba(14, 21, 38, 0.85); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); border-radius: 10px; padding: 12px 20px; margin: -0.5rem 0 1.75rem 0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
<div style="display: flex; align-items: center; gap: 14px;">{logo_svg}</div>
<div style="display: flex; align-items: center; gap: 8px; font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 700; flex-wrap: wrap;">
<a href="#ch-01" style="color: #F9FAFB; text-decoration: none; padding: 4px 8px; border-radius: 4px; transition: color 0.15s ease;">{t('nav_overview', current_lang)}</a>
<span style="color: rgba(255, 255, 255, 0.2);">•</span>
<a href="#ch-02" style="color: #F9FAFB; text-decoration: none; padding: 4px 8px; border-radius: 4px;">{t('chapter_02_title', current_lang)[:12]}</a>
<span style="color: rgba(255, 255, 255, 0.2);">•</span>
<a href="#ch-03" style="color: #F9FAFB; text-decoration: none; padding: 4px 8px; border-radius: 4px;">{t('nav_trade', current_lang)}</a>
<span style="color: rgba(255, 255, 255, 0.2);">•</span>
<a href="#ch-04" style="color: #F9FAFB; text-decoration: none; padding: 4px 8px; border-radius: 4px;">{t('chapter_04_title', current_lang)[:14]}</a>
<span style="color: rgba(255, 255, 255, 0.2);">•</span>
<a href="#ch-05" style="color: #F9FAFB; text-decoration: none; padding: 4px 8px; border-radius: 4px;">{t('nav_india', current_lang)}</a>
<span style="color: rgba(255, 255, 255, 0.2);">•</span>
<a href="#ch-11" style="color: #F9FAFB; text-decoration: none; padding: 4px 8px; border-radius: 4px;">{t('nav_data_trust', current_lang)}</a>
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
    """Renders a modern dark glass horizontal strip with mobile grid support."""
    html_items = []
    for s in signals:
        html_items.append(
            f"""<div class="fuelpulse-signal-item" style="flex: 1; min-width: 170px; padding: 10px 14px; border-right: 1px solid rgba(255, 255, 255, 0.1); display: flex; flex-direction: column;">
<span style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">{s.get('label', '')}</span>
<span class="fuelpulse-signal-val" style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 800; color: #F9FAFB; margin-top: 3px;">{s.get('value', '')}</span>
<span style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; color: #64748B; margin-top: 2px;">{s.get('note', '')}</span>
</div>"""
        )
    rail_html = f"""<div class="fuelpulse-signal-rail" style="background: rgba(14, 21, 38, 0.75); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4); border-radius: 8px; padding: 6px 12px; margin-bottom: 1.5rem; display: flex; flex-wrap: wrap; align-items: center;">
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

    header_html = f"""<div id="{anchor_id}" class="fuelpulse-chapter-header" style="margin-top: 3.5rem; margin-bottom: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255, 255, 255, 0.12);">
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
        dragmode=False,
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


def render_page_header(
    title: str,
    subtitle: str,
    source_tag: str,
    observation_date: str,
    show_universal_header: bool = True
):
    """Renders a modern dark glass page banner for drill-down pages with universal language and news header."""
    apply_theme()
    if show_universal_header:
        render_universal_top_header(active_page_name=title, key_prefix=f"hdr_{title}")
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
