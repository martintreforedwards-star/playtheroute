import pandas as pd

# Load files
master = pd.read_csv(
    "/workspaces/playtheroute/data/Masters/master_station.csv"
)

membership = pd.read_csv(
    "/workspaces/playtheroute/data/Masters/network_membership.csv"
)

merge_map = pd.read_csv(
    "/workspaces/playtheroute/data/audit/station_id_merge_map.csv"
)

# Update network_membership station_ids
mapping = dict(
    zip(
        merge_map["old_station_id"],
        merge_map["new_station_id"]
    )
)

membership["station_id"] = membership["station_id"].replace(mapping)

# Remove duplicate stations from master
remove_ids = set(merge_map["old_station_id"])

master_clean = master[
    ~master["station_id"].isin(remove_ids)
]

# Save outputs (don't overwrite originals yet)
master_clean.to_csv(
    "/workspaces/playtheroute/data/Masters/master_station_deduped.csv",
    index=False
)

membership.to_csv(
    "/workspaces/playtheroute/data/Masters/network_membership_deduped.csv",
    index=False
)

print("=== DEDUPLICATION COMPLETE ===")
print("Master stations:", len(master_clean))
print("Membership rows:", len(membership))
print("Removed stations:", len(remove_ids))