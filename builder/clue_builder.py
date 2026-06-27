import json
from pathlib import Path

from builder.rules import load_rules


def build_clues(config):

    template = Path(config["clue_template"])
    output = Path(config["clues"])

    rules = load_rules(config)
    clue_rules = rules.get("clues", {})

    with open(template, encoding="utf-8") as f:
        clues = json.load(f)

    remove = set(clue_rules.get("remove", []))

    def process(pool):

        result = []

        for clue in pool:

            if clue.get("display") in remove:
                continue

            result.append(clue.copy())

        return result

    clues["rowPool"] = process(clues["rowPool"])
    clues["columnPool"] = process(clues["columnPool"])

    with open(output, "w", encoding="utf-8") as f:
        json.dump(clues, f, indent=2)

    print(f"Clues saved : {output}")