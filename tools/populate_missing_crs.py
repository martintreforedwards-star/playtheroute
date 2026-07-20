import pandas as pd

FILE = "data/Class1/Southern/southern_aggregated_1.csv"

CRS_LOOKUP = {
    "Ashurst": "ASH",
    "Blackfriars": "BFR",
    "Bognor Regis": "BOG",
    "Buxted": "BXD",
    "City Thameslink": "CTK",
    "Cowden": "CWN",
    "Crowborough": "COH",
    "Dorking": "DKG",
    "Dorking West": "DKT",
    "Dormans": "DMS",
    "East Grinstead": "EGR",
    "East Worthing": "EWR",
    "Edenbridge Town": "EBT",
    "Eridge": "ERI",
    "Farringdon": "ZFD",
    "Hever": "HEV",
    "Holmwood": "HLM",
    "Horsham": "HRH",
    "Hurst Green": "HGD",
    "Lingfield": "LFD",
    "Ockley": "OCK",
    "Oxted": "OXT",
    "St Pancras International": "STP",
    "Uckfield": "UCK",
    "Upper Warlingham": "UWL",
    "Wallington": "WLT",
    "Warnham": "WNH",
    "West Sutton": "WSU",
    "Whyteleafe": "WHY",
    "Woldingham": "WOH",
}

df = pd.read_csv(FILE)

updated = 0

for i, row in df.iterrows():

    if pd.notna(row["crs"]) and str(row["crs"]).strip():
        continue

    station = str(row["station_name"]).strip()

    if station in CRS_LOOKUP:
        df.at[i, "crs"] = CRS_LOOKUP[station]
        updated += 1
        print(f"{station} -> {CRS_LOOKUP[station]}")

df.to_csv(FILE, index=False)

print(f"\nUpdated {updated} CRS codes.")