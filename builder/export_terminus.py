import json
import csv

json_file = r"data/Class1/Southern/southern.json"
csv_file = r"data/Class1/Southern/southern_terminus_2.csv"

with open(json_file, "r", encoding="utf-8") as f:
    stations = json.load(f)

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["crs", "terminus"])

    for station in stations:
        writer.writerow([
            station.get("crs", ""),
            station.get("terminus", "")
        ])

print(f"Exported {len(stations)} stations to {csv_file}")