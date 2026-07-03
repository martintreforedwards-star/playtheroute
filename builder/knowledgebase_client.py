import json
from pathlib import Path


def load_knowledgebase(path):

    with open(Path(path), encoding="utf-8") as f:
        return json.load(f)["stations"]