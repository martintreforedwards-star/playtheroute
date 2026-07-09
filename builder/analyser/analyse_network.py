import json
import re
import sys
from pathlib import Path


def normalise(name):
    """Clean station names before analysis."""

    name = re.sub(r"\([^)]*\)", "", name)
    name = name.replace("&", "and")
    name = " ".join(name.split())

    return name.strip()


def analyse_station(name):

    name = normalise(name)
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
        "contains_and": " and " in name.lower(),
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
        "suffix": words[-1][-3:].lower(),
    }


def analyse(network):

    input_file = Path("data") / network / f"{network.lower()}.json"

    output_dir = Path("data") / network / "analysis"

    print(f"Analysis directory: {output_dir.resolve()}")

    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    elif not output_dir.is_dir():
        raise RuntimeError(f"{output_dir} exists but is not a directory")

    output_file = output_dir / f"{network.lower()}_wordplay.json"

    stations = json.loads(input_file.read_text(encoding="utf-8"))

    output = [
        analyse_station(station["station_name"])
        for station in stations
    ]

    output_file.write_text(
        json.dumps(output, indent=2),
        encoding="utf-8",
    )

    print(f"Created {output_file}")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("python builder/analyser/analyse_network.py <network>")
        raise SystemExit

    analyse(sys.argv[1])