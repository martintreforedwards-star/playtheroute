def extract_accessibility(station):

    accessibility = station.get("stationAccessibility") or {}
    stepfree = accessibility.get("stepFreeCategory") or {}

    return {
        "staffing_level": station.get("staffingLevel") or "",
        "step_free_category": stepfree.get("category") or "",
    }