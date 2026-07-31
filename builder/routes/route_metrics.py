from pathlib import Path

import pandas as pd


MASTER = Path("data/Masters")


def station_name(crs, lookup):
    """Return a station name if known, otherwise the original code."""
    return lookup.get(crs, crs)


def common_corridor(details):
    """Return the common corridor shared by every pattern."""

    station_lists = [
        row["stations"].split("|")
        for _, row in details.iterrows()
    ]

    if not station_lists:
        return []

    shortest = min(station_lists, key=len)

    common = []

    for i, station in enumerate(shortest):

        if all(
            len(s) > i and s[i] == station
            for s in station_lists
        ):
            common.append(station)
        else:
            break

    return common


def unique_station_count(details):
    """Return the number of unique stations across all patterns."""

    stations = set()

    for _, row in details.iterrows():
        stations.update(row["stations"].split("|"))

    return len(stations)


def pattern_statistics(details):
    """Return longest pattern statistics."""

    longest = details.loc[
        details["station_count"].idxmax()
    ]

    return (
        longest["pattern_id"],
        int(longest["station_count"]),
        round(details["station_count"].mean(), 1),
    )


def main():

    routes = pd.read_csv(MASTER / "pattern_routes.csv")
    patterns = pd.read_csv(MASTER / "service_patterns.csv")
    tree = pd.read_csv(MASTER / "route_tree.csv")
    stations = pd.read_csv(MASTER / "stations.csv")

    station_lookup = (
        stations
        .dropna(subset=["crs", "station_name"])
        .drop_duplicates(subset=["crs"])
        .set_index("crs")["station_name"]
        .to_dict()
    )

    output = []

    for route_id in sorted(routes["route_id"].unique()):

        members = routes[
            routes["route_id"] == route_id
        ]

        pattern_ids = set(
            members["pattern_id"]
        )

        details = patterns[
            patterns["pattern_id"].isin(pattern_ids)
        ].copy()

        if details.empty:
            continue

        details = details.sort_values(
            "service_count",
            ascending=False,
        )

        busiest = details.iloc[0]

        operational_destination = station_name(
            busiest["destination"],
            station_lookup,
        )

        public_patterns = details[
            details["destination"].isin(
                station_lookup.keys()
            )
        ]

        if public_patterns.empty:

            primary_destination = operational_destination
            is_public_route = False

        else:

            public_patterns = public_patterns.sort_values(
                "service_count",
                ascending=False,
            )

            primary_destination = station_name(
                public_patterns.iloc[0]["destination"],
                station_lookup,
            )

            is_public_route = True

        corridor = common_corridor(details)

        unique_count = unique_station_count(details)

        (
            longest_pattern,
            longest_pattern_length,
            average_pattern_length,
        ) = pattern_statistics(details)

        output.append(
            {
                "route_id": route_id,

                "origin": station_name(
                    busiest["origin"],
                    station_lookup,
                ),

                "operational_destination": operational_destination,

                "primary_destination": primary_destination,

                "is_public_route": is_public_route,

                "pattern_count": len(details),

                "service_count": int(
                    details["service_count"].sum()
                ),

                "unique_station_count": unique_count,

                "branch_count": len(
                    tree[
                        tree["route_id"] == route_id
                    ]
                ),

                "corridor_length": len(corridor),

                "corridor_end": (
                    station_name(
                        corridor[-1],
                        station_lookup,
                    )
                    if corridor
                    else ""
                ),

                "longest_pattern": longest_pattern,

                "longest_pattern_length": longest_pattern_length,

                "average_pattern_length": average_pattern_length,
            }
        )

    routes_df = pd.DataFrame(output)

    routes_df = routes_df.sort_values("route_id")

    outfile = MASTER / "routes.csv"

    routes_df.to_csv(outfile, index=False)

    print(f"Saved {outfile}")
    print(f"Routes : {len(routes_df)}")


if __name__ == "__main__":
    main()