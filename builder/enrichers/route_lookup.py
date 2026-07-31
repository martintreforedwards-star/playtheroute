from pathlib import Path

import pandas as pd


MASTER = Path("data/Masters")


def apply_route_lookup(config):
    """
    Apply route_name and route_group to the enriched network CSV.
    """

    network = config["network"]

    csv_path = (
        Path("data/Class1")
        / network
        / f"{network.lower()}_enriched.csv"
    )

    lookup_path = MASTER / "route_lookup.csv"

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Network CSV not found: {csv_path}"
        )

    if not lookup_path.exists():
        raise FileNotFoundError(
            f"Route lookup not found: {lookup_path}"
        )

    stations = pd.read_csv(csv_path)
    lookup = pd.read_csv(lookup_path)

    # Remove existing columns if present
    for column in ["route_name", "route_group"]:
        if column in stations.columns:
            stations = stations.drop(columns=column)

    stations = stations.merge(
        lookup[
            [
                "route_id",
                "route_name",
                "route_group",
            ]
        ],
        how="left",
        on="route_id",
    )

    stations.to_csv(csv_path, index=False)

    matched = stations["route_name"].notna().sum()

    print()
    print("Applied route lookup")
    print(f"Network : {network}")
    print(f"Matched : {matched}/{len(stations)} stations")
    print(f"Saved   : {csv_path}")