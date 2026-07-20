from pathlib import Path

import pandas as pd


def import_reference_data(config, stations):

    aggregated_file = Path(config["aggregated"])

    if not aggregated_file.exists():
        print(f"Reference file not found: {aggregated_file}")
        return stations

    reference = pd.read_csv(aggregated_file)

    stations.columns = stations.columns.str.strip()
    reference.columns = reference.columns.str.strip()

    stations["crs"] = (
        stations["crs"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    reference["crs"] = (
        reference["crs"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    print("\nBuilder CRS:")
    print(stations["crs"].head(10).tolist())

    print("\nReference CRS:")
    print(reference["crs"].head(10).tolist())

    # Only import fields that cannot be derived by the Builder.
    merge_fields = [
        "operator",
        "route",
        "county",
        "major_interchange",
        "branch_junction",
    ]

    available = [c for c in merge_fields if c in reference.columns]

    print("\nReference rows with CRS:", reference["crs"].ne("").sum())

    merged = stations.merge(
        reference[["crs"] + available],
        on="crs",
        how="left",
        suffixes=("", "_ref"),
    )

    print("Rows after merge:", len(merged))

    for field in available:
        ref = f"{field}_ref"

        if ref in merged.columns:
            print(f"{field}: {merged[ref].notna().sum()} matches")
            merged[field] = merged[ref].combine_first(merged[field])
            merged.drop(columns=[ref], inplace=True)

    return merged