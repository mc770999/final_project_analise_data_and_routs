query_search_by_keywords = lambda keywords, limit :{
        "query": {
            "bool": {
                "filter": [
                    {"exists": {"field": "location.latitude"}},  # Ensure latitude exists
                    {"exists": {"field": "location.longitude"}}  # Ensure longitude exists
                ],
                "must": [
                    {
                        "query_string": {
                            "query": " OR ".join(f"*{keyword}*" for keyword in keywords),  # Join keywords with OR
                            "default_operator": "OR",  # Use OR as the default operator
                            "fields": ["*"],  # Search across all fields
                            "analyze_wildcard": True  # Enable wildcard analysis
                        }
                    }
                ]
            }
        },
        "size": limit  # Limit the number of results returned
    }

query_search_by_keywords_and_index = lambda keywords, limit: {
    "query": {
        "bool": {
            "filter": [
                {"exists": {"field": "location.latitude"}},  # Ensure latitude exists
                {"exists": {"field": "location.longitude"}}  # Ensure longitude exists
            ],
            "must": [
                {
                    "query_string": {
                        "query": " OR ".join(f"*{keyword}*" for keyword in keywords),  # Join keywords with OR
                        "default_operator": "OR",  # Use OR as the default operator
                        "fields": ["*"],  # Search across all fields
                        "analyze_wildcard": True  # Enable wildcard analysis
                    }
                }
            ]
        }
    },
    "size": limit  # Limit the number of results returned
}

query_search_keyword_in_all_indexes_between_dates = lambda keywords, limit: {
    "query": {
        "bool": {
            "filter": [
                {"exists": {"field": "location.latitude"}},  # Ensure latitude exists
                {"exists": {"field": "location.longitude"}},  # Ensure longitude exists
                {"exists": {"field": "date.year"}}  # Ensure longitude exists
            ],
            "must": [
                {
                    "query_string": {
                        "query": " OR ".join(f"*{keyword}*" for keyword in keywords),  # Join keywords with OR
                        "default_operator": "OR",  # Use OR as the default operator
                        "fields": ["*"],  # Search across all fields
                        "analyze_wildcard": True  # Enable wildcard analysis
                    }
                }
            ]
        }
    },
    "size": limit
}