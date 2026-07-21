from pathlib import Path

import pandas as pd


def derive_terminus(config):
    """
    Populate the terminus field with the destination terminus (CRS)
    reachable from each station using service_patterns.csv.
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

    patterns = pd.read_csv(patterns_file, dtype=str).fillna("")
    stations = pd.read_csv(stations_file, dtype=str).fillna("")

    station_lookup = {}

    for _, row in patterns.iterrows():

        destination = row["destination"].strip().upper()
        stations_text = row["stations"].strip()

        if not destination or not stations_text:
            continue

        stations_on_path = [
            s.strip().upper()
            for s in stations_text.split("|")
            if s.strip()
        ]

        for crs in stations_on_path:
            station_lookup.setdefault(crs, set()).add(destination)

    stations["terminus"] = stations["crs"].str.upper().map(
        lambda crs: "|".join(sorted(station_lookup.get(crs, [])))
    )

    stations.to_csv(stations_file, index=False)

    print(f"INFO  Stations with termini : {len(station_lookup)}")
    print(f"PASS  Updated {stations_file}")