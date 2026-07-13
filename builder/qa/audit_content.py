"""
Content audit.
"""


def audit_content(network, report):

    report.info("Checking metadata completeness")

    report.pass_check("Content audit framework loaded")