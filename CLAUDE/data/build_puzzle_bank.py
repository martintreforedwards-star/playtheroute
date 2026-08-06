#!/usr/bin/env python3
"""
Enumerate every valid, playable puzzle (2 rows x 4 columns) for a quiz,
from its board_{quiz}.json + clues_{quiz}.json, and report the pool size.

A puzzle is valid if all 8 row-column cell intersections have >= MIN_CELL
matching stations (matches the game's own playability requirement).

Usage:
    python3 build_puzzle_bank.py <board_dir> <output_dir> quiz_id [quiz_id ...]
    python3 build_puzzle_bank.py <board_dir> <output_dir> --all
"""
import json, sys, time
from pathlib import Path
from itertools import product, combinations

MIN_CELL = 2  # min stations satisfying both row+column for a playable cell


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


def build_bank(quiz_id, board_dir, output_dir):
    board = json.load(open(Path(board_dir) / f"board_{quiz_id}.json", encoding="utf-8"))
    clues = json.load(open(Path(board_dir) / f"clues_{quiz_id}.json", encoding="utf-8"))

    for i, c in enumerate(clues["rowPool"]):
        c["id"] = f"row_{i}"
        c["_set"] = match_set(board, c)
    for i, c in enumerate(clues["columnPool"]):
        c["id"] = f"col_{i}"
        c["_set"] = match_set(board, c)

    high_rows = [c for c in clues["rowPool"] if c["weight"] == "high"]
    med_rows = [c for c in clues["rowPool"] if c["weight"] == "medium"]
    by_cat = {cat: [c for c in clues["columnPool"] if c["category"] == cat]
              for cat in ("service", "geography", "route", "name")}

    bank = []
    t0 = time.time()
    MAX_BANK_SIZE = 5000
    for hr, mr in combinations(clues["rowPool"], 2):
        # prefilter columns that work with BOTH rows before the 4-way product
        filtered = {}
        ok = True
        for cat, cols in by_cat.items():
            survivors = [c for c in cols
                         if len(c["_set"] & hr["_set"]) >= MIN_CELL
                         and len(c["_set"] & mr["_set"]) >= MIN_CELL]
            if not survivors:
                ok = False
                break
            filtered[cat] = survivors
        if not ok:
            continue
        for sv, ge, ro, na in product(filtered["service"], filtered["geography"],
                                       filtered["route"], filtered["name"]):
            bank.append({
                "rows": [hr["id"], mr["id"]],
                "columns": [sv["id"], ge["id"], ro["id"], na["id"]],
            })

    elapsed = time.time() - t0
    full_count = len(bank)
    if full_count > MAX_BANK_SIZE:
        import random
        random.seed(quiz_id)  # deterministic, so reruns produce the same trimmed bank
        bank = random.sample(bank, MAX_BANK_SIZE)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    clean_clues = {
        "rowPool": [{k: v for k, v in c.items() if k != "_set"} for c in clues["rowPool"]],
        "columnPool": [{k: v for k, v in c.items() if k != "_set"} for c in clues["columnPool"]],
    }
    (out / f"clues_{quiz_id}.json").write_text(json.dumps(clean_clues, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / f"puzzlebank_{quiz_id}.json").write_text(json.dumps(bank, indent=2, ensure_ascii=False), encoding="utf-8")

    years = len(bank) / 365
    note = f" (capped from {full_count})" if full_count > MAX_BANK_SIZE else ""
    print(f"  {quiz_id}: {len(bank)} valid puzzles{note}  (~{years:.1f} years before a repeat)  [{elapsed:.1f}s]")
    return len(bank)


def main():
    board_dir, output_dir = sys.argv[1], sys.argv[2]
    quiz_args = sys.argv[3:]
    if quiz_args == ["--all"]:
        quiz_ids = sorted(p.stem.replace("board_", "") for p in Path(board_dir).glob("board_*.json"))
    else:
        quiz_ids = quiz_args
    for q in quiz_ids:
        build_bank(q, board_dir, output_dir)


if __name__ == "__main__":
    main()
