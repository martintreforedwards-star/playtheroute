"""
Route audit.
"""

from pathlib import Path

import pandas as pd


def audit_routes(network, report):

    report.section("Routes")

    root = Path.cwd()
    network_title = network.capitalize()

    master_csv = (
        root / "data" / network_title / f"{network}_master.csv"
    )

    membership_csv = (
        root / "data" / network_title / "route_membership.csv"
    )

    if not master_csv.exists():
        report.fail("Master CSV missing")
        return

    if not membership_csv.exists():
        report.fail("Route membership missing")
        return

    master = pd.read_csv(master_csv)
    membership = pd.read_csv(membership_csv)

    report.pass_check(f"Master stations: {len(master)}")
    report.pass_check(f"Route memberships: {len(membership)}")

    master_crs = set(master["crs"])
    membership_crs = set(membership["crs"])

    missing = master_crs - membership_crs
    unknown = membership_crs - master_crs

    if not missing:
        report.pass_check("All stations have route memberships")
    else:
        report.fail(
            f"{len(missing)} stations missing route memberships"
        )

    if not unknown:
        report.pass_check("No unknown CRS in route memberships")
    else:
        report.fail(
            f"{len(unknown)} unknown CRS values"
        )

    duplicates = membership.duplicated().sum()

    if duplicates == 0:
        report.pass_check("No duplicate route memberships")
    else:
        report.fail(
            f"{duplicates} duplicate route memberships"
        )

    route_duplicates = membership.duplicated(
        subset=["crs", "route_group"]
    ).sum()

    if route_duplicates == 0:
        report.pass_check("No duplicate CRS/route_group pairs")
    else:
        report.fail(
            f"{route_duplicates} duplicate CRS/route_group pairs"
        )

    blank_routes = membership["route_group"].isna().sum()

    if blank_routes == 0:
        report.pass_check("All route_group values populated")
    else:
        report.fail(
            f"{blank_routes} blank route_group values"
        )

    unique_routes = membership["route_group"].dropna().nunique()

    if unique_routes > 0:
        report.pass_check(
            f"Unique route groups: {unique_routes}"
        )
    else:
        report.fail("No route groups defined")