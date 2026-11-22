"""Lattice width of a lattice polygon (minimum over primitive directions v of
max <v,u> - min <v,u>), and fiber-bound checks used in Section 8.4.  License: MIT."""
import sys, os, itertools
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
def width(U, v): vals = [v[0]*u[0] + v[1]*u[1] for u in U]; return max(vals) - min(vals)
def lattice_width(U, B=12):
    best = None
    for a in range(-B, B+1):
        for b in range(0, B+1):
            if (a, b) == (0, 0) or gcd(abs(a), b) != 1 or (b == 0 and a < 0): continue
            w = width(U, (a, b))
            if best is None or w < best[0]: best = (w, [(a, b)])
            elif w == best[0]: best[1].append((a, b))
    return best
T11 = [(0,0),(1,1),(1,2),(1,3),(1,4),(2,1),(2,2),(2,3),(3,1),(3,2),(4,1)]
SQ = [(i,j) for i in range(3) for j in range(3)]
print("principal triangle: lattice width, directions:", lattice_width(T11))
print("square [0,2]^2:     lattice width, directions:", lattice_width(SQ))
# exhaustive check over F_8: max zeros on the torus of f with Newton polygon in [0,2]^2,
# split by whether f has a factor x - c or y - c (c in F_8^*)
from gf import GF
F = GF(8); E = F.elements_star()
def ev(coef, p):
    s = 0
    for (u, c) in zip(SQ, coef):
        if c: s = F.add(s, F.mul(c, F.mul(F.exp[(F.log[p[0]]*u[0]) % 7], F.exp[(F.log[p[1]]*u[1]) % 7])))
    return s
# Use the symmetry: scale so that some coefficient is 1; brute force over 8^9 is 1.3e8 -- too slow in Python.
# Instead sample: random f, and all products of linear factors.
import random
random.seed(1)
mx_nofactor = 0
pts = [(a, b) for a in E for b in E]
for trial in range(20000):
    coef = [random.randrange(8) for _ in SQ]
    if not any(coef): continue
    Z = [p for p in pts if ev(coef, p) == 0]
    # factor x - c divides f iff f vanishes on the whole line x = c (deg_y f <= 2 < 7)
    has_vert = any(all(ev(coef, (c, b)) == 0 for b in E) for c in E)
    has_horiz = any(all(ev(coef, (a, c)) == 0 for a in E) for c in E)
    if not has_vert:
        mx_nofactor = max(mx_nofactor, len(Z))
print("random sample: max torus zeros of f in V_[0,2]^2 over F_8 with no factor x - c:", mx_nofactor, "(fiber bound 2*7 = 14)")
