import pandas as pd

master = pd.read_csv(
    "data/Chiltern/chiltern_midlands_master_v6.csv"
)

reference = pd.read_csv(
    "data/crs_source_of_truth.csv"
)

def normalise(text):
    return (
        str(text)
        .lower()
        .replace("'", "")
        .strip()
    )

master["match_name"] = master["station_name"].apply(normalise)
reference["match_name"] = reference["stationName"].apply(normalise)

merged = master.merge(
    reference[["match_name", "crsCode"]],
    on="match_name",
    how="left"
)

matches = merged[
    merged["crs"] == merged["crsCode"]
]

mismatches = merged[
    (merged["crsCode"].notna()) &
    (merged["crs"] != merged["crsCode"])
]

not_found = merged[
    merged["crsCode"].isna()
]

print("Matches:", len(matches))
print("Mismatches:", len(mismatches))
print("Not found:", len(not_found))

mismatches.to_csv(
    "crs_mismatches.csv",
    index=False
)

not_found.to_csv(
    "crs_not_found.csv",
    index=False
)