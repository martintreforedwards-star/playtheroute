from pathlib import Path

import pandas as pd


MASTER = Path("data/Masters")


def main():

    patterns = pd.read_csv(MASTER / "service_patterns.csv")
    routes = pd.read_csv(MASTER / "pattern_routes.csv")
    stations = pd.read_csv(MASTER / "stations.csv")

    # pattern_id -> route_id
    route_lookup = (
        routes
        .set_index("pattern_id")["route_id"]
        .to_dict()
    )

    # crs -> station_name
    station_lookup = (
        stations
        .drop_duplicates("crs")
        .set_index("crs")["station_name"]
        .to_dict()
    )

    rows = []

    for _, pattern in patterns.iterrows():

        route_id = route_lookup.get(pattern["pattern_id"])

        if route_id is None:
            continue

        station_list = str(pattern["stations"]).split("|")

        for crs in station_list:

            rows.append(
                {
                    "crs": crs,
                    "station_name": station_lookup.get(crs, ""),
                    "route_id": route_id,
                }
            )

    station_routes = pd.DataFrame(rows)

    station_routes = (
        station_routes
        .drop_duplicates()
        .sort_values(["crs", "route_id"])
    )

    outfile = MASTER / "station_routes.csv"

    station_routes.to_csv(outfile, index=False)

    print(f"Saved : {outfile}")
    print(f"Rows  : {len(station_routes):,}")
    print()

    print(station_routes.head(20).to_string(index=False))


if __name__ == "__main__":
    main()