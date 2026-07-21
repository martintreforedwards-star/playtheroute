import csv

DARWIN = r"data/Class1/Southern/southern_terminus.csv"
SOUTHERN = r"data/Class1/Southern/southern.csv"
OUTPUT = r"data/Class1/Southern/southern_terminus_out.csv"

lookup = {}

with open(DARWIN, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        lookup[row["crs"].strip().upper()] = row["terminus"]

rows = []

with open(SOUTHERN, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append({
            "crs": row["crs"],
            "terminus": lookup.get(row["crs"].strip().upper(), "")
        })

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["crs", "terminus"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Stations: {len(rows)}")
print(f"Matched : {sum(1 for r in rows if r['terminus'])}")
print(f"Saved   : {OUTPUT}")