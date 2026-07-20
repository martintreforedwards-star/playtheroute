import pandas as pd

AGGREGATE = "data/Class1/Southern/southern_aggregated_1.csv"

JUNCTIONS = {
    "ARU",  # Arundel
    "BTN",  # Brighton
    "CLJ",  # Clapham Junction
    "ECR",  # East Croydon
    "HHE",  # Hove
    "HRH",  # Horsham
    "LEW",  # Lewes
    "THB",  # Three Bridges
    "WIV",  # Worthing
}

df = pd.read_csv(AGGREGATE)

df["branch_junction"] = (
    df["crs"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.upper()
    .isin(JUNCTIONS)
)

df.to_csv(AGGREGATE, index=False)

print(f"Branch junctions populated: {int(df['branch_junction'].sum())}")