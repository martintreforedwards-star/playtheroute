import csv
import json
from collections import defaultdict

# Load route group memberships
route_groups = defaultdict(list)

with open(
    "data/Southeastern/route_group_membership.csv",
    encoding="utf-8"
) as f:
    reader = csv.DictReader(f)

    for row in reader:
        crs = row["crs"].strip()
        group = row["route_group"].strip()

        route_groups[crs].append(group)

# Load stations
with open(
    "data/stations/southeastern.json",
    encoding="utf-8"
) as f:
    stations = json.load(f)

updated = 0

for station in stations:

    crs = station.get("crs", "").strip()

    if crs in route_groups:
        station["route_groups"] = sorted(route_groups[crs])
        updated += 1
    else:
        station["route_groups"] = []

# Save stations
with open(
    "data/stations/southeastern.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(stations, f, indent=2)

print(f"Stations processed: {len(stations)}")
print(f"Stations with route groups: {updated}")
print("Done.")