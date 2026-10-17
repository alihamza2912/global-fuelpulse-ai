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
        "ja": "グローバル・フューエルパルス AI"
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
        "ja": "エネルギー市場情報プラットフォーム"
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
        "ja": "ライブ 2026"
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
        "ja": "SQLITE 検証済み"
    },
    "select_language": {
        "en": "Language",
        "hi": "भाषा चुनें",
        "es": "Idioma",
        "fr": "Langue",
        "ar": "اللغة",
        "de": "Sprache",
        "zh": "语言选择",
        "ru": "Язык",
        "ja": "言語"
    },
    "live_news_button": {
        "en": "🔔 LIVE NEWS",
        "hi": "🔔 लाइव समाचार",
        "es": "🔔 NOTICIAS EN VIVO",
        "fr": "🔔 ACTUALITÉS EN DIRECT",
        "ar": "🔔 أخبار عاجلة",
        "de": "🔔 LIVE-NACHRICHTEN",
        "zh": "🔔 实时快讯",
        "ru": "🔔 СВЕЖИЕ НОВОСТИ",
        "ja": "🔔 ライブニュース"
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
        "ja": "🔄 フィード更新"
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
        "ja": "🏠 概要"
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
        "ja": "⚡ インテリジェンス・ダッシュボード"
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
        "ja": "🇮🇳 インド燃料センター"
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
        "ja": "🚢 貿易とホルムズ海峡"
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
        "ja": "⚖️ 燃料購入負担指数"
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
        "ja": "🛡️ 供給リスク評価"
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
        "ja": "⚡ 供給ショック・シミュレーター"
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
        "ja": "📈 価格予測レーダー"
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
        "ja": "🔒 データ信頼性センター"
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
        "ja": "🤖 AIエネルギーアナリスト"
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
        "ja": "📖 プロジェクトについて"
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
        "ja": "⚙️ システム構造と動作原理"
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
        "ja": "📋 プラットフォーム機能一覧"
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
        "ja": "📐 算定手法とアルゴリズム"
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
        "ja": "🗺️ ロードマップと開発計画"
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
        "ja": "❓ ドキュメントとよくある質問"
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
