import csv

bands = {}

with open("gwr_new_station_bands.txt", encoding="utf-8") as f:
    for line in f:
        station, band = line.strip().split(",", 1)
        bands[station] = band

with open("gwr_stations_master_v17.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.reader(f))

header = rows[0]
data = rows[1:]

updated = 0

for row in data:
    station = row[1]

    if station in bands:
        row[11] = bands[station]   # distance_band
        updated += 1

with open("gwr_stations_master_v18.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)

print("Rows updated:", updated)
print("Created gwr_stations_master_v18.csv")
