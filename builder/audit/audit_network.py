from pathlib import Path
import json
import sys
import pandas as pd


def audit(network):

    folder = Path("data") / network
    network_id = network.lower()

    print()
    print("=" * 60)
    print(network)
    print("=" * 60)

    master = folder / f"{network_id}_master.csv"

    print(master)

    if not master.exists():
        print("Master not found.")
        return

    df = pd.read_csv(master)

    print()
    print("Stations:", len(df))
    print("Columns:")
    print(df.columns.tolist())


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("python builder/audit/audit_network.py <Network>")
        raise SystemExit

    audit(sys.argv[1])