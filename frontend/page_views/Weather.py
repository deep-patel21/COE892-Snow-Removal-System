import requests
import streamlit as st

from data_layer.data_helpers import API_BASE

COORDINATES = {
    "Zone 1 — North Toronto": {"lat": 43.761, "lon": -79.411},
    "Zone 2 — West Toronto":  {"lat": 43.651, "lon": -79.495},
    "Zone 3 — East Toronto":  {"lat": 43.673, "lon": -79.298},
    "Zone 4 — Brampton":      {"lat": 43.685, "lon": -79.759},
}

@st.cache_data(ttl=600)  # Cache for 10 minutes to reduce API calls
def get_weather_data():
    results = {}

    # Assemble a dictionary of results containing data from multiple zones
    try:
        for zone, coords in COORDINATES.items():
            response = requests.get(f"{API_BASE}/road_status", params=coords)
            response.raise_for_status()
            results[zone] = response.json().get("weather", {})
    except requests.exceptions.RequestException as e:
        st.warning(f"Could not extract Weather data: {e}")
        return None
    return results


def weather_main():
    st.title(":cloud_with_rain: Weather")

    st.subheader("Current Conditions")

    weather_data = get_weather_data()
    zone_filter = st.selectbox(":world_map: Zone", list(COORDINATES.keys()))

    # Isolate the selected zone
    if weather_data:
        zone_weather = weather_data.get(zone_filter, {})
    else:
        zone_weather = {}

    # TK - replace with real data from API
    current_temperature = -5 
    current_snow_rate = 2.5 
    current_visibility = "200 m"
    current_condition = "Snowstorm"
    total_snowfall_today = "15 cm"
    current_wind_speed = "20 km/h"

    c1, c2, c3, c4, c5, c6 = st.columns([1, 1.2, 1, 1.3, 1.2, 1.1])
    c1.metric(":thermometer: Temperature", f"{zone_weather.get('temperature_c',  '—')} °C")
    c2.metric(":snowflake: Snow Depth", f"{zone_weather.get('snow_depth_cm',  '—')} cm")
    c3.metric(":fog: Visibility", f"{current_visibility}")
    c4.metric(":cloud: Condition", f"{current_condition}")
    c5.metric(":snowman: Snowfall Today", f"{total_snowfall_today}")
    c6.metric(":dash: Wind Speed", f"{zone_weather.get('wind_speed_kmh',  '—')} km/h")

    st.divider()

    