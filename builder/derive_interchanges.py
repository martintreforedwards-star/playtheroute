import csv

PATTERNS = r"data/Masters/service_patterns.csv"
SOUTHERN = r"data/Class1/Southern/southern.csv"

usage = {}

with open(PATTERNS, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)

    for row in reader:
        pattern = row["pattern_id"]

        for crs in row["stations"].split("|"):
            crs = crs.strip().upper()
            if crs:
                usage.setdefault(crs, set()).add(pattern)

rows = []

with open(SOUTHERN, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames

    for row in reader:
        crs = row["crs"].strip().upper()
        row["is_interchange"] = str(len(usage.get(crs, set())) > 1)
        rows.append(row)

with open(SOUTHERN, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Stations processed : {len(rows)}")
print(f"Interchanges      : {sum(r['is_interchange']=='True' for r in rows)}")