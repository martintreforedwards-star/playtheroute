import json
from pathlib import Path

JSON_FILE = Path("data/stations/southeastern.json")

with open(JSON_FILE, "r", encoding="utf-8") as f:
    stations = json.load(f)

FLAGS = [
    "direct_to_charing_cross",
    "direct_to_cannon_street",
    "direct_to_victoria",
    "direct_to_london_bridge",
    "direct_to_st_pancras",
]

for flag in FLAGS:

    print()
    print("=" * 70)
    print(flag.upper())
    print("=" * 70)

    matches = [
        s["station_name"]
        for s in stations
        if s.get(flag) is True
    ]

    for name in sorted(matches):
        print(name)

    print()
    print(f"TOTAL: {len(matches)}")