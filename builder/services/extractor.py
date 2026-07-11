import gzip
import xml.etree.ElementTree as ET


PASSENGER_LOCATION_TYPES = {
    "OR",
    "IP",
    "DT",
    "OPOR",
    "PP",
    "OPDT",
}


def extract_service_paths(timetable_path, lookup):
    """
    Extract passenger rail service paths from a Darwin timetable.
    """

    with gzip.open(timetable_path, "rb") as f:
        tree = ET.parse(f)

    root = tree.getroot()

    service_paths = []

    stats = {
        "passenger_services": 0,
        "non_passenger": 0,
        "empty_services": 0,
        "unknown_tiplocs": 0,
        "empty_examples": [],
    }

    for journey in root.iter():

        if journey.tag.split("}")[-1] != "Journey":
            continue

        #
        # Darwin v11+ explicitly tells us whether a service is passenger.
        # Support both documented attribute names.
        #
        is_passenger = journey.attrib.get("isPassengerSvc")

        if is_passenger is None:
            is_passenger = journey.attrib.get("isPassengerService")

        if is_passenger == "false":
            stats["non_passenger"] += 1
            continue

        service = []

        for child in journey:

            tag = child.tag.split("}")[-1]

            if tag not in PASSENGER_LOCATION_TYPES:
                continue

            tiploc = child.attrib.get("tpl")

            info = lookup.get(tiploc)

            if info is None:
                stats["unknown_tiplocs"] += 1
                continue

            crs = info.get("crs", "").strip()

            # Ignore operational locations without CRS codes
            if crs:
                service.append(crs)

        if not service:

            stats["empty_services"] += 1

            if len(stats["empty_examples"]) < 20:
                stats["empty_examples"].append(journey.attrib)

            continue

        service_paths.append(service)
        stats["passenger_services"] += 1

    return service_paths, stats