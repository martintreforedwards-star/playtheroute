from pathlib import Path
import json
import pandas as pd


def create_network(network):

    source = pd.read_csv("crs_source_of_truth.csv")

    with open(f"builder/configs/{network.lower()}.json", encoding="utf-8") as f:
        config = json.load(f)

    # Filter source of truth by CRS codes in config
    master = source[
        source["crsCode"].isin(config["crs"])
    ].copy()

    output_folder = Path(f"data/{config['network']}")
    output_folder.mkdir(parents=True, exist_ok=True)

    output = output_folder / f"{network.lower()}_master.csv"

    master.to_csv(output, index=False)

    print()
    print(f"Network : {config['network']}")
    print(f"Stations: {len(master)}")
    print(f"Saved   : {output}")


if __name__ == "__main__":

    import sys

    if len(sys.argv) != 2:
        print("Usage:")
        print("python builder/create_network.py <network>")
        raise SystemExit

    create_network(sys.argv[1])