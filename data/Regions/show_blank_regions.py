import csv

with open(
    "/workspaces/playtheroute/data/Regions/southeastern_regions.csv",
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:
        if not row["region"].strip():
            print(
                row["crs"],
                "-",
                row["station_name"]
            )