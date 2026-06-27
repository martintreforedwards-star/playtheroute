from pathlib import Path
import pandas as pd


def enrich(config):

    master = Path(config["master"])

    stations = pd.read_csv(master)

    print(f"Stations: {len(stations)}")

    return stations