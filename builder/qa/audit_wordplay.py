"""
Wordplay audit.
"""

from pathlib import Path

import json


def audit_wordplay(network, report):

    report.section("Wordplay")

    root = Path.cwd()
    network_title = network.capitalize()

    wordplay_file = (
        root
        / "data"
        / network_title
        / "analysis"
        / f"{network}_wordplay.json"
    )

    if not wordplay_file.exists():
        report.warning("Wordplay file not found")
        return

    with open(wordplay_file, encoding="utf-8") as f:
        data = json.load(f)

    report.pass_check(f"Wordplay entries: {len(data)}")

    if len(data) > 0:
        report.pass_check("Wordplay available")
    else:
        report.fail("No wordplay entries")