from pathlib import Path
import pandas as pd

MASTER = Path("data/Masters")

patterns = pd.read_csv(MASTER / "service_patterns.csv")
candidates = pd.read_csv(MASTER / "route_candidates.csv")

candidate_lookup = set(candidates["pattern_id"])

missing = patterns[patterns["route_id"].isna()]

print("=" * 60)
print("Missing Route Audit")
print("=" * 60)

print(f"Total patterns        : {len(patterns):,}")
print(f"Route candidates      : {len(candidates):,}")
print(f"Missing route_id      : {len(missing):,}")
print()

for _, row in missing.iterrows():

    pid = row["pattern_id"]

    print(pid)
    print(f"Origin      : {row['origin']}")
    print(f"Destination : {row['destination']}")
    print(f"Stations    : {row['station_count']}")
    print(f"Services    : {row['service_count']}")
    print(f"In candidates : {pid in candidate_lookup}")
    print()