#!/usr/bin/env python3
"""Exact checks supporting the referee report on toric-repns.tex (Draft 3).

Requires Python 3 and sympy (exact rational arithmetic); no floating point.
Run: python3 referee_checks.py
"""
from itertools import combinations
import sympy as sp

V = [(2, -1), (-1, 2), (-1, -1)]


def hilbert_basis(a, b, box=4):
    """Irreducible lattice points of the dual cone {u : <u,a> >= 0, <u,b> >= 0}."""
    pts = [(x, y) for x in range(-box, box + 1) for y in range(-box, box + 1)
           if (x, y) != (0, 0) and x*a[0] + y*a[1] >= 0 and x*b[0] + y*b[1] >= 0]
    S = set(pts)
    return sorted(p for p in pts
                  if not any((p[0]-q[0], p[1]-q[1]) in S for q in pts))


def check_charts():
    hb = {name: hilbert_basis(V[i], V[j])
          for name, (i, j) in {'sigma1': (0, 1), 'sigma2': (1, 2), 'sigma3': (2, 0)}.items()}
    assert hb['sigma1'] == [(1, 1), (1, 2), (2, 1)]
    assert hb['sigma2'] == [(-2, -1), (-1, 0), (-1, 1)]
    assert hb['sigma3'] == [(-1, -2), (0, -1), (1, -1)]
    # Paper's listed order on U_sigma3: z1=(0,-1), z2=(-1,-2), z3=(1,-1).
    z1, z2, z3 = (0, -1), (-1, -2), (1, -1)
    assert tuple(3*c for c in z2) != tuple(a+b for a, b in zip(z1, z3))  # z2^3 = z1 z3 fails
    assert tuple(3*c for c in z1) == tuple(a+b for a, b in zip(z2, z3))  # z1^3 = z2 z3 holds
    print("charts: Hilbert bases OK; with the listed order on U_sigma3 the relation is z1^3 = z2 z3")


def points(q, d):
    a1, a2, a3 = d
    R = range(-10*q - 3, 10*q + 4)
    return sorted((x, y) for x in R for y in R
                  if 2*x - y >= -a1*q and -x + 2*y >= -a2*q and -x - y >= -a3*q)


def check_cartier():
    def cartier(d):
        for i, j in ((0, 1), (1, 2), (2, 0)):
            a, b = V[i], V[j]
            det = a[0]*b[1] - a[1]*b[0]
            # solve <m,a> = -d_i, <m,b> = -d_j
            mx = sp.Rational(-d[i]*b[1] + d[j]*a[1], det)
            my = sp.Rational(-d[j]*a[0] + d[i]*b[0], det)
            if not (mx.is_integer and my.is_integer):
                return False
        return True
    for d in [(a, b, c) for a in range(-4, 5) for b in range(-4, 5) for c in range(-4, 5)]:
        assert cartier(d) == (d[0] % 3 == d[1] % 3 == d[2] % 3), d
    assert cartier((6, 6, 0)) and not cartier((2, 2, 0))
    print("Cartier criterion d1=d2=d3 mod 3 OK on [-4,4]^3; 6D1+6D2 Cartier, 2D1+2D2 not")


def check_non_cartier():
    for q in range(31):
        S = points(q, (2, 2, 0))
        f = sum(1 for u in S if u[0] == u[1])
        num = 8*q*q + 6*q + (3 if q % 3 == 0 else 1)
        assert num % 3 == 0 and len(S) == num // 3, (q, len(S))
        assert f == 2*q + 1
    print("D'=2D1+2D2: dim L(qD') = (8q^2+6q+1)/3 + (2/3)[3|q], trace 2q+1, q=0..30 OK")


def check_king_graph():
    S = points(1, (6, 6, 0))
    idx = {u: i for i, u in enumerate(S)}
    A = sp.zeros(31, 31)
    for u in S:
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                w = (u[0]+a, u[1]+b)
                if (a or b) and w in idx:
                    A[idx[u], idx[w]] = 1
    assert sum(A) == 2*85
    even, odd, seen = [], [], set()
    for u in S:
        if u in seen:
            continue
        g = (u[1], u[0]); seen |= {u, g}
        even.append({u: 1} if g == u else {u: 1, g: 1})
        if g != u:
            odd.append({u: 1, g: -1})
    x = sp.symbols('x')
    polys = []
    for vs in (even, odd):
        B = sp.zeros(31, len(vs))
        for j, v in enumerate(vs):
            for u, c in v.items():
                B[idx[u], j] = c
        M = (B.T*B).inv()*B.T*A*B
        p = sp.Poly(M.charpoly(x).as_expr(), x)
        assert sp.degree(sp.gcd(p, p.diff(x)), x) == 0  # squarefree
        polys.append(p)
    assert sp.degree(sp.gcd(*polys), x) == 0
    print("eight-neighbor graph: 85 edges; char. polys of even (19) and odd (12) blocks "
          "squarefree and coprime => 31 simple eigenvalues")


def check_p1p1():
    h = lambda a, b, q: (a*q + 1)*(b*q + 1)
    assert h(1, 5, 1) == h(2, 3, 1) == 12
    assert h(1, 5, 2) == 33 and h(2, 3, 2) == 35
    assert all(h(1, 2, q) == h(2, 1, q) for q in range(50))
    print("P1xP1: (1,5),(2,3) agree only at q=1 (33 vs 35 at q=2); (1,2),(2,1) agree for all q")


def check_johnson_lattice_graph():
    for n in range(4, 9):
        E = list(combinations(range(n), 2))
        vec = lambda e: tuple(int(i in e) for i in range(n))
        roots = {tuple((k == i) - (k == j) for k in range(n))
                 for i in range(n) for j in range(n) if i != j}
        assert all((tuple(a - b for a, b in zip(vec(e), vec(f))) in roots)
                   == (len(set(e) & set(f)) == 1) for e in E for f in E if e != f)
        # S_n-fixed point of the affine span sum x_i = 2 is (2/n,...,2/n): not integral
        assert 2 % n != 0
        # graphic zonotope of K_n: constant fixed point integral iff n odd
        assert (n*(n-1)//2 % n == 0) == (n % 2 == 1)
    print("J(n,2) = lattice-point graph for B = {e_i - e_j}, n=4..8; no S_n-fixed lattice point "
          "in aff Delta(2,n); K_n zonotope has one iff n odd")


if __name__ == '__main__':
    check_charts()
    check_cartier()
    check_non_cartier()
    check_king_graph()
    check_p1p1()
    check_johnson_lattice_graph()
    print("ALL REFEREE CHECKS PASSED")
