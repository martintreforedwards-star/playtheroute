from pathlib import Path

import pandas as pd


MASTER = Path("data/Masters")


def main():

    route_id = input("Route ID: ").strip().upper()

    routes = pd.read_csv(MASTER / "route_candidates.csv")
    patterns = pd.read_csv(MASTER / "service_patterns.csv")
    tree = pd.read_csv(MASTER / "route_tree.csv")

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
            f"{row['origin']} → {row['destination']}   "
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
                f"after {row['split_after']}   "
                f"→ {row['destination']}   "
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

        shortest = min(
            station_lists,
            key=len,
        )

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
            print(station)

    else:

        print("None")

    print()

    origins = sorted(details["origin"].unique())
    destinations = sorted(details["destination"].unique())

    print("Origins")
    print("-------")
    print(", ".join(origins))

    print()

    print("Destinations")
    print("------------")
    print(", ".join(destinations))


if __name__ == "__main__":
    main()