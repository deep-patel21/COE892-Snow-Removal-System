import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Assuming these will be your imports from the data/scheduler layers
from data_layer.data_helpers import COORDINATES
from scheduler.scheduler import get_fleet_data, dispatch_vehicles  
from scheduler.simulation_data import get_conditions_mock

ZONES = [
    "Zone 1 — North Toronto", "Zone 2 — West Toronto",
    "Zone 3 — East Toronto",  "Zone 4 — Brampton",
    "Zone 5 — Etobicoke",     "Zone 6 — Scarborough",
    "Zone 7 — Richmond Hill", "Zone 8 — Mississauga",
    "Zone 9 — Markham",       "Zone 10 — Vaughan",
]

@st.cache_data(ttl=120)

def fetch_schedules():
    try:
        fleet_df = get_fleet_data()
        zone_conditions = get_conditions_mock()
        plan = dispatch_vehicles(fleet_df, zone_conditions).copy()

        #assign priorities
        priority_map = {zone: data["dispatch_priority"] for zone, data in zone_conditions.items()}
        if zone_conditions:
            plan["Dispatch Priority"] = plan["Zone"].map(priority_map)
            plan["Priority Level"] = plan["Dispatch Priority"].apply(priority_icon)

        # populate assigned and next zones
        plan["assigned_zone"] = plan["assigned_zone"].fillna(plan["Zone"])
        next_zone_map = {}
        for i in range(len(ZONES)):
            current_zone = ZONES[i]
            next_zone_index = (i + 1) % len(ZONES)
            next_zone_map[current_zone] = ZONES[next_zone_index]
        plan["nextzone"] = plan["assigned_zone"].map(next_zone_map)  

        #assign start and end times based on priority 
        now = pd.Timestamp.now().floor('min')

        # how long until each job starts based on priority
        start_delays = {
            "High": 0,   # High: Starts immediately
            "Medium": 2,   # Medium: Starts in 2 hours
            "Low": 6,   # Low: Starts in 6 hours
            "Clear": 24   # Clear: Routine patrol tomorrow
        }

        # how long each job will take based on priority
        job_durations = {
            "High": 3,   # Takes 3 hours
            "Medium": 4,   # Takes 4 hours
            "Low": 4,   # Takes 4 hours
            "Clear": 2    # Takes 2 hours
        }

        random_delays = np.random.randint(10, 80, size=len(plan))

        # Cleans the column just in case there are invisible spaces aaround txt
        priority_col = plan["Dispatch Priority"].str.strip()

        # Creates the Start Time column instantly
        plan["Start Time"] = now + pd.to_timedelta(priority_col.map(start_delays), unit='h') + pd.to_timedelta(random_delays, unit='m')

        # Creates the End Time column instantly
        plan["End Time"] = plan["Start Time"] + pd.to_timedelta(priority_col.map(job_durations), unit='h') 
        
        print(plan)
        return plan
        
    except Exception as e:
        st.error(f"Scheduling algorithm data unavailable: {e}")
        return pd.DataFrame()


def generate_timeline(schedule_df):
    if schedule_df.empty:
        st.info("No active schedules to display.")
        return

    st.subheader("Assignment Timeline")
    
    # Ensure datetime format for Plotly timeline
    schedule_df["Start Time"] = pd.to_datetime(schedule_df["Start Time"])
    schedule_df["End Time"] = pd.to_datetime(schedule_df["End Time"])

    # Create the Gantt chart
    fig = px.timeline(
        schedule_df, 
        x_start="Start Time", 
        x_end="End Time", 
        y="Zone",
        color="Dispatch Priority", # Color-code by priority
        hover_name="ID",
        hover_data=["Type", "Status"],
        title="Vehicle Dispatch Schedule by Zone",
        color_discrete_map={
            "High": "#ef4444",   # Red
            "Medium": "#f97316", # Orange
            "Low": "#facc15",    # Yellow
            "Clear": "#34d399"   # Green
        }
    )
    
    fig.update_yaxes(categoryorder="array", categoryarray=ZONES[::-1])
    fig.update_traces(marker_line_color='rgb(255,255,255)', marker_line_width=2, opacity=1.0)
    # Apply your custom glassmorphism/transparent styling
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white", 
        height=600,
        margin=dict(t=80, b=20, l=20, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, title="Dispatch Priority: ")
    )
    
    st.plotly_chart(fig, use_container_width=True)

def priority_icon(priority):
    priority_icons = {
        "High":   "🔴",
        "Medium": "🟠",
        "Low":    "🟡",
        "Clear":  "🟢",
    }

    return priority_icons.get(priority, "-")



def scheduling_main():
    st.title(":date: Scheduling & Assignments")
    
    schedule_df = fetch_schedules()

    if not schedule_df.empty:
        # High-level metrics
        st.subheader("Schedule Overview")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Active Assignments", len(schedule_df))
        c2.metric("High Priority Zones", len(schedule_df[schedule_df["Dispatch Priority"] == "High"]))
        c3.metric("Vehicles Dispatched", schedule_df["ID"].nunique())
        
        st.divider()

        # Generate the Timeline
        generate_timeline(schedule_df)
        
        st.divider()

        # Detailed Assignment Table
        st.subheader("Assignment Details")
        
        # Add visual icons to the dataframe
        display_df = schedule_df.copy()
        
        # Format the datetimes for cleaner reading in the table
        display_df["Start Time"] = display_df["Start Time"].dt.strftime("%H:%M")
        display_df["End Time"] = display_df["End Time"].dt.strftime("%H:%M")
        
        # Reorder columns for the UI table
        display_df = display_df[["ID", "Zone", "Type", "Priority Level", "Dispatch Priority", "Start Time", "End Time", "Status"]]
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.warning("No scheduling data could be loaded.")
