import gzip
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

TIMETABLE = Path("data/Darwin/PPTimetable_20260702020500_v8.xml.gz")


def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("python tools/inspect_journey.py <RID>")
        return

    rid = sys.argv[1]

    print(f"Searching for RID {rid}...")

    with gzip.open(TIMETABLE, "rb") as f:
        tree = ET.parse(f)

    root = tree.getroot()

    for elem in root.iter():

        if elem.tag.split("}")[-1] != "Journey":
            continue

        if elem.attrib.get("rid") != rid:
            continue

        print("\nJourney attributes")
        print("------------------")

        for k, v in elem.attrib.items():
            print(f"{k:15} {v}")

        print("\nChild elements")
        print("--------------")

        for child in elem:
            print(child.tag.split("}")[-1], child.attrib)

        print("\nRaw XML")
        print("-------")

        print(ET.tostring(elem, encoding="unicode"))

        return

    print("Journey not found")


if __name__ == "__main__":
    main()