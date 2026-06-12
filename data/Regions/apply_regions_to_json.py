import csv
import json

# Load region mappings from CSV
regions = {}

with open(
    "data/Regions/southeastern_regions.csv",
    encoding="utf-8"
) as f:
    reader = csv.DictReader(f)

    for row in reader:
        regions[row["crs"].strip()] = row["region"].strip()

# Load station JSON
with open(
    "data/stations/southeastern.json",
    encoding="utf-8"
) as f:
    stations = json.load(f)

updated = 0
missing = []

for station in stations:

    crs = station.get("crs", "").strip()

    if crs in regions:
        station["region"] = regions[crs]
        updated += 1
    else:
        missing.append(station["station_name"])

# Save JSON
with open(
    "data/stations/southeastern.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(stations, f, indent=2)

print()
print("Stations updated:", updated)
print("Missing:", len(missing))

if missing:
    print()
    print("Missing stations:")
    for s in missing:
        print("-", s)
        