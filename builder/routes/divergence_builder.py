import csv
from itertools import combinations


def analyse_divergence(stations1, stations2):

    shared = 0

    for a, b in zip(stations1, stations2):

        if a != b:
            break

        shared += 1

    if shared == 0:
        return None

    divergence_station = stations1[shared - 1]

    branch_a = (
        stations1[shared]
        if shared < len(stations1)
        else ""
    )

    branch_b = (
        stations2[shared]
        if shared < len(stations2)
        else ""
    )

    overlap = shared / min(
        len(stations1),
        len(stations2),
    )

    return {
        "shared_prefix": shared,
        "divergence_station": divergence_station,
        "branch_a": branch_a,
        "branch_b": branch_b,
        "overlap": round(overlap, 3),
    }


def build_divergences(patterns):

    divergences = []

    for pattern1, pattern2 in combinations(patterns, 2):

        result = analyse_divergence(
            pattern1["stations"],
            pattern2["stations"],
        )

        if result is None:
            continue

        if result["shared_prefix"] < 5:
            continue

        divergences.append({

            "pattern_a": pattern1["pattern_id"],

            "pattern_b": pattern2["pattern_id"],

            "origin": pattern1["stations"][0],

            "destination_a": pattern1["stations"][-1],

            "destination_b": pattern2["stations"][-1],

            **result,

        })

    return divergences


def save_divergences(divergences):

    filename = "data/Masters/service_divergences.csv"

    if not divergences:
        print("No divergences discovered.")
        return

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=divergences[0].keys(),
        )

        writer.writeheader()

        writer.writerows(divergences)

    print(f"Saved: {filename}")


def report_divergences(divergences):

    print()
    print("==========================")
    print("Divergence Report")
    print("==========================")
    print()

    print(f"Related pattern pairs : {len(divergences):,}")

    if not divergences:
        return

    deepest = max(
        divergences,
        key=lambda d: d["shared_prefix"],
    )

    print(
        f"Deepest shared corridor : "
        f"{deepest['shared_prefix']} stations"
    )

    print()
    print("First 20 divergences")
    print("--------------------")

    for d in divergences[:20]:

        print(
            f"{d['pattern_a']}  "
            f"{d['pattern_b']}  "
            f"{d['shared_prefix']:2} shared  "
            f"split at {d['divergence_station']}"
        )