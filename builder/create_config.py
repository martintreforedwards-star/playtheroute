import json
from pathlib import Path


def create_config(network_name, knowledgebase):

    with open(knowledgebase, encoding="utf-8") as f:
        data = json.load(f)

    crs = sorted(
        station["crsCode"]
        for station in data["stations"]
        if station.get("crsCode")
    )

    config = {
        "network": network_name,
        "display_name": network_name,
        "knowledgebase": knowledgebase.replace("\\", "/"),
        "crs": crs,
    }

    output = Path("builder/configs") / f"{network_name.lower()}.json"

    with output.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print(f"Created {output}")
    print(f"{len(crs)} CRS codes")


if __name__ == "__main__":

    create_config(
        "Merseyrail",
        "data/Knowledgebase/ME_network_data.json",
    )