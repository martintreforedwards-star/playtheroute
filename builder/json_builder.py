from pathlib import Path
import ast
import csv
import json


def build_json(config):

    input_file = Path(config["enriched"])
    output_file = Path(config["output"])

    stations = []

    with open(input_file, newline="", encoding="utf-8-sig") as f:

        reader = csv.DictReader(f)

        for row in reader:

            try:
                row["route_groups"] = ast.literal_eval(
                    row["route_groups"]
                )
            except Exception:
                pass

            stations.append(row)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(stations, f, indent=2)

    print(f"JSON saved : {output_file}")