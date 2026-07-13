import sys
import json
from pathlib import Path

import requests

API_KEY = "cOdN62d18qcDlyAG3zxhtCEXO6kThnbAPtyxwOm695yvMe0O"

BASE_URL = (
    "https://api1.raildata.org.uk/"
    "1010-nationalrail-knowledgebase-stations-feed-_json_---production5_0/"
    "stations/tocs/"
)


def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("python builder/download_network.py <TOC>")
        return

    toc = sys.argv[1].upper()

    headers = {
        "x-apikey": API_KEY,
        "User-Agent": "RDG",
    }

    url = BASE_URL + toc

    print(f"Downloading {toc}...")

    response = requests.get(url, headers=headers)

    print(response.status_code)

    if response.status_code != 200:
        print(response.text)
        return

    output_dir = Path("data/Knowledgebase")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{toc}_network_data.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(response.json(), f, indent=4)

    print(f"Saved : {output_file}")


if __name__ == "__main__":
    main()