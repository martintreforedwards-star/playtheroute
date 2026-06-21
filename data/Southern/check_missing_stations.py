import pandas as pd

crs = pd.read_csv("crs_source_of_truth.csv")

stations = [
    "Uckfield",
    "Buxted",
    "Crowborough",
    "Eridge",
    "East Grinstead",
    "Dormans",
    "Lingfield",
    "Wallington",
    "West Sutton",
    "Dorking",
    "Dorking Deepdene",
    "Dorking West",
    "Holmwood",
    "Ockley",
    "Warnham"
]

for station in stations:
    match = crs[
        crs["stationName"].str.lower() == station.lower()
    ]

    if len(match):
        print(f"{station}: FOUND")
    else:
        print(f"{station}: NOT FOUND")