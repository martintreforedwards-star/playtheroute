import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from builder.config import load_config
from builder.assemble import build_master
from builder.enrichment import enrich


def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("python builder/build_network.py <network>")
        return

    network = sys.argv[1]

    config = load_config(network)

    print(f"\n=== Building {network} ===")
    print(f"Network : {config['name']}")

    build_master(config)

    enrich(config)

    print("\nBuild complete.")


if __name__ == "__main__":
    main()