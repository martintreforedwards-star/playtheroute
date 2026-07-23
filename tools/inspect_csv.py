from pathlib import Path
import pandas as pd

MASTER = Path("data/Masters")

for filename in [
    "service_patterns.csv",
    "service_divergences.csv",
    "service_corridors.csv",
    "route_candidates.csv",
    "route_tree.csv",
]:
    path = MASTER / filename

    print("=" * 70)
    print(filename)

    df = pd.read_csv(path)

    print()
    print("Columns:")
    print(list(df.columns))

    print()
    print("Rows:", len(df))

    print()
    print(df.head(3))
    print()