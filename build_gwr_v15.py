import csv

# Load existing stations
with open("gwr_stations_master_v14.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.reader(f))

header = rows[0]
existing = rows[1:]

# Load CRS source
stations = {}

with open("crs_source_of_truth.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        stations[row["stationName"]] = row

routes = {
    "Theale":"Berks & Hants Line",
    "Reading West":"Berks & Hants Line",
    "Aldermaston":"Berks & Hants Line",
    "Midgham":"Berks & Hants Line",
    "Thatcham":"Berks & Hants Line",
    "Newbury Racecourse":"Berks & Hants Line",
    "Newbury":"Berks & Hants Line",
    "Kintbury":"Berks & Hants Line",
    "Hungerford":"Berks & Hants Line",
    "Bedwyn":"Berks & Hants Line",
    "Pewsey":"Berks & Hants Line",

    "Westbury":"TransWilts Line",
    "Melksham":"TransWilts Line",

    "Dilton Marsh":"Westbury Branch",
    "Warminster":"Westbury Branch",

    "Trowbridge":"Avon Valley Line",
    "Bradford-on-Avon":"Avon Valley Line",
    "Freshford":"Avon Valley Line",
    "Avoncliff":"Avon Valley Line",

    "Frome":"Heart of Wessex Line",
    "Bruton":"Heart of Wessex Line",
    "Castle Cary":"Heart of Wessex Line",
    "Yeovil Pen Mill":"Heart of Wessex Line",
    "Thornford":"Heart of Wessex Line",
    "Yetminster":"Heart of Wessex Line",
    "Chetnole":"Heart of Wessex Line",
    "Maiden Newton":"Heart of Wessex Line",
    "Dorchester West":"Heart of Wessex Line",
    "Upwey":"Heart of Wessex Line",
    "Weymouth":"Heart of Wessex Line"
}

new_rows = []

with open("gwr_missing_confirmed.txt", encoding="utf-8") as f:
    for line in f:
        station = line.strip()

        lookup = station
        if station == "Bradford-on-Avon":
            lookup = "Bradford-On-Avon"

        s = stations[lookup]

        station_id = "STN_" + station.lower().replace(" ", "_").replace("-", "_")

        terminus = "TRUE" if station in ["Bedwyn", "Weymouth"] else "FALSE"

        interchange = "TRUE" if station in [
            "Newbury",
            "Westbury",
            "Trowbridge"
        ] else "FALSE"

        row = [
            station_id,
            station,
            s["crsCode"],
            routes[station],
            terminus,
            interchange,
            "",
            s["lat"],
            s["long"],
            s["constituentCountry"],
            "",
            "",
            "FALSE",
            "",
            ""
        ]

        new_rows.append(row)

with open("gwr_v15_preview.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(new_rows)

print("Created gwr_v15_preview.csv")
print("Rows:", len(new_rows))
