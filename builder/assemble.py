from pathlib import Path

import pandas as pd

from builder.network_source import load_network
from builder.save_master import save_master


def build_master(config):
    """
    Build the master CSV if it does not already exist.
    """

    if "master" in config:
        master_file = config["master"]
    else:
        network = config.get("network", "").strip()
        if not network:
            raise KeyError("Config must contain either 'master' or 'network'.")
        master_file = str(Path("data") / network / f"{network.lower()}_master.csv")

    master_path = Path(master_file)

    # Existing master - ensure station_id exists
    if master_path.exists():

        df = pd.read_csv(master_path)

        if "station_id" not in df.columns:

            prefix = config.get(
                "network",
                config.get("name", "")
            )[:2].upper()

            df["station_id"] = [
                f"{prefix}_{i:06d}"
                for i in range(1, len(df) + 1)
            ]

            save_master(df, master_file)

        return master_file

    print("Creating master dataset...")

    df = load_network(config["network"].lower())

    prefix = config["network"][:2].upper()

    df["station_id"] = [
        f"{prefix}_{i:06d}"
        for i in range(1, len(df) + 1)
    ]

    save_master(df, master_file)

    print(f"Saved: {master_file}")

    return master_file