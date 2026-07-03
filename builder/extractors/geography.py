def extract_geography(station):

    location = station.get("location") or {}

    return {
        "latitude": location.get("latitude"),
        "longitude": location.get("longitude"),
    }