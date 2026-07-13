import requests
import json
from pathlib import Path
API_KEY = "cOdN62d18qcDlyAG3zxhtCEXO6kThnbAPtyxwOm695yvMe0O"
headers = {
    "x-apikey": API_KEY,
    "User-Agent": "RDG"
}
URL = "https://api1.raildata.org.uk/1010-nationalrail-knowledgebase-stations-feed-_json_---production5_0/stations/tocs/NT"

response = requests.get(URL, headers=headers)

print(response.status_code)

if response.status_code == 200:

    Path("data/Knowledgebase").mkdir(parents=True, exist_ok=True)

    with open(
        "data/Knowledgebase/TFW_network_data.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(response.json(), f, indent=4)

    print("Download complete.")

else:

    print(response.text)
    