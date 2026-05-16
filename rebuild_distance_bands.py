import json

# LOAD JSON

with open(
    "data/stations/southeastern.json",
    "r",
    encoding="utf-8"
) as file:

    stations = json.load(file)

# DEFINITIONS

COMMUTER_MAX = 55

# TRUE COASTAL STATIONS ONLY

COASTAL_STATIONS = {

    "Margate",
    "Ramsgate",
    "Broadstairs",
    "Westgate-On-Sea",
    "Birchington-On-Sea",
    "Herne Bay",
    "Whitstable",
    "Deal",
    "Walmer",
    "Sandwich",
    "Dover Priory",
    "Folkestone Central",
    "Folkestone West",
    "Hythe",
    "New Romney",
    "Winchelsea",
    "Rye",
    "Hastings",
    "St Leonards Warrior Square",
    "Bexhill",
    "Cooden Beach",
    "Pevensey Bay",
    "Eastbourne"

}

# INNER LONDON / METRO

INNER_STATIONS = {

    "London Bridge",
    "London Cannon Street",
    "London Charing Cross",
    "London Victoria",
    "St Pancras International",
    "City Thameslink",
    "Farringdon",
    "London Blackfriars",
    "London Waterloo (East)",
    "Stratford International",
    "Lewisham",
    "New Cross",
    "St Johns",
    "Catford Bridge",
    "Ladywell",
    "Brixton",
    "Denmark Hill"

}

# PROCESS

for station in stations:

    name = station.get(
        "station_name",
        ""
    )

    mins = station.get(
        "canonical_time_to_london",
        999
    )

    # COASTAL

    if name in COASTAL_STATIONS:

        station["distance_band"] = "coastal"

    # INNER

    elif name in INNER_STATIONS:

        station["distance_band"] = "inner"

    # COMMUTER

    elif mins <= COMMUTER_MAX:

        station["distance_band"] = "commuter"

    # OUTER

    else:

        station["distance_band"] = "outer"

# SAVE

with open(
    "data/stations/southeastern.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        stations,
        file,
        indent=2,
        ensure_ascii=False
    )

print("Distance bands rebuilt.")
