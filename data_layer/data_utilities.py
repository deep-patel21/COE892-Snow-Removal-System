import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOMTOM_KEY = os.getenv("API_KEY")

def fetch_traffic_data(lat: float, lon: float) -> dict:
    """Extracts traffic density and road classification from TomTom."""

    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&key={TOMTOM_KEY}"

    try:
        response = requests.get(url, timeout=5).json()
        flow_data = response.get("flowSegmentData", {})

        return {
            "frc": flow_data.get("frc", "FRC6"),
            "current_speed": flow_data.get("currentSpeed", 0)
        }
    except requests.RequestException:
        # Fallback for network failures in a distributed system
        return {"frc": "FRC6", "current_speed": 0}


def fetch_weather_data(lat: float, lon: float) -> dict:
    """Extracts localized environmental variables using a dynamic bounding box."""

    # Define a localized radius around the coordinates to capture nearby weather stations
    # This creates a tight 10x10km net around the specific road segment
    delta = 0.3
    bbox = f"{lon - delta},{lat - delta},{lon + delta},{lat + delta}"
    url = f"https://api.weather.gc.ca/collections/swob-realtime/items?bbox={bbox}&f=json&limit=1"

    try:
        response = requests.get(url, timeout=5).json()
        features = response.get("features", [])

        if features:
            props = features[0].get("properties", {})
            return {
                "temperature_c": props.get("air_temp", 0.0),
                "wind_speed_kmh": props.get("avg_wnd_spd_10m_pst2mts", 0.0),
                "snow_depth_mm": props.get("snw_dpth", 0.0),
                "day_snowfall_mm": props.get("pcpn_amt_pst24hrs", 0.0),
                "station": props.get("stn_nam-value", "Unknown")
            }
    except requests.RequestException:
        print(f"Warning: MSC GeoMet connection failed for zone {bbox}.")

    # Failsafe ensures the system continues operating if a local sensor is offline
    return {"temperature_c": 0.0, "wind_speed_kmh": 0.0, "snow_depth_cm": 0.0}


def calculate_road_type(frc: str) -> tuple[str, str]:
    """Translates raw API data into road types."""

    if frc in ["FRC0", "FRC1", "FRC2"]:
        road_type = "HIGHWAY"
    elif frc in ["FRC3", "FRC4"]:
        road_type = "MAIN_STREET"
    else:
        road_type = "RESIDENTIAL"

    return road_type