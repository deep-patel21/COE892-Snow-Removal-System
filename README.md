# COE892-Snow-Removal-System
Work in Progress
<br>
Source code for the term project of course COE892 at Toronto Metropolitan University. Please refrain from copying.

1. Dependency Installation (development performed on Python 3.11.9):
```pip install -r requirements.txt```

2. Run the gPRC Server:
```python3 -u data_layer/grpc_server.py```

3. Run the Data Extraction Layer:
```python3 -m uvicorn data_layer.data_extraction:app --reload```

4. Run the Streamlit Dashboard:
```python3 -m streamlit run DashboardSRS.py```
