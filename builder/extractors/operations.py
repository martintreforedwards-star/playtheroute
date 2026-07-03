def extract_operations(station):

    operator = station.get("stationOperator") or {}
    platform = station.get("platformFacilities") or {}

    return {
        "operator_code": operator.get("operatorCode") or "",
        "operator_name": operator.get("name") or "",
        "minimum_connection_time": station.get("minimumConnectionTime") or "",
        "platform_count": platform.get("numberOfPlatforms"),
    }