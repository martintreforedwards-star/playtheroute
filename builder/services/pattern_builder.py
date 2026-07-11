from collections import defaultdict


def build_patterns(service_paths):
    """
    Convert a list of service paths into unique service patterns.

    Returns:
        patterns: list of pattern dictionaries
    """

    counts = defaultdict(int)

    for service in service_paths:

        key = tuple(service)

        counts[key] += 1

    patterns = []

    for i, (stations, count) in enumerate(counts.items(), start=1):

        patterns.append(
            {
                "pattern_id": f"SP{i:06d}",
                "stations": list(stations),
                "service_count": count,
            }
        )

    return patterns