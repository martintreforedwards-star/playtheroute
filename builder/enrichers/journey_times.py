def enrich_journey_times(df, config):
    """
    Add journey-time attributes.

    Placeholder for now.
    """

    df["primary_hub"] = config["primary_hub"]
    df["canonical_time_to_hub"] = None

    return df