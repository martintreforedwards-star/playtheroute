import json
from pathlib import Path

JSON_FILE = Path("data/stations/southeastern.json")

HIGH_SPEED_STATIONS = {
    "St Pancras International",
    "Stratford International",
    "Ebbsfleet International",
    "Gravesend",
    "Strood",
    "Snodland",
    "Maidstone West",
    "Ashford International",
    "Canterbury West",
    "Thanet Parkway",
    "Ramsgate",
    "Dumpton Park",
    "Broadstairs",
    "Margate",
    "Westgate-On-Sea",
    "Birchington-On-Sea",
    "Herne Bay",
    "Chestfield & Swalecliffe",
    "Whitstable",
    "Faversham",
    "Sittingbourne",
    "Rainham (Kent)",
    "Gillingham (Kent)",
    "Chatham",
    "Rochester",
    "Folkestone West",
    "Folkestone Central",
    "Dover Priory",
    "Martin Mill",
    "Walmer",
    "Deal",
    "Sandwich",
}

with open(JSON_FILE, "r", encoding="utf-8") as f:
    stations = json.load(f)

updated = 0

station_names = {
    station["station_name"]
    for station in stations
}

for station in stations:

    station_name = station["station_name"]

    is_high_speed = station_name in HIGH_SPEED_STATIONS

    station["is_high_speed"] = is_high_speed

    route_groups = station.get("route_groups", [])

    if is_high_speed:

        if "High Speed 1" not in route_groups:
            route_groups.append("High Speed 1")

    else:

        if "High Speed 1" in route_groups:
            route_groups.remove("High Speed 1")

    station["route_groups"] = route_groups

    updated += 1

with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(stations, f, indent=2, ensure_ascii=False)

missing = []

for name in sorted(HIGH_SPEED_STATIONS):
    if name not in station_names:
        missing.append(name)

print()
print("MISSING FROM JSON")
print("-" * 40)

if missing:
    for name in missing:
        print(name)
else:
    print("None")

print()
print(f"Updated {updated} stations")
print(f"High Speed stations in definition: {len(HIGH_SPEED_STATIONS)}")