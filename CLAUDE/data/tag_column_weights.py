#!/usr/bin/env python3
"""
Add a "weight" tag (low/medium/high) to every columnPool clue, based on how
rare it is RELATIVE TO ITS OWN CATEGORY - not a fixed global threshold.
Categories have very different baseline rarity (geography clues are always
narrow; route clues range from 10% to 84% of a network), so ranking within
category is the only fair comparison.

Usage:
    python3 tag_column_weights.py <clues_file_in> <clues_file_out>
"""
import json, sys
from pathlib import Path

def tag_weights(clues):
    by_cat = {}
    for c in clues["columnPool"]:
        by_cat.setdefault(c["category"], []).append(c)

    for cat, cols in by_cat.items():
        ranked = sorted(cols, key=lambda c: c["match_count"])
        n = len(ranked)
        for i, c in enumerate(ranked):
            pct = i / max(n - 1, 1)  # 0 = rarest in category, 1 = most common
            if pct <= 0.25:
                c["weight"] = "high"     # rarest quarter within its category
            elif pct >= 0.85:
                c["weight"] = "low"      # near-universal - barely narrows anything
            else:
                c["weight"] = "medium"
    return clues


def main():
    in_path, out_path = sys.argv[1], sys.argv[2]
    clues = json.load(open(in_path, encoding="utf-8"))
    clues = tag_weights(clues)
    Path(out_path).write_text(json.dumps(clues, indent=2, ensure_ascii=False), encoding="utf-8")
    counts = {}
    for c in clues["columnPool"]:
        counts.setdefault((c["category"], c["weight"]), 0)
        counts[(c["category"], c["weight"])] += 1
    for k in sorted(counts):
        print(f"  {k[0]:10s} {k[1]:6s}: {counts[k]}")


if __name__ == "__main__":
    main()
