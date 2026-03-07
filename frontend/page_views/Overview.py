import streamlit as st

def overview_main():
    st.title(":bar_chart: Overview")

    c1, c2, c3, c4 = st.columns(4)

    #TK - replace with real data from API
    active_vehicles = 15
    total_vehicles = 20
    current_snowfall = 2.5
    completed_routes = 8
    total_routes = 10
    avg_response_time = 12

    c1.metric(":truck: Active Vehicles", f"{active_vehicles} / {total_vehicles}")
    c2.metric(":snowflake: Current Snowfall", f"{current_snowfall} cm/hr")
    c3.metric(":white_check_mark: Routes", f"{completed_routes} / {total_routes}")
    c4.metric(":alarm_clock: Avg. Response Time", f"{avg_response_time} min")

    st.divider()

