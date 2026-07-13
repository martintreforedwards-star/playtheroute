from pathlib import Path
import pandas as pd
import json
import sys


def merge_csv(a, b, output):

    df1 = pd.read_csv(a)
    df2 = pd.read_csv(b)

    df = pd.concat([df1, df2], ignore_index=True)

    if "crs" in df.columns:
        df = df.drop_duplicates(subset="crs")

    if "station_name" in df.columns:
        df = df.sort_values("station_name")

    df.to_csv(output, index=False)

    print(f"Saved : {output} ({len(df)} rows)")


def merge_json(a, b, output):

    with open(a, encoding="utf-8") as f:
        j1 = json.load(f)

    with open(b, encoding="utf-8") as f:
        j2 = json.load(f)

    if isinstance(j1, list):

        merged = j1 + j2

        seen = set()
        result = []

        for station in merged:

            crs = station.get("crs")

            if crs in seen:
                continue

            seen.add(crs)
            result.append(station)

        result.sort(key=lambda x: x.get("station_name", ""))

    else:

        result = j1

    with open(output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Saved : {output} ({len(result)} records)")


def main():

    if len(sys.argv) != 4:

        print(
            "Usage:\n"
            "python builder/merge_networks.py "
            "<network1> <network2> <output>"
        )
        return

    n1, n2, out = sys.argv[1:]

    base = Path("data")
    (base / out).mkdir(parents=True, exist_ok=True)
    merge_csv(
        base / n1 / f"{n1.lower()}_master.csv",
        base / n2 / f"{n2.lower()}_master.csv",
        base / out / f"{out.lower()}_master.csv",
    )

    merge_csv(
        base / n1 / f"{n1.lower()}_enriched.csv",
        base / n2 / f"{n2.lower()}_enriched.csv",
        base / out / f"{out.lower()}_enriched.csv",
    )

    merge_json(
        base / n1 / f"{n1.lower()}.json",
        base / n2 / f"{n2.lower()}.json",
        base / out / f"{out.lower()}.json",
    )


if __name__ == "__main__":
    main()