import pandas as pd

new_file = r"data/Class1/Southern/southern.csv"
source_file = r"data/Class1/Southern/southern_aggregated_1.csv"

new_df = pd.read_csv(new_file, dtype=str).fillna("")
source_df = pd.read_csv(source_file, dtype=str).fillna("")

lookup = (
    source_df[["crs", "terminus"]]
    .drop_duplicates(subset=["crs"])
)

new_df = new_df.drop(columns=["terminus"], errors="ignore")
new_df = new_df.merge(lookup, on="crs", how="left")

new_df.to_csv(new_file, index=False)

print(f"Updated terminus for {new_df['terminus'].notna().sum()} stations.")