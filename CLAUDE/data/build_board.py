#!/usr/bin/env python3
"""
Build the merged per-station board file + auto-generated clue pool
for one or more quizzes, from the master audit CSV + {quiz}_wordplay.json.

Usage:
    python3 build_board.py <master_csv> <wordplay_dir> <output_dir> quiz_id [quiz_id ...]
    python3 build_board.py <master_csv> <wordplay_dir> <output_dir> --all
"""
import csv, json, sys, ast
from pathlib import Path
from collections import defaultdict, Counter

MIN_MATCHES = 3
MAX_MATCH_FRACTION = 0.90   # drop near-universal clues (too easy to be useful)
HIGH_WEIGHT_FRACTION = 0.22  # rarer than this -> "high" weight row


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


def viable(board, clue):
    n = count_matches(board, clue)
    frac = n / len(board) if board else 0
    return MIN_MATCHES <= n and frac <= MAX_MATCH_FRACTION, n, frac


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
        pool.append(c)
    return pool


def gen_column_pool(board):
    pool = []

    def add(clue, category):
        ok, n, frac = viable(board, clue)
        if ok:
            clue["category"] = category
            clue["match_count"] = n
            pool.append(clue)

    # geography - region/hub only (is_coastal lives in rows, not here)
    regions = Counter(s["region"] for s in board if s["region"])
    for region, n in regions.most_common(10):
        add({"type": "equals", "field": "region", "value": region, "label": f"Region: {region}"}, "geography")
    hubs = Counter(s["canonical_hub"] for s in board if s["canonical_hub"])
    if len(hubs) > 1:
        for hub in hubs:
            add({"type": "equals", "field": "canonical_hub", "value": hub, "label": f"Hub: {hub}"}, "geography")

    # service - time-bands only (interchange/terminus live in rows, not here)
    for c in tercile_bands(board, "canonical_time_to_hub", "Time to hub"):
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
    row_pool = gen_row_pool(board)
    col_pool = gen_column_pool(board)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"board_{quiz_id}.json").write_text(json.dumps(board, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / f"clues_{quiz_id}.json").write_text(
        json.dumps({"rowPool": row_pool, "columnPool": col_pool}, indent=2, ensure_ascii=False), encoding="utf-8")

    cat_counts = Counter(c["category"] for c in col_pool)
    print(f"  [OK] {quiz_id}: {len(board)} stations, {len(row_pool)} row clues, "
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
