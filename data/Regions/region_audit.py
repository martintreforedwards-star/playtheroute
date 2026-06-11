import csv

filled = 0
blank = 0

with open(
    "/workspaces/playtheroute/data/Regions/southeastern_regions.csv",
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:
        if row["region"].strip():
            filled += 1
        else:
            blank += 1

print("Filled:", filled)
print("Blank:", blank)
print("Total:", filled + blank)