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
            {
                "station": (row.get("stationName") or "").lower(),
                "region": (row.get("region") or "").strip()
            }
        )

with open(CATALOGUE_FILE, encoding="utf-8") as f:
    catalogue = json.load(f)

lines = []

# ==================================================
# NATIONAL REPORT
# ==================================================

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
            1
            for station in stations
            if term.lower() in station["station"]
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
            1
            for station in stations
            if term.lower() in station["station"]
        )

        results.append((term, count))

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    for term, count in results:
        lines.append(f"| {term} | {count} |")

    lines.append("")

# ==================================================
# REGIONAL BREAKDOWN
# ==================================================

regions = sorted(
    {
        station["region"]
        for station in stations
        if station["region"]
    }
)

for region in regions:

    region_stations = [
        station
        for station in stations
        if station["region"] == region
    ]

    lines.append(f"# {region}")
    lines.append("")
    lines.append(f"Stations analysed: {len(region_stations)}")
    lines.append("")

    for category, terms in catalogue.items():

        lines.append(f"## {category.title()}")
        lines.append("")
        lines.append("| Term | Matches |")
        lines.append("|------|---------:|")

        results = []

        for term in terms:

            count = sum(
                1
                for station in region_stations
                if term.lower() in station["station"]
            )

            results.append((term, count))

        results.sort(
            key=lambda x: x[1],
            reverse=True
        )

        for term, count in results:

            if count > 0:
                lines.append(
                    f"| {term} | {count} |"
                )

        lines.append("")

# ==================================================
# SAVE REPORT
# ==================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# ==================================================
# DONE
# ==================================================

print()
print("DONE")
print()
print(f"Stations analysed: {len(stations)}")
print(f"Regions analysed: {len(regions)}")
print(f"Saved: {OUTPUT_FILE}")
