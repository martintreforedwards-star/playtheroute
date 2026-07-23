import csv
from collections import defaultdict


def build_routes(patterns, divergences):

    graph = defaultdict(set)

    #
    # Ensure every service pattern exists in the graph,
    # even if it has no divergence.
    #

    for pattern in patterns:
        graph[pattern["pattern_id"]]

    #
    # Build an undirected graph
    #

    for row in divergences:

        a = row["pattern_a"]
        b = row["pattern_b"]

        graph[a].add(b)
        graph[b].add(a)

    #
    # Find connected components
    #

    visited = set()
    routes = []
    route_number = 1

    for start in sorted(graph):

        if start in visited:
            continue

        stack = [start]
        component = []

        visited.add(start)

        while stack:

            node = stack.pop()
            component.append(node)

            for neighbour in graph[node]:

                if neighbour not in visited:

                    visited.add(neighbour)
                    stack.append(neighbour)

        component.sort()

        routes.append({

            "route_id": f"R{route_number:05d}",
            "patterns": component,
            "pattern_count": len(component),

        })

        route_number += 1

    #
    # Validation
    #

    assigned_patterns = sum(
        route["pattern_count"]
        for route in routes
    )

    if assigned_patterns != len(patterns):

        raise RuntimeError(
            f"Route Builder Error: "
            f"{assigned_patterns:,} of {len(patterns):,} "
            f"service patterns were assigned to routes."
        )

    print(
        f"✓ Assigned all {assigned_patterns:,} "
        f"service patterns to {len(routes):,} routes."
    )

    return routes


def save_routes(routes):

    filename = "data/Masters/route_candidates.csv"

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "route_id",
            "pattern_id",
        ])

        for route in routes:

            for pattern in route["patterns"]:

                writer.writerow([
                    route["route_id"],
                    pattern,
                ])

    print(f"Saved: {filename}")


def report_routes(routes):

    print()
    print("==========================")
    print("Route Candidate Report")
    print("==========================")
    print()

    print(f"Candidate routes : {len(routes):,}")

    largest = max(
        routes,
        key=lambda r: r["pattern_count"],
    )

    print(
        f"Largest candidate : "
        f"{largest['pattern_count']} patterns"
    )

    print()

    print("First 20 candidates")
    print("-------------------")

    for route in routes[:20]:

        print(
            f"{route['route_id']}   "
            f"{route['pattern_count']:4} patterns"
        )