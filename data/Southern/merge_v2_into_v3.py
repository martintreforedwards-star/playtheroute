import csv

# Load v2
v2 = {}

with open("southern_master_v2.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        v2[row["station_name"]] = row

# Read v3 station list
with open("southern_master_v3.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    v3_rows = list(reader)

header = [
    "station_id",
    "station_name",
    "crs",
    "operator",
    "route",
    "county",
    "latitude",
    "longitude",
    "major_interchange",
    "terminus",
    "branch_junction",
    "nearest_landmark",
    "nearest_landmark_km",
    "nearest_castle",
    "nearest_castle_km",
    "nearest_cathedral",
    "nearest_cathedral_km",
    "nearest_museum",
    "nearest_museum_km",
    "nearest_country_house",
    "nearest_country_house_km",
    "nearest_nature_reserve",
    "nearest_nature_reserve_km",
    "route_count",
    "service_count",
    "service_density",
    "route_diversity_band",
    "time_from_london",
    "time_band",
    "accessibility_score",
    "difficulty_score"
]

matched = 0
new = 0

with open(
    "southern_master_v3_enriched.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()

    for row in v3_rows:

        station = row["station_name"]

        if station in v2:

            writer.writerow(v2[station])
            matched += 1

        else:

            blank = {col: "" for col in header}

            blank["station_id"] = row["station_id"]
            blank["station_name"] = station

            writer.writerow(blank)

            new += 1

print("Matched:", matched)
print("New stations:", new)