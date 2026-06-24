import csv
import json

stations = []

with open(
    "southern_v4_enriched.csv",
    newline="",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:
        stations.append(row)

with open(
    "southern.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        stations,
        f,
        indent=2
    )

print(
    f"Saved southern.json ({len(stations)} stations)"
)