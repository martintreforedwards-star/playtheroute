import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from builder.config import load_config
from builder.assemble import build_master
from builder.generate_network_membership import generate_network_membership
from builder.enrichment import enrich
from builder.enrichers.derive_terminus import derive_terminus
from builder.enrichers.route_lookup import apply_route_lookup
from builder.import_reference_data import import_reference_data
from builder.validators import validate
from builder.json_builder import build_json
from builder.analyser.analyse_network import analyse
from builder.generate_clues import generate


def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("python builder/build_network.py <network>")
        return

    requested_network = sys.argv[1]

    config = load_config(requested_network)

    network = config.get(
        "network",
        config.get(
            "display_name",
            requested_network,
        ),
    )

    print(f"\n=== Building {requested_network} ===")
    print(f"Network : {network}")

    #
    # Build master network
    #
    build_master(config)

    #
    # Route membership
    #
    print("Building network memberships...")
    generate_network_membership(config)
    print("Network memberships complete.")

    #
    # Enrichment
    #
    stations = enrich(config)

    #
    # Derive termini
    #
    derive_terminus(config)

    #
    # Import reference data
    #
    stations = import_reference_data(config, stations)

    #
    # Apply route lookup
    #
    apply_route_lookup(config)

    #
    # Reload enriched CSV so subsequent stages use the latest data
    #
    csv_path = (
        Path("data/Class1")
        / config["network"]
        / f"{config['network'].lower()}.csv"
    )

    stations = pd.read_csv(csv_path)

    print("\nColumns returned from enrichment:")
    print(stations.columns.tolist())

    #
    # JSON
    #
    build_json(config)

    #
    # Analysis
    #
    analyse(config)

    #
    # Clues
    #
    generate(config)

    #
    # Validation
    #
    validate(stations)

    print("\nBuild complete.")


if __name__ == "__main__":
    main()