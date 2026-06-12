import csv
import json

with open("data/stations/southeastern.json", encoding="utf-8") as f:
    stations = json.load(f)

valid_crs = {s["crs"] for s in stations}

missing = []

with open(
    "data/Southeastern/route_group_membership.csv",
    encoding="utf-8"
) as f:
    reader = csv.DictReader(f)

    for row in reader:
        crs = row["crs"].strip()

        if crs not in valid_crs:
            missing.append(crs)

if missing:
    print("Unknown CRS codes:")
    for crs in sorted(set(missing)):
        print(crs)
else:
    print("All CRS codes valid")