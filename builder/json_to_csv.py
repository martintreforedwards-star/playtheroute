import json
import pandas as pd

json_file = r"data/Class1/Southern/southern.json"
csv_file = r"data/Class1/Southern/southern.csv"

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

pd.DataFrame(data).to_csv(csv_file, index=False)

print(f"Saved {len(data)} stations to {csv_file}")