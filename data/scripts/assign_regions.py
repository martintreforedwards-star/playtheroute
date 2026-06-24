import csv

INPUT_FILE = "crs_source_of_truth.csv"

rows = []

with open(INPUT_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:

        lat = float(row["lat"])
        country = row["constituentCountry"].lower()

        if country == "scotland":
            region = "Scotland"

        elif country == "wales":
            region = "Wales"

        elif lat < 51.5:
            region = "South East"

        elif lat < 52.5:
            region = "Midlands"

        else:
            region = "North"

        row["region"] = region
        rows.append(row)

fieldnames = list(rows[0].keys())

with open(INPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(rows)

print(f"Updated {len(rows)} stations")