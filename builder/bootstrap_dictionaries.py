from pathlib import Path

DICTIONARIES = {

    "transport": [
        "Road",
        "Street",
        "Bridge",
        "Junction",
        "Parkway",
        "Central",
        "Cross",
        "Lane",
        "Airport",
        "Harbour",
        "International"
    ],

    "nature": [
        "Hill",
        "Wood",
        "Green",
        "Heath",
        "Bank",
        "Field",
        "Vale",
        "Moor",
        "Marsh"
    ],

    "water": [
        "Bay",
        "River",
        "Sea",
        "Quay",
        "Dock"
    ],

    "direction": [
        "North",
        "South",
        "East",
        "West",
        "Upper",
        "Lower"
    ],

    "number": [
        "One",
        "Two",
        "Three",
        "Four",
        "Five",
        "Seven"
    ]

}


def bootstrap():

    folder = Path("builder/dictionaries")
    folder.mkdir(parents=True, exist_ok=True)

    for name, words in DICTIONARIES.items():

        file = folder / f"{name}.csv"

        if file.exists():
            continue

        with open(file, "w", encoding="utf-8") as f:

            for word in words:
                f.write(word + "\n")

        print(f"Created {file}")


if __name__ == "__main__":
    bootstrap()