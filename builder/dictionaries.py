from pathlib import Path


def load_dictionaries():

    dictionaries = {}

    folder = Path("builder/dictionaries")

    for file in folder.glob("*.csv"):

        words = set()

        with open(file, encoding="utf-8") as f:

            for line in f:

                word = line.strip()

                if word:

                    words.add(word)

        dictionaries[file.stem] = words

    return dictionaries