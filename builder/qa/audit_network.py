"""
Master QA runner.
"""

import argparse
from pathlib import Path
from builder.qa.audit_routes import audit_routes
from builder.qa.audit_structure import audit_structure
from builder.qa.report import QAReport
from builder.qa.audit_content import audit_content
from builder.qa.audit_gameplay import audit_gameplay
from builder.qa.audit_wordplay import audit_wordplay
from builder.qa.audit_facts import audit_facts
from builder.qa.audit_certification import audit_certification

AUDITS = [
    ("Structure", audit_structure),
    ("Content", audit_content),
    ("Routes", audit_routes),
    ("Gameplay", audit_gameplay),
    ("Wordplay", audit_wordplay),
    ("Facts", audit_facts),
    ("Certification", audit_certification),
]

def main():

    parser = argparse.ArgumentParser(
        description="The Route QA Audit"
    )

    parser.add_argument(
        "network",
        help="Network name (e.g. southeastern)",
    )

    args = parser.parse_args()

    report = QAReport(args.network)

    report.info("Starting QA audit...")

    for name, audit in AUDITS:
        report.info(f"Running {name} Audit")
        audit(args.network, report)

    report.print_report()

    analysis_dir = (
        Path.cwd()
        / "data"
        / args.network.capitalize()
        / "analysis"
    )

    output_file = analysis_dir / "qa_report.json"

    report.save_json(output_file)

    print()
    print(f"QA report written to: {output_file}")

    raise SystemExit(1 if report.fail_count else 0)


if __name__ == "__main__":
    main()
