import requests
import streamlit as st
import pandas as pd
import plotly.express as px

from concurrent.futures import ThreadPoolExecutor, as_completed

from data_layer.data_helpers import API_BASE
from data_layer.data_helpers import COORDINATES

from scheduler.scheduler import get_conditions
from scheduler.simulation_data import get_conditions_mock

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


@st.cache_data(ttl=120)
def get_zone_conditions():
    try:    
        # return get_conditions()        
        return get_conditions_mock()  # Uncomment to use mock data from peak winter season
    except Exception as e:
        st.error(f"gPRC Service Error. Zone Conditions data unavailable: {e}")
        return {}


def generate_graphs(weather_data, zone_conditions):
    if weather_data:
        st.title("Weather Analytics")
        st.subheader("Weather Conditions")
        rows = [] 
        for zone, data in weather_data.items():
            rows.append({
                "Zone": zone.split("-")[-1].strip(),
                "Temperature (°C)": data.get("temperature_c", 0),
                "Snow Depth (mm)": data.get("snow_depth_mm", 0),
                "Wind Speed (km/h)": data.get("wind_speed_kmh", 0),
            })

        chart_df = pd.DataFrame(rows).sort_values("Zone")  # Sorts zone values in alphabetical order

        fig1 = px.line(
            chart_df, x="Zone", y="Temperature (°C)",
            markers=True, title="Zone Temperatures",
            color_discrete_sequence=["#f97316"],
        )
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="white", height=400,
            margin=dict(t=40, b=20, l=20, r=20),
        )
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.line(
            chart_df, x="Zone", y=["Snow Depth (mm)", "Wind Speed (km/h)"],
            markers=True, title="Zone Snow Depth and Wind Speeds",
            color_discrete_map={
                "Snow Depth (mm)":   "#60a5fa",
                "Wind Speed (km/h)": "#a78bfa",
            }
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="white", height=400,
            margin=dict(t=40, b=20, l=20, r=20),
            legend=dict(orientation="h", y=1.1, title=""),
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    if zone_conditions:
        st.subheader("Road Class Conditions")
        road_snow = {}
        for zone, cond in zone_conditions.items():
            road_type = cond.get("road_type", "Unknown")
            snow = weather_data.get(zone, {}).get("snow_depth_mm", 0) or 0
            if road_type not in road_snow:
                road_snow[road_type] = []
            road_snow[road_type].append(snow)

        road_df = pd.DataFrame([
            {"Road Type": rt, "Avg Snow Depth (mm)": sum(vals) / len(vals)}
            for rt, vals in road_snow.items()
        ]).sort_values("Avg Snow Depth (mm)", ascending=False)

        fig = px.pie(
            road_df,
            names="Road Type",
            values="Avg Snow Depth (mm)",
            title="Average Snow Depth by Road Type",
            color="Road Type",
            color_discrete_map={
                "HIGHWAY":     "#ef4444",
                "MAIN_STREET": "#facc15",
                "RESIDENTIAL": "#60a5fa",
            }
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            height=400,
            margin=dict(t=40, b=20, l=20, r=20),
        )
        st.plotly_chart(fig, use_container_width=True)


def weather_main():
    st.title(":cloud_with_rain: Weather")

    st.subheader("Current Conditions")

    weather_data = get_weather_data()
    zone_conditions = get_zone_conditions()

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

    generate_graphs(weather_data, zone_conditions)

