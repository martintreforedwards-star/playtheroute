import ast
import csv
import json

INPUT_FILE = "data/Southern/southern_v4_enriched.csv"
OUTPUT_FILE = "data/Southern/southern.json"

stations = []

with open(INPUT_FILE, newline="", encoding="utf-8-sig") as f:

    reader = csv.DictReader(f)

    for row in reader:

        # Convert route_groups string into a real list
        try:
            row["route_groups"] = ast.literal_eval(row["route_groups"])
        except:
            row["route_groups"] = []

        stations.append(row)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(stations, f, indent=2)

print()
print("DONE")
print(f"Stations: {len(stations)}")
print(f"Saved: {OUTPUT_FILE}")