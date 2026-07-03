def extract_railway(station):
    """
    Railway-derived attributes.
    """

    minimum_connection = station.get("minimumConnectionTime")

    return {

        "minimum_connection_time": minimum_connection or "",

        "is_request_stop": station.get("isRequestStop", False),

        "minimum_connection_time": minimum_connection or "",
"is_request_stop": station.get("isRequestStop", False),

# To be derived later
"is_interchange": None,
"route_count": None,
"service_count": None,
"is_terminus": None,
"is_branch_line": None,
"is_mainline": None,

        # Future enrichments
        "route_count": None,
        "service_count": None,
        "is_terminus": None,
        "is_branch_line": None,
        "is_mainline": None,
    }