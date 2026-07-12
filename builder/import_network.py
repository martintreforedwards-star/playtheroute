from pathlib import Path
import csv
import json
import sys


def load_config(network):
    config_path = Path(f"data/{network}/network_config.json")

    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def main():

    if len(sys.argv) != 2:
        print("Usage: python builder/import_network.py <network>")
        return

    network = sys.argv[1]

    config = load_config(network)

    operator_code = config["operator_code"]
    operator_name = config["operator"]

    source = Path("data/Knowledgebase/NT_network_data.json")

    with open(source, encoding="utf-8") as f:
        data = json.load(f)

    stations = data["stations"]

    output_dir = Path(f"data/{network}")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{network.lower()}_master.csv"

    fields = [
        "station_name",
        "crs",
        "operator",
        "route",
        "county",
        "latitude",
        "longitude",
        "major_interchange",
        "terminus",
        "branch_junction",
        "nearest_landmark",
        "nearest_landmark_km",
        "nearest_castle",
        "nearest_castle_km",
        "nearest_cathedral",
        "nearest_cathedral_km",
        "nearest_museum",
        "nearest_museum_km",
        "nearest_country_house",
        "nearest_country_house_km",
        "nearest_nature_reserve",
        "nearest_nature_reserve_km",
    ]

    count = 0

    with open(output_file, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        for station in stations:

            op = station.get("stationOperator") or {}

            if op.get("operatorCode") != operator_code:
                continue

            location = station.get("location") or {}

            writer.writerow({
                "station_name": station.get("name", ""),
                "crs": station.get("crsCode", ""),
                "operator": operator_name,
                "route": "",
                "county": "",
                "latitude": location.get("latitude", ""),
                "longitude": location.get("longitude", ""),
                "major_interchange": "",
                "terminus": "",
                "branch_junction": "",
                "nearest_landmark": "",
                "nearest_landmark_km": "",
                "nearest_castle": "",
                "nearest_castle_km": "",
                "nearest_cathedral": "",
                "nearest_cathedral_km": "",
                "nearest_museum": "",
                "nearest_museum_km": "",
                "nearest_country_house": "",
                "nearest_country_house_km": "",
                "nearest_nature_reserve": "",
                "nearest_nature_reserve_km": "",
            })

            count += 1

    print(f"Operator : {operator_name}")
    print(f"Code     : {operator_code}")
    print(f"Stations : {count}")
    print(f"Saved    : {output_file}")


if __name__ == "__main__":
    main()