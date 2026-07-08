import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from builder.config import load_config
from builder.assemble import build_master
from builder.enrichment import enrich
from builder.validators import validate
from builder.clue_builder import build_clues
from builder.json_builder import build_json


def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("python builder/build_network.py <network>")
        return

    network = sys.argv[1]

    config = load_config(network)

    print(f"\n=== Building {network} ===")

    network_name = (
        config.get("display_name")
        or config.get("network")
        or config.get("name", network)
    )

    print(f"Network : {network_name}")

    build_master(config)

    stations = enrich(config)

    print("\nColumns returned from enrichment:")
    print(stations.columns.tolist())

    validate(stations)

    if config.get("clue_template"):
        build_clues(config)
    else:
        print("Skipping clue generation (no clue template configured).")

    build_json(config)

    print("\nBuild complete.")


if __name__ == "__main__":
    main()