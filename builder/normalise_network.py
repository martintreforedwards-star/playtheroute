import pandas as pd

from builder.extractors.identity import extract_identity
from builder.extractors.geography import extract_geography
from builder.extractors.operations import extract_operations
from builder.extractors.accessibility import extract_accessibility
from builder.extractors.linguistics import extract_linguistics
from builder.extractors.wordplay import extract_wordplay
from builder.extractors.railway import extract_railway

from builder.enrichers.routes import enrich_routes
from builder.enrichers.journey_times import enrich_journey_times
from builder.enrichers.validate import validate

from builder.report import write_report


def normalise_network(stations, config):

    wanted = set(config["crs"])
    rows = []

    for station in stations:

        if station.get("crsCode") not in wanted:
            continue

        row = {}

        row.update(extract_identity(station))
        row.update(extract_geography(station))
        row.update(extract_operations(station))
        row.update(extract_accessibility(station))
        row.update(extract_linguistics(station))
        row.update(extract_wordplay(station))
        row.update(extract_railway(station))

        rows.append(row)

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    # Enrichment pipeline
    df = enrich_routes(df, config)
    df = enrich_journey_times(df, config)

    # Validation & reporting
    df = validate(df)
    write_report(df, config)

    return (
        df.sort_values("station_name")
          .reset_index(drop=True)
    )