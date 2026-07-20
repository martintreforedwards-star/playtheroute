import pandas as pd

FILE = "data/Class1/Southern/southern_aggregated_1.csv"
OPERATOR = "Southern"


def main():

    df = pd.read_csv(FILE)

    if "operator" not in df.columns:
        df["operator"] = ""

    df["operator"] = OPERATOR

    df.to_csv(FILE, index=False)

    print(f"Updated {len(df)} stations.")
    print(f"Operator set to '{OPERATOR}'.")


if __name__ == "__main__":
    main()