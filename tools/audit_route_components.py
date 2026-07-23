from pathlib import Path

import pandas as pd

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

MASTER = Path("data/Masters")

patterns_file = MASTER / "service_patterns.csv"
edges_file = MASTER / "pattern_edges.csv"
routes_file = MASTER / "routes.csv"

# ------------------------------------------------------------
# Load
# ------------------------------------------------------------

patterns = pd.read_csv(patterns_file)
edges = pd.read_csv(edges_file)
routes = pd.read_csv(routes_file)

print("=" * 60)
print("Route Component Audit")
print("=" * 60)
print()

print(f"Service patterns : {len(patterns):,}")
print(f"Edges            : {len(edges):,}")
print(f"Components        : {routes['route_id'].nunique():,}")
print()

# ------------------------------------------------------------
# Build edge lookup
# ------------------------------------------------------------

connections = {}

for _, row in edges.iterrows():
    a = row["pattern_a"]
    b = row["pattern_b"]

    connections.setdefault(a, set()).add(b)
    connections.setdefault(b, set()).add(a)

# ------------------------------------------------------------
# Route lookup
# ------------------------------------------------------------

route_lookup = dict(zip(routes["pattern_id"], routes["route_id"]))

# ------------------------------------------------------------
# Analyse every pattern
# ------------------------------------------------------------

orphans = []
isolated = []

for _, row in patterns.iterrows():

    pid = row["pattern_id"]

    neighbours = connections.get(pid, set())

    route = route_lookup.get(pid)

    if len(neighbours) == 0:
        isolated.append(pid)

    if pd.isna(route) or route is None:
        orphans.append(pid)

print(f"Patterns with no edges      : {len(isolated)}")
print(f"Patterns with no route_id   : {len(orphans)}")
print()

# ------------------------------------------------------------
# List isolated patterns
# ------------------------------------------------------------

if isolated:

    print("=" * 60)
    print("Patterns with NO EDGES")
    print("=" * 60)

    for pid in isolated:

        row = patterns.loc[patterns["pattern_id"] == pid].iloc[0]

        print()
        print(pid)

        if "origin" in patterns.columns:
            print(f"Origin      : {row['origin']}")

        if "destination" in patterns.columns:
            print(f"Destination : {row['destination']}")

        if "stations" in patterns.columns:
            stations = str(row["stations"]).split("|")
            print(f"Stations    : {len(stations)}")

# ------------------------------------------------------------
# List missing route_ids
# ------------------------------------------------------------

if orphans:

    print()
    print("=" * 60)
    print("Patterns with NO ROUTE_ID")
    print("=" * 60)

    for pid in orphans:

        row = patterns.loc[patterns["pattern_id"] == pid].iloc[0]

        print()
        print(pid)

        if "origin" in patterns.columns:
            print(f"Origin      : {row['origin']}")

        if "destination" in patterns.columns:
            print(f"Destination : {row['destination']}")

        print(f"Connected patterns : {len(connections.get(pid, []))}")

print()
print("=" * 60)
print("Audit complete")
print("=" * 60)