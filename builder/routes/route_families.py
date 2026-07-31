from pathlib import Path

import pandas as pd


MASTER = Path("data/Masters")


def main():

    routes = pd.read_csv(MASTER / "routes.csv")
    tree = pd.read_csv(MASTER / "route_tree.csv")

    # ------------------------------------------------------------------
    # Build parent lookup
    # ------------------------------------------------------------------

    parent_lookup = {}

    if "child_route" in tree.columns and "parent_route" in tree.columns:

        for _, row in tree.iterrows():
            parent_lookup[row["child_route"]] = row["parent_route"]

    elif "route_id" in tree.columns and "parent_route" in tree.columns:

        for _, row in tree.iterrows():
            parent_lookup[row["route_id"]] = row["parent_route"]

    else:
        raise ValueError(
            "route_tree.csv must contain either "
            "(child_route,parent_route) or "
            "(route_id,parent_route)"
        )

    # ------------------------------------------------------------------
    # Find top-most ancestor
    # ------------------------------------------------------------------

    def find_family(route):

        current = route

        while (
            current in parent_lookup
            and pd.notna(parent_lookup[current])
            and parent_lookup[current] != current
        ):
            current = parent_lookup[current]

        return current

    routes["family_id"] = routes["route_id"].apply(find_family)

    # ------------------------------------------------------------------
    # Family names
    # ------------------------------------------------------------------

    family_lookup = (
        routes
        .set_index("route_id")["primary_destination"]
        .to_dict()
    )

    routes["family_name"] = routes["family_id"].map(
        family_lookup
    )

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    outfile = MASTER / "routes_families.csv"

    routes.to_csv(outfile, index=False)

    print(f"Saved {outfile}")

    print()
    print("Families")
    print("--------")

    summary = (
        routes.groupby("family_id")
        .size()
        .sort_values(ascending=False)
    )

    print(summary.head(20))

    print()
    print(f"Families : {len(summary)}")
    print(f"Routes   : {len(routes)}")


if __name__ == "__main__":
    main()