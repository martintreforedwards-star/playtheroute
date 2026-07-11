import csv


def profile_patterns(patterns):

    pattern_lookup = {
        tuple(pattern["stations"]): pattern["pattern_id"]
        for pattern in patterns
    }

    profiles = []

    for pattern in patterns:

        stations = pattern["stations"]

        reverse = list(reversed(stations))

        reverse_id = pattern_lookup.get(tuple(reverse))

        profiles.append({

            "pattern_id": pattern["pattern_id"],

            "origin": stations[0],

            "destination": stations[-1],

            "station_count": len(stations),

            "service_count": pattern["service_count"],

            "is_circular": stations[0] == stations[-1],

            "is_shuttle": len(stations) == 2,

            "has_reverse": reverse_id is not None,

            "reverse_pattern_id": reverse_id or "",

        })

    return profiles


def save_profiles(profiles):

    filename = "data/Masters/service_pattern_profiles.csv"

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=profiles[0].keys(),
        )

        writer.writeheader()

        writer.writerows(profiles)

    print(f"Saved: {filename}")