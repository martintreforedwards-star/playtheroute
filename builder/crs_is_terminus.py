from pathlib import Path
import pandas as pd

source_file = Path("data/Class1/Scotrail/Scotrail_CRS.csv")
target_file = Path("data/Class1/Scotrail/scotrail.csv")

source = pd.read_csv(source_file, dtype=str).fillna("")
target = pd.read_csv(target_file, dtype=str).fillna("")

# Build CRS -> is_terminus lookup
lookup = (
    source[["crs", "is_terminus"]]
    .drop_duplicates(subset=["crs"])
    .set_index("crs")["is_terminus"]
    .to_dict()
)

updated = 0

for i, crs in target["crs"].items():
    if crs in lookup:
        target.at[i, "is_terminus"] = lookup[crs]
        updated += 1

target.to_csv(target_file, index=False)

print(f"Updated {updated} stations.")
print("Done.")