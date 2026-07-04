from pathlib import Path

import pandas as pd

from builder.rules import load_rules


def distance_band(value):
    try:
        value = float(value)
    except Exception:
        return ""

    if value <= 20:
        return "inner"
    if value <= 40:
        return "outer"
    if value <= 60:
        return "commuter"

    return "regional"


def enrich(config):

    network = config["network"]

    station_col = config.get("station_column", "station_name")
    route_col = config.get("route_group_column", "route_group")
    time_col = config.get("time_column", "time_from_london")
    interchange_col = config.get("interchange_column", "major_interchange")
    terminus_col = config.get("terminus_column", "terminus")
    id_col = config.get("id_column", "station_id")

    master_file = Path(
        config.get(
            "master",
            Path("data") / network / f"{network.lower()}_master.csv"
        )
    )

    membership_file = Path(
        config.get(
            "route_groups",
            Path("data") / network / "route_membership.csv"
        )
    )

    missing_times_file = Path(
        config.get(
            "missing_times",
            Path("data") / network / "missing_times.csv"
        )
    )

    output_file = Path(
        config.get(
            "enriched",
            Path("data") / network / f"{network.lower()}_enriched.csv"
        )
    )

    stations = pd.read_csv(master_file)
    memberships = pd.read_csv(membership_file)

    rules = load_rules(config)

    print(f"Stations loaded : {len(stations)}")

    if missing_times_file.exists():

        missing = pd.read_csv(missing_times_file)

        if station_col in missing.columns and time_col in missing.columns:

            lookup = dict(zip(missing[station_col], missing[time_col]))

            if time_col in stations.columns:
                stations[time_col] = stations.apply(
                    lambda row: lookup.get(
                        row[station_col],
                        row[time_col]
                    ),
                    axis=1
                )

    route_lookup = (
        memberships
        .groupby(station_col)[route_col]
        .apply(list)
        .to_dict()
    )

    stations["route_groups"] = (
        stations[station_col]
        .map(route_lookup)
        .apply(lambda x: x if isinstance(x, list) else [])
    )

    stations["region"] = (
        stations["route_groups"]
        .apply(lambda x: x[0] if len(x) else "")
    )

    if interchange_col in stations.columns:
        stations["is_interchange"] = (
            stations[interchange_col]
            .astype(str)
            .str.lower()
            .eq("true")
        )
    elif "is_interchange" not in stations.columns:
        stations["is_interchange"] = False

    if terminus_col in stations.columns:
        stations["is_terminus"] = (
            stations[terminus_col]
            .astype(str)
            .str.lower()
            .eq("true")
        )
    elif "is_terminus" not in stations.columns:
        stations["is_terminus"] = False

    stations["word_count_band"] = (
        stations[station_col]
        .apply(lambda x: "multiple" if len(str(x).split()) > 1 else "single")
    )

    branch_groups = set(rules.get("branch_groups", []))
    coastal_groups = set(rules.get("coastal_groups", []))

    stations["is_branch_line"] = (
        stations["route_groups"]
        .apply(lambda groups: any(g in branch_groups for g in groups))
    )

    stations["is_mainline"] = ~stations["is_branch_line"]

    stations["is_coastal"] = (
        stations["route_groups"]
        .apply(lambda groups: any(g in coastal_groups for g in groups))
    )

    if id_col in stations.columns:
        stations["route_station_id"] = stations[id_col]
    elif "crs" in stations.columns:
        stations["route_station_id"] = stations["crs"]
    elif "crs_code" in stations.columns:
        stations["route_station_id"] = stations["crs_code"]
    else:
        stations["route_station_id"] = stations.index.astype(str)

    if time_col not in stations.columns:
        stations[time_col] = ""

    stations["canonical_time_to_london"] = stations[time_col]

    if "time_band" not in stations.columns:
        stations["time_band"] = ""

    stations["time_group"] = stations["time_band"]

    stations["is_high_speed"] = False

    stations["distance_band"] = (
        stations[time_col]
        .apply(distance_band)
    )

    stations.to_csv(output_file, index=False)

    print(f"Saved : {output_file}")

    return stations