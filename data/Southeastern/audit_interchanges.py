import json
from pathlib import Path

JSON_FILE = Path("data/stations/southeastern.json")

NON_INTERCHANGES = {
    "Brixton",
    "Herne Hill",
    "Penge East",
    "Sydenham Hill",
    "West Dulwich",
    "Kent House",
    "Farningham Road",
    "Longfield",
    "Meopham",
    "Sole Street",
    "Farringdon",
    "City Thameslink",
    "Belvedere",
    "Erith",
    "Slade Green",
    "New Cross",
    "St Johns",
    "Lewisham",
    "Blackheath",
    "Kidbrooke",
    "Eltham",
    "Falconwood",
    "Welling",
    "Bexleyheath",
    "Barnehurst",
    "Hither Green",
    "Lee",
    "Mottingham",
    "New Eltham",
    "Sidcup",
    "Albany Park",
    "Bexley",
    "Crayford",
    "Ladywell",
    "Crofton Park",
    "Catford",
    "Bellingham",
    "Beckenham Hill",
    "Ravensbourne",
    "Bromley North",
    "Sundridge Park",
    "Elmstead Woods",
    "Chislehurst",
    "New Beckenham",
    "Clock House",
    "Elmers End",
    "Eden Park",
    "West Wickham",
    "Hayes",
    "Chelsfield",
    "Knockholt",
    "Dunton Green",
    "Bat & Ball",
    "Hildenborough",
    "Kemsing",
    "Borough Green & Wrotham",
    "West Malling",
    "East Malling",
    "Barming",
    "High Brooms",
    "Tunbridge Wells",
    "Frant",
    "Wadhurst",
    "Stonegate",
    "Etchingham",
    "Robertsbridge",
    "Battle",
    "Crowhurst",
    "West St Leonards",
    "St Leonards Warrior Square",
    "Hastings",
    "Ore",
    "Three Oaks",
    "Winchelsea",
    "Rye",
    "Appledore",
    "Ham Street",
    "Marden",
    "Staplehurst",
    "Headcorn",
    "Pluckley",
    "Beltring",
    "Yalding",
    "Wateringbury",
    "East Farleigh",
    "Maidstone East",
    "Bearsted",
    "Hollingbourne",
    "Harrietsham",
    "Lenham",
    "Charing",
    "Sheerness-on-Sea",
    "Queenborough",
    "Swale",
    "Kemsley",
    "Newington",
    "Teynham",
    "Minster",
    "Sturry",
    "Chartham",
    "Chilham",
    "Wye",
    "Westenhanger",
    "Sandling",
    "Canterbury East",
    "Kearsney"
}

with open(JSON_FILE, "r", encoding="utf-8") as f:
    stations = json.load(f)

interchanges = []
non_interchanges = []

for station in stations:

    name = station["station_name"]

    if name in NON_INTERCHANGES:
        non_interchanges.append(name)
    else:
        interchanges.append(name)

print("=" * 70)
print("INTERCHANGE CANDIDATES")
print("=" * 70)

for name in sorted(interchanges):
    print(name)

print()
print(f"TOTAL: {len(interchanges)}")

print()
print("=" * 70)
print("NON-INTERCHANGES")
print("=" * 70)

for name in sorted(non_interchanges):
    print(name)

print()
print(f"TOTAL: {len(non_interchanges)}")