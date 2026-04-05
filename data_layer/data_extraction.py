from fastapi import FastAPI, HTTPException
import data_utilities as utils

app = FastAPI(title="Snow Removal Extraction Module")

#gta boundary
BOUNDS = {
    "lat_min": 43.50,
    "lat_max": 44.00,
    "lon_min": -79.85,
    "lon_max": -79.12  
}

@app.get("/api/v1/road_status")
def get_road_status(lat: float, lon: float):
    """
    Coordinates data extraction and returns a structured payload 
    ready for gRPC serialization.
    """
    
    # Enforce geographic constraints to prevent wasted API calls
    if not (BOUNDS["lat_min"] <= lat <= BOUNDS["lat_max"]) or \
       not (BOUNDS["lon_min"] <= lon <= BOUNDS["lon_max"]):
        raise HTTPException(status_code=400, detail="Coordinates outside designated zone.")
    
    traffic = utils.fetch_traffic_data(lat, lon)
    weather = utils.fetch_weather_data(lat, lon)
    
    #frc means functional roade class
    road_type = utils.calculate_road_type(traffic["frc"])
    priority = utils.calculate_priority_level(weather["snow_depth_mm"])
    
    #construct the payload using the data provided by the utils file
    payload = {
        "road_type": road_type,
        "dispatch_priority": priority,
        "traffic_speed_kmh": traffic["current_speed"],
        "weather": {
            "station_name": weather["station"],
            "temperature_c": weather["temperature_c"],
            "wind_speed_kmh": weather["wind_speed_kmh"],
            "snow_depth_mm": weather["snow_depth_mm"],
            "day_snowfall_mm": weather["day_snowfall_mm"]
        }
    }
    
    return payload