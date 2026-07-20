import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

INPUT = "data/Class1/Southern/southern_aggregated_1.csv"
OUTPUT = "data/Reference/county_lookup.csv"

geolocator = Nominatim(user_agent="playtheroute")


def get_county(lat, lon):
    try:
        location = geolocator.reverse(
            (float(lat), float(lon)),
            exactly_one=True,
            language="en",
        )

        if location is None:
            return ""

        address = location.raw.get("address", {})

        return (
            address.get("county")
            or address.get("state_district")
            or address.get("state")
            or ""
        )

    except GeocoderTimedOut:
        return ""
    except Exception as e:
        print(e)
        return ""


def main():

    print("Loading...")

    df = pd.read_csv(INPUT)

    print(f"{len(df)} stations found")

    rows = []

    for _, row in df.iterrows():

        county = get_county(row["latitude"], row["longitude"])

        print(f'{row["crs"]} -> {county}')

        rows.append(
            {
                "crs": row["crs"],
                "county": county,
            }
        )

    pd.DataFrame(rows).to_csv(OUTPUT, index=False)

    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()