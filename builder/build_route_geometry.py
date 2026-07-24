from pathlib import Path

import pandas as pd


MASTER = Path("data/Masters")


def load_routes():
    return pd.read_csv(MASTER / "routes.csv")


def load_patterns():
    return pd.read_csv(MASTER / "service_patterns.csv")


def build_geometry(routes, patterns):
    """
    Build one canonical geometry for every route.

    Version 1 uses the route's longest service pattern.
    """

    lookup = patterns.set_index("pattern_id")

    rows = []

    for _, route in routes.iterrows():

        pattern_id = route["longest_pattern"]

        if pattern_id not in lookup.index:
            print(f"WARNING: Pattern {pattern_id} not found")
            continue

        pattern = lookup.loc[pattern_id]

        stations = pattern["stations"]

        station_list = stations.split("|")

        rows.append(
            {
                "route_id": route["route_id"],
                "pattern_id": pattern_id,
                "origin": pattern["origin"],
                "destination": pattern["destination"],
                "station_count": len(station_list),
                "station_sequence": stations,
            }
        )

    return pd.DataFrame(rows)


def main():

    routes = load_routes()
    patterns = load_patterns()

    geometry = build_geometry(routes, patterns)

    outfile = MASTER / "route_geometry.csv"

    geometry.to_csv(outfile, index=False)

    print(f"Saved {outfile}")
    print()

    print(f"Routes : {len(geometry)}")

    print()
    print(geometry.head(10).to_string(index=False))


if __name__ == "__main__":
    main()