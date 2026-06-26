import json
from pathlib import Path


CONFIG_DIR = Path(__file__).parent / "configs"


def load_config(network_name: str) -> dict:
    """
    Load a network configuration from builder/configs/<network>.json
    """

    config_file = CONFIG_DIR / f"{network_name.lower()}.json"

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration not found: {config_file}")

    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)