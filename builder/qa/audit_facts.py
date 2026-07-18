"""
Facts audit.
"""

import json

from builder.qa.paths import network_path


def audit_facts(network, report):

    report.section("Facts")

    network_dir = network_path(network)

    facts_file = (
        network_dir
        / "analysis"
        / "station-facts.json"
    )

    if not facts_file.exists():
        report.warning("Station facts file not found")
        return

    try:
        with open(facts_file, encoding="utf-8") as f:
            facts = json.load(f)
    except Exception as ex:
        report.fail(f"Unable to read station facts ({ex})")
        return

    report.pass_check(f"Station facts: {len(facts)}")

    if len(facts) == 0:
        report.fail("No station facts found")
        return

    populated = 0

    for value in facts.values():

        if isinstance(value, dict):

            text = (
                value.get("fact")
                or value.get("facts")
                or value.get("description")
                or ""
            )

        else:
            text = str(value)

        if text.strip():
            populated += 1

    report.metric(
        "Stations with facts",
        populated,
        len(facts),
        100,
        "WARN",
    )