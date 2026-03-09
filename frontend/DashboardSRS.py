import logging
from datetime import datetime
from enum import IntEnum
import streamlit as st

from page_views.Weather import weather_main
from page_views.Vehicles import vehicles_main
from page_views.Scheduling import scheduling_main

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("SRS")

class Page(IntEnum):
    WEATHER    = 0
    VEHICLES   = 1 
    SCHEDULING = 2

def configure_streamlit_app():
    st.set_page_config(
        page_title="Snow Removal System",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown("""
        <style>
        [data-testid="stMetric"] {
            background: rgba(0, 0, 128, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            padding: 20px 24px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        [data-testid="stPlotlyChart"] {
            background: rgba(0, 0, 128, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            padding: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

def create_sidebar():
    with st.sidebar:
        st.markdown("## :snowflake: **Snow Removal System**")
        st.caption(f":clock12: {datetime.now().strftime('%A, %b %d %Y — %H:%M')}")
        st.divider()

        pages = [
            ":cloud_with_rain: **Weather**",
            ":truck: **Vehicles**",
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

    match page_selection:
        case Page.WEATHER:
            weather_main()
        case Page.VEHICLES:
            vehicles_main()
        case Page.SCHEDULING:
            scheduling_main()
        case _:
            logger.error("Invalid page selection")


if __name__ == "__main__":
    main()