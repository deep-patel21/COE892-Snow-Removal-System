# COE892-Snow-Removal-System
##### Disclaimer:
Source code for the term project of course COE892 at Toronto Metropolitan University. Please refrain from copying to avoid violation of POL60.

### Objective
The Snow Removal System (SRS) is an interactive tool that combines data from APIs and uses messaging protocols through FastAPI and gRPC to present weather, vehicle, and scheduling data in a minimalistic dashboard. Modular development principles have been used to separate functionalities into the data extraction layer, grpc server, and frontend pages.

### Installation
Please note that development was performed on Python 3.11.9+. Ensure versions match before proceeding to installation and usage.
1. Repository Cloning:
```git clone https://github.com/deep-patel21/COE892-Snow-Removal-System.git```
2. Dependency Installation:
```pip install -r requirements.txt```


### Usage Instructions:
The below commands should be executed in separate terminals sequentially. Please adjust path names based on the operating system being used.
1. Run the gPRC Server:
```python3 -u data_layer/grpc_server.py```

2. Run the Data Extraction Layer:
```python3 -m uvicorn data_layer.data_extraction:app --reload```

3. Run the Streamlit Dashboard:
```python3 -m streamlit run frontend/DashboardSRS.py```


### Architecture:
<p align="center">
  <img src="/documentation_images/architecture.png" alt="system-architecture" style="border:2px solid grey;"><br>
  <em><b>Figure 1:</b> High-level architectural overview of Snow Removal System (SRS).</em>
</p>

### Application Screenshots:
<p align="center">
  <img src="/documentation_images/weather_metrics.jpg" alt="weather-metrics" style="border:2px solid grey;"><br>
  <em><b>Figure 1:</b> Weather data metrics.</em>
</p>
 
<p align="center">
  <img src="/documentation_images/vehicles_metrics.jpg" alt="vehicles-metrics" style="border:2px solid grey;"><br>
  <em><b>Figure 2:</b> Vehicle fleet metrics.</em>
</p>
 
<p align="center">
  <img src="/documentation_images/scheduling_metrics.jpg" alt="scheduling-metrics" style="border:2px solid grey;"><br>
  <em><b>Figure 3:</b> Scheduling timeline metrics.</em>
</p>
 
<p align="center">
  <img src="/documentation_images/weather_analytics.png" alt="weather-analytics" style="border:2px solid grey;"><br>
  <em><b>Figure 4:</b> Weather analytics per zone.</em>
</p>
 
<p align="center">
  <img src="/documentation_images/fleet_analytics.png" alt="fleet-analytics" style="border:2px solid grey;"><br>
  <em><b>Figure 5:</b> Fleet analytics by vehicle type and zones.</em>
</p>
 
<p align="center">
  <img src="/documentation_images/assigment_timeline.png" alt="scheduling-analytics" style="border:2px solid grey;"><br>
  <em><b>Figure 6:</b> Assignment timeline based on priorities.</em>
</p>
 
<p align="center">
  <img src="/documentation_images/assignment_details.png" alt="assignment-details" style="border:2px solid grey;"><br>
  <em><b>Figure 7:</b> Assignment table for vehicle management.</em>
</p>
