import json
from pathlib import Path

JSON_FILE = Path("data/stations/southeastern.json")

with open(JSON_FILE, "r", encoding="utf-8") as f:
    stations = json.load(f)

interchanges = []

for station in stations:

    if station.get("is_interchange") is True:
        interchanges.append(station["station_name"])

print("=" * 70)
print("INTERCHANGE STATIONS")
print("=" * 70)

for station in sorted(interchanges):
    print(station)

print()
print(f"TOTAL: {len(interchanges)}")