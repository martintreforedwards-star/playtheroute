from pathlib import Path
import csv

SOURCE = Path("data/RJRG1052RGM.txt")   # change if needed
OUTPUT = Path("data/Masters/routeing_guide_maps.csv")


def main():

    rows = []
    current_name = None

    with open(SOURCE, encoding="utf-8", errors="ignore") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            if line.startswith("/!!"):
                continue

            if line.startswith("/"):
                current_name = line[1:].strip()
                continue

            if len(line) == 2 and current_name:

                rows.append((line, current_name))
                current_name = None

    rows.sort(key=lambda x: x[0])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)
        writer.writerow(["map_code", "map_name"])
        writer.writerows(rows)

    print(f"Saved : {OUTPUT}")
    print(f"Maps  : {len(rows)}")
    print()

    for row in rows[:20]:
        print(row[0], "-", row[1])


if __name__ == "__main__":
    main()