import csv

# Load CRS source
crs_lookup = {}

with open("../../crs_source_of_truth.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        crs_lookup[row["stationName"].strip().lower()] = row["crsCode"]

# Load v2 station names
v2 = set()

with open("southern_master_v2.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        v2.add(row["station_name"])

# Find new stations
new_stations = []

with open("southern_master_v3.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        station = row["station_name"]

        if station not in v2:
            new_stations.append(station)

print("New stations:", len(new_stations))
print()

matched = 0
missing = 0

for station in sorted(new_stations):

    key = station.lower()

    if key in crs_lookup:
        print(f"✓ {station} -> {crs_lookup[key]}")
        matched += 1
    else:
        print(f"✗ {station}")
        missing += 1

print()
print("Matched:", matched)
print("Missing:", missing)