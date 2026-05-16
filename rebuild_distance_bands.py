import json

with open(
    "data/stations/southeastern.json",
    "r",
    encoding="utf-8"
) as file:

    stations = json.load(file)

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
    "Rye",
    "Hastings"

}

INNER_STATIONS = {

    "London Bridge",
    "London Cannon Street",
    "London Charing Cross",
    "London Victoria",
    "City Thameslink",
    "Farringdon",
    "London Blackfriars",
    "London Waterloo (East)",
    "Lewisham"

}

for station in stations:

    name = station.get(
        "station_name",
        ""
    )

    mins = station.get(
        "canonical_time_to_london",
        999
    )

    if name in COASTAL_STATIONS:

        station["distance_band"] = "coastal"

    elif name in INNER_STATIONS:

        station["distance_band"] = "inner"

    elif mins <= 55:

        station["distance_band"] = "commuter"

    else:

        station["distance_band"] = "outer"

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
