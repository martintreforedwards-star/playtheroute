from pathlib import Path

from builder.network_source import load_network
from builder.save_master import save_master


def build_master(config):
    """
    Build the master CSV if it does not already exist.
    """

    if "master" in config:
        master_file = config["master"]
    else:
        network = config.get("network", "").strip()
        if not network:
            raise KeyError("Config must contain either 'master' or 'network'.")
        master_file = str(Path("data") / network / f"{network.lower()}_master.csv")

    master_path = Path(master_file)

    if master_path.exists():
        return master_file

    print("Creating master dataset...")

    df = load_network(config["network"].lower())
    save_master(df, master_file)

    print(f"Saved: {master_file}")

    return master_file