import csv

stations = {}

with open("crs_source_of_truth.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        stations[row["stationName"]] = row

print("Stations loaded:", len(stations))

missing = []

with open("gwr_missing_confirmed.txt", encoding="utf-8") as f:
    for line in f:
        station = line.strip()

        if station in stations:
            missing.append(station)
        elif station == "Bradford-on-Avon" and "Bradford-On-Avon" in stations:
            missing.append("Bradford-On-Avon")
        else:
            print("NOT FOUND:", station)

print()
print("Matched:", len(missing))

for station in missing:
    print(station)
