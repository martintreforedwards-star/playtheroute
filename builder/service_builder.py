import gzip
import xml.etree.ElementTree as ET
from pathlib import Path

from builder.reference.corpus import load_tiploc_lookup

TIMETABLE = Path("data/Darwin/PPTimetable_20260702020500_v8.xml.gz")


def main():

    print("Starting Service Builder...")

    lookup = load_tiploc_lookup()

    print(f"Loaded {len(lookup):,} TIPLOC lookups")

    print("\nOpening timetable...")

    with gzip.open(TIMETABLE, "rb") as f:
        tree = ET.parse(f)

    root = tree.getroot()

    print(root.tag)

    print("\nSearching for first Journey...")

    for elem in root.iter():

        tag = elem.tag.split("}")[-1]

        if tag != "Journey":
            continue

        print("Journey found!")
        print(elem.attrib)

        print("\nLocations:")

        service = []

        for child in elem:

            child_tag = child.tag.split("}")[-1]

            if child_tag not in ("OR", "IP", "DT"):
                continue

            tiploc = child.attrib.get("tpl")

            info = lookup.get(tiploc)

            if info:

                service.append(info["crs"])

                print(
                    child_tag,
                    f"{tiploc:10}",
                    "→",
                    f"{info['crs']:3}",
                    info["name"],
                )

            else:

                service.append(f"UNKNOWN:{tiploc}")

                print(
                    child_tag,
                    f"{tiploc:10}",
                    "→ UNKNOWN",
                )

        print("\nService path:")
        print(service)

        break


if __name__ == "__main__":
    main()