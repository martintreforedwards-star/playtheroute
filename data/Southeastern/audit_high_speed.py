import json
from pathlib import Path

JSON_FILE = Path("data/stations/southeastern.json")

with open(JSON_FILE, "r", encoding="utf-8") as f:
    stations = json.load(f)

print("=" * 70)
print("HIGH SPEED FLAG")
print("=" * 70)

high_speed_flag = []

for station in stations:
    if station.get("is_high_speed") is True:
        high_speed_flag.append(station["station_name"])

for station in sorted(high_speed_flag):
    print(station)

print()
print(f"TOTAL: {len(high_speed_flag)}")

print()
print("=" * 70)
print("HIGH SPEED ROUTE GROUP")
print("=" * 70)

high_speed_group = []

for station in stations:
    route_groups = station.get("route_groups", [])

    if "High Speed 1" in route_groups:
        high_speed_group.append(station["station_name"])

for station in sorted(high_speed_group):
    print(station)

print()
print(f"TOTAL: {len(high_speed_group)}")

print()
print("=" * 70)
print("FLAGGED BUT NOT IN GROUP")
print("=" * 70)

for station in sorted(set(high_speed_flag) - set(high_speed_group)):
    print(station)

print()
print("=" * 70)
print("IN GROUP BUT NOT FLAGGED")
print("=" * 70)

for station in sorted(set(high_speed_group) - set(high_speed_flag)):
    print(station)