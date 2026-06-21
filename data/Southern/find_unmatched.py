import csv

v2 = set()

with open("southern_master_v2.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        v2.add(row["station_name"])

v3 = set()

with open("southern_master_v3.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        v3.add(row["station_name"])

print("In v3 but not v2:\n")

for station in sorted(v3 - v2):
    print(station)

print("\nIn v2 but not v3:\n")

for station in sorted(v2 - v3):
    print(station)

    