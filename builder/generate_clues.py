import json
from pathlib import Path


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def unique_values(stations, field):
    values = sorted(
        {
            s.get(field)
            for s in stations
            if s.get(field) not in ("", None, False)
        }
    )
    return values


def generate_rows():

    return [

        {
            "display": "Terminus",
            "type": "field",
            "field": "is_terminus",
            "value": True,
            "weight": "medium"
        },

        {
            "display": "Not a Terminus",
            "type": "field",
            "field": "is_terminus",
            "value": False,
            "weight": "high"
        },

        {
            "display": "Interchange",
            "type": "field",
            "field": "is_interchange",
            "value": True,
            "weight": "medium"
        },

        {
            "display": "Branch Line",
            "type": "field",
            "field": "is_branch_line",
            "value": True,
            "weight": "medium"
        },

        {
            "display": "Main Line",
            "type": "field",
            "field": "is_mainline",
            "value": True,
            "weight": "medium"
        }

    ]


def generate_columns(stations):

    columns = []

    def add_field(field, category="general", title=str.title):

        if field not in stations[0]:
            return

        values = sorted(
            {
                s.get(field)
                for s in stations
                if s.get(field) not in ("", None, False)
            }
        )

        for value in values:

            columns.append(
                {
                    "display": title(str(value)),
                    "type": "field",
                    "field": field,
                    "value": value,
                    "weight": "medium",
                    "category": category,
                }
            )

    add_field("region", "geography")
    add_field("distance_band", "geography")
    add_field("time_group", "service")
    add_field("word_count_band", "name")
    add_field("service_density", "service")
    add_field("route_diversity_band", "service")

    route_groups = sorted(
        {
            group
            for station in stations
            for group in station.get("route_groups", [])
        }
    )

    for group in route_groups:

        columns.append(
            {
                "display": group,
                "type": "array_contains",
                "field": "route_groups",
                "value": group,
                "weight": "medium",
                "category": "route",
            }
        )

    return columns


def generate_wordplay_columns(wordplay):

    columns = []

    if not wordplay:
        return columns

    sample = wordplay[0]

    auto_prefixes = (
        "contains_",
        "starts_with_",
        "ends_with_",
        "first_word_",
        "last_word_",
        "prefix_",
        "suffix_",
    )

    for field in sorted(sample.keys()):

        prefix = next(
            (p for p in auto_prefixes if field.startswith(p)),
            None,
        )

        if prefix is None:
            continue

        display = (
            field[len(prefix):]
            .replace("_", " ")
            .title()
        )

        if prefix == "contains_":
            display = f"Contains {display}"
        elif prefix == "starts_with_":
            display = f"Starts With {display}"
        elif prefix == "ends_with_":
            display = f"Ends With {display}"
        elif prefix == "first_word_":
            display = f"First Word {display}"
        elif prefix == "last_word_":
            display = f"Last Word {display}"
        elif prefix == "prefix_":
            display = f"Prefix {display}"
        elif prefix == "suffix_":
            display = f"Suffix {display}"

        columns.append(
            {
                "display": display,
                "type": "field",
                "field": field,
                "value": True,
                "weight": "medium",
                "category": "name",
            }
        )

    return columns


def generate(config):

    network = config["network"]
    network_dir = Path(config["data_root"])

    stations = load_json(Path(config["output"]))

    analysis_folder = network_dir / "analysis"
    wordplay_file = analysis_folder / f"{network.lower()}_wordplay.json"

    if wordplay_file.exists():
        wordplay = load_json(wordplay_file)
    else:
        wordplay = []

    clue_file = {
        "rowPool": generate_rows(),
        "columnPool": (
            generate_columns(stations)
            + generate_wordplay_columns(wordplay)
        ),
    }

    output = Path(config["clues"])

    save_json(output, clue_file)

    print(f"Created {output}")


if __name__ == "__main__":

    import sys
    from builder.config import load_config

    if len(sys.argv) != 2:
        print("Usage:")
        print("python builder/generate_clues.py <network>")
        sys.exit(1)

    generate(load_config(sys.argv[1]))