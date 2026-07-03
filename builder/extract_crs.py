import json

with open("data/Knowledgebase/ME_network_data.json", encoding="utf-8") as f:
    data = json.load(f)

config = {
    "network": "Merseyrail",
    "display_name": "Merseyrail",
    "knowledgebase": "data/Knowledgebase/ME_network_data.json",
    "crs": sorted(
        station["crsCode"]
        for station in data["stations"]
        if station.get("crsCode")
    )
}

with open("builder/configs/merseyrail.json", "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)

print("merseyrail.json created")