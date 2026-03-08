import requests
import streamlit as st

from concurrent.futures import ThreadPoolExecutor, as_completed

from data_layer.data_helpers import API_BASE
from data_layer.data_helpers import COORDINATES

@st.cache_data(ttl=600)  # Cache for 10 minutes to reduce API calls
def get_weather_data():
    results = {}

    def fetch_zone(zone, coords):
        response = requests.get(f"{API_BASE}/road_status", params=coords, timeout=10)
        response.raise_for_status()
        return zone, response.json().get("weather", {})
    
    # Assemble a dictionary of results containing data from multiple zones
    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(fetch_zone, zone, coords): zone
                      for zone, coords in COORDINATES.items()}
            for future in as_completed(futures):
                zone, weather = future.result()
                results[zone] = weather
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

    c1, c2, c3, c4 = st.columns([1, 1.2, 1.3, 1])
    c1.metric(":thermometer: Temperature", f"{zone_weather.get('temperature_c',  '—')} °C")
    c2.metric(":snowflake: Snow Depth", f"{zone_weather.get('snow_depth_mm',  '—')} mm")
    c3.metric(":snowman: Snowfall Today", f"{zone_weather.get('day_snowfall_mm', '—')}")
    c4.metric(":dash: Wind Speed", f"{zone_weather.get('wind_speed_kmh',  '—')} km/h")
    st.caption(f"Data queried from Station: {zone_weather.get('station_name', 'Unknown')}")

    st.divider()

