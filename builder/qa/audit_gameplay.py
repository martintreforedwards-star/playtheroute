"""
Gameplay audit.
"""

import pandas as pd

from builder.qa.paths import network_path


def audit_gameplay(network, report):

    report.section("Gameplay")

    network_dir = network_path(network)

    enriched_csv = (
        network_dir / f"{network}_enriched.csv"
    )

    if not enriched_csv.exists():
        report.fail("Enriched CSV missing")
        return

    try:
        df = pd.read_csv(enriched_csv)
    except Exception as ex:
        report.fail(f"Unable to read Enriched CSV ({ex})")
        return

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

        serviced = (df["service_count"] > 0).sum()

        report.metric(
            "Stations with services",
            serviced,
            len(df),
            100,
            "FAIL",
        )