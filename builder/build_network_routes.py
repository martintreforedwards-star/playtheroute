from pathlib import Path

import pandas as pd


MASTER = Path("data/Masters")


def main():

    routes = pd.read_csv(MASTER / "routes.csv")
    lookup = pd.read_csv(MASTER / "route_lookup.csv")

    network_routes = routes.merge(
        lookup,
        on="route_id",
        how="left",
    )

    columns = [
        "route_id",
        "route_name",
        "route_group",
        "origin",
        "primary_destination",
        "pattern_count",
        "service_count",
        "branch_count",
        "corridor_length",
        "corridor_end",
    ]

    network_routes = network_routes[columns]

    outfile = MASTER / "network_routes.csv"

    network_routes = network_routes.sort_values("route_name")

    network_routes.to_csv(outfile, index=False)

    print(f"Saved : {outfile}")
    print(f"Routes : {len(network_routes):,}")
    print()

    print(network_routes.head(20).to_string(index=False))


if __name__ == "__main__":
    main()