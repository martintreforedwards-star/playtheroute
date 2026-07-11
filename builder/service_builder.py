from pathlib import Path

from builder.reference.corpus import load_tiploc_lookup
from builder.services.extractor import extract_service_paths
from builder.services.pattern_builder import (
    build_patterns,
    save_patterns,
    report_patterns,
)

TIMETABLE = Path("data/Darwin/PPTimetable_20260702020500_v8.xml.gz")


def main():

    print("Starting Service Builder...")
    print()

    lookup = load_tiploc_lookup()

    print(f"Loaded {len(lookup):,} TIPLOC lookups")

    service_paths, stats = extract_service_paths(
        TIMETABLE,
        lookup,
    )

    print()
    print("==========================")
    print("Service Builder Report")
    print("==========================")
    print()

    print(f"Passenger services : {stats['passenger_services']:,}")
    print(f"Non-passenger      : {stats['non_passenger']:,}")
    print(f"No CRS locations   : {stats['empty_services']:,}")
    print(f"Unknown TIPLOCs    : {stats['unknown_tiplocs']:,}")
    print(f"Service paths      : {len(service_paths):,}")

    if stats["empty_services"]:

        print()
        print(
            "Note: These journeys contain only non-CRS locations "
            "(e.g. operational points or rail replacement bus stops)."
        )

    if stats["empty_examples"]:

        print()
        print("First journeys with no CRS locations:")

        for journey in stats["empty_examples"]:
            print(journey)

    print()
    print("First service:")
    print(service_paths[0])

    print()
    print("Last service:")
    print(service_paths[-1])

    print()
    print("Building service patterns...")

    patterns = build_patterns(service_paths)

    save_patterns(patterns)

    print()
    print(f"Unique service patterns : {len(patterns):,}")

    report_patterns(patterns)


if __name__ == "__main__":
    main()