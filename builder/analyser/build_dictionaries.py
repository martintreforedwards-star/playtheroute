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
OUTPUT = Path(f"data/{network}/dictionaries")

OUTPUT.mkdir(exist_ok=True)

stations = json.loads(INPUT.read_text(encoding="utf-8"))

prefix = Counter()
suffix = Counter()
first = Counter()
last = Counter()

for s in stations:
    prefix[s["prefix"]] += 1
    suffix[s["suffix"]] += 1
    first[s["first_word"]] += 1
    last[s["last_word"]] += 1

for name, counter in {
    "prefix": prefix,
    "suffix": suffix,
    "first_word": first,
    "last_word": last,
}.items():

    with open(OUTPUT / f"{name}.json", "w", encoding="utf-8") as f:
        json.dump(dict(sorted(counter.items())), f, indent=2)

print(f"Created {OUTPUT}")