def build_master(config):
    """
    Phase 1

    The master dataset already exists.

    Phase 2 will generate this automatically from the
    CRS Source of Truth.

    For now, simply return the configured master file.
    """

    return config["master"]