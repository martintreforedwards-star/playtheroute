import pandas as pd

southern = pd.read_csv("data/Southern/southern_master_v2.csv")
crs = pd.read_csv("crs_source_of_truth.csv")

# same name fixes used during merge
name_fixes = {
    "Berwick": "Berwick (Sussex)",
    "Durrington-on-Sea": "Durrington-On-Sea",
    "Earlswood": "Earlswood (Surrey)",
    "Goring-by-Sea": "Goring-By-Sea",
    "Shoreham-by-Sea": "Shoreham-By-Sea",
    "Sutton": "Sutton (London)"
}

southern["lookup_name"] = southern["station_name"].replace(name_fixes)

# bring in authoritative CRS
check = southern.merge(
    crs[["stationName", "crsCode"]],
    left_on="lookup_name",
    right_on="stationName",
    how="left"
)

# compare
mismatches = check[
    check["crs"] != check["crsCode"]
]

print("Stations checked:", len(check))
print("Mismatches:", len(mismatches))

if len(mismatches) > 0:
    print(
        mismatches[
            ["station_name", "crs", "crsCode"]
        ].sort_values("station_name")
    )