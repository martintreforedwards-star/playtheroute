import pandas as pd

LOOKUP = "data/Reference/county_lookup.csv"
STATIONS = "data/Class1/Southern/southern_aggregated_1.csv"

# Simple keyword rules
RULES = {
    "Greater London": [
        "London", "Victoria", "Bridge", "Clapham", "Croydon",
        "Sydenham", "Penge", "Norwood", "Forest Hill",
        "Honor Oak", "New Cross", "Peckham", "Battersea",
        "Wandsworth", "Streatham", "Tooting", "Mitcham",
        "Crystal Palace", "Denmark Hill", "Elephant",
        "Herne Hill", "Brixton"
    ],
    "Brighton and Hove": [
        "Brighton",
        "Hove",
        "Preston Park",
        "London Road (Brighton)"
    ],
    "Kent": [
        "Ashford", "Canterbury", "Dover", "Folkestone",
        "Maidstone", "Ramsgate", "Margate", "Tonbridge",
        "Tunbridge", "Sevenoaks"
    ],
    "East Sussex": [
        "Lewes", "Eastbourne", "Bexhill", "Hastings",
        "Battle", "Crowhurst", "Rye", "Ore",
        "Pevensey", "Polegate", "St Leonards"
    ],
    "West Sussex": [
        "Worthing", "Littlehampton", "Bognor", "Chichester",
        "Arundel", "Barnham", "Horsham", "Shoreham",
        "Lancing", "Angmering", "Ford", "Fishbourne"
    ],
    "Surrey": [
        "Redhill", "Reigate", "Horley", "Merstham",
        "Earlswood", "Salfords", "Oxted", "Caterham"
    ],
    "Hampshire": [
        "Portsmouth", "Southampton", "Winchester",
        "Fareham", "Cosham", "Fratton", "Havant",
        "Hilsea", "Portchester"
    ],
}

lookup = pd.read_csv(LOOKUP)
stations = pd.read_csv(STATIONS)

lookup["crs"] = lookup["crs"].fillna("").astype(str).str.upper()
stations["crs"] = stations["crs"].fillna("").astype(str).str.upper()

name_col = next(
    c for c in stations.columns
    if c.lower() in ("name", "station_name", "station")
)

name_lookup = dict(zip(stations["crs"], stations[name_col]))

updated = 0

for i, row in lookup.iterrows():

    county = row.get("county")

    if pd.notna(county) and str(county).strip():
        continue

    name = name_lookup.get(row["crs"], "")

    for county, keywords in RULES.items():
        if any(k.lower() in name.lower() for k in keywords):
            lookup.at[i, "county"] = county
            updated += 1
            print(f"{row['crs']} -> {county}")
            break

lookup.to_csv(LOOKUP, index=False)

print(f"\nUpdated {updated} counties.")