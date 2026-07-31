from pathlib import Path

import pandas as pd


MASTER = Path("data/Masters")


def station_name(crs, lookup):
    """Return the station name for a CRS code."""
    return lookup.get(crs, crs)


def main():

    route_id = input("Route ID: ").strip().upper()

    routes = pd.read_csv(MASTER / "pattern_routes.csv")
    patterns = pd.read_csv(MASTER / "service_patterns.csv")
    tree = pd.read_csv(MASTER / "route_tree.csv")
    stations = pd.read_csv(MASTER / "stations.csv")

    station_lookup = (
        stations
        .dropna(subset=["crs", "station_name"])
        .drop_duplicates(subset=["crs"])
        .set_index("crs")["station_name"]
        .to_dict()
    )

    members = routes[routes["route_id"] == route_id]

    if members.empty:
        print(f"Route {route_id} not found.")
        return

    pattern_ids = set(members["pattern_id"])

    print()
    print("=" * 60)
    print(f"Route {route_id}")
    print("=" * 60)
    print()

    print(f"Patterns : {len(pattern_ids)}")
    print()

    details = patterns[
        patterns["pattern_id"].isin(pattern_ids)
    ].copy()

    details = details.sort_values(
        ["service_count", "station_count"],
        ascending=False,
    )

    print("Patterns")
    print("--------")

    for _, row in details.iterrows():

        print(
            f"{row['pattern_id']}   "
            f"{station_name(row['origin'], station_lookup)}"
            f" → "
            f"{station_name(row['destination'], station_lookup)}   "
            f"{row['station_count']:2} stations   "
            f"{row['service_count']:4} services"
        )

    print()

    branches = tree[
        tree["route_id"] == route_id
    ]

    if not branches.empty:

        print("Branches")
        print("--------")

        for _, row in branches.iterrows():

            print(
                f"{row['branch_pattern']}   "
                f"after {station_name(row['split_after'], station_lookup)}   "
                f"→ {station_name(row['destination'], station_lookup)}   "
                f"({row['shared_prefix']} shared stations)"
            )

        print()

    #
    # Common corridor
    #

    station_lists = [
        row["stations"].split("|")
        for _, row in details.iterrows()
    ]

    common = []

    if station_lists:

        shortest = min(station_lists, key=len)

        for i, station in enumerate(shortest):

            if all(
                len(s) > i and s[i] == station
                for s in station_lists
            ):
                common.append(station)
            else:
                break

    print("Common corridor")
    print("----------------")

    if common:

        for station in common:
            print(station_name(station, station_lookup))

    else:

        print("None")

    print()

    origins = sorted(details["origin"].unique())
    destinations = sorted(details["destination"].unique())

    print("Origins")
    print("-------")
    print(
        ", ".join(
            station_name(crs, station_lookup)
            for crs in origins
        )
    )

    print()

    print("Destinations")
    print("------------")
    print(
        ", ".join(
            station_name(crs, station_lookup)
            for crs in destinations
        )
    )


if __name__ == "__main__":
    main()