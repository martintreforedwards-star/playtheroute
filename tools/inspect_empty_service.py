import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import gzip
import xml.etree.ElementTree as ET
from pathlib import Path

from builder.reference.corpus import load_tiploc_lookup

TIMETABLE = Path("data/Darwin/PPTimetable_20260702020500_v8.xml.gz")

RID = "202607026711967"


def main():

    print(f"Inspecting {RID}")
    print()

    lookup = load_tiploc_lookup()

    with gzip.open(TIMETABLE, "rb") as f:
        tree = ET.parse(f)

    root = tree.getroot()

    for journey in root.iter():

        if journey.tag.split("}")[-1] != "Journey":
            continue

        if journey.attrib.get("rid") != RID:
            continue

        print("Journey attributes")
        print("------------------")

        for key, value in journey.attrib.items():
            print(f"{key:18} {value}")

        print()
        print("Locations")
        print("---------")

        for child in journey:

            tag = child.tag.split("}")[-1]

            tpl = child.attrib.get("tpl", "")

            info = lookup.get(tpl)

            if info:

                crs = info.get("crs", "")
                name = info.get("name", "")

                print(
                    f"{tag:5} "
                    f"{tpl:12} "
                    f"CRS={crs or '(none)':5} "
                    f"{name}"
                )

            else:

                print(
                    f"{tag:5} "
                    f"{tpl:12} "
                    "NOT FOUND"
                )

        return

    print("Journey not found.")


if __name__ == "__main__":
    main()