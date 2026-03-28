import pandas as pd
import streamlit as st
import pydeck
import plotly.express as px
from functools import partial

from data_layer.data_helpers import search_matches
from data_layer.data_helpers import COORDINATES

from scheduler.scheduler import get_fleet_data
from scheduler.scheduler import get_conditions
from scheduler.simulation_data import get_conditions_mock


VEHICLES = ["Highway Plow", "Road Plow", "Pickup Truck Plow", "Salting Truck"]
VEHICLE_STATUS = ["Idle", "En Route", "Active", "Cancelled", "Under Maintenance"]
ZONES = [
    "Zone 1 — North Toronto", "Zone 2 — West Toronto",
    "Zone 3 — East Toronto",  "Zone 4 — Brampton",
    "Zone 5 — Etobicoke",     "Zone 6 — Scarborough",
    "Zone 7 — Richmond Hill", "Zone 8 — Mississauga",
    "Zone 9 — Markham",       "Zone 10 — Vaughan",
]


def get_vehicles_data():
    try:
        return get_fleet_data()
    except Exception as e:
        st.error(f"Fleet data unavailable: {e}")
        return pd.DataFrame(columns=["ID", "Type", "Status", "Zone"])


@st.cache_data(ttl=120)
def get_zone_conditions():
    try:    
        # return get_conditions() 
        return get_conditions_mock()      # Uncomment to use mock data from peak winter season
    except Exception as e:
        st.error(f"gPRC Service Error. Zone Conditions data unavailable: {e}")
        return {}


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

def priority_icon(zone, zone_conditions):
    # Emoji icons are not ideal but necessary here, as Streamlit shortcodes are not supported
    # in dataframes
    priority_icons = {
        "High":   "🔴",
        "Medium": "🟠",
        "Low":    "🟡",
        "Clear":  "🟢",
    }

    priority = zone_conditions.get(zone, {}).get("dispatch_priority", "")
    return priority_icons.get(priority, "-")


def vehicles_main():
    st.title(":truck: Vehicles")
    vehicles_data = get_vehicles_data()
    zone_conditions = get_zone_conditions()

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
    priority_icons = {
        "High": ":red_circle:",
        "Medium": ":orange_circle:",
        "Low": ":yellow_circle:",
        "Clear": ":green_circle:",
    }

    if zone_conditions:
        fleet_df["Dispatch Priority"] = fleet_df["Zone"].map(lambda z: priority_icon(z, zone_conditions))

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
