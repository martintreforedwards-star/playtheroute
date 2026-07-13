"""
Structure audit.
"""

from pathlib import Path

import pandas as pd

from builder.qa.schema import (
    MASTER_SCHEMA,
    ENRICHED_SCHEMA,
)


def check_file(path, description, report):
    if path.exists():
        report.pass_check(f"{description} found")
    else:
        report.fail(f"{description} missing")


def validate_csv(
    path,
    description,
    report,
    required_columns=None,
    unique_columns=None,
    non_blank_columns=None,
):

    if not path.exists():
        return

    required_columns = required_columns or []
    unique_columns = unique_columns or []
    non_blank_columns = non_blank_columns or []

    try:
        df = pd.read_csv(path)
    except Exception as ex:
        report.fail(f"Unable to read {description} ({ex})")
        return

    report.pass_check(f"{description} loaded ({len(df)} rows)")

    for column in required_columns:

        if column in df.columns:
            report.pass_check(f"{description}: column '{column}' present")
        else:
            report.fail(f"{description}: column '{column}' missing")

    for column in unique_columns:

        if column not in df.columns:
            continue

        duplicates = df[column].duplicated().sum()

        if duplicates == 0:
            report.pass_check(f"{description}: '{column}' unique")
        else:
            report.fail(
                f"{description}: {duplicates} duplicate '{column}' values"
            )

    for column in non_blank_columns:

        if column not in df.columns:
            continue

        blanks = df[column].isna().sum()

        if blanks == 0:
            report.pass_check(f"{description}: '{column}' complete")
        else:
            report.fail(
                f"{description}: {blanks} blank '{column}' values"
            )


def audit_structure(network, report):

    root = Path.cwd()
    network_title = network.capitalize()

    master_csv = (
        root / "data" / network_title / f"{network}_master.csv"
    )

    enriched_csv = (
        root / "data" / network_title / f"{network}_enriched.csv"
    )

    files = [
        (
            root / "builder" / "configs" / f"{network}.json",
            "Network config",
        ),
        (
            master_csv,
            "Master CSV",
        ),
        (
            enriched_csv,
            "Enriched CSV",
        ),
        (
            root / "data" / network_title / f"{network}.json",
            "Network JSON",
        ),
        (
            root / "data" / network_title / "route_membership.csv",
            "Route membership",
        ),
        (
            root / "data" / "Masters" / "network_membership.csv",
            "Network membership",
        ),
    ]

    report.section("Files")

    for path, description in files:
        check_file(path, description, report)

    report.section("Master CSV")

    validate_csv(
        master_csv,
        "Master CSV",
        report,
        **MASTER_SCHEMA,
    )

    report.section("Enriched CSV")

    validate_csv(
        enriched_csv,
        "Enriched CSV",
        report,
        **ENRICHED_SCHEMA,
    )