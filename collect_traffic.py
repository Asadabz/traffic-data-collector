import requests
import csv
import os
from datetime import datetime

API_KEY = "URjkRkh3LnTXcHcSne3PkjpAzIXY5p81"

# City, Road Name, Latitude, Longitude
LOCATIONS = [
    # ── Bangalore ──────────────────────────────
    ("Bangalore", "MG Road", 12.9758, 77.6045),
    ("Bangalore", "Brigade Road", 12.9716, 77.6069),
    ("Bangalore", "Commercial Street", 12.9822, 77.6086),
    ("Bangalore", "Residency Road", 12.9698, 77.6047),
    ("Bangalore", "100 Feet Road, Indiranagar", 12.9784, 77.6408),
    ("Bangalore", "CMH Road", 12.9789, 77.6394),
    ("Bangalore", "80 Feet Road, Koramangala", 12.9352, 77.6146),
    ("Bangalore", "Old Airport Road", 12.9611, 77.6497),
    ("Bangalore", "Bannerghatta Road", 12.9082, 77.5972),
    ("Bangalore", "Outer Ring Road, Marathahalli", 12.9569, 77.6974),
    ("Bangalore", "Silk Board Junction", 12.9172, 77.6228),
    ("Bangalore", "Hosur Road", 12.9345, 77.6100),
    ("Bangalore", "Whitefield Main Road", 12.9698, 77.7500),
    ("Bangalore", "Sarjapur Road", 12.9096, 77.6858),
    ("Bangalore", "Tumkur Road", 13.0280, 77.5350),
    ("Bangalore", "Mysore Road", 12.9440, 77.5350),
    ("Bangalore", "Hebbal Flyover", 13.0358, 77.5970),
    ("Bangalore", "Yeshwanthpur Circle", 13.0284, 77.5540),
    ("Bangalore", "Jayanagar 4th Block", 12.9308, 77.5838),
    ("Bangalore", "JP Nagar", 12.9077, 77.5850),

    # ── Mumbai ──────────────────────────────────
    ("Mumbai", "Marine Drive", 18.9440, 72.8237),
    ("Mumbai", "Linking Road, Bandra", 19.0596, 72.8295),
    ("Mumbai", "Western Express Highway, Andheri", 19.1197, 72.8464),
    ("Mumbai", "Eastern Express Highway, Sion", 19.0821, 72.8949),
    ("Mumbai", "SV Road", 19.0728, 72.8380),
    ("Mumbai", "LBS Marg", 19.0783, 72.8913),
    ("Mumbai", "Peddar Road", 18.9701, 72.8090),
    ("Mumbai", "Dadar TT Circle", 19.0178, 72.8478),
    ("Mumbai", "Andheri-Kurla Road", 19.1075, 72.8790),
    ("Mumbai", "Sion-Panvel Highway", 19.0450, 73.0050),
    ("Mumbai", "Worli Sea Link Approach", 19.0176, 72.8177),
    ("Mumbai", "Chembur-Sion Road", 19.0522, 72.8994),
    ("Mumbai", "Ghodbunder Road, Thane", 19.2450, 72.9780),
    ("Mumbai", "Juhu Tara Road", 19.1075, 72.8263),
    ("Mumbai", "Malad Link Road", 19.1868, 72.8412),
    ("Mumbai", "Goregaon-Mulund Link Road", 19.1663, 72.9101),
    ("Mumbai", "Ghatkopar-Mankhurd Link Road", 19.0800, 72.9150),
    ("Mumbai", "CST Road, Kalina", 19.0725, 72.8580),
    ("Mumbai", "Kalanagar Junction, Bandra", 19.0650, 72.8365),
    ("Mumbai", "Vashi Bridge", 19.0770, 72.9990),
]
CSV_FILE = "realtime_traffic_data.csv"

def collect_data():
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "city", "road", "current_speed", "free_flow_speed", "confidence", "congestion_ratio"])

        for city, road, lat, lon in LOCATIONS:
            url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
            params = {"key": API_KEY, "point": f"{lat},{lon}"}
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
                print(f"[OK] {city} - {road}: speed={current_speed}, free_flow={free_flow_speed}, congestion={congestion_ratio}")
            except Exception as e:
                print(f"[ERROR] {city} - {road}: {e}")

if __name__ == "__main__":
    collect_data()