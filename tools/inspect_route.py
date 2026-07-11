import csv

from builder.services.pattern_builder import load_patterns


ROUTE_ID = "R00018"


def load_route(route_id):

    patterns = []

    with open(
        "data/Masters/route_candidates.csv",
        newline="",
        encoding="utf-8",
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:

            if row["route_id"] == route_id:
                patterns.append(row["pattern_id"])

    return patterns


def main():

    all_patterns = {
        pattern["pattern_id"]: pattern
        for pattern in load_patterns()
    }

    route_patterns = load_route(ROUTE_ID)

    print()
    print(f"Route {ROUTE_ID}")
    print("=" * (len(ROUTE_ID) + 6))
    print()

    print(f"Patterns : {len(route_patterns)}")
    print()

    for pattern_id in route_patterns:

        pattern = all_patterns.get(pattern_id)

        if pattern is None:
            continue

        print("-" * 70)

        print(
            f"{pattern_id}   "
            f"{pattern['origin']} → {pattern['destination']}   "
            f"({pattern['service_count']} services)"
        )

        print()
        print(" -> ".join(pattern["stations"]))
        print()


if __name__ == "__main__":
    main()