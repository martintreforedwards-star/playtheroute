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

    master_file = Path(config["master"])
    membership_file = Path(config["route_groups"])
    missing_times_file = Path(config["missing_times"])
    output_file = Path(config["enriched"])

    stations = pd.read_csv(master_file)
    memberships = pd.read_csv(membership_file)

    rules = load_rules(config)

    print(f"Stations loaded : {len(stations)}")

    # --------------------------------------------
    # Optional journey time enrichment
    # --------------------------------------------

    if missing_times_file.exists():

        missing = pd.read_csv(missing_times_file)

        lookup = dict(
            zip(
                missing["station_name"],
                missing["time_from_london"]
            )
        )

        if "time_from_london" in stations.columns:

            stations["time_from_london"] = stations.apply(
                lambda row: lookup.get(
                    row["station_name"],
                    row["time_from_london"]
                ),
                axis=1
            )

    # --------------------------------------------
    # Route Groups
    # --------------------------------------------

    route_lookup = (
        memberships
        .groupby("station_name")["route_group"]
        .apply(list)
        .to_dict()
    )

    stations["route_groups"] = (
        stations["station_name"]
        .map(route_lookup)
        .apply(lambda x: x if isinstance(x, list) else [])
    )

    stations["region"] = (
        stations["route_groups"]
        .apply(lambda x: x[0] if len(x) else "")
    )
    # --------------------------------------------
    # Station flags
    # --------------------------------------------

    stations["is_interchange"] = (
    stations["major_interchange"]
    .astype(str)
    .str.lower()
    .eq("true")
    )

    stations["is_terminus"] = (
    stations["terminus"]
    .astype(str)
    .str.lower()
    .eq("true")
)
    # --------------------------------------------
    # Generic fields
    # --------------------------------------------

    stations["word_count_band"] = (
        stations["station_name"]
        .apply(
            lambda x:
            "multiple"
            if len(str(x).split()) > 1
            else "single"
        )
    )

    # --------------------------------------------
    # Rules
    # --------------------------------------------

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

    # --------------------------------------------
    # Compatibility fields
    # --------------------------------------------

    stations["route_station_id"] = stations["station_id"]

    if "time_from_london" not in stations.columns:
        stations["time_from_london"] = ""

    stations["canonical_time_to_london"] = stations["time_from_london"]

    if "time_band" not in stations.columns:
        stations["time_band"] = ""

    stations["time_group"] = stations["time_band"]

    stations["is_high_speed"] = False

    stations["distance_band"] = (
        stations["time_from_london"]
        .apply(distance_band)
    )

    # --------------------------------------------
    # Export
    # --------------------------------------------

    stations.to_csv(output_file, index=False)

    print(f"Saved : {output_file}")

    return stations