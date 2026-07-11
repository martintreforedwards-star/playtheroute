def report_profiles(profiles):

    reverse = sum(
        1
        for p in profiles
        if p["has_reverse"]
    )

    circular = sum(
        1
        for p in profiles
        if p["is_circular"]
    )

    shuttle = sum(
        1
        for p in profiles
        if p["is_shuttle"]
    )

    print()
    print("==========================")
    print("Pattern Profile Report")
    print("==========================")
    print()

    print(f"Patterns analysed : {len(profiles):,}")
    print(f"Reverse patterns  : {reverse:,}")
    print(f"Circular patterns : {circular:,}")
    print(f"Shuttle patterns  : {shuttle:,}")