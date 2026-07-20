import pandas as pd

AGGREGATE = "data/Class1/Southern/southern_aggregated_1.csv"
LOOKUP = "data/Reference/county_lookup.csv"


def main():

    agg = pd.read_csv(AGGREGATE)
    lookup = pd.read_csv(LOOKUP)

    agg["crs"] = (
        agg["crs"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    lookup["crs"] = (
        lookup["crs"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    lookup = lookup.drop_duplicates("crs")

    agg = agg.drop(columns=["county"], errors="ignore")

    agg = agg.merge(
        lookup,
        on="crs",
        how="left"
    )

    agg.to_csv(AGGREGATE, index=False)

    print(f"Counties populated: {agg['county'].notna().sum()} of {len(agg)}")


if __name__ == "__main__":
    main()