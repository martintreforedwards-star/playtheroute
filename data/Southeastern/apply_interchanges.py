import json
from pathlib import Path

JSON_FILE = Path("data/stations/southeastern.json")

INTERCHANGE_STATIONS = {
    "Ashford International",
    "Bromley South",
    "Canterbury West",
    "Cannon Street",
    "Charing Cross",
    "Dartford",
    "Ebbsfleet International",
    "Faversham",
    "Lewisham",
    "London Bridge",
    "Orpington",
    "Sevenoaks",
    "St Pancras International",
    "Stratford International",
    "Strood",
    "Tonbridge",
    "Victoria",
    
}

with open(JSON_FILE, "r", encoding="utf-8") as f:
    stations = json.load(f)

updated = 0

for station in stations:

    station["is_interchange"] = (
        station["station_name"] in INTERCHANGE_STATIONS
    )

    updated += 1

with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(stations, f, indent=2, ensure_ascii=False)

print(f"Updated {updated} stations")
print(f"Interchange stations: {len(INTERCHANGE_STATIONS)}")