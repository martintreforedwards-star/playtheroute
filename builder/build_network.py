import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from builder.config import load_config
from builder.assemble import build_master
from builder.generate_network_membership import generate_network_membership
from builder.enrichment import enrich
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

    # Stage 1
    build_master(config)

    # Stage 2
    print("Building network memberships...")
    generate_network_membership(config)
    print("Network memberships complete.")

    # Stage 3
    stations = enrich(config)

    print("\nColumns returned from enrichment:")
    print(stations.columns.tolist())

    # Stage 4
    build_json(config)

    # Stage 5
    analyse(config)

    # Stage 6
    generate(config)

    # Stage 7
    validate(stations)

    print("\nBuild complete.")


if __name__ == "__main__":
    main()