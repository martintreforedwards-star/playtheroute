import csv
from pathlib import Path

from .network import Network, Station


def load_network(config: dict) -> Network:

    network = Network(config["name"])

    master_file = Path(config["input_folder"]) / config["master"]

    with open(master_file, newline="", encoding="utf-8-sig") as f:

        reader = csv.DictReader(f)

        for row in reader:

            network.stations[row["crs"]] = Station(
                crs=row["crs"],
                name=row["station_name"],
                latitude=float(row["latitude"]) if row["latitude"] else None,
                longitude=float(row["longitude"]) if row["longitude"] else None,
            )

    return network