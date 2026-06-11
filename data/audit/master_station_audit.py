import pandas as pd

master = pd.read_csv(
    "/workspaces/playtheroute/data/Masters/master_station_deduped.csv"
)

print("Stations:", len(master))
print("Duplicate CRS:", master["crs"].duplicated().sum())
print("Missing CRS:", master["crs"].isna().sum())
print("Missing Latitude:", master["latitude"].isna().sum())
print("Missing Longitude:", master["longitude"].isna().sum())