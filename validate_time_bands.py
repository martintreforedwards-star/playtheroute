import json

FILE_PATH = "data/stations/southeastern.json"

with open(FILE_PATH, "r", encoding="utf-8") as file:
    stations = json.load(file)

def expected_band(minutes):

    if minutes <= 29:
        return "inner"

    elif minutes <= 69:
        return "commuter"

    elif minutes <= 90:
        return "outer"

    else:
        return "coastal"

print("\nTIME BAND VALIDATION\n")

issues_found = 0

for station in stations:

    name = station.get("station_name", "Unknown")

    minutes = station.get(
        "canonical_time_to_london",
        0
    )

    current_band = station.get(
        "time_group",
        ""
    )

    expected = expected_band(minutes)

    expected_label = ""

    if expected == "inner":
        expected_label = "0 to 29"

    elif expected == "commuter":
        expected_label = "30 to 69"

    elif expected == "outer":
        expected_label = "70 to 90"

    else:
        expected_label = "90 plus"

    if current_band != expected_label:

        issues_found += 1

        print(
            f"{name} "
            f"({minutes} mins) "
            f"stored='{current_band}' "
            f"expected='{expected_label}'"
        )

print(
    f"\nValidation complete. "
    f"{issues_found} issue(s) found."
)
