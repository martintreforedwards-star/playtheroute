from pathlib import Path

def build_master(config):
    """
    Phase 1

    The master dataset already exists.

    Phase 2 will generate this automatically from the
    CRS Source of Truth.

    If no master file is explicitly configured,
    derive it from the network name.
    """

    if "master" in config:
        return config["master"]

    network = config.get("network", "").strip()
    if not network:
        raise KeyError("Config must contain either 'master' or 'network'.")

    return str(Path("data") / network / f"{network.lower()}_master.csv")