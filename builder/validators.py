from builder.requirements import REQUIRED_FIELDS


def validate(stations):

    print("\nValidation")

    missing = []

    for field in REQUIRED_FIELDS:

        if field in stations.columns:
            print(f"✓ {field}")
        else:
            print(f"✗ {field}")
            missing.append(field)

    return missing