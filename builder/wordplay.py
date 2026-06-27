import json
from pathlib import Path


def load_dictionary():

    with open(
        Path("builder/wordplay_dictionary.json"),
        encoding="utf-8"
    ) as f:

        return json.load(f)


def analyse_station(name, dictionary):

    tags = []

    lower = name.lower()

    for category, words in dictionary.items():

        for word in words:

            if word.lower() in lower:

                tags.append(
                    f"{category}:{word.lower()}"
                )

    return sorted(set(tags))