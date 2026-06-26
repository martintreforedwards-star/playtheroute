import csv
from routes import ROUTES

rows = []

for route_group, stations in ROUTES.items():
    for station in stations:
        rows.append({
            "station_name": station,
            "route_group": route_group
        })

from pathlib import Path
from routes import ROUTES

print(f"Loaded {len(ROUTES)} routes")
BASE = Path(__file__).parent

OUTPUT = BASE / "route_group_membership.csv"

with open(
    OUTPUT,
    "w",
    newline="",
    encoding="utf-8"
) as f:
    
    writer = csv.DictWriter(
        f,
        fieldnames=["station_name", "route_group"]
    )

    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} route memberships.")