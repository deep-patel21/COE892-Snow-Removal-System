import pandas as pd
import streamlit as st
import pydeck
import plotly.express as px
from functools import partial

from data_layer.data_helpers import search_matches


VEHICLES = ["Highway Plow", "Road Plow", "Pickup Truck Plow", "Salting Truck"]
VEHICLE_STATUS = ["Idle", "En Route", "Active", "Cancelled", "Under Maintenance"]
ZONES = ["Zone 1 — North Toronto", "Zone 2 — West Toronto", "Zone 3 — East Toronto", "Zone 4 — Brampton"]
COORDINATES = {
    "Zone 1 — North Toronto": {"lat": 43.761, "lon": -79.411},
    "Zone 2 — West Toronto":  {"lat": 43.651, "lon": -79.495},
    "Zone 3 — East Toronto":  {"lat": 43.673, "lon": -79.298},
    "Zone 4 — Brampton":      {"lat": 43.685, "lon": -79.759},
}


# TK - move sample vehicle fleet data into a database or dedicated file atleast
def get_fleet_data():
    """Fleet status — would be fed by vehicle management module."""
    return pd.DataFrame([
        {"ID": "SRS-01", "Type": "Highway Plow",      "Status": "Active",            "Zone": "Zone 3 — East Toronto",  "Route": "Hwy 401 E",      "Fuel (%)": 74},
        {"ID": "SRS-02", "Type": "Highway Plow",      "Status": "En Route",          "Zone": "Zone 1 — North Toronto", "Route": "Sheppard Ave",   "Fuel (%)": 91},
        {"ID": "SRS-03", "Type": "Highway Plow",      "Status": "Idle",              "Zone": "Zone 2 — West Toronto",  "Route": "—",              "Fuel (%)": 100},
        {"ID": "SRS-04", "Type": "Highway Plow",      "Status": "Idle",              "Zone": "Zone 2 — West Toronto",  "Route": "—",              "Fuel (%)": 82},
        {"ID": "SRS-05", "Type": "Road Plow",         "Status": "Active",            "Zone": "Zone 2 — West Toronto",  "Route": "Bloor St W",     "Fuel (%)": 55},
        {"ID": "SRS-06", "Type": "Road Plow",         "Status": "Active",            "Zone": "Zone 3 — East Toronto",  "Route": "Bloor St E",     "Fuel (%)": 61},
        {"ID": "SRS-07", "Type": "Road Plow",         "Status": "Active",            "Zone": "Zone 1 — North Toronto", "Route": "Yonge St N",     "Fuel (%)": 67},
        {"ID": "SRS-08", "Type": "Road Plow",         "Status": "En Route",          "Zone": "Zone 2 — West Toronto",  "Route": "Eglinton Ave W", "Fuel (%)": 88},
        {"ID": "SRS-09", "Type": "Road Plow",         "Status": "Under Maintenance", "Zone": "Zone 1 — North Toronto", "Route": "—",              "Fuel (%)": 100},
        {"ID": "SRS-10", "Type": "Road Plow",         "Status": "Idle",              "Zone": "Zone 4 — Brampton",      "Route": "—",              "Fuel (%)": 98},
        {"ID": "SRS-11", "Type": "Road Plow",         "Status": "Active",            "Zone": "Zone 1 — North Toronto", "Route": "Finch Ave",      "Fuel (%)": 72},
        {"ID": "SRS-12", "Type": "Road Plow",         "Status": "Active",            "Zone": "Zone 3 — East Toronto",  "Route": "Danforth Ave",   "Fuel (%)": 50},
        {"ID": "SRS-13", "Type": "Pickup Truck Plow", "Status": "Active",            "Zone": "Zone 4 — Brampton",      "Route": "Bovaird Dr",     "Fuel (%)": 60},
        {"ID": "SRS-14", "Type": "Pickup Truck Plow", "Status": "Cancelled",         "Zone": "Zone 4 — Brampton",      "Route": "—",              "Fuel (%)": 58},
        {"ID": "SRS-15", "Type": "Pickup Truck Plow", "Status": "En Route",          "Zone": "Zone 3 — East Toronto",  "Route": "Kingston Rd",    "Fuel (%)": 85},
        {"ID": "SRS-16", "Type": "Pickup Truck Plow", "Status": "Idle",              "Zone": "Zone 2 — West Toronto",  "Route": "—",              "Fuel (%)": 95},
        {"ID": "SRS-17", "Type": "Pickup Truck Plow", "Status": "Active",            "Zone": "Zone 2 — West Toronto",  "Route": "Kipling Ave",    "Fuel (%)": 44},
        {"ID": "SRS-18", "Type": "Salting Truck",     "Status": "Active",            "Zone": "Zone 1 — North Toronto", "Route": "Wilson Ave",     "Fuel (%)": 53},
        {"ID": "SRS-19", "Type": "Salting Truck",     "Status": "En Route",          "Zone": "Zone 4 — Brampton",      "Route": "Hwy 410",        "Fuel (%)": 78},
        {"ID": "SRS-20", "Type": "Salting Truck",     "Status": "Idle",              "Zone": "Zone 3 — East Toronto",  "Route": "—",              "Fuel (%)": 90},
    ])


def generate_summary(vehicles_data):
    total_vehicles = len(vehicles_data)
    active_vehicles = len(vehicles_data[vehicles_data["Status"] == "Active"])
    en_route_vehicles = len(vehicles_data[vehicles_data["Status"] == "En Route"])
    idle_vehicles = len(vehicles_data[vehicles_data["Status"] == "Idle"])
    cancelled_vehicles = len(vehicles_data[vehicles_data["Status"] == "Cancelled"])
    under_maintenance_vehicles = len(vehicles_data[vehicles_data["Status"] == "Under Maintenance"])

    st.subheader("Fleet Summary")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Active", f"{active_vehicles}")
    c2.metric("En Route", f"{en_route_vehicles}")
    c3.metric("Idle", f"{idle_vehicles}")
    c4.metric("Cancelled", f"{cancelled_vehicles}")
    c5.metric("Under Maintenance", f"{under_maintenance_vehicles}")
    c6.metric("Total Vehicles", f"{total_vehicles}")


def generate_graphs(vehicles_data):
    st.subheader("Fleet Analytics")
    c1, c2 = st.columns(2)

    # Pie chart showing distribution of vehicle status
    with c1:
        status_counts = vehicles_data["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]

        fig = px.pie(
            status_counts,
            names="Status",
            values="Count",
            title="Vehicle Status",
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            height=500,
            margin=dict(t=40, b=20, l=20, r=20),
        )

        st.plotly_chart(fig, use_container_width=True)
    # Geographical map showing counts of operational vehicles in each zone
    with c2:
        operating_vehicles = vehicles_data[vehicles_data["Status"].isin(["Active", "En Route"])]
        zone_counts = operating_vehicles.groupby("Zone").size().reset_index(name="Count")

        zone_counts["lat"] = zone_counts["Zone"].map(lambda z: COORDINATES[z]["lat"])
        zone_counts["lon"] = zone_counts["Zone"].map(lambda z: COORDINATES[z]["lon"])

        layer = pydeck.Layer(
            "ScatterplotLayer",
            data=zone_counts,
            get_position='[lon, lat]',
            get_radius=2000,
            get_fill_color=[100, 180, 255, 160],
            pickable=True,
        )

        text_layer = pydeck.Layer(
            "TextLayer",
            data=zone_counts,
            get_position='[lon, lat]',
            get_text="Count",
            get_size=28,
            get_color=[255, 255, 255],
            get_alignment_baseline="'bottom'",
        )

        view = pydeck.ViewState(latitude=43.69, longitude=-79.5, zoom=9.5)

        st.pydeck_chart(pydeck.Deck(
            layers=[layer, text_layer],
            initial_view_state=view,
            tooltip={"text": "{Zone}\nOperational: {Count}"}
        ))


def color_status(val):
    if val == "Active":
        return "color: #34d399"     # Green
    if val == "Idle":
        return "color: #94a3b8"     # Grey
    if val == "En Route":
        return "color: #facc15"     # Yellow
    if val == "Under Maintenance":
        return "color: #f97316"     # Orange
    if val == "Cancelled":
        return "color: #ef4444"     # Red

    return ""


def vehicles_main():
    st.title(":truck: Vehicles")
    vehicles_data = get_fleet_data()

    generate_summary(vehicles_data)
    st.divider()

    st.subheader("Fleet Filtering")
    search_query = st.text_input(":mag: Search", placeholder="Search by ID, type, route...")

    st.caption("or")

    c7, c8, c9 = st.columns([1, 1, 2])
    with c7:
        vehicle_filter = st.selectbox(":articulated_lorry: Vehicle Type", ["All", *VEHICLES])
    with c8:
        status_filter = st.selectbox(":compass: Status", ["All", *VEHICLE_STATUS])
    with c9:
        zone_filter = st.selectbox(":world_map: Assigned Zone", ["All", *ZONES])

    fleet_df = vehicles_data.copy()

    if search_query:
        # Filter data based on search query
        matches = partial(search_matches, query=search_query)
        search_mask = fleet_df.apply(matches, axis=1)
        fleet_df = fleet_df[search_mask]

    # Filter data based on vehicle, status, or zone
    if vehicle_filter != "All":
        fleet_df = fleet_df[fleet_df["Type"] == vehicle_filter]
    if status_filter != "All":
        fleet_df = fleet_df[fleet_df["Status"] == status_filter]
    if zone_filter != "All":
        fleet_df = fleet_df[fleet_df["Zone"] == zone_filter]

    fleet_df_styled = fleet_df.style.applymap(color_status, subset=["Status"])
    st.dataframe(fleet_df_styled, use_container_width=True, hide_index=True, height=460)

    generate_graphs(vehicles_data)
