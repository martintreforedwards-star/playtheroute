from pathlib import Path

import pandas as pd


def generate_network_membership(config):
    """
    Generate:

    - data/Masters/network_membership.csv (all networks)
    - data/<Network>/route_membership.csv (this network only)
    """

    network = config.get(
        "network",
        config.get(
            "display_name",
            Path(config["master"]).parent.name,
        ),
    )

    master_file = Path(
        config.get(
            "master",
            Path("data") / network / f"{network.lower()}_master.csv",
        )
    )

    df = pd.read_csv(master_file)

    if "station_id" not in df.columns:
        raise KeyError(
            "station_id is missing from the master dataset. "
            "It should be created during build_master()."
        )

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

    network_membership_file = masters / "network_membership.csv"
    route_membership_file = (
        Path("data") / network / "route_membership.csv"
    )

    membership.to_csv(route_membership_file, index=False)

    if network_membership_file.exists():
        existing = pd.read_csv(network_membership_file)

        existing = existing[
            existing["network"].str.lower() != network.lower()
        ]

        network_membership = pd.concat(
            [existing, membership],
            ignore_index=True,
        )

    else:
        network_membership = membership.copy()

    network_membership.to_csv(
        network_membership_file,
        index=False,
    )

    print(f"Saved : {network_membership_file}")
    print(f"Saved : {route_membership_file}")