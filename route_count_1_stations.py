import json

with open("data/stations/southeastern.json") as f:
    stations = json.load(f)

stations = sorted(stations, key=lambda s: s["station_name"])

print()
print("========================================")
print("ROUTE COUNT = 1")
print("========================================")
print()

count = 0

for s in stations:
    if s.get("route_count") == 1:
        print(s["station_name"])
        count += 1

print()
print("Total:", count)
