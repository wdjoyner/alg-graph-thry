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


# ---------------------------------------------------------------- Episode 2
# The projective line P^1(F_11): labels 0..10, with 11 standing for infinity
# (paper, Section 3).  Episode 2 draws the ring, the projective kitten and
# the shuffle relabeling from these definitions, never from typed-in sets.

INF = 11
P = ((0, 3, 11, 2), (5, 9, 8, 10), (4, 1, 6, 7))  # projective MINIMOG (paper, Section 5)
RHO = {P[r][c]: M[r][c] for r, c in product(range(3), range(4))}  # projective -> card labels
# Curtis's kitten in projective labels: corner -> its 3x3 view, rows top to
# bottom (paper, Figure "kitten-threeviews"; the verifier's projective_views).
PROJECTIVE_VIEWS = {11: (6, 10, 3, 2, 7, 4, 5, 9, 8), 0: (5, 7, 3, 6, 9, 4, 2, 10, 8),
                    1: (5, 7, 3, 9, 4, 6, 8, 2, 10)}
# Triangle layout (x, y, projective label), copied from ../math_data.py.
PROJECTIVE_TRIANGLE = ((0, 6, 11), (0, 5, 6), (-1, 4, 2), (1, 4, 10), (-2, 3, 5), (0, 3, 7),
                       (2, 3, 3), (-3, 2, 6), (-1, 2, 9), (1, 2, 4), (3, 2, 6), (-4, 1, 2),
                       (-2, 1, 10), (0, 1, 8), (2, 1, 2), (4, 1, 10), (-5, 0, 0), (5, 0, 1))
DIRECTIONS = {"row": (1, 0), "column": (0, 1), "diagonal": (1, 2), "modular_diagonal": (1, 1)}
# The two perpendicular pairs of directions (axial and diagonal crosses).
PERPENDICULAR = (((1, 0), (0, 1)), ((1, 1), (1, 2)))


def translate(x):
    """alpha(x) = x + 1 mod 11; infinity is fixed."""
    return x if x == INF else (x + 1) % 11


def invert(x):
    """beta(x) = -1/x mod 11; 0 and infinity trade places."""
    return INF if x == 0 else 0 if x == INF else (-pow(x, -1, 11)) % 11


RING_MAPS = {"translate": translate, "invert": invert}


def orbit_layers(seed):
    """Breadth-first orbit of seed under alpha and beta: the new sets at each step."""
    seen, layer, layers = {seed}, [seed], [[seed]]
    while layer:
        nxt = []
        for h in layer:
            for f in (translate, invert):
                k = frozenset(map(f, h))
                if k not in seen:
                    seen.add(k)
                    nxt.append(k)
        layer = nxt
        if nxt:
            layers.append(nxt)
    return layers


ORBIT = {h for layer in orbit_layers(Q) for h in layer}


def view_line(view, direction, k):
    """The points of a 3x3 view on the line a*r + b*c = k (mod 3)."""
    a, b = direction
    return frozenset(view[3 * r + c] for r, c in product(range(3), repeat=2) if (a * r + b * c) % 3 == k)


def view_lines(view):
    """The twelve lines of a view, three in each of the four directions."""
    return {d: [view_line(view, d, k) for k in range(3)] for d in ((1, 0), (0, 1), (1, 1), (1, 2))}


def kitten_parts(views):
    """Every hexad of the four families, with the parts it is made of.

    Returns a list of (family, picture, parts, hexad); family is 0..3 (line +
    corners, two parallel lines, cross + own corner, square + other corners),
    and parts is a list of (direction, k) lines.  The same hexad may come
    from several pictures; all are listed, in a fixed order."""
    corners = set(views)
    out = []
    for p, v in views.items():
        lines = view_lines(v)
        for d, ls in lines.items():
            for k, l in enumerate(ls):
                out.append((0, p, [(d, k)], frozenset(corners) | l))
        for d, ls in lines.items():
            for i, j in combinations(range(3), 2):
                out.append((1, p, [(d, i), (d, j)], ls[i] | ls[j]))
        for d1, d2 in PERPENDICULAR:
            for i, j in product(range(3), repeat=2):
                cross = lines[d1][i] | lines[d2][j]
                out.append((2, p, [(d1, i), (d2, j)], cross | {p}))
                out.append((3, p, [(d1, i), (d2, j)], frozenset(set(v) - cross) | (corners - {p})))
    return out


def decompose(h, views):
    """The first (family, picture, parts) that builds hexad h in the kitten."""
    for fam, p, parts, hexad in kitten_parts(views):
        if hexad == frozenset(h):
            return fam, p, parts
    return None


def fano_completion(a, b):
    """The third point on the unique Fano line through a and b."""
    lines = [l for l in FANO if a in l and b in l]
    assert len(lines) == 1, (a, b, lines)
    return next(x for x in lines[0] if x not in (a, b))


def five_completion(five, blocks):
    """The unique block of a Steiner system S(5,6,12) holding five points."""
    found = [h for h in blocks if set(five) <= h]
    assert len(found) == 1, (five, found)
    return next(iter(found[0] - set(five)))


def fano_positions():
    """The paper's Fano figure: corners 1, 2, 3 on a circle of radius 1, sides'
    midpoints 4, 5, 6, center 7.  Returns {point: (x, y)}."""
    import math
    corner = {1: 90, 2: 210, 3: 330}
    pos = {k: (math.cos(math.radians(a)), math.sin(math.radians(a))) for k, a in corner.items()}
    mid = lambda i, j: ((pos[i][0] + pos[j][0]) / 2, (pos[i][1] + pos[j][1]) / 2)
    pos.update({4: mid(1, 2), 5: mid(2, 3), 6: mid(3, 1), 7: (0.0, 0.0)})
    return {k: (round(x, 6) + 0.0, round(y, 6) + 0.0) for k, (x, y) in pos.items()}


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
    # Triangle layout of the kitten (x, y, label): copied from ../math_data.py
    # (projective labels, 11 = infinity), relabeled into card labels by the
    # paper's cell-by-cell map from the projective array P to the MINIMOG M.
    P = ((0, 3, 11, 2), (5, 9, 8, 10), (4, 1, 6, 7))
    rel = {P[r][c]: M[r][c] for r, c in product(range(3), range(4))}
    tri = ((0, 6, 11), (0, 5, 6), (-1, 4, 2), (1, 4, 10), (-2, 3, 5), (0, 3, 7),
           (2, 3, 3), (-3, 2, 6), (-1, 2, 9), (1, 2, 4), (3, 2, 6), (-4, 1, 2),
           (-2, 1, 10), (0, 1, 8), (2, 1, 2), (4, 1, 10), (-5, 0, 0), (5, 0, 1))
    spots = [[x, y, rel[v]] for x, y, v in tri]
    corners = {tuple(s[:2]): s[2] for s in spots if tuple(s[:2]) in ((0, 6), (-5, 0), (5, 0))}
    objects["kitten:triangle"] = {
        "spots": spots,
        "corners": sorted(corners.values()),
        "labels_are_all_twelve": {s[2] for s in spots} == set(X),
        "corners_match_views": set(corners.values()) == set(VIEWS),
        "note": "Positions (x in -5..5, y in 0..6) of the triangular kitten in card labels; repeated labels are the same point"}
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
    build_episode2(objects)
    build_episode3(objects)
    return objects


def build_episode2(objects):
    """Objects Episode 2 draws: the Fano figure, the ring, the projective
    kitten, the shuffle relabeling, and Episode 1's hands in the kitten."""
    import math
    pos = fano_positions()
    straight = [l for l in FANO if set(l) != {4, 5, 6}]

    def collinear(a, b, c):
        (x1, y1), (x2, y2), (x3, y3) = pos[a], pos[b], pos[c]
        return abs((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)) < 1e-6

    objects["fano"]["positions"] = {str(k): list(v) for k, v in sorted(pos.items())}
    objects["fano"]["straight_lines_collinear"] = all(collinear(*l) for l in straight)
    objects["fano"]["circle_radius"] = round(math.hypot(*pos[4]), 6)
    objects["fano"]["circle_concyclic"] = len({round(math.hypot(*pos[p]), 6) for p in (4, 5, 6)}) == 1
    objects["fano"]["points"] = 7
    objects["fano"]["line_size"] = 3

    layers = orbit_layers(Q)
    fives = Counter(frozenset(s) for h in ORBIT for s in combinations(h, 5))
    five = (1, 2, 3, 4, 5)
    objects["ring:projective"] = {
        "labels": [str(x) for x in range(11)] + ["∞"],
        "infinity_label": INF,
        "translate": [translate(x) for x in range(12)],
        "invert": [invert(x) for x in range(12)],
        "nonzero_squares": sorted({i * i % 11 for i in range(1, 11)}),
        "squares_in_order": [i * i % 11 for i in range(1, 6)],
        "seed": sorted(Q),
        "translate_seed": sorted(map(translate, Q)),
        "invert_seed": sorted(map(invert, Q)),
        "ten_plus_one": translate(10),
        "five_example": {"points": list(five), "completion": five_completion(five, ORBIT)},
        "note": "Projective line mod 11; label 11 is infinity, drawn at the center of the ring"}
    objects["orbit:Q"] = {
        "layers": [len(l) for l in layers],
        "running_totals": [sum(len(l) for l in layers[:i + 1]) for i in range(len(layers))],
        "hexads": len(ORBIT), "five_subsets": len(fives), "per_block": comb(6, 5),
        "each_five_once": len(fives) == comb(12, 5) and set(fives.values()) == {1},
        "fives_counted": len(ORBIT) * comb(6, 5),
        "relabeled_equals_card_hexads": {frozenset(RHO[x] for x in h) for h in ORBIT} == HEXADS,
        "layer_examples": [sorted(min(l, key=sorted)) for l in layers],
        "note": "Breadth-first orbit of the seed under add-one and negative reciprocal"}
    objects["count:design"]["five_in_block"] = comb(6, 5)
    objects["count:design"]["fives_formula"] = [[12, 11, 10, 9, 8], [5, 4, 3, 2, 1]]
    objects["shuffle:rho"] = {
        "map": [RHO[x] for x in range(12)],
        "views_match": {RHO[d]: tuple(RHO[x] for x in v) for d, v in PROJECTIVE_VIEWS.items()} == VIEWS,
        "bijective": sorted(RHO.values()) == list(range(12)),
        "note": "Projective label x (11 = infinity) -> card label map[x]; cell by cell from the projective MINIMOG to the MINIMOG"}

    # Example lines, crosses and family members, in the picture at infinity.
    v = PROJECTIVE_VIEWS[INF]
    ex = {name: {"picture": INF, "parts": [[list(d), 0]], "points": sorted(view_line(v, d, 0))}
          for name, d in DIRECTIONS.items()}
    cross = view_line(v, (1, 0), 0) | view_line(v, (0, 1), 0)
    ex["cross"] = {"picture": INF, "parts": [[[1, 0], 0], [[0, 1], 0]], "points": sorted(cross)}
    ex["square"] = {"picture": INF, "parts": [[[1, 0], 0], [[0, 1], 0]], "points": sorted(set(v) - cross)}
    corners = sorted(PROJECTIVE_VIEWS)
    fams = {}
    wanted = {"family_line": (0, [((1, 0), 0)]), "family_parallel": (1, [((1, 0), 0), ((1, 0), 2)]),
              "family_cross": (2, [((1, 0), 0), ((0, 1), 0)]),
              "family_square": (3, [((1, 0), 0), ((0, 1), 0)])}
    every = kitten_parts(PROJECTIVE_VIEWS)
    for name, (fam, parts) in wanted.items():
        hexad = next(hx for f, p, ps, hx in every if f == fam and p == INF and ps == parts)
        fams[name] = {"family": fam, "picture": INF, "parts": [[list(d), k] for d, k in parts],
                      "hexad": sorted(hexad), "in_orbit": hexad in ORBIT}
    family_sets = [{hx for f, _, _, hx in every if f == i} for i in range(4)]
    repeats = Counter(lab for _, _, lab in PROJECTIVE_TRIANGLE)
    objects["kitten:projective"] = {
        "spots": [list(s) for s in PROJECTIVE_TRIANGLE],
        "corners": [INF, 0, 1],
        "views": [[d, list(PROJECTIVE_VIEWS[d])] for d in (INF, 0, 1)],
        "each_view_is_the_other_nine": all(set(x) == X - set(PROJECTIVE_VIEWS) for x in PROJECTIVE_VIEWS.values()),
        "repeated_labels": {str(k): n for k, n in sorted(repeats.items()) if n > 1},
        "families": [len(f) for f in family_sets],
        "families_disjoint": sum(map(len, family_sets)) == len(set.union(*family_sets)),
        "union_is_orbit": set.union(*family_sets) == ORBIT,
        "crosses_per_picture": len({hx for f, p, _, hx in every if f == 2 and p == INF}),
        "examples": ex,
        "family_examples": fams,
        "note": "Curtis's kitten in projective labels (11 = infinity); views list [corner, nine labels, rows top to bottom]"}

    hands = {}
    for key in ("hand:1to6", "hand:complement_1to6", "hand:hexad_24", "hand:game_after_3", "hand:game_after_1"):
        h = frozenset(objects[key]["cards"])
        fam, p, parts = decompose(h, VIEWS)
        hands[key] = {"cards": sorted(h), "family": fam, "picture": p,
                      "parts": [[list(d), k] for d, k in parts], "hexad": h in HEXADS}
    objects["kitten:ep1_hands"] = {
        "hands": hands,
        "views": [[RHO[d], list(VIEWS[RHO[d]])] for d in (INF, 0, 1)],
        "note": "Episode 1's losing hands in the card-labeled (shuffle) kitten: family 0..3, picture, parts"}


# ---------------------------------------------------------------- Episode 3
# Ada's test: the MINIMOG M, the tetracode T and the odd-man-out reading
# (paper, Section 5).  Episode 3 draws every word, reading, forced word and
# repair from these functions, never from typed-in values.

def tetra_word(a, b):
    """The tetracode word for a, b: (b, a, a+b, a+2b) mod 3."""
    return (b, a, (a + b) % 3, (a + 2 * b) % 3)


def words_through(known):
    """The tetracode words that agree with known, a dict {coordinate: value}."""
    return [t for t in T if all(t[i] == v for i, v in known.items())]


def column_reading(rows):
    """(count, odd man out) of one column whose marked cells are in rows; None is a wildcard."""
    rows = set(rows)
    if len(rows) == 1:
        return 1, next(iter(rows))
    if len(rows) == 2:
        return 2, next(iter(set(range(3)) - rows))
    return len(rows), None


def forbidden(counts):
    """Column counts 0, 1, 2 and 3 in some order: rejected whatever the rows say."""
    return sorted(counts) == [0, 1, 2, 3]


def test_hand(h):
    """Ada's test on a hand: counts, readings, the words that fit, the verdict."""
    counts, odds = coordinates(h)
    fits = words_through({i: o for i, o in enumerate(odds) if o is not None})
    return {"column_counts": counts, "odd_man_out": odds, "forbidden": forbidden(counts),
            "wildcards": sum(o is None for o in odds), "words_fitting": [list(t) for t in fits],
            "passes": not forbidden(counts) and bool(fits)}


def forced_word(h, pair):
    """The one word through the readings at the two coordinates in pair."""
    _, odds = coordinates(h)
    found = words_through({i: odds[i] for i in pair})
    assert len(found) == 1, (sorted(h), pair, found)
    return found[0]


def disagreements(word, odds):
    """Coordinates where a hand's reading (not a wildcard) differs from word."""
    return [i for i, o in enumerate(odds) if o is not None and word[i] != o]


def all_swaps(h):
    """Every single exchange (out, in) of a hand card for a pile card."""
    return [(a, b) for a in sorted(h) for b in sorted(X - h)]


def repairs(h):
    """The swaps that turn h into a hexad."""
    return [m for m in all_swaps(h) if swap(h, m) in HEXADS]


def build_episode3(objects):
    """Objects Episode 3 draws: the MINIMOG's rows and columns, the three-hour
    clock, the tetracode words, the odd-man-out test on Episode 1's hands, the
    forbidden counts, and the repairs of the opening hand."""
    m = objects["minimog"]
    m["row_labels"] = [0, 1, 2]
    m["columns"] = [[M[r][c] for r in range(3)] for c in range(4)]
    m["cards_once"] = sorted(v for row in M for v in row) == list(range(12))
    objects["clock:mod3"] = {
        "hours": [0, 1, 2],
        "sums": {f"{x}+{y}": (x + y) % 3 for x in range(3) for y in range(3)},
        "twice": [2 * x % 3 for x in range(3)],
        "note": "Arithmetic mod 3 on a clock with three hours; 'twice' is x + x"}
    v = PROJECTIVE_VIEWS[INF]
    cells = sorted((r, c) for r in range(3) for c in range(3) if (r + c) % 3 == 0)
    objects["kitten:wrap"] = {
        "picture": INF, "direction": [1, 1], "k": 0,
        "cells": [list(rc) for rc in cells],
        "points": sorted(view_line(v, (1, 1), 0)),
        "cell_points": [v[3 * r + c] for r, c in cells],
        "row_plus_column": [(r + c) % 3 for r, c in cells],
        "note": "Episode 2's wrapped diagonal (picture at infinity, projective labels): row + column = 0 mod 3"}

    t = objects["tetracode"]
    pairs = list(combinations(range(4), 2))
    t["by_ab"] = {f"{a},{b}": list(tetra_word(a, b)) for a, b in product(range(3), repeat=2)}
    t["formula_matches_words"] = sorted(tetra_word(a, b) for a, b in product(range(3), repeat=2)) == T
    t["a1_b1_steps"] = {"b": 1, "a": 1, "a+b": (1 + 1) % 3, "a+2b": (1 + 2) % 3, "a+2b_before_wrap": 1 + 2}
    t["coordinate_pairs"] = [list(p) for p in pairs]
    t["pairs_checked"] = len(pairs)
    t["distinct_pairs_per_choice"] = [len({(w[i], w[j]) for w in T}) for i, j in pairs]
    t["first_two_1_1"] = [list(w) for w in words_through({0: 1, 1: 1})]

    col = M[0][0], M[1][0], M[2][0]
    demos = {"one": [M[1][0]], "two": [M[0][0], M[2][0]], "empty": [], "full": list(col)}
    objects["odd_man_out:demo"] = {
        "column": 0, "cards": list(col),
        "demos": {k: {"cards": cs, "count": column_reading({r for r in range(3) if M[r][0] in cs})[0],
                      "reading": column_reading({r for r in range(3) if M[r][0] in cs})[1]}
                  for k, cs in demos.items()},
        "note": "One column of the MINIMOG marked four ways; reading None is a wildcard"}

    bad = [h for h in HANDS if forbidden(coordinates(h)[0])]
    objects["count:forbidden"] = {
        "hands": len(bad),
        "specified_coordinates": sorted({4 - sum(o is None for o in coordinates(h)[1]) for h in bad}),
        "all_fit_a_word": all(words_through({i: o for i, o in enumerate(coordinates(h)[1]) if o is not None})
                              for h in bad),
        "hexads": sum(h in HEXADS for h in bad),
        "note": "Hands with column counts 0, 1, 2, 3: the words alone would pass them all; none is a hexad"}
    test_agrees = all(test_hand(h)["passes"] == (h in HEXADS) for h in HANDS)
    objects["count:test"] = {"hands": len(HANDS), "test_agrees_with_hexads": test_agrees,
                             "passing": sum(test_hand(h)["passes"] for h in HANDS)}

    A = frozenset(objects["hand:example"]["cards"])
    for key in ("hand:example", "hand:1to6", "hand:game_after_2"):
        h = frozenset(objects[key]["cards"])
        objects[key]["test"] = test_hand(h)
    word = forced_word(A, (0, 1))
    _, odds = coordinates(A)
    off = disagreements(word, odds)
    fix_col = off[0]
    out = next(x for x in A if x in [M[r][fix_col] for r in range(3)])
    inn = M[word[fix_col]][fix_col]
    objects["test:example"] = {
        "hand": "hand:example", "reading": odds, "forced_from": [0, 1],
        "forced_word": list(word), "is_word_a1_b1": list(word) == objects["tetracode"]["word_a1_b1"],
        "disagrees_at": off, "hand_row": odds[fix_col], "word_row": word[fix_col],
        "fix": [out, inn], "fix_is_repair": swap(A, (out, inn)) in HEXADS,
        "fixed_reading": coordinates(swap(A, (out, inn)))[1],
        "note": "The opening hand's first two readings force a word; the last column disagrees, and moving its card to the word's row repairs the hand"}

    reps = repairs(A)
    after = swap(A, (7, 5))
    objects["moves:example_to_hexads"].update({
        "swaps": len(all_swaps(A)), "repairs": len(reps),
        "legal_moves": len(down_moves(A)),
        "legal_repairs": sum(m in down_moves(A) for m in reps),
        "up_totals": [sum(swap(A, m)) for m in reps if m[1] > m[0]],
        "after_7_5": {"cards": sorted(after), **test_hand(after)}})


def cross_check(objects):
    import importlib.util
    spec = importlib.util.spec_from_file_location("verify", HERE.parent.parent / "verify.py")
    paper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(paper)
    assert set(paper.H) == HEXADS, "hexads disagree with the paper's verifier"
    assert set(paper.orbit) == ORBIT, "the ring's orbit disagrees with the paper's verifier"
    assert paper.projective_views == PROJECTIVE_VIEWS and paper.views == VIEWS
    assert paper.rel == RHO, "the shuffle relabeling disagrees with the paper's verifier"
    assert all(set.union(*paper.kitten(vs)) == {hx for f, _, _, hx in kitten_parts(vs)}
               for vs in (VIEWS, PROJECTIVE_VIEWS)), "kitten families disagree"
    print("Cross-check: same 132 hexads, orbit, kitten views and relabeling as verify.py")


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
