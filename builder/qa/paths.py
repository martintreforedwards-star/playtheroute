"""
Common path helpers for QA.
"""

from pathlib import Path


def project_root() -> Path:
    return Path.cwd()


def network_path(network: str) -> Path:
    """
    Returns the root folder for a built network.
    """

    return (
        project_root()
        / "data"
        / "Class1"
        / network.capitalize()
    )


def analysis_path(network: str) -> Path:
    """
    Returns the analysis folder for a network.
    """

    return network_path(network) / "analysis"