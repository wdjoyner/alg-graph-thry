"""Build math_objects.json, the registry of every mathematical object the
episode outlines refer to.

Outlines never type a card, total or count by hand.  They name an object
here (for example "hand:example") and state the fields they rely on; the
outline checker compares those claims with this file.  Rerun this script
whenever an example changes:

    python build_math_objects.py              # write math_objects.json
    python build_math_objects.py --cross-check

The definitions below (the MINIMOG array M, the tetracode T and the
odd-man-out test) are copied from the paper, mog.tex, Section 5, and from
its verifier.  With --cross-check the script also imports ../../verify.py
(the paper's verifier) and asserts that both give the same 132 hexads.
"""
import argparse
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
X = frozenset(range(12))
HANDS = [frozenset(c) for c in combinations(sorted(X), 6)]
M = ((6, 3, 0, 9), (5, 2, 7, 10), (4, 1, 8, 11))  # MINIMOG, shuffle labels
T = sorted({(b, a, (a + b) % 3, (a + 2 * b) % 3)
            for a, b in product(range(3), repeat=2)})
FANO = ((1, 2, 4), (2, 3, 5), (3, 1, 6), (1, 7, 5),
        (2, 7, 6), (3, 7, 4), (4, 5, 6))
Q = frozenset({0, 1, 3, 4, 5, 9})  # seed on the projective line; 11 = infinity


def columns(h):
    return [{r for r in range(3) if M[r][c] in h} for c in range(4)]


def coordinates(h):
    """Column counts and odd-man-out rows (None marks a wildcard column)."""
    cols = columns(h)
    odds = [next(iter(s if len(s) == 1 else set(range(3)) - s))
            if len(s) in (1, 2) else None for s in cols]
    return [len(s) for s in cols], odds


def is_hexad(h):
    counts, odds = coordinates(h)
    if sorted(counts) == [0, 1, 2, 3]:
        return False
    return any(all(o is None or t[c] == o for c, o in enumerate(odds)) for t in T)


HEXADS = {h for h in HANDS if is_hexad(h)}
LEGAL = {h for h in HANDS if sum(h) >= 21}


def down_moves(h):
    """Legal exchanges (out, in): a smaller card, new total at least 21."""
    return [(a, b) for a in sorted(h) for b in sorted(X - h)
            if b < a and sum(h) - a + b >= 21]


def swap(h, move):
    a, b = move
    assert a in h and b not in h
    return (h - {a}) | {b}


def losing_positions():
    losing = set()
    for h in sorted(LEGAL, key=sum):
        if not any(swap(h, m) in losing for m in down_moves(h)):
            losing.add(h)
    return losing


LOSING = losing_positions()

# Curtis's kitten in shuffle labels: corner point -> its 3x3 affine view
# (paper, Section 6; same data as the verifier's `views`).
VIEWS = {6: (5, 11, 3, 8, 2, 4, 9, 10, 7), 1: (5, 11, 3, 2, 4, 8, 7, 9, 10),
         0: (8, 10, 3, 9, 11, 4, 5, 2, 7)}


def kitten_family_sets():
    """Line + corners, two parallel lines, cross + own corner, square + other corners."""
    corners = set(VIEWS)
    fams = [set() for _ in range(4)]
    for p, v in VIEWS.items():
        lines = [[frozenset(v[3 * r + c] for r, c in product(range(3), repeat=2)
                            if (a * r + b * c) % 3 == k) for k in range(3)]
                 for a, b in ((1, 0), (0, 1), (1, 1), (1, 2))]
        fams[0].update(frozenset(corners) | l for ls in lines for l in ls)
        fams[1].update(l | m for ls in lines for l, m in combinations(ls, 2))
        for i, j in ((0, 1), (2, 3)):
            for l, m in product(lines[i], lines[j]):
                fams[2].add((l | m) | {p})
                fams[3].add(frozenset(set(v) - (l | m)) | (corners - {p}))
    return fams


def kitten_families():
    return [len(f) for f in kitten_family_sets()]


def hand(h, note):
    counts, odds = coordinates(h)
    return {"cards": sorted(h), "total": sum(h), "hexad": h in HEXADS,
            "legal": h in LEGAL, "losing": h in LOSING,
            "column_counts": counts, "odd_man_out": odds,
            "down_moves": len(down_moves(h)), "note": note}


def winning_replies(h):
    """For each move from a losing hand, the replies that land on a hexad."""
    tree = []
    for m in down_moves(h):
        k = swap(h, m)
        replies = [r for r in down_moves(k) if swap(k, r) in HEXADS]
        tree.append({"move": list(m), "total": sum(k),
                     "replies": [{"move": list(r), "total": sum(swap(k, r))}
                                 for r in replies]})
    return tree


def build():
    objects = {}
    A = frozenset({0, 2, 4, 6, 7, 11})          # the paper's running example
    low = frozenset(range(1, 7))
    high = X - low
    objects["hand:example"] = hand(A, "Running example A of the paper, total 30")
    objects["hand:1to6"] = hand(low, "The dead hand of Episode 1")
    objects["hand:complement_1to6"] = hand(high, "Its complement, total 45")

    play = [(7, 5), (11, 7), (6, 3)]
    h, steps = A, []
    for i, m in enumerate(play):
        h = swap(h, m)
        objects[f"hand:game_after_{i + 1}"] = hand(h, f"Worked game after move {i + 1}")
        steps.append({"move": list(m), "player": 1 + i % 2, "total": sum(h),
                      "lands_on_hexad": h in HEXADS})
    objects["game:worked"] = {"start": "hand:example", "steps": steps,
                              "winner": 1, "note": "Paper, Section 8.2"}

    exchanges = [(a, b) for a in sorted(A) for b in sorted(X - A)
                 if swap(A, (a, b)) in HEXADS]
    objects["moves:example_to_hexads"] = {
        "all": [list(m) for m in exchanges],
        "down": [list(m) for m in exchanges if m[1] < m[0]],
        "up": [list(m) for m in exchanges if m[1] > m[0]],
        "down_totals": [sum(swap(A, m)) for m in exchanges if m[1] < m[0]]}

    # Episode 1, scene 4: two of Pascal's tries from the 45-hand, with the
    # reply that sends him back to a hexad.  Chosen as his biggest drops.
    tries = sorted(down_moves(high), key=lambda m: m[1] - m[0])[:2]
    objects["tries:complement_1to6"] = {
        "from": "hand:complement_1to6", "moves_available": len(down_moves(high)),
        "tries": [t for t in winning_replies(high) if tuple(t["move"]) in tries]}

    # Episode 1, scene 5: a losing hand of total 24 small enough to check
    # every move on screen.  Pick the 24-hexad with the fewest moves.
    h24 = min((h for h in HEXADS if sum(h) == 24),
              key=lambda h: (len(down_moves(h)), sorted(h)))
    objects["hand:hexad_24"] = hand(h24, "A total-24 losing hand checked exhaustively")
    objects["tree:hexad_24"] = {"from": "hand:hexad_24",
                                "branches": winning_replies(h24)}

    totals = Counter(sum(h) for h in HEXADS)
    big = [h for h in HANDS if sum(h) > 21]
    p = Fraction(sum(h not in HEXADS for h in big), len(big))
    objects["count:game"] = {
        "hands": len(HANDS), "legal": len(LEGAL), "losing": len(LOSING),
        "losing_equals_hexads": LOSING == HEXADS,
        "below_21": sum(sum(h) < 21 for h in HANDS),
        "equal_21": sum(sum(h) == 21 for h in HANDS),
        "all_21_are_hexads": all(h in HEXADS for h in HANDS if sum(h) == 21),
        "hexad_totals": dict(sorted(totals.items())),
        "redeal_probability": f"{p.numerator}/{p.denominator}",
        "redeal_percent": round(100 * p.numerator / p.denominator, 2)}

    fives = Counter(frozenset(s) for h in HEXADS for s in combinations(h, 5))
    objects["count:design"] = {
        "hexads": len(HEXADS), "five_subsets": comb(12, 5),
        "each_five_once": len(fives) == comb(12, 5) and set(fives.values()) == {1},
        "blocks_from_counting": comb(12, 5) // 6,
        "complements_are_hexads": all(X - h in HEXADS for h in HEXADS),
        "kitten_families": kitten_families(),
        "kitten_union_is_all_hexads": set.union(*kitten_family_sets()) == HEXADS}

    nbrs = {h: {swap(h, (a, b)) for a in h for b in X - h} for h in HANDS}
    objects["count:johnson"] = {
        "vertices": len(HANDS), "degree": {len(v) for v in nbrs.values()}.pop(),
        "hexad_independent": all(not (nbrs[h] & HEXADS) for h in HEXADS),
        "nonhexad_hexad_neighbors": {len(nbrs[h] & HEXADS)
                                     for h in HANDS if h not in HEXADS}.pop(),
        "quotient": [[0, 36], [6, 30]]}

    pairs = Counter(p for line in FANO for p in combinations(sorted(line), 2))
    objects["fano"] = {"lines": [list(l) for l in FANO], "circle": [4, 5, 6],
                       "each_pair_once": len(pairs) == 21 and set(pairs.values()) == {1},
                       "completions": {"1,4": 2, "4,5": 6}}
    objects["seed:Q"] = {"points": sorted(Q), "infinity_label": 11,
                         "is_zero_and_squares_mod_11": Q == {i * i % 11 for i in range(11)}}
    objects["minimog"] = {"rows": [list(r) for r in M]}
    objects["kitten:views"] = {
        "corners": sorted(VIEWS),
        "views": {str(k): list(v) for k, v in sorted(VIEWS.items())},
        "each_view_is_the_other_nine": all(set(v) == X - set(VIEWS) for v in VIEWS.values()),
        "note": "Curtis's kitten in card (shuffle) labels; corners are infinity, 0, 1 relabeled"}
    word_a1_b1 = [t for t in T if (t[1], t[0]) == (1, 1)]
    objects["tetracode"] = {
        "words": [list(t) for t in T], "size": len(T),
        "formula": "(b, a, a+b, a+2b) mod 3",
        "word_a1_b1": list(word_a1_b1[0]),
        "any_two_coordinates_determine": all(
            len({(t[i], t[j]) for t in T}) == 9 for i, j in combinations(range(4), 2))}
    a, b = 11, 1  # Pascal's illegal swap in Episode 1, scene 2
    objects["move:illegal_11_1"] = {"from": "hand:example", "move": [a, b],
                                    "new_total": sum(A) - a + b,
                                    "legal": (a, b) in down_moves(A)}
    return objects


def cross_check(objects):
    import importlib.util
    spec = importlib.util.spec_from_file_location("verify", HERE.parent.parent / "verify.py")
    paper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(paper)
    assert set(paper.H) == HEXADS, "hexads disagree with the paper's verifier"
    print("Cross-check: same 132 hexads as verify.py")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--cross-check", action="store_true")
    args = parser.parse_args()
    objects = build()
    assert objects["count:game"]["losing_equals_hexads"]
    if args.cross_check:
        cross_check(objects)
    out = {"_about": ["Generated by build_math_objects.py; do not edit by hand.",
                      "Outlines refer to these objects by key."],
           "objects": objects}
    (HERE / "math_objects.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"Wrote math_objects.json ({len(objects)} objects)")


if __name__ == "__main__":
    main()
