from fastapi import FastAPI, HTTPException
import data_utilities as utils

app = FastAPI(title="Snow Removal Extraction Module")

# Geographic Bounding Box Validation
TORONTO_BOUNDS = {
    "lat_min": 43.58, "lat_max": 43.85,
    "lon_min": -79.63, "lon_max": -79.12
}

@app.get("/api/v1/road_status")
def get_road_status(lat: float, lon: float):
    """
    Coordinates data extraction and returns a structured payload 
    ready for gRPC serialization.
    """
    # Enforce geographic constraints to prevent wasted API calls
    if not (TORONTO_BOUNDS["lat_min"] <= lat <= TORONTO_BOUNDS["lat_max"]) or \
       not (TORONTO_BOUNDS["lon_min"] <= lon <= TORONTO_BOUNDS["lon_max"]):
        raise HTTPException(status_code=400, detail="Coordinates outside designated zone.")

    # 1. Gather Data 
    traffic = utils.fetch_traffic_data(lat, lon)
    weather = utils.fetch_weather_data(lat, lon)
    
    # 2. Process Business Logic
    road_type, priority = utils.calculate_priority(
        traffic["frc"], 
        weather["snow_depth_cm"]
    )
    
    # 3. Construct Final Payload (Maps directly to your Protobuf message)
    payload = {
        "road_type": road_type,
        "dispatch_priority": priority,
        "traffic_speed_kmh": traffic["current_speed"],
        "weather": {
            "temperature_c": weather["temperature_c"],
            "wind_speed_kmh": weather["wind_speed_kmh"],
            "snow_depth_cm": weather["snow_depth_cm"]
        }
    }
    
    return payload

# Run via terminal: uvicorn data_extraction:app --reload