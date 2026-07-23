from pathlib import Path
import pandas as pd

scotrail_file = Path("data/Class1/Scotrail/scotrail.csv")
membership_file = Path("data/Class1/Scotrail/route_group_membership.csv")

scotrail = pd.read_csv(scotrail_file, dtype=str).fillna("")
membership = pd.read_csv(membership_file, dtype=str).fillna("")

# Ensure route order is numeric
membership["route_order"] = pd.to_numeric(
    membership["route_order"], errors="coerce"
)

termini = set()

for _, group in membership.groupby("route_group"):
    group = group.sort_values("route_order")

    if group.empty:
        continue

    termini.add(group.iloc[0]["station_name"])
    termini.add(group.iloc[-1]["station_name"])

scotrail["is_terminus"] = scotrail["station_name"].isin(termini)
scotrail["is_terminus"] = (
    scotrail["is_terminus"]
    .map({True: "TRUE", False: "FALSE"})
)

scotrail.to_csv(scotrail_file, index=False)

print(f"Termini identified: {len(termini)}")
print(
    f"Stations marked as terminus: "
    f"{(scotrail['is_terminus'] == 'TRUE').sum()}"
)
print("Done.")