import gzip
import xml.etree.ElementTree as ET

filename = "data/Darwin/PPTimetable_20260702020500_v8.xml.gz"

with gzip.open(filename, "rb") as f:
    tree = ET.parse(f)

root = tree.getroot()

print(root.tag)

# Print the first 20 unique element names
tags = set()
for elem in root.iter():
    tags.add(elem.tag.split("}")[-1])

for tag in sorted(tags)[:100]:
    print(tag)