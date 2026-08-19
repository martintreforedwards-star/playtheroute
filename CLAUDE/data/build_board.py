#!/usr/bin/env python3
"""
Build the merged per-station board file + auto-generated clue pool
for one or more quizzes, from the master audit CSV + {quiz}_wordplay.json.

Usage:
    python3 build_board.py <master_csv> <wordplay_dir> <output_dir> quiz_id [quiz_id ...]
    python3 build_board.py <master_csv> <wordplay_dir> <output_dir> --all
"""
import csv, json, re, sys, ast
from pathlib import Path
from collections import defaultdict, Counter

MIN_MATCHES = 3
MAX_MATCH_FRACTION = 0.90   # drop near-universal clues (too easy to be useful)
GEOGRAPHY_MAX_MATCH_FRACTION = 0.95  # geography clues get a looser ceiling than
    # other columns: a region/hub clue still meaningfully constrains a puzzle
    # once paired with a row clue, even if it covers most of a geographically
    # concentrated quiz's stations (e.g. semetro is ~94% South East London).
    # Excluding it outright starves the geography category down to whatever's
    # left, and since puzzle-bank generation requires every column category to
    # have a viable option, that one narrow category can bottleneck the whole
    # bank far more than the 0.90 rule's "too easy" rationale intends.
HIGH_WEIGHT_FRACTION = 0.22  # rarer than this -> "high" weight row

# ---------------------------------------------------------------------------
# Player-facing copy, from the label review pass (clue_label_review.csv).
# Anything marked (proposed) was left blank on the sheet - sensible defaults
# filled in here, flagged for a follow-up check rather than blocking on it.
# ---------------------------------------------------------------------------

WORDPLAY_CATEGORY_INFO = {
    "local_suffix": ("a common English place-name ending",
                      "The name ends in a common English place-name suffix, like -ton, -ham, -by or -dale."),
    "gaelic_place": ("Scottish/Gaelic place-name roots",
                      "The name includes a Scottish or Gaelic place-name element, like Inver-, Glen-, Loch- or Kirk-."),
    "welsh_place": ("Welsh place-name roots",
                     "The name includes a Welsh place-name element, like Llan-, Aber-, Pen- or Caer-."),
    "structure": ("an unusual name format",
                  "Something unusual about how the name is written - brackets, a hyphen, an ampersand, or 'St'."),
    "nature": ("a nature word in the name",
               "The name includes a nature word, like Park, Hill, Green, Heath or Wood."),
}


def hub_slug(hub):
    """Turn a hub name into a safe field-name fragment, e.g.
    'Liverpool (Lime St/Central)' -> 'liverpool_lime_st_central'."""
    return re.sub(r"[^a-zA-Z0-9]+", "_", hub).strip("_").lower()


def label_clue(c):
    """Set display (player-facing label) + hint (free tap-explainer text)
    on a clue dict, from the reviewed label set."""
    field, ctype = c["field"], c["type"]
    label = c.get("label", "")

    if field == "is_coastal":
        c["display"] = "Near the coast"
        c["hint"] = "A station within 3 kilometres of the coastline or an estuary."
    elif field == "is_interchange":
        c["display"] = "Is an interchange station"
        c["hint"] = "Served by two or more separate named routes, or where several lines physically meet."  # (proposed)
    elif field == "terminus_max":
        c["display"] = "Terminus station"
        c["hint"] = "At least some journeys terminate at this station - it's not just a stop along the way."
    elif field == "name_word_count":
        if c.get("value") == 1:
            c["display"] = "Station name is one word"
            c["hint"] = "Station is a one-word name."
        else:
            c["display"] = "Station name is 3+ words"
            c["hint"] = "Station name is three or more words long."
    elif field == "name_letter_count":
        if "Short" in label:
            c["display"] = "Station name is 6 letters or fewer"
            c["hint"] = "Station name is 6 characters or fewer."
        elif "Medium" in label:
            c["display"] = "Station name is 7-10 letters"
            c["hint"] = "Station name length is between 7 and 10 characters."
        else:
            c["display"] = "Station name is 11+ letters"
            c["hint"] = "Station name is equal to or exceeds 11 characters."
    elif field == "region":
        v = c["value"]
        c["display"] = f"Is within the {v} region"
        c["hint"] = f"This station is based within the {v} region."
    elif field == "canonical_hub":
        v = c["value"]
        c["display"] = f"Trains head to {v}"  # (proposed)
        c["hint"] = f"This station's journeys are routed via or towards {v}."  # (proposed)
    elif field == "wordplay_category":
        v = c["value"]
        friendly, detail = WORDPLAY_CATEGORY_INFO.get(v, (v, ""))
        c["display"] = f"Naming style: {friendly}"  # (proposed)
        c["hint"] = detail  # (proposed)
    elif field == "wordplay_tags":
        v = c["value"]
        structural = {
            "brackets": ("Name includes brackets", "The station name includes text in brackets, e.g. a disambiguator like '(Cumbria)'."),
            "ampersand": ("Name includes an '&'", "The station name includes an ampersand (&)."),
            "hyphen": ("Name includes a hyphen", "The station name includes a hyphen."),
            "saint": ("Name includes 'St'", "The station name includes 'St' (Saint)."),
            "a_ac": ("Name includes Welsh 'a'/'ac'", "The Welsh station name includes 'a' or 'ac' (meaning 'and'), joining two place names."),
        }
        if v in structural:
            c["display"], c["hint"] = structural[v]
        else:
            c["display"] = f"Word contains '{v}'"
            c["hint"] = f"Word contains '{v}'."
    elif field == "operator":
        v = c["value"]
        c["display"] = f"Route operated by {v}."
        c["hint"] = f"This station is served by {v}."  # (proposed)
    elif field == "route":
        v = c["value"]
        c["display"] = f"Is part of the {v} route"
        c["hint"] = f"A station on the {v} route."
    elif field == "canonical_time_to_hub" or field.startswith("time_to_"):
        m = re.match(r"^Time to (.+?): (.+)$", label)
        target_raw, band = (m.group(1), m.group(2)) if m else ("its hub station", "")
        target = "its hub station" if target_raw.lower() == "hub" else target_raw

        def _mins(v):
            return int(round(v)) if v is not None else None

        lo = _mins(c.get("min"))
        hi = _mins(c.get("max"))

        if band == "shortest third":
            c["display"] = f"A short journey to {target}"
            c["hint"] = (
                f"In this puzzle, 'short' means under {hi} minutes to {target}."
                if hi is not None else
                f"One of the shortest journey times to {target} among this puzzle's candidate stations."
            )
        elif band == "middle third":
            c["display"] = f"A mid-range journey to {target}"
            c["hint"] = (
                f"In this puzzle, 'mid-range' means {lo}-{hi} minutes to {target}."
                if lo is not None and hi is not None else
                f"A middling journey time to {target} among this puzzle's candidate stations."
            )
        else:
            c["display"] = f"A long journey to {target}"
            c["hint"] = (
                f"In this puzzle, 'long' means {lo}+ minutes to {target}."
                if lo is not None else
                f"One of the longest journey times to {target} among this puzzle's candidate stations."
            )
    else:
        c["display"] = label
        c["hint"] = ""
    return c


def load_master(master_csv):
    by_quiz = defaultdict(list)
    with open(master_csv, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            qid = row.get("quiz_id", "").strip()
            if qid:
                by_quiz[qid].append(row)
    return by_quiz


def to_bool(v):
    return v.strip().upper() == "TRUE"


def parse_route(v):
    v = (v or "").strip()
    if not v or v == "not assigned":
        return []
    try:
        parsed = ast.literal_eval(v)
        if isinstance(parsed, list):
            return parsed
    except Exception:
        pass
    return [v]


def name_letter_count(name):
    return sum(1 for ch in name if ch.isalpha())


def name_word_count(name):
    core = name.split("(")[0].strip()  # ignore parenthetical disambiguators like "(Cumbria)"
    return len([w for w in core.replace("&", " ").replace("-", " ").split() if w])


def build_board(quiz_rows, wp_by_name):
    board = []
    for r in quiz_rows:
        wp = wp_by_name.get(r["station_name"], {})
        board.append({
            "station_id": r["station_id"],
            "station_name": r["station_name"],
            "name_word_count": name_word_count(r["station_name"]),
            "name_letter_count": name_letter_count(r["station_name"]),
            "crs": r["crs"] or None,
            "region": r["region"] or None,
            "operator": r["operator"] or None,
            "route": parse_route(r["route"]),
            "is_interchange": to_bool(r["is_interchange"]),
            "is_coastal": to_bool(r["is_coastal"]),
            "terminus_max": int(r["terminus_max"]) if r["terminus_max"] else 0,
            "canonical_hub": r["canonical_hub"] or None,
            "canonical_time_to_hub": float(r["canonical_time_to_hub"]) if r["canonical_time_to_hub"] else None,
            "welsh_name": r["welsh_name"] or None,
            "wordplay_category": wp.get("category"),
            "wordplay_difficulty": wp.get("difficulty"),
            "wordplay_score": wp.get("wordplay_score", 0),
            "wordplay_tags": wp.get("tags", []),
            "time_to_glasgow_central": float(r["time_to_glasgow_central"]) if r.get("time_to_glasgow_central") else None,
            "time_to_victoria": float(r["time_to_victoria"]) if r.get("time_to_victoria") else None,
            "time_to_charing_cross": float(r["time_to_charing_cross"]) if r.get("time_to_charing_cross") else None,
            "time_to_euston": float(r["time_to_euston"]) if r.get("time_to_euston") else None,
            "time_to_liverpool_street": float(r["time_to_liverpool_street"]) if r.get("time_to_liverpool_street") else None,
            "time_to_stratford": float(r["time_to_stratford"]) if r.get("time_to_stratford") else None,
        })
    return board


def add_hub_time_fields(board):
    """For every canonical_hub present in this quiz's board, add a synthetic
    per-hub time field (None for any station that doesn't route to that hub).
    This is what makes it safe to name a specific hub in a time-band clue's
    display/hint text: the clue can only ever match stations that genuinely
    share that hub, even for quizzes that span more than one commuter market.
    Single-hub quizzes go through the same path - it just degenerates to one
    hub, one field, same stations as canonical_time_to_hub - but now the hub
    name is always available to name explicitly rather than falling back to
    a vague "its hub station"."""
    hubs = sorted({s["canonical_hub"] for s in board if s.get("canonical_hub")})
    for hub in hubs:
        field = f"time_to_hub__{hub_slug(hub)}"
        for s in board:
            s[field] = (
                s["canonical_time_to_hub"]
                if s.get("canonical_hub") == hub and s.get("canonical_time_to_hub") is not None
                else None
            )
    return hubs


EXTRA_TIME_FIELDS = [
    ("time_to_glasgow_central", "Glasgow Central"),
    ("time_to_victoria", "Victoria"),
    ("time_to_charing_cross", "Charing Cross"),
    ("time_to_euston", "Euston"),
    ("time_to_liverpool_street", "Liverpool Street"),
    ("time_to_stratford", "Stratford"),
]


def count_matches(board, clue):
    n = 0
    for s in board:
        if clue["type"] == "array_contains":
            val = s.get(clue["field"]) or []
            if isinstance(val, list) and clue["value"] in val:
                n += 1
        elif clue["type"] == "range":
            v = s.get(clue["field"])
            if v is None:
                continue
            if "min" in clue and v < clue["min"]:
                continue
            if "max" in clue and v > clue["max"]:
                continue
            n += 1
        elif clue["type"] == "contains":
            v = str(s.get(clue["field"]) or "").lower()
            if clue["value"].lower() in v:
                n += 1
        else:  # equals
            if s.get(clue["field"]) == clue["value"]:
                n += 1
    return n


def viable(board, clue, max_frac=MAX_MATCH_FRACTION):
    n = count_matches(board, clue)
    frac = n / len(board) if board else 0
    return MIN_MATCHES <= n and frac <= max_frac, n, frac


def tercile_bands(board, field, label):
    """3 roughly-even bands from the field's own observed range, instead of
    fixed cutoffs that only make sense for 'time to a nearby local hub'."""
    vals = sorted(s[field] for s in board if s.get(field) is not None)
    if len(vals) < 6:
        return []
    p33 = vals[len(vals) // 3]
    p66 = vals[(2 * len(vals)) // 3]
    bands = [
        {"type": "range", "field": field, "max": p33, "label": f"{label}: shortest third"},
        {"type": "range", "field": field, "min": p33, "max": p66, "label": f"{label}: middle third"},
        {"type": "range", "field": field, "min": p66, "label": f"{label}: longest third"},
    ]
    return bands


def gen_row_pool(board):
    total = len(board)
    candidates = []
    candidates.append({"type": "equals", "field": "is_interchange", "value": True, "label": "Interchange station"})
    candidates.append({"type": "equals", "field": "is_coastal", "value": True, "label": "Coastal station"})
    candidates.append({"type": "range", "field": "terminus_max", "min": 1, "label": "Terminus station"})
    candidates.append({"type": "equals", "field": "name_word_count", "value": 1, "label": "One-word name"})
    candidates.append({"type": "range", "field": "name_word_count", "min": 3, "label": "Three or more words in name"})
    for lo, hi, label in [(0, 6, "Short name (\u22646 letters)"), (7, 10, "Medium name (7-10 letters)"), (11, None, "Long name (11+ letters)")]:
        c = {"type": "range", "field": "name_letter_count", "label": label}
        if lo is not None:
            c["min"] = lo
        if hi is not None:
            c["max"] = hi
        candidates.append(c)

    # NOTE: region/hub/time-to-hub deliberately NOT offered as rows - they live
    # in the geography/service COLUMN categories instead. Rows and columns must
    # never share a field, or a puzzle can end up with the same fact as both a
    # row and a column (e.g. "Hub: X" as both Platform 1 and Column B) - which
    # makes that cell/column tell the player nothing new.

    pool = []
    for c in candidates:
        ok, n, frac = viable(board, c)
        if not ok:
            continue
        c["weight"] = "high" if frac <= HIGH_WEIGHT_FRACTION else "medium"
        c["match_count"] = n
        pool.append(label_clue(c))
    return pool


def gen_column_pool(board):
    pool = []

    def add(clue, category, max_frac=MAX_MATCH_FRACTION):
        ok, n, frac = viable(board, clue, max_frac)
        if ok:
            clue["category"] = category
            clue["match_count"] = n
            pool.append(label_clue(clue))

    # geography - region/hub only (is_coastal lives in rows, not here)
    regions = Counter(s["region"] for s in board if s["region"])
    for region, n in regions.most_common(10):
        add({"type": "equals", "field": "region", "value": region, "label": f"Region: {region}"}, "geography", max_frac=GEOGRAPHY_MAX_MATCH_FRACTION)
    hubs = Counter(s["canonical_hub"] for s in board if s["canonical_hub"])
    if len(hubs) > 1:
        for hub in hubs:
            add({"type": "equals", "field": "canonical_hub", "value": hub, "label": f"Hub: {hub}"}, "geography", max_frac=GEOGRAPHY_MAX_MATCH_FRACTION)

    # service - time-bands only (interchange/terminus live in rows, not here)
    # Time-to-hub is partitioned PER HUB (see add_hub_time_fields) so a
    # multi-hub quiz never mixes journey times to different termini into
    # one meaningless band, and so the hub can always be safely named in
    # the clue's display/hint text.
    for hub in sorted({s["canonical_hub"] for s in board if s.get("canonical_hub")}):
        field = f"time_to_hub__{hub_slug(hub)}"
        for c in tercile_bands(board, field, f"Time to {hub}"):
            add(c, "service")
    for field, label in EXTRA_TIME_FIELDS:
        for c in tercile_bands(board, field, f"Time to {label}"):
            add(c, "service")

    # route
    operators = Counter(s["operator"] for s in board if s["operator"])
    if len(operators) > 1:
        for op in operators:
            add({"type": "equals", "field": "operator", "value": op, "label": f"Operator: {op}"}, "route")
    route_names = Counter()
    for s in board:
        route_names.update(s["route"])
    for name, n in route_names.most_common(15):
        add({"type": "array_contains", "field": "route", "value": name, "label": f"Route: {name}"}, "route")

    # name (wordplay-driven only - word/letter count moved to rows)
    wp_cats = Counter(s["wordplay_category"] for s in board if s["wordplay_category"] and s["wordplay_category"] != "other")
    for cat, n in wp_cats.most_common():
        add({"type": "equals", "field": "wordplay_category", "value": cat, "label": f"Wordplay: {cat}"}, "name")
    tags = Counter()
    for s in board:
        tags.update(s["wordplay_tags"])
    for tag, n in tags.most_common(15):
        add({"type": "array_contains", "field": "wordplay_tags", "value": tag, "label": f"Name contains '{tag}'"}, "name")

    return pool


def process(quiz_id, quiz_rows, wordplay_dir, output_dir):
    wp_path = Path(wordplay_dir) / f"{quiz_id}_wordplay.json"
    if not wp_path.exists():
        print(f"  [SKIP] {quiz_id}: no wordplay file at {wp_path}")
        return
    wordplay = json.load(open(wp_path, encoding="utf-8"))
    wp_by_name = {w["station_name"]: w for w in wordplay}

    board = build_board(quiz_rows, wp_by_name)
    hubs = add_hub_time_fields(board)
    row_pool = gen_row_pool(board)
    col_pool = gen_column_pool(board)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"board_{quiz_id}.json").write_text(json.dumps(board, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / f"clues_{quiz_id}.json").write_text(
        json.dumps({"rowPool": row_pool, "columnPool": col_pool}, indent=2, ensure_ascii=False), encoding="utf-8")

    cat_counts = Counter(c["category"] for c in col_pool)
    hub_note = f", {len(hubs)} hub(s)" if len(hubs) > 1 else ""
    print(f"  [OK] {quiz_id}: {len(board)} stations{hub_note}, {len(row_pool)} row clues, "
          f"{len(col_pool)} column clues ({dict(cat_counts)})")
    for cat in ("service", "geography", "route", "name"):
        if cat_counts.get(cat, 0) == 0:
            print(f"      WARNING: zero '{cat}' column clues for {quiz_id}")


def main():
    if len(sys.argv) < 5:
        print(__doc__)
        sys.exit(1)
    master_csv, wordplay_dir, output_dir = sys.argv[1:4]
    quiz_args = sys.argv[4:]
    by_quiz = load_master(master_csv)
    quiz_ids = sorted(by_quiz.keys()) if quiz_args == ["--all"] else quiz_args
    for quiz_id in quiz_ids:
        if quiz_id not in by_quiz:
            print(f"  [SKIP] {quiz_id}: not in master CSV")
            continue
        process(quiz_id, by_quiz[quiz_id], wordplay_dir, output_dir)


if __name__ == "__main__":
    main()