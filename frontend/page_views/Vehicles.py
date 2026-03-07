import streamlit as st

VEHICLES = ["Highway Plow", "Road Plow", "Pickup Truck Plow", "Salting Truck"]
VEHICLE_STATUS = ["Idle", "En Route", "Active", "Cancelled", "Under Maintenance"]
ZONES = ["Zone 1", "Zone 2", "Zone 3", "Zone 4"]

def vehicles_main():
    st.title(":truck: Vehicles")

    # TK - replace with real data after integration
    total_vehicles = 12
    active_vehicles = 5
    en_route_vehicles = 2
    idle_vehicles = 7
    cancelled_vehicles = 1
    under_maintenance_vehicles = 2

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
    c7, c8, c9 = st.columns([1, 1, 2])
    with c7:
        vehicle_filter = st.selectbox(":articulated_lorry: Vehicle Type", ["All", *VEHICLES])
    with c8:
        status_filter = st.selectbox(":compass: Status", ["All", *VEHICLE_STATUS])
    with c9:
        zone_filter = st.selectbox(":world_map: Assigned Zone", ["All", *ZONES])