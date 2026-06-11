import csv

seen = set()
dupes = []

with open(
    "/workspaces/playtheroute/data/Regions/southeastern_regions.csv",
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        station_id = row["station_id"]

        if station_id in seen:
            dupes.append(row)

        seen.add(station_id)

print("Unique stations:", len(seen))
print("Duplicate rows:", len(dupes))

for row in dupes:
    print(
        row["station_id"],
        row["crs"],
        row["station_name"]
    )