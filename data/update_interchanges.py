import json

# Read interchange list
with open("data/interchanges.txt") as f:
    interchanges = {
        line.strip()
        for line in f
        if line.strip()
    }

# Read station data
with open("data/stations/southeastern.json") as f:
    stations = json.load(f)

for station in stations:
    station["is_interchange"] = (
        station["station_name"] in interchanges
    )

# Save updated JSON
with open("data/stations/southeastern.json", "w") as f:
    json.dump(stations, f, indent=2)

print("Stations processed:", len(stations))
print("Interchanges set:", len(interchanges))
print("Done.")