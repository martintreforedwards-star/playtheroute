import csv

# Load mappings
region_map = {}

with open(
    "/workspaces/playtheroute/data/Regions/southeastern_region_map.csv",
    newline="",
    encoding="utf-8"
) as f:
    reader = csv.DictReader(f)

    for row in reader:
        region_map[row["crs"]] = row["region"]

# Update region file
rows = []

with open(
    "/workspaces/playtheroute/data/Regions/southeastern_regions.csv",
    newline="",
    encoding="utf-8"
) as f:
    reader = csv.DictReader(f)

    for row in reader:

        crs = row["crs"]

        if crs in region_map:
            row["region"] = region_map[crs]

        rows.append(row)

# Save
with open(
    "/workspaces/playtheroute/data/Regions/southeastern_regions.csv",
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

print("Regions applied")