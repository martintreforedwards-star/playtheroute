from pathlib import Path
import pandas as pd

print("Starting audit...")

# -----------------------------------------------------
# Paths
# -----------------------------------------------------

BASE = Path(__file__).parent

MASTER_FILE = BASE / "scotrail_master_v1.csv"
MEMBERSHIP_FILE = BASE / "route_group_membership.csv"

# -----------------------------------------------------
# Load data
# -----------------------------------------------------

master = pd.read_csv(MASTER_FILE)
members = pd.read_csv(MEMBERSHIP_FILE)

print("Loaded files")
print()

print("Master columns:")
print(master.columns.tolist())
print()

print("Membership columns:")
print(members.columns.tolist())
print()

# -----------------------------------------------------
# Find station name columns
# -----------------------------------------------------

master_col = next(
    c for c in master.columns
    if c.lower() == "station_name"
)

member_col = next(
    c for c in members.columns
    if c.lower() == "station_name"
)

# -----------------------------------------------------
# Compare
# -----------------------------------------------------

master_names = set(
    master[master_col]
    .dropna()
    .astype(str)
    .str.strip()
)

member_names = set(
    members[member_col]
    .dropna()
    .astype(str)
    .str.strip()
)

missing = sorted(master_names - member_names)
extra = sorted(member_names - master_names)

# -----------------------------------------------------
# Report
# -----------------------------------------------------

print("===================================")
print(" ScotRail Route Coverage Audit")
print("===================================")
print()

print(f"Stations in master : {len(master_names)}")
print(f"Stations assigned  : {len(member_names)}")
print(f"Stations missing   : {len(missing)}")
print(f"Unknown stations   : {len(extra)}")

print()

if missing:
    print("Missing stations:")
    print("-----------------")
    for station in missing:
        print(station)

print()

if extra:
    print("Stations not found in master:")
    print("-----------------------------")
    for station in extra:
        print(station)

print()
print("Audit complete.")