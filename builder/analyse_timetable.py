from pathlib import Path
import csv
import gzip
import xml.etree.ElementTree as ET
from collections import Counter


def load_toc_dictionary():
    """
    Load the TOC lookup dictionary.
    """

    toc_lookup = {}

    dictionary = Path("builder/dictionaries/toc_codes.csv")

    with open(dictionary, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            toc_lookup[row["toc"]] = row

    return toc_lookup


def analyse_timetable(filename):

    print(f"Opening {filename}")

    with gzip.open(filename, "rb") as f:
        tree = ET.parse(f)

    root = tree.getroot()

    print("Loaded XML successfully.")
    print(f"Root tag: {root.tag}")

    toc_lookup = load_toc_dictionary()

    namespace = {
        "tt": "http://www.thalesgroup.com/rtti/XmlTimetable/v4/rttiCTTSchema.xsd"
    }

    journeys = root.findall(".//tt:Journey", namespace)

    print(f"\nJourneys found: {len(journeys):,}")

    toc_counter = Counter()

    for journey in journeys:
        toc = journey.get("toc")
        if toc:
            toc_counter[toc] += 1

    print("\nOperators")
    print("---------")

    for toc, count in toc_counter.most_common():

        if toc in toc_lookup:
            operator = toc_lookup[toc].get("operator", "UNKNOWN")
            confidence = toc_lookup[toc].get("confidence") or ""
        else:
            operator = "UNKNOWN"
            confidence = "Missing"

        print(
            f"{toc:3} "
            f"{count:6,}  "
            f"{operator:35} "
            f"{confidence}"
        )

    print("\nFirst Journey")
    print("-------------")

    first = journeys[0]

    print(f"RID   : {first.get('rid')}")
    print(f"TOC   : {first.get('toc')}")
    print(f"Train : {first.get('trainId')}")
    print(f"UID   : {first.get('uid')}")
    print(f"SSD   : {first.get('ssd')}")

    print("\nJourney elements")
    print("----------------")

    for child in first:

        tag = child.tag.split("}")[-1]

        print(f"\n{tag}")

        for key, value in child.attrib.items():
            print(f"   {key} = {value}")


if __name__ == "__main__":

    filename = input("Timetable file: ").strip()

    analyse_timetable(filename)