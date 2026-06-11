import csv
import json

# Load master stations
master_lookup = {}

with open(
    "/workspaces/playtheroute/data/Masters/master_station.csv",
    newline="",
    encoding="utf-8"
) as f:
    reader = csv.DictReader(f)

    for row in reader:
        crs = row["crs"].strip()
        master_lookup[crs] = {
            "station_id": row["station_id"],
            "station_name": row["station_name"]
        }

# Load Southeastern JSON
with open(
    "/workspaces/playtheroute/data/stations/southeastern.json",
    "r",
    encoding="utf-8"
) as f:
    se_data = json.load(f)

# Build output rows
rows = []

seen = set()

for station in se_data:

    crs = station["crs"].strip()

    if crs in master_lookup:

        station_id = master_lookup[crs]["station_id"]

        if station_id not in seen:

            rows.append({
                "station_id": station_id,
                "crs": crs,
                "station_name": master_lookup[crs]["station_name"],
                "region": ""
            })

            seen.add(station_id)

# Sort alphabetically
rows = sorted(rows, key=lambda x: x["station_name"])

# Save
output_file = (
    "/workspaces/playtheroute/data/Regions/"
    "southeastern_regions.csv"
)

with open(
    output_file,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "station_id",
            "crs",
            "station_name",
            "region"
        ]
    )

    writer.writeheader()
    writer.writerows(rows)

print("Created:", output_file)
print("Stations:", len(rows))