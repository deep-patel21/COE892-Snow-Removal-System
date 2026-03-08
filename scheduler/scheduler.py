import sys
import os
import grpc
import pandas as pd

import data_layer.snow_removal_pb2 as snow_removal_pb2
import data_layer.snow_removal_pb2_grpc as snow_removal_pb2_grpc
from data_layer.data_helpers import COORDINATES as locations

#Temp
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


def get_conditions():
    conditions = {}
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = snow_removal_pb2_grpc.RoadMonitorStub(channel)
        for name, coords in locations.items():
            request = snow_removal_pb2.CoordinateRequest(latitude=coords["lat"], longitude=coords["lon"])
            try:
                responses = stub.StreamConditions(request)
                for response in responses:
                    conditions[name] = {
                        "road_type": response.road_type,
                        "dispatch_priority": response.dispatch_priority,
                        "traffic_speed_kmh": response.traffic_speed_kmh,
                        "weather": {
                            "temperature_c": response.weather.temperature_c,
                            "wind_speed_kmh": response.weather.wind_speed_kmh,
                            "snow_depth_mm": response.weather.snow_depth_mm
                        }
                    }
                    break
            except grpc.RpcError as e:
                conditions[name] = {"error": e.details()}
    return conditions


def dispatch_vehicles(fleet_df: pd.DataFrame, zone_conditions: dict) -> pd.DataFrame:  
    priority_order = ["High", "Medium", "Low"]

    # Ensure necessary columns exist
    if 'assigned_zone' not in fleet_df.columns:
        fleet_df['assigned_zone'] = None
    if 'nextzone' not in fleet_df.columns:
        fleet_df['nextzone'] = None

    # Filter only zones that need service
    zones_needed = []
    for zone, cond in zone_conditions.items():
        priority = cond.get("dispatch_priority")
        snow = cond.get("weather", {}).get("snow_depth_mm", 0)
        if priority in priority_order and snow != "clear" and snow > 0:
            zones_needed.append({
                "zone": zone,
                "priority": priority,
                "road_type": cond.get("road_type", ""),
                "snow_depth_mm": snow
            })
    print(f"\nzones need {zones_needed}")

    # Sort zones: high priority and heavy snow first
    zones_needed.sort(key=lambda x: (priority_order.index(x["priority"]), -x["snow_depth_mm"]))

    # Map zones to "neighbors" (example: zone1 -> zone2, zone2 -> zone1 & zone3)
    zone_names = list(zone_conditions.keys())
    zone_neighbors = {}
    for i, z in enumerate(zone_names):
        neighbors = []
        if i > 0:
            neighbors.append(zone_names[i-1])
        if i < len(zone_names)-1:
            neighbors.append(zone_names[i+1])
        zone_neighbors[z] = neighbors

    # Filter idle vehicles
    idle_vehicles = fleet_df[fleet_df["Status"].isin(["Idle"])].copy()
    
    for zone_info in zones_needed:
        zone_name = zone_info["zone"]
        road_type = zone_info["road_type"]

        # Check if zone already has a vehicle assigned
        zone_has_vehicle = fleet_df[fleet_df['Zone'] == zone_name].shape[0] > 0
        if zone_has_vehicle:
            continue  # skip, already has vehicle in zone

        assigned = False

        # Try to assign an idle vehicle first
        for idx, vehicle in idle_vehicles.iterrows():
            v_type = vehicle["Type"]
            if fleet_df.at[idx, 'assigned_zone'] is not None:
                continue  # already assigned

            # Vehicle matching rules
            if ("Highway" in v_type and "HIGHWAY" in road_type) or \
               ("Road Plow" in v_type and "MAIN" in road_type) or \
               ("Pickup Truck" in v_type) or \
               ("Salting" in v_type and zone_info["priority"] == "High"):

                fleet_df.at[idx, 'assigned_zone'] = zone_name
                fleet_df.at[idx, 'nextzone'] = None
                assigned = True
                break

        if not assigned:
            # No idle vehicle available, try active vehicles in neighboring zones
            neighbors = zone_neighbors.get(zone_name, [])
            active_neighbors = fleet_df[
                (fleet_df["Status"].isin(["Active"])) & 
                (fleet_df["Zone"].isin(neighbors))
            ]

            if not active_neighbors.empty:
                idx = active_neighbors.index[0]
                fleet_df.at[idx, 'nextzone'] = zone_name  # vehicle will move there next

    return fleet_df


if __name__ == "__main__":
    fleet_df = get_fleet_data()
    zone_conditions = get_conditions()
    print(zone_conditions)
    plan = dispatch_vehicles(fleet_df, zone_conditions)
    print(plan)