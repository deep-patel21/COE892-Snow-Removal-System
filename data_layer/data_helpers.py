def search_matches(row, query):
    """
    Utility function to determine if the data set contains a match to a search query
    """
    
    return row.astype(str).str.contains(query, case=False).any()