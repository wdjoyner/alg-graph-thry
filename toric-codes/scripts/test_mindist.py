"""Validate mindist (bz mode) against brute force on random small codes."""
import sys, os, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gf import GF, rank_and_rref
from toric import run_mindist
random.seed(1)
bad = 0
for trial in range(300):
    q = random.choice([2, 3, 4, 5, 7, 8, 9])
    F = GF(q)
    k = random.randint(1, 4); n = random.randint(k, 14)
    rows = [[random.randrange(q) for _ in range(n)] for _ in range(k)]
    r, R, _ = rank_and_rref(F, rows)
    if r == 0: continue
    best = n + 1
    for coeffs in itertools.product(range(q), repeat=r):
        if not any(coeffs): continue
        v = [0]*n
        for c, row in zip(coeffs, R):
            v = [F.add(a, F.mul(c, b)) for a, b in zip(v, row)]
        best = min(best, sum(1 for x in v if x))
    res = run_mindist(rows, q, "bz", F)
    if res["d"] != best or res["k"] != r:
        bad += 1; print("MISMATCH", q, n, k, res, best)
print("trials done, mismatches:", bad)
