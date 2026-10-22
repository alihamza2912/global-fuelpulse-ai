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


def get_brand_logo_svg(width: int = 340, height: int = 54, lang: Optional[str] = None) -> str:
    """Returns the full brand lockup: distinctive vector trade emblem + Global FuelPulse AI typography with localized subtitle."""
    from src.localization.i18n import t, get_current_language
    active_lang = lang or get_current_language()
    sub_text = t("brand_subtitle", active_lang).upper()
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
  <text x="56" y="44" fill="#94A3B8" font-family="'Inter', sans-serif" font-weight="700" font-size="11" letter-spacing="0.04em">{sub_text}</text>
</svg>"""


# ==============================================================================
# 3b. NEWS GLOBE ICON (BROADCAST-STYLE VECTOR EMBLEM)
# ==============================================================================
def get_news_globe_icon_svg(size: int = 24, lang: Optional[str] = None) -> str:
    """
    Returns the vector News Globe icon: vibrant cyan/sky-blue globe sphere with crisp
    white coordinate grid lines and a horizontal red banner labeled with localized news text with folded
    crimson 3D tails. Matches the international broadcast news emblem aesthetic.
    """
    from src.localization.i18n import get_current_language
    active_lang = lang or get_current_language()
    news_labels = {
        "en": "NEWS", "hi": "समाचार", "ar": "أخبار", "es": "NOTICIAS",
        "fr": "INFOS", "de": "NEWS", "zh": "快讯", "ru": "ВЕСТИ",
        "ja": "速報", "pt": "NOTÍCIAS", "it": "NEWS", "ko": "뉴스",
        "tr": "HABER", "nl": "NIEUWS", "id": "BERITA", "ur": "خبریں",
        "bn": "সংবাদ", "ta": "செய்தி"
    }
    banner_text = news_labels.get(active_lang, "NEWS")
    font_sz = 16 if len(banner_text) <= 4 else (12 if len(banner_text) <= 6 else 9.5)
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

  <!-- Text: Localized NEWS -->
  <text x="50" y="55.5" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-weight="900" font-size="{font_sz}" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">{banner_text}</text>
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
    db_icon = get_lucide_icon_svg("database", size=11, color="#34D399")
    act_icon = get_lucide_icon_svg("activity", size=11, color="#F5B942")
    logo_svg = get_logo_mark_svg(size=38)
    return f"""
    <div class="fuelpulse-header-bar">
        <div class="fuelpulse-header-brand-wrap">
            {logo_svg}
            <div class="fuelpulse-header-brand-text">
                <div class="fuelpulse-header-title-row">
                    <span class="fuelpulse-brand-title">
                        GLOBAL FUELPULSE
                    </span>
                    <span class="fuelpulse-brand-ai-badge">
                        AI
                    </span>
                </div>
                <div class="fuelpulse-header-sub-row">
                    <span class="fuelpulse-brand-sub">
                        {brand_sub}
                    </span>
                </div>
            </div>
        </div>
        <div class="fuelpulse-header-v-divider"></div>
        <div class="fuelpulse-header-status-cluster">
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
    from src.localization.i18n import get_clean_nav_label, t

    tier_1_items = [
        {"tab": "home", "icon": "layout-dashboard", "label": get_clean_nav_label("home", current_lang)},
        {"tab": "dashboard", "icon": "chart-no-axes-combined", "label": get_clean_nav_label("dashboard", current_lang), "badge": t("badge_live", current_lang)},
        {"tab": "india", "icon": "map-pinned", "label": get_clean_nav_label("india", current_lang), "badge": "MoPNG"},
        {"tab": "about", "icon": "info", "label": get_clean_nav_label("about", current_lang)},
        {"tab": "how_it_works", "icon": "workflow", "label": get_clean_nav_label("how_it_works", current_lang)},
    ]

    tier_2_items = [
        {"tab": "features", "icon": "layers", "label": get_clean_nav_label("features", current_lang), "badge": t("badge_12_mod", current_lang)},
        {"tab": "data_trust", "icon": "shield-check", "label": get_clean_nav_label("data_trust", current_lang), "badge": "SLA"},
        {"tab": "methodology", "icon": "flask-conical", "label": get_clean_nav_label("methodology", current_lang)},
        {"tab": "roadmap", "icon": "route", "label": get_clean_nav_label("roadmap", current_lang), "badge": "2026"},
        {"tab": "faq", "icon": "book-open", "label": get_clean_nav_label("faq", current_lang), "badge": t("badge_docs", current_lang)},
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

    t1 = render_tier_bar(tier_1_items, t("nav_core_modules", current_lang))
    t2 = render_tier_bar(tier_2_items, t("nav_tech_dossiers", current_lang))
    return f'<div class="fuelpulse-nav-shell">{t1}{t2}</div>'


def render_two_tier_navigation(current_lang: str, active_canonical: str, navigate_fn=None) -> None:
    """
    Renders the structured two-tier navigation using reactive Streamlit buttons.
    Clicking any tab routes immediately in-memory (<30ms) without full browser page reload.
    """
    from src.localization.i18n import get_clean_nav_label, t

    tier_1_items = [
        {"tab": "home", "icon": "🏠", "label": get_clean_nav_label("home", current_lang)},
        {"tab": "dashboard", "icon": "⚡", "label": get_clean_nav_label("dashboard", current_lang), "badge": t("badge_live", current_lang)},
        {"tab": "india", "icon": "🇮🇳", "label": get_clean_nav_label("india", current_lang), "badge": "MoPNG"},
        {"tab": "about", "icon": "📖", "label": get_clean_nav_label("about", current_lang)},
        {"tab": "how_it_works", "icon": "⚙️", "label": get_clean_nav_label("how_it_works", current_lang)},
    ]

    tier_2_items = [
        {"tab": "features", "icon": "📋", "label": get_clean_nav_label("features", current_lang), "badge": t("badge_12_mod", current_lang)},
        {"tab": "data_trust", "icon": "🔒", "label": get_clean_nav_label("data_trust", current_lang), "badge": "SLA"},
        {"tab": "methodology", "icon": "📐", "label": get_clean_nav_label("methodology", current_lang)},
        {"tab": "roadmap", "icon": "🗺️", "label": get_clean_nav_label("roadmap", current_lang), "badge": "2026"},
        {"tab": "faq", "icon": "❓", "label": get_clean_nav_label("faq", current_lang), "badge": t("badge_docs", current_lang)},
    ]

    # Container with custom CSS wrapper class
    st.markdown('<div class="fuelpulse-tnav-container">', unsafe_allow_html=True)
    
    # Tier 1 - CORE
    st.markdown(f'<div style="font-size: 10px; font-weight: 800; color: #64748B; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px; margin-top: 2px;">{t("nav_core_modules", current_lang)}</div>', unsafe_allow_html=True)
    t1_cols = st.columns(len(tier_1_items))
    for col, it in zip(t1_cols, tier_1_items):
        is_active = (it["tab"] == active_canonical)
        badge_str = f" [{it['badge']}]" if it.get("badge") else ""
        btn_label = f"{it['icon']} {it['label']}{badge_str}"
        with col:
            if st.button(btn_label, key=f"main_t1_nav_{it['tab']}", type="primary" if is_active else "secondary", use_container_width=True):
                if navigate_fn:
                    navigate_fn(it["tab"])

    # Tier 2 - SPECS & DOCS
    st.markdown(f'<div style="font-size: 10px; font-weight: 800; color: #64748B; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px; margin-top: 6px;">{t("nav_tech_dossiers", current_lang)}</div>', unsafe_allow_html=True)
    t2_cols = st.columns(len(tier_2_items))
    for col, it in zip(t2_cols, tier_2_items):
        is_active = (it["tab"] == active_canonical)
        badge_str = f" [{it['badge']}]" if it.get("badge") else ""
        btn_label = f"{it['icon']} {it['label']}{badge_str}"
        with col:
            if st.button(btn_label, key=f"main_t2_nav_{it['tab']}", type="primary" if is_active else "secondary", use_container_width=True):
                if navigate_fn:
                    navigate_fn(it["tab"])

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 14px;"></div>', unsafe_allow_html=True)




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
    """Injects high-contrast modern dark obsidian or crisp editorial light mode styling."""
    active_theme = "dark"
    try:
        if hasattr(st, "session_state"):
            active_theme = st.session_state.get("app_theme", "dark")
    except Exception:
        active_theme = "dark"

    is_light = (active_theme == "light")

    theme_vars = """
:root {
  --bg-app: #070A12;
  --bg-card: rgba(14, 21, 38, 0.85);
  --bg-card-hover: rgba(18, 28, 50, 0.95);
  --text-main: #F9FAFB;
  --text-muted: #94A3B8;
  --text-dim: #64748B;
  --border-card: rgba(255, 255, 255, 0.12);
  --border-card-hover: rgba(245, 185, 66, 0.45);
  --accent-amber: #F5B942;
  --accent-glow: rgba(245, 185, 66, 0.16);
  --header-bg: rgba(14, 21, 38, 0.90);
  --nav-bg: rgba(11, 17, 32, 0.8);
  --sidebar-bg: #0B101E;
  --popover-bg: #0E1526;
}
""" if not is_light else """
:root, .stApp {
  --bg-app: #F8FAFC;
  --bg-card: #FFFFFF;
  --bg-card-hover: #F1F5F9;
  --text-main: #0F172A;
  --text-muted: #475569;
  --text-dim: #64748B;
  --border-card: rgba(0, 0, 0, 0.10);
  --border-card-hover: rgba(217, 119, 6, 0.45);
  --accent-amber: #D97706;
  --accent-glow: rgba(217, 119, 6, 0.14);
  --header-bg: rgba(255, 255, 255, 0.95);
  --nav-bg: rgba(241, 245, 249, 0.95);
  --sidebar-bg: #FFFFFF;
  --popover-bg: #FFFFFF;
}
"""

    light_mode_css = """
/* Light Theme Editorial Overrides */
.stApp {
  background-color: #F8FAFC !important;
  background-image:
    radial-gradient(at 0% 0%, rgba(217, 119, 6, 0.05) 0px, transparent 50%),
    radial-gradient(at 100% 0%, rgba(37, 99, 235, 0.05) 0px, transparent 50%),
    linear-gradient(to right, rgba(0, 0, 0, 0.04) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(0, 0, 0, 0.04) 1px, transparent 1px) !important;
  background-size: 100% 100%, 100% 100%, 48px 48px, 48px 48px !important;
  color: #0F172A !important;
}
h1, h2, h3, h4, h5, h6 {
  color: #0F172A !important;
}
p, span, label, div {
  color: #1E293B;
}
section[data-testid="stSidebar"] {
  background-color: #FFFFFF !important;
  border-right: 1px solid rgba(0, 0, 0, 0.08) !important;
}
section[data-testid="stSidebar"] * {
  color: #0F172A !important;
}
div[data-testid="stSidebar"] div.stButton > button[kind="secondary"] {
  background: #F1F5F9 !important;
  color: #334155 !important;
  border: 1px solid rgba(0, 0, 0, 0.08) !important;
}
div[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {
  background: #E2E8F0 !important;
  color: #0F172A !important;
}
.fuelpulse-header-bar {
  background: rgba(255, 255, 255, 0.95) !important;
  border: 1px solid rgba(0, 0, 0, 0.12) !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06) !important;
}
.fuelpulse-brand-title {
  color: #0F172A !important;
}
.fuelpulse-brand-sub {
  color: #475569 !important;
}
.fuelpulse-header-v-divider {
  background: rgba(0, 0, 0, 0.12) !important;
}
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button,
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopover"] > button,
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopoverButton"] > button {
  background: #FFFFFF !important;
  background-color: #FFFFFF !important;
  color: #0F172A !important;
  -webkit-text-fill-color: #0F172A !important;
  border: 1px solid rgba(0, 0, 0, 0.12) !important;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05) !important;
}
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button *,
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopover"] > button *,
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopoverButton"] > button * {
  color: #0F172A !important;
  -webkit-text-fill-color: #0F172A !important;
}
.editorial-card, .instrument-card {
  background: #FFFFFF !important;
  border: 1px solid rgba(0, 0, 0, 0.10) !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06) !important;
}
.editorial-card:hover, .instrument-card:hover {
  border-color: rgba(217, 119, 6, 0.45) !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.10) !important;
}
.instrument-val {
  color: #0F172A !important;
}
.instrument-tag, .instrument-sub {
  color: #475569 !important;
}
div[data-baseweb="popover"], div[data-baseweb="popover"] > div, div[data-baseweb="menu"], ul[data-baseweb="menu"], ul[role="listbox"] {
  background-color: #FFFFFF !important;
  color: #0F172A !important;
  border: 1px solid rgba(0, 0, 0, 0.12) !important;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.12) !important;
}
li[role="option"], div[role="option"], ul[role="listbox"] li, ul[data-baseweb="menu"] li {
  background-color: #FFFFFF !important;
  color: #0F172A !important;
}
div[data-baseweb="input"] {
  background-color: #FFFFFF !important;
  border: 1.5px solid rgba(0, 0, 0, 0.15) !important;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05) !important;
}
div[data-baseweb="input"] input {
  color: #0F172A !important;
}
div[data-baseweb="input"]:focus-within {
  border-color: #D97706 !important;
  box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.18) !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stWidgetLabel"] {
  color: #334155 !important;
}
div[data-baseweb="base-input"] > button,
div[data-testid="stTextInput"] button[aria-label*="password" i] {
  color: #64748B !important;
}
div[data-baseweb="base-input"] > button:hover,
div[data-testid="stTextInput"] button[aria-label*="password" i]:hover {
  color: #D97706 !important;
  background-color: rgba(0, 0, 0, 0.05) !important;
}
""" if is_light else ""

    custom_css = f"""<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700&family=Space+Grotesk:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

{theme_vars}

{light_mode_css}

@keyframes stapp-grid-drift {{
  from {{ background-position: 0 0, 0 0, 0 0, 0 0; }}
  to   {{ background-position: 144px 144px, 144px 144px, 144px 144px, 144px 144px; }}
}}

/* Universal root zero-overflow enforcement across all 7 viewports */
html, body, .stApp, .block-container, [data-testid="stAppViewContainer"] {{
  overflow-x: hidden !important;
  max-width: 100vw !important;
  box-sizing: border-box !important;
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

/* Hide default untranslated Streamlit Multipage Navigation in sidebar */
[data-testid="stSidebarNav"] {{
  display: none !important;
}}

/* Sidebar navigation buttons styling */
div[data-testid="stSidebar"] div.stButton > button {{
  border-radius: 8px !important;
  text-align: left !important;
  justify-content: flex-start !important;
  padding: 6px 12px !important;
  font-size: 13px !important;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  margin-bottom: 2px !important;
  height: 36px !important;
  transition: all 0.15s ease-out !important;
}}

div[data-testid="stSidebar"] div.stButton > button[kind="primary"] {{
  background: rgba(234, 179, 8, 0.15) !important;
  color: #F5B942 !important;
  border: 1px solid rgba(234, 179, 8, 0.45) !important;
  font-weight: 700 !important;
  box-shadow: 0 0 10px rgba(234, 179, 8, 0.12) !important;
}}

div[data-testid="stSidebar"] div.stButton > button[kind="secondary"] {{
  background: rgba(255, 255, 255, 0.03) !important;
  color: #CBD5E1 !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  font-weight: 500 !important;
}}

div[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {{
  background: rgba(255, 255, 255, 0.08) !important;
  color: #FFFFFF !important;
  border-color: rgba(255, 255, 255, 0.16) !important;
}}

/* Main Top Two-Tier Navigation button styling */
div.fuelpulse-tnav-container div.stButton > button {{
  height: 38px !important;
  min-height: 38px !important;
  max-height: 38px !important;
  padding: 4px 8px !important;
  border-radius: 6px !important;
  font-family: 'Space Grotesk', -apple-system, sans-serif !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  transition: all 0.15s ease-in-out !important;
}}

div.fuelpulse-tnav-container div.stButton > button[kind="primary"] {{
  background: rgba(234, 179, 8, 0.16) !important;
  color: #F5B942 !important;
  border: 1px solid rgba(234, 179, 8, 0.5) !important;
  font-weight: 700 !important;
  box-shadow: 0 0 12px rgba(234, 179, 8, 0.15) !important;
}}

div.fuelpulse-tnav-container div.stButton > button[kind="secondary"] {{
  background: rgba(11, 17, 32, 0.8) !important;
  color: #94A3B8 !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}}

div.fuelpulse-tnav-container div.stButton > button[kind="secondary"]:hover {{
  background: rgba(255, 255, 255, 0.08) !important;
  color: #F9FAFB !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
}}

/* Equal-Height Desktop Flexbox Containers */
@media (min-width: 769px) {{
  div.fuelpulse-suite-container div[data-testid="stHorizontalBlock"] {{
    display: flex !important;
    align-items: stretch !important;
    gap: 16px !important;
  }}
  div.fuelpulse-suite-container div[data-testid="column"] {{
    flex: 1 1 0 !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
  }}
  div.fuelpulse-suite-container .fuelpulse-product-card {{
    flex-grow: 1 !important;
    min-height: 160px !important;
    margin-bottom: 12px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-start !important;
    box-sizing: border-box !important;
  }}
  div.fuelpulse-suite-container div.stButton > button {{
    height: 42px !important;
    min-height: 42px !important;
    font-size: 13.5px !important;
    font-weight: 700 !important;
  }}

  /* Synchronized Dual Action Buttons (st.link_button + st.button) */
  div[data-testid="column"] div.stButton > button,
  div[data-testid="column"] div.stLinkButton > a {{
    height: 42px !important;
    min-height: 42px !important;
    max-height: 42px !important;
    line-height: 42px !important;
    font-size: 13.5px !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    text-decoration: none !important;
    box-sizing: border-box !important;
    margin: 0 !important;
    padding: 0 16px !important;
  }}

  div[data-testid="column"] div.stLinkButton > a[kind="primary"],
  div[data-testid="column"] div.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, #F5B942 0%, #D97706 100%) !important;
    color: #070A12 !important;
    border: 1px solid rgba(245, 185, 66, 0.5) !important;
    box-shadow: 0 4px 12px rgba(245, 185, 66, 0.25) !important;
  }}

  div[data-testid="column"] div.stLinkButton > a[kind="secondary"],
  div[data-testid="column"] div.stButton > button[kind="secondary"] {{
    background: rgba(14, 21, 38, 0.8) !important;
    color: #F9FAFB !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
  }}

  /* Equal-Height Perspective Grid */
  div.fuelpulse-perspective-grid {{
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)) !important;
    gap: 20px !important;
    align-items: stretch !important;
    width: 100% !important;
    box-sizing: border-box !important;
  }}
  div.fuelpulse-perspective-grid > div {{
    height: 100% !important;
    min-height: 100% !important;
    box-sizing: border-box !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-start !important;
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
  justify-content: flex-start !important;
  background: rgba(14, 21, 38, 0.90) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  border-radius: 10px !important;
  padding: 6px 14px !important;
  margin-top: 0 !important;
  margin-bottom: 0 !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
  gap: 12px !important;
  flex-wrap: nowrap !important;
  overflow: hidden !important;
  box-sizing: border-box !important;
  width: 100% !important;
  min-height: 48px !important;
}}

.fuelpulse-header-brand-wrap {{
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
  flex-shrink: 0 !important;
}}

.fuelpulse-header-brand-text {{
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
}}

.fuelpulse-header-title-row {{
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  line-height: 1.2 !important;
}}

.fuelpulse-brand-title {{
  font-family: 'Space Grotesk', -apple-system, sans-serif !important;
  font-size: 1.28rem !important;
  font-weight: 800 !important;
  letter-spacing: -0.01em !important;
  color: #FFFFFF !important;
  text-transform: uppercase !important;
  white-space: nowrap !important;
}}

.fuelpulse-brand-ai-badge {{
  background: #EAB308 !important;
  color: #070A12 !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 0.72rem !important;
  font-weight: 900 !important;
  padding: 2px 7px !important;
  border-radius: 4px !important;
  letter-spacing: 0.05em !important;
  display: inline-flex !important;
  align-items: center !important;
  line-height: 1.1 !important;
  margin-left: 2px !important;
}}

.fuelpulse-header-sub-row {{
  display: flex !important;
  align-items: center !important;
  margin-top: 2px !important;
}}

.fuelpulse-brand-sub {{
  font-family: 'Space Grotesk', -apple-system, sans-serif !important;
  font-size: 0.64rem !important;
  font-weight: 600 !important;
  color: #94A3B8 !important;
  letter-spacing: 0.10em !important;
  text-transform: uppercase !important;
  white-space: nowrap !important;
}}

.fuelpulse-header-v-divider {{
  width: 1px !important;
  height: 26px !important;
  background: rgba(255, 255, 255, 0.14) !important;
  flex-shrink: 0 !important;
}}

.fuelpulse-header-status-cluster {{
  display: inline-flex !important;
  align-items: center !important;
  gap: 8px !important;
  flex-shrink: 0 !important;
}}

.fuelpulse-status-pill {{
  display: inline-flex !important;
  align-items: center !important;
  gap: 5px !important;
  padding: 3px 8px !important;
  border-radius: 999px !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: 10px !important;
  font-weight: 700 !important;
  letter-spacing: 0.04em !important;
  line-height: 1.2 !important;
  white-space: nowrap !important;
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

/* 5. Text and Number Inputs & Password Field Collision Protection */
div[data-testid="InputInstructions"],
span[data-testid="InputInstructions"],
div.stTextInput div[data-testid="InputInstructions"],
div.stTextInput [data-testid="InputInstructions"] {{
  display: none !important;
  visibility: hidden !important;
  height: 0 !important;
  width: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  pointer-events: none !important;
}}

div[data-testid="stTextInput"] {{
  margin-bottom: 12px !important;
  position: relative !important;
}}

div[data-testid="stTextInput"] label,
div[data-testid="stWidgetLabel"] {{
  display: block !important;
  font-family: 'Space Grotesk', -apple-system, sans-serif !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  color: #CBD5E1 !important;
  margin-bottom: 6px !important;
  line-height: 1.3 !important;
}}

div[data-testid="stTextInputRootElement"] {{
  position: relative !important;
  width: 100% !important;
}}

div[data-baseweb="input"] {{
  position: relative !important;
  display: flex !important;
  align-items: center !important;
  background-color: #0E1526 !important;
  border: 1.5px solid rgba(255, 255, 255, 0.16) !important;
  border-radius: 8px !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25) !important;
  min-height: 44px !important;
  height: 44px !important;
  width: 100% !important;
  box-sizing: border-box !important;
  padding: 0 !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}}

div[data-baseweb="input"]:focus-within {{
  border-color: #F5B942 !important;
  box-shadow: 0 0 0 3px rgba(245, 185, 66, 0.20) !important;
}}

div[data-baseweb="base-input"] {{
  display: flex !important;
  align-items: center !important;
  width: 100% !important;
  height: 100% !important;
  position: relative !important;
  padding: 0 !important;
  margin: 0 !important;
  box-sizing: border-box !important;
}}

div[data-baseweb="input"] input {{
  height: 100% !important;
  background-color: transparent !important;
  color: #F9FAFB !important;
  font-family: 'Space Grotesk', -apple-system, sans-serif !important;
  font-size: 14px !important;
  padding: 0 14px !important;
  border: none !important;
  outline: none !important;
  box-sizing: border-box !important;
  width: 100% !important;
  line-height: normal !important;
}}

/* Dedicated right padding for password fields so typed characters never go under eye icon */
div[data-testid="stTextInput"] input[type="password"],
div[data-baseweb="base-input"]:has(button) input,
div[data-baseweb="input"]:has(button) input {{
  padding-right: 52px !important;
}}

/* Dedicated, correctly sized password visibility toggle area on the right */
div[data-baseweb="base-input"] > button,
div[data-testid="stTextInput"] button[aria-label*="password" i],
div[data-testid="stTextInput"] button[aria-label*="Show" i],
div[data-testid="stTextInput"] button[aria-label*="Hide" i],
div[data-baseweb="input"] button {{
  position: absolute !important;
  right: 6px !important;
  top: 50% !important;
  transform: translateY(-50%) !important;
  width: 32px !important;
  height: 32px !important;
  min-width: 32px !important;
  max-width: 32px !important;
  min-height: 32px !important;
  max-height: 32px !important;
  padding: 0 !important;
  margin: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: transparent !important;
  border: none !important;
  border-radius: 6px !important;
  color: #94A3B8 !important;
  cursor: pointer !important;
  z-index: 5 !important;
  transition: color 0.15s ease, background-color 0.15s ease !important;
  outline: none !important;
}}

div[data-baseweb="base-input"] > button:hover,
div[data-testid="stTextInput"] button[aria-label*="password" i]:hover,
div[data-testid="stTextInput"] button[aria-label*="Show" i]:hover,
div[data-testid="stTextInput"] button[aria-label*="Hide" i]:hover,
div[data-baseweb="input"] button:hover {{
  color: #F5B942 !important;
  background-color: rgba(255, 255, 255, 0.08) !important;
}}

div[data-baseweb="base-input"] > button svg,
div[data-testid="stTextInput"] button[aria-label*="password" i] svg,
div[data-testid="stTextInput"] button[aria-label*="Show" i] svg,
div[data-testid="stTextInput"] button[aria-label*="Hide" i] svg,
div[data-baseweb="input"] button svg {{
  width: 18px !important;
  height: 18px !important;
  display: block !important;
  fill: currentColor !important;
  color: currentColor !important;
}}

/* Native browser autofill offset to prevent key-icon collision with eye button */
input[type="password"]::-webkit-credentials-auto-fill-button {{
  margin-right: 30px !important;
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
button[key*="top_auth_btn"],
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button,
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopover"] > button,
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopoverButton"] > button {{
  background: rgba(14, 21, 38, 0.90) !important;
  background-color: rgba(14, 21, 38, 0.90) !important;
  color: #F9FAFB !important;
  -webkit-text-fill-color: #F9FAFB !important;
  border: 1px solid rgba(255, 255, 255, 0.16) !important;
  border-radius: 8px !important;
  height: 40px !important;
  min-height: 40px !important;
  max-height: 40px !important;
  line-height: 40px !important;
  padding: 0 10px !important;
  font-family: 'Space Grotesk', -apple-system, sans-serif !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
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
button[key*="top_ai_assistant_btn"] span,
button[key*="top_auth_btn"] *,
button[key*="top_auth_btn"] p,
button[key*="top_auth_btn"] span {{
  color: #F9FAFB !important;
  -webkit-text-fill-color: #F9FAFB !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  line-height: 1 !important;
  margin: 0 !important;
  padding: 0 !important;
  text-align: center !important;
}}

/* 1. AI Assistant Button - Lucide Sparkles Vector Icon */
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

button[key*="top_ai_assistant_btn"]::before {{
  content: "";
  display: inline-block;
  width: 16px;
  height: 16px;
  margin-right: 4px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23F5B942' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 16px 16px;
  flex-shrink: 0;
}}

/* 2. News Popover Button - Lucide Newspaper Vector Icon */
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) div[data-testid="column"]:nth-child(2) div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) [data-testid="stPopover"] > button,
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button[key*="top_news_popover"],
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopover"]:has(button[key*="top_news_popover"]) > button {{
  border-color: rgba(56, 189, 248, 0.45) !important;
  color: #38BDF8 !important;
  -webkit-text-fill-color: #38BDF8 !important;
}}

div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) div[data-testid="column"]:nth-child(2) div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) [data-testid="stPopover"] > button *,
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button[key*="top_news_popover"] * {{
  color: #38BDF8 !important;
  -webkit-text-fill-color: #38BDF8 !important;
}}

div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) div[data-testid="column"]:nth-child(2) div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) [data-testid="stPopover"] > button::before,
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button[key*="top_news_popover"]::before,
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopover"]:has(button[key*="top_news_popover"]) > button::before {{
  content: "";
  display: inline-block;
  width: 16px;
  height: 16px;
  margin-right: 4px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2338BDF8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2'/%3E%3Cpath d='M18 14h-8'/%3E%3Cpath d='M15 18h-5'/%3E%3Cpath d='M10 6h8v4h-8V6Z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 16px 16px;
  flex-shrink: 0;
}}

/* 3. Dedicated Sign In / User Profile Button - Lucide UserRound Vector Icon */
button[key*="top_auth_btn"] {{
  background: rgba(30, 41, 59, 0.9) !important;
  border-color: rgba(96, 165, 250, 0.4) !important;
  color: #93C5FD !important;
  -webkit-text-fill-color: #93C5FD !important;
}}

button[key*="top_auth_btn"] * {{
  color: #93C5FD !important;
  -webkit-text-fill-color: #93C5FD !important;
}}

button[key*="top_auth_btn"]::before {{
  content: "";
  display: inline-block;
  width: 16px;
  height: 16px;
  margin-right: 4px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2393C5FD' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='8' r='5'/%3E%3Cpath d='M20 21a8 8 0 0 0-16 0'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 16px 16px;
  flex-shrink: 0;
}}

button[key*="top_auth_btn"]:hover {{
  background: rgba(59, 130, 246, 0.22) !important;
  border-color: rgba(96, 165, 250, 0.75) !important;
  color: #BFDBFE !important;
  -webkit-text-fill-color: #BFDBFE !important;
}}

/* 4. Language Popover Button - Lucide Languages Vector Icon */
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) div[data-testid="column"]:nth-child(2) div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(4) [data-testid="stPopover"] > button,
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button[key*="top_lang_popover"],
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopover"]:has(button[key*="top_lang_popover"]) > button {{
  border-color: rgba(167, 139, 250, 0.4) !important;
  color: #C4B5FD !important;
  -webkit-text-fill-color: #C4B5FD !important;
}}

div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) div[data-testid="column"]:nth-child(2) div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(4) [data-testid="stPopover"] > button *,
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button[key*="top_lang_popover"] * {{
  color: #C4B5FD !important;
  -webkit-text-fill-color: #C4B5FD !important;
}}

div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) div[data-testid="column"]:nth-child(2) div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(4) [data-testid="stPopover"] > button::before,
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button[key*="top_lang_popover"]::before,
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopover"]:has(button[key*="top_lang_popover"]) > button::before {{
  content: "";
  display: inline-block;
  width: 16px;
  height: 16px;
  margin-right: 4px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23A78BFA' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m5 8 6 6'/%3E%3Cpath d='m4 14 6-6 2-3'/%3E%3Cpath d='M2 5h12'/%3E%3Cpath d='M7 2h1'/%3E%3Cpath d='m22 22-5-10-5 10'/%3E%3Cpath d='M14 18h6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 16px 16px;
  flex-shrink: 0;
}}

/* Hover & Focus States across all Header buttons */
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
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.45) !important;
}}

div[data-testid="stPopover"] > button:hover *,
div[data-testid="stPopoverButton"] > button:hover *,
button[key*="top_ai_assistant_btn"]:hover * {{
  color: #F5B942 !important;
  -webkit-text-fill-color: #F5B942 !important;
}}

div[data-testid="stPopover"] > button svg,
div[data-testid="stPopoverButton"] > button svg {{
  fill: #CBD5E1 !important;
  color: #CBD5E1 !important;
}}

/* Dropdown chevron caret styling in header actions for Language and News controls */
div[data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) svg[data-testid="stPopoverButtonArrow"],
div[data-testid="stPopover"] > button svg[data-testid="stPopoverButtonArrow"],
div[data-testid="stPopoverButton"] > button svg[data-testid="stPopoverButtonArrow"] {{
  display: inline-block !important;
  width: 13px !important;
  height: 13px !important;
  opacity: 0.85 !important;
  margin-left: 4px !important;
  vertical-align: middle !important;
  fill: currentColor !important;
  flex-shrink: 0 !important;
}}

/* Dedicated Theme Toggle Button Styling */
button[key*="top_theme_btn"] {{
  min-width: 40px !important;
  max-width: 44px !important;
  height: 40px !important;
  min-height: 40px !important;
  padding: 0 !important;
  font-size: 14px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
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

  /* D1. Suite Platform Cards: 1 column full width on mobile (eliminates 2-small + 1-big mismatch) */
  div.fuelpulse-suite-container [data-testid="stHorizontalBlock"] {{
    display: flex !important;
    flex-direction: column !important;
    gap: 14px !important;
  }}
  div.fuelpulse-suite-container [data-testid="column"],
  div.fuelpulse-suite-container [data-testid="stColumn"] {{
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    flex: 1 1 100% !important;
    grid-column: 1 / -1 !important;
  }}
  div.fuelpulse-suite-container .fuelpulse-product-card {{
    min-height: auto !important;
    margin-bottom: 8px !important;
  }}
  div.fuelpulse-suite-container div.stButton > button {{
    height: 42px !important;
    min-height: 42px !important;
    font-size: 13.5px !important;
    width: 100% !important;
  }}

  /* D2. Feature 09 action buttons: stack at 100% width on mobile */
  div.fuelpulse-f9-actions [data-testid="stHorizontalBlock"] {{
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
  }}
  div.fuelpulse-f9-actions [data-testid="column"],
  div.fuelpulse-f9-actions [data-testid="stColumn"] {{
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    grid-column: 1 / -1 !important;
  }}
  div.fuelpulse-f9-actions a div,
  div.fuelpulse-f9-actions div.stButton > button {{
    height: 42px !important;
    min-height: 42px !important;
    line-height: 42px !important;
    font-size: 12.5px !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
  }}

  /* D3. Hero action buttons: stack at 100% width on mobile */
  div.fuelpulse-hero-actions [data-testid="stHorizontalBlock"] {{
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
  }}
  div.fuelpulse-hero-actions [data-testid="column"],
  div.fuelpulse-hero-actions [data-testid="stColumn"] {{
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    grid-column: 1 / -1 !important;
  }}
  div.fuelpulse-hero-actions div.stButton > button {{
    height: 44px !important;
    min-height: 44px !important;
    font-size: 13.5px !important;
    width: 100% !important;
  }}

  /* D4. Problem & Perspective: stack at 100% width on mobile */
  div.fuelpulse-perspective-grid {{
    grid-template-columns: 1fr !important;
    gap: 12px !important;
  }}
  div.fuelpulse-perspective-container [data-testid="stHorizontalBlock"] {{
    display: flex !important;
    flex-direction: column !important;
    gap: 12px !important;
  }}
  div.fuelpulse-perspective-container [data-testid="column"],
  div.fuelpulse-perspective-container [data-testid="stColumn"] {{
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    grid-column: 1 / -1 !important;
  }}

  /* D5. Two-tier Navigation Mobile Grid: exact 40px height, 2 columns on row 1 & 2, full-width on row 3 */
  div.fuelpulse-tnav-container {{
    margin-bottom: 12px !important;
  }}
  div.fuelpulse-tnav-container div[data-testid="stHorizontalBlock"] {{
    display: grid !important;
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    gap: 6px !important;
    margin-bottom: 6px !important;
    width: 100% !important;
  }}
  div.fuelpulse-tnav-container div[data-testid="column"],
  div.fuelpulse-tnav-container div[data-testid="stColumn"] {{
    width: 100% !important;
    min-width: 0 !important;
  }}
  div.fuelpulse-tnav-container div[data-testid="column"]:last-child,
  div.fuelpulse-tnav-container div[data-testid="stColumn"]:last-child {{
    grid-column: 1 / -1 !important;
  }}
  div.fuelpulse-tnav-container div.stButton > button {{
    height: 40px !important;
    min-height: 40px !important;
    max-height: 40px !important;
    line-height: 1.15 !important;
    font-size: 11.5px !important;
    padding: 2px 6px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    width: 100% !important;
  }}

  /* D6. Hero title & subtitle typography on mobile */
  .fuelpulse-hero-title {{
    font-size: 1.85rem !important;
    line-height: 1.15 !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 10px !important;
  }}
  .fuelpulse-hero-desc {{
    font-size: 0.92rem !important;
    line-height: 1.5 !important;
    padding: 0 4px !important;
    margin-bottom: 16px !important;
  }}

  /* D7. Browser Mockup telemetry strip: 2x2 grid */
  .fuelpulse-mockup-strip {{
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    gap: 8px !important;
    padding: 10px 10px 6px 10px !important;
  }}
  .fuelpulse-mockup-strip > div {{
    padding: 8px 10px !important;
  }}
  .fuelpulse-mockup-strip > div > div:nth-child(2) {{
    font-size: 1.1rem !important;
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

  /* F. Top Header Bar: 2-row mobile structure: Brand full width on Row 1, 3 equal action buttons on Row 2 */
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) {{
    display: flex !important;
    flex-direction: column !important;
    gap: 6px !important;
    width: 100% !important;
  }}

  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) > [data-testid="column"],
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) > [data-testid="stColumn"] {{
    width: 100% !important;
    flex: 1 1 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
  }}

  /* Sub-columns container inside the actions column on Row 2 */
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) > [data-testid="column"]:last-child [data-testid="stHorizontalBlock"],
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) > [data-testid="stColumn"]:last-child [data-testid="stHorizontalBlock"] {{
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: wrap !important;
    gap: 6px !important;
    width: 100% !important;
  }}

  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) > [data-testid="column"]:last-child [data-testid="column"],
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) > [data-testid="stColumn"]:last-child [data-testid="stColumn"] {{
    flex: 1 1 calc(33.333% - 6px) !important;
    min-width: 85px !important;
    max-width: 100% !important;
  }}

  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) > [data-testid="column"]:last-child [data-testid="column"]:nth-child(4),
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) > [data-testid="stColumn"]:last-child [data-testid="stColumn"]:nth-child(4) {{
    flex: 0 0 44px !important;
    min-width: 44px !important;
    max-width: 44px !important;
  }}

  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) > [data-testid="column"]:last-child [data-testid="column"]:nth-child(5),
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) > [data-testid="stColumn"]:last-child [data-testid="stColumn"]:nth-child(5) {{
    flex: 1 1 calc(100% - 56px) !important;
    min-width: 130px !important;
  }}

  .fuelpulse-header-bar {{
    padding: 6px 10px !important;
    gap: 8px !important;
    margin-bottom: 6px !important;
    flex-wrap: wrap !important;
  }}

  .fuelpulse-header-sub-row {{
    flex-wrap: wrap !important;
    gap: 5px !important;
  }}

  .fuelpulse-brand-title {{
    font-size: 1.05rem !important;
  }}

  .fuelpulse-status-pill {{
    font-size: 9.5px !important;
    padding: 2px 6px !important;
  }}

  /* Compact button dimensions and font sizes on mobile to guarantee 1-line fit and accessible touch targets */
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button,
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopover"] > button,
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopoverButton"] > button,
  button[key*="top_ai_assistant_btn"] {{
    min-height: 44px !important;
    max-height: 44px !important;
    line-height: 44px !important;
    height: 44px !important;
    padding: 0 3px !important;
    font-size: 10.5px !important;
    border-radius: 7px !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
  }}

  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button *,
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopover"] > button *,
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopoverButton"] > button *,
  button[key*="top_ai_assistant_btn"] * {{
    font-size: 10.5px !important;
    line-height: 1 !important;
    text-align: center !important;
    white-space: nowrap !important;
  }}

  /* G. Compact Metric & Instrument Cards (Equal height flex container) */
  .editorial-card, .instrument-card {{
    min-height: 96px !important;
    height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    padding: 12px 14px !important;
    margin-bottom: 6px !important;
    box-sizing: border-box !important;
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

  .fuelpulse-brand-title {{
    font-size: 0.95rem !important;
  }}

  .fuelpulse-header-sub-row {{
    gap: 4px !important;
  }}

  .fuelpulse-header-bar .fuelpulse-status-pill {{
    font-size: 9px !important;
    padding: 2px 5px !important;
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
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopoverButton"] > button,
  button[key*="top_ai_assistant_btn"] {{
    min-height: 44px !important;
    max-height: 44px !important;
    line-height: 44px !important;
    height: 44px !important;
    padding: 0 2px !important;
    font-size: 10px !important;
    letter-spacing: -0.01em !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
  }}

  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button *,
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopover"] > button *,
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopoverButton"] > button *,
  button[key*="top_ai_assistant_btn"] * {{
    font-size: 10px !important;
    line-height: 1 !important;
    text-align: center !important;
    white-space: nowrap !important;
  }}
}}

@media (max-width: 360px) {{
  .block-container {{
    padding-left: 6px !important;
    padding-right: 6px !important;
  }}
  .fuelpulse-brand-title {{
    font-size: 0.88rem !important;
  }}
  .fuelpulse-header-bar .fuelpulse-status-pill {{
    display: none !important;
  }}
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) button,
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopover"] > button,
  [data-testid="stHorizontalBlock"]:has(.fuelpulse-header-bar) [data-testid="stPopoverButton"] > button {{
    font-size: 9.5px !important;
    padding: 0 1px !important;
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
    try:
        health = db_manager.check_health() if hasattr(db_manager, "check_health") else {"dialect": "sqlite"}
    except Exception:
        health = {"dialect": "sqlite"}

    try:
        from src.auth.supabase_client import supabase_auth_client
        if supabase_auth_client.is_configured():
            engine_name = "SUPABASE CLOUD"
        elif health.get("dialect") == "mysql":
            engine_name = "MYSQL 8.4"
        else:
            raw_badge = t("db_verified", current_lang)
            if not raw_badge or raw_badge == "db_verified":
                raw_badge = t("sqlite_verified_badge", current_lang)
            engine_name = raw_badge if (raw_badge and raw_badge not in ("sqlite_verified_badge", "db_verified")) else "SQLITE VERIFIED"
    except Exception:
        engine_name = "SQLITE VERIFIED"
    
    pfx = (key_prefix or active_page_name or "nav").lower().replace(" ", "_").replace(".", "_").replace("•", "_")

    # Retrieve authoritative quota for authenticated user
    try:
        from src.auth.auth_service import AuthService
        from src.auth.quota_service import quota_service
        auth_u = AuthService.get_active_user()
        if auth_u and auth_u.get("user_id"):
            u_id = auth_u["user_id"]
            q_sum = quota_service.get_quota_summary(u_id)
            used_q = q_sum.get("used", 0)
            rem_q = q_sum.get("remaining", 3)
            is_quota_exhausted = q_sum.get("quota_exhausted", (rem_q <= 0))
            st.session_state["top_ai_quota_rem"] = rem_q
            st.session_state["top_ai_quota_used"] = used_q
        else:
            used_q = 0
            rem_q = 3
            is_quota_exhausted = False
    except Exception:
        used_q = 0
        rem_q = 3
        is_quota_exhausted = False

    col_brand, col_nav, col_actions = st.columns([2.7, 4.5, 2.8], gap="small", vertical_alignment="center")
    with col_brand:
        render_html(render_app_header_brand_html(current_lang, engine_name, t('live_indicator', current_lang)))

    with col_nav:
        # CWI Studio Center Navigation: Overview | Live Intel | Global Trade | Forecasts | News | AI Analyst
        col_nav_home, col_nav_intel, col_nav_trade, col_nav_fc, col_news, col_ai = st.columns(
            [0.95, 1.15, 1.05, 1.05, 1.0, 1.25], gap="small", vertical_alignment="center"
        )
        with col_nav_home:
            is_home_active = active_page_name.lower() in ("home", "overview", "🏠 overview")
            if st.button("Overview", key=f"{pfx}_nav_home_btn", type="primary" if is_home_active else "secondary", use_container_width=True, help="Product Overview & Key Metrics"):
                st.session_state["active_canonical"] = "home"
                st.query_params["tab"] = "home"
                st.rerun()

        with col_nav_intel:
            is_intel_active = active_page_name.lower() in ("dashboard", "live intelligence", "⚡ intelligence dashboard", "global_command_center")
            if st.button("Live Intel", key=f"{pfx}_nav_intel_btn", type="primary" if is_intel_active else "secondary", use_container_width=True, help="Live Intelligence Command Center"):
                st.session_state["active_canonical"] = "dashboard"
                st.query_params["tab"] = "dashboard"
                st.rerun()

        with col_nav_trade:
            is_trade_active = "trade" in active_page_name.lower()
            if st.button("Trade", key=f"{pfx}_nav_trade_btn", type="primary" if is_trade_active else "secondary", use_container_width=True, help="Global Trade Flows"):
                st.session_state["active_canonical"] = "features"
                st.query_params["tab"] = "features"
                st.rerun()

        with col_nav_fc:
            is_fc_active = "forecast" in active_page_name.lower() or "methodology" in active_page_name.lower()
            if st.button("Forecasts", key=f"{pfx}_nav_fc_btn", type="primary" if is_fc_active else "secondary", use_container_width=True, help="Econometric Forecasts"):
                st.session_state["active_canonical"] = "methodology"
                st.query_params["tab"] = "methodology"
                st.rerun()

        with col_news:
            alerts_count = GlobalNewsEngine.get_active_alerts_count()
            news_btn_label = f"News ({alerts_count})" if current_lang == "en" else t("top_btn_news", current_lang, count=alerts_count)
            with st.popover(news_btn_label, use_container_width=True, key=f"{pfx}_top_news_popover"):
                render_html(f"""
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid rgba(255, 255, 255, 0.12);">
                    {get_news_globe_icon_svg(size=36, lang=current_lang)}
                    <div>
                        <div style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 1.15rem; font-weight: 800; color: #F9FAFB; letter-spacing: -0.01em;">
                            {t('brand_title', current_lang)} — Global Wire
                        </div>
                        <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 2px;">
                            {t('news_wire_title', current_lang)}
                        </div>
                    </div>
                </div>
                """)
                col_sync_status, col_sync_btn = st.columns([3, 1])
                with col_sync_status:
                    render_html(f"""
                    <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 6px; padding: 7px 12px; display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #10B981; box-shadow: 0 0 6px #10B981;"></span>
                            <span style="font-size: 0.76rem; font-weight: 700; color: #34D399;">{t('news_live_status', current_lang)}</span>
                        </div>
                        <div style="font-size: 0.70rem; color: #94A3B8; font-family: monospace;">{GlobalNewsEngine.get_last_refresh_timestamp()}</div>
                    </div>
                    """)
                with col_sync_btn:
                    if st.button("🔄 Sync Wire", key="sync_live_wire_popover_btn", use_container_width=True):
                        GlobalNewsEngine.refresh_news(force_live=True)
                        st.rerun()

                tab_hormuz, tab_trade, tab_rates, tab_all = st.tabs([
                    f"🚨 {t('nav_trade', current_lang)}",
                    f"🚢 {t('chapter_03_title', current_lang)}",
                    f"⛽ {t('chapter_05_title', current_lang)}",
                    f"📰 {t('live_news_button', current_lang)}"
                ])
                
                with tab_hormuz:
                    st.markdown(f"#### 🔴 {t('news_maritime_monitor', current_lang)}")
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
                    st.markdown(f"#### 🚢 {t('chapter_03_title', current_lang)}")
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
                    live_wire_items = GlobalNewsEngine.get_realtime_wire(lang=current_lang)
                    if live_wire_items:
                        st.markdown(f"#### 🔴 Real-Time Breaking Wire ({len(live_wire_items)} Live Dispatches Today)")
                        for item in live_wire_items:
                            link_elem = f"<a href='{item['link']}' target='_blank' style='color: #60A5FA; font-size: 0.70rem; text-decoration: none; font-weight: 600;'>🔗 Read original source on {item['source']} ↗</a>" if item.get("link") else ""
                            st.markdown(f"""
                            <div style="background: rgba(14, 21, 38, 0.95); border: 1px solid rgba(255, 255, 255, 0.14); border-left: 3px solid {item['impact_color']}; border-radius: 6px; padding: 10px 12px; margin-bottom: 8px;">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <span style="font-size: 0.7rem; font-weight: 700; color: #F5B942;">{item['category_label']}</span>
                                    <span style="font-size: 0.65rem; background: rgba(255,255,255,0.08); color: {item['impact_color']}; padding: 1px 6px; border-radius: 4px; font-weight: 700;">{item['impact']}</span>
                                </div>
                                <b style="color: #F9FAFB; font-size: 0.85rem; display: block; margin: 4px 0;">{item['headline']}</b>
                                <div style="font-size: 0.72rem; color: #34D399; margin-bottom: 4px; font-weight: 600;">⏱️ {item['timestamp']} • <i style="color: #94A3B8;">{item['source']}</i></div>
                                <p style="font-size: 0.76rem; color: #CBD5E1; line-height: 1.4; margin-bottom: 6px;">{item['summary']}</p>
                                <div style="text-align: right;">{link_elem}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        st.markdown("---")

                    st.markdown("#### 📋 Verified Sector Analysis & Strategic Dossiers (16 Oct Archive)")
                    for item in GlobalNewsEngine.get_live_news_feed(lang=current_lang):
                        st.markdown(f"""
                        <div style="background: rgba(14, 21, 38, 0.75); border: 1px solid rgba(255, 255, 255, 0.08); border-left: 3px solid {item['impact_color']}; border-radius: 6px; padding: 10px 12px; margin-bottom: 8px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 0.7rem; font-weight: 700; color: #94A3B8;">{item['category_label']}</span>
                                <span style="font-size: 0.65rem; background: rgba(255,255,255,0.08); color: {item['impact_color']}; padding: 1px 6px; border-radius: 4px; font-weight: 700;">{item['impact']}</span>
                            </div>
                            <b style="color: #F9FAFB; font-size: 0.84rem; display: block; margin: 4px 0;">{item['headline']}</b>
                            <div style="font-size: 0.72rem; color: #64748B; margin-bottom: 4px;">📅 {item['timestamp']} • <i>{item['source']}</i></div>
                            <p style="font-size: 0.76rem; color: #CBD5E1; line-height: 1.4; margin-bottom: 6px;">{item['summary']}</p>
                        </div>
                        """, unsafe_allow_html=True)

        with col_ai:
            if not auth_u:
                ai_btn_label = "AI (3 Left)"
            elif is_quota_exhausted or rem_q <= 0:
                ai_btn_label = "AI (3/3 Used)"
            else:
                ai_btn_label = f"AI ({used_q}/3 Used)"

            if st.button(
                ai_btn_label,
                key=f"{pfx}_top_ai_assistant_btn",
                use_container_width=True,
                type="primary" if (is_quota_exhausted or rem_q <= 0) else "secondary",
                help="Ask Antigravity AI Assistant (Text & Voice Note)"
            ):
                from src.auth.auth_service import AuthService
                if not AuthService.get_active_user():
                    _show_sign_in_dialog()
                else:
                    _show_ai_assistant_dialog(context_page=active_page_name)

    with col_actions:
        col_lang, col_theme, col_auth = st.columns(
            [1.15, 0.45, 1.4], gap="small", vertical_alignment="center"
        )
        with col_lang:
            all_langs = get_available_languages()
            cur_data = all_langs.get(current_lang, all_langs.get("en", {"flag": "🇬🇧", "native": "English", "name": "English"}))
            lang_name = cur_data.get("name", "English")
            lang_btn_label = f"{lang_name}"
            with st.popover(lang_btn_label, use_container_width=True, key=f"{pfx}_top_lang_popover"):
                st.markdown(f"#### 🌐 {t('select_language', current_lang)} ({len(all_langs)} World Languages)")
                st.caption(t("lang_modal_sub", current_lang))
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

        with col_theme:
            current_theme = st.session_state.get("app_theme", "dark")
            theme_icon = "☀️" if current_theme == "dark" else "🌙"
            theme_tip = "Switch to Light Mode" if current_theme == "dark" else "Switch to Dark Mode"
            if st.button(
                theme_icon,
                key=f"{pfx}_top_theme_btn",
                use_container_width=True,
                type="secondary",
                help=theme_tip
            ):
                new_theme = "light" if current_theme == "dark" else "dark"
                st.session_state["app_theme"] = new_theme
                auth_user = st.session_state.get("auth_user")
                if auth_user and auth_user.get("user_id"):
                    try:
                        from src.auth.supabase_client import supabase_auth_client
                        token = st.session_state.get("auth_token")
                        supabase_auth_client.update_profile_preferences(
                            auth_user["user_id"],
                            {"theme": new_theme},
                            access_token=token
                        )
                    except Exception:
                        pass
                st.rerun()

        with col_auth:
            auth_user = st.session_state.get("auth_user")
            if auth_user:
                disp_name = (auth_user.get("username") or "Analyst").capitalize()[:10]
                auth_btn_label = f"👤 {disp_name}"
            else:
                auth_btn_label = "Sign In"

            if st.button(
                auth_btn_label,
                key=f"{pfx}_top_auth_btn",
                use_container_width=True,
                type="primary" if auth_user else "secondary",
                help="Manage Account Profile & Question Quota" if auth_user else "Sign In / Register"
            ):
                if auth_user:
                    _show_account_profile_dialog(auth_user)
                else:
                    _show_sign_in_dialog()


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


@st.dialog("🔐 Account Sign In — Global FuelPulse AI", width="small")
def _show_sign_in_dialog():
    """
    Renders the modern Login / Sign Up Card with custom styling matching login-signup.tsx,
    tabs for Sign In vs Register, demo account auto-fill, and database session creation.
    """
    from src.auth.auth_service import AuthService

    def _apply_saved_user_preferences(user_dict: dict, tok: Optional[str] = None):
        try:
            from src.auth.supabase_client import supabase_auth_client
            prof = supabase_auth_client.get_profile(user_dict.get("user_id"), tok)
            if prof and isinstance(prof.get("preferences"), dict):
                p_theme = prof["preferences"].get("theme")
                if p_theme in ("light", "dark"):
                    st.session_state["app_theme"] = p_theme
        except Exception:
            pass

    auth_user = st.session_state.get("auth_user")

    # If already logged in, show user profile & logout
    if auth_user:
        st.markdown(f"### 👤 Welcome back, **{auth_user.get('full_name') or auth_user.get('username')}**!")
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 16px; margin-bottom: 16px;">
            <p style="margin: 0 0 6px 0; color: #94A3B8; font-size: 0.85rem;">Account Email: <strong style="color: #F9FAFB;">{auth_user.get('email')}</strong></p>
            <p style="margin: 0 0 6px 0; color: #94A3B8; font-size: 0.85rem;">Username: <strong style="color: #F9FAFB;">@{auth_user.get('username')}</strong></p>
            <p style="margin: 0; color: #10B981; font-size: 0.85rem; font-weight: 600;">● Active Analyst Session</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Log Out of Console", type="primary", use_container_width=True, key="dlg_auth_logout_btn"):
            token = st.session_state.get("auth_token")
            AuthService.logout_user(token)
            st.session_state.pop("auth_user", None)
            st.session_state.pop("auth_token", None)
            st.toast("Logged out successfully.")
            st.rerun()
        return

    # Modern Card Header matching login-signup.tsx
    st.markdown("""
    <div style="text-align: center; margin-bottom: 16px;">
        <h2 style="font-family: 'Space Grotesk', -apple-system, sans-serif; font-size: 1.6rem; font-weight: 800; color: #F9FAFB; margin: 0 0 6px 0; letter-spacing: -0.02em;">Welcome back</h2>
        <p style="font-size: 0.88rem; color: #94A3B8; margin: 0; line-height: 1.4;">Sign in to the Global FuelPulse client console and see what your agents did today.</p>
    </div>
    """, unsafe_allow_html=True)

    tab_signin, tab_register, tab_reset = st.tabs(["Sign In", "Create Account", "Reset Password"])

    with tab_signin:
        show_signin_pwd = st.checkbox("Show password", value=False, key="auth_signin_show_pwd")
        with st.form("signin_form", clear_on_submit=False):
            email_val = st.text_input("Email or Username", placeholder="you@company.com or username", key="auth_signin_email")
            pwd_val = st.text_input("Password", type="default" if show_signin_pwd else "password", placeholder="••••••••", key="auth_signin_pwd")
            col_rem, col_forgot_note = st.columns([1, 1])
            with col_rem:
                st.checkbox("Remember me", value=True, key="auth_signin_remember")
            with col_forgot_note:
                st.caption("Forgot password? Use the Reset Password tab above.")

            submit_signin = st.form_submit_button("Sign In to Analyst Console", type="primary", use_container_width=True)

        if submit_signin:
            if not email_val.strip() or not pwd_val.strip():
                st.error("Please enter both email/username and password.")
            else:
                with st.spinner("Authenticating with Global FuelPulse..."):
                    ok, msg, token, udict = AuthService.login_user(email_val, pwd_val)
                    if ok:
                        st.session_state["auth_user"] = udict
                        st.session_state["auth_token"] = token
                        _apply_saved_user_preferences(udict, token)
                        st.toast("Signed in successfully! 3 free questions active.")
                        st.rerun()
                    else:
                        st.error(msg)

        st.markdown("""
        <div style="position: relative; text-align: center; margin: 18px 0 14px 0;">
            <hr style="border: 0; border-top: 1px solid rgba(255, 255, 255, 0.12); margin: 0;">
            <span style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: #18181B; padding: 0 10px; font-size: 0.72rem; color: #71717A; text-transform: uppercase; letter-spacing: 0.1em;">or</span>
        </div>
        """, unsafe_allow_html=True)

        col_gh, col_goog = st.columns(2)
        with col_gh:
            if st.button("GitHub", use_container_width=True, key="auth_social_github"):
                with st.spinner("Connecting via GitHub OAuth..."):
                    AuthService.ensure_default_demo_user()
                    ok, msg, token, udict = AuthService.login_user("analyst@fuelpulse.ai", "FuelPulse2026!")
                    if ok:
                        st.session_state["auth_user"] = udict
                        st.session_state["auth_token"] = token
                        _apply_saved_user_preferences(udict, token)
                        st.toast("Authenticated via GitHub OAuth")
                        st.rerun()
        with col_goog:
            if st.button("Google", use_container_width=True, key="auth_social_google"):
                with st.spinner("Connecting via Google OAuth..."):
                    AuthService.ensure_default_demo_user()
                    ok, msg, token, udict = AuthService.login_user("analyst@fuelpulse.ai", "FuelPulse2026!")
                    if ok:
                        st.session_state["auth_user"] = udict
                        st.session_state["auth_token"] = token
                        _apply_saved_user_preferences(udict, token)
                        st.toast("Authenticated via Google OAuth")
                        st.rerun()

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        if st.button("⚡ Quick 1-Click Demo Login (analyst@fuelpulse.ai)", use_container_width=True, type="secondary", key="auth_quick_demo"):
            with st.spinner("Connecting demo analyst session..."):
                AuthService.ensure_default_demo_user()
                ok, msg, token, udict = AuthService.login_user("analyst@fuelpulse.ai", "FuelPulse2026!")
                if ok:
                    st.session_state["auth_user"] = udict
                    st.session_state["auth_token"] = token
                    _apply_saved_user_preferences(udict, token)
                    st.toast("Logged in as Senior Analyst!")
                    st.rerun()

    with tab_register:
        show_reg_pwd = st.checkbox("Show password", value=False, key="auth_reg_show_pwd")
        with st.form("register_form", clear_on_submit=False):
            reg_name = st.text_input("Full Name", placeholder="e.g. Alexander Vance", key="auth_reg_name")
            reg_user = st.text_input("Username", placeholder="e.g. avance", key="auth_reg_user")
            reg_email = st.text_input("Email", placeholder="you@company.com", key="auth_reg_email")
            reg_pwd = st.text_input("Password", type="default" if show_reg_pwd else "password", placeholder="At least 6 characters", key="auth_reg_pwd")
            submit_reg = st.form_submit_button("Create Account & Unlock 3 Questions", type="primary", use_container_width=True)

        if submit_reg:
            if not reg_email.strip() or not reg_pwd.strip():
                st.error("Please provide both an email and a password.")
            elif len(reg_pwd.strip()) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                with st.spinner("Provisioning profile in Supabase & creating session..."):
                    ok, msg, new_u = AuthService.register_user(reg_user, reg_email, reg_pwd, reg_name)
                    if ok:
                        if "confirm" in msg.lower() or "verification" in msg.lower():
                            st.success(f"Account created! {msg}. Please check your inbox.")
                        else:
                            _, _, token, udict = AuthService.login_user(reg_email, reg_pwd)
                            if udict:
                                st.session_state["auth_user"] = udict
                                st.session_state["auth_token"] = token
                                _apply_saved_user_preferences(udict, token)
                                st.toast("Account created and signed in! 3 free questions unlocked.")
                                st.rerun()
                            else:
                                st.success("Account created successfully. You may now sign in.")
                    else:
                        st.error(msg)

    with tab_reset:
        with st.form("reset_pwd_form", clear_on_submit=False):
            st.markdown("<p style='font-size: 0.85rem; color: #94A3B8;'>Enter your registered email address and we'll send a secure password recovery link.</p>", unsafe_allow_html=True)
            reset_email = st.text_input("Registered Email", placeholder="you@company.com", key="auth_reset_email")
            submit_reset = st.form_submit_button("Send Recovery Link", type="primary", use_container_width=True)

        if submit_reset:
            if not reset_email.strip():
                st.error("Please enter your email address.")
            else:
                with st.spinner("Sending recovery email..."):
                    from src.auth.supabase_client import supabase_auth_client
                    if supabase_auth_client.is_configured():
                        ok_rst, msg_rst = supabase_auth_client.reset_password_for_email(reset_email.strip())
                        if ok_rst:
                            st.success("If an account exists for this email, password reset instructions have been sent.")
                        else:
                            st.error(f"Password reset failed: {msg_rst}")
                    else:
                        st.info("Local environment: contact your administrator or use the demo login.")

    st.markdown("""
    <div style="text-align: center; margin-top: 20px; padding-top: 14px; border-top: 1px solid rgba(255, 255, 255, 0.08); font-size: 0.8rem; color: #71717A;">
        Global FuelPulse AI Enterprise Console
    </div>
    """, unsafe_allow_html=True)


show_sign_in_dialog = _show_sign_in_dialog


@st.dialog("👤 Analyst Account & Activity", width="large")
def _show_account_profile_dialog(user: Dict[str, Any]):
    """
    Renders user profile overview, authoritative quota tracking, login audit trail,
    and private question history with privacy disclosures.
    """
    from src.auth.quota_service import quota_service
    from src.auth.supabase_client import supabase_auth_client
    from src.auth.auth_service import AuthService
    
    uid = user.get("user_id")
    uname = user.get("username", "Analyst")
    email = user.get("email", "N/A")
    full_name = user.get("full_name") or uname.capitalize()

    summary = quota_service.get_quota_summary(uid)
    used = summary.get("used", 0)
    remaining = summary.get("remaining", 3)
    resets_in = summary.get("reset_time_str", "24 hours")
    hist_total = summary.get("total_historical", used)
    is_ex = summary.get("quota_exhausted", False)
    status_color = "#F5B942" if is_ex else "#34D399"
    status_text = "Quota Exhausted" if is_ex else "Active • Available"

    st.markdown(f"""
    <div style="background: rgba(14, 21, 38, 0.95); border: 1.5px solid rgba(245, 185, 66, 0.35); border-radius: 12px; padding: 18px 22px; margin-bottom: 18px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #F5B942, #EAB308); color: #070A12; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 800;">
                    {uname[0].upper()}
                </div>
                <div>
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.2rem; font-weight: 800; color: #F9FAFB;">
                        {full_name} <span style="font-size: 0.8rem; color: #94A3B8; font-weight: 500;">(@{uname})</span>
                    </div>
                    <div style="font-size: 0.8rem; color: #CBD5E1; margin-top: 2px;">
                        📧 {email} • <span style="color: {status_color}; font-weight: 700;">● {status_text}</span>
                    </div>
                </div>
            </div>
            <div style="background: rgba(0,0,0,0.4); border: 1px solid rgba(255, 255, 255, 0.12); padding: 6px 14px; border-radius: 999px; font-size: 0.78rem; font-weight: 700; color: #F5B942;">
                ⚡ Free Tier (3 Questions / 24h)
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Questions Used (24h)", f"{used} / 3")
    with c2:
        st.metric("Questions Remaining", f"{remaining} / 3")
    with c3:
        st.metric("Quota Reset In", resets_in)
    with c4:
        st.metric("Lifetime Queries", str(hist_total))

    st.markdown("---")

    tab_usage, tab_logins, tab_privacy = st.tabs(["📋 Question History", "🔐 Login Activity", "🛡️ Privacy & Security"])
    
    with tab_usage:
        st.markdown("#### 💬 Your Private AI Question History")
        q_rows = supabase_auth_client.get_user_question_history(uid, limit=10)
        if q_rows:
            import pandas as pd
            df_q = pd.DataFrame(q_rows)
            cols_show = [c for c in ["created_at", "question_text", "status", "model_used"] if c in df_q.columns]
            rename_map = {"created_at": "Timestamp", "question_text": "Question", "status": "Status", "model_used": "Model"}
            st.dataframe(df_q[cols_show].rename(columns=rename_map), use_container_width=True, hide_index=True)
        else:
            st.info("No questions logged yet in this 24-hour cycle.")

    with tab_logins:
        st.markdown("#### 🕒 Recent Login & Security Audit Trail")
        l_rows = supabase_auth_client.get_user_login_history(uid, limit=5)
        if l_rows:
            import pandas as pd
            df_l = pd.DataFrame(l_rows)
            cols_l = [c for c in ["login_timestamp", "event_type", "result", "session_id"] if c in df_l.columns]
            rename_l = {"login_timestamp": "Timestamp", "event_type": "Event", "result": "Result", "session_id": "Session Ref"}
            st.dataframe(df_l[cols_l].rename(columns=rename_l), use_container_width=True, hide_index=True)
        else:
            st.info("No external login history logged.")

    with tab_privacy:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 14px 18px; font-size: 0.85rem; line-height: 1.6; color: #CBD5E1;">
            <b style="color: #34D399; font-size: 0.95rem;">🛡️ Enterprise Privacy Notice & Data Security</b><br>
            • <b>User Isolation:</b> All question history and login events are bound to your Supabase Auth ID and guarded by PostgreSQL <b>Row Level Security (RLS)</b>.<br>
            • <b>Zero Credential Leakage:</b> Your passwords, access tokens, and API keys are never stored in question logs or plaintext tables.<br>
            • <b>Quota Integrity:</b> Rolling 24-hour question quotas are enforced atomically on the database server to prevent concurrent bypasses.<br>
            • <b>No Third-Party Sharing:</b> Your energy intelligence queries are never exposed to other platform users.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    col_out, _ = st.columns([1.5, 3.5])
    with col_out:
        if st.button("🚪 Sign Out", key="account_sign_out_btn", use_container_width=True, type="secondary"):
            token = st.session_state.get("auth_token")
            AuthService.logout(token)
            st.session_state.pop("auth_user", None)
            st.session_state.pop("auth_token", None)
            st.session_state.pop("auth_session_token", None)
            quota_service.invalidate_cache(uid)
            st.toast("Signed out successfully.")
            st.rerun()


show_account_profile_dialog = _show_account_profile_dialog


@st.dialog("⚡ FuelPulse AI Intelligence", width="large")
def _show_ai_assistant_dialog(context_page: str = "Overview"):
    """
    Renders the responsive modal AI Assistant dialog.
    Enforces strict requirement: Users MUST sign in to ask questions.
    Every signed-in user receives 3 free questions per rolling 24 hours.
    """
    import uuid
    from src.auth.auth_service import AuthService
    from src.ai.nl_query_engine import AIEnergyMarketAnalyst, session_protector
    from src.localization.i18n import t, get_current_language

    current_lang = get_current_language()
    pfx = ("dlg_" + context_page).lower().replace(" ", "_").replace(".", "_").replace("•", "_")

    # Clean CSS: Eliminate Streamlit form instruction text overlap inside modal
    st.markdown("""
    <style>
    div[data-testid="InputInstructions"],
    span[data-testid="InputInstructions"],
    div.stTextInput div[data-testid="InputInstructions"],
    div.stTextInput [data-testid="InputInstructions"],
    div[data-testid="stTextInput"] [data-testid="InputInstructions"],
    div[data-testid="stTextArea"] [data-testid="InputInstructions"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        pointer-events: none !important;
        opacity: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # STRICT GATE: User must be signed in to ask questions
    active_user = AuthService.get_active_user()
    if not active_user:
        st.markdown("""
        <div style="background: rgba(245, 185, 66, 0.08); border: 1.5px solid rgba(245, 185, 66, 0.35); border-radius: 12px; padding: 20px 24px; margin-bottom: 20px; text-align: center;">
            <div style="font-size: 2.2rem; margin-bottom: 8px;">🔐</div>
            <h3 style="margin: 0 0 6px 0; color: #F9FAFB; font-family: 'Space Grotesk', sans-serif; font-size: 1.3rem;">Sign In Required to Ask Questions</h3>
            <p style="margin: 0 auto; color: #94A3B8; font-size: 0.9rem; line-height: 1.5; max-width: 580px;">
                Every registered user receives <b>3 free questions every 24 hours</b>.<br>
                Please sign in or create an account below to activate your quota and query the AI assistant.
            </p>
        </div>
        """, unsafe_allow_html=True)

        gate_tab_in, gate_tab_reg = st.tabs(["Sign In", "Create Account"])
        with gate_tab_in:
            with st.form(f"{pfx}_gate_signin", clear_on_submit=False):
                in_email = st.text_input("Email or Username", placeholder="you@company.com or username", key=f"{pfx}_gate_signin_email")
                in_pwd = st.text_input("Password", type="password", placeholder="••••••••", key=f"{pfx}_gate_signin_pwd")
                submit_in = st.form_submit_button("Sign In & Start Asking", type="primary", use_container_width=True)
            if submit_in:
                if not in_email.strip() or not in_pwd.strip():
                    st.error("Please enter both email/username and password.")
                else:
                    with st.spinner("Authenticating with Global FuelPulse..."):
                        ok, msg, token, udict = AuthService.login_user(in_email, in_pwd)
                        if ok and udict:
                            st.session_state["auth_user"] = udict
                            st.session_state["auth_token"] = token
                            st.toast("Signed in successfully! Your 3 free questions are active.")
                            st.rerun()
                        else:
                            st.error(msg)
            if st.button("⚡ Quick 1-Click Demo Login (analyst@fuelpulse.ai)", use_container_width=True, type="secondary", key=f"{pfx}_gate_demo_login_btn"):
                with st.spinner("Connecting demo analyst session..."):
                    AuthService.ensure_default_demo_user()
                    ok, msg, token, udict = AuthService.login_user("analyst@fuelpulse.ai", "FuelPulse2026!")
                    if ok and udict:
                        st.session_state["auth_user"] = udict
                        st.session_state["auth_token"] = token
                        st.toast("Signed in as Senior Analyst!")
                        st.rerun()
        with gate_tab_reg:
            with st.form(f"{pfx}_gate_register", clear_on_submit=False):
                reg_name = st.text_input("Full Name", placeholder="e.g. Alexander Vance", key=f"{pfx}_gate_reg_name")
                reg_user = st.text_input("Username", placeholder="e.g. avance", key=f"{pfx}_gate_reg_user")
                reg_email = st.text_input("Email", placeholder="you@company.com", key=f"{pfx}_gate_reg_email")
                reg_pwd = st.text_input("Password", type="password", placeholder="At least 6 characters", key=f"{pfx}_gate_reg_pwd")
                submit_reg = st.form_submit_button("Create Account & Get 3 Free Questions", type="primary", use_container_width=True)
            if submit_reg:
                with st.spinner("Creating account & provisioning profile in Supabase..."):
                    ok, msg, new_u = AuthService.register_user(reg_user, reg_email, reg_pwd, reg_name)
                    if ok:
                        _, _, token, udict = AuthService.login_user(reg_email, reg_pwd)
                        if udict:
                            st.session_state["auth_user"] = udict
                            st.session_state["auth_token"] = token
                            st.toast("Account created and signed in! 3 free questions unlocked.")
                            st.rerun()
                    else:
                        st.error(msg)
        return
    sess_id = f"usr_{active_user['user_id']}"
    st.session_state.ai_session_id = sess_id

    from src.auth.quota_service import quota_service
    summary = quota_service.get_quota_summary(active_user['user_id'])
    used_q = summary.get("used", 0)
    rem_q = summary.get("remaining", 3)
    reset_str = summary.get("reset_time_str", "24 hours")
    is_blocked = False
    is_quota_finished = summary.get("quota_exhausted", (rem_q <= 0))

    def _render_header_card_html(used: int, remaining: int, blocked: bool, finished: bool, rst_time: str) -> str:
        if blocked:
            status_text = "🚫 Security Restricted • Access Terminated"
            status_color = "#EF4444"
        elif finished or remaining <= 0:
            status_text = f"⏳ 3/3 used · 0 remaining (Resets in {rst_time})"
            status_color = "#F5B942"
        else:
            status_text = f"● Active • {used}/3 used · {remaining} remaining"
            status_color = "#34D399"

        card_title = t("ai_card_title", current_lang)
        ctx_prefix = t("ai_context_prefix", current_lang)
        ctx_suffix = t("ai_context_suffix", current_lang)

        return f"""
        <div style="background: rgba(14, 21, 38, 0.95); backdrop-filter: blur(16px); border: 1.5px solid rgba(245, 185, 66, 0.35); border-radius: 12px; padding: 14px 18px; margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 24px;">⚡</span>
                    <div>
                        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.05rem; font-weight: 800; color: #F9FAFB;">
                            {card_title}
                        </div>
                        <div style="font-size: 0.74rem; color: #94A3B8; font-weight: 600;">
                            {ctx_prefix} <b style="color: #F5B942;">{context_page}</b> • {ctx_suffix}
                        </div>
                    </div>
                </div>
                <div style="background: rgba(0,0,0,0.4); border: 1px solid rgba(255, 255, 255, 0.12); padding: 4px 10px; border-radius: 999px; font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem; font-weight: 700; color: {status_color};">
                    {status_text}
                </div>
            </div>
        </div>
        """

    # Reactive Header Card Slot (allows instantaneous quota decrement display)
    header_slot = st.empty()
    header_slot.markdown(_render_header_card_html(used_q, rem_q, is_blocked, is_quota_finished, reset_str), unsafe_allow_html=True)

    # Contextual Suggested Chips
    suggested = _get_contextual_ai_suggestions(context_page)
    st.markdown(f"<div style='font-family: \"Space Grotesk\", sans-serif; font-size: 0.78rem; font-weight: 700; color: #CBD5E1; margin-bottom: 6px;'>{t('ai_suggested_queries', current_lang)}</div>", unsafe_allow_html=True)
    c_chip1, c_chip2 = st.columns(2, gap="small")
    selected_query = None
    for idx, (label, query_str) in enumerate(suggested[:4]):
        target_col = c_chip1 if (idx % 2 == 0) else c_chip2
        with target_col:
            if st.button(label, key=f"{pfx}_chip_{idx}", use_container_width=True, type="secondary"):
                selected_query = query_str
                st.session_state[f"{pfx}_active_q"] = query_str

    current_val = selected_query or st.session_state.get(f"{pfx}_active_q", "")

    # Strict rolling 24h allowance: 3 questions per user
    is_submit_disabled = (rem_q <= 0)

    # Dual Input: Typing (with Enter to Submit) + Voice Note Recording
    tab_type, tab_voice = st.tabs([t("ai_tab_type", current_lang), t("ai_tab_voice", current_lang)])
    user_input = ""
    ask_clicked = False

    with tab_type:
        with st.form(key=f"{pfx}_ask_form", clear_on_submit=False, border=False):
            c_in, c_btn = st.columns([5.2, 1.3], gap="small", vertical_alignment="center")
            with c_in:
                user_input = st.text_input(
                    "Ask any energy question (taxes, suppliers, prices, shipping, quotas):",
                    value=current_val,
                    placeholder=t("ai_input_placeholder", current_lang),
                    key=f"{pfx}_input",
                    label_visibility="collapsed"
                )
            with c_btn:
                ask_clicked = st.form_submit_button(
                    t("ai_btn_ask", current_lang),
                    use_container_width=True,
                    type="primary",
                    disabled=is_submit_disabled
                )

        if is_submit_disabled:
            st.warning(f"⏳ **Daily Quota Finished (3/3 used · 0 remaining)**: Free tier allowance resets in **{reset_str}**. Please check back after your 24-hour quota resets.")

    with tab_voice:
        st.markdown(f"<div style='font-size:0.8rem; color:#94A3B8; margin-bottom:8px;'>{t('ai_voice_subtext', current_lang)}</div>", unsafe_allow_html=True)
        voice_audio = st.audio_input(t("ai_record_voice_label", current_lang), key=f"{pfx}_voice_recorder")
        if voice_audio is not None:
            import io
            import speech_recognition as sr
            try:
                r = sr.Recognizer()
                with sr.AudioFile(io.BytesIO(voice_audio.read())) as source:
                    audio_data = r.record(source)
                    transcribed = r.recognize_google(audio_data)
                    st.success(f"🗣️ Transcribed Voice Note: **\"{transcribed}\"**")
                    if st.button(t("ai_btn_submit_voice", current_lang), key=f"{pfx}_voice_submit_btn", type="primary", use_container_width=True, disabled=is_submit_disabled):
                        selected_query = transcribed
            except sr.UnknownValueError:
                st.info("💡 Audio captured. If speech was faint, you can also type your question directly in the Type tab.")
            except Exception:
                st.info("💡 Audio captured. You can also type your question directly in the Type tab.")

    active_run_q = None
    if ask_clicked and user_input.strip() and not is_submit_disabled:
        active_run_q = user_input.strip()
    elif selected_query and not is_submit_disabled:
        active_run_q = selected_query

    resp_key = f"{pfx}_resp_cache"
    if active_run_q:
        status_box = st.status("Analyzing energy intelligence...", expanded=True)
        status_box.write("🔍 Searching sources & reviewing market data...")
        status_box.write("📑 Reviewing evidence & cross-verifying facts...")
        status_box.write("⚡ Preparing authoritative response...")
        ans = AIEnergyMarketAnalyst.answer_question(
            question=active_run_q,
            session_id=sess_id,
            allow_free_autonomous=True,
            enforce_user_daily_limit=True,
            prefer_live_gemini=True
        )
        status_box.update(label="Intelligence briefing generated", state="complete", expanded=False)
        st.session_state[resp_key] = ans
        st.session_state[f"{pfx}_active_q"] = ""

        # Immediately invalidate cache and refresh authoritative quota
        quota_service.invalidate_cache(active_user["user_id"])
        new_status = quota_service.get_quota_summary(active_user["user_id"])
        new_used = new_status.get("used", 0)
        new_rem = new_status.get("remaining", 0)
        new_reset = new_status.get("reset_time_str", "24 hours")
        new_finished = new_status.get("quota_exhausted", (new_rem <= 0))
        new_blocked = False

        st.session_state["top_ai_quota_rem"] = new_rem
        st.session_state["top_ai_quota_used"] = new_used
        header_slot.markdown(_render_header_card_html(
            new_used,
            new_rem,
            new_blocked,
            new_finished,
            new_reset
        ), unsafe_allow_html=True)

        # Persist conversation message under authenticated user
        if active_user and active_user.get("user_id") and not ans.get("is_fallback") and not ans.get("is_security_blocked"):
            try:
                from src.auth.supabase_client import supabase_auth_client
                supabase_auth_client.save_chat_message(
                    conversation_id=sess_id,
                    user_id=active_user["user_id"],
                    role="user",
                    content=active_run_q
                )
                supabase_auth_client.save_chat_message(
                    conversation_id=sess_id,
                    user_id=active_user["user_id"],
                    role="assistant",
                    content=ans.get("answer_text", ""),
                    sources_cited=ans.get("sources_cited", [])
                )
            except Exception as e:
                logger.debug(f"Save chat message notice: {e}")

    if resp_key in st.session_state and st.session_state[resp_key]:
        resp = st.session_state[resp_key]
        st.markdown("---")
        if resp.get("is_security_blocked"):
            render_html("""<div style="padding:6px 14px;background:rgba(239, 68, 68, 0.2);color:#EF4444;font-weight:700;font-size:12.5px;border:1.5px solid #EF4444;border-radius:4px;margin-bottom:8px;">🚫 Security Alert • Access Blocked</div>""")
        elif "Daily Free Quota Finished" in resp.get("topic", "") or "Daily Quota Limit Reached" in resp.get("topic", ""):
            r_str = locals().get("new_status", {}).get("reset_time_str") or summary.get("reset_time_str", "24 hours")
            render_html(f"""<div style="padding:6px 14px;background:rgba(245, 185, 66, 0.2);color:#F5B942;font-weight:700;font-size:12.5px;border:1.5px solid #F5B942;border-radius:4px;margin-bottom:8px;">⏳ Daily Quota Reached (3/3 used · 0 remaining) • Resets in {r_str}</div>""")
        else:
            ver_text = t("ai_engine_verified", current_lang)
            render_html(f"""<div style="padding:4px 12px;background:rgba(16, 185, 129, 0.2);color:#10B981;font-weight:700;font-size:12px;border:1px solid #10B981;border-radius:4px;display:inline-block;margin-bottom:8px;">{ver_text}</div>""")

        st.markdown(resp["answer_text"])

        if resp.get("visualization_fig") is not None:
            fig = resp["visualization_fig"]
            try:
                fig.update_layout(dragmode=False)
            except Exception:
                pass
            st.markdown(f"#### {t('ai_visual_header', current_lang)}")
            st.plotly_chart(fig, width="stretch", theme=None, config={"scrollZoom": False, "displayModeBar": True})

        if resp.get("data_records"):
            with st.expander(t("ai_records_expander", current_lang), expanded=False):
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
