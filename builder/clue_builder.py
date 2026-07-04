import json
from pathlib import Path

from builder.rules import load_rules


def build_clues(config):

    network = config["network"]

    template = Path(
        config.get(
            "clue_template",
            Path("data") / "clues" / "template.json"
        )
    )

    output = Path(
        config.get(
            "clues",
            Path("data") / network / f"{network.lower()}-clues.json"
        )
    )

    if not template.exists():
        raise FileNotFoundError(
            f"Clue template not found: {template}\n"
            "Add 'clue_template' to the network config or create the default template."
        )

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

    clues["rowPool"] = process(clues.get("rowPool", []))
    clues["columnPool"] = process(clues.get("columnPool", []))

    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(clues, f, indent=2)

    print(f"Clues saved : {output}")