from itertools import combinations
from pathlib import Path

import pandas as pd


MASTER = Path("data/Masters")


def load_geometry():
    """Load the canonical route geometry."""
    return pd.read_csv(MASTER / "route_geometry.csv")


def longest_common_prefix(a, b):
    """Return the number of matching stations from the start."""

    count = 0

    for x, y in zip(a, b):
        if x != y:
            break
        count += 1

    return count


def longest_common_suffix(a, b):
    """Return the number of matching stations from the end."""

    count = 0

    for x, y in zip(reversed(a), reversed(b)):
        if x != y:
            break
        count += 1

    return count


def shared_station_count(a, b):
    """Return the number of stations shared by both routes."""

    return len(set(a) & set(b))


def overlap_percent(shared, len_a, len_b):
    """Calculate percentage overlap."""

    longest = max(len_a, len_b)

    if longest == 0:
        return 0.0

    return round((shared / longest) * 100, 1)


def compare_routes(route_a, route_b):
    """
    Compare two routes.

    Ignore routes that share neither an origin nor a destination.
    """

    if (
        route_a["origin"] != route_b["origin"]
        and route_a["destination"] != route_b["destination"]
    ):
        return None

    stations_a = route_a["station_sequence"].split("|")
    stations_b = route_b["station_sequence"].split("|")

    shared = shared_station_count(stations_a, stations_b)

    return {
        "route_a": route_a["route_id"],
        "route_b": route_b["route_id"],
        "route_a_length": len(stations_a),
        "route_b_length": len(stations_b),
        "shared_prefix": longest_common_prefix(
            stations_a,
            stations_b,
        ),
        "shared_suffix": longest_common_suffix(
            stations_a,
            stations_b,
        ),
        "shared_stations": shared,
        "overlap_percent": overlap_percent(
            shared,
            len(stations_a),
            len(stations_b),
        ),
    }


def build_relationships(geometry):
    """Compare every relevant pair of routes."""

    rows = []

    total_pairs = 0

    for (_, route_a), (_, route_b) in combinations(
        geometry.iterrows(), 2
    ):

        total_pairs += 1

        result = compare_routes(route_a, route_b)

        if result is not None:
            rows.append(result)

    print(f"Possible comparisons : {total_pairs:,}")
    print(f"Stored comparisons   : {len(rows):,}")

    return pd.DataFrame(rows)


def main():

    geometry = load_geometry()

    print(f"Loaded {len(geometry):,} routes")

    relationships = build_relationships(geometry)

    outfile = MASTER / "route_relationships.csv"

    relationships.to_csv(outfile, index=False)

    print()
    print(f"Saved {outfile}")
    print()

    print(relationships.head(20).to_string(index=False))


if __name__ == "__main__":
    main()