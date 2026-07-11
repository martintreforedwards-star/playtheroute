from pathlib import Path
import json


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

KNOWLEDGEBASE = (
    ROOT
    / "data"
    / "knowledgebase"
    / "NT_network_data.json"
)


# ---------------------------------------------------------------------
# Load knowledgebase
# ---------------------------------------------------------------------

def load_knowledgebase():
    """
    Load the National Rail station knowledgebase.
    """

    print("Loading station knowledgebase...")
    print(f"File : {KNOWLEDGEBASE}")

    if not KNOWLEDGEBASE.exists():
        raise FileNotFoundError(
            f"Knowledgebase not found:\n{KNOWLEDGEBASE}"
        )

    with KNOWLEDGEBASE.open(
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    print(f"Top-level type : {type(data).__name__}")

    if isinstance(data, dict):
        print("Top-level keys:")
        for key in data.keys():
            print(f"  - {key}")

    return data


# ---------------------------------------------------------------------
# Build CRS lookup
# ---------------------------------------------------------------------

def build_lookup(data):
    """
    Build a lookup keyed by CRS code.
    """

    lookup = {}

    stations = data.get("stations", [])

    print(f"Stations found : {len(stations):,}")

    missing_crs = 0

    for station in stations:

        crs = station.get("crsCode")

        if not crs:
            missing_crs += 1
            continue

        lookup[crs] = station

    print(f"CRS lookups built : {len(lookup):,}")
    print(f"Missing CRS       : {missing_crs:,}")

    return lookup


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():

    data = load_knowledgebase()

    lookup = build_lookup(data)

    # Display one example record
    if lookup:

        first_crs = sorted(lookup.keys())[0]

        print()
        print("Example station")
        print("----------------")
        print(first_crs)

        for key in sorted(lookup[first_crs].keys()):
            print(f"{key}: {lookup[first_crs][key]}")


if __name__ == "__main__":
    main()