from pathlib import Path
import csv
from collections import defaultdict

ROUTE_LINKS = Path("data/Masters/route_links.csv")
RG_LINKS = Path("data/Masters/routeing_guide_links.csv")
OUTPUT = Path("data/Masters/route_map_matches.csv")


def main():

    print("Loading Routeing Guide links...")

    rg_lookup = defaultdict(list)

    with open(RG_LINKS, newline="", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:

            key = (row["from_crs"], row["to_crs"])

            rg_lookup[key].append(row["map_code"])

    print(f"Unique Routeing Guide links : {len(rg_lookup):,}")

    print("Matching Builder routes...")

    matches = defaultdict(int)

    with open(ROUTE_LINKS, newline="", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:

            key = (row["from_crs"], row["to_crs"])

            if key not in rg_lookup:
                continue

            route_id = row["route_id"]

            for map_code in rg_lookup[key]:

                matches[(route_id, map_code)] += 1

    rows = []

    for (route_id, map_code), count in matches.items():

        rows.append(
            (
                route_id,
                map_code,
                count,
            )
        )

    rows.sort(key=lambda x: (x[0], -x[2], x[1]))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(
        OUTPUT,
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "route_id",
                "map_code",
                "match_count",
            ]
        )

        writer.writerows(rows)

    print()
    print(f"Saved : {OUTPUT}")
    print(f"Matches : {len(rows):,}")
    print()

    print("Top 20 matches")
    print()

    for row in rows[:20]:
        print(f"{row[0]}  {row[1]}  {row[2]}")


if __name__ == "__main__":
    main()