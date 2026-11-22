"""Simplex-type error-correcting pairs for D = C_Q, Q = principal 11-point triangle, q = 8.
Find g in GL_2(Z/7), u in (Z/7)^2 and the largest s with u + g(S_s) inside
P = complement of -Q (mod 7).  Then A = g(S_a), B = u + g(S_b) with a + b = s.
License: MIT."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from toric import lattice_points, residues
m = 7
Q = set(residues(lattice_points([(5,-1),(-1,5),(-1,-1)],[0,0,5]), 8))
negQ = {((-a) % m, (-b) % m) for a, b in Q}
def S(s): return [(i, j) for i in range(s+1) for j in range(s+1-i)]
best = {}
for g in itertools.product(range(m), repeat=4):
    if (g[0]*g[3]-g[1]*g[2]) % m == 0: continue
    for u in itertools.product(range(m), repeat=2):
        s = 0
        while s < 12:
            img = {((u[0] + g[0]*i + g[1]*j) % m, (u[1] + g[2]*i + g[3]*j) % m) for i, j in S(s+1)}
            if img & negQ: break
            s += 1
        if s not in best: best[s] = (g, u)
smax = max(best)
print("largest simplex size s with a translate of g(S_s) avoiding -Q mod 7:", smax, "example g,u:", best[smax])
from math import comb
for s in range(1, smax+1):
    opts = []
    for a in range(1, s+1):
        b = s - a
        if a * 7 >= 28: continue          # need a(q-1) < d(D) = 28
        t = min(comb(a+2, 2) - 1, b + 1)
        opts.append((t, a, b))
    print("s =", s, "best (t, a, b):", max(opts) if opts else None)
