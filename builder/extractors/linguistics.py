import re


def extract_linguistics(station):

    name = (station.get("name") or "").strip()

    words = name.split()

    return {
        "word_count": len(words),
        "first_word": words[0] if words else "",
        "last_word": words[-1] if words else "",
        "character_count": len(name),
        "initial_letter": name[:1].upper(),
        "final_letter": name[-1:].upper(),
        "contains_hyphen": "-" in name,
        "contains_apostrophe": "'" in name,
        "contains_digits": bool(re.search(r"\d", name)),
    }