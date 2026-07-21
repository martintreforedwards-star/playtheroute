import csv

SOURCE = r"data/Class1/Southern/southern_terminus_3_completed.csv"
TARGET = r"data/Class1/Southern/southern.csv"

lookup = {}

with open(SOURCE, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        lookup[row["crs"].strip().upper()] = row["terminus"]

rows = []

with open(TARGET, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames

    for row in reader:
        crs = row["crs"].strip().upper()
        if crs in lookup:
            row["is_terminus"] = lookup[crs]
        rows.append(row)

with open(TARGET, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated {len(rows)} stations.")