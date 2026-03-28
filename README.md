# COE892-Snow-Removal-System
Source code for the term project of course COE892 at Toronto Metropolitan University. Please refrain from copying.
<br>
The Snow Removal System (SRS) is an interactive tool that combines data from APIs and uses messaging protocols through FastAPI and gRPC to present weather, vehicle, and scheduling data in a minimalistic dashboard.

Please note that development was performed on Python 3.11.9+. Ensure versions match before proceeding to installation and usage.

Installation:
1. Repository Cloning
```git clone https://github.com/deep-patel21/COE892-Snow-Removal-System.git```
2. Dependency Installation:
```pip install -r requirements.txt```


Usage Instructions:
The below commands should be executed in separate terminals sequentially. Please adjust path names based on the operating system being used.
1. Run the gPRC Server:
```python3 -u data_layer/grpc_server.py```

2. Run the Data Extraction Layer:
```python3 -m uvicorn data_layer.data_extraction:app --reload```

3. Run the Streamlit Dashboard:
```python3 -m streamlit run frontend/DashboardSRS.py```


Architecture:
<figure>
  <img src="/documentation_images/architecture.png" alt="system-architecture" style="border:2px solid grey;">
  <figcaption align="center">
    <i><b>Figure 1:</b></i> High-level architectural overview of Snow Removal System (SRS).
  </figcaption>
</figure>

Application Screenshots:
<figure>
  <img src="/documentation_images/weather_metrics.jpg" alt="weather-metrics" style="border:2px solid grey;">
  <figcaption align="center">
    <i><b>Figure 1:</b></i> Weather data metrics.
  </figcaption>
</figure>

<figure>
  <img src="/documentation_images/vehicles_metrics.jpg" alt="vehicles-metrics" style="border:2px solid grey;">
  <figcaption align="center">
    <i><b>Figure 2:</b></i> Vehicle fleet metrics.
  </figcaption>
</figure>

<figure>
  <img src="/documentation_images/scheduling_metrics.jpg" alt="scheduling-metrics" style="border:2px solid grey;">
  <figcaption align="center">
    <i><b>Figure 3:</b></i> Scheduling timeline metrics.
  </figcaption>
</figure>

<figure>
  <img src="/documentation_images/weather_analytics.png" alt="weather-analytics" style="border:2px solid grey;">
  <figcaption align="center">
    <i><b>Figure 4:</b></i> Weather analytics per zone.
  </figcaption>
</figure>

<figure>
  <img src="/documentation_images/fleet_analytics.png" alt="fleet-analytics" style="border:2px solid grey;">
  <figcaption align="center">
    <i><b>Figure 5:</b></i> Fleet analytics by vehicle type and zones.
  </figcaption>
</figure>

<figure>
  <img src="/documentation_images/assigment_timeline.png" alt="scheduling-analytics" style="border:2px solid grey;">
  <figcaption align="center">
    <i><b>Figure 6:</b></i> Assignment timeline based on priorities.
  </figcaption>
</figure>

<figure>
  <img src="/documentation_images/assignment_details.png" alt="fleet-analytics" style="border:2px solid grey;">
  <figcaption align="center">
    <i><b>Figure 7:</b></i> Assignment table for vehicle management.
  </figcaption>
</figure>
