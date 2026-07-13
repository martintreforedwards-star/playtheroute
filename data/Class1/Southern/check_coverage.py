import pandas as pd

df = pd.read_csv("data/Southern/southern_master_v2.csv")

for station in [
    "Uckfield",
    "Buxted",
    "Crowborough",
    "Eridge",
    "East Grinstead",
    "Dormans",
    "Lingfield",
    "Dorking",
    "Wallington",
    "West Sutton"
]:
    print(f"{station}: {station in df['station_name'].values}")