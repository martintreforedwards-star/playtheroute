import pandas as pd

# -----------------------------
# LOAD FILES
# -----------------------------

southern = pd.read_csv("data/Southern/southern_master_v1.csv")
crs = pd.read_csv("crs_source_of_truth.csv")

# -----------------------------
# FIX STATION NAME MISMATCHES
# -----------------------------

name_fixes = {
    "Berwick": "Berwick (Sussex)",
    "Durrington-on-Sea": "Durrington-On-Sea",
    "Earlswood": "Earlswood (Surrey)",
    "Goring-by-Sea": "Goring-By-Sea",
    "Shoreham-by-Sea": "Shoreham-By-Sea",
    "Sutton": "Sutton (London)"
}

southern["lookup_name"] = (
    southern["station_name"]
    .replace(name_fixes)
)

# -----------------------------
# MERGE CRS DATA
# -----------------------------

merged = southern.merge(
    crs[["stationName", "crsCode", "lat", "long"]],
    left_on="lookup_name",
    right_on="stationName",
    how="left"
)

# -----------------------------
# POPULATE CRS + COORDINATES
# -----------------------------

merged["crs"] = merged["crsCode"]
merged["latitude"] = merged["lat"]
merged["longitude"] = merged["long"]

# -----------------------------
# CREATE STATION IDS
# -----------------------------

merged["station_id"] = [
    f"SR{str(i+1).zfill(3)}"
    for i in range(len(merged))
]

# -----------------------------
# CLEANUP
# -----------------------------

merged = merged.drop(
    columns=[
        "lookup_name",
        "stationName",
        "crsCode",
        "lat",
        "long"
    ],
    errors="ignore"
)

# -----------------------------
# VALIDATION
# -----------------------------

print("Missing CRS:", merged["crs"].isna().sum())
print("Duplicate CRS:", merged["crs"].duplicated().sum())

# -----------------------------
# SAVE
# -----------------------------

merged.to_csv(
    "data/Southern/southern_master_v2.csv",
    index=False
)

print("Saved southern_master_v2.csv")