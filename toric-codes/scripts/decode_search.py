"""Search for error-correcting pairs (A,B) for the toric code D = C_Q over F_8,
Q = the 11-point triangle of the principal example.

By the duality theorem, D = C_P^perp with P = complement of -Q in (Z/7)^2.
Conditions (Pellikaan): A+B subset of P (mod 7), dim C_A > t,
d(C_B^perp) > t, and n - d(C_A) < d(D) = 28.
License: MIT."""
import sys, os, itertools, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gf import GF
from toric import lattice_points, residues, gen_matrix, run_mindist

q = 8; m = q - 1; n = m * m
F = GF(q)
Q = residues(lattice_points([(5,-1),(-1,5),(-1,-1)],[0,0,5]), q)
ALL = [(i, j) for i in range(m) for j in range(m)]
negQ = {((-a) % m, (-b) % m) for a, b in Q}
P = set(ALL) - negQ
assert len(P) == n - len(Q)

def d_of(U):
    U = sorted(set((a % m, b % m) for a, b in U))
    return run_mindist(gen_matrix(U, q, 2, F), q, "bz", F)["d"]

def dual_dist(B):
    Bs = set(ALL) - {((-a) % m, (-b) % m) for a, b in B}
    return d_of(Bs)

def convex_sets(N=5):
    pts = [(i, j) for i in range(N) for j in range(N)]
    seen = set()
    def hull_points(V):
        # lattice points in conv(V) via half-plane test on hull edges
        import math
        V = sorted(set(V))
        if len(V) == 1: return set(V)
        def cross(o, a, b): return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
        lower, upper = [], []
        for p in V:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0: lower.pop()
            lower.append(p)
        for p in reversed(V):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0: upper.pop()
            upper.append(p)
        H = lower[:-1] + upper[:-1]
        if len(H) <= 2:
            a, b = V[0], V[-1]
            return {p for p in pts if cross(a, b, p) == 0 and min(a[0],b[0]) <= p[0] <= max(a[0],b[0]) and min(a[1],b[1]) <= p[1] <= max(a[1],b[1])}
        return {p for p in pts if all(cross(H[i], H[(i+1)%len(H)], p) >= 0 for i in range(len(H)))}
    for r in range(1, 5):
        for V in itertools.combinations(pts, r):
            S = hull_points(V)
            mx = min(x for x, y in S); my = min(y for x, y in S)
            key = frozenset((x-mx, y-my) for x, y in S)
            if key not in seen:
                seen.add(key); yield sorted(key)

best = []
cache_A = {}
cands = list(convex_sets(5))
print("candidate shapes:", len(cands), flush=True)
for A in cands:
    if len(A) < 3: continue
    Ar = {(a % m, b % m) for a, b in A}
    if len(Ar) < len(A): continue
    # translate A over all residues: only shape matters, but B depends on P, so use B_max(A)
    B = [w for w in ALL if all(((w[0]+a) % m, (w[1]+b) % m) in P for a, b in Ar)]
    if not B: continue
    tmax = min(len(A) - 1, len(B))
    if best and tmax <= best[0][0]: continue
    dA = d_of(A)
    if n - dA >= 28: continue
    sep = dual_dist(B) - 1
    t = min(len(A) - 1, sep)
    rec = (t, len(A), dA, len(B), sep, A, B)
    if not best or t > best[0][0]:
        best = [rec]; print("new best", rec[:5], A, flush=True)
    elif t == best[0][0]:
        best.append(rec)
print("BEST t =", best[0][0], "number of optimal shapes:", len(best))
json.dump([dict(t=r[0], dimA=r[1], dA=r[2], dimB=r[3], sepB=r[4], A=r[5], B=r[6]) for r in best],
          open("decode_search.json", "w"), indent=0)
