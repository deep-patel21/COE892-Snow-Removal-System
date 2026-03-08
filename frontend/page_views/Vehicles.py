import pandas as pd
import streamlit as st
from functools import partial

from data_layer.data_utilities import search_matches


VEHICLES = ["Highway Plow", "Road Plow", "Pickup Truck Plow", "Salting Truck"]
VEHICLE_STATUS = ["Idle", "En Route", "Active", "Cancelled", "Under Maintenance"]
ZONES = ["Zone 1 — North Toronto", "Zone 2 — West Toronto", "Zone 3 — East Toronto", "Zone 4 — Brampton"]

# TK - move sample vehicle fleet data into a database or dedicated file atleast
def get_fleet_data():
    """Fleet status — would be fed by vehicle management module."""
    return pd.DataFrame([
        {"ID": "SRS-01", "Type": "Highway Plow",      "Status": "Active",            "Zone": "Zone 3 — East Toronto",  "Route": "Hwy 401 E",      "Fuel (%)": 74,  "km Today": 41},
        {"ID": "SRS-02", "Type": "Highway Plow",      "Status": "En Route",          "Zone": "Zone 1 — North Toronto", "Route": "Sheppard Ave",   "Fuel (%)": 91,  "km Today": 12},
        {"ID": "SRS-03", "Type": "Highway Plow",      "Status": "Idle",              "Zone": "Zone 2 — West Toronto",  "Route": "—",              "Fuel (%)": 100, "km Today": 0 },
        {"ID": "SRS-04", "Type": "Highway Plow",      "Status": "Idle",              "Zone": "Zone 2 — West Toronto",  "Route": "—",              "Fuel (%)": 82,  "km Today": 34},
        {"ID": "SRS-05", "Type": "Road Plow",         "Status": "Active",            "Zone": "Zone 2 — West Toronto",  "Route": "Bloor St W",     "Fuel (%)": 55,  "km Today": 28},
        {"ID": "SRS-06", "Type": "Road Plow",         "Status": "Active",            "Zone": "Zone 3 — East Toronto",  "Route": "Bloor St E",     "Fuel (%)": 61,  "km Today": 25},
        {"ID": "SRS-07", "Type": "Road Plow",         "Status": "Active",            "Zone": "Zone 1 — North Toronto", "Route": "Yonge St N",     "Fuel (%)": 67,  "km Today": 22},
        {"ID": "SRS-08", "Type": "Road Plow",         "Status": "En Route",          "Zone": "Zone 2 — West Toronto",  "Route": "Eglinton Ave W", "Fuel (%)": 88,  "km Today": 5 },
        {"ID": "SRS-09", "Type": "Road Plow",         "Status": "Under Maintenance", "Zone": "Zone 1 — North Toronto", "Route": "—",              "Fuel (%)": 100, "km Today": 0 },
        {"ID": "SRS-10", "Type": "Road Plow",         "Status": "Idle",              "Zone": "Zone 4 — Brampton",      "Route": "—",              "Fuel (%)": 98,  "km Today": 0 },
        {"ID": "SRS-11", "Type": "Road Plow",         "Status": "Active",            "Zone": "Zone 1 — North Toronto", "Route": "Finch Ave",      "Fuel (%)": 72,  "km Today": 18},
        {"ID": "SRS-12", "Type": "Road Plow",         "Status": "Active",            "Zone": "Zone 3 — East Toronto",  "Route": "Danforth Ave",   "Fuel (%)": 50,  "km Today": 35},
        {"ID": "SRS-13", "Type": "Pickup Truck Plow", "Status": "Active",            "Zone": "Zone 4 — Brampton",      "Route": "Bovaird Dr",     "Fuel (%)": 60,  "km Today": 14},
        {"ID": "SRS-14", "Type": "Pickup Truck Plow", "Status": "Cancelled",         "Zone": "Zone 4 — Brampton",      "Route": "—",              "Fuel (%)": 58,  "km Today": 16},
        {"ID": "SRS-15", "Type": "Pickup Truck Plow", "Status": "En Route",          "Zone": "Zone 3 — East Toronto",  "Route": "Kingston Rd",    "Fuel (%)": 85,  "km Today": 7 },
        {"ID": "SRS-16", "Type": "Pickup Truck Plow", "Status": "Idle",              "Zone": "Zone 2 — West Toronto",  "Route": "—",              "Fuel (%)": 95,  "km Today": 0 },
        {"ID": "SRS-17", "Type": "Pickup Truck Plow", "Status": "Active",            "Zone": "Zone 2 — West Toronto",  "Route": "Kipling Ave",    "Fuel (%)": 44,  "km Today": 31},
        {"ID": "SRS-18", "Type": "Salting Truck",     "Status": "Active",            "Zone": "Zone 1 — North Toronto", "Route": "Wilson Ave",     "Fuel (%)": 53,  "km Today": 29},
        {"ID": "SRS-19", "Type": "Salting Truck",     "Status": "En Route",          "Zone": "Zone 4 — Brampton",      "Route": "Hwy 410",        "Fuel (%)": 78,  "km Today": 11},
        {"ID": "SRS-20", "Type": "Salting Truck",     "Status": "Idle",              "Zone": "Zone 3 — East Toronto",  "Route": "—",              "Fuel (%)": 90,  "km Today": 0 },
    ])

def vehicles_main():
    st.title(":truck: Vehicles")
    vehicles_data = get_fleet_data()

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

    st.divider()

    st.subheader("Operations Filtering")
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

    st.dataframe(fleet_df, use_container_width=True, hide_index=True, height=460)

