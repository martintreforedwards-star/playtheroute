"""
Certification audit.
"""


def audit_certification(network, report):

    report.section("Certification")

    if report.fail_count == 0:
        report.pass_check("Network is RELEASE READY")
    elif report.fail_count <= 2:
        report.warning("Network is PROVISIONAL")
    else:
        report.fail("Network is NOT READY")

    score = (
        report.pass_count
        / (
            report.pass_count
            + report.warn_count
            + report.fail_count
        )
    ) * 100

    report.info(f"Overall QA score: {score:.1f}%")