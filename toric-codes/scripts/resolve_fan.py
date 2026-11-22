"""Minimal smooth refinement of a complete 2-dimensional fan, and the weighted
cycle graph of the resulting smooth toric surface (self-intersections D_i^2 = -a_i,
where v_{i-1} + v_{i+1} = a_i v_i).  License: MIT."""
import math, sys
from math import gcd

def cone_resolution(v, w, box=40):
    """Lattice points on the compact boundary of conv((cone(v,w) cap Z^2) minus 0),
    ordered from v to w.  For a 2-dimensional cone these are exactly the rays of
    the minimal resolution (Hirzebruch-Jung)."""
    det = v[0]*w[1] - v[1]*w[0]
    assert det > 0
    pts = [(x, y) for x in range(-box, box+1) for y in range(-box, box+1)
           if (x, y) != (0, 0) and v[0]*y - v[1]*x >= 0 and x*w[1] - y*w[0] >= 0]
    # walk: from current ray c, the next ray is the lattice point p in the cone with
    # det(c, p) = 1 that is "closest" to c in angle (smallest angle beyond c)
    rays = [v]; c = v
    while c != w:
        cand = [p for p in pts if c[0]*p[1] - c[1]*p[0] == 1]
        if w in pts and c[0]*w[1] - c[1]*w[0] == 1:
            cand.append(w)
        # choose candidate minimizing angle from c
        ang = lambda p: (math.atan2(p[1], p[0]) - math.atan2(c[1], c[0])) % (2*math.pi)
        nxt = max(cand, key=ang)   # the point of the half-line nearest to w
        rays.append(nxt); c = nxt
    return rays

def resolve(rays):
    rays = sorted(rays, key=lambda v: math.atan2(v[1], v[0]))
    out = []
    s = len(rays)
    for i in range(s):
        part = cone_resolution(rays[i], rays[(i+1) % s])
        out += part[:-1]
    return out

def weights(rays):
    s = len(rays); a = []
    for i in range(s):
        u = (rays[i-1][0] + rays[(i+1) % s][0], rays[i-1][1] + rays[(i+1) % s][1])
        v = rays[i]
        ai = u[0] // v[0] if v[0] else u[1] // v[1]
        assert u == (ai*v[0], ai*v[1]), (u, v)
        a.append(ai)
    return a

for name, R in [("normal fan of conv{(0,0),(4,1),(1,4)}", [(4,-1),(-1,4),(-1,-1)]),
                ("fan of the 2004 principal example", [(5,-1),(-1,5),(-1,-1)]),
                ("fan1 (P^2/mu_3)", [(2,-1),(-1,2),(-1,-1)]),
                ("fan5 = P(1,1,2)", [(1,0),(-1,1),(-1,-1)])]:
    sm = resolve(R)
    dets = [sm[i][0]*sm[(i+1)%len(sm)][1]-sm[i][1]*sm[(i+1)%len(sm)][0] for i in range(len(sm))]
    a = weights(sm)
    print(name)
    print("  smooth rays:", sm)
    print("  all dets 1:", all(d == 1 for d in dets), " s =", len(sm))
    print("  self-intersections D_i^2:", [-x for x in a], " sum a_i =", sum(a), " 3s-12 =", 3*len(sm)-12)
