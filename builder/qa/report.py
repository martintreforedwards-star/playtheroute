"""
QA Report framework for The Route Builder.
"""

from dataclasses import asdict, dataclass
from pathlib import Path
import json


@dataclass
class QAResult:
    section: str
    level: str
    message: str


class QAReport:

    def __init__(self, network):
        self.network = network
        self.results = []
        self.current_section = "General"

    def section(self, name):
        self.current_section = name

    def pass_check(self, message):
        self.results.append(QAResult(self.current_section, "PASS", message))

    def warning(self, message):
        self.results.append(QAResult(self.current_section, "WARN", message))

    def fail(self, message):
        self.results.append(QAResult(self.current_section, "FAIL", message))

    def info(self, message):
        self.results.append(QAResult(self.current_section, "INFO", message))

    @property
    def pass_count(self):
        return sum(r.level == "PASS" for r in self.results)

    @property
    def warn_count(self):
        return sum(r.level == "WARN" for r in self.results)

    @property
    def fail_count(self):
        return sum(r.level == "FAIL" for r in self.results)

    @property
    def info_count(self):
        return sum(r.level == "INFO" for r in self.results)

    def print_report(self):
        print()
        print("=" * 60)
        print("The Route QA Audit")
        print("=" * 60)
        print(f"Network : {self.network}")
        print()

        current = None

        for result in self.results:
            if result.section != current:
                current = result.section
                print()
                print(current)
                print("-" * len(current))

            print(f"{result.level:5} {result.message}")

        print()
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"PASS : {self.pass_count}")
        print(f"WARN : {self.warn_count}")
        print(f"FAIL : {self.fail_count}")
        print(f"INFO : {self.info_count}")
        print("=" * 60)

    def to_dict(self):
        return {
            "network": self.network,
            "summary": {
                "pass": self.pass_count,
                "warn": self.warn_count,
                "fail": self.fail_count,
                "info": self.info_count,
            },
            "results": [asdict(r) for r in self.results],
        }

    def save_json(self, output_path):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

        return output_path
