#!/usr/bin/env python3
"""
validate_data.py - catches the "orphaned/duplicate wordplay category" bug
class (the Chilham/suffix bug) plus a few other structural sanity checks,
across all board_/clues_/puzzlebank_ files for every quiz.

Run this after every data rebuild, before deploying:

    python3 validate_data.py <data_dir>

Exit code is 0 if clean, 1 if any ERROR-level issue was found (WARNINGs
don't fail the build but are worth reading).
"""
import json, sys
from pathlib import Path
from collections import Counter, defaultdict

MIN_CELL = 2          # must match build_puzzle_bank.py's MIN_CELL
MIN_BANK_SIZE = 500   # below this, a quiz will start repeating puzzles fast

# Keep this in sync with build_board.py's WORDPLAY_CATEGORY_INFO keys.
KNOWN_WORDPLAY_CATEGORIES = {
    "local_suffix", "gaelic_place", "welsh_place", "structure", "nature",
    "other",  # intentionally excluded from clue generation, not an error
}


def match_set(board, clue):
    s = set()
    for st in board:
        if clue["type"] == "array_contains":
            val = st.get(clue["field"]) or []
            if isinstance(val, list) and clue["value"] in val:
                s.add(st["station_id"])
        elif clue["type"] == "range":
            v = st.get(clue["field"])
            if v is None:
                continue
            if "min" in clue and v < clue["min"]:
                continue
            if "max" in clue and v > clue["max"]:
                continue
            s.add(st["station_id"])
        elif clue["type"] == "contains":
            v = str(st.get(clue["field"]) or "").lower()
            if clue["value"].lower() in v:
                s.add(st["station_id"])
        else:
            if st.get(clue["field"]) == clue["value"]:
                s.add(st["station_id"])
    return s


def check_orphaned_categories(board, quiz_id, errors, warnings):
    """Flag any wordplay_category with no defined label - this is exactly
    how Chilham silently fell out of its intended clue."""
    cats = Counter(s.get("wordplay_category") for s in board if s.get("wordplay_category"))
    unknown = set(cats) - KNOWN_WORDPLAY_CATEGORIES
    for cat in unknown:
        errors.append(
            f"[{quiz_id}] wordplay_category '{cat}' ({cats[cat]} stations) has no "
            f"label in WORDPLAY_CATEGORY_INFO - these stations will show an ugly "
            f"raw label if ever selected as a clue, or silently vanish from the "
            f"category they should belong to. Known categories: {sorted(KNOWN_WORDPLAY_CATEGORIES)}"
        )


def check_near_duplicate_categories(board, quiz_id, warnings):
    """Flag categories whose tag vocabularies overlap heavily - the
    underlying signature of the suffix/local_suffix and place/welsh_place
    bugs, independent of what the category happens to be named."""
    cat_tags = defaultdict(set)
    for s in board:
        cat = s.get("wordplay_category")
        if cat and cat != "other":
            cat_tags[cat].update(s.get("wordplay_tags") or [])

    cats = list(cat_tags)
    for i in range(len(cats)):
        for j in range(i + 1, len(cats)):
            a, b = cats[i], cats[j]
            overlap = cat_tags[a] & cat_tags[b]
            union = cat_tags[a] | cat_tags[b]
            if union and len(overlap) / len(union) >= 0.5:
                warnings.append(
                    f"[{quiz_id}] categories '{a}' {sorted(cat_tags[a])} and "
                    f"'{b}' {sorted(cat_tags[b])} share {len(overlap)}/{len(union)} "
                    f"tags - likely the same concept split across two category "
                    f"names. Worth a manual look."
                )


def check_clue_match_counts(clues, board, quiz_id, errors):
    """Recompute match_count independently - catches stale numbers left
    over from a manual JSON patch instead of a real rebuild."""
    for pool_name in ("rowPool", "columnPool"):
        for c in clues[pool_name]:
            if "match_count" not in c:
                continue
            actual = len(match_set(board, c))
            if actual != c["match_count"]:
                errors.append(
                    f"[{quiz_id}] clue '{c.get('display', c.get('value'))}' "
                    f"({pool_name}) has match_count={c['match_count']} but "
                    f"recomputing from the board gives {actual} - data is stale, "
                    f"needs a rebuild."
                )
            if actual == 0:
                errors.append(
                    f"[{quiz_id}] clue '{c.get('display', c.get('value'))}' matches "
                    f"ZERO stations - completely unplayable, should not exist in "
                    f"the clue pool at all."
                )


def check_puzzlebank_playability(bank, clues, board, quiz_id, errors):
    """Independently re-verify every cell of every banked puzzle actually
    has >= MIN_CELL matching stations - catches generator bugs rather than
    trusting the generator's own output."""
    row_by_id = {c["id"]: c for c in clues["rowPool"]}
    col_by_id = {c["id"]: c for c in clues["columnPool"]}
    sets_cache = {}

    def get_set(clue_id, clue):
        if clue_id not in sets_cache:
            sets_cache[clue_id] = match_set(board, clue)
        return sets_cache[clue_id]

    bad = 0
    for puzzle in bank:
        for r_id in puzzle["rows"]:
            for c_id in puzzle["columns"]:
                r_set = get_set(r_id, row_by_id[r_id])
                c_set = get_set(c_id, col_by_id[c_id])
                if len(r_set & c_set) < MIN_CELL:
                    bad += 1
    if bad:
        errors.append(
            f"[{quiz_id}] {bad} cell(s) across the puzzle bank have fewer than "
            f"{MIN_CELL} matching stations - these puzzles are unplayable as "
            f"generated. Re-run build_puzzle_bank.py."
        )


def check_bank_size(bank, quiz_id, warnings):
    if len(bank) < MIN_BANK_SIZE:
        years = len(bank) / 365
        warnings.append(
            f"[{quiz_id}] puzzle bank is thin: {len(bank)} puzzles (~{years:.1f} "
            f"years before a repeat). Consider adding stations or clue variety."
        )


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 validate_data.py <data_dir>")
        sys.exit(2)
    data_dir = Path(sys.argv[1])

    quiz_ids = sorted(p.stem.replace("board_", "") for p in data_dir.glob("board_*.json"))
    if not quiz_ids:
        print(f"No board_*.json files found in {data_dir}")
        sys.exit(2)

    all_errors, all_warnings = [], []

    for quiz_id in quiz_ids:
        board_path = data_dir / f"board_{quiz_id}.json"
        clues_path = data_dir / f"clues_{quiz_id}.json"
        bank_path = data_dir / f"puzzlebank_{quiz_id}.json"

        if not clues_path.exists():
            all_errors.append(f"[{quiz_id}] missing clues_{quiz_id}.json")
            continue

        board = json.loads(board_path.read_text(encoding="utf-8"))
        clues = json.loads(clues_path.read_text(encoding="utf-8"))

        check_orphaned_categories(board, quiz_id, all_errors, all_warnings)
        check_near_duplicate_categories(board, quiz_id, all_warnings)
        check_clue_match_counts(clues, board, quiz_id, all_errors)

        if bank_path.exists():
            bank = json.loads(bank_path.read_text(encoding="utf-8"))
            check_puzzlebank_playability(bank, clues, board, quiz_id, all_errors)
            check_bank_size(bank, quiz_id, all_warnings)
        else:
            all_warnings.append(f"[{quiz_id}] no puzzlebank_{quiz_id}.json found - skipped playability check")

    print(f"Checked {len(quiz_ids)} quizzes.\n")

    if all_warnings:
        print(f"--- {len(all_warnings)} WARNING(S) ---")
        for w in all_warnings:
            print("  WARN:", w)
        print()

    if all_errors:
        print(f"--- {len(all_errors)} ERROR(S) ---")
        for e in all_errors:
            print("  ERROR:", e)
        print()
        print("FAILED")
        sys.exit(1)
    else:
        print("PASSED - no errors found")
        sys.exit(0)


if __name__ == "__main__":
    main()
