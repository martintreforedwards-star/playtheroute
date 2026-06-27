import json
from pathlib import Path


def load_rules(config):

    rules_file = Path(config["rules"])

    if not rules_file.exists():
        return {}

    with open(rules_file, encoding="utf-8") as f:
        return json.load(f)