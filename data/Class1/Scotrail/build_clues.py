import json

# =====================================================
# LOAD SOUTHEASTERN CLUES
# =====================================================

with open("data/clues/southeastern-clues.json", "r", encoding="utf-8") as f:
    clues = json.load(f)

# =====================================================
# SOUTHERN CONFIGURATION
# =====================================================

southern_regions = [
    "Brighton Main Line",
    "West Coastway",
    "East Coastway",
    "Arun Valley",
    "Portsmouth",
    "Uckfield Branch",
    "East Grinstead Branch",
    "Mole Valley",
    "Sutton Loop",
    "West London Line",
    "Waterloo"
]

southern_routes = southern_regions.copy()

terminal_map = {
    "Charing Cross": "London Victoria",
    "Cannon Street": "London Bridge",
    "Victoria": "London Victoria",
    "St Pancras": "St Pancras International"
}

# =====================================================
# PROCESS EXISTING CLUES
# =====================================================

def process(pool):

    output = []

    for clue in pool:

        clue = clue.copy()

        # Remove High Speed
        if clue.get("display") == "High Speed 1":
            continue

        # Remove Southeastern region clues
        if clue.get("field") == "region":
            continue

        # Remove Southeastern route group clues
        if (
            clue.get("type") == "array_contains"
            and clue.get("field") == "route_groups"
        ):
            continue

        # Replace London terminal names
        if "display" in clue:
            for old, new in terminal_map.items():
                clue["display"] = clue["display"].replace(old, new)

        output.append(clue)

    return output


clues["rowPool"] = process(clues["rowPool"])
clues["columnPool"] = process(clues["columnPool"])

# =====================================================
# ADD SOUTHERN REGION CLUES
# =====================================================

for region in southern_regions:

    clues["columnPool"].append(
        {
            "display": region,
            "type": "field",
            "field": "region",
            "value": region,
            "weight": "medium",
            "category": "geography"
        }
    )

# =====================================================
# ADD SOUTHERN ROUTE GROUP CLUES
# =====================================================

for route in southern_routes:

    clues["columnPool"].append(
        {
            "display": route,
            "type": "array_contains",
            "field": "route_groups",
            "value": route,
            "weight": "medium",
            "category": "route"
        }
    )

# =====================================================
# SAVE
# =====================================================

with open(
    "data/Southern/southern-clues.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(clues, f, indent=2)

print()
print("Southern clues generated.")
print(f"Regions: {len(southern_regions)}")
print(f"Route groups: {len(southern_routes)}")