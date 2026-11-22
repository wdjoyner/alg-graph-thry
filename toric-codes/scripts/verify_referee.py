"""Independent checks of the claims in the ChatGPT referee report (Level 1).
License: MIT."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from gf import GF
from toric import (lattice_points, residues, toric_code_params, det2,
                   polygon_vertices, area)

def zeros_on_torus(F, f, r=2):
    """f: callable on tuples of field elements; count zeros on (F^*)^r."""
    pts = itertools.product(F.elements_star(), repeat=r)
    return sum(1 for p in pts if f(p) == 0)

print("== 3.1 Conjecture conj:shansen, P^1 x P^1, P_G=[0,1]^2, q=9")
F = GF(9); q = 9; n = (q-1)**2; vol = 1; N = 6
print("hypothesis 2N vol <= n <= 2N^2 vol:", 2*N*vol, "<=", n, "<=", 2*N*N*vol)
a, b = F.exp[1], F.exp[2]
f = lambda p: F.mul(F.sub(p[0], a), F.sub(p[1], b))
z = zeros_on_torus(F, f); print("zeros of (x-a)(y-b):", z, " weight:", n - z, " conjectured d >=", n - 2*N*vol)
print("exact d of the square code:", toric_code_params([(0,0),(1,0),(0,1),(1,1)], 9)[:3])

print("== 3.2 Conjecture conj:main, P^2, P_G=S_1, q=9")
z = zeros_on_torus(F, lambda p: F.sub(p[0], a)); print("zeros of x-a:", z, " weight", n-z, " conjectured d >=", n - 2*3)
print("exact:", toric_code_params([(0,0),(1,0),(0,1)], 9)[:3])

print("== 3.3 Injectivity: x^{q-1}-1 vanishes on torus for every q (shown q=9,11,13)")
for qq in (9, 11, 13):
    FF = GF(qq)
    pw = lambda x, e: FF.exp[(FF.log[x]*e) % (qq-1)]
    print(qq, all(FF.sub(pw(p[0], qq-1), 1) == 0 for p in itertools.product(FF.elements_star(), repeat=2)))

print("== 4.2 Theorem thrm:subcode2 item (5), r=3, q=5, a=1")
F5 = GF(5); q = 5
claimed = (q-1)*q**2 - 3*(q-1)**2 - 1
z = sum(1 for p in itertools.product(F5.elements_star(), repeat=3) if F5.sub(p[0], 1) == 0)
print("claimed lower bound", claimed, " weight of x1-1:", 64 - z)
print("exact d of C_{S_1} in dim 3, q=5:", toric_code_params([(0,0,0),(1,0,0),(0,1,0),(0,0,1)], 5, r=3)[:3])

print("== 4.2 item (1): P_G=[0,1]^2 contains S_1; dims on torus q=5")
print("dim C_{S_1} =", len(residues([(0,0),(1,0),(0,1)],5)), " dim C_square =", len(residues([(0,0),(1,0),(0,1),(1,1)],5)))

print("== 4.3 Upper bound theorem: h must be <= q-2 (h = q-1 gives the zero word)")
F7 = GF(7)
prod_all = lambda p: 0 if True else 1
z = sum(1 for p in itertools.product(F7.elements_star(), repeat=2)
        if all(True for _ in [0]) and __import__('functools').reduce(lambda acc, c: F7.mul(acc, F7.sub(p[0], c)), F7.elements_star(), 1) == 0)
print("prod_{c in F7^*} (x-c) vanishes at", z, "of 36 torus points (so it is the zero codeword)")

print("== Remark after Hansen's theorem: q=9, a=3")
q, a_ = 9, 3
print("d (Hansen b) =", (q-1)**2 - a_*(q-1), "; d_RM - 2q + 1 =", (q-a_)*q - 2*q + 1, "(original text says 10)")

print("== 4.5 Fans: determinants of consecutive rays, relation, surface type")
fans = {
 "fan7 (principal)": [(5,-1),(-1,5),(-1,-1)],
 "fan1": [(2,-1),(-1,2),(-1,-1)],
 "fan5": [(1,0),(-1,1),(-1,-1)],
 "fan5 'refined' (original, v4=-e2)": [(1,0),(-1,1),(-1,-1),(0,-1)],
 "fan5 corrected refinement (v4=-e1)": [(1,0),(-1,1),(-1,0),(-1,-1)],
 "fan4": [(1,0),(0,1),(-1,-1)],
 "fan3": [(1,0),(0,1),(-1,0),(0,-1)],
 "fan2 m=3": [(1,0),(-1,3),(0,-1)],
 "fan2' m=3": [(1,0),(0,1),(-1,3),(0,-1)],
 "fan6": [(2,-1),(-1,1),(-1,0)],
}
import math
for name, rays in fans.items():
    rays = sorted(rays, key=lambda v: math.atan2(v[1], v[0]))
    s = len(rays)
    dets = [det2(rays[i], rays[(i+1) % s]) for i in range(s)]
    line = f"{name}: rays {rays} dets {dets}"
    if all(d == 1 for d in dets):
        # self-intersections: v_{i-1}+v_{i+1} = a_i v_i, D_i^2 = -a_i
        avals = []
        for i in range(s):
            u = (rays[i-1][0]+rays[(i+1)%s][0], rays[i-1][1]+rays[(i+1)%s][1])
            v = rays[i]
            ai = u[0]//v[0] if v[0] else u[1]//v[1]
            assert (u[0], u[1]) == (ai*v[0], ai*v[1])
            avals.append(ai)
        line += f" smooth; D_i^2 = {[-x for x in avals]}, sum a_i = {sum(avals)} (3s-12 = {3*s-12})"
    else:
        line += " singular"
    print(line)

print("== 4.5 fan5 divisor (0,0,a) with original refinement d4=2a: lattice points for a=1")
print(lattice_points([(1,0),(-1,1),(-1,-1),(0,-1)], [0,0,1,2]))
print("Hansen (a) triangle a=1 needs:", lattice_points([(1,0),(-1,1),(-1,-1)], [0,0,2]))
print("corrected: G = 2a D3 + a D4 on rays (1,0),(-1,1),(-1,-1),(-1,0), a=2:",
      sorted(lattice_points([(1,0),(-1,1),(-1,-1),(-1,0)], [0,0,4,2])) == sorted(
      [(i,j) for i in range(3) for j in range(5) if i <= j <= 4-i]))

print("== 4.5 fan6 area: vertices and area vs formulas")
for d in [(1,1,3),(0,0,2),(2,1,4),(4,1,1)]:
    V = polygon_vertices([(2,-1),(-1,1),(-1,0)], list(d))
    A = area(V); s = sum(d)
    orig = Fraction(1,2)*(2*d[0]+d[2])*(d[2]-d[0]-d[1])
    print(d, "vertices", [(str(x),str(y)) for x,y in V], "area", A, " (d1+d2+d3)^2/2 =", Fraction(s*s,2), " original formula", orig)
print("fan6 polygon is lattice-equivalent to S_s, s=d1+d2+d3: check (1,1,3)",
      len(lattice_points([(2,-1),(-1,1),(-1,0)],[1,1,3])), "points vs", (5+1)*(5+2)//2)

print("== principal example polygon")
U = lattice_points([(5,-1),(-1,5),(-1,-1)], [0,0,5])
print("points:", U, " count", len(U))
print("rational vertices:", [(str(x),str(y)) for x,y in polygon_vertices([(5,-1),(-1,5),(-1,-1)],[0,0,5])])
print("area of conv{(0,0),(4,1),(1,4)} =", area([(0,0),(4,1),(1,4)]))

print("== 4.6 duplicated row fan1 (5;2,3,3)")
U = lattice_points([(2,-1),(-1,2),(-1,-1)], [2,3,3])
from collections import Counter
c = Counter(tuple(x % 4 for x in u) for u in U)
print(len(U), "lattice points,", len(c), "classes; collisions:", [ [u for u in U if tuple(x%4 for x in u)==k] for k,v in c.items() if v>1])

print("== Example fan2: Cartier condition and F_m ampleness (edge lengths)")
m = 3
for d in [(0,0,1,1),(0,1,2,1),(0,0,0,1),(1,1,1,0)]:
    V = polygon_vertices([(1,0),(0,1),(-1,m),(0,-1)], list(d))
    print("F_3 offsets", d, "vertices", [(str(x),str(y)) for x,y in V], " test d2+d4>0 and d1+d3>m*d2:", d[1]+d[3]>0 and d[0]+d[2]>m*d[1])
