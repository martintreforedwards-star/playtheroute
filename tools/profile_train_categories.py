import gzip
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

TIMETABLE = Path("data/Darwin/PPTimetable_20260702020500_v8.xml.gz")

counts = Counter()

with gzip.open(TIMETABLE, "rb") as f:
    tree = ET.parse(f)

root = tree.getroot()

for journey in root.iter():

    if journey.tag.split("}")[-1] != "Journey":
        continue

    cat = journey.attrib.get("trainCat", "(none)")
    counts[cat] += 1

print()

print("Train Categories")
print("----------------")

for cat, count in counts.most_common():
    print(f"{cat:5} {count:7}")