import pandas as pd

AGGREGATE = "data/Class1/Southern/southern_aggregated_1.csv"
ROUTES = "data/Southern/route_membership.csv"


def main():

    agg = pd.read_csv(AGGREGATE)
    routes = pd.read_csv(ROUTES)

    agg["crs"] = agg["crs"].fillna("").astype(str).str.strip().str.upper()
    routes["crs"] = routes["crs"].fillna("").astype(str).str.strip().str.upper()

    route_col = None

    for col in routes.columns:
        if col.lower() in ("route", "route_group", "route_groups"):
            route_col = col
            break

    if route_col is None:
        print("No route column found.")
        print(routes.columns.tolist())
        return

    lookup = (
        routes.groupby("crs")[route_col]
        .first()
        .reset_index()
    )

    agg = agg.drop(columns=["route"], errors="ignore")

    agg = agg.merge(
        lookup,
        on="crs",
        how="left"
    )

    agg.rename(columns={route_col: "route"}, inplace=True)

    agg.to_csv(AGGREGATE, index=False)

    print(f"Routes populated: {agg['route'].notna().sum()}")


if __name__ == "__main__":
    main()