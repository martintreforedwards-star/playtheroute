from pathlib import Path
import csv

SOURCE = Path("data/Masters/route_geometry.csv")
OUTPUT = Path("data/Masters/route_links.csv")


def main():

    rows = []

    with open(SOURCE, newline="", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for route in reader:

            route_id = route["route_id"]

            stations = route["station_sequence"].split("|")

            for i in range(len(stations) - 1):

                rows.append(
                    (
                        route_id,
                        stations[i],
                        stations[i + 1],
                    )
                )

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
                "from_crs",
                "to_crs",
            ]
        )

        writer.writerows(rows)

    print(f"Saved : {OUTPUT}")
    print(f"Links : {len(rows):,}")
    print()

    for row in rows[:20]:
        print(",".join(row))


if __name__ == "__main__":
    main()