import pandas as pd

master = pd.read_csv("data/Chiltern/chiltern_midlands_master_v5.csv")
source = pd.read_csv("crs_source_of_truth.csv")

master["key"] = master["station_name"].str.lower().str.replace("'", "", regex=False)
source["key"] = source["stationName"].str.lower().str.replace("'", "", regex=False)

merged = master.merge(
    source[["key", "crsCode", "lat", "long"]],
    on="key",
    how="left"
)

merged["crs"] = merged["crsCode"].fillna(merged["crs"])
merged["latitude"] = merged["lat"].fillna(merged["latitude"])
merged["longitude"] = merged["long"].fillna(merged["longitude"])

merged.drop(columns=["key", "crsCode", "lat", "long"], inplace=True)

merged.to_csv(
    "data/Chiltern/chiltern_midlands_master_v6.csv",
    index=False
)

print("Done")
print("Missing lat:", merged["latitude"].isna().sum())
print("Missing lon:", merged["longitude"].isna().sum())