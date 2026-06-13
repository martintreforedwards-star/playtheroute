import json
from pathlib import Path

JSON_FILE = Path("data/stations/southeastern.json")
GROUP_FILE = Path("data/Southeastern/route_group_definitions.txt")

with open(JSON_FILE, "r", encoding="utf-8") as f:
    stations = json.load(f)

station_lookup = {
    s["station_name"]: s
    for s in stations
}

groups = {}
current_group = None

with open(GROUP_FILE, "r", encoding="utf-8") as f:
    for raw in f:
        line = raw.strip()

        if not line:
            continue

        if line.startswith("[") and line.endswith("]"):
            current_group = line[1:-1]
            groups[current_group] = []
            continue

        groups[current_group].append(line)

assigned = 0
missing = []

for station in stations:
    station["route_groups"] = []

for group_name, members in groups.items():
    for station_name in members:

        station = station_lookup.get(station_name)

        if not station:
            missing.append(station_name)
            continue

        station["route_groups"].append(group_name)
        assigned += 1

for station in stations:
    station["is_high_speed"] = (
        "High Speed 1" in station["route_groups"]
    )

with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(stations, f, indent=2)

print()
print("Stations:", len(stations))
print("Assignments:", assigned)
print("Missing station names:", len(missing))

if missing:
    print()
    print("Missing:")
    for m in sorted(set(missing)):
        print(" -", m)

print()
print(
    "High Speed stations:",
    sum(
        1
        for s in stations
        if s.get("is_high_speed")
    )
)

print("Done.")