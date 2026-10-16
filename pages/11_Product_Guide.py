"""
Page 11: Product Guide & Enterprise Documentation Suite.
Comprehensive project dossiers, architectural blueprint, methodology equations, and FAQs.
"""

import streamlit as st
from src.ui_components import apply_theme, render_page_header
from src.views.about import render_about_view
from src.views.how_it_works import render_how_it_works_view
from src.views.features import render_features_view
from src.views.data_trust import render_data_trust_view
from src.views.methodology import render_methodology_view
from src.views.roadmap import render_roadmap_view
from src.views.faq import render_faq_view

apply_theme()

render_page_header(
    title="PRODUCT GUIDE & ENTERPRISE DOCUMENTATION",
    subtitle="System Architecture, Economic Mechanics, Methodology Formulas, and FAQ",
    source_tag="Global FuelPulse AI Technical Dossier",
    observation_date="Version 2.0 Production Release"
)

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
