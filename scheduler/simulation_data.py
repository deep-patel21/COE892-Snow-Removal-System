
# Simulating values from peak winter time. Project demonstration may not align with active snow conditions
def get_conditions_mock():
    return {
        "Zone 1 — North Toronto": {
            "road_type": "HIGHWAY",
            "dispatch_priority": "High",
            "traffic_speed_kmh": 12.0,
            "weather": {"temperature_c": -9.0, "wind_speed_kmh": 45.0, "snow_depth_mm": 310.0}
        },
        "Zone 2 — West Toronto": {
            "road_type": "MAIN_STREET",
            "dispatch_priority": "High",
            "traffic_speed_kmh": 18.0,
            "weather": {"temperature_c": -7.0, "wind_speed_kmh": 35.0, "snow_depth_mm": 250.0}
        },
        "Zone 3 — East Toronto": {
            "road_type": "MAIN_STREET",
            "dispatch_priority": "Medium",
            "traffic_speed_kmh": 30.0,
            "weather": {"temperature_c": -4.0, "wind_speed_kmh": 20.0, "snow_depth_mm": 160.0}
        },
        "Zone 4 — Brampton": {
            "road_type": "RESIDENTIAL",
            "dispatch_priority": "Medium",
            "traffic_speed_kmh": 25.0,
            "weather": {"temperature_c": -3.0, "wind_speed_kmh": 18.0, "snow_depth_mm": 120.0}
        },
        "Zone 5 — Etobicoke": {
            "road_type": "HIGHWAY",
            "dispatch_priority": "High",
            "traffic_speed_kmh": 10.0,
            "weather": {"temperature_c": -8.0, "wind_speed_kmh": 40.0, "snow_depth_mm": 290.0}
        },
        "Zone 6 — Scarborough": {
            "road_type": "MAIN_STREET",
            "dispatch_priority": "Low",
            "traffic_speed_kmh": 38.0,
            "weather": {"temperature_c": -2.0, "wind_speed_kmh": 12.0, "snow_depth_mm": 60.0}
        },
        "Zone 7 — Richmond Hill": {
            "road_type": "RESIDENTIAL",
            "dispatch_priority": "Low",
            "traffic_speed_kmh": 44.0,
            "weather": {"temperature_c": -1.0, "wind_speed_kmh": 8.0, "snow_depth_mm": 35.0}
        },
        "Zone 8 — Mississauga": {
            "road_type": "HIGHWAY",
            "dispatch_priority": "Medium",
            "traffic_speed_kmh": 32.0,
            "weather": {"temperature_c": -3.0, "wind_speed_kmh": 22.0, "snow_depth_mm": 130.0}
        },
        "Zone 9 — Markham": {
            "road_type": "RESIDENTIAL",
            "dispatch_priority": "Clear",
            "traffic_speed_kmh": 58.0,
            "weather": {"temperature_c": 1.0, "wind_speed_kmh": 5.0, "snow_depth_mm": 0.0}
        },
        "Zone 10 — Vaughan": {
            "road_type": "RESIDENTIAL",
            "dispatch_priority": "Clear",
            "traffic_speed_kmh": 55.0,
            "weather": {"temperature_c": 2.0, "wind_speed_kmh": 4.0, "snow_depth_mm": 0.0}
        },
    }