import pandas as pd

df = pd.read_csv("data/Southern/southern_master_v1.csv")

dupes = df[df["crs"].duplicated(keep=False)]

print("Duplicate CRS count:", len(dupes))

if len(dupes) > 0:
    print(dupes[["station_name", "crs"]].sort_values("crs"))