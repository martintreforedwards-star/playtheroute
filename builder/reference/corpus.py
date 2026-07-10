import gzip
import json
from pathlib import Path

CORPUS_FILE = Path("data/CORPUS/CORPUSExtract.json.gz")


def load_tiploc_lookup():
    """
    Load the Network Rail CORPUS reference data and return a
    dictionary keyed by TIPLOC.

    Returns
    -------
    dict

    Example
    -------
    {
        "WKIRBY": {
            "crs": "WKI",
            "name": "WEST KIRBY"
        },
        ...
    }
    """

    with gzip.open(CORPUS_FILE, "rt", encoding="utf-8") as f:
        corpus = json.load(f)

    lookup = {}

    for record in corpus["TIPLOCDATA"]:

        tiploc = record.get("TIPLOC")

        if not tiploc:
            continue

        lookup[tiploc] = {
            "crs": record.get("3ALPHA", "").strip(),
            "name": record.get("NLCDESC", "").strip(),
            "nlc": record.get("NLC"),
            "stanox": record.get("STANOX"),
        }

    return lookup


if __name__ == "__main__":

    lookup = load_tiploc_lookup()

    print(f"Lookup entries : {len(lookup):,}")
    print()

    sample = "FENTON"

    print(f"Sample ({sample})")
    print(lookup.get(sample))