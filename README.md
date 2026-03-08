# COE892-Snow-Removal-System
Work in Progress
<br>
Source code for the term project of course COE892 at Toronto Metropolitan University. Please refrain from copying.

Dependency Installation (development performed on Python 3.11.9):
```pip install -r requirements.txt```

Run the Data Extraction Layer:
```python3 -m uvicorn data_layer.data_extraction:app --reload```

Run the Streamlit Dashboard:
```python3 -m streamlit run DashboardSRS.py```
