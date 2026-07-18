"""
Wordplay audit.
"""

import json

from builder.qa.paths import network_path


def audit_wordplay(network, report):

    report.section("Wordplay")

    network_dir = network_path(network)

    wordplay_file = (
        network_dir
        / "analysis"
        / f"{network}_wordplay.json"
    )

    if not wordplay_file.exists():
        report.warning("Wordplay file not found")
        return

    try:
        with open(wordplay_file, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as ex:
        report.fail(f"Unable to read wordplay ({ex})")
        return

    report.pass_check(f"Wordplay entries: {len(data)}")

    if len(data) > 0:
        report.pass_check("Wordplay available")
    else:
        report.fail("No wordplay entries")