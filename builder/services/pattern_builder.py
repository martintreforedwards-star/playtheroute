from collections import defaultdict
from pathlib import Path

import csv


OUTPUT = Path("data/Masters/service_patterns.csv")


def build_patterns(service_paths):
    """
    Convert service paths into unique service patterns.
    """

    counts = defaultdict(int)

    for service in service_paths:
        counts[tuple(service)] += 1

    patterns = []

    for i, (stations, count) in enumerate(counts.items(), start=1):

        patterns.append(
            {
                "pattern_id": f"SP{i:06d}",
                "service_count": count,
                "station_count": len(stations),
                "origin": stations[0],
                "destination": stations[-1],
                "stations": list(stations),
            }
        )

    return patterns


def save_patterns(patterns):

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "pattern_id",
                "service_count",
                "station_count",
                "origin",
                "destination",
                "stations",
            ]
        )

        for pattern in patterns:

            writer.writerow(
                [
                    pattern["pattern_id"],
                    pattern["service_count"],
                    pattern["station_count"],
                    pattern["origin"],
                    pattern["destination"],
                    "|".join(pattern["stations"]),
                ]
            )
def report_patterns(patterns):

    print()
    print("==========================")
    print("Pattern Report")
    print("==========================")
    print()

    print(f"Patterns discovered : {len(patterns):,}")

    service_counts = [p["service_count"] for p in patterns]
    station_counts = [p["station_count"] for p in patterns]

    print(f"Most common pattern : {max(service_counts)} services")
    print(f"Least common pattern: {min(service_counts)} services")
    print(f"Average frequency   : {sum(service_counts) / len(service_counts):.2f}")

    print()

    print(f"Longest pattern     : {max(station_counts)} stations")
    print(f"Shortest pattern    : {min(station_counts)} stations")
    print(f"Average length      : {sum(station_counts) / len(station_counts):.2f}")

    print()
    print("Top 20 service patterns")
    print("-----------------------")

    ranked = sorted(
        patterns,
        key=lambda p: p["service_count"],
        reverse=True,
    )

    for pattern in ranked[:20]:

        print(
            f'{pattern["pattern_id"]:9} '
            f'{pattern["service_count"]:5} services   '
            f'{pattern["origin"]:3} → {pattern["destination"]:3}   '
            f'({pattern["station_count"]:2} stations)'
        )
    print(f"Saved: {OUTPUT}")