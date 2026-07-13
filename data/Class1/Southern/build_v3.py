from routes_v3 import southern_route_templates
import csv

stations = set()

for route in southern_route_templates:
    for station in route:
        stations.add(station)

stations = sorted(stations)

with open("southern_master_v3.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "station_id",
        "station_name"
    ])

    for i, station in enumerate(stations, start=1):
        writer.writerow([
            f"SR{i:03}",
            station
        ])

print("Stations exported:", len(stations))