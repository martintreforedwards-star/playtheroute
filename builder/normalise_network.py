import pandas as pd


def normalise_network(stations, config):
    """
    Convert National Rail Knowledgebase stations into
    The Route master station format.
    """

    wanted = set(config["crs"])
    rows = []

    for station in stations:

        crs = station.get("crsCode")

        if crs not in wanted:
            continue

        # Nested objects (safe against null values)
        location = station.get("location") or {}
        operator = station.get("stationOperator") or {}
        platform = station.get("platformFacilities") or {}
        accessibility = station.get("stationAccessibility") or {}
        stepfree = accessibility.get("stepFreeCategory") or {}

        rows.append({

            # Identity
            "station_name": station.get("name") or "",
            "crs": crs,
            "nlc": station.get("nationalLocationCode") or "",
            "slug": station.get("slug") or "",

            # Geography
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude"),

            # Operator
            "operator_code": operator.get("operatorCode") or "",
            "operator_name": operator.get("name") or "",

            # Operations
            "minimum_connection_time": station.get("minimumConnectionTime") or "",
            "platform_count": platform.get("numberOfPlatforms"),

            # Accessibility
            "staffing_level": station.get("staffingLevel") or "",
            "step_free_category": stepfree.get("category") or "",

        })

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    return (
        df
        .sort_values("station_name")
        .reset_index(drop=True)
    )