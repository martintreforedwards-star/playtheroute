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