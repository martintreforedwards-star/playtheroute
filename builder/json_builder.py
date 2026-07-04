from pathlib import Path
import ast
import csv
import json


def build_json(config):

    network = config["network"]

    input_file = Path(
        config.get(
            "enriched",
            Path("data") / network / f"{network.lower()}_enriched.csv"
        )
    )

    output_file = Path(
        config.get(
            "output",
            Path("data") / network / f"{network.lower()}.json"
        )
    )

    stations = []

    with open(input_file, newline="", encoding="utf-8-sig") as f:

        reader = csv.DictReader(f)

        for row in reader:

            if "route_groups" in row:
                try:
                    row["route_groups"] = ast.literal_eval(row["route_groups"])
                except Exception:
                    row["route_groups"] = []

            stations.append(row)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(stations, f, indent=2)

    print(f"JSON saved : {output_file}")