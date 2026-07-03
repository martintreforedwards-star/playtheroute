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

        location = station.get("location", {})
        operator = station.get("stationOperator", {})

        rows.append(
            {
                "station_name": station.get("name"),
                "crs": crs,
                "latitude": location.get("latitude"),
                "longitude": location.get("longitude"),
                "operator_code": operator.get("code"),
                "operator_name": operator.get("name"),
            }
        )

    df = pd.DataFrame(rows)

    return df.sort_values("station_name").reset_index(drop=True)