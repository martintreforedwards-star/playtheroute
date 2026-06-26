"""
Generic Network Builder

Usage:
    python builder/build_network.py scotrail
    python builder/build_network.py northern
"""

import sys
from pathlib import Path

# Allow imports when running this file directly
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from builder.config import load_config
from builder.loaders import load_network


def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("    python builder/build_network.py <network>")
        sys.exit(1)

    network_name = sys.argv[1]

    print(f"\n=== Building {network_name} ===")

    # Load configuration
    config = load_config(network_name)

    # Load master dataset
    network = load_network(config)

    # Summary
    print(f"Network : {network.name}")
    print(f"Stations: {len(network.stations)}")

    print("\nSUCCESS")


if __name__ == "__main__":
    main()