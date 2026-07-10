import gzip
import xml.etree.ElementTree as ET

filename = "data/Darwin/PPTimetable_20260702020500_v8.xml.gz"

with gzip.open(filename, "rb") as f:
    tree = ET.parse(f)

root = tree.getroot()

tiplocs = set()

for elem in root.iter():
    tag = elem.tag.split("}")[-1]
    if tag in ("OR", "IP", "DT", "OPOR", "OPIP", "OPDT"):
        tpl = elem.attrib.get("tpl")
        if tpl:
            tiplocs.add(tpl)

print(f"Unique TIPLOCs: {len(tiplocs)}")

print("\nFirst 50:")

for tpl in sorted(tiplocs)[:50]:
    print(tpl)