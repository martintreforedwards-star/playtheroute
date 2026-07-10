import gzip
import xml.etree.ElementTree as ET

filename = "data/Darwin/PPTimetable_20260702020500_v8.xml.gz"

with gzip.open(filename, "rb") as f:
    tree = ET.parse(f)

root = tree.getroot()

tags = ("OR", "IP", "DT", "OPOR", "OPIP", "OPDT")

count = 0

for elem in root.iter():
    tag = elem.tag.split("}")[-1]
    if tag in tags:
        count += 1
        if "tpl" not in elem.attrib:
            print("Missing tpl:", tag, elem.attrib)
            break

print(f"Checked {count} location records.")
print("Done.")