import requests
import csv
import os
import time
from datetime import datetime

# GitHub Actions Secrets se milengi: TOMTOM_API_KEY_1, TOMTOM_API_KEY_2, TOMTOM_API_KEY_3
# Local test ke liye environment variables set karna:
#   export TOMTOM_API_KEY_1=xxxx
#   export TOMTOM_API_KEY_2=xxxx
#   export TOMTOM_API_KEY_3=xxxx
API_KEYS = [
    os.environ.get("TOMTOM_API_KEY_1"),
    os.environ.get("TOMTOM_API_KEY_2"),
    os.environ.get("TOMTOM_API_KEY_3"),
]
API_KEYS = [k for k in API_KEYS if k]  # empty/missing keys hata do

# ─────────────────────────────────────────────────────────────
# BANGALORE — 150 major roads (arterial + key sub-arterial),
# covering all zones + roads leading to famous landmarks
# ─────────────────────────────────────────────────────────────
LOCATIONS = [
    # ── Central Bangalore ──────────────────────────────
    ("Bangalore", "MG Road", 12.9758, 77.6045),
    ("Bangalore", "Brigade Road", 12.9716, 77.6069),
    ("Bangalore", "Commercial Street", 12.9822, 77.6086),
    ("Bangalore", "Residency Road", 12.9698, 77.6047),
    ("Bangalore", "Infantry Road", 12.9868, 77.5978),
    ("Bangalore", "Cubbon Road", 12.9770, 77.5952),
    ("Bangalore", "Kasturba Road", 12.9762, 77.5951),
    ("Bangalore", "Church Street", 12.9750, 77.6058),
    ("Bangalore", "St Marks Road", 12.9730, 77.6023),
    ("Bangalore", "Vittal Mallya Road", 12.9700, 77.5980),
    ("Bangalore", "Richmond Road", 12.9646, 77.6042),
    ("Bangalore", "Lavelle Road", 12.9711, 77.5983),
    ("Bangalore", "Museum Road", 12.9739, 77.6035),
    ("Bangalore", "Palace Road", 12.9988, 77.5900),
    ("Bangalore", "Sankey Road", 13.0020, 77.5780),
    ("Bangalore", "Race Course Road", 12.9880, 77.5810),
    ("Bangalore", "K H Road", 12.9560, 77.6010),
    ("Bangalore", "Wilson Garden Road", 12.9530, 77.5980),
    ("Bangalore", "Double Road, Sirsi Circle", 12.9670, 77.5650),
    ("Bangalore", "Seshadripuram Main Road", 12.9950, 77.5750),
    ("Bangalore", "Gandhinagar Main Road", 12.9800, 77.5780),
    ("Bangalore", "Avenue Road", 12.9640, 77.5790),
    ("Bangalore", "Dr Ambedkar Veedhi, Vidhana Soudha", 12.9794, 77.5912),
    ("Bangalore", "Sheshadri Road, KSR Station", 12.9760, 77.5700),
    ("Bangalore", "Gubbi Thotadappa Road, City Station", 12.9784, 77.5700),
    ("Bangalore", "Tank Bund Road, Majestic", 12.9770, 77.5720),
    ("Bangalore", "Magrath Road, Garuda Mall", 12.9730, 77.6080),
    ("Bangalore", "Shanthi Nagar Bus Stand Road", 12.9590, 77.5990),
    ("Bangalore", "K G Road, Corporation Circle", 12.9670, 77.5850),
    ("Bangalore", "City Market Road", 12.9630, 77.5760),
    ("Bangalore", "Chickpet Main Road", 12.9680, 77.5780),
    ("Bangalore", "Nagarathpet Road", 12.9670, 77.5750),
    ("Bangalore", "Lalbagh Siddapura Road", 12.9500, 77.5850),
    ("Bangalore", "Adugodi Main Road", 12.9440, 77.6130),

    # ── North Bangalore ──────────────────────────────
    ("Bangalore", "Hebbal Flyover", 13.0358, 77.5970),
    ("Bangalore", "Yeshwanthpur Circle", 13.0284, 77.5540),
    ("Bangalore", "Tumkur Road", 13.0280, 77.5350),
    ("Bangalore", "Malleshwaram Sampige Road", 13.0060, 77.5700),
    ("Bangalore", "Rajajinagar Main Road", 12.9910, 77.5530),
    ("Bangalore", "RT Nagar Main Road", 13.0200, 77.5950),
    ("Bangalore", "Hennur Road", 13.0300, 77.6350),
    ("Bangalore", "Thanisandra Main Road", 13.0550, 77.6300),
    ("Bangalore", "Bagalur Main Road", 13.1000, 77.6300),
    ("Bangalore", "Bellary Road NH44, Airport Approach", 13.0450, 77.5850),
    ("Bangalore", "Kempegowda International Airport Road", 13.1986, 77.7066),
    ("Bangalore", "Jalahalli Road", 13.0450, 77.5500),
    ("Bangalore", "Vidyaranyapura Main Road", 13.0700, 77.5560),
    ("Bangalore", "New BEL Road", 13.0180, 77.5650),
    ("Bangalore", "HMT Main Road", 13.0480, 77.5560),
    ("Bangalore", "Sanjaynagar Main Road", 13.0230, 77.5780),
    ("Bangalore", "Sadashivanagar Main Road", 13.0060, 77.5820),
    ("Bangalore", "Yelahanka Main Road", 13.1005, 77.5960),
    ("Bangalore", "Yelahanka New Town Road", 13.1010, 77.5850),
    ("Bangalore", "Doddaballapur Road", 13.1200, 77.5800),
    ("Bangalore", "Hebbal-Nagawara ORR", 13.0350, 77.6220),
    ("Bangalore", "Nagawara Main Road", 13.0400, 77.6240),
    ("Bangalore", "Manyata Tech Park Road", 13.0480, 77.6200),
    ("Bangalore", "Peenya Main Road", 13.0290, 77.5170),
    ("Bangalore", "Peenya Industrial Road", 13.0350, 77.5220),
    ("Bangalore", "Nelamangala Road NH48", 13.0980, 77.4200),
    ("Bangalore", "Dasarahalli Main Road", 13.0430, 77.5230),
    ("Bangalore", "ISKCON Hare Krishna Hill Road", 13.0100, 77.5510),
    ("Bangalore", "Kammanahalli Main Road", 13.0170, 77.6370),
    ("Bangalore", "Banaswadi Main Road", 13.0140, 77.6500),
    ("Bangalore", "HBR Layout Main Road", 13.0270, 77.6230),
    ("Bangalore", "Kalyan Nagar Main Road", 13.0230, 77.6400),
    ("Bangalore", "Horamavu Main Road", 13.0330, 77.6560),

    # ── East Bangalore ──────────────────────────────
    ("Bangalore", "100 Feet Road, Indiranagar", 12.9784, 77.6408),
    ("Bangalore", "CMH Road", 12.9789, 77.6394),
    ("Bangalore", "Domlur Road", 12.9610, 77.6390),
    ("Bangalore", "Old Airport Road", 12.9611, 77.6497),
    ("Bangalore", "Outer Ring Road, Marathahalli", 12.9569, 77.6974),
    ("Bangalore", "Whitefield Main Road", 12.9698, 77.7500),
    ("Bangalore", "Varthur Road", 12.9420, 77.7350),
    ("Bangalore", "KR Puram Main Road", 13.0060, 77.6960),
    ("Bangalore", "Old Madras Road towards Hoskote", 13.0100, 77.7100),
    ("Bangalore", "Hoskote Road", 13.0700, 77.7900),
    ("Bangalore", "ITPL Main Road", 12.9860, 77.7280),
    ("Bangalore", "Kadugodi Main Road", 12.9910, 77.7620),
    ("Bangalore", "Panathur Main Road", 12.9370, 77.6980),
    ("Bangalore", "Bellandur Main Road", 12.9260, 77.6770),
    ("Bangalore", "Outer Ring Road, Bellandur-Marathahalli", 12.9350, 77.6900),
    ("Bangalore", "Tin Factory Junction", 13.0020, 77.6690),
    ("Bangalore", "Ramamurthy Nagar Main Road", 13.0170, 77.6650),
    ("Bangalore", "CV Raman Nagar Main Road", 12.9840, 77.6660),
    ("Bangalore", "Cambridge Layout Road", 12.9680, 77.6390),
    ("Bangalore", "HAL 2nd Stage Road", 12.9600, 77.6420),
    ("Bangalore", "Jeevanbheemanagar Main Road", 12.9630, 77.6540),
    ("Bangalore", "Vimanapura Main Road", 12.9600, 77.6650),
    ("Bangalore", "Konena Agrahara Main Road", 12.9500, 77.6700),
    ("Bangalore", "Devarabeesanahalli Road", 12.9350, 77.6930),
    ("Bangalore", "Kundalahalli Main Road", 12.9700, 77.7160),
    ("Bangalore", "Kadubeesanahalli Main Road", 12.9280, 77.6970),
    ("Bangalore", "Phoenix Marketcity Road, Mahadevapura", 12.9970, 77.6960),
    ("Bangalore", "Ejipura Main Road", 12.9370, 77.6350),

    # ── South Bangalore ──────────────────────────────
    ("Bangalore", "Jayanagar 4th Block", 12.9308, 77.5838),
    ("Bangalore", "JP Nagar", 12.9077, 77.5850),
    ("Bangalore", "Bannerghatta Road", 12.9082, 77.5972),
    ("Bangalore", "Hosur Road", 12.9345, 77.6100),
    ("Bangalore", "80 Feet Road, Koramangala", 12.9352, 77.6146),
    ("Bangalore", "HSR Layout 27th Main", 12.9110, 77.6370),
    ("Bangalore", "Electronic City Main Road", 12.8450, 77.6600),
    ("Bangalore", "Bommanahalli Main Road", 12.9000, 77.6150),
    ("Bangalore", "Silk Board Junction", 12.9172, 77.6228),
    ("Bangalore", "BTM Layout Main Road", 12.9160, 77.6100),
    ("Bangalore", "Banashankari Main Road", 12.9250, 77.5460),
    ("Bangalore", "Kanakapura Road", 12.9080, 77.5400),
    ("Bangalore", "Uttarahalli Main Road", 12.9010, 77.5460),
    ("Bangalore", "Bull Temple Road, Basavanagudi", 12.9430, 77.5730),
    ("Bangalore", "Gandhi Bazaar Main Road", 12.9420, 77.5730),
    ("Bangalore", "RV Road", 12.9350, 77.5730),
    ("Bangalore", "NICE Road, South", 12.8900, 77.5300),

    # ── West Bangalore ──────────────────────────────
    ("Bangalore", "Mysore Road", 12.9440, 77.5350),
    ("Bangalore", "Magadi Road", 12.9750, 77.5450),
    ("Bangalore", "Vijayanagar Main Road", 12.9700, 77.5300),
    ("Bangalore", "Nagarbhavi Main Road", 12.9600, 77.5030),
    ("Bangalore", "Kengeri Main Road", 12.9080, 77.4820),
    ("Bangalore", "Chord Road", 12.9970, 77.5560),
    ("Bangalore", "Sarjapur Road", 12.9096, 77.6858),

    # ── Additional coverage — famous places, connectors, gaps ──
    ("Bangalore", "Bangalore Palace Approach Road", 12.9987, 77.5920),
    ("Bangalore", "Cunningham Road", 12.9910, 77.5940),
    ("Bangalore", "Millers Road", 12.9930, 77.5900),
    ("Bangalore", "Queens Road", 12.9840, 77.5930),
    ("Bangalore", "Cauvery Road, Ulsoor", 12.9820, 77.6180),
    ("Bangalore", "Ulsoor Lake Road", 12.9810, 77.6220),
    ("Bangalore", "Assaye Road", 12.9840, 77.6150),
    ("Bangalore", "Trinity Circle Road", 12.9730, 77.6180),
    ("Bangalore", "Langford Road", 12.9560, 77.6080),
    ("Bangalore", "Hosur Road, Bommasandra", 12.8050, 77.6900),
    ("Bangalore", "Attibele Road", 12.7800, 77.7700),
    ("Bangalore", "Begur Main Road", 12.8830, 77.6300),
    ("Bangalore", "Hulimavu Main Road", 12.8850, 77.6020),
    ("Bangalore", "Bilekahalli Main Road", 12.8940, 77.5980),
    ("Bangalore", "Arekere Main Road", 12.8850, 77.5920),
    ("Bangalore", "Kanakapura Main Road, Konanakunte", 12.8790, 77.5560),
    ("Bangalore", "Vasanthapura Main Road", 12.8940, 77.5460),
    ("Bangalore", "Ideal Homes Township Road", 12.9160, 77.4970),
    ("Bangalore", "RR Nagar Main Road", 12.9250, 77.5150),
    ("Bangalore", "Bapuji Nagar Main Road", 12.9550, 77.5280),
    ("Bangalore", "Basaveshwaranagar Main Road", 12.9880, 77.5350),
    ("Bangalore", "Kamakshipalya Main Road", 12.9960, 77.5350),
    ("Bangalore", "Laggere Main Road", 13.0080, 77.5170),
    ("Bangalore", "Goraguntepalya Junction Road", 13.0230, 77.5340),
    ("Bangalore", "Byatarayanapura Main Road", 13.0680, 77.5940),
    ("Bangalore", "Jakkur Main Road", 13.0770, 77.6100),
    ("Bangalore", "Hebbagodi Main Road", 12.8130, 77.6470),
    ("Bangalore", "Chandapura Main Road", 12.8020, 77.7060),
    ("Bangalore", "Anekal Main Road", 12.7100, 77.6960),
    ("Bangalore", "Marathahalli-Sarjapur Connector", 12.9200, 77.6900),
    ("Bangalore", "Iblur Junction Road", 12.9280, 77.6810),
]

CSV_FILE = "realtime_traffic_data.csv"


def collect_data():
    if not API_KEYS:
        print("[FATAL] No TomTom API keys found in environment!")
        return

    print(f"[INFO] Using {len(API_KEYS)} API key(s) in round-robin, {len(LOCATIONS)} roads total")

    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "city", "road", "current_speed", "free_flow_speed", "confidence", "congestion_ratio"])

        for i, (city, road, lat, lon) in enumerate(LOCATIONS):
            api_key = API_KEYS[i % len(API_KEYS)]  # round-robin across keys
            url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
            params = {"key": api_key, "point": f"{lat},{lon}"}
            try:
                resp = requests.get(url, params=params, timeout=10)
                data = resp.json()
                seg = data.get("flowSegmentData", {})
                current_speed = seg.get("currentSpeed")
                free_flow_speed = seg.get("freeFlowSpeed")
                confidence = seg.get("confidence")
                congestion_ratio = None
                if current_speed is not None and free_flow_speed:
                    congestion_ratio = round(1 - (current_speed / free_flow_speed), 3)

                writer.writerow([datetime.now().isoformat(), city, road, current_speed, free_flow_speed, confidence, congestion_ratio])
                print(f"[OK] {road}: speed={current_speed}, congestion={congestion_ratio}")
            except Exception as e:
                print(f"[ERROR] {road}: {e}")

            # QPS limit safety: TomTom free tier = 5 calls/sec max
            time.sleep(0.25)


if __name__ == "__main__":
    collect_data()
