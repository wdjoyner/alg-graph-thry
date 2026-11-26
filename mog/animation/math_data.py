"""Animation data and additional exact checks on displayed examples."""
from collections import Counter
from itertools import combinations, product
from math import comb

import verify_draft3 as paper

FANO = ((1, 2, 4), (2, 3, 5), (3, 1, 6), (1, 7, 5),
        (2, 7, 6), (3, 7, 4), (4, 5, 6))
TRIANGLE = ((0, 6, 11), (0, 5, 6), (-1, 4, 2), (1, 4, 10),
            (-2, 3, 5), (0, 3, 7), (2, 3, 3), (-3, 2, 6),
            (-1, 2, 9), (1, 2, 4), (3, 2, 6), (-4, 1, 2),
            (-2, 1, 10), (0, 1, 8), (2, 1, 2), (4, 1, 10),
            (-5, 0, 0), (5, 0, 1))
D = frozenset(paper.projective_views)
Q = paper.Q
ALPHA_Q = frozenset(map(paper.translate, Q))
BETA_Q = frozenset(map(paper.invert, Q))
HAND = paper.example
MOVES = ((4, 3), (7, 5), (11, 9))
PLAY = ((7, 5), (11, 7), (6, 3))


def exchange(hand, move):
    a, b = move
    assert a in hand and b in paper.X - hand
    return (hand - {a}) | {b}


def line(view, a, b, k):
    return frozenset(view[3*r+c] for r, c in product(range(3), repeat=2)
                     if (a*r+b*c) % 3 == k)


V = paper.projective_views[11]
ROW = line(V, 1, 0, 0)
PARALLEL = ROW | line(V, 1, 0, 2)
AXIAL = ROW | line(V, 0, 1, 0)
DIAGONAL = line(V, 1, 1, 0) | line(V, 1, 2, 0)
SQUARE = frozenset(V) - AXIAL
KITTEN = (ROW | D, PARALLEL, AXIAL | {11}, SQUARE | (D - {11}))


def coordinates(hand):
    rows = [{r for r in range(3) if paper.M[r][c] in hand} for c in range(4)]
    counts = tuple(map(len, rows))
    odds = tuple(next(iter(s if len(s) == 1 else set(range(3)) - s))
                 if len(s) in (1, 2) else None for s in rows)
    return counts, odds


def verify():
    pairs = Counter(tuple(sorted(pair)) for block in FANO for pair in combinations(block, 2))
    assert len(pairs) == comb(7, 2) and set(pairs.values()) == {1}
    vectors = dict(zip(range(1, 8), (1, 2, 4, 3, 6, 5, 7)))
    assert all(vectors[a] ^ vectors[b] ^ vectors[c] == 0 for a, b, c in FANO)
    assert Q == {i*i % 11 for i in range(11)}
    assert ALPHA_Q == {1, 2, 4, 5, 6, 10} and BETA_Q == {2, 6, 7, 8, 10, 11}
    assert {x for _, _, x in TRIANGLE} == paper.X
    assert all(set(view) == paper.X - D for view in paper.projective_views.values())
    assert len(AXIAL) == len(DIAGONAL) == 5
    assert line(V, 1, 1, 0) == {4, 6, 9}
    for view in paper.projective_views.values():
        crosses = {line(view, *one, i) | line(view, *two, j)
                   for one, two in (((1, 0), (0, 1)), ((1, 1), (1, 2)))
                   for i, j in product(range(3), repeat=2)}
        assert len(crosses) == 18 and set(map(len, crosses)) == {5}
    assert DIAGONAL | {11} in paper.orbit
    types = paper.kitten(paper.projective_views)
    assert all(h in family for h, family in zip(KITTEN, types))
    assert len(paper.T) == 9 and Counter(sum(x != 0 for x in t) for t in paper.T) == {0: 1, 3: 8}
    assert all(len({(t[i], t[j]) for t in paper.T}) == 9 for i, j in combinations(range(4), 2))
    assert HAND not in paper.H
    assert coordinates(HAND) == ((2, 1, 2, 1), (1, 1, 2, 2))
    assert [t for t in paper.T if t[:2] == (1, 1)] == [(1, 1, 2, 0)]
    assert frozenset(range(1, 7)) in paper.H
    assert coordinates(frozenset(range(1, 7))) == ((3, 3, 0, 0), (None,) * 4)
    assert len(paper.hands) == 924 and len(paper.legal) == 905 and len(paper.H) == 132
    assert paper.losing == paper.H
    assert tuple(m for m in paper.exchanges if m[1] < m[0]) == MOVES
    assert sum(HAND) == 30
    assert [sum(exchange(HAND, m)) for m in MOVES] == [29, 28, 28]
    h = HAND
    for move, total, losing in zip(PLAY, (28, 24, 21), (True, False, True)):
        h = exchange(h, move)
        assert sum(h) == total and (h in paper.H) == losing
    assert not any((h - {a}) | {b} in paper.legal for a in h for b in paper.X - h if b < a)
    second = exchange(HAND, PLAY[0])
    assert coordinates(second)[1] == (None, 1, 0, 2)
    assert [t for t in paper.T if t[1:] == (1, 0, 2)] == [(2, 1, 0, 2)]
    assert sorted(coordinates(exchange(second, PLAY[1]))[0]) == [0, 1, 2, 3]
    print("All displayed examples passed the exact checks.")


if __name__ == "__main__":
    verify()
