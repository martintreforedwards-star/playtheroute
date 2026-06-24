import csv
import json
from pathlib import Path

# ==================================================
# PATHS
# ==================================================

ROOT = Path(__file__).resolve().parent.parent.parent

STATIONS_FILE = ROOT / "crs_source_of_truth.csv"
CATALOGUE_FILE = ROOT / "data" / "wordplay_catalogue.json"
OUTPUT_FILE = ROOT / "docs" / "wordplay_report.md"

# ==================================================
# LOAD STATIONS
# ==================================================

stations = []

with open(STATIONS_FILE, newline="", encoding="utf-8") as f:

    reader = csv.DictReader(f)

    for row in reader:

        station_name = (
            row.get("stationName") or ""
        ).lower()

        network = (
            row.get("network") or ""
        ).strip()

        stations.append(
            {
                "station": station_name,
                "network": network
            }
        )

# ==================================================
# LOAD WORDPLAY CATALOGUE
# ==================================================

with open(CATALOGUE_FILE, encoding="utf-8") as f:
    catalogue = json.load(f)

# ==================================================
# BUILD REPORT
# ==================================================

lines = []

lines.append("# National Wordplay Report")
lines.append("")
lines.append(f"Stations analysed: {len(stations)}")
lines.append("")

# ==================================================
# NATIONAL CATEGORY TOTALS
# ==================================================

lines.append("## National Category Totals")
lines.append("")

lines.append("| Category | Total Matches |")
lines.append("|----------|--------------:|")

national_totals = {}

for category, terms in catalogue.items():

    category_total = 0

    for term in terms:

        count = sum(
            1
            for station in stations
            if term.lower() in station["station"]
        )

        category_total += count

    national_totals[category] = category_total

for category, total in sorted(
    national_totals.items(),
    key=lambda x: x[1],
    reverse=True
):

    lines.append(
        f"| {category.title()} | {total} |"
    )

lines.append("")

# ==================================================
# NATIONAL TERM BREAKDOWN
# ==================================================

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

        results.append(
            (term, count)
        )

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    for term, count in results:

        lines.append(
            f"| {term} | {count} |"
        )

    lines.append("")

# ==================================================
# NETWORK CATEGORY TOTALS
# ==================================================

lines.append("# Network Category Totals")
lines.append("")

networks = sorted(
    {
        station["network"]
        for station in stations
        if station["network"]
    }
)

header = "| Network |"
divider = "|---------|"

for category in catalogue.keys():

    header += f" {category.title()} |"
    divider += "----------:|"

lines.append(header)
lines.append(divider)

for network in networks:jq length data/Southern/southern.json
jq length data/stations/southeastern.json

    network_stations = [
        station
        for station in stations
        if station["network"] == network
    ]

    row = f"| {network} |"

    for category, terms in catalogue.items():

        category_total = 0

        for term in terms:

            count = sum(
                1
                for station in network_stations
                if term.lower() in station["station"]
            )

            category_total += count

        row += f" {category_total} |"

    lines.append(row)

lines.append("")

# ==================================================
# NETWORK TERM BREAKDOWN
# ==================================================

for network in networks:

    lines.append(f"# {network}")
    lines.append("")

    network_stations = [
        station
        for station in stations
        if station["network"] == network
    ]

    for category, terms in catalogue.items():

        lines.append(f"## {category.title()}")
        lines.append("")

        lines.append("| Term | Matches |")
        lines.append("|------|---------:|")

        results = []

        for term in terms:

            count = sum(
                1
                for station in network_stations
                if term.lower() in station["station"]
            )

            results.append(
                (term, count)
            )

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

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "\n".join(lines)
    )

# ==================================================
# DONE
# ==================================================

print()
print("DONE")
print()
print(f"Stations analysed: {len(stations)}")
print(f"Networks analysed: {len(networks)}")
print(f"Saved: {OUTPUT_FILE}")