def validate(df):

    print()
    print("Validation")
    print("----------")

    print(f"Stations              : {len(df)}")
    print(f"Unique CRS            : {df['crs'].is_unique}")

    print(f"Missing CRS           : {df['crs'].isna().sum()}")
    print(f"Missing Station Names : {df['station_name'].isna().sum()}")
    print(f"Missing Latitude      : {df['latitude'].isna().sum()}")
    print(f"Missing Longitude     : {df['longitude'].isna().sum()}")
    print(f"Missing NLC           : {df['nlc'].eq('').sum()}")
    print(f"Missing Operator      : {df['operator_name'].eq('').sum()}")
    print(f"Missing Slug          : {df['slug'].eq('').sum()}")

    duplicates = df.duplicated("crs").sum()
    print(f"Duplicate CRS         : {duplicates}")

    return df