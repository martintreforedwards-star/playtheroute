import json

STATIONS_FILE = "data/stations/southeastern.json"
CLUES_FILE = "data/clues/southeastern-clues.json"


def clue_matches(station, clue):

    clue_type = clue["type"]

    if clue_type == "field":
        return station.get(clue["field"]) == clue["value"]

    if clue_type == "contains":
        text = str(
            station.get(clue["field"], "")
        ).lower()

        return clue["value"].lower() in text

    if clue_type == "word_group":

        WORD_GROUPS = {

            "nature": [
                "wood",
                "woods",
                "hill",
                "green",
                "park",
                "heath",
                "grove",
                "oak",
                "elm",
                "ash"
            ],

            "water": [
                "bay",
                "sea",
                "brook",
                "river",
                "mere",
                "marsh",
                "quay",
                "harbour"
            ],

            "direction": [
                "north",
                "south",
                "east",
                "west"
            ],

            "settlement": [
                "town",
                "village",
                "road",
                "street",
                "gate",
                "cross",
                "bridge"
            ],

            "religious": [
                "st",
                "saint",
                "abbey",
                "priory",
                "church"
            ]

        }

        text = str(
            station.get(clue["field"], "")
        ).lower()

        return any(
            word in text
            for word in WORD_GROUPS[
                clue["group"]
            ]
        )

    if clue_type == "array_contains":
        values = station.get(
            clue["field"],
            []
        )

        return clue["value"] in values

    if clue_type == "range":

        value = station.get(
            clue["field"]
        )

        if value is None:
            return False

        if (
            "min" in clue and
            value < clue["min"]
        ):
            return False

        if (
            "max" in clue and
            value > clue["max"]
        ):
            return False

        return True

    return False

with open(STATIONS_FILE) as f:
    stations = json.load(f)

with open(CLUES_FILE) as f:
    clues = json.load(f)

rows = clues["rowPool"]
columns = clues["columnPool"]

zero_count = 0
one_count = 0
small_count = 0
large_count = 0

print()
print("=" * 60)
print("ROW × COLUMN AUDIT")
print("=" * 60)

for row in rows:

    for column in columns:

        matches = 0

        for station in stations:

            if (
                clue_matches(
                    station,
                    row
                )
                and
                clue_matches(
                    station,
                    column
                )
            ):
                matches += 1

        print(
            f'{row["display"]} × '
            f'{column["display"]} '
            f'= {matches}'
        )

        if matches == 0:
            zero_count += 1

        elif matches == 1:
            one_count += 1

        elif matches <= 5:
            small_count += 1

        else:
            large_count += 1

total = (
    zero_count +
    one_count +
    small_count +
    large_count
)

print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)

print(f"Total intersections: {total}")
print(f"0 matches: {zero_count}")
print(f"1 match: {one_count}")
print(f"2-5 matches: {small_count}")
print(f"6+ matches: {large_count}")
print()
print("=" * 60)
print("ROW CLUE SIZES")
print("=" * 60)

for row in rows:

    count = 0

    for station in stations:

        if (
            row["type"] == "field"
            and station.get(
                row["field"]
            ) == row["value"]
        ):
            count += 1

    print(
        f'{row["display"]}: {count}'
    )

print()
print("=" * 60)
print("ALL CLUES BY COVERAGE")
print("=" * 60)

all_clues = []

# Row clues

for row in rows:

    count = 0

    for station in stations:

        if clue_matches(
            station,
            row
        ):
            count += 1

    all_clues.append(
        (
            row["display"],
            count,
            "ROW"
        )
    )

# Column clues

for column in columns:

    count = 0

    for station in stations:

        if clue_matches(
            station,
            column
        ):
            count += 1

    all_clues.append(
        (
            column["display"],
            count,
            "COLUMN"
        )
    )

# Sort by coverage

all_clues.sort(
    key=lambda x: x[1],
    reverse=True
)

# Output

for name, count, clue_type in all_clues:

    print(
        f"{count:3}  [{clue_type}]  {name}"
    )