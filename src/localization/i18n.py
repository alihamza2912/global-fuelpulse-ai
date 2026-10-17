"""
GLOBAL FUELPULSE AI — MULTI-LANGUAGE LOCALIZATION (i18n) ENGINE
Comprehensive internationalization system supporting:
- English (EN - English)
- Hindi (HI - हिन्दी)
- Spanish (ES - Español)
- French (FR - Français)
- Arabic (AR - العربية)
- German (DE - Deutsch)
- Chinese (ZH - 简体中文)
- Russian (RU - Русский)
- Japanese (JA - 日本語)

Supports editorial UI ribbons, chapter narratives, navigation portals,
live benchmark telemetry, and maritime chokepoints.
"""

from typing import Dict, Any, Optional
import streamlit as st

# ==============================================================================
# 1. LANGUAGE CATALOG & REGISTRY
# ==============================================================================
SUPPORTED_LANGUAGES: Dict[str, Dict[str, str]] = {
    "en": {
        "code": "en",
        "name": "English",
        "native": "English",
        "flag": "🇬🇧",
        "dir": "ltr"
    },
    "hi": {
        "code": "hi",
        "name": "Hindi",
        "native": "हिन्दी",
        "flag": "🇮🇳",
        "dir": "ltr"
    },
    "es": {
        "code": "es",
        "name": "Spanish",
        "native": "Español",
        "flag": "🇪🇸",
        "dir": "ltr"
    },
    "fr": {
        "code": "fr",
        "name": "French",
        "native": "Français",
        "flag": "🇫🇷",
        "dir": "ltr"
    },
    "ar": {
        "code": "ar",
        "name": "Arabic",
        "native": "العربية",
        "flag": "🇸🇦",
        "dir": "rtl"
    },
    "de": {
        "code": "de",
        "name": "German",
        "native": "Deutsch",
        "flag": "🇩🇪",
        "dir": "ltr"
    },
    "zh": {
        "code": "zh",
        "name": "Chinese",
        "native": "简体中文",
        "flag": "🇨🇳",
        "dir": "ltr"
    },
    "ru": {
        "code": "ru",
        "name": "Russian",
        "native": "Русский",
        "flag": "🇷🇺",
        "dir": "ltr"
    },
    "ja": {
        "code": "ja",
        "name": "Japanese",
        "native": "日本語",
        "flag": "🇯🇵",
        "dir": "ltr"
    },
    "pt": {
        "code": "pt",
        "name": "Portuguese",
        "native": "Português",
        "flag": "🇧🇷",
        "dir": "ltr"
    },
    "it": {
        "code": "it",
        "name": "Italian",
        "native": "Italiano",
        "flag": "🇮🇹",
        "dir": "ltr"
    },
    "ko": {
        "code": "ko",
        "name": "Korean",
        "native": "한국어",
        "flag": "🇰🇷",
        "dir": "ltr"
    },
    "tr": {
        "code": "tr",
        "name": "Turkish",
        "native": "Türkçe",
        "flag": "🇹🇷",
        "dir": "ltr"
    },
    "nl": {
        "code": "nl",
        "name": "Dutch",
        "native": "Nederlands",
        "flag": "🇳🇱",
        "dir": "ltr"
    },
    "id": {
        "code": "id",
        "name": "Indonesian",
        "native": "Bahasa Indonesia",
        "flag": "🇮🇩",
        "dir": "ltr"
    },
    "ur": {
        "code": "ur",
        "name": "Urdu",
        "native": "اردو",
        "flag": "🇵🇰",
        "dir": "rtl"
    },
    "bn": {
        "code": "bn",
        "name": "Bengali",
        "native": "বাংলা",
        "flag": "🇧🇩",
        "dir": "ltr"
    },
    "ta": {
        "code": "ta",
        "name": "Tamil",
        "native": "தமிழ்",
        "flag": "🇮🇳",
        "dir": "ltr"
    }
}

# ==============================================================================
# 2. COMPREHENSIVE MULTI-LINGUAL TRANSLATION DICTIONARY
# ==============================================================================
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # --------------------------------------------------------------------------
    # TOP HEADER & BRAND LOCKUP
    # --------------------------------------------------------------------------
    "brand_title": {
        "en": "GLOBAL FUELPULSE AI",
        "hi": "ग्लोबल फ्यूलपल्स एआई",
        "es": "GLOBAL FUELPULSE AI",
        "fr": "GLOBAL FUELPULSE AI",
        "ar": "نبض الوقود العالمي بالذكاء الاصطناعي",
        "de": "GLOBAL FUELPULSE AI",
        "zh": "全球燃料脉搏 AI",
        "ru": "GLOBAL FUELPULSE AI",
        "ja": "グローバル・フューエルパルス AI",
        "pt": "GLOBAL FUELPULSE AI",
        "it": "GLOBAL FUELPULSE AI",
        "ko": "글로벌 퓨얼펄스 AI",
        "tr": "GLOBAL FUELPULSE AI",
        "nl": "GLOBAL FUELPULSE AI",
        "id": "GLOBAL FUELPULSE AI",
        "ur": "گلوبل فیول پلس اے آئی",
        "bn": "গ্লোবাল ফুয়েলপালস এআই",
        "ta": "குளோபல் ஃப்யூல் பல்ஸ் AI"
    },
    "brand_subtitle": {
        "en": "ENERGY INTELLIGENCE PLATFORM",
        "hi": "ऊर्जा खुफिया एवं बाजार विश्लेषण मंच",
        "es": "PLATAFORMA DE INTELIGENCIA ENERGÉTICA",
        "fr": "PLATEFORME D'INTELLIGENCE ÉNERGÉTIQUE",
        "ar": "منصة معلومات وأسواق الطاقة العالمية",
        "de": "ENERGIE-INTELLIGENZ-PLATTFORM",
        "zh": "能源情报与市场分析平台",
        "ru": "ПЛАТФОРМА ЭНЕРГЕТИЧЕСКОЙ РАЗВЕДКИ",
        "ja": "エネルギー市場情報プラットフォーム",
        "pt": "PLATAFORMA DE INTELIGÊNCIA ENERGÉTICA",
        "it": "PIATTAFORMA DI INTELLIGENZA ENERGETICA",
        "ko": "에너지 인텔리전스 및 시장 분석 플랫폼",
        "tr": "ENERJİ İSTİHBARAT PLATFORMU",
        "nl": "ENERGIE-INTELLIGENTIEPLATFORM",
        "id": "PLATFORM INTELIJEN ENERGI",
        "ur": "انرجی انٹیلیجنس اور مارکیٹ تجزیہ پلیٹ فارم",
        "bn": "এনার্জি ইন্টেলিজেন্স ও মার্কেট অ্যানালিটিক্স প্ল্যাটফর্ম",
        "ta": "ஆற்றல் நுண்ணறிவு மற்றும் சந்தை பகுப்பாய்வு தளம்"
    },
    "live_indicator": {
        "en": "LIVE 2026",
        "hi": "लाइव 2026",
        "es": "EN VIVO 2026",
        "fr": "EN DIRECT 2026",
        "ar": "مباشر 2026",
        "de": "LIVE 2026",
        "zh": "实时 2026",
        "ru": "В РЕАЛЬНОМ ВРЕМЕНИ 2026",
        "ja": "ライブ 2026",
        "pt": "AO VIVO 2026",
        "it": "IN TEMPO REALE 2026",
        "ko": "실시간 2026",
        "tr": "CANLI 2026",
        "nl": "LIVE 2026",
        "id": "LANGSUNG 2026",
        "ur": "براہ راست 2026",
        "bn": "লাইভ ২০২৬",
        "ta": "நேரலை 2026"
    },
    "db_verified": {
        "en": "SQLITE VERIFIED",
        "hi": "एसक्यूलाइट सत्यापित",
        "es": "SQLITE VERIFICADO",
        "fr": "SQLITE VÉRIFIÉ",
        "ar": "تم التحقق من قاعدة البيانات",
        "de": "SQLITE VERIFIZIERT",
        "zh": "SQLITE 已验证",
        "ru": "SQLITE ПРОВЕРЕНО",
        "ja": "SQLITE 検証済み",
        "pt": "SQLITE VERIFICADO",
        "it": "SQLITE VERIFICATO",
        "ko": "SQLITE 검증됨",
        "tr": "SQLITE DOĞRULANDI",
        "nl": "SQLITE GEVERIFIEERD",
        "id": "SQLITE TERVERIFIKASI",
        "ur": "تصدیق شدہ ایس کیو لائٹ",
        "bn": "এসকিউলাইট যাচাইকৃত",
        "ta": "SQLite சரிபார்க்கப்பட்டது"
    },
    "select_language": {
        "en": "Change Language",
        "hi": "भाषा बदलें",
        "es": "Cambiar Idioma",
        "fr": "Changer de Langue",
        "ar": "تغيير اللغة",
        "de": "Sprache Ändern",
        "zh": "切换语言",
        "ru": "Сменить язык",
        "ja": "言語を変更",
        "pt": "Alterar Idioma",
        "it": "Cambia Lingua",
        "ko": "언어 변경",
        "tr": "Dili Değiştir",
        "nl": "Taal Wijzigen",
        "id": "Ubah Bahasa",
        "ur": "زبان تبدیل کریں",
        "bn": "ভাষা পরিবর্তন করুন",
        "ta": "மொழியை மாற்றவும்"
    },
    "live_news_button": {
        "en": "LIVE NEWS",
        "hi": "लाइव समाचार",
        "es": "NOTICIAS EN VIVO",
        "fr": "ACTUALITÉS EN DIRECT",
        "ar": "أخبار عاجلة",
        "de": "LIVE-NACHRICHTEN",
        "zh": "实时快讯",
        "ru": "СВЕЖИЕ НОВОСТИ",
        "ja": "ライブニュース",
        "pt": "NOTÍCIAS AO VIVO",
        "it": "NOTIZIE IN DIRETTA",
        "ko": "실시간 뉴스",
        "tr": "CANLI HABERLER",
        "nl": "LIVE NIEUWS",
        "id": "BERITA TERKINI",
        "ur": "تازہ ترین خبریں",
        "bn": "লাইভ সংবাদ",
        "ta": "நேரலைச் செய்திகள்"
    },
    "refresh_feeds": {
        "en": "🔄 Refresh Feeds",
        "hi": "🔄 समाचार रीफ्रेश करें",
        "es": "🔄 Actualizar Fuentes",
        "fr": "🔄 Actualiser le Flux",
        "ar": "🔄 تحديث الأخبار",
        "de": "🔄 Feeds aktualisieren",
        "zh": "🔄 刷新情报",
        "ru": "🔄 Обновить ленту",
        "ja": "🔄 フィード更新",
        "pt": "🔄 Atualizar Notícias",
        "it": "🔄 Aggiorna Notizie",
        "ko": "🔄 뉴스 새로고침",
        "tr": "🔄 Akışı Yenile",
        "nl": "🔄 Feeds vernieuwen",
        "id": "🔄 Segarkan Berita",
        "ur": "🔄 خبریں تازہ کریں",
        "bn": "🔄 সংবাদ রিফ্রেশ করুন",
        "ta": "🔄 செய்திகளைப் புதுப்பிக்கவும்"
    },

    # --------------------------------------------------------------------------
    # MAIN TOPICS & EDITORIAL NAVIGATION PORTALS
    # --------------------------------------------------------------------------
    "nav_overview": {
        "en": "🏠 Overview",
        "hi": "🏠 अवलोकन",
        "es": "🏠 Panorama",
        "fr": "🏠 Aperçu",
        "ar": "🏠 نظرة عامة",
        "de": "🏠 Übersicht",
        "zh": "🏠 概览",
        "ru": "🏠 Обзор",
        "ja": "🏠 概要",
        "pt": "🏠 Visão Geral",
        "it": "🏠 Panoramica",
        "ko": "🏠 개요",
        "tr": "🏠 Genel Bakış",
        "nl": "🏠 Overzicht",
        "id": "🏠 Ikhtisar",
        "ur": "🏠 جائزہ",
        "bn": "🏠 সারসংক্ষেপ",
        "ta": "🏠 மேலோட்டம்"
    },
    "nav_dashboard": {
        "en": "⚡ Intelligence Dashboard",
        "hi": "⚡ इंटेलिजेंस डैशबोर्ड",
        "es": "⚡ Panel de Inteligencia",
        "fr": "⚡ Tableau de Bord",
        "ar": "⚡ لوحة معلومات الطاقة",
        "de": "⚡ Lagezentrum",
        "zh": "⚡ 市场智能仪表板",
        "ru": "⚡ Центр аналитики",
        "ja": "⚡ インテリジェンス・ダッシュボード",
        "pt": "⚡ Painel de Inteligência",
        "it": "⚡ Dashboard di Intelligence",
        "ko": "⚡ 인텔리전스 대시보드",
        "tr": "⚡ İstihbarat Paneli",
        "nl": "⚡ Intelligentiedashboard",
        "id": "⚡ Dasbor Intelijen",
        "ur": "⚡ انٹیلیجنس ڈیش بورڈ",
        "bn": "⚡ ইন্টেলিজেন্স ড্যাশবোর্ড",
        "ta": "⚡ நுண்ணறிவு பலகை"
    },
    "nav_india": {
        "en": "🇮🇳 India Fuel Center",
        "hi": "🇮🇳 भारत ईंधन केंद्र",
        "es": "🇮🇳 Centro de India",
        "fr": "🇮🇳 Centre Inde",
        "ar": "🇮🇳 مركز الوقود الهندي",
        "de": "🇮🇳 Indien-Zentrum",
        "zh": "🇮🇳 印度燃料中心",
        "ru": "🇮🇳 Центр топлива Индии",
        "ja": "🇮🇳 インド燃料センター",
        "pt": "🇮🇳 Centro de Combustível da Índia",
        "it": "🇮🇳 Centro Carburanti India",
        "ko": "🇮🇳 인도 연료 센터",
        "tr": "🇮🇳 Hindistan Yakıt Merkezi",
        "nl": "🇮🇳 India Brandstofcentrum",
        "id": "🇮🇳 Pusat Bahan Bakar India",
        "ur": "🇮🇳 بھارت فیول سینٹر",
        "bn": "🇮🇳 ভারত জ্বালানি কেন্দ্র",
        "ta": "🇮🇳 இந்திய எரிபொருள் மையம்"
    },
    "nav_trade": {
        "en": "🚢 Trade & Hormuz",
        "hi": "🚢 व्यापार व होर्मुज",
        "es": "🚢 Comercio y Ormuz",
        "fr": "🚢 Commerce et Ormuz",
        "ar": "🚢 التجارة ومضيق هرمز",
        "de": "🚢 Handel & Straße von Hormus",
        "zh": "🚢 原油贸易与霍尔木兹",
        "ru": "🚢 Торговля и Ормуз",
        "ja": "🚢 貿易とホルムズ海峡",
        "pt": "🚢 Comércio e Ormuz",
        "it": "🚢 Commercio e Hormuz",
        "ko": "🚢 무역 및 호르무즈",
        "tr": "🚢 Ticaret ve Hürmüz",
        "nl": "🚢 Handel & Straat van Hormuz",
        "id": "🚢 Perdagangan & Selat Hormuz",
        "ur": "🚢 تجارت اور آبنائے ہرمز",
        "bn": "🚢 বাণিজ্য ও হরমুজ প্রণালী",
        "ta": "🚢 வர்த்தகம் மற்றும் ஹார்முஸ்"
    },
    "nav_affordability": {
        "en": "⚖️ Affordability",
        "hi": "⚖️ मूल्य सामर्थ्य",
        "es": "⚖️ Asequibilidad",
        "fr": "⚖️ Abordabilité",
        "ar": "⚖️ القدرة على تحمل التكاليف",
        "de": "⚖️ Erschwinglichkeit",
        "zh": "⚖️ 燃料可负担性",
        "ru": "⚖️ Ценовая доступность",
        "ja": "⚖️ 燃料購入負担指数",
        "pt": "⚖️ Acessibilidade",
        "it": "⚖️ Accessibilità Prezzi",
        "ko": "⚖️ 연료 가격 부담도",
        "tr": "⚖️ Satın Alınabilirlik",
        "nl": "⚖️ Betaalbaarheid",
        "id": "⚖️ Keterjangkauan Harga",
        "ur": "⚖️ سکت اور قیمتیں",
        "bn": "⚖️ ক্রয়ক্ষমতা সূচক",
        "ta": "⚖️ மலிவுத்தன்மை"
    },
    "nav_supply_risk": {
        "en": "🛡️ Supply Risk",
        "hi": "🛡️ आपूर्ति जोखिम",
        "es": "🛡️ Riesgo de Suministro",
        "fr": "🛡️ Risque d'Approvisionnement",
        "ar": "🛡️ مخاطر الإمدادات",
        "de": "🛡️ Versorgungsrisiko",
        "zh": "🛡️ 供应集中度风险",
        "ru": "🛡️ Риск поставок",
        "ja": "🛡️ 供給リスク評価",
        "pt": "🛡️ Risco de Suprimento",
        "it": "🛡️ Rischio di Fornitura",
        "ko": "🛡️ 공급망 위험도",
        "tr": "🛡️ Tedarik Riski",
        "nl": "🛡️ Leveringsrisico",
        "id": "🛡️ Risiko Pasokan",
        "ur": "🛡️ رسد کا خطرہ",
        "bn": "🛡️ সরবরাহ ঝুঁকি",
        "ta": "🛡️ விநியோக இடர்"
    },
    "nav_shock_simulator": {
        "en": "⚡ Shock Simulator",
        "hi": "⚡ शॉक सिम्युलेटर",
        "es": "⚡ Simulador de Choque",
        "fr": "⚡ Simulateur de Choc",
        "ar": "⚡ محاكي صدمات الإمداد",
        "de": "⚡ Schock-Simulator",
        "zh": "⚡ 地缘供给冲击模拟器",
        "ru": "⚡ Симулятор шоков",
        "ja": "⚡ 供給ショック・シミュレーター",
        "pt": "⚡ Simulador de Choque",
        "it": "⚡ Simulatore di Shock",
        "ko": "⚡ 공급 충격 시뮬레이터",
        "tr": "⚡ Şok Simülatörü",
        "nl": "⚡ Schoksimulator",
        "id": "⚡ Simulator Guncangan",
        "ur": "⚡ سپلائی شاک سمیلیٹر",
        "bn": "⚡ সরবরাহ শক সিমুলেটর",
        "ta": "⚡ விநியோக அதிர்ச்சி மாதிரி"
    },
    "nav_forecasting": {
        "en": "📈 Forecasting",
        "hi": "📈 मूल्य पूर्वानुमान",
        "es": "📈 Pronósticos",
        "fr": "📈 Prévisions",
        "ar": "📈 التنبؤ بالأسعار",
        "de": "📈 Preisprognosen",
        "zh": "📈 价格预测模型",
        "ru": "📈 Прогнозирование цен",
        "ja": "📈 価格予測レーダー",
        "pt": "📈 Previsões",
        "it": "📈 Previsioni",
        "ko": "📈 가격 전망",
        "tr": "📈 Fiyat Tahmini",
        "nl": "📈 Prijsvoorspellingen",
        "id": "📈 Prakiraan Harga",
        "ur": "📈 قیمتوں کی پیش گوئی",
        "bn": "📈 মূল্য পূর্বাভাস",
        "ta": "📈 விலை முன்னறிவிப்பு"
    },
    "nav_data_trust": {
        "en": "🔒 Data Trust",
        "hi": "🔒 डेटा प्रमाणिकता",
        "es": "🔒 Confianza de Datos",
        "fr": "🔒 Confiance des Données",
        "ar": "🔒 موثوقية البيانات",
        "de": "🔒 Datenintegrität",
        "zh": "🔒 数据可信度与审计",
        "ru": "🔒 Достоверность данных",
        "ja": "🔒 データ信頼性センター",
        "pt": "🔒 Confiança de Dados",
        "it": "🔒 Fiducia nei Dati",
        "ko": "🔒 데이터 신뢰성",
        "tr": "🔒 Veri Güvenilirliği",
        "nl": "🔒 Gegevensbetrouwbaarheid",
        "id": "🔒 Kepercayaan Data",
        "ur": "🔒 ڈیٹا پر اعتماد",
        "bn": "🔒 ডেটা নির্ভরযোগ্যতা",
        "ta": "🔒 தரவு நம்பகத்தன்மை"
    },
    "nav_ai_analyst": {
        "en": "🤖 AI Analyst",
        "hi": "🤖 एआई ऊर्जा विश्लेषक",
        "es": "🤖 Analista IA",
        "fr": "🤖 Analyste IA",
        "ar": "🤖 محلل الذكاء الاصطناعي",
        "de": "🤖 KI-Analyst",
        "zh": "🤖 AI 能源市场分析师",
        "ru": "🤖 ИИ-аналитик",
        "ja": "🤖 AIエネルギーアナリスト",
        "pt": "🤖 Analista de IA",
        "it": "🤖 Analista IA",
        "ko": "🤖 AI 에너지 분석가",
        "tr": "🤖 Yapay Zeka Analisti",
        "nl": "🤖 AI-energieanalist",
        "id": "🤖 Analis AI",
        "ur": "🤖 اے آئی انرجی تجزیہ کار",
        "bn": "🤖 এআই এনার্জি বিশ্লেষক",
        "ta": "🤖 AI ஆற்றல் ஆய்வாளர்"
    },
    "nav_about": {
        "en": "📖 About Project",
        "hi": "📖 प्रोजेक्ट के बारे में",
        "es": "📖 Acerca del Proyecto",
        "fr": "📖 À Propos du Projet",
        "ar": "📖 حول المشروع",
        "de": "📖 Über das Projekt",
        "zh": "📖 关于项目",
        "ru": "📖 О проекте",
        "ja": "📖 プロジェクトについて",
        "pt": "📖 Sobre o Projeto",
        "it": "📖 Informazioni sul Progetto",
        "ko": "📖 프로젝트 소개",
        "tr": "📖 Proje Hakkında",
        "nl": "📖 Over het Project",
        "id": "📖 Tentang Proyek",
        "ur": "📖 منصوبے کے بارے میں",
        "bn": "📖 প্রকল্প সম্পর্কে",
        "ta": "📖 திட்டம் பற்றி"
    },
    "nav_how_it_works": {
        "en": "⚙️ How It Works",
        "hi": "⚙️ वास्तुकला व कार्यप्रणाली",
        "es": "⚙️ Cómo Funciona",
        "fr": "⚙️ Fonctionnement",
        "ar": "⚙️ كيف يعمل والنظام",
        "de": "⚙️ Funktionsweise",
        "zh": "⚙️ 系统架构与运作逻辑",
        "ru": "⚙️ Архитектура и работа",
        "ja": "⚙️ システム構造と動作原理",
        "pt": "⚙️ Como Funciona",
        "it": "⚙️ Come Funziona",
        "ko": "⚙️ 시스템 구조 및 원리",
        "tr": "⚙️ Nasıl Çalışır",
        "nl": "⚙️ Hoe Het Werkt",
        "id": "⚙️ Cara Kerja",
        "ur": "⚙️ یہ کیسے کام کرتا ہے",
        "bn": "⚙️ কীভাবে কাজ করে",
        "ta": "⚙️ செயல்படும் விதம்"
    },
    "nav_features": {
        "en": "📋 Features",
        "hi": "📋 सुविधाएं व क्षमताएं",
        "es": "📋 Características",
        "fr": "📋 Fonctionnalités",
        "ar": "📋 المميزات والقدرات",
        "de": "📋 Funktionsübersicht",
        "zh": "📋 核心功能全景目录",
        "ru": "📋 Возможности платформы",
        "ja": "📋 プラットフォーム機能一覧",
        "pt": "📋 Recursos",
        "it": "📋 Funzionalità",
        "ko": "📋 기능 목록",
        "tr": "📋 Özellikler",
        "nl": "📋 Functies",
        "id": "📋 Fitur",
        "ur": "📋 خصوصیات",
        "bn": "📋 সুবিধাসমূহ",
        "ta": "📋 அம்சங்கள்"
    },
    "nav_methodology": {
        "en": "📐 Methodology",
        "hi": "📐 गणितीय कार्यप्रणाली",
        "es": "📐 Metodología",
        "fr": "📐 Méthodologie",
        "ar": "📐 المنهجية الحسابية",
        "de": "📐 Methodik & Formeln",
        "zh": "📐 计算方法论与算法规范",
        "ru": "📐 Методология расчетов",
        "ja": "📐 算定手法とアルゴリズム",
        "pt": "📐 Metodologia",
        "it": "📐 Metodologia",
        "ko": "📐 방법론 및 알고리즘",
        "tr": "📐 Metodoloji",
        "nl": "📐 Methodologie",
        "id": "📐 Metodologi",
        "ur": "📐 طریقہ کار",
        "bn": "📐 কার্যপদ্ধতি",
        "ta": "📐 முறைமை"
    },
    "nav_roadmap": {
        "en": "🗺️ Roadmap",
        "hi": "🗺️ विकास रोडमैप",
        "es": "🗺️ Hoja de Ruta",
        "fr": "🗺️ Feuille de Route",
        "ar": "🗺️ خارطة الطريق المستقبلية",
        "de": "🗺️ Entwicklungs-Roadmap",
        "zh": "🗺️ 演进路线图与里程碑",
        "ru": "🗺️ Дорожная карта",
        "ja": "🗺️ ロードマップと開発計画",
        "pt": "🗺️ Roteiro",
        "it": "🗺️ Tabella di Marcia",
        "ko": "🗺️ 개발 로드맵",
        "tr": "🗺️ Yol Haritası",
        "nl": "🗺️ Routekaart",
        "id": "🗺️ Peta Jalan",
        "ur": "🗺️ روڈ میپ",
        "bn": "🗺️ রোডম্যাপ",
        "ta": "🗺️ திட்ட வரைபடம்"
    },
    "nav_faq": {
        "en": "❓ Docs & FAQ",
        "hi": "❓ दस्तावेज व सामान्य प्रश्न",
        "es": "❓ Documentación y FAQ",
        "fr": "❓ Documentation et FAQ",
        "ar": "❓ الأسئلة الشائعة والتوثيق",
        "de": "❓ Dokumentation & FAQ",
        "zh": "❓ 架构文档与常见疑问",
        "ru": "❓ Документация и FAQ",
        "ja": "❓ ドキュメントとよくある質問",
        "pt": "❓ Docs e FAQ",
        "it": "❓ Documentazione e FAQ",
        "ko": "❓ 문서 및 자주 묻는 질문",
        "tr": "❓ Belgeler ve SSS",
        "nl": "❓ Documentatie & FAQ",
        "id": "❓ Dokumentasi & FAQ",
        "ur": "❓ دستاویزات اور سوالات",
        "bn": "❓ নির্দেশিকা ও প্রশ্নোত্তর",
        "ta": "❓ ஆவணங்கள் மற்றும் கேள்விகள்"
    },

    # --------------------------------------------------------------------------
    # CHAPTER HEADERS & NARRATIVE TITLES (11 CHAPTERS)
    # --------------------------------------------------------------------------
    "chapter_01_title": {
        "en": "Global Energy at a Glance",
        "hi": "वैश्विक ऊर्जा परिदृश्य एक नज़र में",
        "es": "Energía Global de un Vistazo",
        "fr": "L'Énergie Mondiale en un Coup d'Œil",
        "ar": "نظرة عامة على الطاقة العالمية",
        "de": "Globale Energie auf einen Blick",
        "zh": "全球能源全景概览",
        "ru": "Мировая энергетика с первого взгляда",
        "ja": "世界エネルギー市場の概観"
    },
    "chapter_01_subtitle": {
        "en": "Primary macroeconomic indicators governing international energy trade, benchmark spot crude pricing, and structural reserves.",
        "hi": "अंतरराष्ट्रीय ऊर्जा व्यापार, बेंचमार्क कच्चे तेल के हाजिर मूल्य और संरचनात्मक भंडार को नियंत्रित करने वाले प्राथमिक व्यापक आर्थिक संकेतक।",
        "es": "Principales indicadores macroeconómicos que rigen el comercio internacional de energía y los precios del crudo.",
        "fr": "Principaux indicateurs macroéconomiques régissant le commerce international de l'énergie et les prix du brut.",
        "ar": "المؤشرات الاقتصادية الكلية الرئيسية التي تحكم تجارة الطاقة الدولية وأسعار النفط الخام الفورية.",
        "de": "Wichtigste makroökonomische Indikatoren für den internationalen Energiehandel und die Rohölpreise.",
        "zh": "主导国际能源贸易、基准原油现货价格以及地缘战略储备的核心宏观经济指标。",
        "ru": "Ключевые макроэкономические индикаторы, регулирующие мировую торговлю энергоносителями и цены на нефть.",
        "ja": "国際エネルギー貿易、原油スポット価格、および戦略的備蓄を決定づける主要なマクロ経済指標。"
    },
    "chapter_02_title": {
        "en": "Where the World Produces Oil",
        "hi": "दुनिया कहां तेल उत्पादन करती है",
        "es": "¿Dónde Produce Petróleo el Mundo?",
        "fr": "Où le Monde Produit-il du Pétrole ?",
        "ar": "أين ينتج العالم النفط؟",
        "de": "Wo die Welt Öl fördert",
        "zh": "全球石油生产地理分布",
        "ru": "Где в мире добывают нефть",
        "ja": "世界の石油生産拠点と埋蔵量"
    },
    "chapter_02_subtitle": {
        "en": "Crude extraction leaderboards, global cartel concentration (OPEC+ vs Non-OPEC), and geographical reserves.",
        "hi": "कच्चे तेल के निष्कर्षण की रैंकिंग, वैश्विक कार्टेल एकाग्रता (ओपेक+ बनाम गैर-ओपेक) और भौगोलिक भंडार।",
        "es": "Líderes de extracción de crudo, concentración de la OPEP+ frente a no OPEP y reservas mundiales.",
        "fr": "Classement de l'extraction de brut, concentration de l'OPEP+ vs Non-OPEP et réserves mondiales.",
        "ar": "قادة استخراج النفط الخام، وتحالف أوبك+ مقابل المنتجين المستقلين، والاحتياطيات الجغرافية.",
        "de": "Ranglisten der Rohölförderung, OPEC+ vs. Nicht-OPEC-Aufteilung und geologische Reserven.",
        "zh": "全球原油开采排行榜、OPEC+ 与非欧佩克产量对比以及地质战略储量。",
        "ru": "Лидеры добычи сырой нефти, баланс ОПЕК+ и независимых производителей, запасы недр.",
        "ja": "原油採掘リーダーボード、OPEC+と非加盟国のシェア比率、および地質学的埋蔵量。"
    },
    "chapter_03_title": {
        "en": "Who Exports and Who Imports?",
        "hi": "कौन निर्यात करता है और कौन आयात करता है?",
        "es": "¿Quién Exporta y Quién Importa?",
        "fr": "Qui Exporte et Qui Importe ?",
        "ar": "من يصدّر ومن يستورد؟",
        "de": "Wer exportiert und wer importiert?",
        "zh": "全球原油进出口双边贸易网络",
        "ru": "Кто экспортирует, а кто импортирует?",
        "ja": "石油輸出入国とサプライチェーン"
    },
    "chapter_03_subtitle": {
        "en": "Bilateral physical trade flows (HS 2709 Crude & HS 2710 Products), maritime bottleneck security, and supplier concentration.",
        "hi": "द्विपक्षीय भौतिक व्यापार प्रवाह (कच्चा तेल व रिफाइंड उत्पाद), समुद्री चोकपॉइंट सुरक्षा और आपूर्तिकर्ता एकाग्रता।",
        "es": "Flujos comerciales bilaterales, seguridad de cuellos de botella marítimos y concentración de proveedores.",
        "fr": "Flux commerciaux bilatéraux, sécurité des goulots d'étranglement maritimes et dépendance d'approvisionnement.",
        "ar": "تدفقات التجارة الثنائية، وأمن المضائق البحرية الاستراتيجية، وتركيز الموردين.",
        "de": "Bilaterale Handelsströme, maritime Engpass-Sicherheit und Lieferantenkonzentration.",
        "zh": "双边物理贸易流动（HS 2709 原油与 HS 2710 成品油）、海运咽喉安全与供应集中度。",
        "ru": "Двусторонние торговые потоки нефти, безопасность морских узлов и концентрация поставщиков.",
        "ja": "二国間物理貿易フロー（HS 2709 原油 / HS 2710 石油製品）、チョークポイントの海上安全保障。"
    },
    "chapter_04_title": {
        "en": "Follow the Fuel Price",
        "hi": "ईंधन की कीमतों का वैश्विक सफर",
        "es": "Siga el Precio del Combustible",
        "fr": "Suivez le Prix du Carburant",
        "ar": "تتبع أسعار الوقود",
        "de": "Folgen Sie dem Kraftstoffpreis",
        "zh": "全球终端零售燃油价格探索",
        "ru": "Следуйте за ценой на топливо",
        "ja": "世界各国の小売燃料価格比較"
    },
    "chapter_04_subtitle": {
        "en": "Retail petrol and diesel pump price comparison across 25+ economies: Fiscal taxation vs. domestic producer subsidies.",
        "hi": "25+ अर्थव्यवस्थाओं में पेट्रोल और डीजल के पंप मूल्यों की तुलना: राजकोषीय कर बनाम घरेलू उत्पादक सब्सिडी।",
        "es": "Comparativa de precios de gasolina y diésel en 25+ economías: Impuestos fiscales frente a subsidios.",
        "fr": "Comparaison des prix à la pompe de l'essence et du diesel dans 25+ économies : Fiscalité vs subventions.",
        "ar": "مقارنة أسعار البنزين والديزل في أكثر من 25 دولة: الضرائب المالية مقابل الدعم الحكومي.",
        "de": "Vergleich der Benzin- und Dieselpreise an Zapfsäulen in 25+ Volkswirtschaften: Steuern vs. Subventionen.",
        "zh": "横跨25+主要经济体的汽柴油泵价对比：主权税负重压与产油国国内补贴之鸿沟。",
        "ru": "Сравнение розничных цен на бензин и дизель в 25+ странах: Налогообложение против субсидий.",
        "ja": "主要25カ国以上のガソリン・軽油ポンプ価格比較：国家税負担 vs 産油国補助金。"
    },
    "chapter_05_title": {
        "en": "India's Petrol and Diesel Price",
        "hi": "भारत में पेट्रोल और डीजल की कीमतें",
        "es": "Precios de Gasolina y Diésel en India",
        "fr": "Prix de l'Essence et du Diesel en Inde",
        "ar": "أسعار البنزين والديزل في الهند",
        "de": "Benzin- und Dieselpreise in Indien",
        "zh": "印度各邦汽柴油零售价格与税收构成",
        "ru": "Цены на бензин и дизель в Индии",
        "ja": "インド各都市のガソリン・軽油価格と税構造"
    },
    "chapter_05_subtitle": {
        "en": "Daily price decomposition across Delhi and 28 States: Base refinery transfer, central excise, dealer margin, and state VAT.",
        "hi": "दिल्ली और 28 राज्यों में दैनिक मूल्य विश्लेषण: आधार रिफाइनरी लागत, केंद्रीय उत्पाद शुल्क, डीलर कमीशन और राज्य वैट।",
        "es": "Desglose diario de precios en Delhi y 28 estados: Precio base de refinería, impuestos centrales y margen.",
        "fr": "Décomposition quotidienne des prix à Delhi et dans 28 États : Prix de base, accises centrales et TVA d'État.",
        "ar": "تفصيل الأسعار اليومية في دلهي و28 ولاية هندية: سعر المصفاة الأساسي والضرائب وهوامش التجار.",
        "de": "Tägliche Preisaufschlüsselung in Delhi und 28 Bundesstaaten: Raffinerie-Basis, Verbrauchssteuer und Mehrwertsteuer.",
        "zh": "德里与印度28个邦的每日油价解构：炼油厂基础转让价、中央消费税、经销商佣金与邦增值税。",
        "ru": "Ежедневная разбивка цен в Дели и 28 штатах Индии: Базовая цена, акцизы и налог штата.",
        "ja": "デリーおよびインド28州の毎日の価格分解：精製原価、中央消費税、販売業者マージン、州付加価値税。"
    },
    "chapter_06_title": {
        "en": "India's Oil Companies",
        "hi": "भारत की तेल कंपनियां",
        "es": "Empresas Petroleras de India",
        "fr": "Compagnies Pétrolières en Inde",
        "ar": "شركات النفط في الهند",
        "de": "Indiens Ölkonzerne",
        "zh": "印度主要石油与石化企业",
        "ru": "Нефтяные компании Индии",
        "ja": "インドの主要石油企業と精製能力"
    },
    "chapter_06_subtitle": {
        "en": "Refining capacity, domestic retail distribution, market capitalization, and gross refining margins (GRM) across IOCL, BPCL, HPCL, and Reliance.",
        "hi": "आईओसीएल, बीपीसीएल, एचपीसीएल और रिलायंस में रिफाइनिंग क्षमता, खुदरा नेटवर्क, बाजार पूंजीकरण और सकल रिफाइनिंग मार्जिन।",
        "es": "Capacidad de refinación, distribución minorista y márgenes de refinación brutos de IOCL, BPCL, HPCL y Reliance.",
        "fr": "Capacités de raffinage, réseau de détail et marges brutes de raffinage d'IOCL, BPCL, HPCL et Reliance.",
        "ar": "طاقة التكرير وشبكات التجزئة وهوامش التكرير الإجمالية لشركات IOCL وBPCL وHPCL وReliance.",
        "de": "Raffineriekapazität, Tankstellennetz und Bruttomargen von IOCL, BPCL, HPCL und Reliance.",
        "zh": "IOCL、BPCL、HPCL及信实工业的炼油加工能力、零售加油站网络与综合炼油毛利分析。",
        "ru": "Мощности НПЗ, розничные сети и маржинальность переработки компаний IOCL, BPCL, HPCL и Reliance.",
        "ja": "IOCL、BPCL、HPCL、リライアンスの精製能力、小売スタンド網、精製マージン(GRM)。"
    },
    "chapter_07_title": {
        "en": "Where India Consumes Fuel",
        "hi": "भारत कहां ईंधन खपत करता है",
        "es": "¿Dónde Consume Combustible India?",
        "fr": "Où l'Inde Consomme-t-elle le Carburant ?",
        "ar": "أين تستهلك الهند الوقود؟",
        "de": "Wo Indien Kraftstoff verbraucht",
        "zh": "印度各邦汽柴油消费地理分布",
        "ru": "Где Индия потребляет топливо",
        "ja": "インド国内の燃料消費分布"
    },
    "chapter_07_subtitle": {
        "en": "Geographical distribution of motor spirit (petrol) and high-speed diesel (HSD) consumption across Indian states and union territories.",
        "hi": "भारतीय राज्यों और केंद्र शासित प्रदेशों में पेट्रोल और हाई-स्पीड डीजल की खपत का भौगोलिक वितरण।",
        "es": "Distribución geográfica del consumo de gasolina y diésel en los estados y territorios de la India.",
        "fr": "Répartition géographique de la consommation d'essence et de diesel dans les États et territoires indiens.",
        "ar": "التوزيع الجغرافي لاستهلاك البنزين والديزل عبر الولايات والأقاليم الهندية.",
        "de": "Geografische Verteilung des Benzin- und Dieselverbrauchs in indischen Bundesstaaten.",
        "zh": "印度各邦及中央直辖区汽油与高速柴油年度实际消耗规模地理热力图。",
        "ru": "Географическое распределение потребления бензина и дизельного топлива по штатам Индии.",
        "ja": "インド各州・連邦直辖地域におけるガソリンおよび軽油の地理的消費規模。"
    },
    "chapter_08_title": {
        "en": "Fuel Taxes and Government Revenue",
        "hi": "ईंधन कर और सरकारी राजस्व",
        "es": "Impuestos al Combustible e Ingresos Fiscales",
        "fr": "Taxes sur le Carburant et Recettes Publiques",
        "ar": "ضرائب الوقود والإيرادات الحكومية",
        "de": "Kraftstoffsteuern und Staatseinnahmen",
        "zh": "燃油税收结构与国家财政金库贡献",
        "ru": "Налоги на топливо и доходы бюджета",
        "ja": "燃料税制と政府歳入構造"
    },
    "chapter_08_subtitle": {
        "en": "Combined fiscal collection: Union government central excise contribution and state sales tax/VAT earnings from petroleum.",
        "hi": "संयुक्त राजकोषीय संग्रह: केंद्र सरकार का उत्पाद शुल्क योगदान और राज्यों की बिक्री कर/वैट कमाई।",
        "es": "Recaudación fiscal combinada: Aporte de impuestos centrales de la Unión e ingresos por IVA estatal.",
        "fr": "Recouvrement fiscal combiné : Droits d'accise centraux et recettes de TVA des États fédérés.",
        "ar": "التحصيل المالي الإجمالي: مساهمة المكوس المركزية وعائدات ضريبة القيمة المضافة للولايات.",
        "de": "Steueraufkommen: Zentrale Verbrauchssteuern und Mehrwertsteuereinnahmen der Bundesländer.",
        "zh": "央地综合财政收入解构：中央特别消费税与各邦增值税对石油产业链的财政汲取规模。",
        "ru": "Совокупные фискальные поступления: Доля центральных акцизов и доходы штатов от НДС на нефтепродукты.",
        "ja": "政府総合歳入：連邦中央消費税および各州付加価値税(VAT)による石油財政収入。"
    },
    "chapter_09_title": {
        "en": "Energy Risk and Affordability",
        "hi": "ऊर्जा जोखिम और वहनीयता",
        "es": "Riesgo Energético y Asequibilidad",
        "fr": "Risque Énergétique et Abordabilité",
        "ar": "مخاطر الطاقة والقدرة على تحمل التكاليف",
        "de": "Energierisiko und Erschwinglichkeit",
        "zh": "国家能源安全脆弱度与民生负担评估",
        "ru": "Энергетический риск и доступность цен",
        "ja": "エネルギー地政学リスクと国民購入負担"
    },
    "chapter_09_subtitle": {
        "en": "Evaluating energy import vulnerability: Net import dependency ratio, supplier concentration (HHI index), and fuel cost as % of daily income.",
        "hi": "आयात भेद्यता का मूल्यांकन: शुद्ध आयात निर्भरता अनुपात, आपूर्तिकर्ता एकाग्रता (एचएचआई) और दैनिक आय के प्रतिशत के रूप में ईंधन लागत।",
        "es": "Evaluación de vulnerabilidad de importaciones: Dependencia neta, concentración HHI y costo sobre ingreso diario.",
        "fr": "Évaluation de la vulnérabilité aux importations : Dépendance nette, indice HHI et part du revenu quotidien.",
        "ar": "تقييم مخاطر الاستيراد: نسبة الاعتماد الصافي، ومؤشر تركيز الموردين، وتكلفة الوقود من الدخل اليومي.",
        "de": "Bewertung der Importanfälligkeit: Importabhängigkeitsquote, Lieferantenkonzentration (HHI) und Anteil am Einkommen.",
        "zh": "国家原油对外依存度（88.2%）、HHI 进口来源国集中度指数与居民日均油费支出压力。",
        "ru": "Оценка уязвимости импорта: Коэффициент чистой зависимости, индекс концентрации поставщиков HHI и доля в доходах.",
        "ja": "原油輸入脆弱性評価：純輸入依存率(88.2%)、供給国集中度(HHI)、日給に占める燃料費負担率。"
    },
    "chapter_10_title": {
        "en": "Simulate a Supply Cut",
        "hi": "आपूर्ति कटौती सिमुलेशन लैब",
        "es": "Simular un Corte de Suministro",
        "fr": "Simuler une Coupure d'Approvisionnement",
        "ar": "محاكاة انقطاع الإمدادات النفطية",
        "de": "Versorgungsunterbrechung simulieren",
        "zh": "地缘原油断供情景压力测试模拟",
        "ru": "Симуляция перебоев в поставках",
        "ja": "地政学原油供給途絶シミュレーション"
    },
    "chapter_10_subtitle": {
        "en": "Interactive geopolitical shock simulation: Model retail pump inflation and commercial fleet operating expenditures under bilateral trade disruptions.",
        "hi": "इंटरैक्टिव भू-राजनीतिक शॉक सिमुलेशन: व्यापार व्यवधानों के तहत खुदरा पंप मुद्रास्फीति और वाणिज्यिक बेड़े के खर्च का मॉडल।",
        "es": "Simulación interactiva de choque geopolítico: Inflación minorista y gasto de flotas comerciales ante disrupciones.",
        "fr": "Simulation interactive de choc géopolitique : Inflation à la pompe et surcoût pour les flottes commerciales.",
        "ar": "محاكاة الصدمات الجيوسياسية: نمذجة تضخم أسعار التجزئة ومصروفات الأساطيل التجارية عند اضطراب التجارة.",
        "de": "Interaktive Simulation geopolitischer Schocks: Modellierung von Zapfsäuleninflation und Flottenkosten.",
        "zh": "交互式双边地缘断供模型：动态测算断供情景下的终端零售泵价涨幅及25万辆商用车队月度增支。",
        "ru": "Интерактивная симуляция геополитических шоков: Расчет инфляции на АЗС и расходов автопарков.",
        "ja": "地政学的ショック・シミュレーション：供給途絶時の小売ポンプ価格上昇率と商用車群の月次コスト試算。"
    },
    "chapter_11_title": {
        "en": "Data Pipelines and Quality Audits",
        "hi": "डेटा पाइपलाइन और गुणवत्ता ऑडिट",
        "es": "Pipelines de Datos y Auditorías de Calidad",
        "fr": "Pipelines de Données et Audits de Qualité",
        "ar": "أنابيب البيانات وتدقيق الجودة",
        "de": "Datenpipelines und Qualitätsprüfungen",
        "zh": "自动化数据管道与数据完整性审计",
        "ru": "Конвейеры данных и аудит качества",
        "ja": "データパイプラインと品質監査証明"
    },
    "chapter_11_subtitle": {
        "en": "Automated ETL ingestion provenance, data freshness SLAs, outlier quarantine audits, and relational schema validation.",
        "hi": "स्वचालित ईटीएल डेटा स्रोत प्रमाणिकता, डेटा ताजगी एसएलए, असामान्य डेटा संगरोध ऑडिट और संबंधपरक स्कीमा सत्यापन।",
        "es": "Trazabilidad ETL automatizada, SLA de frescura de datos, auditorías de anomalías y validación de esquemas.",
        "fr": "Traçabilité ETL automatisée, SLA de fraîcheur des données, audits de quarantaine et validation de schémas.",
        "ar": "سلاسل معالجة البيانات المؤتمتة، واتفاقيات مستوى حداثة البيانات، وتدقيق الجودة، والتحقق من المخطط العلائقي.",
        "de": "Automatisierte ETL-Verarbeitung, Datenfrische-SLAs, Quarantäneprüfungen und Schema-Validierung.",
        "zh": "自动化 ETL 摄取数据溯源、数据时效 SLA 履约率、异常值隔离审计与关系型数据仓库校验。",
        "ru": "Автоматизированные конвейеры ETL, SLA свежести данных, аудит карантина аномалий и проверка схем.",
        "ja": "自動ETLデータ系列追跡、データ鮮度SLA、異常値隔離監査、リレーショナルスキーマ整合性検証。"
    },

    # --------------------------------------------------------------------------
    # LIVE BENCHMARKS & DELHI TELEMETRY
    # --------------------------------------------------------------------------
    "delhi_headline": {
        "en": "DELHI TODAY (LIVE BENCHMARK)",
        "hi": "दिल्ली आज (लाइव बेंचमार्क)",
        "es": "DELHI HOY (REFERENCIA EN VIVO)",
        "fr": "DELHI AUJOURD'HUI (RÉFÉRENCE EN DIRECT)",
        "ar": "دلهي اليوم (المؤشر المباشر)",
        "de": "DELHI HEUTE (LIVE-REFERENZ)",
        "zh": "德里今日牌价（实时官方基准）",
        "ru": "ДЕЛИ СЕГОДНЯ (ОФИЦИАЛЬНЫЙ КУРС)",
        "ja": "デリー本日価格（リアルタイム公式基準）"
    },
    "petrol_rsp": {
        "en": "Petrol (Motor Spirit)",
        "hi": "पेट्रोल (मोटर स्पिरिट)",
        "es": "Gasolina (Motor Spirit)",
        "fr": "Essence (Super Sans Plomb)",
        "ar": "بنزين (ممتاز)",
        "de": "Benzin (Super E10)",
        "zh": "汽油 (95号/常规汽油)",
        "ru": "Бензин (АИ-95)",
        "ja": "レギュラーガソリン"
    },
    "diesel_rsp": {
        "en": "Diesel (High-Speed Diesel)",
        "hi": "डीजल (हाई-स्पीड डीजल)",
        "es": "Diésel (HSD)",
        "fr": "Diesel (Gazole)",
        "ar": "ديزل (عالي السرعة)",
        "de": "Dieselkraftstoff",
        "zh": "柴油 (高速柴油)",
        "ru": "Дизельное топливо",
        "ja": "軽油 (ディーゼル)"
    },
    "base_refinery_price": {
        "en": "Base Refinery Transfer",
        "hi": "आधार रिफाइनरी स्थानांतरण मूल्य",
        "es": "Transferencia Base de Refinería",
        "fr": "Prix de Base de Raffinerie",
        "ar": "سعر تحويل المصفاة الأساسي",
        "de": "Raffinerie-Basispreis",
        "zh": "炼油厂基准转让出厂价",
        "ru": "Базовая цена НПЗ",
        "ja": "製油所基礎出荷価格"
    },
    "central_excise": {
        "en": "Central Excise Duty",
        "hi": "केंद्रीय उत्पाद शुल्क",
        "es": "Impuesto Especial Central",
        "fr": "Droit d'Accise Central",
        "ar": "رسوم المكوس المركزية",
        "de": "Zentrale Verbrauchssteuer",
        "zh": "中央政府特别消费税",
        "ru": "Центральный акцизный сбор",
        "ja": "中央揮発油税"
    },
    "state_vat": {
        "en": "State VAT / Sales Tax",
        "hi": "राज्य वैट / बिक्री कर",
        "es": "IVA Estatal / Impuesto sobre Ventas",
        "fr": "TVA d'État / Taxe sur les Ventes",
        "ar": "ضريبة القيمة المضافة للولاية",
        "de": "Landes-Mehrwertsteuer",
        "zh": "邦增值税 (State VAT)",
        "ru": "НДС штата",
        "ja": "地方州消費税"
    },
    "dealer_commission": {
        "en": "Dealer Commission",
        "hi": "डीलर कमीशन",
        "es": "Comisión del Distribuidor",
        "fr": "Commission du Distributeur",
        "ar": "عمولة تاجر التجزئة",
        "de": "Händlerprovision",
        "zh": "加油站经销商佣金",
        "ru": "Комиссия дилера",
        "ja": "販売店取扱手数料"
    },
    "tax_wedge_pct": {
        "en": "Combined Govt Tax Wedge",
        "hi": "कुल सरकारी कर हिस्सा",
        "es": "Carga Fiscal Gubernamental Total",
        "fr": "Prélèvement Fiscal Total",
        "ar": "إجمالي العبء الضريبي الحكومي",
        "de": "Gesamter staatlicher Steuerkeil",
        "zh": "政府综合税费占比",
        "ru": "Совокупная налоговая нагрузка",
        "ja": "政府公租公課負担率"
    },

    # --------------------------------------------------------------------------
    # MARITIME CHOKEPOINTS & HORMUZ TELEMETRY
    # --------------------------------------------------------------------------
    "chokepoints_header": {
        "en": "🚨 Global Maritime Chokepoints & Seaborne Transport Bottlenecks",
        "hi": "🚨 वैश्विक समुद्री चोकपॉइंट्स व समुद्री परिवहन बाधाएं",
        "es": "🚨 Cuellos de Botella Marítimos Globales y Transporte de Crudo",
        "fr": "🚨 Goulots d'Étranglement Maritimes et Transport Mondial",
        "ar": "🚨 المضائق البحرية العالمية وعوائق النقل البحري",
        "de": "🚨 Globale maritime Engpässe und Seetransport-Blockaden",
        "zh": "🚨 全球原油海运咽喉要道与战略运输瓶颈",
        "ru": "🚨 Мировые морские узлы и транспортные узкие места",
        "ja": "🚨 世界の海上チョークポイントとタンカー輸送ボトルネック"
    },
    "chokepoints_caption": {
        "en": "Real-time AIS tanker throughput, Strait of Hormuz naval alerts, Red Sea rerouting impacts, and strategic bypass pipeline capacities.",
        "hi": "वास्तविक समय एआईएस टैंकर थ्रूपुट, होर्मुज जलडमरूमध्य नौसैनिक अलर्ट, लाल सागर मार्ग परिवर्तन प्रभाव और रणनीतिक बाईपास पाइपलाइन क्षमता।",
        "es": "Tránsito de buques cisterna en tiempo real, alertas en Ormuz, desvíos en el Mar Rojo y oleoductos de contingencia.",
        "fr": "Flux de pétroliers AIS en temps réel, alertes dans le détroit d'Ormuz, déviations par la Mer Rouge et capacités d'évitement.",
        "ar": "رصد ناقلات النفط عبر الأقمار الصناعية، وتنبيهات مضيق هرمز البحرية، وتحويلات البحر الأحمر، وقدرات خطوط الأنابيب البديلة.",
        "de": "Echtzeit-Tankerüberwachung, Marine-Warnungen in der Straße von Hormus, Rotes-Meer-Umleitungen und Notfallpipelines.",
        "zh": "实时 AIS 油轮吞吐量追踪、霍尔木兹海峡海军战备巡逻、红海绕航好望角影响及战略绕行管道负荷。",
        "ru": "Спутниковый мониторинг танкеров, оповещения в Ормузском проливе, обходные пути Красного моря и нефтепроводы.",
        "ja": "リアルタイムAISタンカー航行量、ホルムズ海峡の海上警戒、紅海・喜望峰迂回影響、バイパスパイプライン稼働率。"
    },
    "risk_index": {
        "en": "Risk Index",
        "hi": "जोखिम सूचकांक",
        "es": "Índice de Riesgo",
        "fr": "Indice de Risque",
        "ar": "مؤشر المخاطر",
        "de": "Risikoindex",
        "zh": "风险指数",
        "ru": "Индекс риска",
        "ja": "地政学的リスク指数"
    },
    "key_threat": {
        "en": "Key Threat",
        "hi": "मुख्य खतरा",
        "es": "Amenaza Principal",
        "fr": "Menace Principale",
        "ar": "التهديد الرئيسي",
        "de": "Hauptbedrohung",
        "zh": "核心威胁",
        "ru": "Основная угроза",
        "ja": "主要な航行脅威"
    },
    "bypass_pipeline": {
        "en": "Bypass Pipeline",
        "hi": "बाईपास पाइपलाइन मार्ग",
        "es": "Oleoducto de Desvío",
        "fr": "Oléoduc de Contournement",
        "ar": "خط أنابيب الالتفاف",
        "de": "Bypass-Pipeline",
        "zh": "应急绕行输油管道",
        "ru": "Обходной нефтепровод",
        "ja": "緊急迂回パイプライン"
    },

    # --------------------------------------------------------------------------
    # EXECUTIVE BRIEFING & METHODOLOGY CALLOUTS
    # --------------------------------------------------------------------------
    "exec_briefing_title": {
        "en": "EXECUTIVE BRIEFING:",
        "hi": "कार्यकारी ब्रीफिंग (संक्षेप):",
        "es": "INFORME EJECUTIVO:",
        "fr": "RAPPORT EXÉCUTIF :",
        "ar": "موجز تنفيذي:",
        "de": "EXECUTIVE BRIEFING:",
        "zh": "高层决策简报：",
        "ru": "ОПЕРАТИВНЫЙ БРИФИНГ:",
        "ja": "エグゼクティブ・サマリー:",
        "pt": "RESUMO EXECUTIVO:",
        "it": "INFORMATIVA ESECUTIVA:",
        "ko": "경영진 요약 보고:",
        "tr": "YÖNETİCİ BİLGİLENDİRMESİ:",
        "nl": "EXECUTIVE BRIEFING:",
        "id": "RINGKASAN EKSEKUTIF:",
        "ur": "ایگزیکٹو بریفنگ:",
        "bn": "নির্বাহী ব্রিফিং:",
        "ta": "நிர்வாக சுருக்கம்:"
    },
    "exec_briefing_cartel": {
        "en": "Cartel Dynamics: OPEC+ nations coordinate ~55% of world tracked oil supply, holding the largest low-cost swing capacity.",
        "hi": "कार्टेल गतिकी: ओपेक+ देश दुनिया की लगभग 55% ट्रैक की गई तेल आपूर्ति का समन्वय करते हैं, जिनके पास सबसे बड़ी कम लागत वाली स्विंग क्षमता है।",
        "es": "Dinámica del Cártel: Los países de la OPEP+ coordinan ~55% del suministro mundial de petróleo rastreado, manteniendo la mayor capacidad oscilante de bajo costo.",
        "fr": "Dynamique du Cartel : Les nations de l'OPEP+ coordonnent ~55% de l'offre pétrolière mondiale suivie, détenant la plus grande capacité d'ajustement à faible coût.",
        "ar": "ديناميكيات الكارتل: تنسق دول أوبك+ حوالي 55% من إمدادات النفط العالمية المرصودة، وتمتلك أكبر طاقة إنتاجية فائضة منخفضة التكلفة.",
        "de": "Kartelldynamik: Die OPEC+-Länder koordinieren ca. 55 % des weltweiten Ölangebots und verfügen über die größte kostengünstige Reservekapazität.",
        "zh": "卡特尔统筹：OPEC+ 核心成员国统筹全球约 55% 的在轨原油供应，掌握着全球规模最大的低边际成本弹性产能。",
        "ru": "Динамика картеля: Страны ОПЕК+ координируют около 55% мировых поставок нефти, удерживая основные недорогие резервные мощности.",
        "ja": "カルテル動向: OPEC+諸国は世界で追跡される石油供給の約55%を協調管理し、最大の低コスト調整余力を保持。",
        "pt": "Dinâmica do Cartel: Os países da OPEP+ coordenam ~55% da oferta mundial rastreada de petróleo, detendo a maior capacidade excedente de baixo custo.",
        "it": "Dinamica del Cartello: I paesi OPEC+ coordinano circa il 55% dell'offerta globale di petrolio tracciata, disponendo della maggiore capacità di riserva a basso costo.",
        "ko": "카르텔 역학: OPEC+ 국가는 전 세계 추적 석유 공급량의 약 55%를 조율하며 최대 규모의 저비용 잉여 생산 능력을 보유하고 있습니다.",
        "tr": "Kartel Dinamikleri: OPEC+ ülkeleri, dünya genelinde takip edilen petrol arzının ~%55'ini koordine etmekte ve en büyük düşük maliyetli esnek kapasiteyi elinde tutmaktadır.",
        "nl": "Karteldynamiek: OPEC+-landen coördineren circa 55% van het wereldwijd gevolgde olieaanbod en beschikken over de grootste goedkope reservecapaciteit.",
        "id": "Dinamika Kartel: Negara-negara OPEC+ mengoordinasikan ~55% pasokan minyak dunia yang dilacak, memegang kapasitas ayunan berbiaya rendah terbesar.",
        "ur": "کارٹل حرکیات: اوپیک پلس ممالک دنیا کی تقریباً 55 فیصد ٹریک شدہ تیل کی فراہمی کو مربوط کرتے ہیں، جس کے پاس سب سے بڑی کم لاگت سوئنگ صلاحیت ہے۔",
        "bn": "কার্টেল গতিশীলতা: ওপেক+ দেশগুলি বিশ্বের ট্র্যাক করা তেল সরবরাহের প্রায় ৫৫% সমন্বয় করে, যাদের সর্বাধিক স্বল্পমূল্যের সুইং ক্ষমতা রয়েছে।",
        "ta": "கார்டெல் இயக்கவியல்: ஒபெக்+ நாடுகள் உலகளாவிய கண்காணிக்கப்பட்ட எண்ணெய் விநியோகத்தில் ~55% ஒருங்கிணைத்து, மிகப்பெரிய குறைந்த செலவு உற்பத்தித் திறனைக் கொண்டுள்ளன."
    },
    "exec_briefing_shale": {
        "en": "US Shale Hegemony: The United States leads extraction with 13.2 mbpd, serving as the dominant non-OPEC pricing anchor.",
        "hi": "अमेरिकी शेल वर्चस्व: संयुक्त राज्य अमेरिका 13.2 mbpd के साथ उत्पादन में सबसे आगे है, जो प्रमुख गैर-ओपेक मूल्य निर्धारण आधार के रूप में कार्य करता है।",
        "es": "Hegemonía del Esquisto de EE. UU.: Estados Unidos lidera la extracción con 13.2 mbpd, sirviendo como el ancla dominante de precios fuera de la OPEP.",
        "fr": "Hégémonie du Schiste Américain : Les États-Unis dominent l'extraction avec 13,2 mbpd, servant de référence tarifaire hors-OPEP.",
        "ar": "هيمنة النفط الصخري الأمريكي: تتصدر الولايات المتحدة استخراج النفط بمعدل 13.2 مليون برميل/يوم، لتكون ركيزة التسعير المستقلة الرئيسية خارج أوبك.",
        "de": "US-Schieferöl-Vorherrschaft: Die Vereinigten Staaten führen die Förderung mit 13,2 mbpd an und dienen als wichtigster Nicht-OPEC-Preisanker.",
        "zh": "美页岩油霸权：美国以日产 13.2 百万桶居全球开采之首，充当着非欧佩克阵营最具定价话语权的锚定基石。",
        "ru": "Сланцевая гегемония США: США лидируют по добыче с 13,2 млн барр./сут, выступая главным независимым ценовым якорем вне ОПЕК.",
        "ja": "米シェール台頭: 米国は日量1320万バレルで採掘を牽引し、OPEC非加盟国における最大の価格形成アンカーとして機能。",
        "pt": "Hegemonia do Xisto dos EUA: Os Estados Unidos lideram a extração com 13,2 mbpd, servindo como a âncora dominante de preços fora da OPEP.",
        "it": "Egemonia dello Shale USA: Gli Stati Uniti guidano l'estrazione con 13,2 mbpd, fungendo da principale ancora di prezzo non-OPEC.",
        "ko": "미국 셰일 패권: 미국은 1,320만 bpd로 원유 추출을 선도하며 지배적인 비OPEC 가격 앵커 역할을 합니다.",
        "tr": "ABD Kayaç Hegemonyası: Amerika Birleşik Devletleri 13,2 mbpd ile çıkarmada lider konumda olup, OPEC dışı baskın fiyat çıpası vazifesi görmektedir.",
        "nl": "Amerikaanse Schalie-hegemonie: De Verenigde Staten leiden de winning met 13,2 mbpd en fungeren als het dominante niet-OPEC prijsanker.",
        "id": "Hegemoni Shale AS: Amerika Serikat memimpin ekstraksi dengan 13,2 mbpd, berfungsi sebagai jangkar harga non-OPEC yang dominan.",
        "ur": "امریکی شیل بالادستی: امریکہ 13.2 ایم بی پی ڈی کے ساتھ پیداوار میں سرفہرست ہے، جو غیر اوپیک کا بنیادی قیمت اینکر ہے۔",
        "bn": "মার্কিন শেল আধিপত্য: মার্কিন যুক্তরাষ্ট্র ১৩.২ এমবিপিডি নিয়ে উত্তোলনে শীর্ষে রয়েছে, যা প্রভাবশালী অ-ওপেক মূল্য নোঙ্গর হিসেবে কাজ করে।",
        "ta": "அமெரிக்க ஷேல் மேலாதிக்கம்: அமெரிக்கா 13.2 mbpd உடன் எண்ணெய் எடுப்பில் முன்னணியில் உள்ளது, இது ஒபெக் அல்லாத முக்கிய விலை நங்கூரமாக செயல்படுகிறது."
    },
    "exec_briefing_india": {
        "en": "India Geopolitics: 88.2% foreign crude intake makes national fiscal balances sensitive to freight corridors and crude swings.",
        "hi": "भारत भू-राजनीति: 88.2% विदेशी कच्चे तेल के आयात पर निर्भरता राष्ट्रीय वित्तीय संतुलन को समुद्री मार्गों और कच्चे तेल के उतार-चढ़ाव के प्रति संवेदनशील बनाती है।",
        "es": "Geopolítica de la India: El 88.2% de dependencia del crudo extranjero vuelve el balance fiscal nacional muy sensible a los fletes y la volatilidad.",
        "fr": "Géopolitique de l'Inde : 88,2% de dépendance au brut étranger rend les équilibres budgétaires très vulnérables aux corridors maritimes et au cours du brut.",
        "ar": "جيوسياسة الهند: 88.2% من واردات النفط الخام الأجنبي تجعل الميزان المالي الوطني شديد الحساسية لممرات الشحن وتقلبات الأسعار.",
        "de": "Geopolitik Indiens: 88,2 % Importabhängigkeit bei Rohöl machen den Staatshaushalt anfällig für Frachtkorridore und Preisschwankungen.",
        "zh": "印度地缘格局：88.2% 的原油外采依存度使印度国家财政收支对海运要道畅通度及现货油价波动极其敏感。",
        "ru": "Геополитика Индии: Зависимость от импорта сырой нефти на 88,2% делает фискальный баланс страны крайне уязвимым к логистике и скачкам цен.",
        "ja": "インドの地政学: 原油の88.2%を海外輸入に依存するため、海上輸送回廊や原油価格の変動が国家財政に直結。",
        "pt": "Geopolítica da Índia: 88,2% de dependência do petróleo bruto importado torna os saldos fiscais nacionais sensíveis aos corredores de frete e oscilações do petróleo.",
        "it": "Geopolitica dell'India: L'88,2% di greggio importato rende i bilanci fiscali nazionali vulnerabili ai corridoi marittimi e alle oscillazioni del greggio.",
        "ko": "인도 지정학: 88.2%의 해외 원유 수입 의존도로 인해 인도 국가 재정 수지는 해상 운송로와 유가 변동에 매우 민감합니다.",
        "tr": "Hindistan Jeopolitiği: %88,2 yabancı ham petrol alımı, ulusal mali dengeleri navlun koridorlarına ve petrol dalgalanmalarına karşı duyarlı kılmaktadır.",
        "nl": "Geopolitiek van India: 88,2% afhankelijkheid van buitenlandse ruwe olie maakt nationale begrotingssaldi kwetsbaar voor vrachtcorridors en olieschommelingen.",
        "id": "Geopolitik India: 88,2% asupan minyak mentah asing membuat neraca fiskal nasional sangat sensitif terhadap koridor pengiriman dan fluktuasi minyak mentah.",
        "ur": "ہندوستان کی جغرافیائی سیاست: 88.2 فیصد غیر ملکی خام تیل پر انحصار قومی مالیاتی توازن کو بحری راہداریوں اور قیمتوں کے لیے حساس بناتا ہے۔",
        "bn": "ভারতের ভূ-রাজনীতি: ৮৮.২% বিদেশী অপরিশোধিত তেল গ্রহণের ফলে জাতীয় রাজস্ব ভারসাম্য মালবাহী করিডোর এবং তেলের ওঠানামার প্রতি সংবেদনশীল।",
        "ta": "இந்திய புவிசார் அரசியல்: 88.2% வெளிநாட்டு கச்சா எண்ணெய் இறக்குமதி சார்ந்து இருப்பது, தேசிய நிதி இருப்பை கப்பல் பாதைகள் மற்றும் கச்சா எண்ணெய் ஏற்ற இறக்கங்களுக்கு மிகவும் உணர்திறன் கொண்டதாக மாற்றுகிறது."
    },
    "method_distinction_title": {
        "en": "METHODOLOGICAL DISTINCTION:",
        "hi": "पद्धतिगत स्पष्टीकरण (विधि):",
        "es": "DISTINCIÓN METODOLÓGICA:",
        "fr": "DISTINCTION MÉTHODOLOGIQUE :",
        "ar": "التمايز المنهجي والمحاسبي:",
        "de": "METHODISCHE ABGRENZUNG:",
        "zh": "统计口径与方法论界定：",
        "ru": "МЕТОДОЛОГИЧЕСКОЕ РАЗГРАНИЧЕНИЕ:",
        "ja": "統計手法・計量基準の明確化:",
        "pt": "DISTINÇÃO METODOLÓGICA:",
        "it": "DISTINZIONE METODOLOGICA:",
        "ko": "방법론적 구분 및 통계 기준:",
        "tr": "METODOLOJİK AYRIM:",
        "nl": "METHODOLOGISCH ONDERSCHEID:",
        "id": "PERBEDAAN METODOLOGI:",
        "ur": "طریقہ کار کا فرق:",
        "bn": "পদ্ধতিগত পার্থক্য:",
        "ta": "முறைசார் வேறுபாடு:"
    },
    "method_distinction_text": {
        "en": "This dataset strictly accounts for crude oil and lease condensate. It explicitly excludes Natural Gas Liquids (NGLs), refinery processing gains, and biofuels. Proven reserves represent underground resources recoverable under current economic and operating conditions, whereas production measures active daily extraction rate.",
        "hi": "यह डेटासेट केवल कच्चे तेल और लीज घनीभूत (कंडेनसेट) का हिसाब रखता है। इसमें प्राकृतिक गैस तरल (NGLs), रिफाइनरी प्रसंस्करण लाभ और जैव ईंधन शामिल नहीं हैं। सिद्ध भंडार उन भूमिगत संसाधनों का प्रतिनिधित्व करते हैं जो वर्तमान आर्थिक और परिचालन स्थितियों के तहत पुनर्प्राप्त करने योग्य हैं, जबकि उत्पादन सक्रिय दैनिक निष्कर्षण दर को मापता है।",
        "es": "Este conjunto de datos contabiliza estrictamente el petróleo crudo y el condensado de arrendamiento. Excluye explícitamente los líquidos de gas natural (LGN), las ganancias de procesamiento de refinería y los biocombustibles. Las reservas probadas representan recursos subterráneos recuperables en condiciones económicas y operativas actuales, mientras que la producción mide la tasa de extracción diaria activa.",
        "fr": "Ce jeu de données comptabilise strictement le pétrole brut et les condensats de bail. Il exclut explicitement les liquides de gaz naturel (LGN), les gains de traitement en raffinerie et les biocarburants. Les réserves prouvées représentent les ressources souterraines récupérables dans les conditions économiques et opérationnelles actuelles, tandis que la production mesure le taux d'extraction quotidien actif.",
        "ar": "هذه المجموعة من البيانات مخصصة بدقة للنفط الخام والمكثفات البترولية فقط. وتستثني صراحة سوائل الغاز الطبيعي (NGLs)، ومكاسب معالجة المصافي، والوقود الحيوي. تمثل الاحتياطيات المؤكدة الموارد الجوفية القابلة للاستخراج في ظل الظروف الاقتصادية والتشغيلية الحالية، بينما يقيس الإنتاج معدل الاستخراج اليومي الفعلي.",
        "de": "Dieser Datensatz erfasst ausschließlich Rohöl und Kondensat. Ausdrücklich ausgeschlossen sind Flüssiggase (NGL), Raffineriegewinne und Biokraftstoffe. Nachgewiesene Reserven stellen unterirdische Ressourcen dar, die unter aktuellen wirtschaftlichen und betrieblichen Bedingungen förderbar sind, während die Produktion die tägliche Fördermenge misst.",
        "zh": "本核算数据集严格界定为原油及租赁凝析油（Crude Oil & Lease Condensate）。已明确排除天然气凝析液（NGLs）、炼油厂加工增益及生物燃料。已探明储量代表在现行商业经济与开采技术条件下具备商业开采价值的地下储集资产，而开采量则度量每日活跃物理采出速率。",
        "ru": "В данном наборе данных строго учитываются сырая нефть и арендный конденсат. Из него исключены широкие фракции легких углеводородов (ШФЛУ/NGL), технологический прирост НПЗ и биотопливо. Доказанные запасы представляют собой извлекаемые ресурсы при текущих экономических условиях, а добыча отражает фактический суточный дебит.",
        "ja": "本データセットは原油およびリースコンデンセートのみを厳密に集計しています。天然ガス液（NGL）、製油所精製利得、バイオ燃料は除外されています。確認埋蔵量は現在の経済的・操業条件下で回収可能な地下資源を示し、生産量は日々の物理的採掘量を測定しています。",
        "pt": "Este conjunto de dados contabiliza estritamente o petróleo bruto e o condensado de arrendamento. Exclui explicitamente líquidos de gás natural (LGN), ganhos de processamento em refinarias e biocombustíveis. As reservas provadas representam recursos subterrâneos recuperáveis sob condições econômicas e operacionais vigentes, enquanto a produção mede a taxa diária de extração ativa.",
        "it": "Questo set di dati contabilizza rigorosamente il petrolio greggio e il condensato di giacimento. Esclude esplicitamente i liquidi di gas naturale (NGL), i guadagni di raffinazione e i biocarburanti. Le riserve accertate rappresentano risorse sotterranee recuperabili alle attuali condizioni economiche, mentre la produzione misura il tasso di estrazione attivo.",
        "ko": "이 데이터세트는 원유와 리스 콘덴세이트만을 엄격하게 집계합니다. 천연가스액(NGL), 정유소 공정 증분 및 바이오연료는 명시적으로 제외됩니다. 확인 매장량은 현재의 경제적·운영 조건 하에서 회수 가능한 지하 자원을 의미하며, 생산량은 일일 활성 물리적 추출 속도를 측정합니다.",
        "tr": "Bu veri seti yalnızca ham petrol ve kira kondensatını hesaba katmaktadır. Doğal Gaz Sıvıları (NGL), rafineri işleme kazançları ve biyoyakıtları açıkça hariç tutar. Kanıtlanmış rezervler mevcut ekonomik ve işletme koşullarında geri kazanılabilir yeraltı kaynaklarını temsil ederken, üretim aktif günlük çıkarma hızını ölçer.",
        "nl": "Deze dataset houdt strikt rekening met ruwe olie en leasecondensaat. Het sluit expliciet vloeibare aardgassen (NGL's), raffinageverwerkingswinsten en biobrandstoffen uit. Bewezen reserves vertegenwoordigen ondergrondse hulpbronnen die onder de huidige economische en operationele omstandigheden winbaar zijn, terwijl productie de actieve dagelijkse winningssnelheid meet.",
        "id": "Kumpulan data ini secara ketat memperhitungkan minyak mentah dan kondensat sewa. Secara eksplisit mengecualikan Cairan Gas Alam (NGL), keuntungan pemrosesan kilang, dan biofuel. Cadangan terbukti mewakili sumber daya bawah tanah yang dapat dipulihkan dalam kondisi ekonomi dan operasional saat ini, sedangkan produksi mengukur laju ekstraksi harian yang aktif.",
        "ur": "یہ ڈیٹا سیٹ سختی سے خام تیل اور لیز کنڈینسیٹ کا حساب رکھتا ہے۔ اس میں قدرتی گیس کے مائعات (NGLs)، ریفائنری پروسیسنگ کے فوائد اور بائیو فیول شامل نہیں ہیں۔ ثابت شدہ ذخائر زیر زمین وسائل کی نمائندگی کرتے ہیں جو موجودہ معاشی اور آپریشنل حالات کے تحت قابل بازیابی ہیں، جبکہ پیداوار روزانہ فعال نکالنے کی شرح کی پیمائش کرتی ہے۔",
        "bn": "এই ডেটাসেট কঠোরভাবে অপরিশোধিত তেল এবং লিজ কনডেনসেটের হিসাব রাখে। এটি স্পষ্টভাবে প্রাকৃতিক গ্যাস তরল (NGLs), শোধনাগার প্রক্রিয়াকরণ লাভ এবং জৈব জ্বালানি বাদ দেয়। প্রমাণিত মজুদ বর্তমান অর্থনৈতিক এবং পরিচালন পরিস্থিতিতে পুনরুদ্ধারযোগ্য ভূগর্ভস্থ সম্পদের প্রতিনিধিত্ব করে, যখন উৎপাদন সক্রিয় দৈনিক নিষ্কাশন হার পরিমাপ করে।",
        "ta": "இந்த தரவுத்தொகுப்பு கச்சா எண்ணெய் மற்றும் குத்தகை மின்தேக்கியை மட்டுமே துல்லியமாக கணக்கிடுகிறது. இது இயற்கை எரிவாயு திரவங்கள் (NGLs), சுத்திகரிப்பு ஆலை செயலாக்க ஆதாயங்கள் மற்றும் உயிரி எரிபொருட்களை வெளிப்படையாக விலக்குகிறது. நிரூபிக்கப்பட்ட இருப்புக்கள் தற்போதைய பொருளாதார மற்றும் இயக்க நிலைமைகளின் கீழ் மீட்டெடுக்கக்கூடிய நிலத்தடி வளங்களைக் குறிக்கின்றன, அதே நேரத்தில் உற்பத்தி தினசரி பிரித்தெடுக்கும் வீதத்தை அளவிடுகிறது."
    },
    "maritime_alerts_expander": {
        "en": "📡 View Breaking Maritime Transport & Bilateral Flow Alerts (Live Wire)",
        "hi": "📡 ब्रेकिंग समुद्री परिवहन और द्विपक्षीय प्रवाह अलर्ट देखें (लाइव वायर)",
        "es": "📡 Ver Alertas de Transporte Marítimo y Flujos Bilaterales en Directo (Live Wire)",
        "fr": "📡 Voir les Alertes de Transport Maritime et Flux Bilatéraux en Direct (Fil d'Info)",
        "ar": "📡 عرض تنبيهات النقل البحري وتدفقات التجارة الثنائية العاجلة (شريط مباشر)",
        "de": "📡 Eilmeldungen zu Seetransport und bilateralen Handelsströmen ansehen (Live-Ticker)",
        "zh": "📡 查看最新全球海运要道与双边贸易突发预警（实时电报）",
        "ru": "📡 Срочные оповещения морского транспорта и двусторонних потоков (Прямой эфир)",
        "ja": "📡 海上輸送・二国間石油流動の速報アラートを表示（ライブ通信）",
        "pt": "📡 Ver Alertas de Transporte Marítimo e Fluxos Bilaterais ao Vivo (Live Wire)",
        "it": "📡 Visualizza Avvisi sul Trasporto Marittimo e Flussi Bilaterali in Tempo Reale",
        "ko": "📡 실시간 해상 운송 및 양자 간 무역 흐름 속보 보기 (라이브 와이어)",
        "tr": "📡 Son Dakika Deniz Taşımacılığı ve İkili Akış Uyarılarını Görüntüle (Canlı Akış)",
        "nl": "📡 Bekijk Brekende Maritieme Transport- & Bilaterale Stroomwaarschuwingen (Live Wire)",
        "id": "📡 Lihat Peringatan Terkini Transportasi Maritim & Arus Bilateral (Live Wire)",
        "ur": "📡 بریکنگ میری ٹائم ٹرانسپورٹ اور دوطرفہ فلو الرٹس دیکھیں (لائیو وائر)",
        "bn": "📡 ব্রেকিং মেরিটাইম ট্রান্সপোর্ট এবং দ্বিপাক্ষিক প্রবাহ সতর্কতা দেখুন (লাইভ ওয়্যার)",
        "ta": "📡 முக்கிய கடல்சார் போக்குவரத்து மற்றும் இருதரப்பு ஓட்ட எச்சரிக்கைகளைக் காண்க (நேரலை)"
    },
    "market_signals_leaderboard": {
        "en": "⚡ Market Signals & Leaderboard",
        "hi": "⚡ बाजार संकेत और लीडरबोर्ड",
        "es": "⚡ Señales de Mercado y Clasificación",
        "fr": "⚡ Signaux du Marché & Classement",
        "ar": "⚡ إشارات السوق وقائمة الصدارة",
        "de": "⚡ Marktsignale & Rangliste",
        "zh": "⚡ 核心市场信号与开采排行榜",
        "ru": "⚡ Рыночные сигналы и лидеры",
        "ja": "⚡ 市場シグナル＆リーダーボード"
    },
    "world_extraction_geo": {
        "en": "🗺️ World Petroleum Extraction Geography",
        "hi": "🗺️ विश्व पेट्रोलियम निष्कर्षण भूगोल",
        "es": "🗺️ Geografía Mundial de Extracción de Petróleo",
        "fr": "🗺️ Géographie Mondiale de l'Extraction Pétrolière",
        "ar": "🗺️ جغرافيا استخراج البترول العالمية",
        "de": "🗺️ Globale Erdölförderungs-Geografie",
        "zh": "🗺️ 全球原油开采地缘分布图",
        "ru": "🗺️ География мировой добычи нефти",
        "ja": "🗺️ 世界の石油採掘地理マップ"
    },
    "top_10_producers_title": {
        "en": "Top 10 Crude Oil Producing Nations (2024 vs 2023)",
        "hi": "शीर्ष 10 कच्चा तेल उत्पादक राष्ट्र (2024 बनाम 2023)",
        "es": "Los 10 Principales Países Productores de Petróleo Crudo (2024 vs 2023)",
        "fr": "Top 10 des Pays Producteurs de Pétrole Brut (2024 vs 2023)",
        "ar": "أكبر 10 دول منتجة للنفط الخام (2024 مقابل 2023)",
        "de": "Top 10 Rohölförderländer (2024 vs. 2023)",
        "zh": "全球前十大原油生产国开采量对比 (2024 vs 2023)",
        "ru": "Топ-10 стран-производителей сырой нефти (2024 против 2023)",
        "ja": "主要原油生産国トップ10（2024年 vs 2023年）"
    },
    "regional_prod_shares_title": {
        "en": "Regional Production Shares",
        "hi": "क्षेत्रीय उत्पादन हिस्सेदारी",
        "es": "Participaciones de Producción Regional",
        "fr": "Parts de Production Régionale",
        "ar": "الحصص الإقليمية في الإنتاج",
        "de": "Regionale Produktionsanteile",
        "zh": "全球各主要大区原油产能份额",
        "ru": "Доли регионов в мировой добыче",
        "ja": "地域別石油生産シェア"
    },
    "top_5_exporters_title": {
        "en": "Top 5 Petroleum Exporters (Tracked Seaborne Flow)",
        "hi": "शीर्ष 5 पेट्रोलियम निर्यातक (ट्रैक किया गया समुद्री प्रवाह)",
        "es": "Los 5 Principales Exportadores de Petróleo (Flujo Marítimo)",
        "fr": "Top 5 des Exportateurs de Pétrole (Flux Maritimes Suivis)",
        "ar": "أكبر 5 دول مصدّرة للبترول (التدفقات البحرية المرصودة)",
        "de": "Top 5 Erdölexporteure (Erfasste Seetransporte)",
        "zh": "全球前五大原油出口国（在轨海运实物量）",
        "ru": "Топ-5 экспортеров нефти (Морские поставки)",
        "ja": "主要石油輸出国トップ5（追跡海上フロー）"
    },
    "top_5_importers_title": {
        "en": "Top 5 Petroleum Importers (Daily Intake)",
        "hi": "शीर्ष 5 पेट्रोलियम आयातक (दैनिक खपत)",
        "es": "Los 5 Principales Importadores de Petróleo (Consumo Diario)",
        "fr": "Top 5 des Importateurs de Pétrole (Entrées Quotidiennes)",
        "ar": "أكبر 5 دول مستوردة للبترول (الاستهلاك اليومي)",
        "de": "Top 5 Erdölimporteure (Täglicher Bezug)",
        "zh": "全球前五大原油进口国（每日物理入港量）",
        "ru": "Топ-5 импортеров нефти (Суточное потребление)",
        "ja": "主要石油輸入国トップ5（日量消費輸入）"
    },
    "bilateral_trade_flows_title": {
        "en": "Verified Bilateral Trade Flows (HS 2709 Crude & HS 2710 Products)",
        "hi": "सत्यापित द्विपक्षीय व्यापार प्रवाह (HS 2709 कच्चा तेल व HS 2710 उत्पाद)",
        "es": "Flujos Comerciales Bilaterales Verificados (HS 2709 Crudo y HS 2710)",
        "fr": "Flux Commerciaux Bilatéraux Vérifiés (HS 2709 Brut & HS 2710)",
        "ar": "تدفقات التجارة الثنائية المؤكدة (HS 2709 خام و HS 2710 منتجات)",
        "de": "Verifizierte bilaterale Handelsströme (HS 2709 Rohöl & HS 2710)",
        "zh": "经核验的原油双边海运物理贸易流（HS 2709 原油与 HS 2710 成品油）",
        "ru": "Верифицированные двусторонние торговые потоки (HS 2709 и HS 2710)",
        "ja": "検証済み二国間石油貿易フロー（HS 2709 原油 / HS 2710 製品）"
    },
    "tracked_daily_flow": {
        "en": "Tracked Daily Flow",
        "hi": "ट्रैक किया गया दैनिक प्रवाह",
        "es": "Flujo Diario Rastreado",
        "fr": "Flux Quotidien Suivi",
        "ar": "التدفق اليومي المرصود",
        "de": "Erfasster Tagesfluss",
        "zh": "在轨追踪日均实物流",
        "ru": "Отслеживаемый суточный поток",
        "ja": "追跡日量フロー"
    },
    "opec_coordinated_share": {
        "en": "OPEC+ Coordinated Share",
        "hi": "ओपेक+ समन्वित हिस्सेदारी",
        "es": "Cuota Coordinada OPEP+",
        "fr": "Part Coordonnée OPEP+",
        "ar": "حصة أوبك+ المنسقة",
        "de": "OPEC+ koordinierter Anteil",
        "zh": "OPEC+ 统筹配额份额",
        "ru": "Координируемая доля ОПЕК+",
        "ja": "OPEC+ 協調シェア"
    },
    "non_opec_output": {
        "en": "Non-OPEC Output",
        "hi": "गैर-ओपेक उत्पादन",
        "es": "Producción No-OPEP",
        "fr": "Production Hors-OPEP",
        "ar": "إنتاج الدول غير الأعضاء في أوبك",
        "de": "Nicht-OPEC-Förderung",
        "zh": "非欧佩克自营开采量",
        "ru": "Добыча вне ОПЕК",
        "ja": "非OPEC加盟国産出量"
    },
    "top_geological_reserve": {
        "en": "Top Geological Reserve",
        "hi": "शीर्ष भूवैज्ञानिक भंडार",
        "es": "Mayor Reserva Geológica",
        "fr": "Première Réserve Géologique",
        "ar": "أكبر احتياطي جيولوجي مؤكد",
        "de": "Größte geologische Reserve",
        "zh": "全球最大地质储集资产",
        "ru": "Крупнейшие запасы недр",
        "ja": "最大地質学的埋蔵量"
    },

    # --------------------------------------------------------------------------
    # COMMON ACTION LABELS
    # --------------------------------------------------------------------------
    "explore_drilldown": {
        "en": "EXPLORE DRILL-DOWN",
        "hi": "विस्तृत विश्लेषण देखें",
        "es": "EXPLORAR DETALLE",
        "fr": "EXPLORER EN DÉTAIL",
        "ar": "استكشاف التحليل المفصل",
        "de": "DETAILANALYSE ÖFFNEN",
        "zh": "展开深度钻取分析",
        "ru": "ПОДРОБНЫЙ АНАЛИЗ",
        "ja": "詳細ドリルダウンを開く"
    },
    "download_csv": {
        "en": "Download CSV Dataset",
        "hi": "सीएसवी डेटा डाउनलोड करें",
        "es": "Descargar Datos CSV",
        "fr": "Télécharger Données CSV",
        "ar": "تحميل ملف CSV",
        "de": "CSV-Datensatz herunterladen",
        "zh": "下载完整 CSV 数据集",
        "ru": "Скачать CSV данные",
        "ja": "CSVデータをダウンロード"
    },

    # --------------------------------------------------------------------------
    # HOME VIEW TRANSLATIONS
    # --------------------------------------------------------------------------
    "home_eyebrow": {
        "en": "ENERGY INTELLIGENCE PLATFORM • REAL-TIME COMMODITY FLOWS",
        "hi": "ऊर्जा खुफिया मंच • वास्तविक समय कमोडिटी प्रवाह",
        "es": "PLATAFORMA DE INTELIGENCIA ENERGÉTICA • FLUJOS EN TIEMPO REAL",
        "fr": "PLATEFORME D'INTELLIGENCE ÉNERGÉTIQUE • FLUX EN TEMPS RÉEL",
        "ar": "منصة معلومات الطاقة • تدفقات السلع في الوقت الفعلي",
        "de": "ENERGIE-INTELLIGENZ-PLATTFORM • ECHTZEIT-WARENFLÜSSE",
        "zh": "能源情报分析平台 • 实时大宗商品流向",
        "ru": "ПЛАТФОРМА ЭНЕРГЕТИЧЕСКОЙ РАЗВЕДКИ • ПОТОКИ В РЕАЛЬНОМ ВРЕМЕНИ",
        "ja": "エネルギー市場情報プラットフォーム • リアルタイム・フロー",
        "pt": "PLATAFORMA DE INTELIGÊNCIA ENERGÉTICA • FLUXOS EM TEMPO REAL",
        "it": "PIATTAFORMA DI INTELLIGENZA ENERGETICA • FLUSSI IN TEMPO REALE",
        "ko": "에너지 인텔리전스 플랫폼 • 실시간 원자재 흐름",
        "tr": "ENERJİ İSTİHBARAT PLATFORMU • GERÇEK ZAMANLI EMTİA AKIŞLARI",
        "nl": "ENERGIE-INTELLIGENTIEPLATFORM • REALTIME COMMODITY-STROMEN",
        "id": "PLATFORM INTELIJEN ENERGI • ARUS KOMODITAS REAL-TIME",
        "ur": "انرجی انٹیلیجنس پلیٹ فارم • رئیل ٹائم کموڈٹی فلو",
        "bn": "এনার্জি ইন্টেলিজেন্স প্ল্যাটফর্ম • রিয়েল-টাইম কমোডিটি প্রবাহ",
        "ta": "ஆற்றல் நுண்ணறிவு தளம் • நேரலை பொருட்கள் ஓட்டம்"
    },
    "home_hero_title": {
        "en": "Understand the world's real-time energy flows.",
        "hi": "दुनिया के वास्तविक समय के ऊर्जा प्रवाह को समझें।",
        "es": "Comprenda los flujos de energía del mundo en tiempo real.",
        "fr": "Comprenez les flux énergétiques mondiaux en temps réel.",
        "ar": "افهم تدفقات الطاقة العالمية في الوقت الفعلي.",
        "de": "Verstehen Sie die globalen Energieflüsse in Echtzeit.",
        "zh": "洞悉全球能源的实时流向与市场格局。",
        "ru": "Поймите мировые энергетические потоки в реальном времени.",
        "ja": "世界のリアルタイムなエネルギー動向を正確に把握。"
    },
    "home_hero_subtitle": {
        "en": "Unify international crude benchmarks, maritime seaborne tanker routes, and downstream retail pump pricing into an integrated, deterministic intelligence platform.",
        "hi": "अंतरराष्ट्रीय कच्चे तेल के बेंचमार्क, समुद्री टैंकर मार्गों और खुदरा पंप मूल्य निर्धारण को एक एकीकृत विश्लेषण मंच में जोड़ें।",
        "es": "Unifique referencias internacionales de crudo, rutas marítimas y precios en surtidor en una plataforma de inteligencia integrada.",
        "fr": "Unifiez les références internationales de brut, les routes maritimes et les prix à la pompe dans une plateforme intégrée.",
        "ar": "توحيد معايير النفط الخام العالمية وطرق الناقلات البحرية وأسعار المضخات في منصة معلوماتية متكاملة.",
        "de": "Integrieren Sie Rohöl-Benchmarks, Tankschifffahrtsrouten und Endverbraucherpreise in eine einheitliche Plattform.",
        "zh": "将国际原油基准价格、海上油轮航运干线及终端加油站零售价格整合为一体化决策情报平台。",
        "ru": "Объедините мировые котировки нефти, морские танкерные маршруты и розничные цены на АЗС в единую систему.",
        "ja": "国際原油ベンチマーク、海上タンカールート、末端ガソリンスタンド価格を統合した情報プラットフォーム。"
    },
    "home_cta_dashboard": {
        "en": "⚡ Launch Live Intelligence Dashboard",
        "hi": "⚡ लाइव इंटेलिजेंस डैशबोर्ड शुरू करें",
        "es": "⚡ Lanzar Panel de Inteligencia en Vivo",
        "fr": "⚡ Lancer le Tableau de Bord en Direct",
        "ar": "⚡ فتح لوحة معلومات الطاقة المباشرة",
        "de": "⚡ Live-Lagezentrum öffnen",
        "zh": "⚡ 启动实时市场情报仪表板",
        "ru": "⚡ Открыть интерактивную панель",
        "ja": "⚡ ライブ・ダッシュボードを起動"
    },
    "home_cta_india": {
        "en": "🇮🇳 Explore India Fuel Center →",
        "hi": "🇮🇳 भारत ईंधन केंद्र देखें →",
        "es": "🇮🇳 Explorar Centro de India →",
        "fr": "🇮🇳 Explorer le Centre Inde →",
        "ar": "🇮🇳 استكشاف مركز الوقود الهندي →",
        "de": "🇮🇳 Indien-Zentrum erkunden →",
        "zh": "🇮🇳 探索印度能源与燃料中心 →",
        "ru": "🇮🇳 Центр топлива Индии →",
        "ja": "🇮🇳 インド燃料センターを開く →"
    },
    "home_mockup_telemetry": {
        "en": "● 25 NATIONS LIVE TELEMETRY",
        "hi": "● 25 देशों की लाइव टेलीमेट्री",
        "es": "● TELEMETRÍA EN VIVO DE 25 NACIONES",
        "fr": "● TÉLÉMÉTRIE EN DIRECT DE 25 PAYS",
        "ar": "● بيانات مباشرة لـ 25 دولة",
        "de": "● LIVE-TELEMETRIE AUS 25 LÄNDERN",
        "zh": "● 25 国实时能源遥测数据",
        "ru": "● ТЕЛЕМЕТРИЯ 25 СТРАН В РЕАЛЬНОМ ВРЕМЕНИ",
        "ja": "● 主要25カ国リアルタイム通信"
    },
    "home_brent_spot": {
        "en": "BRENT CRUDE SPOT",
        "hi": "ब्रेंट क्रूड हाजिर भाव",
        "es": "BRENT CRUDO SPOT",
        "fr": "PÉTROLE BRENT SPOT",
        "ar": "خام برنت الفوري",
        "de": "BRENT-ROHÖL SPOT",
        "zh": "布伦特原油现货基准",
        "ru": "НЕФТЬ BRENT (СПОТ)",
        "ja": "ブレント原油スポット価格"
    },
    "home_brent_sub": {
        "en": "▲ Daily Reference Benchmark",
        "hi": "▲ दैनिक संदर्भ बेंचमार्क",
        "es": "▲ Referencia Diaria del Mercado",
        "fr": "▲ Indice de Référence Quotidien",
        "ar": "▲ المؤشر المرجعي اليومي",
        "de": "▲ Täglicher Referenzwert",
        "zh": "▲ 每日现货指导基准",
        "ru": "▲ Дневной эталонный ориентир",
        "ja": "▲ 每日参照ベンチマーク"
    },
    "home_delhi_diesel": {
        "en": "DELHI DIESEL PUMP",
        "hi": "दिल्ली डीजल खुदरा मूल्य",
        "es": "DIÉSEL EN DELHI (SURTIDOR)",
        "fr": "DIESEL À DELHI (POMPE)",
        "ar": "ديزل دلهي عند المضخة",
        "de": "DIESEL DELHI TANKSTELLE",
        "zh": "印度德里柴油零售价",
        "ru": "ДИЗЕЛЬ В ДЕЛИ (АЗС)",
        "ja": "デリー・ディーゼル小売価格"
    },
    "home_delhi_sub": {
        "en": "Official PPAC Metro Benchmark",
        "hi": "आधिकारिक पीपीएसी मेट्रो बेंचमार्क",
        "es": "Punto de Referencia Oficial PPAC",
        "fr": "Référence Officielle PPAC Métro",
        "ar": "المعيار الرسمي المعتمد من PPAC",
        "de": "Offizieller PPAC-Metropolwert",
        "zh": "印度石油部官方 PPAC 基准",
        "ru": "Официальный ориентир PPAC",
        "ja": "PPAC公式メトロ価格"
    },
    "home_hormuz_title": {
        "en": "STRAIT OF HORMUZ",
        "hi": "होर्मुज जलडमरूमध्य",
        "es": "ESTRECHO DE ORMUZ",
        "fr": "DÉTROIT D'ORMUZ",
        "ar": "مضيق هرمز الاستراتيجي",
        "de": "STRASSE VON HORMUS",
        "zh": "霍尔木兹海峡战略咽喉",
        "ru": "ОРМУЗСКИЙ ПРОЛИВ",
        "ja": "ホルムズ海峡海上輸送路"
    },
    "home_hormuz_sub": {
        "en": "Critical Seaborne Chokepoint",
        "hi": "अतिसंवेदनशील समुद्री चोकपॉइंट",
        "es": "Punto de Estrangulamiento Crítico",
        "fr": "Point de Passage Maritime Critique",
        "ar": "أهم ممر مائي استراتيجي للطاقة",
        "de": "Kritischer maritimer Nadelöhr",
        "zh": "全球核心原油海上命脉",
        "ru": "Критический морской пролив",
        "ja": "最重要チョークポイント"
    },
    "home_latency_title": {
        "en": "IN-MEMORY LATENCY",
        "hi": "मेमोरी प्रतिक्रिया समय",
        "es": "LATENCIA EN MEMORIA",
        "fr": "LATENCE EN MÉMOIRE",
        "ar": "سرعة الاستجابة في الذاكرة",
        "de": "IN-MEMORY LATENZ",
        "zh": "内存缓存响应延迟",
        "ru": "СКОРОСТЬ В ПАМЯТИ",
        "ja": "インメモリ応答速度"
    },
    "home_latency_sub": {
        "en": "Multi-Tier Cache Engine",
        "hi": "मल्टी-टीयर कैश इंजन",
        "es": "Motor de Caché Multinivel",
        "fr": "Moteur de Cache Multi-Niveaux",
        "ar": "محرك تخزين مؤقت متعدد الطبقات",
        "de": "Multi-Tier Cache-Architektur",
        "zh": "多级高性能缓存架构",
        "ru": "Многоуровневое кэширование",
        "ja": "多層キャッシュエンジン"
    },
    "home_chart_title": {
        "en": "TOP GLOBAL CRUDE PRODUCERS PREVIEW (mbpd)",
        "hi": "शीर्ष वैश्विक कच्चा तेल उत्पादक (मिलियन बैरल/दिन)",
        "es": "PRINCIPALES PRODUCTORES GLOBALES DE CRUDO (mbpd)",
        "fr": "PRINCIPAUX PRODUCTEURS MONDIAUX DE BRUT (mbpd)",
        "ar": "أكبر منتجي النفط الخام في العالم (مليون برميل/يوم)",
        "de": "GRÖSSTE ROHÖLFÖRDERER WELTWEIT (mbpd)",
        "zh": "全球主要原油生产国排行榜 (百万桶/日)",
        "ru": "КРУПНЕЙШИЕ ПРОИЗВОДИТЕЛИ НЕФТИ В МИРЕ (млн барр/день)",
        "ja": "世界主要産油国ランキング (百万バレル/日)"
    },
    "home_chart_sub": {
        "en": "EIA & OPEC VERIFIED 2024–25",
        "hi": "ईआईए एवं ओपेक सत्यापित 2024–25",
        "es": "VERIFICADO POR EIA Y OPEP 2024–25",
        "fr": "VÉRIFIÉ PAR L'EIA ET L'OPEP 2024–25",
        "ar": "معتمد من إدارة معلومات الطاقة وأوبك 2024-25",
        "de": "EIA & OPEC VERIFIZIERT 2024–25",
        "zh": "EIA 与 OPEC 官方核验数据 2024–25",
        "ru": "ПРОВЕРЕНО EIA И ОПЕК 2024–25",
        "ja": "EIAおよびOPEC検証済み 2024–25"
    },
    "home_challenge_eyebrow": {
        "en": "THE CORE CHALLENGE",
        "hi": "मुख्य चुनौती",
        "es": "EL DESAFÍO CENTRAL",
        "fr": "LE DÉFI PRINCIPAL",
        "ar": "التحدي الجوهري",
        "de": "DIE KERNHERAUSFORDERUNG",
        "zh": "行业核心痛点",
        "ru": "ГЛАВНЫЙ ВЫЗОВ",
        "ja": "核心的課題"
    },
    "home_challenge_title": {
        "en": "The Decoupling of Crude Oil and Retail Fuel Prices",
        "hi": "कच्चे तेल और खुदरा ईंधन की कीमतों का अलगाव",
        "es": "El Desacoplamiento entre el Petróleo Crudo y los Precios Minoristas",
        "fr": "Le Découplage entre Pétrole Brut et Prix des Carburants",
        "ar": "انفصال أسعار النفط الخام عن أسعار التجزئة عند المضخات",
        "de": "Die Entkopplung von Rohöl- und Endverbraucherpreisen",
        "zh": "原油国际现货与加油站零售价格的脱节机制",
        "ru": "Разрыв между ценами на нефть и ценами на АЗС",
        "ja": "原油スポット価格とガソリンスタンド小売価格の乖離"
    },
    "home_challenge_p1": {
        "en": "Crude oil is traded internationally as a fungible commodity in US Dollars per barrel. Yet what consumers, freight fleets, and industrial enterprises pay at the pump varies wildly across nations—from under $0.35/L in subsidized oil-producing states to over $2.15/L in heavily taxed European markets.",
        "hi": "कच्चे तेल का अंतरराष्ट्रीय स्तर पर अमेरिकी डॉलर प्रति बैरल में एक विनिमेय वस्तु के रूप में व्यापार होता है। फिर भी उपभोक्ता, मालवाहक बेड़े और औद्योगिक उद्यम जो पंप पर भुगतान करते हैं, वह देशों में भिन्न होता है—सब्सिडी वाले उत्पादक देशों में $0.35/लीटर से कम से लेकर अत्यधिक कर वाले यूरोपीय बाजारों में $2.15/लीटर से अधिक तक।",
        "es": "El petróleo crudo se comercializa internacionalmente en dólares por barril. Sin embargo, lo que pagan los consumidores y flotas en surtidor varía ampliamente entre naciones: desde menos de $0.35/L en países subsidiados hasta más de $2.15/L en mercados europeos gravados.",
        "fr": "Le pétrole brut s'échange en dollars américains par baril. Pourtant, ce que paient les consommateurs et flottes varie considérablement selon les pays : de moins de 0,35 $/L dans les pays subventionnés à plus de 2,15 $/L en Europe lourdement taxée.",
        "ar": "يتم تداول النفط الخام بالدولار الأمريكي للبرميل، لكن ما يدفعه المستهلكون وأساطيل النقل يختلف اختلافاً شاسعاً بين الدول: من أقل من 0.35 دولار/لتر في الدول المنتجة المدعومة إلى أكثر من 2.15 دولار/لتر في الأسواق الأوروبية الخاضعة للضرائب الباهظة.",
        "de": "Rohöl wird weltweit in US-Dollar pro Barrel gehandelt. Doch was Verbraucher und Flotten an der Zapfsäule zahlen, variiert stark: von unter 0,35 $/L in subventionierten Förderländern bis über 2,15 $/L in hochbesteuerten europäischen Märkten.",
        "zh": "原油作为全球大宗商品以美元/桶定价进行交易。然而最终用户与物流运输车队在加油站实际支付的燃油价格却天差地别——从产油补贴国的低于 0.35 美元/升，到重税欧洲市场的逾 2.15 美元/升。",
        "ru": "Нефть торгуется на международном рынке в долларах за баррель. Однако цены на АЗС для потребителей и автопарков различаются колоссально: от менее $0.35/л в субсидируемых странах до более $2.15/л на европейских рынках с высокими налогами.",
        "ja": "原油は米ドル/バレルで国際取引される代替可能な商品です。しかし一般消費者や物流フリートが給油所で支払う小売価格は国によって劇的に異なり、産油国補助金の0.35ドル/L未満から、高税率な欧州の2.15ドル/L超まで幅広く分岐します。"
    },
    "home_challenge_p2": {
        "en": "This spread is driven not by oil quality, but by refinery crack spreads, currency depreciation against the USD, national fuel subsidies, and sovereign excise taxes and regional VAT. Global FuelPulse AI makes these mechanisms transparent, auditable, and quantifiable.",
        "hi": "यह अंतर तेल की गुणवत्ता से नहीं, बल्कि रिफाइनरी क्रैक स्प्रेड, डॉलर के मुकाबले मुद्रा मूल्यह्रास, राष्ट्रीय ईंधन सब्सिडी, और उत्पाद शुल्क व क्षेत्रीय वैट द्वारा संचालित होता है। ग्लोबल फ्यूलपल्स एआई इन तंत्रों को पारदर्शी, ऑडिट-योग्य और मापने योग्य बनाता है।",
        "es": "Esta brecha no se debe a la calidad del crudo, sino a los márgenes de refinación, la depreciación cambiaria, los subsidios nacionales, los impuestos especiales soberanos y el IVA regional. Global FuelPulse AI hace que estos mecanismos sean transparentes y auditables.",
        "fr": "Cet écart ne provient pas de la qualité du pétrole, mais des marges de raffinage, de la dépréciation des devises, des subventions nationales et des taxes souveraines et TVA. Global FuelPulse AI rend ces mécanismes transparents, vérifiables et quantifiables.",
        "ar": "لا يعود هذا التباين إلى جودة النفط، بل إلى هوامش التكرير، وانخفاض قيمة العملات أمام الدولار، والدعم الحكومي للوقود، والضرائب الانتقائية وضريبة القيمة المضافة. منصة Global FuelPulse AI تجعل هذه الآليات شفافة وقابلة للتدقيق والقياس الكمي.",
        "de": "Diese Differenz entsteht nicht durch Ölqualität, sondern durch Raffineriemargen (Crack Spreads), Währungsabwertungen, Subventionen sowie nationale Verbrauchssteuern und Mehrwertsteuer. Global FuelPulse AI macht diese Zusammenhänge transparent und messbar.",
        "zh": "这一巨大的价格差异并非源自原油本身的品质，而是由炼厂裂解价差、对美元汇率波动、国家燃油补贴政策以及中央消费税与地方增值税共同决定。Global FuelPulse AI 让这些复杂的传导机制完全透明可查。",
        "ru": "Этот разрыв обусловлен не качеством нефти, а маржой нефтепереработки (крэк-спредами), колебаниями валютных курсов к доллару, субсидиями и государственными акцизами и НДС. Global FuelPulse AI делает эту цепочку прозрачной и поддающейся расчету.",
        "ja": "この価格差は原油の品質ではなく、精製クラックスプレッド、対ドル為替変動、国家燃料補助金、そして国税（物品税）や地方付加価値税（VAT）によって生じます。Global FuelPulse AI はこれらの構造を透明化し、定量分析を可能にします。"
    },
    "home_value_eyebrow": {
        "en": "USER VALUE",
        "hi": "उपयोगकर्ता मूल्य",
        "es": "VALOR PARA EL USUARIO",
        "fr": "VALEUR UTILISATEUR",
        "ar": "القيمة للمستخدم",
        "de": "NUTZWERT",
        "zh": "商业与决策价值",
        "ru": "ЦЕННОСТЬ ДЛЯ ПОЛЬЗОВАТЕЛЯ",
        "ja": "ユーザー価値"
    },
    "home_value_title": {
        "en": "Who Relies on Global FuelPulse AI?",
        "hi": "ग्लोबल फ्यूलपल्स एआई पर कौन भरोसा करता है?",
        "es": "¿Quién Confía en Global FuelPulse AI?",
        "fr": "Qui s'Appuie sur Global FuelPulse AI ?",
        "ar": "من يعتمد على Global FuelPulse AI؟",
        "de": "Wer vertraut auf Global FuelPulse AI?",
        "zh": "哪些专业团队依赖 Global FuelPulse AI？",
        "ru": "Кто полагается на Global FuelPulse AI?",
        "ja": "Global FuelPulse AI を活用するプロフェッショナル"
    },
    "home_val_fleet_title": {
        "en": "Fleet & Logistics Operators",
        "hi": "फ्लीट एवं लॉजिस्टिक्स ऑपरेटर",
        "es": "Operadores de Flotas y Logística",
        "fr": "Opérateurs de Flottes et Logistique",
        "ar": "مشغلو أساطيل النقل والخدمات اللوجستية",
        "de": "Flotten- & Logistikbetreiber",
        "zh": "物流运输与重卡车队运营商",
        "ru": "Операторы автопарков и логистики",
        "ja": "物流・フリート運行管理企業"
    },
    "home_val_fleet_desc": {
        "en": "Accurately forecast diesel fuel expenditures, model fuel surcharge rate adjustments, and benchmark multi-state fuel bunkering.",
        "hi": "डीजल ईंधन व्यय का सटीक पूर्वानुमान लगाएं, अधिभार दरों को मॉडल करें और अंतर-राज्यीय ईंधन खरीद का बेंचमार्क बनाएं।",
        "es": "Pronostique con precisión gastos en diésel, modele recargos por combustible y compare costos de abastecimiento en múltiples estados.",
        "fr": "Prévoir avec précision les dépenses de diesel, modéliser les surtaxes carburant et comparer l'avitaillement multi-régional.",
        "ar": "التنبؤ الدقيق بنفقات وقود الديزل، ونمذجة تعديلات رسوم الوقود الإضافية، ومقارنة تكاليف التزود بالوقود عبر المناطق المختلفة.",
        "de": "Dieselkosten präzise prognostizieren, Treibstoffzuschläge modellieren und tankstrategische Kosten über Regionen hinweg vergleichen.",
        "zh": "精准预测柴油开支走势，构建燃油附加费动态调节模型，并对比跨省跨国加油补给成本。",
        "ru": "Точно прогнозируйте расходы на дизель, моделируйте топливные надбавки и оптимизируйте заправку по регионам.",
        "ja": "ディーゼル燃料費の正確な予測、燃料サーチャージ調整モデルの構築、複数州にまたがる給油コストの最適化。"
    },
    "home_val_analyst_title": {
        "en": "Energy & Commodity Analysts",
        "hi": "ऊर्जा एवं कमोडिटी विश्लेषक",
        "es": "Analistas de Energía y Materias Primas",
        "fr": "Analystes Énergie et Matières Premières",
        "ar": "محللو الطاقة والسلع الأساسية",
        "de": "Energie- & Rohstoffanalysten",
        "zh": "能源与大宗商品研究分析师",
        "ru": "Аналитики энергетических и сырьевых рынков",
        "ja": "エネルギー・コモディティアナリスト"
    },
    "home_val_analyst_desc": {
        "en": "Monitor seaborne petroleum trade lanes, tanker transit chokepoints (Hormuz, Malacca, Suez), and supplier concentration risk (HHI).",
        "hi": "समुद्री पेट्रोलियम व्यापार गलियारों, टैंकर चोकपॉइंट्स (होर्मुज, मलक्का, स्वेज) और आपूर्तिकर्ता एकाग्रता जोखिम (HHI) की निगरानी करें।",
        "es": "Monitoree rutas marítimas de petróleo, puntos de estrangulamiento (Ormuz, Malaca, Suez) y concentración de proveedores (HHI).",
        "fr": "Surveillez les routes maritimes pétrolières, les détroits stratégiques (Ormuz, Malacca, Suez) et le risque de concentration (HHI).",
        "ar": "مراقبة مسارات تجارة النفط البحرية، ومضائق العبور الحيوية (هرمز، ملقا، السويس)، ومخاطر تركز الموردين (HHI).",
        "de": "Seewege des Ölhandels, Engpässe wie Hormus, Malakka und Sues sowie Lieferantenkonzentrationsrisiken (HHI) überwachen.",
        "zh": "监控全球海上原油贸易航线、关键海峡要道（霍尔木兹、马六甲、苏伊士）及供应集中度风险指数 (HHI)。",
        "ru": "Отслеживайте морские торговые пути, ключевые проливы (Ормуз, Малакка, Суэц) и индекс концентрации поставщиков (HHI).",
        "ja": "海上石油輸送航路、要衝海峡（ホルムズ、マラッカ、スエズ）、および供給元集中度リスク（HHI）を監視。"
    },
    "home_val_policy_title": {
        "en": "Economic & Policy Researchers",
        "hi": "आर्थिक एवं नीति शोधकर्ता",
        "es": "Investigadores Económicos y de Políticas",
        "fr": "Chercheurs en Économie et Politiques",
        "ar": "الباحثون الاقتصاديون وواضعو السياسات",
        "de": "Wirtschafts- & Politikforscher",
        "zh": "宏观经济与公共政策学者",
        "ru": "Экономисты и исследователи политики",
        "ja": "経済・エネルギー政策研究機関"
    },
    "home_val_policy_desc": {
        "en": "Dissect price build-up structures, evaluate tax wedge impacts, and calculate genuine fuel affordability burdens across income deciles.",
        "hi": "मूल्य निर्माण संरचनाओं का विश्लेषण करें, कर वेज के प्रभावों का मूल्यांकन करें और आय स्तरों के अनुसार वास्तविक सामर्थ्य की गणना करें।",
        "es": "Analice estructuras de precios, evalúe el impacto de la cuña fiscal y calcule la asequibilidad del combustible por deciles de ingresos.",
        "fr": "Analyser les structures de formation des prix, évaluer l'impact des taxes et mesurer le fardeau d'accessibilité par niveau de revenu.",
        "ar": "تشريح هياكل تكوين الأسعار، وتقييم أثر الأعباء الضريبية، وحساب القدرة الفعلية على تحمل تكاليف الوقود عبر فئات الدخل.",
        "de": "Preisbildungsstrukturen aufschlüsseln, Steuerkeileffekte analysieren und Erschwinglichkeitsbelastungen berechnen.",
        "zh": "解剖终端燃油成本构成瀑布图，评估税收楔子政策影响，并基于各阶层收入计算真实的能源消费负担指数。",
        "ru": "Анализируйте структуру формирования цен, оценивайте налоговые клинья и рассчитывайте реальную доступность топлива.",
        "ja": "価格形成構造の分解、税負担ウェッジの影響評価、所得分位別の実質燃料購入負担指数の算出。"
    },
    "home_val_corp_title": {
        "en": "Corporate Procurement Teams",
        "hi": "कॉर्पोरेट खरीद एवं क्रय दल",
        "es": "Equipos de Adquisiciones Corporativas",
        "fr": "Équipes d'Approvisionnement Corporatif",
        "ar": "فرق المشتريات المؤسسية",
        "de": "Einkaufs- & Beschaffungsteams",
        "zh": "企业能源大宗采购与风险对冲团队",
        "ru": "Корпоративные отделы закупок",
        "ja": "企業調達・リスクヘッジ部門"
    },
    "home_val_corp_desc": {
        "en": "Stress-test procurement budgets against crude oil supply shocks and currency volatility scenarios.",
        "hi": "कच्चे तेल की आपूर्ति झटकों और मुद्रा अस्थिरता के परिदृश्यों के विरुद्ध खरीद बजट का तनाव-परीक्षण करें।",
        "es": "Pruebe el estrés de los presupuestos de compras ante shocks de suministro de crudo y volatilidad cambiaria.",
        "fr": "Testez la résistance des budgets d'achat face aux chocs d'approvisionnement en brut et aux scénarios de volatilité des devises.",
        "ar": "اختبار قدرة ميزانيات المشتريات على تحمل صدمات إمدادات النفط الخام وسيناريوهات تقلب أسعار العملات.",
        "de": "Einkaufsbudgets gegen Rohölpreisschocks und Wechselkursschwankungen per Stresstest absichern.",
        "zh": "模拟突发地缘原油供应断供与汇率剧烈波动，对大宗能源采购预算开展压力测试。",
        "ru": "Проводите стресс-тестирование бюджетов закупок на случай перебоев поставок нефти и валютных колебаний.",
        "ja": "原油供給ショックや為替変動シナリオに対して調達予算のストレステストを実施。"
    },
    "home_suite_title": {
        "en": "EXPLORE THE PLATFORM SUITE",
        "hi": "प्लेटफ़ॉर्म सुइट का अन्वेषण करें",
        "es": "EXPLORE LA SUITE DE LA PLATAFORMA",
        "fr": "EXPLORER LA SUITE DE LA PLATEFORME",
        "ar": "استكشف خدمات المنصة المتكاملة",
        "de": "ENTDECKEN SIE DIE PLATTFORM",
        "zh": "探索平台核心产品套件",
        "ru": "МОДУЛИ И СЕРВИСЫ ПЛАТФОРМЫ",
        "ja": "プラットフォーム主要機能群"
    },
    "home_card_dash_title": {
        "en": "Live Intelligence Dashboard",
        "hi": "लाइव इंटेलिजेंस डैशबोर्ड",
        "es": "Panel de Inteligencia en Vivo",
        "fr": "Tableau de Bord en Direct",
        "ar": "لوحة معلومات الطاقة المباشرة",
        "de": "Live-Lagezentrum",
        "zh": "实时能源市场全景仪表板",
        "ru": "Оперативная панель аналитики",
        "ja": "リアルタイム・インテリジェンス・ダッシュボード"
    },
    "home_card_dash_desc": {
        "en": "11 narrative chapters tracing the petroleum value chain: extraction leaderboards, bilateral trade matrices, retail price explorer, shock simulation, and ML price radar.",
        "hi": "पेट्रोलियम मूल्य श्रृंखला को दर्शाने वाले 11 अध्याय: निष्कर्षण लीडरबोर्ड, द्विपक्षीय व्यापार, खुदरा मूल्य एक्सप्लोरर, शॉक सिमुलेशन और एमएल मूल्य रडार।",
        "es": "11 capítulos que recorren la cadena de valor: extracción, comercio bilateral, precios minoristas, simulación de choque y radar predictivo ML.",
        "fr": "11 chapitres retraçant la chaîne de valeur : extraction, commerce bilatéral, prix au détail, simulation de choc et radar prédictif ML.",
        "ar": "11 فصلاً تحليلياً تغطي سلسلة القيمة النفطية: ترتيب الإنتاج، التجارة الثنائية، أسعار التجزئة، محاكاة الصدمات، ورادار التنبؤ بالذكاء الاصطناعي.",
        "de": "11 Kapitel zur Wertschöpfungskette: Förder-Ranglisten, bilateraler Handel, Endverbraucherpreise, Schocksimulation und ML-Radar.",
        "zh": "11 个循序渐进的深度专题：从开采国排行、双边贸易流动矩阵，到终端加油站零售价格、冲击模拟与机器学习价格雷达。",
        "ru": "11 глав по цепочке создания стоимости: добыча, двусторонняя торговля, розничные цены, симуляция шоков и прогнозный радар ML.",
        "ja": "石油バリューチェーンを網羅する11のチャプター：採掘ランキング、二国間貿易マトリクス、小売価格エクスプローラー、ショックシミュレーション、ML予測レーダー。"
    },
    "home_btn_open_dash": {
        "en": "Open Dashboard →",
        "hi": "डैशबोर्ड खोलें →",
        "es": "Abrir Panel →",
        "fr": "Ouvrir Tableau →",
        "ar": "فتح لوحة المعلومات →",
        "de": "Lagezentrum öffnen →",
        "zh": "进入数据仪表板 →",
        "ru": "Открыть панель →",
        "ja": "ダッシュボードを開く →"
    },
    "home_card_india_title": {
        "en": "India Fuel Center",
        "hi": "भारत ईंधन केंद्र",
        "es": "Centro de Combustibles de India",
        "fr": "Centre Carburants Inde",
        "ar": "مركز الوقود في الهند",
        "de": "Indien Kraftstoffzentrum",
        "zh": "印度国家燃料与税收智库",
        "ru": "Центр топлива Индии",
        "ja": "インド燃料インテリジェンスセンター"
    },
    "home_card_india_desc": {
        "en": "Official PPAC metro daily city benchmarks (Delhi, Mumbai, Kolkata, Chennai), MoPNG retail price build-up waterfall, and OMC market footprint breakdown.",
        "hi": "आधिकारिक पीपीएसी दैनिक मेट्रो बेंचमार्क (दिल्ली, मुंबई, कोलकाता, चेन्नई), MoPNG मूल्य निर्माण वॉटरफॉल, और ओएमसी बाजार पदचिह्न।",
        "es": "Precios oficiales diarios de PPAC (Delhi, Mumbai, Kolkata, Chennai), desglose de precios de MoPNG y cuota de mercado de OMCs.",
        "fr": "Repères officiels quotidiens PPAC (Delhi, Mumbai, Kolkata, Chennai), cascade de formation des prix MoPNG et parts de marché OMC.",
        "ar": "المؤشرات الرسمية اليومية الصادرة عن PPAC في المدن الكبرى (دلهي، مومباي، كولكاتا، تشيناي)، وتفصيل أسعار التجزئة، وحصص شركات التسويق.",
        "de": "Offizielle tägliche PPAC-Preise für Delhi, Mumbai, Kolkata, Chennai, MoPNG-Preiskaskade und Marktanteile der Ölgesellschaften.",
        "zh": "印度石油部 PPAC 四大都会每日基准（德里、孟买、加尔各答、金奈）、官方价格瀑布分解图及国有与私营炼厂网络。",
        "ru": "Официальные ежедневные котировки PPAC (Дели, Мумбаи, Калькутта, Ченнаи), структура цен MoPNG и доли нефтяных компаний.",
        "ja": "PPAC公式デリー・ムンバイ等主要都市日次ベンチマーク、MoPNG価格形成ウォーターフォール、石油元売りシェア構成。"
    },
    "home_btn_open_india": {
        "en": "Open India Center →",
        "hi": "भारत केंद्र खोलें →",
        "es": "Abrir Centro de India →",
        "fr": "Ouvrir Centre Inde →",
        "ar": "فتح مركز الهند →",
        "de": "Indien-Zentrum öffnen →",
        "zh": "进入印度数据中心 →",
        "ru": "Открыть центр Индии →",
        "ja": "インドセンターを開く →"
    },
    "home_card_trust_title": {
        "en": "Data Trust & Provenance",
        "hi": "डेटा प्रमाणिकता एवं स्रोत",
        "es": "Confianza y Procedencia de Datos",
        "fr": "Confiance et Traçabilité des Données",
        "ar": "موثوقية البيانات ومصادرها",
        "de": "Datenintegrität & Provenienz",
        "zh": "数据透明度、可信度与审计源",
        "ru": "Достоверность данных и источники",
        "ja": "データ信頼性とデータ出所"
    },
    "home_card_trust_desc": {
        "en": "Full transparency over the 7 registered data providers, observation dates vs retrieval timestamps, SLA thresholds, and automated quality quarantine logs.",
        "hi": "7 पंजीकृत डेटा प्रदाताओं की पूरी पारदर्शिता, अवलोकन तिथियां बनाम पुनर्प्राप्ति समय, एसएलए सीमाएं और स्वचालित गुणवत्ता संगरोध लॉग।",
        "es": "Transparencia total sobre los 7 proveedores de datos, fechas de observación vs marcas de tiempo, umbrales SLA y cuarentena de calidad.",
        "fr": "Transparence totale sur les 7 fournisseurs de données, dates d'observation vs horodatages, seuils SLA et quarantaine de qualité.",
        "ar": "شفافية كاملة حول مقدمي البيانات السبعة المعتمدين، ومواعيد الرصد، وحدود اتفاقيات مستوى الخدمة، وسجلات مراقبة الجودة الآلية.",
        "de": "Volle Transparenz über die 7 Datenquellen, Erfassungsdaten vs. Abrufzeitpunkte, SLA-Schwellenwerte und automatisierte Quarantäneprotokolle.",
        "zh": "完全公开 7 大官方数据源接口规范、观测采集时间与抓取时间戳对比、SLA 刷新阈值及自动化数据清洗隔离日志。",
        "ru": "Полная прозрачность по 7 поставщикам данных, даты наблюдений против времени запросов, пороги SLA и журналы контроля качества.",
        "ja": "登録された7つのデータ提供元、観測日時と取得タイムスタンプ、SLA基準値、自動品質隔離ログの完全な透明性。"
    },
    "home_btn_open_trust": {
        "en": "Open Trust Center →",
        "hi": "प्रमाणिकता केंद्र खोलें →",
        "es": "Abrir Centro de Confianza →",
        "fr": "Ouvrir Centre de Confiance →",
        "ar": "فتح مركز الموثوقية →",
        "de": "Vertrauenszentrum öffnen →",
        "zh": "进入数据可信中心 →",
        "ru": "Открыть центр надежности →",
        "ja": "信頼性センターを開く →"
    },
    "home_disclosure_title": {
        "en": "ETHICAL DATA DISCLOSURE",
        "hi": "नैतिक डेटा प्रकटीकरण",
        "es": "DIVULGACIÓN ÉTICA DE DATOS",
        "fr": "DIVULGATION ÉTHIQUE DES DONNÉES",
        "ar": "الإفصاح الأخلاقي عن البيانات",
        "de": "ETHISCHE DATENOFFENLEGUNG",
        "zh": "数据伦理与透明度公开声明",
        "ru": "ЭТИЧЕСКОЕ РАСКРЫТИЕ ДАННЫХ",
        "ja": "データ利用に関する倫理的開示"
    },
    "home_disclosure_desc": {
        "en": "Global FuelPulse AI operates on real, verified benchmark data from public institutions (US EIA, India PPAC, European Commission, UN Comtrade, Open Exchange Rates). We deliberately do not fabricate synthetic pricing or hallucinate unmonitored rural stations. Where data is collected weekly or annually, the exact observation dates and provenance are visibly stamped on every metric and chart.",
        "hi": "ग्लोबल फ्यूलपल्स एआई सार्वजनिक संस्थानों (यूएस ईआईए, भारत पीपीएसी, यूरोपीय आयोग, संयुक्त राष्ट्र कॉमट्रेड, ओपन एक्सचेंज रेट्स) से वास्तविक, सत्यापित बेंचमार्क डेटा पर काम करता है। हम जानबूझकर नकली मूल्य निर्धारण नहीं बनाते हैं। जहां डेटा साप्ताहिक या वार्षिक रूप से एकत्र किया जाता है, सटीक अवलोकन तिथियां हर मीट्रिक और चार्ट पर दिखाई देती हैं।",
        "es": "Global FuelPulse AI opera con datos reales y verificados de instituciones públicas (US EIA, India PPAC, Comisión Europea, UN Comtrade, Open Exchange Rates). No fabricamos precios sintéticos ni alucinamos estaciones no monitoreadas. Las fechas de observación exactas se estampan de forma visible en cada métrica.",
        "fr": "Global FuelPulse AI fonctionne sur des données réelles et vérifiées d'institutions publiques (US EIA, Inde PPAC, Commission Européenne, ONU Comtrade, Open Exchange Rates). Nous ne fabriquons pas de prix synthétiques. Les dates exactes d'observation sont clairement indiquées sur chaque graphique.",
        "ar": "تعمل منصة Global FuelPulse AI على بيانات حقيقية وموثقة من مؤسسات عامة رسمية (إدارة معلومات الطاقة الأمريكية، وPPAC الهندية، والمفوضية الأوروبية، والأمم المتحدة). نحن لا نختلق أسعاراً وهمية، وتاريخ الرصد الدقيق مختوم بوضوح على كل مقياس ورسم بياني.",
        "de": "Global FuelPulse AI arbeitet mit realen, verifizierten Referenzdaten öffentlicher Institutionen (US EIA, Indien PPAC, EU-Kommission, UN Comtrade, Open Exchange Rates). Wir generieren keine synthetischen Preise. Die exakten Erfassungsdaten sind auf jedem Diagramm ausgewiesen.",
        "zh": "Global FuelPulse AI 严格基于国际公共权威机构（美国能源信息署 EIA、印度石油计划与分析局 PPAC、欧盟委员会、联合国商品贸易数据库 UN Comtrade、Open Exchange Rates）发布的已核验真实数据运行。本平台绝不伪造合成虚构价格，所有指标与图表均明确标注实际观测日期与源头出处。",
        "ru": "Global FuelPulse AI работает на основе реальных проверенных данных официальных институтов (US EIA, Индия PPAC, Европейская комиссия, ООН Comtrade, Open Exchange Rates). Мы не генерируем синтетические цены. Точные даты наблюдений четко указаны на каждом графике.",
        "ja": "Global FuelPulse AI は、各国の公的機関（米国EIA、インドPPAC、欧州委員会、国連Comtrade、Open Exchange Rates）の検証済み実測データのみに基づいて動作します。架空の合成価格を作成することは一切ありません。すべての指標やグラフには観測日と出所が明記されています。"
    },

    # --------------------------------------------------------------------------
    # INDIA CENTER TRANSLATIONS
    # --------------------------------------------------------------------------
    "india_center_title": {
        "en": "India Energy & Fuel Intelligence Center",
        "hi": "भारत ऊर्जा एवं ईंधन खुफिया केंद्र",
        "es": "Centro de Inteligencia Energética de India",
        "fr": "Centre d'Intelligence Énergétique de l'Inde",
        "ar": "مركز استخبارات الطاقة والوقود في الهند",
        "de": "Indien Energie- & Kraftstoff-Lagezentrum",
        "zh": "印度能源与燃料市场国家情报中心",
        "ru": "Центр энергетической аналитики Индии",
        "ja": "インドエネルギー・燃料インテリジェンスセンター"
    },
    "india_center_subtitle": {
        "en": "Official PPAC daily metro benchmarks, MoPNG price build-up waterfall, and state-owned vs private oil marketing company (OMC) market structures.",
        "hi": "आधिकारिक पीपीएसी दैनिक मेट्रो बेंचमार्क, पेट्रोलियम मंत्रालय (MoPNG) मूल्य निर्माण वॉटरफॉल, और तेल विपणन कंपनियों (OMC) की बाजार संरचनाएं।",
        "es": "Referencias metropolitanas oficiales diarias de PPAC, desglose en cascada de precios de MoPNG y estructura de mercado de las OMCs.",
        "fr": "Repères métropolitains officiels quotidiens PPAC, cascade de prix MoPNG et structures de marché des compagnies pétrolières (OMC).",
        "ar": "المؤشرات المرجعية اليومية الرسمية من PPAC في المدن الكبرى، وتفصيل أسعار وزارة النفط (MoPNG)، وهيكل شركات تسويق النفط (OMC).",
        "de": "Offizielle tägliche PPAC-Referenzwerte für Metropolen, MoPNG-Preiskaskade und Marktstrukturen der staatlichen und privaten Ölkonzerne.",
        "zh": "印度石油计划与分析局 (PPAC) 四大都会每日基准、石油部 (MoPNG) 价格瀑布模型，以及公营与私营炼厂零售网络格局。",
        "ru": "Официальные ежедневные котировки PPAC для мегаполисов, каскад цен MoPNG и структура рынка государственных и частных компаний (OMC).",
        "ja": "PPAC公式メトロ日次ベンチマーク、MoPNG価格形成ウォーターフォール、および石油元売り各社の市場構造。"
    },
    "india_delhi_petrol_kpi": {
        "en": "Delhi Petrol Benchmark",
        "hi": "दिल्ली पेट्रोल बेंचमार्क",
        "es": "Referencia de Gasolina en Delhi",
        "fr": "Référence Essence à Delhi",
        "ar": "معيار البنزين في دلهي",
        "de": "Benzin-Referenzpreis Delhi",
        "zh": "德里汽油官方基准零售价",
        "ru": "Эталон бензина в Дели",
        "ja": "デリー・ガソリン基準価格"
    },
    "india_delhi_diesel_kpi": {
        "en": "Delhi Diesel Benchmark",
        "hi": "दिल्ली डीजल बेंचमार्क",
        "es": "Referencia de Diésel en Delhi",
        "fr": "Référence Diesel à Delhi",
        "ar": "معيار الديزل في دلهي",
        "de": "Diesel-Referenzpreis Delhi",
        "zh": "德里柴油官方基准零售价",
        "ru": "Эталон дизеля в Дели",
        "ja": "デリー・ディーゼル基準価格"
    },
    "india_delhi_petrol_sub": {
        "en": "PPAC Metro Benchmark (₹102.12 / L)",
        "hi": "पीपीएसी मेट्रो बेंचमार्क (₹102.12 / ली)",
        "es": "Referencia Metro PPAC (₹102.12 / L)",
        "fr": "Référence PPAC Métro (102,12 ₹ / L)",
        "ar": "معيار PPAC للمدن (102.12 روبية/لتر)",
        "de": "PPAC-Metropolpreis (102,12 ₹ / L)",
        "zh": "PPAC 都会基准价 (₹102.12 / 升)",
        "ru": "Ориентир PPAC (102,12 ₹ / л)",
        "ja": "PPAC都市基準価格 (₹102.12 / L)"
    },
    "india_delhi_diesel_sub": {
        "en": "Commercial Transport (₹95.20 / L)",
        "hi": "वाणिज्यिक परिवहन बेंचमार्क (₹95.20 / ली)",
        "es": "Transporte Comercial (₹95.20 / L)",
        "fr": "Transport Commercial (95,20 ₹ / L)",
        "ar": "وقود النقل التجاري (95.20 روبية/لتر)",
        "de": "Gewerblicher Transport (95,20 ₹ / L)",
        "zh": "商业与物流货运基准 (₹95.20 / 升)",
        "ru": "Коммерческий транспорт (95,20 ₹ / л)",
        "ja": "商用輸送基準 (₹95.20 / L)"
    },
    "india_crude_basket_kpi": {
        "en": "Indian Crude Basket",
        "hi": "भारतीय कच्चा तेल बास्केट",
        "es": "Cesta de Crudo Indio",
        "fr": "Panier de Brut Indien",
        "ar": "سلة الخام الهندي",
        "de": "Indischer Rohölkorb",
        "zh": "印度原油进口综合篮子",
        "ru": "Индийская корзина нефти",
        "ja": "インド原油バスケット"
    },
    "india_crude_basket_sub": {
        "en": "Oman-Dubai sour (75.6%) + Brent (24.4%)",
        "hi": "ओमान-दुबई सौर (75.6%) + ब्रेंट (24.4%)",
        "es": "Oman-Dubai sour (75.6%) + Brent (24.4%)",
        "fr": "Oman-Dubaï sour (75,6 %) + Brent (24,4 %)",
        "ar": "عمان-دبي عالي الكبريت (75.6%) + برنت (24.4%)",
        "de": "Oman-Dubai sauer (75,6%) + Brent (24,4%)",
        "zh": "阿曼-迪拜含硫原油 (75.6%) + 布伦特 (24.4%)",
        "ru": "Оман-Дубай кислый (75.6%) + Brent (24.4%)",
        "ja": "オマーン・ドバイ高硫黄 (75.6%) + ブレント (24.4%)"
    },
    "india_crude_import_dep": {
        "en": "Crude Import Dependency",
        "hi": "कच्चा तेल आयात निर्भरता",
        "es": "Dependencia de Importación de Crudo",
        "fr": "Dépendance aux Importations de Brut",
        "ar": "التبعية لاستيراد النفط الخام",
        "de": "Rohöl-Importabhängigkeit",
        "zh": "国家原油对外依存度",
        "ru": "Зависимость от импорта нефти",
        "ja": "原油輸入依存度"
    },
    "india_crude_import_sub": {
        "en": "Refinery throughput imported",
        "hi": "रिफाइनरी थ्रूपुट आयातित",
        "es": "Procesamiento de refinería importado",
        "fr": "Raffinage issu de l'importation",
        "ar": "نسبة استيراد مدخلات المصافي",
        "de": "Importierter Raffineriedurchsatz",
        "zh": "炼厂加工原油中进口占比",
        "ru": "Доля импорта в переработке",
        "ja": "精製処理量の輸入比率"
    },
    "india_sec1_title": {
        "en": "1. OFFICIAL METRO PUMP BENCHMARKS (PPAC SERIES)",
        "hi": "1. आधिकारिक मेट्रो पंप बेंचमार्क (पीपीएसी श्रृंखला)",
        "es": "1. PRECIOS OFICIALES METROPOLITANOS (SERIE PPAC)",
        "fr": "1. REPÈRES MÉTROPOLITAINS OFFICIELS (SÉRIE PPAC)",
        "ar": "1. المؤشرات الرسمية للمدن الكبرى (سلسلة PPAC)",
        "de": "1. OFFIZIELLE METROPOLEN-REFERENZPREISE (PPAC)",
        "zh": "1. 印度四大都会官方加油站零售基准 (PPAC 数据列)",
        "ru": "1. ОФИЦИАЛЬНЫЕ ЦЕНЫ В МЕГАПОЛИСАХ (СЕРИЯ PPAC)",
        "ja": "1. 公式メトロ小売価格ベンチマーク (PPACシリーズ)"
    },
    "india_sec2_title": {
        "en": "2. MoPNG RETAIL PRICE WATERFALL BREAKDOWN (DELHI BENCHMARK)",
        "hi": "2. MoPNG खुदरा मूल्य निर्माण वॉटरफॉल (दिल्ली बेंचमार्क)",
        "es": "2. DESGLOSE EN CASCADA DE PRECIOS MoPNG (DELHI)",
        "fr": "2. CASCADE DE FORMATION DES PRIX MoPNG (REPÈRE DELHI)",
        "ar": "2. تفصيل شلال أسعار التجزئة MoPNG (معيار دلهي)",
        "de": "2. MoPNG-PREISKASKADE (REFERENZ DELHI)",
        "zh": "2. 印度石油部 (MoPNG) 燃油零售价格瀑布结构分解 (德里基准)",
        "ru": "2. СТРУКТУРА ЦЕНЫ MoPNG (ЭТАЛОН ДЕЛИ)",
        "ja": "2. MoPNG 小売価格ウォーターフォール詳細 (デリー基準)"
    },
    "india_sec3_title": {
        "en": "3. PUBLIC VS PRIVATE OIL MARKETING COMPANY (OMC) RETAIL FOOTPRINT",
        "hi": "3. सार्वजनिक बनाम निजी तेल विपणन कंपनी (OMC) नेटवर्क",
        "es": "3. RED MINORISTA DE OMCs PÚBLICAS VS PRIVADAS",
        "fr": "3. RÉSEAU DES COMPAGNIES PÉTROLIÈRES PUBLIQUES ET PRIVÉES",
        "ar": "3. شبكة محطات شركات تسويق النفط العامة والخاصة (OMC)",
        "de": "3. TANKSTELLENNETZ DER STAATLICHEN & PRIVATEN ÖL-KONZERNE",
        "zh": "3. 印度国有骨干与民营跨国石油营销公司 (OMC) 零售网络占比",
        "ru": "3. СЕТЬ ГОСУДАРСТВЕННЫХ И ЧАСТНЫХ КОМПАНИЙ (OMC)",
        "ja": "3. 国営 vs 民間 石油販売会社 (OMC) リテール網比較"
    },
    "india_sec4_title": {
        "en": "4. STATE-BY-STATE VAT & TAX DIVERGENCE",
        "hi": "4. राज्य-वार वैट एवं कर अंतर",
        "es": "4. DIVERGENCIA DE IVA E IMPUESTOS POR ESTADO",
        "fr": "4. DIVERGENCE DES TAXES ET TVA PAR ÉTAT",
        "ar": "4. تباين ضريبة القيمة المضافة والرسوم بين الولايات",
        "de": "4. STEUER- & MEHRWERTSTEUER-UNTERSCHIEDE NACH BUNDESSTAATEN",
        "zh": "4. 印度各邦增值税 (VAT) 与地方附加税税率差异分析",
        "ru": "4. РАЗЛИЧИЯ В НДС И НАЛОГАХ ПО ШТАТАМ ИНДИИ",
        "ja": "4. 州別付加価値税 (VAT) および地方税率の格差"
    },
    "india_sec5_title": {
        "en": "5. METHODOLOGY & PPAC REGULATORY DISCLOSURES",
        "hi": "5. कार्यप्रणाली एवं पीपीएसी नियामक प्रकटीकरण",
        "es": "5. METODOLOGÍA Y DIVULGACIONES REGULATORIAS DE PPAC",
        "fr": "5. MÉTHODOLOGIE ET DIVULGATIONS RÉGLEMENTAIRES PPAC",
        "ar": "5. المنهجية والإفصاحات التنظيمية الصادرة عن PPAC",
        "de": "5. METHODIK & REGULATORISCHE PPAC-OFFENLEGUNGEN",
        "zh": "5. 定价方法论规范与印度 PPAC 监管法规说明",
        "ru": "5. МЕТОДОЛОГИЯ И НОРМАТИВНЫЕ РАСКРЫТИЯ PPAC",
        "ja": "5. 算定方法論およびPPAC規制情報開示"
    },

    # --------------------------------------------------------------------------
    # SIDEBAR TRANSLATIONS
    # --------------------------------------------------------------------------
    "sidebar_tree_nav": {
        "en": "Tree Nav",
        "hi": "नेविगेशन ट्री",
        "es": "ÁRBOL DE NAVEGACIÓN",
        "fr": "ARBORESCENCE",
        "ar": "شجرة التنقل",
        "de": "NAVIGATION-TREE",
        "zh": "系统功能导航树",
        "ru": "НАВИГАЦИОННОЕ ДЕРЕВО",
        "ja": "ナビゲーションツリー"
    },
    "sidebar_drilldown": {
        "en": "🌿 Granular Drill-Down Tree",
        "hi": "🌿 विस्तृत विश्लेषण शाखाएं",
        "es": "🌿 Árbol de Detalle Granular",
        "fr": "🌿 Arborescence Détaillée",
        "ar": "🌿 شجرة التحليل المتعمق",
        "de": "🌿 Detaillierte Drilldown-Struktur",
        "zh": "🌿 深度钻取数据专题树",
        "ru": "🌿 Дерево детального анализа",
        "ja": "🌿 詳細ドリルダウンツリー"
    },
    "sidebar_01_command": {
        "en": "01. 🌐 Command Center",
        "hi": "01. 🌐 कमांड सेंटर",
        "es": "01. 🌐 Centro de Mando",
        "fr": "01. 🌐 Centre de Commandement",
        "ar": "01. 🌐 مركز القيادة الرئيسي",
        "de": "01. 🌐 Lagezentrum",
        "zh": "01. 🌐 全球能源态势中心",
        "ru": "01. 🌐 Главный командный центр",
        "ja": "01. 🌐 コマンドセンター"
    },
    "sidebar_02_explorer": {
        "en": "02. ⛽ Fuel Explorer",
        "hi": "02. ⛽ ईंधन एक्सप्लोरर",
        "es": "02. ⛽ Explorador de Combustible",
        "fr": "02. ⛽ Explorateur Carburant",
        "ar": "02. ⛽ مستكشف أسعار الوقود",
        "de": "02. ⛽ Kraftstoff-Explorer",
        "zh": "02. ⛽ 零售燃油价格探索器",
        "ru": "02. ⛽ Исследователь цен на топливо",
        "ja": "02. ⛽ 燃料価格エクスプローラー"
    },
    "sidebar_03_trade": {
        "en": "03. 🚢 Trade Flows",
        "hi": "03. 🚢 व्यापार प्रवाह",
        "es": "03. 🚢 Flujos Comerciales",
        "fr": "03. 🚢 Flux Commerciaux",
        "ar": "03. 🚢 تدفقات التجارة العالمية",
        "de": "03. 🚢 Handelsströme",
        "zh": "03. 🚢 原油贸易海运流向",
        "ru": "03. 🚢 Торговые потоки нефти",
        "ja": "03. 🚢 石油貿易フロー"
    },
    "sidebar_04_afford": {
        "en": "04. ⚖️ Affordability",
        "hi": "04. ⚖️ मूल्य सामर्थ्य",
        "es": "04. ⚖️ Asequibilidad",
        "fr": "04. ⚖️ Abordabilité",
        "ar": "04. ⚖️ القدرة على تحمل التكاليف",
        "de": "04. ⚖️ Erschwinglichkeit",
        "zh": "04. ⚖️ 人均负担力指数",
        "ru": "04. ⚖️ Ценовая доступность",
        "ja": "04. ⚖️ 燃料購入負担指数"
    },
    "sidebar_05_risk": {
        "en": "05. 🛡️ Supply Risk",
        "hi": "05. 🛡️ आपूर्ति जोखिम",
        "es": "05. 🛡️ Riesgo de Suministro",
        "fr": "05. 🛡️ Risque d'Approvisionnement",
        "ar": "05. 🛡️ مخاطر الإمدادات",
        "de": "05. 🛡️ Versorgungsrisiko",
        "zh": "05. 🛡️ 进口集中度风险 (HHI)",
        "ru": "05. 🛡️ Риск поставок",
        "ja": "05. 🛡️ 供給集中リスク"
    },
    "sidebar_06_shock": {
        "en": "06. ⚡ Shock Simulator",
        "hi": "06. ⚡ शॉक सिम्युलेटर",
        "es": "06. ⚡ Simulador de Choque",
        "fr": "06. ⚡ Simulateur de Choc",
        "ar": "06. ⚡ محاكي صدمات الإمداد",
        "de": "06. ⚡ Schock-Simulator",
        "zh": "06. ⚡ 供给短缺冲击模拟器",
        "ru": "06. ⚡ Симулятор шоков",
        "ja": "06. ⚡ 供給ショック・シミュレーター"
    },
    "sidebar_07_forecast": {
        "en": "07. 📈 Forecasting Radar",
        "hi": "07. 📈 पूर्वानुमान रडार",
        "es": "07. 📈 Radar de Pronósticos",
        "fr": "07. 📈 Radar de Prévisions",
        "ar": "07. 📈 رادار التنبؤ بالأسعار",
        "de": "07. 📈 Prognose-Radar",
        "zh": "07. 📈 机器学习价格预测雷达",
        "ru": "07. 📈 Прогнозный радар",
        "ja": "07. 📈 価格予測レーダー"
    },
    "sidebar_08_trust": {
        "en": "08. 🔒 Data Trust Center",
        "hi": "08. 🔒 डेटा प्रमाणिकता केंद्र",
        "es": "08. 🔒 Centro de Confianza de Datos",
        "fr": "08. 🔒 Centre de Confiance des Données",
        "ar": "08. 🔒 مركز موثوقية البيانات",
        "de": "08. 🔒 Datenintegritätszentrum",
        "zh": "08. 🔒 数据可信与接口审计",
        "ru": "08. 🔒 Центр достоверности данных",
        "ja": "08. 🔒 データ信頼性センター"
    },
    "sidebar_09_ai": {
        "en": "09. 🤖 AI Energy Analyst",
        "hi": "09. 🤖 एआई ऊर्जा विश्लेषक",
        "es": "09. 🤖 Analista de Energía IA",
        "fr": "09. 🤖 Analyste Énergie IA",
        "ar": "09. 🤖 محلل الطاقة الذكي",
        "de": "09. 🤖 KI-Energieanalyst",
        "zh": "09. 🤖 AI 能源大模型分析助手",
        "ru": "09. 🤖 ИИ-аналитик энергетики",
        "ja": "09. 🤖 AIエネルギーアナリスト"
    },
    "sidebar_10_india": {
        "en": "10. 🇮🇳 India Intelligence",
        "hi": "10. 🇮🇳 भारत ऊर्जा खुफिया",
        "es": "10. 🇮🇳 Inteligencia de India",
        "fr": "10. 🇮🇳 Renseignement Inde",
        "ar": "10. 🇮🇳 استخبارات الطاقة الهندية",
        "de": "10. 🇮🇳 Indien-Intelligence",
        "zh": "10. 🇮🇳 印度国家专项智库",
        "ru": "10. 🇮🇳 Аналитика Индии",
        "ja": "10. 🇮🇳 インド市場インテリジェンス"
    },
    "sidebar_11_guide": {
        "en": "11. 📖 Product Guide",
        "hi": "11. 📖 उत्पाद गाइड",
        "es": "11. 📖 Guía del Producto",
        "fr": "11. 📖 Guide du Produit",
        "ar": "11. 📖 دليل استخدام المنصة",
        "de": "11. 📖 Produkthandbuch",
        "zh": "11. 📖 平台使用手册与指南",
        "ru": "11. 📖 Руководство пользователя",
        "ja": "11. 📖 プロダクトガイド"
    },
    "sidebar_sync_title": {
        "en": "⚡ Live Pipeline Sync",
        "hi": "⚡ लाइव डेटा पाइपलाइन सिंक",
        "es": "⚡ Sincronización en Vivo",
        "fr": "⚡ Synchronisation en Direct",
        "ar": "⚡ مزامنة البيانات المباشرة",
        "de": "⚡ Live-Pipeline-Sync",
        "zh": "⚡ 实时数据同步管道",
        "ru": "⚡ Синхронизация данных",
        "ja": "⚡ リアルタイム同期パイプライン"
    },
    "sidebar_sync_btn": {
        "en": "⚡ Refresh Live Data",
        "hi": "⚡ लाइव डेटा रीफ्रेश करें",
        "es": "⚡ Actualizar Datos en Vivo",
        "fr": "⚡ Actualiser les Données",
        "ar": "⚡ تحديث البيانات المباشرة",
        "de": "⚡ Live-Daten aktualisieren",
        "zh": "⚡ 立即拉取最新实时数据",
        "ru": "⚡ Обновить данные",
        "ja": "⚡ 最新データを再取得"
    },
    "sidebar_provenance_title": {
        "en": "📡 DATA PROVENANCE & SYNC:",
        "hi": "📡 डेटा स्रोत एवं सिंक स्थिति:",
        "es": "📡 PROCEDENCIA Y ESTADO:",
        "fr": "📡 PROVENANCE ET ÉTAT :",
        "ar": "📡 مصدر البيانات والمزامنة:",
        "de": "📡 DATENQUELLE & STATUS:",
        "zh": "📡 数据源头认证与同步状态:",
        "ru": "📡 ИСТОЧНИК И СТАТУС ДАННЫХ:",
        "ja": "📡 データ出所と同期ステータス:"
    },

    # --------------------------------------------------------------------------
    # OTHER VIEWS HEADERS TRANSLATIONS
    # --------------------------------------------------------------------------
    "about_hero_title": {
        "en": "About Global FuelPulse AI",
        "hi": "ग्लोबल फ्यूलपल्स एआई के बारे में",
        "es": "Acerca de Global FuelPulse AI",
        "fr": "À Propos de Global FuelPulse AI",
        "ar": "حول منصة Global FuelPulse AI",
        "de": "Über Global FuelPulse AI",
        "zh": "关于 Global FuelPulse AI 全球能源智库",
        "ru": "О проекте Global FuelPulse AI",
        "ja": "Global FuelPulse AI について"
    },
    "about_hero_sub": {
        "en": "An open architectural dossier on global petroleum market forces, sovereign tax interventions, pass-through mechanics, and the mission behind this platform.",
        "hi": "वैश्विक पेट्रोलियम बाजार शक्तियों, संप्रभु कर हस्तक्षेपों और इस मंच के पीछे के मिशन पर एक खुला वास्तुशिल्प दस्तावेज।",
        "es": "Un informe arquitectónico abierto sobre las fuerzas del mercado petrolero, impuestos soberanos y la misión de la plataforma.",
        "fr": "Un dossier d'architecture ouvert sur les forces du marché pétrolier, les taxes souveraines et la mission de la plateforme.",
        "ar": "ملف تعريفي شامل حول قوى سوق النفط العالمية، والتدخلات الضريبية الحكومية، والمهمة التي تتبناها هذه المنصة.",
        "de": "Ein offenes Dossier über Rohölmarktkräfte, staatliche Steuereingriffe und die Mission hinter dieser Plattform.",
        "zh": "深入剖析全球原油供需力量、主权财税干预机制、成本传导逻辑及本平台核心工程使命的系统性文献。",
        "ru": "Открытое досье о силах мирового нефтяного рынка, налоговом регулировании и миссии платформы.",
        "ja": "世界の石油市場の原動力、主権国家の税制介入、価格転嫁メカニズム、そして本プラットフォームのミッションに関する解説。"
    },
    "how_hero_title": {
        "en": "How Global FuelPulse AI Works",
        "hi": "ग्लोबल फ्यूलपल्स एआई कैसे काम करता है",
        "es": "Cómo Funciona Global FuelPulse AI",
        "fr": "Comment Fonctionne Global FuelPulse AI",
        "ar": "كيف تعمل منصة Global FuelPulse AI",
        "de": "Funktionsweise von Global FuelPulse AI",
        "zh": "Global FuelPulse AI 架构与运作机理",
        "ru": "Как работает Global FuelPulse AI",
        "ja": "Global FuelPulse AI のシステム構成と動作原理"
    },
    "how_hero_sub": {
        "en": "An end-to-end technical walkthrough: from multi-source data ingestion to analytical normalization, econometric forecasting, and UI rendering.",
        "hi": "एंड-टू-एंड तकनीकी वॉकथ्रू: बहु-स्रोत डेटा अंतर्ग्रहण से विश्लेषणात्मक सामान्यीकरण, अर्थमितीय पूर्वानुमान और यूआई रेंडरिंग तक।",
        "es": "Recorrido técnico integral: desde la ingesta de datos multifuente hasta la normalización, pronósticos econométricos y renderizado.",
        "fr": "Visite technique de bout en bout : de l'ingestion de données multi-sources à la normalisation, prévisions et rendu.",
        "ar": "جولة تقنية شاملة: من جمع البيانات متعددة المصادر إلى المعالجة والنمذجة التنبؤية وعرض واجهة المستخدم.",
        "de": "Vollständiger technischer Durchstich: von der Datenaufnahme über Normalisierung bis zur ML-Prognose und Visualisierung.",
        "zh": "端到端技术链路全景揭秘：从异构多源数据自动化采集、规范化清洗，到计量经济学预测及响应式前端呈现。",
        "ru": "Полный технический обзор: от сбора данных из разных источников до нормализации, эконометрики и визуализации.",
        "ja": "エンドツーエンドの技術解説：マルチソースデータ収集から正規化、計量経済予測、UIレンダリングまで。"
    },
    "features_hero_title": {
        "en": "Platform Capability Catalog",
        "hi": "प्लेटफ़ॉर्म क्षमता सूची",
        "es": "Catálogo de Capacidades de la Plataforma",
        "fr": "Catalogue des Capacités de la Plateforme",
        "ar": "كتالوج قدرات ومميزات المنصة",
        "de": "Funktions- & Leistungskatalog",
        "zh": "平台核心功能与引擎全景目录",
        "ru": "Каталог возможностей платформы",
        "ja": "プラットフォーム機能全景カタログ"
    },
    "features_hero_sub": {
        "en": "Comprehensive inventory of analytical modules, predictive tools, and decision-support engines engineered into Global FuelPulse AI.",
        "hi": "ग्लोबल फ्यूलपल्स एआई में इंजीनियर किए गए विश्लेषणात्मक मॉड्यूल, पूर्वानुमान उपकरण और निर्णय-समर्थन इंजनों की विस्तृत सूची।",
        "es": "Inventario completo de módulos analíticos, herramientas predictivas y motores de decisión integrados en la plataforma.",
        "fr": "Inventaire complet des modules analytiques, outils prédictifs et moteurs décisionnels intégrés dans la plateforme.",
        "ar": "دليل شامل للوحدات التحليلية والأدوات التنبؤية ومحركات دعم القرار المدمجة في المنصة.",
        "de": "Umfassende Übersicht über analytische Module, Prognose-Tools und Entscheidungshilfen der Plattform.",
        "zh": "Global FuelPulse AI 原生构建的 12 项高阶分析引擎、预测模型与决策支持系统完整技术清单。",
        "ru": "Полный перечень аналитических модулей, инструментов прогнозирования и систем поддержки решений.",
        "ja": "Global FuelPulse AI に搭載された分析モジュール、予測ツール、意思決定支援エンジンの全機能一覧。"
    },
    "trust_hero_title": {
        "en": "Data Trust & Provider SLA Registry",
        "hi": "डेटा प्रमाणिकता एवं प्रदाता एसएलए रजिस्ट्री",
        "es": "Confianza de Datos y Registro de SLA",
        "fr": "Confiance des Données et Registre SLA",
        "ar": "سجل موثوقية البيانات ومستوى الخدمة (SLA)",
        "de": "Datenintegrität & SLA-Register",
        "zh": "数据透明度、数据信赖与数据源 SLA 注册表",
        "ru": "Достоверность данных и реестр SLA",
        "ja": "データ信頼性およびプロバイダーSLAレジストリ"
    },
    "trust_hero_sub": {
        "en": "Full transparency over observation frequencies, API authentication, licensing compliance, and data freshness telemetry.",
        "hi": "अवलोकन आवृत्तियों, एपीआई प्रमाणीकरण, लाइसेंस अनुपालन और डेटा ताजगी टेलीमेट्री पर पूरी पारदर्शिता।",
        "es": "Transparencia total sobre frecuencias de observación, autenticación de API, licencias y frescura de datos.",
        "fr": "Transparence totale sur la fréquence des données, authentification API, conformité des licences et fraîcheur des données.",
        "ar": "شفافية كاملة حول تواتر الرصد، والمصادقة على واجهات البرمجة، والامتثال للتراخيص، وحداثة البيانات.",
        "de": "Vollständige Transparenz über Erfassungszyklen, API-Authentifizierung, Lizenztreue und Datenaktualität.",
        "zh": "全景公开各官方接口采集频次、API 鉴权方式、数据版权合规许可及端到端数据新鲜度健康监测。",
        "ru": "Полная прозрачность частоты сбора, аутентификации API, лицензионной чистоты и свежести данных.",
        "ja": "観測頻度、API認証、ライセンス遵守状況、データ鮮度テレメトリに関する完全な透明性開示。"
    },
    "method_hero_title": {
        "en": "Mathematical & Algorithmic Methodology",
        "hi": "गणितीय एवं एल्गोरिथम कार्यप्रणाली",
        "es": "Metodología Matemática y Algorítmica",
        "fr": "Méthodologie Mathématique et Algorithmique",
        "ar": "المنهجية الرياضية والخوارزمية",
        "de": "Mathematische & Algorithmische Methodik",
        "zh": "系统核心数学公式与算法规范",
        "ru": "Математическая и алгоритмическая методология",
        "ja": "数学的・アルゴリズム的算定手法"
    },
    "method_hero_sub": {
        "en": "Deterministic mathematical specifications for HHI supplier concentration, affordability indices, and time-series forecasting.",
        "hi": "एचएचआई आपूर्तिकर्ता एकाग्रता, मूल्य सामर्थ्य सूचकांक और समय-श्रृंखला पूर्वानुमान के लिए सटीक गणितीय विनिर्देश।",
        "es": "Especificaciones matemáticas formales para concentración HHI, índices de asequibilidad y pronósticos de series temporales.",
        "fr": "Spécifications mathématiques rigoureuses pour la concentration HHI, les indices d'accessibilité et les prévisions.",
        "ar": "المواصفات الرياضية الدقيقة لحساب تركز الموردين (HHI)، ومؤشرات القدرة الشرائية، والتنبؤ بالسلاسل الزمنية.",
        "de": "Mathematische Formeln für HHI-Lieferantenkonzentration, Erschwinglichkeitsindizes und Zeitreihenprognosen.",
        "zh": "关于赫芬达尔-赫希曼供应商集中度指数 (HHI)、居民燃油消费负担指数及 Holt-Winters 时序预测模型的标准数学公式推导。",
        "ru": "Математические спецификации расчета индекса HHI, доступности топлива и временных рядов.",
        "ja": "HHI供給元集中度、購買負担指数、および時系列予測モデルに関する確定的な数学的仕様。"
    },
    "roadmap_hero_title": {
        "en": "Product Roadmap & Engineering Milestones",
        "hi": "उत्पाद रोडमैप एवं विकास मील के पत्थर",
        "es": "Hoja de Ruta del Producto e Hitos",
        "fr": "Feuille de Route et Jalons Techniques",
        "ar": "خارطة طريق المنتج والمعالم الهندسية",
        "de": "Produkt-Roadmap & Entwicklungs-Meilensteine",
        "zh": "产品演进路线图与技术里程碑",
        "ru": "Дорожная карта продукта и этапы разработки",
        "ja": "プロダクトロードマップおよび開発マイルストーン"
    },
    "roadmap_hero_sub": {
        "en": "Delivered architecture and upcoming horizon milestones: from core ingestion to satellite AIS tracking and enterprise API gateways.",
        "hi": "वितरित वास्तुकला और आगामी मील के पत्थर: मुख्य अंतर्ग्रहण से लेकर उपग्रह एआईएस ट्रैकिंग और उद्यम एपीआई गेटवे तक।",
        "es": "Arquitectura implementada y próximos hitos: desde la ingesta central hasta el rastreo satelital AIS y pasarelas API.",
        "fr": "Architecture livrée et jalons futurs : de l'ingestion centrale au suivi satellite AIS et passerelles API d'entreprise.",
        "ar": "المراحل الهندسية المنجزة والمستقبلية: من تجميع البيانات إلى تتبع السفن عبر الأقمار الصناعية وبوابات API المؤسسية.",
        "de": "Realisierte Architektur und zukünftige Meilensteine: von Datenaufnahme bis zu Satelliten-AIS und Unternehmens-APIs.",
        "zh": "已落地系统架构与未来演进路线：从核心异构数据采集中枢，到卫星 AIS 实时油轮追踪及企业级开放 API 网关。",
        "ru": "Реализованная архитектура и ориентиры развития: от сбора данных до спутникового трекинга AIS и API-шлюзов.",
        "ja": "実装済みアーキテクチャと今後の開発目標：データ収集から衛星AIS船舶追跡、エンタープライズAPIゲートウェイまで。"
    },
    "faq_hero_title": {
        "en": "Knowledge Base & Technical Documentation",
        "hi": "ज्ञानकोष एवं तकनीकी दस्तावेज",
        "es": "Base de Conocimientos y Documentación",
        "fr": "Base de Connaissances et Documentation",
        "ar": "قاعدة المعرفة والتوثيق الفني",
        "de": "Wissensdatenbank & Technische Dokumentation",
        "zh": "知识库、技术白皮书与架构问答",
        "ru": "База знаний и техническая документация",
        "ja": "ナレッジベースおよび技術ドキュメント"
    },
    "faq_hero_sub": {
        "en": "Frequently asked technical, operational, and data modeling questions about Global FuelPulse AI.",
        "hi": "ग्लोबल फ्यूलपल्स एआई के बारे में अक्सर पूछे जाने वाले तकनीकी, परिचालन और डेटा मॉडलिंग प्रश्न।",
        "es": "Preguntas frecuentes sobre aspectos técnicos, operativos y de modelado de datos de la plataforma.",
        "fr": "Questions fréquentes sur les aspects techniques, opérationnels et de modélisation des données.",
        "ar": "الأسئلة الشائعة حول الجوانب التقنية والتشغيلية ونمذجة البيانات في المنصة.",
        "de": "Häufig gestellte Fragen zu Technik, Betrieb und Datenmodellierung der Plattform.",
        "zh": "关于 Global FuelPulse AI 系统架构、实时数据管道运维及计量经济学建模的常见疑难解答。",
        "ru": "Часто задаваемые вопросы по технической части, архитектуре и моделированию данных.",
        "ja": "Global FuelPulse AI の技術仕様、運用体制、データモデリングに関するFAQ集。"
    }
}


# ==============================================================================
# 3. HELPER FUNCTIONS
# ==============================================================================
def get_current_language() -> str:
    """
    Retrieves the currently selected language code from session state or URL params.
    Defaults to 'en'.
    """
    if "app_language" not in st.session_state:
        # Check query param first
        qp_lang = st.query_params.get("lang")
        if qp_lang and qp_lang in SUPPORTED_LANGUAGES:
            st.session_state["app_language"] = qp_lang
        else:
            st.session_state["app_language"] = "en"
    return st.session_state["app_language"]


def set_language(lang_code: str) -> None:
    """Updates the active application language in session state and query parameters."""
    if lang_code in SUPPORTED_LANGUAGES:
        st.session_state["app_language"] = lang_code
        st.query_params["lang"] = lang_code


def t(key: str, lang: Optional[str] = None, **kwargs) -> str:
    """
    Safely retrieves the localized string for a given translation key.
    Falls back to English if key is missing in the target language.
    If key is completely unknown, returns key itself.
    Supports str.format kwargs.
    """
    active_lang = lang or get_current_language()
    
    if key in TRANSLATIONS:
        lang_dict = TRANSLATIONS[key]
        text = lang_dict.get(active_lang) or lang_dict.get("en") or key
    else:
        text = key
        
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text


def get_available_languages() -> Dict[str, Dict[str, str]]:
    """Returns the full catalog of supported languages."""
    return SUPPORTED_LANGUAGES


def get_localized_nav_map(lang: Optional[str] = None) -> Dict[str, str]:
    """
    Returns a dictionary mapping canonical navigation IDs to their localized labels:
    e.g. {'home': '🏠 अवलोकन', 'dashboard': '⚡ इंटेलिजेंस डैशबोर्ड', ...}
    """
    active_lang = lang or get_current_language()
    nav_keys = [
        ("home", "nav_overview"),
        ("dashboard", "nav_dashboard"),
        ("india", "nav_india"),
        ("about", "nav_about"),
        ("how_it_works", "nav_how_it_works"),
        ("features", "nav_features"),
        ("data_trust", "nav_data_trust"),
        ("methodology", "nav_methodology"),
        ("roadmap", "nav_roadmap"),
        ("faq", "nav_faq")
    ]
    return {canonical: t(key, active_lang) for canonical, key in nav_keys}
