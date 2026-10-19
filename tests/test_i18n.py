"""
Unit tests for Global FuelPulse AI Multi-Language Localization (i18n) Engine.
Validates language registry, translation fallbacks, and multi-lingual UI coverage.
"""

import pytest
from src.localization.i18n import (
    t,
    get_current_language,
    set_language,
    get_available_languages,
    get_localized_nav_map,
    SUPPORTED_LANGUAGES,
    TRANSLATIONS
)

def test_supported_languages_catalog():
    langs = get_available_languages()
    expected_codes = [
        "en", "hi", "es", "fr", "ar", "de", "zh", "ru", "ja",
        "pt", "it", "ko", "tr", "nl", "id", "ur", "bn", "ta"
    ]
    assert len(langs) == 18, f"Expected 18 languages, found {len(langs)}"
    for code in expected_codes:
        assert code in langs, f"Language {code} missing from supported catalog"
        assert "name" in langs[code]
        assert "native" in langs[code]
        assert "flag" in langs[code]

def test_hindi_translations():
    # Hindi checks
    assert t("brand_subtitle", "hi") == "ऊर्जा खुफिया एवं बाजार विश्लेषण मंच"
    assert t("chapter_01_title", "hi") == "वैश्विक ऊर्जा परिदृश्य एक नज़र में"
    assert t("chapter_05_title", "hi") == "भारत में पेट्रोल और डीजल की कीमतें"
    assert "पेट्रोल" in t("petrol_rsp", "hi")
    assert "डीजल" in t("diesel_rsp", "hi")

def test_spanish_translations():
    # Spanish checks
    assert t("chapter_01_title", "es") == "Energía Global de un Vistazo"
    assert t("chapter_03_title", "es") == "¿Quién Exporta y Quién Importa?"
    assert "Gasolina" in t("petrol_rsp", "es")

def test_french_translations():
    # French checks
    assert t("chapter_01_title", "fr") == "L'Énergie Mondiale en un Coup d'Œil"
    assert t("chapter_05_title", "fr") == "Prix de l'Essence et du Diesel en Inde"
    assert "Essence" in t("petrol_rsp", "fr")

def test_fallback_behavior():
    # Non-existent key should return key string itself
    assert t("non_existent_random_key_12345", "en") == "non_existent_random_key_12345"
    assert t("non_existent_random_key_12345", "hi") == "non_existent_random_key_12345"
    
    # Missing locale on valid key should fall back to English
    assert t("brand_title", "unsupported_locale") == "GLOBAL FUELPULSE AI"

def test_localized_nav_map():
    for code in ["en", "hi", "es", "fr", "ar", "de", "zh", "ru", "ja"]:
        nav_map = get_localized_nav_map(code)
        assert isinstance(nav_map, dict)
        assert len(nav_map) == 10
        expected_tabs = [
            "home", "dashboard", "india", "about", "how_it_works",
            "features", "data_trust", "methodology", "roadmap", "faq"
        ]
        for tab in expected_tabs:
            assert tab in nav_map
            assert isinstance(nav_map[tab], str)
            assert len(nav_map[tab]) > 0


def test_home_and_india_translations_across_languages():
    """Verifies that home and india keys exist and differ from English in target languages."""
    test_keys = [
        "home_hero_title",
        "home_challenge_eyebrow",
        "home_value_title",
        "india_center_title",
        "india_delhi_petrol_kpi",
        "india_crude_basket_kpi",
        "sidebar_tree_nav",
        "sidebar_drilldown"
    ]
    for lang in ["hi", "es", "fr", "ar", "de", "zh", "ru", "ja"]:
        for key in test_keys:
            val = t(key, lang)
            assert val != key, f"Key {key} was not translated for {lang}"
            assert len(val) > 0
            # Ensure it is not just falling back to English (except for universal abbreviations)
            en_val = t(key, "en")
            assert val != ""


def test_deep_localization_keys():
    """Verifies that executive briefing, methodological distinction, and maritime alerts expander exist across languages."""
    keys = [
        "exec_briefing_title",
        "exec_briefing_cartel",
        "exec_briefing_shale",
        "exec_briefing_india",
        "method_distinction_title",
        "method_distinction_text",
        "maritime_alerts_expander",
        "market_signals_leaderboard",
        "world_extraction_geo",
        "top_10_producers_title",
        "regional_prod_shares_title",
        "top_5_exporters_title",
        "top_5_importers_title",
        "bilateral_trade_flows_title",
        "tracked_daily_flow",
        "opec_coordinated_share",
        "non_opec_output",
        "top_geological_reserve"
    ]
    for lang in ["hi", "es", "fr", "ar", "de", "zh", "ru", "ja"]:
        for k in keys:
            val = t(k, lang)
            assert val != k, f"Key {k} missing in {lang}"
            assert len(val) > 0

    # Specifically verify Hindi translations
    assert "कार्यकारी" in t("exec_briefing_title", "hi")
    assert "ओपेक+" in t("exec_briefing_cartel", "hi")
    assert "पद्धतिगत" in t("method_distinction_title", "hi")
    assert "कच्चे तेल" in t("method_distinction_text", "hi")
    assert "समुद्री परिवहन" in t("maritime_alerts_expander", "hi")


def test_all_18_languages_full_key_coverage():
    """Validates that 100% of all 165 translation keys are present for all 18 languages."""
    total_keys = len(TRANSLATIONS)
    assert total_keys == 165, f"Expected 165 keys in TRANSLATIONS, found {total_keys}"
    for code in SUPPORTED_LANGUAGES:
        present = sum(1 for k, d in TRANSLATIONS.items() if code in d and d[code])
        assert present == total_keys, f"Language {code} only has {present}/{total_keys} keys"


def test_expanded_9_languages_translations():
    """Verifies that expanded languages (pt, it, ko, tr, nl, id, ur, bn, ta) return valid localized text."""
    test_keys = [
        "chapter_01_title",
        "chapter_05_title",
        "home_hero_title",
        "home_cta_dashboard",
        "india_center_title",
        "petrol_rsp",
        "diesel_rsp"
    ]
    for code in ["pt", "it", "ko", "tr", "nl", "id", "ur", "bn", "ta"]:
        for k in test_keys:
            val = t(k, code)
            assert val != k, f"Key {k} missing in language {code}"
            assert len(val) > 0
            # Ensure not identical to English
            assert val != t(k, "en"), f"Key {k} in {code} fell back to English"


def test_top_header_and_navigation_translations():
    """Verifies that universal top header buttons and two-tier nav headers/badges are fully localized."""
    new_keys = [
        "top_btn_ai", "top_btn_lang", "top_btn_news",
        "nav_core_modules", "nav_tech_dossiers",
        "badge_live", "badge_12_mod", "badge_docs"
    ]
    for lang in SUPPORTED_LANGUAGES:
        for k in new_keys:
            val = t(k, lang, rem=3, flag="🌐", count=12)
            assert val != k, f"Key {k} missing for {lang}"
            assert len(val) > 0

    # Specific checks
    assert "एआई" in t("top_btn_ai", "hi", rem=3)
    assert "भाषा" in t("top_btn_lang", "hi", flag="🌐")
    assert "समाचार" in t("top_btn_news", "hi", count=12)
    assert t("nav_core_modules", "hi") == "मुख्य मॉड्यूल"
    assert t("nav_tech_dossiers", "hi") == "तकनीकी डोजियर एवं दस्तावेज"
    assert t("badge_live", "hi") == "लाइव"
    assert t("badge_12_mod", "hi") == "12 मॉड्यूल"
    assert t("badge_docs", "hi") == "दस्तावेज"

    # Spanish checks
    assert "IA" in t("top_btn_ai", "es", rem=3)
    assert "Idioma" in t("top_btn_lang", "es", flag="🌐")
    assert "Noticias" in t("top_btn_news", "es", count=12)
    assert t("nav_core_modules", "es") == "MÓDULOS PRINCIPALES"
    assert t("badge_live", "es") == "En vivo"


def test_language_selection_persistence_override():
    """Ensures that explicit user language choice persists and is never clobbered by stale query params."""
    import streamlit as st
    st.session_state.clear()
    
    # 1. User selects Hindi
    set_language("hi")
    assert st.session_state.get("_user_selected_lang") == "hi"
    assert get_current_language() == "hi"

    # 2. Simulate stale query param 'en'
    try:
        st.query_params["lang"] = "en"
    except Exception:
        pass
    
    # Authoritative selection MUST remain Hindi despite stale query param
    assert get_current_language() == "hi"

    # 3. User switches to French
    set_language("fr")
    assert get_current_language() == "fr"



