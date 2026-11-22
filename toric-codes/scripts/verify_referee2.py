"""Independent checks of the second ChatGPT referee report (2026-11-22),
findings M1, M2, M3, M4, M5 and C3. Exact arithmetic only.
License: MIT."""
import itertools, math
from fractions import Fraction as Fr

print("== M1: the triangle of Example 'A projective plane in disguise'")
def tri(d1, d2, d3):
    return [(-d1-d2, -d1-2*d2), (d3, d3-d2), (d3, 2*d3+d1)]
def apply(g, p): return (g[0][0]*p[0]+g[0][1]*p[1], g[1][0]*p[0]+g[1][1]*p[1])
old = ((1, 0), (-1, 1))      # (x,y) -> (x, y-x), the map of Draft 3
new = ((2, -1), (-1, 1))     # (x,y) -> (2x-y, y-x), the referee's map
ok_old = ok_new = True
for d1, d2, d3 in itertools.product(range(-3, 5), repeat=3):
    s = d1 + d2 + d3
    if s <= 0: continue
    S = {(0, 0), (s, 0), (0, s)}
    for g, name in ((old, "old"), (new, "new")):
        img = [apply(g, p) for p in tri(d1, d2, d3)]
        mx, my = min(p[0] for p in img), min(p[1] for p in img)
        is_translate = {(p[0]-mx, p[1]-my) for p in img} == S
        if name == "old": ok_old &= is_translate
        else: ok_new &= is_translate
img = [apply(old, p) for p in tri(1, 1, 3)]
print("old map, (d1,d2,d3)=(1,1,3): image", img, "-> translate of S_s?", ok_old)
img = [apply(new, p) for p in tri(1, 1, 3)]
print("new map, (d1,d2,d3)=(1,1,3): image", img, "-> translate of S_s?", ok_new)
print("det of new map:", new[0][0]*new[1][1]-new[0][1]*new[1][0])

print("== M3: direction of the ends of Trop(1+x+y), min convention")
def trop_ends(terms):
    """terms: dict u -> val(c_u). Returns directions of ends from a far circle."""
    found = set()
    for k in range(360):
        ang = 2*math.pi*k/360
        w = (1000*math.cos(ang), 1000*math.sin(ang))
        vals = sorted((v + u[0]*w[0] + u[1]*w[1], u) for u, v in terms.items())
        if abs(vals[0][0]-vals[1][0]) < 9:   # two terms tie (near a ray)
            a, b = vals[0][1], vals[1][1]
            e = (b[0]-a[0], b[1]-a[1]); g = math.gcd(*e)
            nrm = (-e[1]//g, e[0]//g)
            if nrm[0]*w[0]+nrm[1]*w[1] < 0: nrm = (-nrm[0], -nrm[1])
            found.add((nrm, (a, b)))
    return found
for nrm, edge in sorted(trop_ends({(0, 0): 0, (1, 0): 0, (0, 1): 0})):
    # inward normal of edge of conv{(0,0),(1,0),(0,1)}: points to the third vertex
    third = ({(0, 0), (1, 0), (0, 1)} - set(edge)).pop()
    inward = (third[0]-edge[0][0])*nrm[0] + (third[1]-edge[0][1])*nrm[1] > 0
    print("  ray", nrm, "dual to edge", edge, "inward normal:", inward)

print("== M2: f=(1+x+y)^2; dual edges have lattice length 2, so every ray has weight 2")
# Newton polygon 2*S_1. Projection to w1: with the lattice-length metric the
# slope on the horizontal ray is |a_e| = 1; with the metric length/weight
# (Mikhalkin's parametrized curve) the slope is mu_e*|a_e| = 2.
rays = {(-1, -1): 2, (1, 0): 2, (0, 1): 2}  # min convention: inward normals of 2*S_1
right = sum(m*a for (a, b), m in rays.items() if a > 0)
left = sum(m*-a for (a, b), m in rays.items() if a < 0)
print("  weighted slopes right/left at the vertex:", right, left,
      "; vertical extent of 2*S_1 = 2")
print("  lattice-length slopes right/left:", sum(1 for (a, b) in rays if a > 0),
      sum(1 for (a, b) in rays if a < 0), "(degree 1, not 2)")

print("== M4: [0,2]^2 is Hansen type (c) with a=b=2")
a = b = 2; print("  k=(a+1)(b+1) =", (a+1)*(b+1), "lattice points of [0,2]^2 =", 9,
                 "; d over F_8 =", (7-a)*(7-b))

print("== M5: estimate (i) for P=[0,1]^2 and N = ceil((q-1)/sqrt 2)")
def isqrt_ceil_half(m):  # smallest N with 2N^2 >= m^2
    N = math.isqrt(m*m // 2)
    while 2*N*N < m*m: N += 1
    return N
prime_powers = [q for q in range(3, 2000)
                if len({p for p in range(2, q+1) if q % p == 0 and all(p % r for r in range(2, p))}) == 1]
bad = []
for q in prime_powers:
    n, N = (q-1)**2, isqrt_ceil_half(q-1)
    hyp = N > 1 and 2*N <= n <= 2*N*N
    d = (q-2)**2
    if not (hyp and d < n - 2*N): bad.append(q)
print("  prime powers 3 <= q < 2000 where the family is NOT a counterexample:", bad)
print("  (for q-1 >= 10: N <= (q-1)/sqrt2 + 1 < q - 3/2, so d = n-2(q-1)+1 < n-2N)")

print("== C3: moment checks of Table 'weight distribution'")
A = {0: 1, 28: 833, 29: 2058, 30: 21952, 31: 105644, 32: 412629, 33: 1184036,
     34: 3980515, 35: 11983293, 36: 34115123, 37: 82757668, 38: 181602036,
     39: 361137840, 40: 626918936, 41: 969862341, 42: 1290940427,
     43: 1471503957, 44: 1397799774, 45: 1095370500, 46: 665332878,
     47: 296872674, 48: 84948752, 49: 13080725}
print("  sum A_w = 8^11:", sum(A.values()) == 8**11)
print("  sum w A_w = 49*7*8^10:", sum(w*x for w, x in A.items()) == 49*7*8**10)
print("  sum w(w-1) A_w = 49*48*7^2*8^9:",
      sum(w*(w-1)*x for w, x in A.items()) == 49*48*49*8**9)
print("  7 | A_w for w>0:", all(x % 7 == 0 for w, x in A.items() if w))
