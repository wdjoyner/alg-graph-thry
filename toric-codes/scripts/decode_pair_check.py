"""Verify an error-correcting pair (A,B) for the [49,11,28]_8 code found by
decode_search.py, and test the decoder with it.  License: MIT."""
import sys, os, random, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gf import GF, solve_linear, nullspace
from toric import lattice_points, residues, gen_matrix, torus_points, run_mindist
q = 8; m = 7; n = 49; F = GF(q)
Q = residues(lattice_points([(5,-1),(-1,5),(-1,-1)],[0,0,5]), q)
ALL = [(i, j) for i in range(m) for j in range(m)]
negQ = {((-a) % m, (-b) % m) for a, b in Q}
P = sorted(set(ALL) - negQ)
A = [tuple(x) for x in json.loads(sys.argv[1])] if len(sys.argv) > 1 else \
    [(0,0),(0,1),(0,2),(1,1),(1,2),(2,2),(3,2)]
B = [w for w in ALL if all(((w[0]+a[0]) % m, (w[1]+a[1]) % m) in P for a in A)]
def dist(U): return run_mindist(gen_matrix(sorted(set((u[0]%m, u[1]%m) for u in U)), q, 2, F), q, "bz", F)["d"]
dA = dist(A)
Bstar = [w for w in ALL if ((-w[0]) % m, (-w[1]) % m) not in set(B)]
dBperp = dist(Bstar)
t = min(len(A) - 1, dBperp - 1)
print("A =", A); print("B =", B, "|B| =", len(B))
print("dim A =", len(set((a[0]%m,a[1]%m) for a in A)), " d(C_A) =", dA, " max zeros =", n - dA, "(< 28 needed)")
print("d(C_B^perp) =", dBperp, " => separates", dBperp - 1, "points")
print("guaranteed t =", t if n - dA < 28 else None)
pts = torus_points(q)
def ev(u, k): return F.pow_gen(u[0]*pts[k][0] + u[1]*pts[k][1])
GQ = gen_matrix(Q, q, 2, F)
def decode(r):
    syn = {}
    for w in P:
        s = 0
        for k in range(n): s = F.add(s, F.mul(r[k], ev(w, k)))
        syn[w] = s
    K = [[syn[((a[0]+b[0]) % m, (a[1]+b[1]) % m)] for a in A] for b in B]
    null = nullspace(F, K, len(A))
    if not null: return None
    al = null[0]
    N = [k for k in range(n) if not any(1 for _ in [0]) or
         (lambda s: s == 0)(__import__('functools').reduce(lambda acc, ca: F.add(acc, F.mul(ca[0], ev(ca[1], k))), zip(al, A), 0))]
    M = [[ev(w, k) for k in N] for w in P]
    y, nl = solve_linear(F, M, [syn[w] for w in P])
    if y is None or nl: return None
    e = [0]*n
    for k, v in zip(N, y): e[k] = v
    return [F.sub(a, b) for a, b in zip(r, e)]
random.seed(7)
for terr in (5, 6, 7):
    ok = 0
    for _ in range(200):
        msg = [random.randrange(q) for _ in Q]
        c = [0]*n
        for coef, row in zip(msg, GQ): c = [F.add(x, F.mul(coef, y)) for x, y in zip(c, row)]
        r = list(c)
        for k in random.sample(range(n), terr): r[k] = F.add(r[k], random.randrange(1, q))
        ok += decode(r) == c
    print("errors", terr, ":", ok, "/ 200 decoded correctly")
