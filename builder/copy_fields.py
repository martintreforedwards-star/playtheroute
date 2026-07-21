import csv

SOURCE = r"data/Class1/Southern/southern_aggregated_1.csv"
TARGET = r"data/Class1/Southern/southern.csv"

FIELDS = [
    "county",
    "major_interchange",
    "branch_junction",
]

lookup = {}

with open(SOURCE, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        crs = row["crs"].strip().upper()
        lookup[crs] = {field: row.get(field, "") for field in FIELDS}

rows = []

with open(TARGET, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames

    for row in reader:
        crs = row["crs"].strip().upper()
        if crs in lookup:
            for field in FIELDS:
                row[field] = lookup[crs][field]
        rows.append(row)

with open(TARGET, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated {len(rows)} stations.")