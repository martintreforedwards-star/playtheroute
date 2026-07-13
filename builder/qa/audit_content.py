"""
Content audit.
"""

from pathlib import Path

import pandas as pd

from builder.qa.schema import CONTENT_SCHEMA


def audit_content(network, report):

    report.section("Content")

    root = Path.cwd()
    network_title = network.capitalize()

    enriched_csv = (
        root / "data" / network_title / f"{network}_enriched.csv"
    )

    if not enriched_csv.exists():
        report.fail("Enriched CSV missing")
        return

    try:
        df = pd.read_csv(enriched_csv)
    except Exception as ex:
        report.fail(f"Unable to read Enriched CSV ({ex})")
        return

    total = len(df)

    for field, rules in CONTENT_SCHEMA.items():

        threshold = rules["threshold"]
        severity = rules["severity"]

        if field not in df.columns:
            if severity == "WARN":
                report.warning(f"{field} column missing")
            else:
                report.fail(f"{field} column missing")
            continue

        complete = df[field].notna().sum()

        percentage = (complete / total) * 100 if total else 0

        report.metric(
    field,
    complete,
    total,
    threshold,
    severity,
)