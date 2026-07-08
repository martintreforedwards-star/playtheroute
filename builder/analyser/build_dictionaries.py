import json
import sys
from collections import Counter
from pathlib import Path


if len(sys.argv) != 2:
    print("Usage:")
    print("python builder/analyser/build_dictionaries.py <network>")
    raise SystemExit

network = sys.argv[1]

INPUT = Path(f"data/{network}/{network.lower()}_wordplay.json")
OUTPUT_DIR = Path(f"data/{network}/dictionaries")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT = OUTPUT_DIR / "wordplay_dictionary.json"

stations = json.loads(INPUT.read_text(encoding="utf-8"))

dictionary = {
    "prefix": Counter(),
    "suffix": Counter(),
    "first_word": Counter(),
    "last_word": Counter(),
    "tokens": Counter(),
}

for s in stations:

    dictionary["prefix"][s["prefix"]] += 1
    dictionary["suffix"][s["suffix"]] += 1
    dictionary["first_word"][s["first_word"]] += 1
    dictionary["last_word"][s["last_word"]] += 1

    for token in s["station_name"].split():
        dictionary["tokens"][token] += 1

output = {}

for key, counter in dictionary.items():
    output[key] = dict(sorted(counter.items()))

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"Created {OUTPUT}")