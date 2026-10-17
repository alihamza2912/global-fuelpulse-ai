"""
Global Fuel & Sovereign/State Tax Intelligence Engine.
Provides comprehensive price decomposition and tax breakdown for all 28 Indian States,
8 Union Territories, major Indian cities (e.g. Prayagraj, Lucknow, Mumbai, Bengaluru, etc.),
and premier global jurisdictions (USA states, Canada provinces, UK, Germany, France, Japan, etc.).
"""

from typing import Dict, Any, List, Optional
import math


class GlobalTaxEngine:
    """
    Sub-millisecond resolution engine for retail fuel pricing, central/federal excise duties,
    and state/provincial VAT or sales taxes.
    """

    # USD to INR benchmark exchange rate
    USD_INR_RATE = 86.60
    # EUR to USD benchmark
    EUR_USD_RATE = 1.08
    # GBP to USD benchmark
    GBP_USD_RATE = 1.30
    # CAD to USD benchmark
    CAD_USD_RATE = 0.73
    # JPY to USD benchmark
    JPY_USD_RATE = 0.0067
    # AUD to USD benchmark
    AUD_USD_RATE = 0.65
    # AED to USD benchmark
    AED_USD_RATE = 0.2723
    # SAR to USD benchmark
    SAR_USD_RATE = 0.2667
    # BRL to USD benchmark
    BRL_USD_RATE = 0.18

    # ==========================================================================
    # 1. INDIAN STATES AND UNION TERRITORIES TAX DATABASE (MoPNG & State VAT Circulars)
    # All petrol rates strictly > ₹100/L.
    # ==========================================================================
    INDIA_TAX_DATA: Dict[str, Dict[str, Any]] = {
        "Uttar Pradesh": {
            "type": "Indian State",
            "capital": "Lucknow",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Uttar Pradesh (Commercial Tax Dept)",
            "vat_petrol_pct": 19.36,
            "vat_petrol_min": 14.85,
            "vat_diesel_pct": 15.54,
            "vat_diesel_min": 10.45,
            "petrol_rsp": 101.45,
            "diesel_rsp": 93.30,
            "base_petrol": 57.40,
            "freight_petrol": 0.35,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.32,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "prayagraj", "allahabad", "lucknow", "kanpur", "varanasi", "banaras", "kashi",
                "noida", "greater noida", "ghaziabad", "agra", "meerut", "bareilly", "aligarh",
                "moradabad", "gorakhpur", "mathura", "firozabad", "jhansi", "muzaffarnagar",
                "ayodhya", "faizabad", "saharanpur", "etawah", "mirzapur", "raebareli"
            ],
            "tax_statute_note": "Levies 19.36% ad-valorem VAT (with minimum floor rate of ₹14.85/L) on petrol and 15.54% on diesel under UP VAT Act 2008."
        },
        "Maharashtra": {
            "type": "Indian State",
            "capital": "Mumbai",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Maharashtra (State GST & VAT)",
            "vat_petrol_pct": 25.0,
            "vat_petrol_cess": 5.12,
            "vat_diesel_pct": 21.0,
            "vat_diesel_cess": 3.00,
            "petrol_rsp": 106.31,
            "diesel_rsp": 94.27,
            "base_petrol": 57.40,
            "freight_petrol": 0.38,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.35,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "mumbai", "bombay", "pune", "nagpur", "nashik", "thane", "aurangabad",
                "chhatrapati sambhajinagar", "solapur", "navi mumbai", "kolhapur", "amravati",
                "nanded", "jalgaon", "akola", "latur", "dhule", "ahmednagar", "satara"
            ],
            "tax_statute_note": "Levies 25% ad-valorem VAT plus an additional ₹5.12/L state drought and infrastructure surcharge cess on motor spirit."
        },
        "Delhi (NCT)": {
            "type": "Union Territory & National Capital",
            "capital": "New Delhi",
            "flag": "🇮🇳",
            "statutory_authority": "Government of NCT of Delhi (Department of Trade & Taxes)",
            "vat_petrol_pct": 19.40,
            "vat_diesel_pct": 16.75,
            "petrol_rsp": 102.12,
            "diesel_rsp": 95.20,
            "base_petrol": 57.50,
            "freight_petrol": 0.36,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 59.80,
            "freight_diesel": 0.38,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "delhi", "new delhi", "dwarka", "rohini", "saket", "nct", "connaught place",
                "vasant kunj", "pitampura", "karol bagh", "chandni chowk"
            ],
            "tax_statute_note": "Levies 19.40% ad-valorem VAT under Delhi Value Added Tax Act, maintaining standard capital benchmark parity."
        },
        "Karnataka": {
            "type": "Indian State",
            "capital": "Bengaluru",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Karnataka (Commercial Taxes Department)",
            "vat_petrol_pct": 29.84,
            "vat_diesel_pct": 18.44,
            "petrol_rsp": 102.86,
            "diesel_rsp": 88.94,
            "base_petrol": 57.40,
            "freight_petrol": 0.36,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.32,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "bengaluru", "bangalore", "mysuru", "mysore", "mangaluru", "mangalore",
                "hubballi", "hubli", "belagavi", "belgaum", "davangere", "ballari",
                "vijayapura", "shivamogga", "tumakuru", "raichur", "bidar", "hassan"
            ],
            "tax_statute_note": "Karnataka Sales Tax (KST) rate revised to 29.84% on petrol and 18.44% on diesel to fund state social guarantees."
        },
        "Tamil Nadu": {
            "type": "Indian State",
            "capital": "Chennai",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Tamil Nadu (Commercial Taxes Department)",
            "vat_petrol_pct": 13.0,
            "vat_petrol_cess": 11.52,
            "vat_diesel_pct": 11.0,
            "vat_diesel_cess": 9.62,
            "petrol_rsp": 102.63,
            "diesel_rsp": 94.24,
            "base_petrol": 57.40,
            "freight_petrol": 0.40,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.38,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "chennai", "madras", "coimbatore", "madurai", "tiruchirappalli", "trichy",
                "salem", "tirunelveli", "tiruppur", "erode", "vellore", "thoothukudi",
                "dindigul", "thanjavur", "ranipet", "sivakasi", "karur"
            ],
            "tax_statute_note": "Levies hybrid ad-valorem plus specific tax: 13% + ₹11.52/L on petrol and 11% + ₹9.62/L on diesel."
        },
        "West Bengal": {
            "type": "Indian State",
            "capital": "Kolkata",
            "flag": "🇮🇳",
            "statutory_authority": "Government of West Bengal (Directorate of Commercial Taxes)",
            "vat_petrol_pct": 25.0,
            "vat_petrol_min": 13.12,
            "vat_diesel_pct": 17.0,
            "vat_diesel_min": 7.70,
            "petrol_rsp": 105.85,
            "diesel_rsp": 92.76,
            "base_petrol": 57.40,
            "freight_petrol": 0.44,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.40,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "kolkata", "calcutta", "howrah", "durgapur", "asansol", "siliguri",
                "bardhaman", "malda", "kharagpur", "haldia", "habra", "shantipur", "berhampore"
            ],
            "tax_statute_note": "Levies 25% ad-valorem sales tax on petrol or ₹13.12/L (whichever is higher) plus state transport rebate concessions."
        },
        "Rajasthan": {
            "type": "Indian State",
            "capital": "Jaipur",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Rajasthan (Commercial Taxes Department)",
            "vat_petrol_pct": 31.04,
            "vat_petrol_cess": 1.50,
            "vat_diesel_pct": 19.30,
            "vat_diesel_cess": 1.75,
            "petrol_rsp": 108.48,
            "diesel_rsp": 93.72,
            "base_petrol": 57.40,
            "freight_petrol": 0.45,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.42,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "jaipur", "jodhpur", "udaipur", "kota", "bikaner", "ajmer", "bhilwara",
                "alwar", "sikar", "sri ganganagar", "pali", "chittorgarh", "bharatpur"
            ],
            "tax_statute_note": "Highest state tax regime in northern India: 31.04% VAT + ₹1.50/L road development cess on motor spirit."
        },
        "Bihar": {
            "type": "Indian State",
            "capital": "Patna",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Bihar (Commercial Taxes Department)",
            "vat_petrol_pct": 23.58,
            "vat_diesel_pct": 19.00,
            "petrol_rsp": 107.24,
            "diesel_rsp": 94.04,
            "base_petrol": 57.40,
            "freight_petrol": 0.50,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.45,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "patna", "gaya", "bhagalpur", "muzaffarpur", "purnia", "darbhanga",
                "bihar sharif", "arrah", "begusarai", "katihar", "munger", "chhapra", "sasaram"
            ],
            "tax_statute_note": "Levies 23.58% ad-valorem VAT under Bihar Value Added Tax Ordinance, compensating for landlocked freight logistics."
        },
        "Gujarat": {
            "type": "Indian State",
            "capital": "Gandhinagar",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Gujarat (Commercial Tax Department)",
            "vat_petrol_pct": 13.7,
            "vat_petrol_cess": 4.0,
            "vat_diesel_pct": 14.9,
            "vat_diesel_cess": 4.0,
            "petrol_rsp": 101.10,
            "diesel_rsp": 92.40,
            "base_petrol": 57.40,
            "freight_petrol": 0.28,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.25,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "ahmedabad", "surat", "vadodara", "baroda", "rajkot", "bhavnagar",
                "jamnagar", "gandhinagar", "junagadh", "anand", "navsari", "morbi", "bharuch"
            ],
            "tax_statute_note": "Levies 13.7% basic VAT plus 4% education & welfare cess on motor spirit; benefits from local refinery hubs (Jamnagar/Vadinar)."
        },
        "Telangana": {
            "type": "Indian State",
            "capital": "Hyderabad",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Telangana (Commercial Taxes Dept)",
            "vat_petrol_pct": 35.20,
            "vat_diesel_pct": 27.00,
            "petrol_rsp": 109.66,
            "diesel_rsp": 97.82,
            "base_petrol": 57.40,
            "freight_petrol": 0.42,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.38,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "hyderabad", "secunderabad", "warangal", "nizamabad", "karimnagar",
                "khammam", "ramagundam", "mahbubnagar", "nalgonda", "adilabad", "siddipet"
            ],
            "tax_statute_note": "Highest ad-valorem state VAT rate in India at 35.20% on petrol, resulting in elevated retail pump prices across the state."
        },
        "Andhra Pradesh": {
            "type": "Indian State",
            "capital": "Amaravati",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Andhra Pradesh (Commercial Taxes Department)",
            "vat_petrol_pct": 31.0,
            "vat_petrol_cess": 5.0,
            "vat_diesel_pct": 22.25,
            "vat_diesel_cess": 4.0,
            "petrol_rsp": 109.80,
            "diesel_rsp": 97.60,
            "base_petrol": 57.40,
            "freight_petrol": 0.40,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.36,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "amaravati", "visakhapatnam", "vizag", "vijayawada", "guntur", "nellore",
                "kurnool", "tirupati", "kakinada", "rajamahendravaram", "kadapa", "anantapur", "eluru"
            ],
            "tax_statute_note": "Levies 31% VAT plus ₹4/L additional VAT + ₹1/L road development cess on petrol."
        },
        "Kerala": {
            "type": "Indian State",
            "capital": "Thiruvananthapuram",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Kerala (State Taxes Department)",
            "vat_petrol_pct": 30.08,
            "vat_petrol_cess": 2.0,
            "vat_diesel_pct": 22.76,
            "vat_diesel_cess": 2.0,
            "petrol_rsp": 107.56,
            "diesel_rsp": 96.43,
            "base_petrol": 57.40,
            "freight_petrol": 0.38,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.35,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "thiruvananthapuram", "trivandrum", "kochi", "cochin", "ernakulam",
                "kozhikode", "calicut", "thrissur", "kollam", "kannur", "alappuzha",
                "palakkad", "kottayam", "malappuram"
            ],
            "tax_statute_note": "Levies 30.08% sales tax plus ₹2/L social security cess on petrol to fund state pension schemes."
        },
        "Madhya Pradesh": {
            "type": "Indian State",
            "capital": "Bhopal",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Madhya Pradesh (Commercial Tax Dept)",
            "vat_petrol_pct": 29.0,
            "vat_petrol_cess": 4.50,
            "vat_diesel_pct": 19.0,
            "vat_diesel_cess": 3.00,
            "petrol_rsp": 108.65,
            "diesel_rsp": 93.90,
            "base_petrol": 57.40,
            "freight_petrol": 0.46,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.40,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "bhopal", "indore", "jabalpur", "gwalior", "ujjain", "sagar",
                "dewas", "satna", "ratlam", "rewa", "katni", "singrauli", "burhanpur"
            ],
            "tax_statute_note": "Levies 29% VAT plus ₹4.50/L cess on petrol and 19% + ₹3.00/L cess on diesel under MP VAT Act."
        },
        "Punjab": {
            "type": "Indian State",
            "capital": "Chandigarh",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Punjab (Excise & Taxation Department)",
            "vat_petrol_pct": 15.74,
            "vat_petrol_cess": 1.10,
            "vat_diesel_pct": 12.00,
            "vat_diesel_cess": 1.10,
            "petrol_rsp": 101.43,
            "diesel_rsp": 91.68,
            "base_petrol": 57.40,
            "freight_petrol": 0.34,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.30,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "ludhiana", "amritsar", "jalandhar", "patiala", "bathinda", "mohali",
                "hoshiarpur", "batala", "pathankot", "moga", "abohar", "malerkotla"
            ],
            "tax_statute_note": "Levies 15.74% VAT + cess on petrol; adjusted to maintain agricultural logistics viability."
        },
        "Haryana": {
            "type": "Indian State",
            "capital": "Chandigarh",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Haryana (Excise & Taxation Department)",
            "vat_petrol_pct": 18.20,
            "vat_diesel_pct": 16.00,
            "petrol_rsp": 101.80,
            "diesel_rsp": 92.40,
            "base_petrol": 57.40,
            "freight_petrol": 0.32,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.28,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "gurugram", "gurgaon", "faridabad", "panipat", "ambala", "yamunanagar",
                "rohtak", "hisar", "karnal", "sonipat", "panchkula", "sirsa", "bhiwani", "bahadurgarh"
            ],
            "tax_statute_note": "Levies 18.20% VAT on petrol; benefits from proximity to Panipat Refinery hub."
        },
        "Odisha": {
            "type": "Indian State",
            "capital": "Bhubaneswar",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Odisha (Commercial Taxes)",
            "vat_petrol_pct": 28.0,
            "vat_diesel_pct": 24.0,
            "petrol_rsp": 103.19,
            "diesel_rsp": 94.76,
            "base_petrol": 57.40,
            "freight_petrol": 0.36,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.32,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "bhubaneswar", "cuttack", "rourkela", "berhampur", "sambalpur",
                "puri", "balasore", "bhadrak", "baripada", "jharsuguda", "paradip"
            ],
            "tax_statute_note": "Levies 28% VAT on petrol and 24% on diesel under Odisha Value Added Tax Act; coastal Paradip refinery terminal."
        },
        "Assam": {
            "type": "Indian State",
            "capital": "Dispur",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Assam (Commissioner of Taxes)",
            "vat_petrol_pct": 25.5,
            "vat_petrol_min": 17.5,
            "vat_diesel_pct": 17.5,
            "petrol_rsp": 101.20,
            "diesel_rsp": 90.30,
            "base_petrol": 57.40,
            "freight_petrol": 0.40,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.35,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "guwahati", "dispur", "silchar", "dibrugarh", "jorhat", "nagaon",
                "tinsukia", "tezpur", "bongaigaon", "karimganj", "sivasagar", "digboi"
            ],
            "tax_statute_note": "Northeast regional refining hub (Digboi, Guwahati, Numaligarh, Bongaigaon); levies 25.5% VAT on petrol."
        },
        "Jharkhand": {
            "type": "Indian State",
            "capital": "Ranchi",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Jharkhand (Commercial Taxes)",
            "vat_petrol_pct": 22.0,
            "vat_diesel_pct": 22.0,
            "petrol_rsp": 102.80,
            "diesel_rsp": 94.50,
            "base_petrol": 57.40,
            "freight_petrol": 0.42,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.38,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "ranchi", "jamshedpur", "dhanbad", "bokaro", "deoghar",
                "hazaribagh", "giridih", "ramgarh", "medininagar", "chirkunda"
            ],
            "tax_statute_note": "Levies 22% VAT on both petrol and diesel under Jharkhand VAT Act."
        },
        "Chhattisgarh": {
            "type": "Indian State",
            "capital": "Raipur",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Chhattisgarh (Commercial Tax)",
            "vat_petrol_pct": 24.0,
            "vat_petrol_cess": 2.0,
            "vat_diesel_pct": 23.0,
            "vat_diesel_cess": 1.0,
            "petrol_rsp": 102.98,
            "diesel_rsp": 94.94,
            "base_petrol": 57.40,
            "freight_petrol": 0.44,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.40,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "raipur", "bilaspur", "durg", "bhilai", "korba", "rajnandgaon",
                "jagdalpur", "ambikapur", "dhamtari", "raigarh"
            ],
            "tax_statute_note": "Levies 24% VAT plus ₹2/L urban development cess on petrol."
        },
        "Uttarakhand": {
            "type": "Indian State",
            "capital": "Dehradun",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Uttarakhand (State Tax Dept)",
            "vat_petrol_pct": 20.0,
            "vat_diesel_pct": 15.0,
            "petrol_rsp": 101.40,
            "diesel_rsp": 92.20,
            "base_petrol": 57.40,
            "freight_petrol": 0.38,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.34,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "dehradun", "haridwar", "roorkee", "haldwani", "rudrapur",
                "kashipur", "rishikesh", "nainital", "pithoragarh"
            ],
            "tax_statute_note": "Levies 20% VAT on petrol and 15% on diesel; hilly terrain freight offset."
        },
        "Himachal Pradesh": {
            "type": "Indian State",
            "capital": "Shimla",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Himachal Pradesh (State Taxes and Excise)",
            "vat_petrol_pct": 17.5,
            "vat_diesel_pct": 13.9,
            "petrol_rsp": 101.30,
            "diesel_rsp": 91.80,
            "base_petrol": 57.40,
            "freight_petrol": 0.42,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.38,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "shimla", "dharamshala", "solan", "mandi", "kullu", "manali", "baddi", "palampur", "bilaspur hp", "hamirpur"
            ],
            "tax_statute_note": "Levies 17.5% VAT on petrol; higher transport freight compensated by moderate state VAT."
        },
        "Jammu and Kashmir": {
            "type": "Union Territory",
            "capital": "Srinagar / Jammu",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Jammu and Kashmir (State Taxes Dept)",
            "vat_petrol_pct": 21.0,
            "vat_diesel_pct": 16.0,
            "petrol_rsp": 101.60,
            "diesel_rsp": 92.50,
            "base_petrol": 57.40,
            "freight_petrol": 0.46,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.42,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "srinagar", "jammu", "anantnag", "baramulla", "udhampur",
                "katra", "sopore", "kathua", "rajouri", "pulwama"
            ],
            "tax_statute_note": "Levies 21% VAT on motor spirit with special winter freight provisions for Kashmir valley."
        },
        "Goa": {
            "type": "Indian State",
            "capital": "Panaji",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Goa (Commercial Tax Department)",
            "vat_petrol_pct": 20.0,
            "vat_diesel_pct": 18.0,
            "petrol_rsp": 101.10,
            "diesel_rsp": 91.90,
            "base_petrol": 57.40,
            "freight_petrol": 0.30,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.28,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": [
                "panaji", "panjim", "margao", "vasco da gama", "mapusa", "ponda", "calangute"
            ],
            "tax_statute_note": "Goa maintains among the lowest coastal VAT structures (20% on petrol) in western India."
        },
        "Chandigarh": {
            "type": "Union Territory",
            "capital": "Chandigarh",
            "flag": "🇮🇳",
            "statutory_authority": "Chandigarh Administration (Excise & Taxation)",
            "vat_petrol_pct": 15.24,
            "vat_diesel_pct": 11.40,
            "petrol_rsp": 101.20,
            "diesel_rsp": 91.50,
            "base_petrol": 57.40,
            "freight_petrol": 0.32,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.28,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": ["chandigarh", "manimajra"],
            "tax_statute_note": "UT administration maintains uniform 15.24% VAT to avoid retail arbitrage with Punjab and Haryana."
        },
        "Puducherry": {
            "type": "Union Territory",
            "capital": "Puducherry",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Puducherry (Commercial Taxes)",
            "vat_petrol_pct": 14.55,
            "vat_diesel_pct": 12.25,
            "petrol_rsp": 100.80,
            "diesel_rsp": 90.75,
            "base_petrol": 57.40,
            "freight_petrol": 0.35,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.30,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": ["puducherry", "pondicherry", "karaikal", "mahe", "yanam"],
            "tax_statute_note": "Low VAT enclave with 14.55% on petrol, frequently attracting cross-border refuelling."
        },
        "Tripura": {
            "type": "Indian State",
            "capital": "Agartala",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Tripura (Taxes & Excise)",
            "vat_petrol_pct": 22.0,
            "vat_diesel_pct": 18.0,
            "petrol_rsp": 101.35,
            "diesel_rsp": 90.40,
            "base_petrol": 57.40,
            "freight_petrol": 0.55,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.48,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": ["agartala", "dharmanagar", "udaipur tripura", "kailashahar"],
            "tax_statute_note": "Northeastern state pricing factoring multimodal freight transport via Assam rail corridors."
        },
        "Meghalaya": {
            "type": "Indian State",
            "capital": "Shillong",
            "flag": "🇮🇳",
            "statutory_authority": "Government of Meghalaya (Taxation Dept)",
            "vat_petrol_pct": 20.0,
            "vat_diesel_pct": 14.5,
            "petrol_rsp": 101.15,
            "diesel_rsp": 89.90,
            "base_petrol": 57.40,
            "freight_petrol": 0.50,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.44,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": ["shillong", "tura", "jowai", "nongpoh"],
            "tax_statute_note": "20% state VAT balancing consumer price sensitivity in highland tribal autonomous districts."
        },
        "Ladakh": {
            "type": "Union Territory",
            "capital": "Leh",
            "flag": "🇮🇳",
            "statutory_authority": "Administration of Union Territory of Ladakh",
            "vat_petrol_pct": 19.5,
            "vat_diesel_pct": 15.0,
            "petrol_rsp": 102.50,
            "diesel_rsp": 93.80,
            "base_petrol": 57.40,
            "freight_petrol": 0.95,
            "central_excise_petrol": 19.90,
            "dealer_margin_petrol": 3.86,
            "base_diesel": 58.80,
            "freight_diesel": 0.85,
            "central_excise_diesel": 15.80,
            "dealer_margin_diesel": 2.62,
            "cities": ["leh", "kargil", "nubra", "drass", "zanskar"],
            "tax_statute_note": "High-altitude strategic frontier with highest inland freight cushion; special winter-grade fuel blends."
        }
    }

    # ==========================================================================
    # 2. GLOBAL JURISDICTIONS (USA STATES, CANADA, UK, EU, ASIA, MIDDLE EAST)
    # Calibrated to official IEA, EIA, and European Commission fuel bulletins.
    # ==========================================================================
    GLOBAL_TAX_DATA: Dict[str, Dict[str, Any]] = {
        "California": {
            "country": "United States",
            "country_iso3": "USA",
            "type": "US State",
            "capital": "Sacramento",
            "flag": "🇺🇸",
            "currency": "USD",
            "currency_symbol": "$",
            "statutory_authority": "California Dept of Tax and Fee Administration (CDTFA)",
            "petrol_rsp": 1.28,      # USD / Litre ($4.85 / gal)
            "diesel_rsp": 1.37,      # USD / Litre ($5.20 / gal)
            "petrol_per_gal": 4.85,
            "diesel_per_gal": 5.20,
            "base_petrol": 0.82,     # Crude + Refining
            "freight_petrol": 0.05,
            "federal_excise_petrol": 0.0486, # $0.184/gal
            "dealer_margin_petrol": 0.18,
            "state_tax_petrol": 0.1814,      # $0.686/gal (Excise + LCFS + Cap-and-Trade + Sales tax)
            "state_tax_pct": 14.2,
            "cities": [
                "california", "ca", "los angeles", "la", "san francisco", "sf", "san diego",
                "san jose", "fresno", "sacramento", "long beach", "oakland", "bakersfield", "anaheim"
            ],
            "tax_statute_note": "Highest fuel tax regime in the US: $0.68/gal combining state motor vehicle fuel tax, cap-and-trade carbon fees, Low Carbon Fuel Standard (LCFS), and state sales tax."
        },
        "Texas": {
            "country": "United States",
            "country_iso3": "USA",
            "type": "US State",
            "capital": "Austin",
            "flag": "🇺🇸",
            "currency": "USD",
            "currency_symbol": "$",
            "statutory_authority": "Texas Comptroller of Public Accounts",
            "petrol_rsp": 0.78,      # USD / Litre ($2.95 / gal)
            "diesel_rsp": 0.91,      # USD / Litre ($3.45 / gal)
            "petrol_per_gal": 2.95,
            "diesel_per_gal": 3.45,
            "base_petrol": 0.52,
            "freight_petrol": 0.03,
            "federal_excise_petrol": 0.0486, # $0.184/gal
            "dealer_margin_petrol": 0.12,
            "state_tax_petrol": 0.0528,      # $0.20/gal state gasoline tax
            "state_tax_pct": 6.8,
            "cities": [
                "texas", "tx", "houston", "dallas", "austin", "san antonio",
                "fort worth", "el paso", "arlington", "corpus christi", "plano", "lubbock"
            ],
            "tax_statute_note": "Major global refining hub on Gulf Coast. Levies flat $0.20/gal state motor fuel tax, keeping consumer pump prices among lowest in industrial nations."
        },
        "New York": {
            "country": "United States",
            "country_iso3": "USA",
            "type": "US State",
            "capital": "Albany",
            "flag": "🇺🇸",
            "currency": "USD",
            "currency_symbol": "$",
            "statutory_authority": "New York State Department of Taxation and Finance",
            "petrol_rsp": 0.91,      # USD / Litre ($3.45 / gal)
            "diesel_rsp": 1.05,      # USD / Litre ($3.98 / gal)
            "petrol_per_gal": 3.45,
            "diesel_per_gal": 3.98,
            "base_petrol": 0.60,
            "freight_petrol": 0.04,
            "federal_excise_petrol": 0.0486,
            "dealer_margin_petrol": 0.13,
            "state_tax_petrol": 0.0914,      # $0.346/gal
            "state_tax_pct": 10.0,
            "cities": [
                "new york", "ny", "nyc", "new york city", "buffalo", "rochester",
                "yonkers", "syracuse", "albany", "brooklyn", "manhattan", "queens"
            ],
            "tax_statute_note": "Combines state motor fuel tax, petroleum business tax (PBT), and state/local sales tax (~$0.346/gal total state levy)."
        },
        "Florida": {
            "country": "United States",
            "country_iso3": "USA",
            "type": "US State",
            "capital": "Tallahassee",
            "flag": "🇺🇸",
            "currency": "USD",
            "currency_symbol": "$",
            "statutory_authority": "Florida Department of Revenue",
            "petrol_rsp": 0.86,      # USD / Litre ($3.25 / gal)
            "diesel_rsp": 0.98,      # USD / Litre ($3.70 / gal)
            "petrol_per_gal": 3.25,
            "diesel_per_gal": 3.70,
            "base_petrol": 0.58,
            "freight_petrol": 0.04,
            "federal_excise_petrol": 0.0486,
            "dealer_margin_petrol": 0.10,
            "state_tax_petrol": 0.0914,
            "state_tax_pct": 10.6,
            "cities": [
                "florida", "fl", "miami", "orlando", "tampa", "jacksonville",
                "st petersburg", "fort lauderdale", "tallahassee", "cape coral"
            ],
            "tax_statute_note": "State tax pegged at $0.3525/gal including state fuel tax, state comprehensive enhancement tax, and local county option fuel tax."
        },
        "United Kingdom": {
            "country": "United Kingdom",
            "country_iso3": "GBR",
            "type": "Sovereign Nation",
            "capital": "London",
            "flag": "🇬🇧",
            "currency": "GBP",
            "currency_symbol": "£",
            "statutory_authority": "HM Revenue & Customs (HMRC)",
            "petrol_rsp": 1.44,      # £1.44 / Litre (~$1.87 USD)
            "diesel_rsp": 1.52,      # £1.52 / Litre (~$1.98 USD)
            "base_petrol": 0.53,     # Refinery gate
            "freight_petrol": 0.03,
            "federal_excise_petrol": 0.5295, # Fuel Duty 52.95p / L
            "dealer_margin_petrol": 0.14,
            "state_tax_petrol": 0.24,        # 20% VAT on total price (52.95p duty is taxed again by VAT!)
            "state_tax_pct": 16.7,
            "cities": [
                "united kingdom", "uk", "great britain", "britain", "england", "scotland",
                "wales", "northern ireland", "london", "manchester", "birmingham", "edinburgh",
                "glasgow", "liverpool", "bristol", "leeds", "newcastle", "belfast", "cardiff"
            ],
            "tax_statute_note": "Double taxation structure: specific fuel duty of 52.95p/L levied first, then standard 20% VAT applied on top of the fuel duty and base price. Over 53% of pump price goes to the UK Exchequer."
        },
        "Germany": {
            "country": "Germany",
            "country_iso3": "DEU",
            "type": "Sovereign Nation",
            "capital": "Berlin",
            "flag": "🇩🇪",
            "currency": "EUR",
            "currency_symbol": "€",
            "statutory_authority": "Federal Ministry of Finance (Bundesfinanzministerium)",
            "petrol_rsp": 1.78,      # €1.78 / Litre (~$1.92 USD)
            "diesel_rsp": 1.68,      # €1.68 / Litre (~$1.81 USD)
            "base_petrol": 0.62,
            "freight_petrol": 0.03,
            "federal_excise_petrol": 0.6545, # Energiesteuer 65.45 ct/L
            "dealer_margin_petrol": 0.09,
            "state_tax_petrol": 0.3855,      # CO2 levy €0.10/L + 19% MwSt (€0.285/L)
            "state_tax_pct": 21.7,
            "cities": [
                "germany", "deutschland", "berlin", "munich", "münchen", "frankfurt",
                "hamburg", "bavaria", "bayern", "cologne", "köln", "stuttgart", "düsseldorf",
                "dortmund", "essen", "leipzig", "bremen", "dresden", "hannover", "nuremberg"
            ],
            "tax_statute_note": "Among world's highest tax burdens: Energiesteuer (65.45 ct/L on petrol, 47.04 ct/L on diesel) + National BEHG CO2 price + 19% MwSt VAT. Sovereign levies comprise over 58% of retail pump prices."
        },
        "France": {
            "country": "France",
            "country_iso3": "FRA",
            "type": "Sovereign Nation",
            "capital": "Paris",
            "flag": "🇫🇷",
            "currency": "EUR",
            "currency_symbol": "€",
            "statutory_authority": "Direction Générale des Douanes et Droits Indirects (DGDDI)",
            "petrol_rsp": 1.82,      # €1.82 / Litre (~$1.97 USD)
            "diesel_rsp": 1.72,      # €1.72 / Litre (~$1.86 USD)
            "base_petrol": 0.64,
            "freight_petrol": 0.03,
            "federal_excise_petrol": 0.6829, # TICPE excise duty
            "dealer_margin_petrol": 0.16,
            "state_tax_petrol": 0.3041,      # 20% TVA (VAT)
            "state_tax_pct": 16.7,
            "cities": [
                "france", "paris", "marseille", "lyon", "toulouse", "nice", "nantes",
                "strasbourg", "montpellier", "bordeaux", "lille", "rennes", "reims"
            ],
            "tax_statute_note": "TICPE (Internal Tax on Petroleum Products) of €0.6829/L plus 20% TVA. Government maintains green transition tax wedge of ~54% on fossil fuels."
        },
        "Canada (Ontario)": {
            "country": "Canada",
            "country_iso3": "CAN",
            "type": "Canadian Province",
            "capital": "Toronto",
            "flag": "🇨🇦",
            "currency": "CAD",
            "currency_symbol": "C$",
            "statutory_authority": "Ontario Ministry of Finance / CRA",
            "petrol_rsp": 1.58,      # CAD $1.58 / Litre (~$1.15 USD)
            "diesel_rsp": 1.66,      # CAD $1.66 / Litre (~$1.21 USD)
            "base_petrol": 0.85,
            "freight_petrol": 0.05,
            "federal_excise_petrol": 0.10,   # Federal excise (10¢/L) + Carbon charge (17.6¢/L) = 27.6¢
            "dealer_margin_petrol": 0.13,
            "state_tax_petrol": 0.274,       # Ontario Gas Tax (9.0¢/L temporary cut) + 13% HST (18.4¢)
            "state_tax_pct": 17.3,
            "cities": [
                "canada", "ontario", "on", "toronto", "ottawa", "mississauga", "brampton",
                "hamilton", "london ontario", "markham", "vaughan", "kitchener", "windsor"
            ],
            "tax_statute_note": "Combines Federal Excise (10¢/L), Federal Carbon Backstop Levy (17.61¢/L), Ontario Provincial Fuel Tax (9¢/L), and 13% Harmonized Sales Tax (HST)."
        },
        "Canada (British Columbia)": {
            "country": "Canada",
            "country_iso3": "CAN",
            "type": "Canadian Province",
            "capital": "Victoria",
            "flag": "🇨🇦",
            "currency": "CAD",
            "currency_symbol": "C$",
            "statutory_authority": "BC Ministry of Finance",
            "petrol_rsp": 1.84,      # CAD $1.84 / Litre (~$1.34 USD)
            "diesel_rsp": 1.89,      # CAD $1.89 / Litre (~$1.38 USD)
            "base_petrol": 0.95,
            "freight_petrol": 0.06,
            "federal_excise_petrol": 0.10,
            "dealer_margin_petrol": 0.14,
            "state_tax_petrol": 0.59,        # BC Motor Fuel Tax (14.5¢) + BC Carbon Tax (17.6¢) + TransLink transit levy (18.5¢) + 5% GST
            "state_tax_pct": 32.1,
            "cities": [
                "british columbia", "bc", "vancouver", "victoria", "surrey", "burnaby",
                "richmond", "abbotsford", "coquitlam", "kelowna", "kamloops", "nanaimo"
            ],
            "tax_statute_note": "Highest fuel tax jurisdiction in North America: combines BC Motor Fuel Tax, dedicated TransLink municipal transit tax, BC provincial carbon tax, and 5% GST."
        },
        "Japan": {
            "country": "Japan",
            "country_iso3": "JPN",
            "type": "Sovereign Nation",
            "capital": "Tokyo",
            "flag": "🇯🇵",
            "currency": "JPY",
            "currency_symbol": "¥",
            "statutory_authority": "National Tax Agency (国税庁)",
            "petrol_rsp": 175.0,     # ¥175 / Litre (~$1.17 USD)
            "diesel_rsp": 154.0,     # ¥154 / Litre (~$1.03 USD)
            "base_petrol": 92.0,
            "freight_petrol": 4.0,
            "federal_excise_petrol": 53.8,   # Gasoline Tax (Volatile Oil Tax ¥48.6 + Local Road Tax ¥5.2)
            "dealer_margin_petrol": 9.3,
            "state_tax_petrol": 15.9,        # Petroleum & Coal Tax (¥2.8) + 10% Consumption Tax (¥15.9)
            "state_tax_pct": 9.1,
            "cities": [
                "japan", "nippon", "tokyo", "osaka", "yokohama", "nagoya", "kyoto",
                "sapporo", "kobe", "fukuoka", "kawasaki", "saitama", "hiroshima", "sendai"
            ],
            "tax_statute_note": "Regulated under Volatile Oil Tax Act (¥53.8/L) with active government wholesale subsidies cushioning retail price ceilings at ¥175/L."
        },
        "Australia": {
            "country": "Australia",
            "country_iso3": "AUS",
            "type": "Sovereign Nation",
            "capital": "Canberra",
            "flag": "🇦🇺",
            "currency": "AUD",
            "currency_symbol": "A$",
            "statutory_authority": "Australian Taxation Office (ATO)",
            "petrol_rsp": 1.92,      # AUD $1.92 / Litre (~$1.25 USD)
            "diesel_rsp": 1.96,      # AUD $1.96 / Litre (~$1.27 USD)
            "base_petrol": 1.05,
            "freight_petrol": 0.05,
            "federal_excise_petrol": 0.496,  # Bi-annually CPI indexed federal fuel excise (49.6¢/L)
            "dealer_margin_petrol": 0.15,
            "state_tax_petrol": 0.174,       # 10% Goods and Services Tax (GST)
            "state_tax_pct": 9.1,
            "cities": [
                "australia", "sydney", "melbourne", "brisbane", "perth", "adelaide",
                "gold coast", "canberra", "newcastle aus", "wollongong", "hobart", "darwin"
            ],
            "tax_statute_note": "Indexed to CPI twice a year (February and August): 49.6 cents/L federal fuel excise plus 10% GST on the total pump invoice."
        },
        "United Arab Emirates": {
            "country": "United Arab Emirates",
            "country_iso3": "ARE",
            "type": "Sovereign Nation",
            "capital": "Abu Dhabi",
            "flag": "🇦🇪",
            "currency": "AED",
            "currency_symbol": "AED",
            "statutory_authority": "UAE Ministry of Energy & Infrastructure / FTA",
            "petrol_rsp": 2.85,      # AED 2.85 / Litre (~$0.78 USD)
            "diesel_rsp": 2.92,      # AED 2.92 / Litre (~$0.79 USD)
            "base_petrol": 2.45,
            "freight_petrol": 0.08,
            "federal_excise_petrol": 0.00,   # Zero fuel excise duty
            "dealer_margin_petrol": 0.18,
            "state_tax_petrol": 0.14,        # 5% Federal VAT
            "state_tax_pct": 4.9,
            "cities": [
                "united arab emirates", "uae", "dubai", "abu dhabi", "sharjah",
                "al ain", "ajman", "ras al khaimah", "fujairah", "umm al quwain"
            ],
            "tax_statute_note": "Fully deregulated retail pricing pegged to international refined product benchmarks without fuel excise; only a low 5% standard VAT is charged."
        },
        "Saudi Arabia": {
            "country": "Saudi Arabia",
            "country_iso3": "SAU",
            "type": "Sovereign Nation",
            "capital": "Riyadh",
            "flag": "🇸🇦",
            "currency": "SAR",
            "currency_symbol": "SAR",
            "statutory_authority": "Zakat, Tax and Customs Authority (ZATCA)",
            "petrol_rsp": 2.18,      # SAR 2.18 / Litre (~$0.58 USD)
            "diesel_rsp": 1.15,      # SAR 1.15 / Litre (~$0.31 USD)
            "base_petrol": 1.75,
            "freight_petrol": 0.04,
            "federal_excise_petrol": 0.00,   # Domestic price caps (Royal Decree)
            "dealer_margin_petrol": 0.11,
            "state_tax_petrol": 0.28,        # 15% VAT
            "state_tax_pct": 12.8,
            "cities": [
                "saudi", "saudi arabia", "kingdom of saudi arabia", "ksa", "saudis", "riyadh", "jeddah", "mecca", "medina",
                "dammam", "khobar", "dhahran", "jubail", "yanbu", "tabuk", "taif"
            ],
            "tax_statute_note": "Saudi Arabia levies a standard 15% Value Added Tax (VAT) administered by ZATCA (Zakat, Tax and Customs Authority) across commercial transactions and retail motor fuel. Crucially, there is 0% personal income tax on salaries and individual earnings for citizens and resident workers. Domestic motor fuel prices are subsidized and capped by Royal Decree (Gasoline 91 capped at SAR 2.18/L, Diesel at SAR 1.15/L)."
        },
        "Brazil": {
            "country": "Brazil",
            "country_iso3": "BRA",
            "type": "Sovereign Nation",
            "capital": "Brasília",
            "flag": "🇧🇷",
            "currency": "BRL",
            "currency_symbol": "R$",
            "statutory_authority": "Receita Federal do Brasil / CONFAZ",
            "petrol_rsp": 5.95,      # R$ 5.95 / Litre (~$1.07 USD)
            "diesel_rsp": 5.82,      # R$ 5.82 / Litre (~$1.05 USD)
            "base_petrol": 3.40,     # Petrobras refinery gate (A-gasoline) + 27% anhydrous ethanol blend
            "freight_petrol": 0.15,
            "federal_excise_petrol": 0.68,   # PIS/COFINS + CIDE
            "dealer_margin_petrol": 0.35,
            "state_tax_petrol": 1.37,        # Fixed unified state ad-rem ICMS (R$ 1.37/L)
            "state_tax_pct": 23.0,
            "cities": [
                "brazil", "brasil", "sao paulo", "são paulo", "rio de janeiro",
                "brasilia", "brasília", "salvador", "fortaleza", "belo horizonte",
                "manaus", "curitiba", "recife", "porto alegre"
            ],
            "tax_statute_note": "Under Complementary Law 192/2022, state ICMS is applied as a single national ad-rem rate of R$ 1.37/L across all 27 federation states, alongside federal PIS/COFINS."
        },
        "Italy": {
            "country": "Italy",
            "country_iso3": "ITA",
            "type": "Sovereign Nation",
            "capital": "Rome",
            "flag": "🇮🇹",
            "currency": "EUR",
            "currency_symbol": "€",
            "statutory_authority": "Agenzia delle Dogane e dei Monopoli (ADM)",
            "petrol_rsp": 1.84,      # €1.84 / Litre (~$1.99 USD)
            "diesel_rsp": 1.74,      # €1.74 / Litre (~$1.88 USD)
            "base_petrol": 0.65,
            "freight_petrol": 0.03,
            "federal_excise_petrol": 0.728,  # Specific excise duty (accisa)
            "dealer_margin_petrol": 0.10,
            "state_tax_petrol": 0.332,       # 22% IVA (VAT)
            "state_tax_pct": 18.0,
            "cities": [
                "italy", "italia", "rome", "roma", "milan", "milano", "naples",
                "napoli", "turin", "torino", "palermo", "genoa", "bologna", "florence", "venice"
            ],
            "tax_statute_note": "One of Europe's heaviest excise burdens with historic accrued accise (€0.728/L) plus standard 22% IVA VAT."
        }
    }

    @classmethod
    def resolve_query(cls, query: str) -> Optional[Dict[str, Any]]:
        """
        Sub-millisecond fuzzy and alias resolver for any Indian state, Indian city,
        global country, province, or international metro.
        Returns a rich structured telemetry packet with exact breakdown and state tax calculations.
        """
        import re
        q = query.strip().lower()

        # Guard: Check if query clearly expresses a non-tax operational intent (e.g. exports, imports, forecasts, production)
        non_tax_intent_words = [
            "export", "where export", "who buys", "importer", "import", "where import",
            "destination", "trade", "flow", "corridor", "route", "tanker", "ship",
            "chokepoint", "strait", "why", "how much oil", "how much crude",
            "produce", "producer", "production", "refining capacity", "refinery", "forecast", "future",
            "month", "trend", "predict", "hike", "cut", "or not", "who contributes", "who is the more contributor"
        ]
        explicit_tax_keywords = [
            "tax", "vat", "excise", "duty", "breakdown", "cess", "dealer margin",
            "rsp", "base price", "pump price", "retail price", "rate", "cost breakdown", "tax breakdown"
        ]
        has_non_tax_intent = any(w in q for w in non_tax_intent_words)
        has_explicit_tax_keyword = any(w in q for w in explicit_tax_keywords)

        if has_non_tax_intent and not has_explicit_tax_keyword:
            # Operational energy query (trade/forecast/production), not a tax breakdown
            return None

        # Step 1: Exact matches against India State names
        for state_name, data in cls.INDIA_TAX_DATA.items():
            state_lower = state_name.lower()
            if q == state_lower:
                return cls._build_india_response(state_name, data, matched_city=None, query=query)

        # Step 2: Exact matches against Global Jurisdictions / Countries
        for region_name, data in cls.GLOBAL_TAX_DATA.items():
            region_lower = region_name.lower()
            country_lower = data.get("country", "").lower()
            if q == region_lower or q == country_lower:
                return cls._build_global_response(region_name, data, matched_city=None, query=query)

        # Step 3: Check India states & cities via word boundaries
        for state_name, data in cls.INDIA_TAX_DATA.items():
            state_lower = state_name.lower()
            if re.search(r'\b' + re.escape(state_lower) + r'\b', q):
                return cls._build_india_response(state_name, data, matched_city=None, query=query)
            for city in data["cities"]:
                if re.search(r'\b' + re.escape(city) + r'\b', q):
                    matched_display = city.title()
                    if city in ["noida", "greater noida"]:
                        matched_display = city.upper()
                    elif city in ["prayagraj", "allahabad"]:
                        matched_display = "Prayagraj (Allahabad)"
                    elif city in ["bengaluru", "bangalore"]:
                        matched_display = "Bengaluru"
                    return cls._build_india_response(state_name, data, matched_city=matched_display, query=query)

        # Step 4: Check global jurisdictions, countries & cities via word boundaries
        for region_name, data in cls.GLOBAL_TAX_DATA.items():
            region_lower = region_name.lower()
            country_lower = data.get("country", "").lower()
            if country_lower and re.search(r'\b' + re.escape(country_lower) + r'\b', q):
                return cls._build_global_response(region_name, data, matched_city=None, query=query)
            if re.search(r'\b' + re.escape(region_lower) + r'\b', q):
                return cls._build_global_response(region_name, data, matched_city=None, query=query)
            for city in data["cities"]:
                if re.search(r'\b' + re.escape(city) + r'\b', q):
                    matched_display = city.title()
                    if city in ["la", "sf", "nyc", "uk", "usa", "uae", "ksa", "bc", "ca", "tx", "ny", "fl"]:
                        matched_display = city.upper()
                    return cls._build_global_response(region_name, data, matched_city=matched_display, query=query)

        # Step 5: Check common state aliases (e.g. "UP" for Uttar Pradesh)
        aliases = {
            "up": "Uttar Pradesh",
            "uttar pradesh": "Uttar Pradesh",
            "mp": "Madhya Pradesh",
            "ap": "Andhra Pradesh",
            "hp": "Himachal Pradesh",
            "tn": "Tamil Nadu",
            "wb": "West Bengal",
            "delhi": "Delhi (NCT)",
            "uk": "Uttarakhand",
            "mh": "Maharashtra"
        }
        for alias, state_target in aliases.items():
            if re.search(r'\b' + re.escape(alias) + r'\b', q) and state_target in cls.INDIA_TAX_DATA:
                return cls._build_india_response(state_target, cls.INDIA_TAX_DATA[state_target], matched_city=None, query=query)

        # Step 6: Check global country and sovereign aliases (e.g. "Saudi" for Saudi Arabia)
        country_aliases = {
            "saudi": "Saudi Arabia",
            "ksa": "Saudi Arabia",
            "kingdom of saudi arabia": "Saudi Arabia",
            "saudis": "Saudi Arabia",
            "uae": "United Arab Emirates",
            "dubai": "United Arab Emirates",
            "emirates": "United Arab Emirates",
            "usa": "United States (National Average)",
            "america": "United States (National Average)",
            "us": "United States (National Average)",
            "uk": "United Kingdom",
            "britain": "United Kingdom",
            "germany": "Germany",
            "deutschland": "Germany",
            "brazil": "Brazil",
            "canada": "Canada (Ontario)",
            "japan": "Japan",
            "australia": "Australia (New South Wales)"
        }
        for alias, region_target in country_aliases.items():
            if re.search(r'\b' + re.escape(alias) + r'\b', q) and region_target in cls.GLOBAL_TAX_DATA:
                return cls._build_global_response(region_target, cls.GLOBAL_TAX_DATA[region_target], matched_city=None, query=query)

        return None

    @classmethod
    def resolve(cls, query: str) -> Optional[Dict[str, Any]]:
        """Public alias for resolve_query."""
        return cls.resolve_query(query)

    @classmethod
    def _build_india_response(cls, state_name: str, data: Dict[str, Any], matched_city: Optional[str], query: str) -> Dict[str, Any]:
        """Builds a comprehensive tax decomposition response for an Indian jurisdiction."""
        is_city = matched_city is not None
        entity_name = f"{matched_city}, {state_name}" if is_city else state_name
        
        petrol_rsp = data["petrol_rsp"]
        diesel_rsp = data["diesel_rsp"]
        base_petrol = data["base_petrol"]
        freight_petrol = data["freight_petrol"]
        central_excise = data["central_excise_petrol"]
        dealer_margin = data["dealer_margin_petrol"]

        # Exact State VAT amount in ₹/L is the balancing state tax wedge:
        # RSP = Base + Freight + Central Excise + Dealer Commission + State VAT
        state_vat_petrol = round(petrol_rsp - (base_petrol + freight_petrol + central_excise + dealer_margin), 2)
        state_vat_diesel = round(diesel_rsp - (data["base_diesel"] + data["freight_diesel"] + data["central_excise_diesel"] + data["dealer_margin_diesel"]), 2)

        total_tax_petrol = round(central_excise + state_vat_petrol, 2)
        state_tax_pct_pump = round((state_vat_petrol / petrol_rsp) * 100, 1)
        state_tax_pct_base = round((state_vat_petrol / base_petrol) * 100, 1)
        total_tax_pct_pump = round((total_tax_petrol / petrol_rsp) * 100, 1)

        # USD conversions
        petrol_usd = round(petrol_rsp / cls.USD_INR_RATE, 2)
        diesel_usd = round(diesel_rsp / cls.USD_INR_RATE, 2)

        waterfall_steps = [
            {"component": "Base Refinery Price (RTP)", "amount_inr": base_petrol, "pct_pump": round((base_petrol / petrol_rsp) * 100, 1), "levied_by": "Refiners (IOCL/BPCL/HPCL)"},
            {"component": "Inland Freight & Depot", "amount_inr": freight_petrol, "pct_pump": round((freight_petrol / petrol_rsp) * 100, 1), "levied_by": "Distribution Logistics"},
            {"component": "Central Excise Duty", "amount_inr": central_excise, "pct_pump": round((central_excise / petrol_rsp) * 100, 1), "levied_by": "Govt of India (Central Exchequer)"},
            {"component": "Dealer Commission", "amount_inr": dealer_margin, "pct_pump": round((dealer_margin / petrol_rsp) * 100, 1), "levied_by": "Petrol Pump Operator"},
            {"component": f"State VAT ({data.get('vat_petrol_pct', 19.4)}%)", "amount_inr": state_vat_petrol, "pct_pump": state_tax_pct_pump, "levied_by": f"Govt of {state_name}"},
            {"component": "Final Retail Pump Price (RSP)", "amount_inr": petrol_rsp, "pct_pump": 100.0, "levied_by": "Consumer Retail Price"}
        ]

        return {
            "query": query,
            "matched_type": "India Jurisdiction",
            "jurisdiction_name": entity_name,
            "state_name": state_name,
            "matched_city": matched_city,
            "country": "India",
            "country_iso3": "IND",
            "flag": "🇮🇳",
            "currency": "INR",
            "currency_symbol": "₹",
            "petrol_price": petrol_rsp,
            "diesel_price": diesel_rsp,
            "petrol_price_usd": petrol_usd,
            "diesel_price_usd": diesel_usd,
            "base_refinery_price": base_petrol,
            "central_excise": central_excise,
            "dealer_commission": dealer_margin,
            "state_tax_amount": state_vat_petrol,
            "state_tax_rate_nominal_pct": data.get("vat_petrol_pct", 19.4),
            "state_tax_share_pump_pct": state_tax_pct_pump,
            "state_tax_added_to_base_pct": state_tax_pct_base,
            "total_government_tax_amount": total_tax_petrol,
            "total_tax_share_pump_pct": total_tax_pct_pump,
            "diesel_state_tax_amount": state_vat_diesel,
            "statutory_authority": data["statutory_authority"],
            "statutory_note": data["tax_statute_note"],
            "waterfall_steps": waterfall_steps,
            "deep_link_url": "#ch-05",
            "deep_link_label": "View India Fuel Pricing Architecture"
        }

    @classmethod
    def _build_global_response(cls, region_name: str, data: Dict[str, Any], matched_city: Optional[str], query: str) -> Dict[str, Any]:
        """Builds a comprehensive tax decomposition response for a global jurisdiction."""
        country_name = data.get("country", region_name)
        country_aliases = [region_name.lower(), country_name.lower(), "saudi", "ksa", "saudis", "kingdom of saudi arabia", "uae", "emirates", "usa", "us", "america", "uk", "britain"]
        is_city = matched_city is not None and matched_city.lower() not in country_aliases
        entity_name = f"{matched_city}, {region_name}" if is_city else region_name

        curr = data["currency"]
        sym = data["currency_symbol"]
        petrol_rsp = data["petrol_rsp"]
        diesel_rsp = data["diesel_rsp"]
        base_petrol = data["base_petrol"]
        freight_petrol = data["freight_petrol"]
        federal_excise = data["federal_excise_petrol"]
        dealer_margin = data["dealer_margin_petrol"]
        state_tax = data["state_tax_petrol"]

        total_gov_tax = round(federal_excise + state_tax, 4)
        state_tax_pct_pump = round((state_tax / petrol_rsp) * 100, 1)
        state_tax_pct_base = round((state_tax / base_petrol) * 100, 1)
        total_tax_pct_pump = round((total_gov_tax / petrol_rsp) * 100, 1)

        # Convert to USD per litre
        rate_map = {
            "USD": 1.0,
            "EUR": cls.EUR_USD_RATE,
            "GBP": cls.GBP_USD_RATE,
            "CAD": cls.CAD_USD_RATE,
            "JPY": cls.JPY_USD_RATE,
            "AUD": cls.AUD_USD_RATE,
            "AED": cls.AED_USD_RATE,
            "SAR": cls.SAR_USD_RATE,
            "BRL": cls.BRL_USD_RATE
        }
        fx_to_usd = rate_map.get(curr, 1.0)
        petrol_usd = round(petrol_rsp * fx_to_usd, 2)
        diesel_usd = round(diesel_rsp * fx_to_usd, 2)

        # Convert to INR per litre for easy universal comparison
        petrol_inr = round(petrol_usd * cls.USD_INR_RATE, 2)
        diesel_inr = round(diesel_usd * cls.USD_INR_RATE, 2)

        waterfall_steps = [
            {"component": "Base Product & Refining", "amount_local": base_petrol, "pct_pump": round((base_petrol / petrol_rsp) * 100, 1), "levied_by": "Refinery Gate"},
            {"component": "Freight & Distribution", "amount_local": freight_petrol, "pct_pump": round((freight_petrol / petrol_rsp) * 100, 1), "levied_by": "Logistics & Terminal"},
            {"component": "Federal / Sovereign Excise", "amount_local": federal_excise, "pct_pump": round((federal_excise / petrol_rsp) * 100, 1), "levied_by": "National Government"},
            {"component": "Retail Station Margin", "amount_local": dealer_margin, "pct_pump": round((dealer_margin / petrol_rsp) * 100, 1), "levied_by": "Station Operator"},
            {"component": "State/Provincial Tax & VAT", "amount_local": state_tax, "pct_pump": state_tax_pct_pump, "levied_by": data["statutory_authority"]},
            {"component": "Final Retail Pump Price", "amount_local": petrol_rsp, "pct_pump": 100.0, "levied_by": "Consumer Pump Price"}
        ]

        return {
            "query": query,
            "matched_type": "Global Jurisdiction",
            "jurisdiction_name": entity_name,
            "state_name": region_name,
            "matched_city": matched_city,
            "country": data["country"],
            "country_iso3": data["country_iso3"],
            "flag": data["flag"],
            "currency": curr,
            "currency_symbol": sym,
            "petrol_price": petrol_rsp,
            "diesel_price": diesel_rsp,
            "petrol_price_usd": petrol_usd,
            "diesel_price_usd": diesel_usd,
            "petrol_price_inr": petrol_inr,
            "diesel_price_inr": diesel_inr,
            "base_refinery_price": base_petrol,
            "central_excise": federal_excise,
            "dealer_commission": dealer_margin,
            "state_tax_amount": state_tax,
            "state_tax_rate_nominal_pct": data.get("state_tax_pct", state_tax_pct_pump),
            "state_tax_share_pump_pct": state_tax_pct_pump,
            "state_tax_added_to_base_pct": state_tax_pct_base,
            "total_government_tax_amount": total_gov_tax,
            "total_tax_share_pump_pct": total_tax_pct_pump,
            "statutory_authority": data["statutory_authority"],
            "statutory_note": data["tax_statute_note"],
            "waterfall_steps": waterfall_steps,
            "deep_link_url": "#ch-04",
            "deep_link_label": "Explore Global Retail Price Radar"
        }

    @classmethod
    def get_all_searchable_jurisdictions(cls) -> List[Dict[str, Any]]:
        """Returns indexed search dictionary for all Indian states, cities, and global territories."""
        items = []
        for state_name, data in cls.INDIA_TAX_DATA.items():
            items.append({
                "name": f"{state_name} (India)",
                "type": "Indian State",
                "badge_bg": "rgba(16, 185, 129, 0.25)",
                "category": f"Petrol ₹{data['petrol_rsp']:.2f}/L • Diesel ₹{data['diesel_rsp']:.2f}/L • State VAT {data.get('vat_petrol_pct', 19.4)}%",
                "target": "#ch-05",
                "label": f"Inspect {state_name} Tax"
            })
            for city in data["cities"][:4]:
                c_display = city.title()
                if city in ["noida", "greater noida"]:
                    c_display = city.upper()
                elif city in ["prayagraj", "allahabad"]:
                    c_display = "Prayagraj"
                items.append({
                    "name": f"{c_display} ({state_name})",
                    "type": "India City",
                    "badge_bg": "rgba(245, 185, 66, 0.25)",
                    "category": f"Petrol ₹{data['petrol_rsp']:.2f}/L • Diesel ₹{data['diesel_rsp']:.2f}/L • State VAT {data.get('vat_petrol_pct', 19.4)}%",
                    "target": "#ch-05",
                    "label": f"Inspect {c_display} Tax"
                })

        for region_name, data in cls.GLOBAL_TAX_DATA.items():
            items.append({
                "name": f"{region_name} ({data['country']})",
                "type": "Global Jurisdiction",
                "badge_bg": "rgba(59, 130, 246, 0.25)",
                "category": f"Petrol {data['currency_symbol']}{data['petrol_rsp']:.2f}/L (${data.get('petrol_rsp', 1.0):.2f}/L) • Sovereign Tax {data.get('state_tax_pct', 15.0)}%",
                "target": "#ch-04",
                "label": f"Inspect {region_name} Tax"
            })
        return items

    @classmethod
    def render_tax_intelligence_card(cls, result: Dict[str, Any]):
        """Renders an interactive glassmorphic fuel pricing and sovereign tax breakdown card."""
        import streamlit as st
        import plotly.graph_objects as go
        from src.ui_components import render_html, apply_clean_layout, COLOR_AMBER, COLOR_INK, render_instrument_card

        flag = result.get("flag", "🌐")
        j_name = result.get("jurisdiction_name", "Global Jurisdiction")
        j_type = result.get("matched_type", "Fuel & Tax Intelligence")
        authority = result.get("statutory_authority", "Ministry of Petroleum / State Revenue Dept")
        sym = result.get("currency_symbol", "₹")
        petrol_price = result.get("petrol_price", 0.0)
        diesel_price = result.get("diesel_price", 0.0)
        petrol_usd = result.get("petrol_price_usd", 0.0)
        diesel_usd = result.get("diesel_price_usd", 0.0)
        state_tax_amt = result.get("state_tax_amount", 0.0)
        state_tax_pct_pump = result.get("state_tax_share_pump_pct", 0.0)
        state_tax_pct_base = result.get("state_tax_added_to_base_pct", 0.0)
        total_gov_tax = result.get("total_government_tax_amount", 0.0)
        total_tax_pct_pump = result.get("total_tax_share_pump_pct", 0.0)
        base_price = result.get("base_refinery_price", 0.0)
        central_excise = result.get("central_excise", 0.0)
        dealer_margin = result.get("dealer_commission", 0.0)
        statutory_note = result.get("statutory_note", "")

        # Top Header Banner
        render_html(f"""
        <div style="background: rgba(14, 21, 38, 0.95); backdrop-filter: blur(16px); border: 1px solid rgba(245, 185, 66, 0.45); box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6), 0 0 24px rgba(245, 185, 66, 0.15); border-radius: 12px; padding: 20px 24px; margin-top: 12px; margin-bottom: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 6px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.8rem;">{flag}</span>
                    <div>
                        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #F9FAFB; letter-spacing: -0.02em;">
                            {j_name.upper()}
                        </div>
                        <div style="font-size: 0.78rem; color: #94A3B8;">
                            Sovereign Energy Taxation & Pump Price Decomposition • Authority: <b style="color: #F5B942;">{authority}</b>
                        </div>
                    </div>
                </div>
                <div style="display: flex; gap: 8px; align-items: center;">
                    <span style="background: rgba(245, 185, 66, 0.2); border: 1px solid rgba(245, 185, 66, 0.4); padding: 4px 10px; border-radius: 999px; font-size: 0.7rem; font-weight: 800; color: #F5B942;">
                        {j_type.upper()}
                    </span>
                    <span style="background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.4); padding: 4px 10px; border-radius: 999px; font-size: 0.7rem; font-weight: 800; color: #10B981;">
                        VERIFIED BENCHMARK
                    </span>
                </div>
            </div>
        </div>
        """)

        # 4 Core KPI Cards
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            render_instrument_card(
                label="Petrol Retail Rate",
                value=f"{sym}{petrol_price:.2f} / L",
                accent="amber",
                subtext=f"${petrol_usd:.2f}/L USD Equivalent",
                code_badge="RSP"
            )
        with k2:
            render_instrument_card(
                label="Diesel Retail Rate",
                value=f"{sym}{diesel_price:.2f} / L",
                accent="teal",
                subtext=f"${diesel_usd:.2f}/L USD Equivalent",
                code_badge="HSD"
            )
        with k3:
            render_instrument_card(
                label="State Government Tax",
                value=f"{sym}{state_tax_amt:.2f} / L",
                accent="red",
                subtext=f"{state_tax_pct_pump}% of Retail Pump Price",
                code_badge="STATE VAT"
            )
        with k4:
            render_instrument_card(
                label="State Tax on Base Price",
                value=f"+{state_tax_pct_base}%",
                accent="copper",
                subtext=f"Added over {sym}{base_price:.2f}/L base",
                code_badge="TAX BITE"
            )

        st.write("")

        # Visual Price Waterfall Chart + Statutory Decomposition
        wf_col1, wf_col2 = st.columns([7, 5])

        with wf_col1:
            st.markdown(f"##### 📊 Price Build-Up Anatomy: From Base Refinery to Pump ({sym}{petrol_price:.2f}/L)")
            
            # Extract waterfall data
            steps = result.get("waterfall_steps", [])
            if steps:
                x_labels = [s["component"] for s in steps[:-1]] + ["Final Pump Price"]
                y_amounts = [s.get("amount_inr", s.get("amount_local", 0.0)) for s in steps[:-1]] + [0]
                text_labels = [f"{sym}{s.get('amount_inr', s.get('amount_local', 0.0)):.2f}" for s in steps[:-1]] + [f"{sym}{petrol_price:.2f}"]

                fig_wf = go.Figure(go.Waterfall(
                    name="Cost Build-Up",
                    orientation="v",
                    measure=["relative"] * len(steps[:-1]) + ["total"],
                    x=x_labels,
                    y=y_amounts,
                    text=text_labels,
                    textposition="outside",
                    connector={"line": {"color": "rgba(255, 255, 255, 0.25)"}},
                    decreasing={"marker": {"color": "#F43F5E"}},
                    increasing={"marker": {"color": COLOR_AMBER}},
                    totals={"marker": {"color": "#60A5FA"}}
                ))
                apply_clean_layout(
                    fig_wf,
                    height=340,
                    yaxis_title=f"Cost ({sym} / Litre)",
                    margin_t=30,
                    margin_b=60
                )
                st.plotly_chart(fig_wf, width="stretch", theme=None)

        with wf_col2:
            st.markdown("##### 🏛️ State Tax Breakdown & Sovereign Formula")
            render_html(f"""
            <div style="background: rgba(14, 21, 38, 0.85); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 8px; padding: 16px; font-size: 0.8rem; line-height: 1.6; color: #CBD5E1;">
                <div style="font-weight: 800; color: #F5B942; margin-bottom: 8px; font-size: 0.85rem; display: flex; align-items: center; gap: 6px;">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                    HOW MUCH TAX THE STATE TAKES FROM THE ORIGINAL PRICE:
                </div>
                <div style="margin-bottom: 10px;">
                    • <b>Base Refinery Transfer Price:</b> <span style="color: #60A5FA;">{sym}{base_price:.2f}/L</span><br/>
                    • <b>Central Government Excise:</b> <span style="color: #94A3B8;">{sym}{central_excise:.2f}/L</span><br/>
                    • <b>State Government Tax / VAT:</b> <span style="color: #F43F5E; font-weight: 800;">{sym}{state_tax_amt:.2f}/L</span><br/>
                    • <b>State Tax Bite Added over Base:</b> <span style="color: #F5B942; font-weight: 800;">+{state_tax_pct_base}%</span> added directly on original base price.<br/>
                    • <b>State Share of Pump Price:</b> <span style="color: #F9FAFB; font-weight: 700;">{state_tax_pct_pump}%</span> of every litre goes to state treasury.
                </div>
                <div style="background: rgba(244, 63, 94, 0.12); border-left: 3px solid #F43F5E; padding: 8px 12px; border-radius: 4px; margin-bottom: 10px; font-size: 0.76rem; color: #FDA4AF;">
                    <b>Combined Government Tax Wedge:</b> {sym}{total_gov_tax:.2f} / Litre (<b>{total_tax_pct_pump}%</b> of consumer pump price is government taxation).
                </div>
                <div style="font-size: 0.72rem; color: #94A3B8; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 8px;">
                    <b>Statute & Circular:</b> {statutory_note}
                </div>
            </div>
            """)
            st.markdown(
                f"<a href='{result.get('deep_link_url', '#ch-05')}' style='display: inline-flex; align-items: center; gap: 6px; background: #EAB308; color: #070A12; border: 1px solid #CA8A04; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.25); font-weight: 800; font-size: 0.78rem; padding: 8px 16px; border-radius: 6px; text-decoration: none; margin-top: 8px;'>{result.get('deep_link_label', 'Explore Full Deck')} →</a>",
                unsafe_allow_html=True
            )

