import csv
import sys

SERVICE_PATTERNS = "data/Masters/service_patterns.csv"


def inspect_station(crs):

    count = 0

    with open(SERVICE_PATTERNS, newline="", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:

            stations = row["stations"].split("|")

            if crs in stations:

                count += 1

                print()
                print("=" * 80)
                print(row["pattern_id"])
                print(f'{row["origin"]} -> {row["destination"]}')
                print(f'Services : {row["service_count"]}')
                print(row["stations"])

    print()
    print(f"Patterns found: {count}")


if __name__ == "__main__":

    inspect_station(sys.argv[1].upper())