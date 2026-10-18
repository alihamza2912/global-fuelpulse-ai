"""
Page 11: Product Guide & Enterprise Documentation Suite.
Comprehensive project dossiers, architectural blueprint, methodology equations, and FAQs.
"""

import sys
from pathlib import Path

# Ensure project root AND src directory are in sys.path and remove conflicting parent mount
ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"

parent_mount = ROOT_DIR.parent
sys.path = [p for p in sys.path if Path(p).resolve() != parent_mount and Path(p).resolve() != parent_mount.parent]

for d in [str(ROOT_DIR), str(SRC_DIR)]:
    while d in sys.path:
        sys.path.remove(d)
    sys.path.insert(0, d)

import streamlit as st
from src.ui_components import apply_theme, render_page_header, render_universal_ai_assistant
from src.localization.i18n import t, get_current_language
from src.views.about import render_about_view
from src.views.how_it_works import render_how_it_works_view
from src.views.features import render_features_view
from src.views.data_trust import render_data_trust_view
from src.views.methodology import render_methodology_view
from src.views.roadmap import render_roadmap_view
from src.views.faq import render_faq_view

apply_theme()
current_lang = get_current_language()

render_page_header(
    title=t("sidebar_11_guide", current_lang),
    subtitle="System Architecture, Economic Mechanics, Methodology Formulas, and FAQ",
    source_tag="Global FuelPulse AI Technical Dossier",
    observation_date="Version 2.0 Production Release"
)

# Integrated Universal AI Assistant Dock
render_universal_ai_assistant(context_page="Product Guide", key_prefix="p11_guide")

tab_about, tab_arch, tab_feat, tab_trust, tab_meth, tab_road, tab_faq = st.tabs([
    "📖 About Project",
    "⚙️ Architecture",
    "📋 Features",
    "🔒 Data Trust",
    "📐 Methodology",
    "🗺️ Roadmap",
    "❓ Docs & FAQ"
])

with tab_about:
    render_about_view()

with tab_arch:
    render_how_it_works_view()

with tab_feat:
    render_features_view()

with tab_trust:
    render_data_trust_view()

with tab_meth:
    render_methodology_view()

with tab_road:
    render_roadmap_view()

with tab_faq:
    render_faq_view()
