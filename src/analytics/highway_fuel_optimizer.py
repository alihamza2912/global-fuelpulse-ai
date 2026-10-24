"""
Highway Fuel Trip & Cross-Border Arbitrage Optimizer Engine.
Covers:
- All 28 States & 8 Union Territories of India (PPAC/MoPNG VAT disparity)
- Saudi Arabia (Aramco provinces & expressways)
- Dubai & UAE Emirates (Deregulated Fuel Price Committee)
- GCC Middle East Cross-Border Freight Corridors (UAE, Saudi Arabia, Oman, Qatar, Kuwait, Bahrain)
"""

import math
from typing import Dict, Any, List, Optional, Tuple

class HighwayFuelOptimizer:
    """
    Algorithmic optimization engine for highway routing, interstate border fuel arbitrage,
    and fleet cost minimization.
    """

    # 1. VEHICLE PROFILES
    VEHICLE_PROFILES = {
        "commercial_truck_40t": {
            "name": "Heavy Commercial Truck (16-Wheeler / 40T)",
            "tank_capacity_l": 400.0,
            "consumption_kml": 3.4,
            "icon": "🚛",
            "category": "commercial"
        },
        "medium_truck_bus": {
            "name": "Medium Truck / Inter-City Bus (15T)",
            "tank_capacity_l": 160.0,
            "consumption_kml": 6.2,
            "icon": "🚌",
            "category": "commercial"
        },
        "light_commercial_van": {
            "name": "Light Commercial Van / Pickup (LCV)",
            "tank_capacity_l": 75.0,
            "consumption_kml": 10.5,
            "icon": "🚐",
            "category": "fleet"
        },
        "suv_4x4": {
            "name": "Mid-to-Full Size SUV / 4x4",
            "tank_capacity_l": 65.0,
            "consumption_kml": 13.0,
            "icon": "🚙",
            "category": "personal"
        },
        "sedan_hatchback": {
            "name": "Sedan / Hatchback",
            "tank_capacity_l": 45.0,
            "consumption_kml": 16.5,
            "icon": "🚗",
            "category": "personal"
        }
    }

    # 2. INDIA STATES & UTS DATABASE (Live benchmark retail pump rates in INR)
    INDIA_NODES = {
        "Delhi": {"state": "Delhi (NCT)", "petrol": 96.72, "diesel": 87.62, "vat_pct": 19.4, "lat": 28.6139, "lon": 77.2090},
        "Haryana": {"state": "Haryana", "petrol": 95.25, "diesel": 88.05, "vat_pct": 18.2, "lat": 28.4595, "lon": 77.0266},
        "Uttar Pradesh": {"state": "Uttar Pradesh", "petrol": 94.75, "diesel": 87.85, "vat_pct": 17.5, "lat": 26.8467, "lon": 80.9462},
        "Rajasthan": {"state": "Rajasthan", "petrol": 104.88, "diesel": 90.36, "vat_pct": 31.0, "lat": 26.9124, "lon": 75.7873},
        "Gujarat": {"state": "Gujarat", "petrol": 94.42, "diesel": 89.15, "vat_pct": 13.7, "lat": 23.0225, "lon": 72.5714},
        "Maharashtra": {"state": "Maharashtra", "petrol": 104.21, "diesel": 92.15, "vat_pct": 25.0, "lat": 19.0760, "lon": 72.8777},
        "Karnataka": {"state": "Karnataka", "petrol": 102.86, "diesel": 88.94, "vat_pct": 18.4, "lat": 12.9716, "lon": 77.5946},
        "Tamil Nadu": {"state": "Tamil Nadu", "petrol": 100.75, "diesel": 92.34, "vat_pct": 15.0, "lat": 13.0827, "lon": 80.2707},
        "Telangana": {"state": "Telangana", "petrol": 107.41, "diesel": 95.65, "vat_pct": 35.2, "lat": 17.3850, "lon": 78.4867},
        "Andhra Pradesh": {"state": "Andhra Pradesh", "petrol": 109.87, "diesel": 97.71, "vat_pct": 31.0, "lat": 16.5062, "lon": 80.6480},
        "West Bengal": {"state": "West Bengal", "petrol": 103.94, "diesel": 90.76, "vat_pct": 25.0, "lat": 22.5726, "lon": 88.3639},
        "Punjab": {"state": "Punjab", "petrol": 96.88, "diesel": 87.16, "vat_pct": 15.5, "lat": 30.9010, "lon": 75.8573},
        "Madhya Pradesh": {"state": "Madhya Pradesh", "petrol": 106.47, "diesel": 91.84, "vat_pct": 29.0, "lat": 23.2599, "lon": 77.4126},
        "Bihar": {"state": "Bihar", "petrol": 105.18, "diesel": 92.04, "vat_pct": 26.0, "lat": 25.5941, "lon": 85.1376},
        "Kerala": {"state": "Kerala", "petrol": 105.84, "diesel": 94.84, "vat_pct": 30.0, "lat": 9.9312, "lon": 76.2673},
        "Odisha": {"state": "Odisha", "petrol": 101.06, "diesel": 92.64, "vat_pct": 28.0, "lat": 20.2961, "lon": 85.8245},
        "Assam": {"state": "Assam", "petrol": 96.01, "diesel": 88.27, "vat_pct": 22.0, "lat": 26.1445, "lon": 91.7362},
        "Jharkhand": {"state": "Jharkhand", "petrol": 97.81, "diesel": 92.56, "vat_pct": 22.0, "lat": 23.3441, "lon": 85.3096},
        "Chhattisgarh": {"state": "Chhattisgarh", "petrol": 100.39, "diesel": 93.33, "vat_pct": 24.0, "lat": 21.2514, "lon": 81.6296},
        "Himachal Pradesh": {"state": "Himachal Pradesh", "petrol": 95.28, "diesel": 87.32, "vat_pct": 14.0, "lat": 31.1048, "lon": 77.1734},
        "Uttarakhand": {"state": "Uttarakhand", "petrol": 93.45, "diesel": 88.32, "vat_pct": 17.0, "lat": 30.3165, "lon": 78.0322},
        "Goa": {"state": "Goa", "petrol": 96.48, "diesel": 88.24, "vat_pct": 21.0, "lat": 15.4909, "lon": 73.8278},
        "Jammu & Kashmir": {"state": "Jammu & Kashmir", "petrol": 97.50, "diesel": 83.26, "vat_pct": 16.5, "lat": 34.0837, "lon": 74.7973},
        "Chandigarh": {"state": "Chandigarh (UT)", "petrol": 94.24, "diesel": 82.40, "vat_pct": 11.0, "lat": 30.7333, "lon": 76.7794},
        "Puducherry": {"state": "Puducherry (UT)", "petrol": 94.18, "diesel": 84.34, "vat_pct": 14.0, "lat": 11.9416, "lon": 79.8083},
        "Daman & Diu": {"state": "Dadra & Nagar Haveli and Daman & Diu", "petrol": 92.50, "diesel": 87.80, "vat_pct": 12.0, "lat": 20.4283, "lon": 72.8397},
        "Sikkim": {"state": "Sikkim", "petrol": 100.75, "diesel": 88.90, "vat_pct": 20.0, "lat": 27.3389, "lon": 88.6065},
        "Meghalaya": {"state": "Meghalaya", "petrol": 96.80, "diesel": 87.90, "vat_pct": 20.0, "lat": 25.5788, "lon": 91.8933},
        "Tripura": {"state": "Tripura", "petrol": 97.45, "diesel": 86.50, "vat_pct": 21.0, "lat": 23.8315, "lon": 91.2868},
        "Nagaland": {"state": "Nagaland", "petrol": 97.10, "diesel": 88.40, "vat_pct": 21.5, "lat": 25.6751, "lon": 94.1086},
        "Manipur": {"state": "Manipur", "petrol": 99.20, "diesel": 87.60, "vat_pct": 22.0, "lat": 24.8170, "lon": 93.9368},
        "Mizoram": {"state": "Mizoram", "petrol": 99.15, "diesel": 88.02, "vat_pct": 22.0, "lat": 23.7271, "lon": 92.7176},
        "Arunachal Pradesh": {"state": "Arunachal Pradesh", "petrol": 90.95, "diesel": 80.45, "vat_pct": 10.0, "lat": 27.0844, "lon": 93.6053},
        "Ladakh": {"state": "Ladakh (UT)", "petrol": 98.40, "diesel": 84.10, "vat_pct": 16.5, "lat": 34.1526, "lon": 77.5771}
    }

    # 3. SAUDI ARABIA HUBS (Aramco official regulated prices in SAR)
    SAUDI_NODES = {
        "Riyadh": {"province": "Riyadh Province (Central)", "petrol_91": 2.18, "petrol_95": 2.33, "diesel": 1.15, "vat_pct": 15.0, "lat": 24.7136, "lon": 46.6753},
        "Jeddah": {"province": "Makkah Province (Western)", "petrol_91": 2.18, "petrol_95": 2.33, "diesel": 1.15, "vat_pct": 15.0, "lat": 21.4858, "lon": 39.1925},
        "Dammam": {"province": "Eastern Province", "petrol_91": 2.18, "petrol_95": 2.33, "diesel": 1.15, "vat_pct": 15.0, "lat": 26.4207, "lon": 50.0888},
        "Mecca": {"province": "Makkah Province", "petrol_91": 2.18, "petrol_95": 2.33, "diesel": 1.15, "vat_pct": 15.0, "lat": 21.3891, "lon": 39.8579},
        "Medina": {"province": "Madinah Province", "petrol_91": 2.18, "petrol_95": 2.33, "diesel": 1.15, "vat_pct": 15.0, "lat": 24.5247, "lon": 39.5692},
        "Tabuk": {"province": "Tabuk Province (North-West)", "petrol_91": 2.18, "petrol_95": 2.33, "diesel": 1.15, "vat_pct": 15.0, "lat": 28.3835, "lon": 36.5662},
        "Jubail": {"province": "Eastern Province (Industrial)", "petrol_91": 2.18, "petrol_95": 2.33, "diesel": 1.15, "vat_pct": 15.0, "lat": 27.0046, "lon": 49.6601},
        "Abha": {"province": "Asir Province (South)", "petrol_91": 2.18, "petrol_95": 2.33, "diesel": 1.15, "vat_pct": 15.0, "lat": 18.2164, "lon": 42.5053},
        "Yanbu": {"province": "Madinah (Port & Petrochemical)", "petrol_91": 2.18, "petrol_95": 2.33, "diesel": 1.15, "vat_pct": 15.0, "lat": 24.0891, "lon": 38.0618},
        "Al Batha Border": {"province": "Eastern Province (UAE Border)", "petrol_91": 2.18, "petrol_95": 2.33, "diesel": 1.15, "vat_pct": 15.0, "lat": 24.1293, "lon": 51.5833},
        "Salwa Border": {"province": "Eastern Province (Qatar Border)", "petrol_91": 2.18, "petrol_95": 2.33, "diesel": 1.15, "vat_pct": 15.0, "lat": 24.7333, "lon": 50.7667},
        "Khafji Border": {"province": "Eastern Province (Kuwait Border)", "petrol_91": 2.18, "petrol_95": 2.33, "diesel": 1.15, "vat_pct": 15.0, "lat": 28.4392, "lon": 48.4914}
    }

    # 4. DUBAI & UAE EMIRATES (Deregulated Fuel Price Committee rates in AED)
    UAE_NODES = {
        "Dubai": {"emirate": "Dubai", "petrol_95": 2.93, "petrol_98": 3.05, "diesel": 3.10, "vat_pct": 5.0, "lat": 25.2048, "lon": 55.2708},
        "Abu Dhabi": {"emirate": "Abu Dhabi (Capital)", "petrol_95": 2.93, "petrol_98": 3.05, "diesel": 3.10, "vat_pct": 5.0, "lat": 24.4539, "lon": 54.3773},
        "Sharjah": {"emirate": "Sharjah", "petrol_95": 2.93, "petrol_98": 3.05, "diesel": 3.10, "vat_pct": 5.0, "lat": 25.3463, "lon": 55.4209},
        "Ajman": {"emirate": "Ajman", "petrol_95": 2.93, "petrol_98": 3.05, "diesel": 3.10, "vat_pct": 5.0, "lat": 25.4052, "lon": 55.5136},
        "Ras Al Khaimah": {"emirate": "Ras Al Khaimah", "petrol_95": 2.93, "petrol_98": 3.05, "diesel": 3.10, "vat_pct": 5.0, "lat": 25.6741, "lon": 55.9804},
        "Fujairah": {"emirate": "Fujairah (Bunkering Hub)", "petrol_95": 2.93, "petrol_98": 3.05, "diesel": 3.10, "vat_pct": 5.0, "lat": 25.1288, "lon": 56.3265},
        "Umm Al Quwain": {"emirate": "Umm Al Quwain", "petrol_95": 2.93, "petrol_98": 3.05, "diesel": 3.10, "vat_pct": 5.0, "lat": 25.5647, "lon": 55.5552},
        "Al Ain": {"emirate": "Abu Dhabi (Eastern Region)", "petrol_95": 2.93, "petrol_98": 3.05, "diesel": 3.10, "vat_pct": 5.0, "lat": 24.2075, "lon": 55.7447},
        "Hatta": {"emirate": "Dubai (Oman Border)", "petrol_95": 2.93, "petrol_98": 3.05, "diesel": 3.10, "vat_pct": 5.0, "lat": 24.8058, "lon": 56.1264},
        "Ghuwaifat": {"emirate": "Abu Dhabi (Saudi Border)", "petrol_95": 2.93, "petrol_98": 3.05, "diesel": 3.10, "vat_pct": 5.0, "lat": 24.1200, "lon": 51.6000}
    }

    # 5. MIDDLE EAST GCC HUBS (Local currencies normalized to USD / AED / SAR)
    # Currency Rates: 1 USD = 3.6725 AED = 3.75 SAR = 0.385 OMR = 3.64 QAR = 0.308 KWD = 0.376 BHD
    GCC_CROSS_BORDER_NODES = {
        "Dubai (UAE)": {"country": "UAE", "currency": "AED", "petrol": 2.93, "diesel": 3.10, "diesel_sar_equiv": 3.17, "lat": 25.2048, "lon": 55.2708},
        "Abu Dhabi (UAE)": {"country": "UAE", "currency": "AED", "petrol": 2.93, "diesel": 3.10, "diesel_sar_equiv": 3.17, "lat": 24.4539, "lon": 54.3773},
        "Riyadh (Saudi Arabia)": {"country": "Saudi Arabia", "currency": "SAR", "petrol": 2.18, "diesel": 1.15, "diesel_sar_equiv": 1.15, "lat": 24.7136, "lon": 46.6753},
        "Dammam (Saudi Arabia)": {"country": "Saudi Arabia", "currency": "SAR", "petrol": 2.18, "diesel": 1.15, "diesel_sar_equiv": 1.15, "lat": 26.4207, "lon": 50.0888},
        "Al Batha Border (KSA/UAE)": {"country": "Saudi Border", "currency": "SAR", "petrol": 2.18, "diesel": 1.15, "diesel_sar_equiv": 1.15, "lat": 24.1293, "lon": 51.5833},
        "Muscat (Oman)": {"country": "Oman", "currency": "OMR", "petrol": 0.239, "diesel": 0.258, "diesel_sar_equiv": 2.51, "lat": 23.5880, "lon": 58.3829},
        "Doha (Qatar)": {"country": "Qatar", "currency": "QAR", "petrol": 2.10, "diesel": 2.05, "diesel_sar_equiv": 2.11, "lat": 25.2854, "lon": 51.5310},
        "Manama (Bahrain)": {"country": "Bahrain", "currency": "BHD", "petrol": 0.200, "diesel": 0.180, "diesel_sar_equiv": 1.79, "lat": 26.2285, "lon": 50.5860},
        "Kuwait City (Kuwait)": {"country": "Kuwait", "currency": "KWD", "petrol": 0.105, "diesel": 0.115, "diesel_sar_equiv": 1.40, "lat": 29.3759, "lon": 47.9774}
    }

    # 6. POPULAR FREIGHT CORRIDORS
    PRESET_CORRIDORS = {
        "india": [
            {
                "id": "delhi_mumbai",
                "name": "Delhi ➔ Mumbai Freight Express (NH48)",
                "distance_km": 1420,
                "highway": "NH48 (Western Dedicated Freight Corridor)",
                "path": ["Delhi", "Haryana", "Rajasthan", "Gujarat", "Maharashtra"],
                "path_segments_km": [45, 110, 480, 515, 270]
            },
            {
                "id": "delhi_kolkata",
                "name": "Delhi ➔ Kolkata Golden Corridor (NH19)",
                "distance_km": 1510,
                "highway": "NH19 (Grand Trunk Freight Route)",
                "path": ["Delhi", "Uttar Pradesh", "Bihar", "Jharkhand", "West Bengal"],
                "path_segments_km": [35, 785, 220, 240, 230]
            },
            {
                "id": "mumbai_chennai",
                "name": "Mumbai ➔ Chennai Logistics Highway (NH48)",
                "distance_km": 1340,
                "highway": "NH48 (Deccan Logistics Spine)",
                "path": ["Maharashtra", "Karnataka", "Andhra Pradesh", "Tamil Nadu"],
                "path_segments_km": [380, 640, 180, 140]
            },
            {
                "id": "delhi_amritsar",
                "name": "Delhi ➔ Amritsar Northern Spine (NH44)",
                "distance_km": 460,
                "highway": "NH44 (North India Industrial Axis)",
                "path": ["Delhi", "Haryana", "Punjab"],
                "path_segments_km": [35, 235, 190]
            },
            {
                "id": "bangalore_hyderabad",
                "name": "Bengaluru ➔ Hyderabad Tech & Freight Line (NH44)",
                "distance_km": 570,
                "highway": "NH44 (Peninsular Express Route)",
                "path": ["Karnataka", "Andhra Pradesh", "Telangana"],
                "path_segments_km": [105, 260, 205]
            },
            {
                "id": "kolkata_guwahati",
                "name": "Kolkata ➔ Guwahati Northeast Gateway (NH12/NH27)",
                "distance_km": 1010,
                "highway": "NH12 / NH27 (Chicken's Neck Corridor)",
                "path": ["West Bengal", "Bihar", "Assam"],
                "path_segments_km": [520, 160, 330]
            }
        ],
        "saudi": [
            {
                "id": "riyadh_jeddah",
                "name": "Riyadh ➔ Jeddah Trans-Peninsula Highway (Route 40)",
                "distance_km": 950,
                "highway": "Makkah-Madinah Highway / Route 40",
                "path": ["Riyadh", "Mecca", "Jeddah"],
                "path_segments_km": [480, 390, 80]
            },
            {
                "id": "dammam_riyadh",
                "name": "Dammam ➔ Riyadh Industrial Supply Axis (Route 40)",
                "distance_km": 390,
                "highway": "Dammam-Riyadh Expressway",
                "path": ["Dammam", "Jubail", "Riyadh"],
                "path_segments_km": [85, 120, 185]
            },
            {
                "id": "jeddah_medina",
                "name": "Jeddah ➔ Medina Pilgrimage & Cargo Expressway (Route 15)",
                "distance_km": 420,
                "highway": "Al Hijrah Expressway",
                "path": ["Jeddah", "Yanbu", "Medina"],
                "path_segments_km": [180, 110, 130]
            },
            {
                "id": "riyadh_tabuk",
                "name": "Riyadh ➔ Tabuk Northern Trade Link (Route 65)",
                "distance_km": 1100,
                "highway": "Highway 65 / Jordan Gateway",
                "path": ["Riyadh", "Medina", "Tabuk"],
                "path_segments_km": [420, 360, 320]
            }
        ],
        "uae": [
            {
                "id": "abudhabi_fujairah",
                "name": "Abu Dhabi ➔ Dubai ➔ Sharjah ➔ Fujairah (E11/E84)",
                "distance_km": 260,
                "highway": "E11 Sheikh Zayed Road / E84 Sheikh Khalifa Highway",
                "path": ["Abu Dhabi", "Dubai", "Sharjah", "Fujairah"],
                "path_segments_km": [130, 25, 45, 60]
            },
            {
                "id": "dubai_alain",
                "name": "Dubai ➔ Al Ain Oasis Freight Link (E66)",
                "distance_km": 135,
                "highway": "Dubai-Al Ain Road (E66)",
                "path": ["Dubai", "Abu Dhabi", "Al Ain"],
                "path_segments_km": [40, 45, 50]
            },
            {
                "id": "dubai_hatta",
                "name": "Dubai ➔ Hatta Oman Transit Highway (E44)",
                "distance_km": 115,
                "highway": "Al Awir Road / Hatta Expressway (E44)",
                "path": ["Dubai", "Sharjah", "Hatta"],
                "path_segments_km": [45, 30, 40]
            },
            {
                "id": "abudhabi_ghuwaifat",
                "name": "Abu Dhabi ➔ Ghuwaifat Saudi Frontier (E11)",
                "distance_km": 350,
                "highway": "Sheikh Khalifa bin Zayed International Road (E11)",
                "path": ["Abu Dhabi", "Ghuwaifat"],
                "path_segments_km": [160, 190]
            }
        ],
        "gcc_cross_border": [
            {
                "id": "dubai_riyadh",
                "name": "Dubai (UAE) ➔ Riyadh (Saudi Arabia) via Al Batha",
                "distance_km": 1050,
                "highway": "GCC Trans-Arabian Highway (E11 / KSA Route 10 / Route 40)",
                "path": ["Dubai (UAE)", "Abu Dhabi (UAE)", "Al Batha Border (KSA/UAE)", "Riyadh (Saudi Arabia)"],
                "path_segments_km": [135, 335, 160, 420],
                "border_crossing": "Ghuwaifat / Al Batha Border Post"
            },
            {
                "id": "abudhabi_muscat",
                "name": "Abu Dhabi (UAE) ➔ Muscat (Oman) via Al Ain",
                "distance_km": 465,
                "highway": "UAE-Oman Trade Corridor (E22 / Oman Route 7)",
                "path": ["Abu Dhabi (UAE)", "Dubai (UAE)", "Muscat (Oman)"],
                "path_segments_km": [135, 110, 220],
                "border_crossing": "Mezyad / Hafit Border Post"
            },
            {
                "id": "dammam_bahrain",
                "name": "Dammam (Saudi Arabia) ➔ Manama (Bahrain) Causeway",
                "distance_km": 85,
                "highway": "King Fahd Causeway Marine Highway",
                "path": ["Dammam (Saudi Arabia)", "Manama (Bahrain)"],
                "path_segments_km": [45, 40],
                "border_crossing": "Passport Island / King Fahd Causeway"
            },
            {
                "id": "riyadh_doha",
                "name": "Riyadh (Saudi Arabia) ➔ Doha (Qatar) via Salwa",
                "distance_km": 590,
                "highway": "Route 40 / Salwa-Doha Highway",
                "path": ["Riyadh (Saudi Arabia)", "Dammam (Saudi Arabia)", "Doha (Qatar)"],
                "path_segments_km": [310, 140, 140],
                "border_crossing": "Salwa / Abu Samra Border Post"
            },
            {
                "id": "kuwait_dammam",
                "name": "Kuwait City ➔ Dammam (Saudi Arabia) via Nuwaiseeb",
                "distance_km": 415,
                "highway": "Route 40 / Arabian Gulf Freight Corridor",
                "path": ["Kuwait City (Kuwait)", "Dammam (Saudi Arabia)"],
                "path_segments_km": [115, 300],
                "border_crossing": "Nuwaiseeb / Khafji Border Post"
            }
        ]
    }

    @classmethod
    def calculate_haversine_distance(cls, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculates spherical distance in km between two lat/lon points with highway road factor 1.25."""
        R = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        crow_dist = R * c
        return round(crow_dist * 1.25, 1)  # Highway routing curvature factor

    @classmethod
    def get_corridors_for_region(cls, region: str) -> List[Dict[str, Any]]:
        """Returns list of preset corridors for the selected region."""
        return cls.PRESET_CORRIDORS.get(region, cls.PRESET_CORRIDORS["india"])

    @classmethod
    def optimize_trip(
        cls,
        region: str,
        origin: str,
        destination: str,
        vehicle_type: str,
        fuel_type: str = "diesel",
        custom_tank_l: Optional[float] = None,
        custom_kml: Optional[float] = None,
        selected_corridor_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculates the complete highway fuel optimization blueprint:
        - Total distance, transit waypoints, fuel required
        - Arbitrage strategy: Optimal stops (lowest VAT/cheapest fuel), where to fill full tank
        - Naive baseline cost vs Optimized cost
        - Net cash savings and % savings
        """
        # 1. Resolve vehicle configuration
        v_profile = cls.VEHICLE_PROFILES.get(vehicle_type, cls.VEHICLE_PROFILES["commercial_truck_40t"])
        tank_cap = float(custom_tank_l) if custom_tank_l and custom_tank_l > 0 else v_profile["tank_capacity_l"]
        mileage_kml = float(custom_kml) if custom_kml and custom_kml > 0 else v_profile["consumption_kml"]
        mileage_kml = max(mileage_kml, 1.0)
        tank_range_km = tank_cap * mileage_kml

        # 2. Select node database and currency based on region
        if region == "saudi":
            nodes_db = cls.SAUDI_NODES
            currency_code = "SAR"
            currency_symbol = "SAR "
            preset_list = cls.PRESET_CORRIDORS["saudi"]
        elif region == "uae":
            nodes_db = cls.UAE_NODES
            currency_code = "AED"
            currency_symbol = "AED "
            preset_list = cls.PRESET_CORRIDORS["uae"]
        elif region == "gcc_cross_border":
            nodes_db = cls.GCC_CROSS_BORDER_NODES
            currency_code = "SAR"
            currency_symbol = "SAR (Equiv) "
            preset_list = cls.PRESET_CORRIDORS["gcc_cross_border"]
        else:
            region = "india"
            nodes_db = cls.INDIA_NODES
            currency_code = "INR"
            currency_symbol = "₹"
            preset_list = cls.PRESET_CORRIDORS["india"]

        # 3. Resolve path and distance
        matched_corridor = None
        if selected_corridor_id:
            for c in preset_list:
                if c["id"] == selected_corridor_id:
                    matched_corridor = c
                    break

        if matched_corridor:
            path = matched_corridor["path"]
            segments = matched_corridor.get("path_segments_km", [])
            total_dist_km = matched_corridor["distance_km"]
            highway_name = matched_corridor.get("highway", "Primary Freight Corridor")
            corridor_title = matched_corridor["name"]
        else:
            # Custom origin / destination routing
            if origin not in nodes_db:
                origin = list(nodes_db.keys())[0]
            if destination not in nodes_db:
                destination = list(nodes_db.keys())[1]

            if origin == destination:
                path = [origin]
                segments = [0]
                total_dist_km = 50.0  # Local distribution loop
            else:
                path = [origin, destination]
                n1 = nodes_db[origin]
                n2 = nodes_db[destination]
                calc_dist = cls.calculate_haversine_distance(n1["lat"], n1["lon"], n2["lat"], n2["lon"])
                total_dist_km = max(calc_dist, 60.0)
                segments = [round(total_dist_km, 1)]
            highway_name = f"Direct Route: {origin} ➔ {destination}"
            corridor_title = f"{origin} ➔ {destination} Freight Axis"

        # 4. Extract fuel price per node
        def _get_node_price(node_key: str) -> float:
            nd = nodes_db.get(node_key, {})
            if region == "india":
                return nd.get("diesel" if fuel_type == "diesel" else "petrol", 89.0)
            elif region == "saudi":
                if fuel_type == "diesel":
                    return nd.get("diesel", 1.15)
                elif fuel_type == "petrol_95":
                    return nd.get("petrol_95", 2.33)
                return nd.get("petrol_91", 2.18)
            elif region == "uae":
                if fuel_type == "diesel":
                    return nd.get("diesel", 3.10)
                elif fuel_type == "petrol_98":
                    return nd.get("petrol_98", 3.05)
                return nd.get("petrol_95", 2.93)
            elif region == "gcc_cross_border":
                # Returns normalized SAR equivalent for cross-border fairness
                return nd.get("diesel_sar_equiv" if fuel_type == "diesel" else "petrol", 2.18)
            return 89.0

        # Calculate waypoint distances cumulative from origin
        waypoints_data = []
        cum_km = 0.0
        for i, node_name in enumerate(path):
            seg_len = segments[i] if i < len(segments) else (total_dist_km - cum_km)
            p_price = _get_node_price(node_name)
            node_info = nodes_db.get(node_name, {})
            vat = node_info.get("vat_pct", 18.0)
            jurisdiction = node_info.get("state") or node_info.get("province") or node_info.get("emirate") or node_info.get("country", node_name)
            
            waypoints_data.append({
                "index": i + 1,
                "node": node_name,
                "jurisdiction": jurisdiction,
                "segment_km": seg_len,
                "cumulative_km": cum_km,
                "fuel_price": p_price,
                "vat_pct": vat,
                "lat": node_info.get("lat", 0.0),
                "lon": node_info.get("lon", 0.0)
            })
            cum_km += seg_len

        total_dist_km = max(cum_km, 1.0)
        total_fuel_needed_l = round(total_dist_km / mileage_kml, 1)

        # 5. Price Analysis: Find cheapest & most expensive stops
        prices_on_route = [w["fuel_price"] for w in waypoints_data]
        min_price = min(prices_on_route)
        max_price = max(prices_on_route)
        avg_price = sum(prices_on_route) / len(prices_on_route)
        price_spread = round(max_price - min_price, 2)

        # 6. Arbitrage Strategy Simulation
        # Naive Strategy: Refuel evenly or randomly whenever empty, paying average corridor price
        naive_total_cost = round(total_fuel_needed_l * avg_price, 2)

        # Optimal Strategy: Top-up heavily at waypoints where price <= min_price + 0.15 * spread
        # Avoid filling at waypoints where price is within top 25% of spread
        cheapest_nodes = [w for w in waypoints_data if w["fuel_price"] <= (min_price + 0.20 * price_spread + 0.01)]
        cheapest_node_names = [w["node"] for w in cheapest_nodes]
        expensive_nodes = [w for w in waypoints_data if w["fuel_price"] >= (max_price - 0.20 * price_spread - 0.01)]
        expensive_node_names = [w["node"] for w in expensive_nodes]

        # Waypoint strategy recommendations
        refuel_schedule = []
        fuel_remaining_l = tank_cap * 0.40  # Assume vehicle starts with 40% tank
        optimized_total_cost = 0.0
        total_liters_bought = 0.0

        for i, wp in enumerate(waypoints_data):
            dist_to_next = segments[i] if i < len(segments) else (total_dist_km - wp["cumulative_km"])
            fuel_burn_to_next = dist_to_next / mileage_kml
            
            is_cheapest = wp["node"] in cheapest_node_names
            is_expensive = wp["node"] in expensive_node_names
            is_origin = (i == 0)
            is_destination = (i == len(waypoints_data) - 1)

            fill_action = "Transit Pass"
            fill_liters = 0.0
            fill_cost = 0.0
            reason = "Adequate fuel buffer; transit without stopping."

            if is_origin:
                if is_cheapest or wp["fuel_price"] < avg_price:
                    fill_action = "Full Tank Top-Up ⛽"
                    fill_liters = round(tank_cap - fuel_remaining_l, 1)
                    reason = f"Origin fuel is low cost ({currency_symbol}{wp['fuel_price']}/L). Lock in full tank capacity."
                else:
                    # Origin is somewhat expensive, buy only minimum safety buffer
                    fill_action = "Strategic Partial Fill 🟡"
                    needed_to_cheapest = min(tank_cap, max(fuel_burn_to_next * 1.3, 40.0))
                    fill_liters = round(max(0.0, needed_to_cheapest - fuel_remaining_l), 1)
                    reason = f"High tax zone ({wp['vat_pct']}% VAT). Buy only minimum required until reaching cheaper border zone."
            elif is_destination:
                fill_action = "Trip Complete 🏁"
                fill_liters = 0.0
                reason = "Arrived at destination hub."
            elif is_cheapest:
                fill_action = "MAX REFUEL ARBITRAGE ⭐"
                fill_liters = round(tank_cap - fuel_remaining_l, 1)
                reason = f"Optimal arbitrage zone ({currency_symbol}{wp['fuel_price']}/L)! Top up to 100% capacity before higher tax state."
            elif is_expensive:
                # Avoid filling here if fuel buffer permits
                if fuel_remaining_l > fuel_burn_to_next * 1.15:
                    fill_action = "DO NOT REFUEL 🛑"
                    fill_liters = 0.0
                    reason = f"High VAT alert ({currency_symbol}{wp['fuel_price']}/L, {wp['vat_pct']}% VAT). Avoid purchasing here!"
                else:
                    fill_action = "Emergency Splash Only ⚠️"
                    fill_liters = round(max(10.0, (fuel_burn_to_next * 1.25) - fuel_remaining_l), 1)
                    reason = f"High price zone. Refuel only {fill_liters}L emergency buffer to reach next discount border stop."
            else:
                if fuel_remaining_l < (tank_cap * 0.25):
                    fill_action = "Maintenance Top-Up ⛽"
                    fill_liters = round(tank_cap * 0.5 - fuel_remaining_l, 1)
                    reason = "Mid-range buffer maintainer."

            fill_liters = max(0.0, fill_liters)
            fill_cost = round(fill_liters * wp["fuel_price"], 2)
            fuel_remaining_l = min(tank_cap, fuel_remaining_l + fill_liters)
            
            # Consume fuel for next segment
            fuel_remaining_l = max(0.0, fuel_remaining_l - fuel_burn_to_next)
            optimized_total_cost += fill_cost
            total_liters_bought += fill_liters

            refuel_schedule.append({
                "step": i + 1,
                "location": wp["node"],
                "jurisdiction": wp["jurisdiction"],
                "km_mark": round(wp["cumulative_km"], 1),
                "price": wp["fuel_price"],
                "action": fill_action,
                "liters_filled": fill_liters,
                "cost": fill_cost,
                "reason": reason,
                "vat_pct": wp["vat_pct"]
            })

        # Ensure realistic baseline comparison
        if total_liters_bought < total_fuel_needed_l:
            deficit = total_fuel_needed_l - total_liters_bought
            optimized_total_cost += round(deficit * min_price, 2)
            total_liters_bought = total_fuel_needed_l

        # Unoptimized cost assumes 50% bought at highest price and 50% at average price
        unoptimized_cost = round(total_fuel_needed_l * (0.6 * max_price + 0.4 * avg_price), 2)
        net_savings = max(0.0, round(unoptimized_cost - optimized_total_cost, 2))
        savings_pct = round((net_savings / unoptimized_cost * 100), 1) if unoptimized_cost > 0 else 0.0

        return {
            "region": region,
            "corridor_title": corridor_title,
            "highway_name": highway_name,
            "origin": origin,
            "destination": destination,
            "total_distance_km": total_dist_km,
            "est_transit_hours": round(total_dist_km / 65.0, 1),
            "vehicle": v_profile["name"],
            "vehicle_icon": v_profile["icon"],
            "tank_capacity_l": tank_cap,
            "mileage_kml": mileage_kml,
            "tank_range_km": round(tank_range_km, 1),
            "fuel_type": fuel_type.upper().replace("_", " "),
            "total_fuel_needed_l": total_fuel_needed_l,
            "currency_code": currency_code,
            "currency_symbol": currency_symbol,
            "price_metrics": {
                "min_price": min_price,
                "max_price": max_price,
                "avg_price": round(avg_price, 2),
                "price_spread": price_spread,
                "cheapest_hubs": cheapest_node_names,
                "expensive_hubs": expensive_node_names
            },
            "financial_summary": {
                "unoptimized_cost": unoptimized_cost,
                "optimized_cost": round(optimized_total_cost, 2),
                "net_savings": net_savings,
                "savings_pct": savings_pct,
                "cost_per_km": round(optimized_total_cost / total_dist_km, 2) if total_dist_km > 0 else 0.0
            },
            "waypoints": waypoints_data,
            "refuel_schedule": refuel_schedule
        }
