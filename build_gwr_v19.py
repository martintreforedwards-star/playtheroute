import csv

termini = set()
interchanges = set()

with open("gwr_termini.txt", encoding="utf-8") as f:
    for line in f:
        termini.add(line.strip())

with open("gwr_interchanges.txt", encoding="utf-8") as f:
    for line in f:
        interchanges.add(line.strip())

with open("gwr_stations_master_v18.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.reader(f))

header = rows[0]
data = rows[1:]

terminus_count = 0
interchange_count = 0

for row in data:

    station = row[1]

    row[4] = "TRUE" if station in termini else "FALSE"
    row[5] = "TRUE" if station in interchanges else "FALSE"

    if row[4] == "TRUE":
        terminus_count += 1

    if row[5] == "TRUE":
        interchange_count += 1

with open("gwr_stations_master_v19.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)

print("Stations:", len(data))
print("Termini:", terminus_count)
print("Interchanges:", interchange_count)
print("Created gwr_stations_master_v19.csv")
