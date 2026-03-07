import logging
from datetime import datetime
from enum import IntEnum
import streamlit as st

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("SRS")

class Page(IntEnum):
    OVERVIEW   = 0 
    WEATHER    = 1 
    VEHICLES   = 2 
    SCHEDULING = 3

def configure_streamlit_app():
    st.set_page_config(
        page_title="Snow Removal System",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def create_sidebar():
    with st.sidebar:
        st.markdown("## :snowflake: **Snow Removal System**")
        st.caption(f":clock12: {datetime.now().strftime('%A, %b %d %Y — %H:%M')}")
        st.divider()

        pages = [
            ":bar_chart: **Overview**",
            ":cloud_with_rain: **Weather**",
            ":red_car: **Vehicles**",
            ":date: **Scheduling**"
        ]

        page_selection = st.radio(
            "Page View:", 
            pages,
            label_visibility="collapsed"
        )

        st.divider()
        st.markdown("Page Controls")
        auto_refresh = st.toggle("Auto-refresh data", value=False)

        if auto_refresh:
            st.cache_data.clear()
            st.rerun()

    return Page(pages.index(page_selection))

def main():
    configure_streamlit_app()
    page_selection = create_sidebar()

    # weather_data  = get_weather_data()
    # routes_data   = get_routes_data()
    # fleet_data    = get_fleet_data()
    # schedule_data = get_schedule_data()

    match page_selection:
        case Page.OVERVIEW:
            pass
        case Page.WEATHER:
            pass
        case Page.VEHICLES:
            pass
        case Page.SCHEDULING:
            pass
        case _:
            logger.error("Invalid page selection")


if __name__ == "__main__":
    main()