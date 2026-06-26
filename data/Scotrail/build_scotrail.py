from pathlib import Path
import pandas as pd

# =====================================================
# PATHS
# =====================================================

BASE = Path(__file__).parent

MASTER_FILE = BASE / "scotrail_master_v1.csv"
MEMBERSHIP_FILE = BASE / "route_group_membership.csv"
MISSING_TIMES_FILE = BASE / "missing_times.csv"
OUTPUT_FILE = BASE / "scotrail_v1_enriched.csv"

# =====================================================
# LOAD DATA
# =====================================================

stations = pd.read_csv(MASTER_FILE)
memberships = pd.read_csv(MEMBERSHIP_FILE)

# =====================================================
# OPTIONAL JOURNEY TIMES
# =====================================================

if MISSING_TIMES_FILE.exists():

    missing_times = pd.read_csv(MISSING_TIMES_FILE)

    time_lookup = dict(
        zip(
            missing_times["station_name"],
            missing_times["time_from_london"]
        )
    )

    if "time_from_london" in stations.columns:

        stations["time_from_london"] = stations.apply(
            lambda row: time_lookup.get(
                row["station_name"],
                row["time_from_london"]
            ),
            axis=1
        )

else:

    print("missing_times.csv not found - skipping journey time enrichment.")

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
    .apply(lambda x: x[0] if len(x) > 0 else "")
)

# =====================================================
# BRANCH / MAINLINE
# =====================================================

branch_groups = {
    "Oban Branch",
    "Kyle Line",
    "Far North Line",
    "Largs Branch",
    "Ardrossan Branch",
    "Neilston Line",
    "Lanark Line",
    "Borders Railway"
}

stations["is_branch_line"] = (
    stations["route_groups"]
    .apply(lambda groups: any(g in branch_groups for g in groups))
)

stations["is_mainline"] = ~stations["is_branch_line"]

# =====================================================
# COASTAL
# =====================================================

coastal_groups = {
    "Ayrshire Coast",
    "Inverclyde Line",
    "Largs Branch",
    "Ardrossan Branch",
    "West Highland Line",
    "Kyle Line",
    "Far North Line"
}

stations["is_coastal"] = (
    stations["route_groups"]
    .apply(lambda groups: any(g in coastal_groups for g in groups))
)

# =====================================================
# WORD COUNT
# =====================================================

stations["word_count_band"] = (
    stations["station_name"]
    .apply(lambda x: "multiple" if len(str(x).split()) > 1 else "single")
)

# =====================================================
# FLAGS
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

stations["route_station_id"] = stations["station_id"]

# =====================================================
# COMPATIBILITY FIELDS
# =====================================================

if "time_from_london" not in stations.columns:
    stations["time_from_london"] = ""

stations["canonical_time_to_london"] = stations["time_from_london"]

if "time_band" not in stations.columns:
    stations["time_band"] = ""

stations["time_group"] = stations["time_band"]

stations["is_high_speed"] = False

# =====================================================
# DISTANCE BAND
# =====================================================

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


stations["distance_band"] = (
    stations["time_from_london"]
    .apply(distance_band)
)

# =====================================================
# EXPORT
# =====================================================

stations.to_csv(
    OUTPUT_FILE,
    index=False
)

print()
print("DONE")
print()
print(f"Saved: {OUTPUT_FILE}")
print(f"Stations: {len(stations)}")