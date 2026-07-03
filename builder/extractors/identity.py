def extract_identity(station):

    return {
        "station_name": station.get("name") or "",
        "crs": station.get("crsCode") or "",
        "nlc": station.get("nationalLocationCode") or "",
        "slug": station.get("slug") or "",
    }