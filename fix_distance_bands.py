import json

TARGETS = {

    "Chartham": "outer",
    "Chilham": "outer",
    "Harrietsham": "outer",
    "Lenham": "outer",
    "Wye": "outer",
    "Appledore": "outer",
    "Sturry": "outer"

}

FILE_PATH = "data/stations/southeastern.json"

with open(FILE_PATH, "r", encoding="utf-8") as file:
    stations = json.load(file)

for station in stations:

    name = station.get("station_name")

    if name in TARGETS:

        station["distance_band"] = TARGETS[name]

        print(
            f"Updated {name} -> {TARGETS[name]}"
        )

with open(FILE_PATH, "w", encoding="utf-8") as file:

    json.dump(
        stations,
        file,
        indent=2,
        ensure_ascii=False
    )

print("\nDistance bands updated.")
