import json
import sys
from pathlib import Path

OPERATORS = {
    "AW": "Transport for Wales",
    "CC": "c2c",
    "LE": "Greater Anglia",
    "ME": "Merseyrail",
    "NT": "Northern",
    "SE": "Southeastern",
    "SN": "Southern",
    "SW": "South Western Railway",
}


def main():

    if len(sys.argv) != 3:
        print("Usage:")
        print("python builder/create_configs.py <Folder> <TOC>")
        return

    folder = sys.argv[1]
    toc = sys.argv[2].upper()

    operator = OPERATORS.get(toc)

    if operator is None:
        print(f"Unknown operator code: {toc}")
        return

    network_id = folder.lower()

    # ----------------------------
    # data/<Network>/network_config.json
    # ----------------------------

    data_folder = Path("data") / folder
    data_folder.mkdir(parents=True, exist_ok=True)

    network_config = {
        "network": folder,
        "network_id": network_id,
        "operator": operator,
        "operator_code": toc,
    }

    with open(data_folder / "network_config.json", "w", encoding="utf-8") as f:
        json.dump(network_config, f, indent=2)

    # ----------------------------
    # builder/configs/<network>.json
    # ----------------------------

    config_folder = Path("builder/configs")
    config_folder.mkdir(parents=True, exist_ok=True)

    builder_config = {
        "name": folder,
        "network": folder,
        "master": f"data/{folder}/{network_id}_master.csv",
        "route_groups": f"data/{folder}/route_membership.csv",
        "missing_times": f"data/{folder}/missing_times.csv",
        "rules": f"builder/configs/{network_id}_rules.json",
        "clue_template": "data/clues/southeastern-clues.json",
        "clues": f"data/{folder}/{network_id}-clues.json",
        "enriched": f"data/{folder}/{network_id}_enriched.csv",
        "output": f"data/{folder}/{network_id}.json",
    }

    with open(config_folder / f"{network_id}.json", "w", encoding="utf-8") as f:
        json.dump(builder_config, f, indent=2)

    print(f"Created data/{folder}/network_config.json")
    print(f"Created builder/configs/{network_id}.json")


if __name__ == "__main__":
    main()