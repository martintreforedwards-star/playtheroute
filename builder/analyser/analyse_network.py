import json
import sys
from pathlib import Path


if len(sys.argv) != 2:
    print("Usage:")
    print("python builder/analyser/analyse_network.py <network>")
    raise SystemExit

NETWORK = sys.argv[1]

INPUT = Path(f"data/{NETWORK}/{NETWORK.lower()}.json")
OUTPUT = Path(f"data/{NETWORK}/{NETWORK.lower()}_wordplay.json")


def analyse(name):

    words = name.split()

    return {
        "station_name": name,
        "word_count": len(words),
        "character_count": len(name),
        "first_word": words[0],
        "last_word": words[-1],
        "initial_letter": name[0],
        "final_letter": name[-1],
        "contains_hyphen": "-" in name,
        "contains_apostrophe": "'" in name,
        "contains_digits": any(c.isdigit() for c in name),
        "starts_with_the": name.startswith("The "),
        "starts_with_st": name.startswith("St "),
        "contains_and": " and " in name,
        "contains_central": "Central" in name,
        "contains_parkway": "Parkway" in name,
        "contains_junction": "Junction" in name,
        "contains_road": "Road" in name,
        "contains_street": "Street" in name,
        "contains_bridge": "Bridge" in name,
        "contains_green": "Green" in name,
        "contains_cross": "Cross" in name,
        "contains_hill": "Hill" in name,
        "contains_lane": "Lane" in name,
        "contains_square": "Square" in name,
        "contains_mount": "Mount" in name,
        "contains_new": "New" in name,
        "contains_old": "Old" in name,
        "contains_upper": "Upper" in name,
        "contains_lower": "Lower" in name,
        "contains_north": "North" in name,
        "contains_south": "South" in name,
        "contains_east": "East" in name,
        "contains_west": "West" in name,
        "prefix": words[0][:3].lower(),
        "suffix": words[-1][-3:].lower()
    }


stations = json.loads(INPUT.read_text(encoding="utf-8"))

output = [analyse(s["station_name"]) for s in stations]

OUTPUT.write_text(
    json.dumps(output, indent=2),
    encoding="utf-8"
)

print(f"Created {OUTPUT}")