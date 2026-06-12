import json

# Load coastal station names
with open(
    "data/Southeastern/coastal_stations.txt",
    encoding="utf-8"
) as f:
    coastal_stations = {
        line.strip()
        for line in f
        if line.strip()
    }

# Load station data
with open(
    "data/stations/southeastern.json",
    encoding="utf-8"
) as f:
    stations = json.load(f)

coastal_count = 0

for station in stations:

    station["is_coastal"] = (
        station["station_name"] in coastal_stations
    )

    if station["is_coastal"]:
        coastal_count += 1

# Save updated station data
with open(
    "data/stations/southeastern.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(stations, f, indent=2)

print(f"Stations processed: {len(stations)}")
print(f"Coastal stations: {coastal_count}")
print("Done.")