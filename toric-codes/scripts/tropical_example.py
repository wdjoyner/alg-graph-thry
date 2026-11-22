"""Tropical curve of f = sum_{u in [0,2]^2} t^{h(u)} x^u, h(i,j) = i^2 + i*j + j^2,
over a valued field (min convention), and the projection (w1,w2) -> w1.

Computes the dual subdivision, the vertices, bounded edges and ends of the
tropical curve, checks balancing, builds a finite model G -> T of the
projection, checks the Baker-Norine harmonicity condition and the
Riemann-Hurwitz formula, and writes TikZ code for the figure.
License: MIT."""
import itertools
from fractions import Fraction as Fr

PTS = [(i, j) for i in range(3) for j in range(3)]
h = {u: u[0]**2 + u[0]*u[1] + u[1]**2 for u in PTS}

def F_terms(w):
    vals = {u: h[u] + u[0]*w[0] + u[1]*w[1] for u in PTS}
    m = min(vals.values())
    return m, [u for u in PTS if vals[u] == m]

# vertices: points where >= 3 non-collinear terms tie and they are minimal
verts = {}
for a, b, c in itertools.combinations(PTS, 3):
    det = (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
    if det == 0: continue
    # solve h(a)+a.w = h(b)+b.w = h(c)+c.w
    A = [[b[0]-a[0], b[1]-a[1]], [c[0]-a[0], c[1]-a[1]]]
    r = [h[a]-h[b], h[a]-h[c]]
    D = Fr(A[0][0]*A[1][1]-A[0][1]*A[1][0])
    w = (Fr(r[0]*A[1][1]-A[0][1]*r[1])/D, Fr(A[0][0]*r[1]-r[0]*A[1][0])/D)
    m, ties = F_terms(w)
    if a in ties and b in ties and c in ties:
        verts[w] = tuple(sorted(ties))
cells = sorted(set(verts.values()))
print("vertices (with dual cells):")
for w, cell in sorted(verts.items()):
    print("  ", (str(w[0]), str(w[1])), cell)
assert all(len(c) == 3 for c in cells), "subdivision is not a triangulation"
# check unimodular
for c in cells:
    a, b, cc = c
    assert abs((b[0]-a[0])*(cc[1]-a[1]) - (b[1]-a[1])*(cc[0]-a[0])) == 1
# edges of the subdivision
def cell_edges(c): return [tuple(sorted(e)) for e in itertools.combinations(c, 2)]
from collections import defaultdict
edge_cells = defaultdict(list)
for w, c in verts.items():
    for e in cell_edges(c): edge_cells[e].append(w)
bounded, ends = [], []
for e, ws in edge_cells.items():
    d = (e[1][0]-e[0][0], e[1][1]-e[0][1])
    perp = (-d[1], d[0])   # primitive since edges are primitive
    if len(ws) == 2:
        bounded.append((ws[0], ws[1], e))
    else:
        w = ws[0]
        # direction of the end: perpendicular to e, pointing away from the third vertex side.
        # Determine by testing: along w + s*perp for small s>0 the two terms of e stay minimal.
        for sgn in (1, -1):
            p = (w[0] + sgn*perp[0]*Fr(1,100), w[1] + sgn*perp[1]*Fr(1,100))
            m, ties = F_terms(p)
            if set(e) <= set(ties):
                ends.append((w, (sgn*perp[0], sgn*perp[1]), e))
print("bounded edges:", len(bounded), " ends:", len(ends), " vertices:", len(verts))
genus = len(bounded) - len(verts) + 1
print("first Betti number of the tropical curve:", genus, "(interior lattice points of [0,2]^2: 1)")
# balancing at each vertex
for w in verts:
    s = [0, 0]
    for (a, b, e) in bounded:
        if w in (a, b):
            o = b if w == a else a
            d = (o[0]-w[0], o[1]-w[1]); g = max(abs(d[0]), abs(d[1]))
            # primitive direction
            from math import gcd
            gg = gcd(int(d[0]*1000000), int(d[1]*1000000)) or 1
            prim = (int(d[0]*1000000)//gg, int(d[1]*1000000)//gg)
            s[0] += prim[0]; s[1] += prim[1]
    for (a, dvec, e) in ends:
        if a == w: s[0] += dvec[0]; s[1] += dvec[1]
    assert s == [0, 0], (w, s)
print("balancing holds at every vertex")
# projection to w1: dilation |a| of primitive direction (a,b)
def prim(d):
    from math import gcd
    num = [int(x*1000000) for x in d]; g = gcd(abs(num[0]), abs(num[1]))
    return (num[0]//g, num[1]//g)
dil = []
for (a, b, e) in bounded:
    p = prim((b[0]-a[0], b[1]-a[1])); dil.append(abs(p[0]))
print("dilation factors of bounded edges:", sorted(dil), "; of ends:", sorted(abs(d[0]) for _, d, _ in ends))
left = sum(abs(d[0]) for _, d, _ in ends if d[0] < 0)
right = sum(d[0] for _, d, _ in ends if d[0] > 0)
print("degree from the left ends:", left, " from the right ends:", right, " (vertical extent of the square: 2)")

# ---- finite model: subdivide at x-coordinates of vertices, truncate horizontal ends, drop vertical ends
xs = sorted(set(w[0] for w in verts))
xmin, xmax = xs[0] - 1, xs[-1] + 1
Tx = [xmin] + xs + [xmax]
Gv = set(verts)
Ge = []   # edges as (p, q)
def add_path(p, q):
    if p[0] == q[0]:
        Ge.append((p, q)); return
    lo, hi = sorted([p, q])
    cuts = [x for x in Tx if lo[0] < x < hi[0]]
    pts = [lo]
    for x in cuts:
        t = (x - lo[0]) / (hi[0] - lo[0])
        pts.append((x, lo[1] + t*(hi[1]-lo[1])))
    pts.append(hi)
    for u, v in zip(pts, pts[1:]):
        Gv.add(u); Gv.add(v); Ge.append((u, v))
for (a, b, e) in bounded: add_path(a, b)
dropped = 0
for (a, d, e) in ends:
    if d[0] == 0:
        dropped += 1; continue
    x = xmin if d[0] < 0 else xmax
    t = (x - a[0]) / d[0]
    add_path(a, (x, a[1] + t*d[1]))
phi = {v: v[0] for v in Gv}
Te = list(zip(Tx, Tx[1:]))
def image(e):
    a, b = e
    if a[0] == b[0]: return None
    return tuple(sorted([a[0], b[0]]))
ok = True; mult = {}; vert_count = {}
for v in Gv:
    y = phi[v]
    inc = [e for e in Ge if v in e]
    vert_count[v] = sum(1 for e in inc if image(e) is None)
    counts = [sum(1 for e in inc if image(e) == te) for te in Te if y in te]
    if len(set(counts)) != 1: ok = False; print("not harmonic at", v, counts)
    mult[v] = counts[0]
print("finite model: |V(G)| =", len(Gv), " |E(G)| =", len(Ge), " |V(T)| =", len(Tx), " vertical ends dropped:", dropped)
print("Baker-Norine harmonic:", ok)
deg = sum(1 for e in Ge if image(e) == Te[0])
gG = len(Ge) - len(Gv) + 1
rh = sum(2*(mult[v]-1) + vert_count[v] for v in Gv)
print("degree:", deg, " genus(G):", gG, " genus(T): 0")
print("Riemann-Hurwitz: 2g(G)-2 =", 2*gG-2, " ; deg*(2g(T)-2) + sum[2(m-1)+v] =", deg*(-2) + rh)
print("vertices with m(x)=2 or vertical edges:")
for v in sorted(Gv):
    if mult[v] != 1 or vert_count[v]:
        print("   ", (str(v[0]), str(v[1])), "m =", mult[v], " vertical =", vert_count[v])

# ---- TikZ
def c(p): return f"({float(p[0]):.3f},{float(p[1]):.3f})"
lines = []
for (a, b, e) in bounded: lines.append(f"\\draw[thick] {c(a)} -- {c(b)};")
for (a, d, e) in ends:
    L = Fr(3, 2)
    b = (a[0] + L*d[0], a[1] + L*d[1])
    style = "thick,dashed" if d[0] == 0 else "thick"
    lines.append(f"\\draw[{style},->] {c(a)} -- {c(b)};")
for w in verts: lines.append(f"\\fill {c(w)} circle (1.6pt);")
open("tropical_example_tikz.tex", "w").write("\n".join(lines) + "\n")
print("x-coordinates of T-vertices:", [str(x) for x in Tx])
