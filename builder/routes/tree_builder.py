import csv


def shared_prefix(stations1, stations2):

    shared = 0

    for a, b in zip(stations1, stations2):

        if a != b:
            break

        shared += 1

    return shared


def build_route_tree(routes, patterns):

    #
    # Quick lookup
    #

    pattern_lookup = {
        p["pattern_id"]: p
        for p in patterns
    }

    tree = []

    for route in routes:

        members = [
            pattern_lookup[p]
            for p in route["patterns"]
            if p in pattern_lookup
        ]

        if len(members) < 2:
            continue

        #
        # Highest frequency becomes trunk
        #

        trunk = max(
            members,
            key=lambda p: p["service_count"],
        )

        for pattern in members:

            if pattern["pattern_id"] == trunk["pattern_id"]:
                continue

            shared = shared_prefix(
                trunk["stations"],
                pattern["stations"],
            )

            split_after = ""

            if shared:

                split_after = trunk["stations"][shared - 1]

            tree.append({

                "route_id": route["route_id"],

                "trunk_pattern": trunk["pattern_id"],

                "branch_pattern": pattern["pattern_id"],

                "shared_prefix": shared,

                "split_after": split_after,

                "destination": pattern["destination"],

                "service_count": pattern["service_count"],

            })

    return tree


def save_tree(tree):

    filename = "data/Masters/route_tree.csv"

    if not tree:
        print("No route tree produced.")
        return

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=tree[0].keys(),
        )

        writer.writeheader()

        writer.writerows(tree)

    print(f"Saved: {filename}")


def report_tree(tree):

    print()
    print("==========================")
    print("Route Tree Report")
    print("==========================")
    print()

    print(f"Branches discovered : {len(tree):,}")

    if not tree:
        return

    deepest = max(
        tree,
        key=lambda r: r["shared_prefix"],
    )

    print(
        f"Deepest branch : "
        f"{deepest['shared_prefix']} shared stations"
    )

    print()
    print("First 20 branches")
    print("-----------------")

    ranked = sorted(
        tree,
        key=lambda r: (
            r["route_id"],
            -r["shared_prefix"],
        ),
    )

    for row in ranked[:20]:

        print(
            f"{row['route_id']}   "
            f"{row['branch_pattern']}   "
            f"after {row['split_after']:3}   "
            f"{row['destination']:3}   "
            f"({row['shared_prefix']:2} shared)"
        )