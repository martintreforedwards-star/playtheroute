from collections import Counter
from pathlib import Path
from builder.dictionaries import load_dictionaries
import pandas as pd
import re


def analyse(source_file):

    stations = pd.read_csv(source_file)

    reports = Path("builder/reports")
    reports.mkdir(exist_ok=True)

    # Load all theme dictionaries
    THEMES = load_dictionaries()

    first_words = Counter()
    last_words = Counter()
    single_words = []
    all_words = Counter()
    word_index = []

    # ---------------------------------
    # Analyse station names
    # ---------------------------------

    for name in stations["stationName"]:

        # Remove bracketed qualifiers
        name = re.sub(r"\([^)]*\)", "", str(name)).strip()

        words = name.split()

        if not words:
            continue

        # First / Last words
        first_words[words[0]] += 1
        last_words[words[-1]] += 1

        # Single-word stations
        if len(words) == 1:
            single_words.append(name)

        # Every word
        for word in words:

            all_words[word] += 1

        word_index.append(
        {
            "word": word,
            "station": name
        }
    )

    # ---------------------------------
    # Theme candidates
    # ---------------------------------

    theme_rows = []

    for word, count in all_words.items():

        for theme, vocabulary in THEMES.items():

            if word in vocabulary:

                theme_rows.append(
                    {
                        "theme": theme,
                        "word": word,
                        "count": count
                    }
                )

    # ---------------------------------
    # Reports
    # ---------------------------------

    pd.DataFrame(
        first_words.items(),
        columns=["word", "count"]
    ).sort_values(
        "count",
        ascending=False
    ).to_csv(
        reports / "first_words.csv",
        index=False
    )

    pd.DataFrame(
        last_words.items(),
        columns=["word", "count"]
    ).sort_values(
        "count",
        ascending=False
    ).to_csv(
        reports / "last_words.csv",
        index=False
    )

    pd.DataFrame(
        {"station": sorted(single_words)}
    ).to_csv(
        reports / "single_word_stations.csv",
        index=False
    )

    pd.DataFrame(
        all_words.items(),
        columns=["word", "count"]
    ).sort_values(
        "count",
        ascending=False
    ).to_csv(
        reports / "word_frequency.csv",
        index=False
    )
    pd.DataFrame(
    word_index
    ).sort_values(
    ["word", "station"]
    ).to_csv(
    reports / "word_index.csv",
    index=False
    )
    pd.DataFrame(
        theme_rows
    ).sort_values(
        ["theme", "count"],
        ascending=[True, False]
    ).to_csv(
        reports / "theme_candidates.csv",
        index=False
    )

    # ---------------------------------
    # Summary
    # ---------------------------------

    print()
    print(f"Stations analysed      : {len(stations)}")
    print(f"Unique first words     : {len(first_words)}")
    print(f"Unique last words      : {len(last_words)}")
    print(f"Single-word stations   : {len(single_words)}")
    print(f"Unique words           : {len(all_words)}")
    print(f"Theme candidates       : {len(theme_rows)}")
    print()
    print(f"Reports written to {reports}")

    return stations