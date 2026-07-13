"""
Gameplay audit.
"""

from pathlib import Path

import pandas as pd


def audit_gameplay(network, report):

    report.section("Gameplay")

    root = Path.cwd()
    network_title = network.capitalize()

    enriched_csv = (
        root / "data" / network_title / f"{network}_enriched.csv"
    )

    if not enriched_csv.exists():
        report.fail("Enriched CSV missing")
        return

    df = pd.read_csv(enriched_csv)

    report.pass_check(f"Stations: {len(df)}")

    required = [
        "route_count",
        "service_count",
        "latitude",
        "longitude",
    ]

    for field in required:

        if field not in df.columns:
            report.fail(f"{field} missing")
            continue

        populated = df[field].notna().sum()

        report.metric(
            field,
            populated,
            len(df),
            100,
            "FAIL",
        )

    if "route_count" in df.columns:

        playable = (df["route_count"] > 0).sum()

        report.metric(
            "Playable stations",
            playable,
            len(df),
            100,
            "FAIL",
        )

    if "service_count" in df.columns:

        playable = (df["service_count"] > 0).sum()

        report.metric(
            "Stations with services",
            playable,
            len(df),
            100,
            "FAIL",
        )