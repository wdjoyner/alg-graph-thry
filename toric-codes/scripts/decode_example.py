"""Error-locator decoding of the [49,11,28]_8 toric code C_Q (Q = 11-point triangle).

D = C_Q = C_P^perp with P = complement of -Q mod 7 (duality theorem).
Error-correcting pair: A = S_2 (6 monomials), B = (1,1) + S_4 (15 monomials),
A + B = (1,1) + S_6, a subset of P.  Guaranteed radius t = 5.
License: MIT."""
import sys, os, random, itertools, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gf import GF, solve_linear, nullspace
from toric import lattice_points, residues, gen_matrix, torus_points

q = 8; m = 7; n = 49
F = GF(q)
Q = residues(lattice_points([(5,-1),(-1,5),(-1,-1)],[0,0,5]), q)
ALL = [(i, j) for i in range(m) for j in range(m)]
negQ = {((-a) % m, (-b) % m) for a, b in Q}
P = sorted(set(ALL) - negQ)
A = [(i, j) for i in range(3) for j in range(3 - i)]
B = [(1 + i, 1 + j) for i in range(5) for j in range(5 - i)]
assert all(((a[0]+b[0]) % m, (a[1]+b[1]) % m) in P for a in A for b in B)
pts = torus_points(q)                       # (i,j) <-> (w^i, w^j)
def ev(u, k): return F.pow_gen(u[0]*pts[k][0] + u[1]*pts[k][1])
GQ = gen_matrix(Q, q, 2, F)
# sanity: every row of G_Q is orthogonal to every x^w, w in P
for row in GQ:
    for w in P:
        s = 0
        for k in range(n): s = F.add(s, F.mul(row[k], ev(w, k)))
        assert s == 0

def syndrome(r, w):
    s = 0
    for k in range(n): s = F.add(s, F.mul(r[k], ev((w[0] % m, w[1] % m), k)))
    return s

def decode(r, verbose=False):
    syn = {w: syndrome(r, w) for w in P}
    # key equations: sum_a alpha_a [r, x^{a+b}] = 0 for all b in B
    K = [[syn[((a[0]+b[0]) % m, (a[1]+b[1]) % m)] for a in A] for b in B]
    null = nullspace(F, K, len(A))
    if not null: return None, None
    alpha = null[0]
    loc = [0]*n
    for k in range(n):
        s = 0
        for c, a in zip(alpha, A): s = F.add(s, F.mul(c, ev(a, k)))
        loc[k] = s
    N = [k for k in range(n) if loc[k] == 0]
    # error values: sum_{k in N} y_k x^w(p_k) = [r, x^w], w in P
    M = [[ev(w, k) for k in N] for w in P]
    y, nl = solve_linear(F, M, [syn[w] for w in P])
    if y is None or nl: return None, None
    e = [0]*n
    for k, val in zip(N, y): e[k] = val
    c = [F.sub(a, b) for a, b in zip(r, e)]
    info = dict(K=K, alpha=alpha, N=N, null_dim=len(null))
    return c, info

def encode(msg):
    c = [0]*n
    for coef, row in zip(msg, GQ):
        c = [F.add(x, F.mul(coef, y)) for x, y in zip(c, row)]
    return c

random.seed(2026)
stats = {}
for t in range(0, 8):
    ok = 0; trials = 300 if t <= 5 else 300
    for _ in range(trials):
        msg = [random.randrange(q) for _ in range(len(Q))]
        c = encode(msg)
        pos = random.sample(range(n), t)
        r = list(c)
        for k in pos: r[k] = F.add(r[k], random.randrange(1, q))
        c2, _ = decode(r)
        ok += (c2 == c)
    stats[t] = (ok, trials); print("errors", t, "decoded correctly", ok, "/", trials, flush=True)

# explicit example for the paper
L = lambda a: "0" if a == 0 else f"w^{F.log[a]}"
f_pts = {(0,0): 1, (1,2): 1}                 # transmitted c = ev(1 + x y^2)
c = [F.add(ev((0,0),k), ev((1,2),k)) for k in range(n)]
err = {pts.index((0,0)): F.exp[0], pts.index((2,5)): F.exp[3], pts.index((3,1)): F.exp[6],
       pts.index((4,4)): F.exp[2], pts.index((6,2)): F.exp[5]}
r = list(c)
for k, v in err.items(): r[k] = F.add(r[k], v)
c2, info = decode(r, verbose=True)
print("explicit example decoded correctly:", c2 == c)
ex = dict(points=pts, c=[F.log[x] if x else None for x in c], r=[F.log[x] if x else None for x in r],
          err={str(pts[k]): F.log[v] for k, v in err.items()},
          K=[[F.log[x] if x else None for x in row] for row in info["K"]],
          alpha=[F.log[x] if x else None for x in info["alpha"]], A=A, B=B,
          N=[pts[k] for k in info["N"]], null_dim=info["null_dim"], stats=stats, P=P)
json.dump(ex, open("decode_example.json", "w"))
print("kernel dimension", info["null_dim"], "alpha (log w)", ex["alpha"])
print("zero set of locator:", ex["N"])
