API_BASE = "http://localhost:8000/api/v1"   # Dedicated local API endpoint

COORDINATES = {
    "Zone 1 — North Toronto":  {"lat": 43.761, "lon": -79.411},
    "Zone 2 — West Toronto":   {"lat": 43.651, "lon": -79.495},
    "Zone 3 — East Toronto":   {"lat": 43.673, "lon": -79.298},
    "Zone 4 — Brampton":       {"lat": 43.685, "lon": -79.759},
    "Zone 5 — Etobicoke":      {"lat": 43.713, "lon": -79.559},
    "Zone 6 — Scarborough":    {"lat": 43.773, "lon": -79.228},
    "Zone 7 — Richmond Hill":  {"lat": 43.882, "lon": -79.437},
    "Zone 8 — Mississauga":    {"lat": 43.589, "lon": -79.644},
    "Zone 9 — Markham":        {"lat": 43.856, "lon": -79.337},
    "Zone 10 — Vaughan":       {"lat": 43.837, "lon": -79.508},
}

def search_matches(row, query):
    """
    Utility function to determine if the data set contains a match to a search query
    """
    
    return row.astype(str).str.contains(query, case=False).any()