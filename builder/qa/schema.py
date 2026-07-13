"""
QA schema definitions.

Defines what every generated file is expected to contain.
"""

MASTER_SCHEMA = {
    "required_columns": [
        "station_id",
        "crs",
        "station_name",
    ],
    "unique_columns": [
        "station_id",
        "crs",
    ],
    "non_blank_columns": [
        "crs",
    ],
}

ENRICHED_SCHEMA = {
    "required_columns": [
        "station_id",
        "crs",
        "latitude",
        "longitude",
    ],
    "unique_columns": [
        "station_id",
        "crs",
    ],
    "non_blank_columns": [
        "latitude",
        "longitude",
    ],
}

CONTENT_SCHEMA = {
    "latitude": {"threshold": 100, "severity": "FAIL"},
    "longitude": {"threshold": 100, "severity": "FAIL"},
    "route_count": {"threshold": 100, "severity": "FAIL"},
    "service_count": {"threshold": 100, "severity": "FAIL"},
    "difficulty_score": {"threshold": 100, "severity": "WARN"},
    "accessibility_score": {"threshold": 100, "severity": "WARN"},
  "county": {"threshold": 0, "severity": "INFO"},
"region": {"threshold": 0, "severity": "INFO"},
}