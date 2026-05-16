# LOAD JSON

with open(
    "data/stations/southeastern.json",
    "r",
    encoding="utf-8"
) as file:

    stations = json.load(file)

# DEFINITIONS

INNER_MAX = 25
COMMUTER_MAX = 55

COASTAL_STATIONS = {

    "Margate",
    "Ramsgate",
    "Broadstairs",
    "Whitstable",
    "Herne Bay",
    "Deal",
    "Dover Priory",
    "Folkestone Central",
    "Folkestone West",
    "Rye",
    "Hastings",
    "Westgate-On-Sea",
    "Birchington-On-Sea",
    "Walmer",
    "Sandwich"

}

INNER_STATIONS = {

    "London Bridge",
    "London Cannon Street",
    "London Charing Cross",
    "London Victoria",
    "City Thameslink",
    "Farringdon",
    "London Blackfriars",
    "Waterloo East"

}

# PROCESS

for station in stations:

    name = station.get(
        "station_name",
        ""
    )

    mins = station.get(
        "travel_time_mins",
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

print(
    "Distance bands rebuilt."
)
