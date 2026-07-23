from pathlib import Path
import pandas as pd

membership_file = Path("data/Class1/Scotrail/route_group_membership.csv")
scotrail_file = Path("data/Class1/Scotrail/scotrail.csv")

membership = pd.read_csv(membership_file, dtype=str).fillna("")
scotrail = pd.read_csv(scotrail_file, dtype=str).fillna("")

# If a station appears more than once, combine all its route groups
lookup = (
    membership.groupby("station_name")["route_group"]
    .apply(lambda s: "|".join(sorted(set(x for x in s if x))))
    .to_dict()
)

updated = 0

for i, station in scotrail["station_name"].items():
    if station in lookup:
        scotrail.at[i, "route_groups"] = lookup[station]
        updated += 1

scotrail.to_csv(scotrail_file, index=False)

print(f"Updated {updated} stations.")