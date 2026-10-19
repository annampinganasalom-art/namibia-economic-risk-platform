import json
from datetime import datetime
import pandas as pd
import requests

# 1. Define Key Namibian Economic Regions & Coordinates
NAMIBIA_NODES = {
    "Windhoek": {
        "region": "Khomas",
        "sector": "Banking & Services",
        "lat": -22.5609,
        "lon": 17.0836,
    },
    "Walvis Bay": {
        "region": "Erongo",
        "sector": "Logistics & Shipping",
        "lat": -22.9575,
        "lon": 14.5053,
    },
    "Rundu": {
        "region": "Kavango East",
        "sector": "Agriculture & Farming",
        "lat": -17.9333,
        "lon": 19.7667,
    },
    "Keetmanshoop": {
        "region": " //Kharas",
        "sector": "Mining & Energy",
        "lat": -26.5833,
        "lon": 18.1333,
    },
}

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_node_climate_data(node_name, node_info):
    """Fetches real-time weather indicators from Open-Meteo API."""
    params = {
        "latitude": node_info["lat"],
        "longitude": node_info["lon"],
        "current": ["temperature_2m", "relative_humidity_2m", "precipitation"],
        "daily": ["precipitation_sum", "temperature_2m_max"],
        "timezone": "auto",
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract real-time metrics and construct payload[cite: 1]
        current_data = data.get("current", {})
        payload = {
            "node": node_name,
            "region": node_info["region"],
            "primary_sector": node_info["sector"],
            "timestamp": datetime.now().isoformat(),
            "temperature_celsius": current_data.get("temperature_2m"),
            "humidity_percent": current_data.get("relative_humidity_2m"),
            "precipitation_mm": current_data.get("precipitation"),
        }
        return payload

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {node_name}: {e}")
        return None


def main():
    print("--- Starting Ingestion for Namibia Economic Nodes ---")
    collected_records = []

    for node_name, info in NAMIBIA_NODES.items():
        record = fetch_node_climate_data(node_name, info)
        if record:
            collected_records.append(record)
            print(
                f"[SUCCESS] Ingested data for {node_name} ({info['sector']})"
            )

    # Convert to pandas DataFrame for processing[cite: 1]
    df = pd.DataFrame(collected_records)
    print("\nProcessed DataFrame:")
    print(df.to_string())

    # Save initial raw JSON payload[cite: 1]
    with open("raw_namibia_ingestion.json", "w") as f:
        json.dump(collected_records, f, indent=4)
    print("\nSaved raw JSON stream to 'raw_namibia_ingestion.json'")


if __name__ == "__main__":
    main()