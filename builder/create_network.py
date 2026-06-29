from pathlib import Path
from builder.network_source import load_network


def create_network(network):

    master = load_network(network)

    output_folder = Path(f"data/{network.title()}")
    output_folder.mkdir(parents=True, exist_ok=True)

    output = output_folder / f"{network.lower()}_master.csv"

    master.to_csv(output, index=False)

    print()
    print(f"Network : {network}")
    print(f"Stations: {len(master)}")
    print(f"Saved   : {output}")


if __name__ == "__main__":

    import sys

    if len(sys.argv) != 2:
        print("Usage:")
        print("python builder/create_network.py <network>")
        raise SystemExit

    create_network(sys.argv[1])