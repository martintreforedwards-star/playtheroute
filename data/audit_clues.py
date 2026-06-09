import json
from itertools import combinations

with open("data/stations/southeastern.json") as f:
    stations = json.load(f)

with open("data/clues/southeastern-clues.json") as f:
    clues = json.load(f)

row_clues = clues["rowPool"]
col_clues = clues["columnPool"]


def matches_clue(station, clue):

    if clue["type"] == "field":
        return station.get(clue["field"]) == clue["value"]

    if clue["type"] == "contains":
        return clue["value"].lower() in station.get(
            clue["field"], ""
        ).lower()

    if clue["type"] == "range":

        value = station.get(clue["field"])

        if value is None:
            return False

        if "min" in clue and value < clue["min"]:
            return False

        if "max" in clue and value > clue["max"]:
            return False

        return True

    return False


playable = 0
rejected = 0

worst_board = None
worst_min = 999999

for rows in combinations(row_clues, 2):
    for cols in combinations(col_clues, 4):

        counts = []
        valid = True

        for row in rows:
            for col in cols:

                matches = [
                    s
                    for s in stations
                    if matches_clue(s, row)
                    and matches_clue(s, col)
                ]

                counts.append(len(matches))

                if len(matches) == 0:
                    valid = False

        if valid:
            playable += 1

            board_min = min(counts)

            if board_min < worst_min:
                worst_min = board_min
                worst_board = {
                    "rows": [r["display"] for r in rows],
                    "cols": [c["display"] for c in cols],
                    "counts": counts,
                }

        else:
            rejected += 1


print()
print("==============================")
print("AUDIT RESULTS")
print("==============================")
print()

print("Rows:", len(row_clues))
print("Columns:", len(col_clues))
print()

print("Playable:", playable)
print("Rejected:", rejected)
print("Total:", playable + rejected)

if playable + rejected:
    print(
        "Playable %:",
        round(
            playable * 100 / (playable + rejected),
            1
        )
    )

print()

print("==============================")
print("WORST PLAYABLE BOARD")
print("==============================")
print()

print(worst_board)
