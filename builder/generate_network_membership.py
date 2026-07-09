from pathlib import Path

import pandas as pd


def generate_network_membership(config):
    """
    Generate network_membership.csv and route_membership.csv
    from the network master dataset.
    """

    network = config["network"]

    master_file = Path(
        config.get(
            "master",
            Path("data") / network / f"{network.lower()}_master.csv",
        )
    )

    df = pd.read_csv(master_file)

    # Create station_id if required
    if "station_id" not in df.columns:
        prefix = network[:2].upper()
        df["station_id"] = [
            f"{prefix}_{i:06d}"
            for i in range(1, len(df) + 1)
        ]

    membership = pd.DataFrame(
        {
            "station_id": df["station_id"],
            "network": network,
            "route_station_id": [
                f"{network[:2].upper()}{i:04d}"
                for i in range(1, len(df) + 1)
            ],
            "route_group": "",
            "crs": df["crs"],
            "station_name": df["station_name"],
        }
    )

    masters = Path("data") / "Masters"
    masters.mkdir(parents=True, exist_ok=True)

    network_membership = masters / "network_membership.csv"
    route_membership = (
        Path("data") / network / "route_membership.csv"
    )

    if network_membership.exists():
        existing = pd.read_csv(network_membership)
        existing = existing[
            existing["network"].str.lower() != network.lower()
        ]
        membership = pd.concat(
            [existing, membership],
            ignore_index=True,
        )

    membership.to_csv(network_membership, index=False)
    membership.to_csv(route_membership, index=False)

    print(f"Saved : {network_membership}")
    print(f"Saved : {route_membership}")