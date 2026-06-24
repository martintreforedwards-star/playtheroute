import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

STATIONS_FILE = ROOT / "crs_source_of_truth.csv"
CATALOGUE_FILE = ROOT / "data" / "wordplay_catalogue.json"
OUTPUT_FILE = ROOT / "docs" / "wordplay_report.md"

stations = []

with open(STATIONS_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        stations.append(
            (row.get("stationName") or "").lower()
        )

with open(CATALOGUE_FILE, encoding="utf-8") as f:
    catalogue = json.load(f)

lines = []

lines.append("# National Wordplay Report")
lines.append("")
lines.append(f"Stations analysed: {len(stations)}")
lines.append("")

lines.append("## National Category Totals")
lines.append("")
lines.append("| Category | Total Matches |")
lines.append("|----------|--------------:|")

totals = {}

for category, terms in catalogue.items():

    total = 0

    for term in terms:
        total += sum(
            1 for station in stations
            if term.lower() in station
        )

    totals[category] = total

for category, total in sorted(
    totals.items(),
    key=lambda x: x[1],
    reverse=True
):
    lines.append(f"| {category.title()} | {total} |")

lines.append("")
lines.append("# National Term Breakdown")
lines.append("")

for category, terms in catalogue.items():

    lines.append(f"## {category.title()}")
    lines.append("")
    lines.append("| Term | Matches |")
    lines.append("|------|---------:|")

    results = []

    for term in terms:

        count = sum(
            1 for station in stations
            if term.lower() in station
        )

        results.append((term, count))

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    for term, count in results:
        lines.append(f"| {term} | {count} |")

    lines.append("")

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print()
print("DONE")
print()
print(f"Stations analysed: {len(stations)}")
print(f"Saved: {OUTPUT_FILE}")
