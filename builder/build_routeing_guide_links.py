from pathlib import Path
import csv

SOURCE = Path("data/RJRG1052RGL.txt")
OUTPUT = Path("data/Masters/routeing_guide_links.csv")


def main():

    rows = []

    with open(SOURCE, encoding="utf-8", errors="ignore") as f:

        for line in f:

            line = line.strip()

            if (
                not line
                or line.startswith("/")
                or line.startswith("/!!")
            ):
                continue

            parts = [p.strip() for p in line.split(",")]

            if len(parts) < 3:
                continue

            from_crs = parts[0]
            to_crs = parts[1]

            # Remaining values are map codes
            for map_code in parts[2:]:

                if map_code:

                    rows.append(
                        (
                            from_crs,
                            to_crs,
                            map_code,
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
                "from_crs",
                "to_crs",
                "map_code",
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