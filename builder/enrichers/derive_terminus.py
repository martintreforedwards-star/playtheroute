from pathlib import Path

import pandas as pd


def derive_terminus(config):
    """
    Populate the terminus flag from the Service Builder output.

    service_patterns.csv already contains CRS codes in the
    origin and destination columns.
    """

    network = config["network"]

    patterns_file = Path("data/Masters/service_patterns.csv")
    stations_file = (
        Path("data/Class1")
        / network
        / f"{network.lower()}_aggregated_1.csv"
    )

    if not patterns_file.exists():
        print("WARN  service_patterns.csv not found")
        return

    if not stations_file.exists():
        print("WARN  Aggregated station file not found")
        return

    patterns = pd.read_csv(patterns_file)
    stations = pd.read_csv(stations_file)

    termini = set()

    if "origin" in patterns.columns:
        termini.update(
            patterns["origin"]
            .dropna()
            .astype(str)
            .str.strip()
            .str.upper()
        )

    if "destination" in patterns.columns:
        termini.update(
            patterns["destination"]
            .dropna()
            .astype(str)
            .str.strip()
            .str.upper()
        )

    stations["terminus"] = (
        stations["crs"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
        .isin(termini)
    )

    stations.to_csv(stations_file, index=False)

    print(f"INFO  Termini identified : {len(termini)}")
    print(f"PASS  Updated {stations_file}")