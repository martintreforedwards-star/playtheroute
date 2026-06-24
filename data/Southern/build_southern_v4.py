import pandas as pd

# =====================================================
# LOAD DATA
# =====================================================

stations = pd.read_csv(
    "data/Southern/southern_master_v3_enriched.csv"
)

memberships = pd.read_csv(
    "data/Southern/route_group_membership.csv"
)

missing_times = pd.read_csv(
    "data/Southern/missing_times.csv"
)

# =====================================================
# APPLY MISSING TIMES
# =====================================================

time_lookup = dict(
    zip(
        missing_times["station_name"],
        missing_times["time_from_london"]
    )
)

stations["time_from_london"] = stations.apply(
    lambda row:
    time_lookup.get(
        row["station_name"],
        row["time_from_london"]
    ),
    axis=1
)

# =====================================================
# ROUTE GROUPS
# =====================================================

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
    .apply(
        lambda x: x[0] if len(x) > 0 else ""
    )
)

# =====================================================
# BRANCH / MAINLINE
# =====================================================

branch_groups = {
    "East Grinstead Branch",
    "Uckfield Branch"
}

stations["is_branch_line"] = (
    stations["route_groups"]
    .apply(
        lambda groups:
        any(g in branch_groups for g in groups)
    )
)

stations["is_mainline"] = (
    ~stations["is_branch_line"]
)

# =====================================================
# COASTAL
# =====================================================

coastal_groups = {
    "East Coastway",
    "West Coastway"
}

stations["is_coastal"] = (
    stations["route_groups"]
    .apply(
        lambda groups:
        any(g in coastal_groups for g in groups)
    )
)

# =====================================================
# WORD COUNT
# =====================================================

stations["word_count_band"] = (
    stations["station_name"]
    .apply(
        lambda x:
        "multiple"
        if len(str(x).split()) > 1
        else "single"
    )
)

# =====================================================
# INTERCHANGE / TERMINUS
# =====================================================

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

# =====================================================
# SOUTHEASTERN PARITY
# =====================================================

stations["route_station_id"] = stations["station_id"]

stations["canonical_time_to_london"] = (
    stations["time_from_london"]
)

stations["time_group"] = (
    stations["time_band"]
)

stations["is_high_speed"] = False

# =====================================================
# DISTANCE BAND
# =====================================================

def distance_band(value):

    try:
        value = float(value)
    except:
        return ""

    if value <= 20:
        return "inner"

    if value <= 40:
        return "outer"

    if value <= 60:
        return "commuter"

    return "regional"

stations["distance_band"] = (
    stations["time_from_london"]
    .apply(distance_band)
)

# =====================================================
# EXPORT
# =====================================================

OUTPUT_FILE = (
    "data/Southern/southern_v4_enriched.csv"
)

stations.to_csv(
    OUTPUT_FILE,
    index=False
)

print()
print("DONE")
print()
print(f"Saved {OUTPUT_FILE}")
print(f"Rows: {len(stations)}")