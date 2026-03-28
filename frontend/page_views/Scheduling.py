import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Assuming these will be your imports from the data/scheduler layers
from data_layer.data_helpers import COORDINATES
from scheduler.scheduler import get_fleet_data, dispatch_vehicles  
from scheduler.simulation_data import get_conditions_mock



@st.cache_data(ttl=120)

def fetch_schedules():
    try:
        fleet_df = get_fleet_data()
        zone_conditions = get_conditions_mock()
        plan = dispatch_vehicles(fleet_df, zone_conditions).copy()
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
