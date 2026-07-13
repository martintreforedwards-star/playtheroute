import csv

stations = []

with open("southern_master_v3.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        stations.append(row["station_name"])

v2 = set()

with open("southern_master_v2.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        v2.add(row["station_name"])

new_stations = [s for s in stations if s not in v2]

print("New stations:", len(new_stations))

for s in sorted(new_stations):
    print(s)