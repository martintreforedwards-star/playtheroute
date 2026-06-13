import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent
JSON_FILE = ROOT.parent / "stations" / "southeastern.json"


def load_data():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    stations = load_data()

    print("=" * 70)
    print("SOUTHEASTERN AUDIT")
    print("=" * 70)

    print(f"\nStations loaded: {len(stations)}\n")

    required_fields = [
        "route_station_id",
        "crs",
        "station_name",
        "region",
        "route_groups",
        "difficulty_score",
        "accessibility_score",
        "is_coastal",
    ]

    missing_fields = []
    duplicate_crs = []
    empty_route_groups = []
    invalid_route_groups = []

    region_counter = Counter()
    route_group_counter = Counter()
    coastal_counter = Counter()
    difficulty_counter = Counter()
    accessibility_counter = Counter()
    crs_counter = Counter()

    for station in stations:

        name = station.get("station_name", "<unknown>")
        crs = station.get("crs", "")

        crs_counter[crs] += 1

        # Required fields
        for field in required_fields:
            if field not in station:
                missing_fields.append(
                    f"{name} ({crs}) missing '{field}'"
                )

        # Region stats
        region = station.get("region")
        if region:
            region_counter[region] += 1

        # Route groups
        route_groups = station.get("route_groups", [])

        if not route_groups:
            empty_route_groups.append(
                f"{name} ({crs})"
            )

        for group in route_groups:
            route_group_counter[group] += 1

        # Coastal
        coastal_counter[str(station.get("is_coastal"))] += 1

        # Difficulty
        difficulty = station.get("difficulty_score")
        if difficulty is not None:
            difficulty_counter[difficulty] += 1

        # Accessibility
        accessibility = station.get("accessibility_score")
        if accessibility is not None:
            accessibility_counter[accessibility] += 1

    # Duplicate CRS check
    for crs, count in crs_counter.items():
        if count > 1:
            duplicate_crs.append(
                f"{crs} ({count} records)"
            )

    print("-" * 70)
    print("MISSING REQUIRED FIELDS")
    print("-" * 70)

    if missing_fields:
        for issue in missing_fields:
            print(f"❌ {issue}")
    else:
        print("✅ None")

    print("\n" + "-" * 70)
    print("DUPLICATE CRS CODES")
    print("-" * 70)

    if duplicate_crs:
        for issue in duplicate_crs:
            print(f"❌ {issue}")
    else:
        print("✅ None")

    print("\n" + "-" * 70)
    print("STATIONS WITH NO ROUTE GROUPS")
    print("-" * 70)

    if empty_route_groups:
        print(f"Count: {len(empty_route_groups)}\n")

        for station in empty_route_groups:
            print(f"❌ {station}")
    else:
        print("✅ All stations assigned")

    print("\n" + "-" * 70)
    print("REGION DISTRIBUTION")
    print("-" * 70)

    for region, count in sorted(region_counter.items()):
        print(f"{region:<25} {count}")

    print("\n" + "-" * 70)
    print("ROUTE GROUP DISTRIBUTION")
    print("-" * 70)

    if route_group_counter:
        for group, count in sorted(route_group_counter.items()):
            print(f"{group:<35} {count}")
    else:
        print("No route groups found")

    print("\n" + "-" * 70)
    print("COASTAL DISTRIBUTION")
    print("-" * 70)

    for value, count in sorted(coastal_counter.items()):
        print(f"{value:<10} {count}")

    print("\n" + "-" * 70)
    print("DIFFICULTY SCORE DISTRIBUTION")
    print("-" * 70)

    for score, count in sorted(difficulty_counter.items()):
        print(f"{score:<10} {count}")

    print("\n" + "-" * 70)
    print("ACCESSIBILITY SCORE DISTRIBUTION")
    print("-" * 70)

    for score, count in sorted(accessibility_counter.items()):
        print(f"{score:<10} {count}")

    print("\n" + "=" * 70)
    print("AUDIT COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()