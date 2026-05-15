import json

with open("data/stations/southeastern.json", "r", encoding="utf-8") as file:
    stations = json.load(file)

rows = []

for station in stations:

    name = station.get("station_name", "")
    crs = station.get("crs", "")
    band = station.get("distance_band", "")

    rows.append((name, crs, band))

rows.sort()

for row in rows:
    print(f"{row[0]} ({row[1]}) --> {row[2]}")
