from pathlib import Path
import csv


OUTPUT = Path("data/Masters/services.csv")


def save_services(services):
    """
    Save raw passenger services extracted from Darwin.

    One row = one passenger service.
    """

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "service_id",
                "toc",
                "origin",
                "destination",
                "station_count",
                "stations",
            ]
        )

        for i, service in enumerate(services, start=1):

            stations = service["stations"]

            writer.writerow(
                [
                    f"SV{i:06d}",
                    service["toc"],
                    stations[0],
                    stations[-1],
                    len(stations),
                    "|".join(stations),
                ]
            )

    print(f"Saved : {OUTPUT}")