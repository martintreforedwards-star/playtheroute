import pandas as pd

master = pd.read_csv("data/Class1/Southern/southern_master.csv")
agg = pd.read_csv("data/Class1/Southern/southern_aggregated_1.csv")

lookup = master[["crs", "station_id"]]

agg = agg.drop(columns=["station_id"], errors="ignore")
agg = agg.merge(lookup, on="crs", how="left")

cols = ["station_id"] + [c for c in agg.columns if c != "station_id"]
agg = agg[cols]

agg.to_csv("data/Class1/Southern/southern_aggregated_1.csv", index=False)

print("Updated station_id values.")