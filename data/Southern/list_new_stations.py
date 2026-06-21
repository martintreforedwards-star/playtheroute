import csv

v2 = set()

with open("southern_master_v2.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        v2.add(row["station_name"])

with open("southern_master_v3.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["station_name"] not in v2:
            print(row["station_name"])