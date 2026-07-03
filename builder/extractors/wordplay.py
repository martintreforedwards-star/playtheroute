def extract_wordplay(station):

    name = (station.get("name") or "").strip()

    words = name.split()

    return {
        "starts_with_the": name.lower().startswith("the "),
        "starts_with_st": words[0].lower() in ("st", "st.") if words else False,
        "contains_and": " and " in name.lower(),
        "contains_central": "central" in name.lower(),
        "contains_parkway": "parkway" in name.lower(),
        "contains_junction": "junction" in name.lower(),
    }