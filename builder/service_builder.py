import gzip
import xml.etree.ElementTree as ET
from pathlib import Path

from builder.reference.corpus import load_tiploc_lookup
from builder.services.pattern_builder import build_patterns

TIMETABLE = Path("data/Darwin/PPTimetable_20260702020500_v8.xml.gz")


def extract_service_path(journey, lookup):

    service = []
    unknown = 0

    for child in journey:

        child_tag = child.tag.split("}")[-1]

        if child_tag not in ("OR", "IP", "DT"):
            continue

        tiploc = child.attrib.get("tpl")

        info = lookup.get(tiploc)

        if info:
            service.append(info["crs"])
        else:
            service.append(f"UNKNOWN:{tiploc}")
            unknown += 1

    return service, unknown


def main():

    print("Starting Service Builder...")

    lookup = load_tiploc_lookup()

    print(f"Loaded {len(lookup):,} TIPLOC lookups")

    with gzip.open(TIMETABLE, "rb") as f:
        tree = ET.parse(f)

    root = tree.getroot()

    service_paths = []

    passenger_services = 0
    skipped_non_passenger = 0
    unknown_count = 0

    all_stations = set()

    shortest = None
    longest = 0
    total_length = 0

    empty_services = []

    for elem in root.iter():

        if elem.tag.split("}")[-1] != "Journey":
            continue

        if elem.attrib.get("isPassengerSvc") == "false":
            skipped_non_passenger += 1
            continue

        service, unknown = extract_service_path(elem, lookup)

        if len(service) == 0:
            empty_services.append(elem.attrib)
            continue

        service_paths.append(service)

        passenger_services += 1
        unknown_count += unknown

        service_length = len(service)

        total_length += service_length

        if shortest is None or service_length < shortest:
            shortest = service_length

        if service_length > longest:
            longest = service_length

        for crs in service:
            if not crs.startswith("UNKNOWN:"):
                all_stations.add(crs)

    average = total_length / passenger_services if passenger_services else 0

    print()
    print("==========================")
    print("Service Builder Report")
    print("==========================")
    print()

    print(f"Passenger services : {passenger_services:,}")
    print(f"Non-passenger      : {skipped_non_passenger:,}")
    print(f"Empty services     : {len(empty_services):,}")
    print(f"Service paths      : {len(service_paths):,}")
    print(f"Unique CRS stations: {len(all_stations):,}")
    print(f"Unknown TIPLOCs    : {unknown_count:,}")
    print(f"Shortest service   : {shortest}")
    print(f"Longest service    : {longest}")
    print(f"Average length     : {average:.2f}")

    if empty_services:

        print()
        print("First 10 empty passenger services:")

        for service in empty_services[:10]:
            print(service)

    print()
    print("First service:")
    print(service_paths[0])

    print()
    print("Last service:")
    print(service_paths[-1])

    print()
    print("Building service patterns...")

    patterns = build_patterns(service_paths)

    print(f"Unique service patterns : {len(patterns):,}")

    print()
    print("First pattern:")
    print(patterns[0])


if __name__ == "__main__":
    main()