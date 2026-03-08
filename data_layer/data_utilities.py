import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Hardcoded for development; move to environment variables for production.
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
    """Extracts live environmental variables from MSC GeoMet."""
    url = f"https://api.weather.gc.ca/collections/swob-realtime/items?lat={lat}&lon={lon}&f=json&limit=1"
    
    try:
        response = requests.get(url, timeout=5).json()
        features = response.get("features", [])
        
        if features:
            props = features[0].get("properties", {})
            return {
                "temperature_c": props.get("air_temp", 0.0),
                "wind_speed_kmh": props.get("wind_spd", 0.0),
                "snow_depth_cm": props.get("snw_dpth", 0.0)
            }
    except requests.RequestException:
        pass
    
    return {"temperature_c": 0.0, "wind_speed_kmh": 0.0, "snow_depth_cm": 0.0}

def calculate_priority(frc: str, snow_depth: float) -> tuple[str, str]:
    """Translates raw API data into Scheduler priorities."""
    if frc in ["FRC0", "FRC1", "FRC2"]:
        road_type = "HIGHWAY"
    elif frc in ["FRC3", "FRC4"]:
        road_type = "MAIN_STREET"
    else:
        road_type = "RESIDENTIAL"
        
    if snow_depth > 5.0 and road_type == "HIGHWAY":
        priority = "CRITICAL"
    elif snow_depth > 2.0:
        priority = "HIGH"
    else:
        priority = "NORMAL"
        
    return road_type, priority