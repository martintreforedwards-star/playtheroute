import pandas as pd

master = pd.read_csv(
    "/workspaces/playtheroute/data/Masters/master_station_enriched.csv"
)

missing = master[
    master["latitude"].isna() |
    master["longitude"].isna()
]

print(missing)