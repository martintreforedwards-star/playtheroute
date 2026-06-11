import pandas as pd

master = pd.read_csv(
    "/workspaces/playtheroute/data/Masters/master_station.csv"
)

print(master.columns.tolist())