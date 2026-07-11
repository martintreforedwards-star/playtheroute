import csv
from itertools import combinations


def shared_prefix(stations1, stations2):

    count = 0

    for a, b in zip(stations1, stations2):

        if a != b:
            break

        count += 1

    return count


def build_corridors(patterns):

    corridors = []

    for pattern1, pattern2 in combinations(patterns, 2):

        shared = shared_prefix(
            pattern1["stations"],
            pattern2["stations"],
        )

        # Ignore unrelated patterns
        if shared < 3:
            continue

        corridors.append({

            "pattern_a": pattern1["pattern_id"],

            "pattern_b": pattern2["pattern_id"],

            "shared_prefix": shared,

            "origin": pattern1["stations"][0],

            "destination_a": pattern1["stations"][-1],

            "destination_b": pattern2["stations"][-1],

        })

    return corridors


def save_corridors(corridors):

    filename = "data/Masters/service_corridors.csv"

    if not corridors:

        print("No corridors discovered.")
        return

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=corridors[0].keys(),
        )

        writer.writeheader()

        writer.writerows(corridors)

    print(f"Saved: {filename}")


def report_corridors(corridors):

    print()
    print("==========================")
    print("Corridor Report")
    print("==========================")
    print()

    print(f"Related pattern pairs : {len(corridors):,}")

    if not corridors:
        return

    longest = max(
        corridors,
        key=lambda c: c["shared_prefix"],
    )

    print(
        f"Longest shared prefix : "
        f"{longest['shared_prefix']} stations"
    )

    print()
    print("First 20 corridors")
    print("------------------")

    for corridor in corridors[:20]:

        print(
            f"{corridor['pattern_a']}  "
            f"{corridor['pattern_b']}  "
            f"{corridor['shared_prefix']:2} shared stations"
        )