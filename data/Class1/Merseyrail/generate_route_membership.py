import csv

from routes import ROUTES

rows = []

for route, stations in ROUTES.items():
    for station in stations:
        rows.append({
            "station_name": station,
            "route_group": route
        })

with open(
    "data/Merseyrail/route_group_membership.csv",
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

print(f"Generated {len(rows)} memberships.")