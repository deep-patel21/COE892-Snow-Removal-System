import streamlit as st

def weather_main():
    st.title(":cloud_with_rain: Weather")

    st.subheader("Current Conditions")
    c1, c2, c3, c4, c5, c6 = st.columns([1, 1.2, 1, 1.3, 1.2, 1.1])

    # TK - replace with real data from API
    current_temperature = -5 
    current_snow_rate = 2.5 
    current_visibility = "200 m"
    current_condition = "Snowstorm"
    total_snowfall_today = "15 cm"
    current_wind_speed = "20 km/h"

    c1.metric(":thermometer: Temperature", f"{current_temperature} °C")
    c2.metric(":snowflake: Snow Rate", f"{current_snow_rate} cm/hr")
    c3.metric(":fog: Visibility", current_visibility)
    c4.metric(":cloud: Condition", current_condition)
    c5.metric(":snowman: Snowfall Today", total_snowfall_today)
    c6.metric(":dash: Wind Speed", current_wind_speed)

    st.divider()