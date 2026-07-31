from pathlib import Path

import pandas as pd


MASTER = Path("data/Masters")


def classify(row):
    """
    Classify a route.
    """

    if not row["is_public_route"]:
        return "Operational"

    if row["origin"] == row["primary_destination"]:
        return "Circular"

    if (
        row["pattern_count"] == 1
        and row["unique_station_count"] <= 5
    ):
        return "Shuttle"

    if (
        row["pattern_count"] <= 3
        and row["branch_count"] <= 2
        and row["unique_station_count"] < 20
    ):
        return "Branch"

    if (
        row["average_pattern_length"] < 12
        and row["service_count"] > 100
    ):
        return "Metro"

    return "Main Line"


def complexity(row):
    """
    Calculate a simple complexity score.
    """

    score = (
        row["pattern_count"]
        + row["branch_count"]
        + (row["unique_station_count"] / 10)
    )

    if score < 6:
        return "Simple"

    if score < 16:
        return "Moderate"

    return "Complex"


def main():

    infile = MASTER / "routes.csv"

    routes = pd.read_csv(infile)

    routes["route_type"] = routes.apply(
        classify,
        axis=1,
    )

    routes["complexity"] = routes.apply(
        complexity,
        axis=1,
    )

    routes["is_branch"] = (
        routes["route_type"] == "Branch"
    )

    routes["is_circular"] = (
        routes["route_type"] == "Circular"
    )

    routes["is_operational"] = (
        routes["route_type"] == "Operational"
    )

    outfile = MASTER / "routes_classified.csv"

    routes.to_csv(outfile, index=False)

    print(f"Saved {outfile}")
    print(f"Routes classified : {len(routes)}")

    print()
    print("Route Types")
    print("-----------")
    print(routes["route_type"].value_counts())

    print()
    print("Complexity")
    print("----------")
    print(routes["complexity"].value_counts())


if __name__ == "__main__":
    main()