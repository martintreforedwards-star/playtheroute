from pathlib import Path
import pandas as pd


def detect(source_file):

    stations = pd.read_csv(source_file)

    reports = Path("builder/reports")
    reports.mkdir(exist_ok=True)

    # Load known words
    freq = pd.read_csv(reports / "word_frequency.csv")
    known_words = set(freq["word"])

    candidates = []

    for station in stations["stationName"]:

        station = str(station)

        # Ignore stations already containing spaces
        if " " in station:
            continue

        lower = station.lower()

        for word in known_words:

            if len(word) < 4:
                continue

            w = word.lower()

            if lower.endswith(w):

                prefix = station[:-len(word)]

                # Prefix must itself be a known station word
                if (
                    len(prefix) >= 3
                    and prefix in known_words
                ):

                    candidates.append(
                        {
                            "station": station,
                            "prefix": prefix,
                            "suffix": word
                        }
                    )

    pd.DataFrame(candidates) \
        .drop_duplicates() \
        .sort_values("station") \
        .to_csv(
            reports / "wordplay_candidates.csv",
            index=False
        )

    print(f"Compound candidates: {len(candidates)}")