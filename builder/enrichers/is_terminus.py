from pathlib import Path
import pandas as pd

SERVICE_PATTERNS = Path("data/Masters/service_patterns.csv")
SCOTRAIL = Path("data/Class1/Scotrail/scotrail.csv")

# --------------------------------------------------------------------
# Load data
# --------------------------------------------------------------------

patterns = pd.read_csv(SERVICE_PATTERNS, dtype=str).fillna("")
stations = pd.read_csv(SCOTRAIL, dtype=str).fillna("")

# --------------------------------------------------------------------
# Collect every origin and destination CRS
# --------------------------------------------------------------------

termini = set()

for _, row in patterns.iterrows():

    origin = row["origin"].strip()
    destination = row["destination"].strip()

    if origin:
        termini.add(origin)

    if destination:
        termini.add(destination)

# --------------------------------------------------------------------
# Populate field
# --------------------------------------------------------------------

stations["is_terminus"] = stations["crs"].apply(
    lambda x: "TRUE" if x in termini else "FALSE"
)

stations.to_csv(SCOTRAIL, index=False)

print(f"Unique termini found : {len(termini)}")
print(
    f"Stations marked TRUE : "
    f"{(stations['is_terminus'] == 'TRUE').sum()}"
)
print("Done.")