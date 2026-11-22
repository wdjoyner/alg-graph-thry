#!/usr/bin/env python3
"""Exact integer checks for toric-repns.tex (stdlib only).

Validates worked examples; the manuscript supplies the mathematical proofs.
Run: python3 verify_examples.py
"""
from itertools import combinations
from math import comb


def surface_points(q):
    """P_{qD} for v1=(2,-1), v2=(-1,2), v3=(-1,-1), D=(6,6,0)."""
    return {(x, y) for x in range(-6*q, 2*q + 1)
                     for y in range(-6*q, 2*q + 1)
                     if 2*x-y >= -6*q and -x+2*y >= -6*q and x+y <= 0}


def graph_edges(S):
    """Undirected eight-neighbor lattice graph, without loops."""
    B = {(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b}
    return {tuple(sorted((u, (u[0]+a, u[1]+b))))
            for u in S for a, b in B if (u[0]+a, u[1]+b) in S}


def verify_surface():
    for q in range(0, 13):
        S = surface_points(q)
        f = {u for u in S if u[0] == u[1]}
        assert len(S) == 24*q*q+6*q+1, (q, len(S))
        assert len(f) == 6*q+1, (q, len(f))
        assert (len(S)+len(f))//2 == 12*q*q+6*q+1
        assert (len(S)-len(f))//2 == 12*q*q
    S = surface_points(1)
    E = graph_edges(S)
    assert len(S) == 31
    assert len(E) == 85, len(E)
    swap = lambda u: (u[1], u[0])
    exchange_edges = {e for e in E if e[0] == swap(e[1])}
    assert len(exchange_edges) == 5
    twisted_A = sum(1 for u in S if tuple(sorted((u, swap(u)))) in E)
    assert twisted_A == 10
    seen, todo = set(), [next(iter(S))]
    while todo:
        u = todo.pop()
        if u in seen:
            continue
        seen.add(u)
        todo.extend(v if u == w else w for v, w in E if u == v or u == w)
    assert len(seen) == 31
    print("C2 toric surface: q=0..12 Ehrhart/fixed counts OK; q=1: V=31 E=85, connected, twisted trace=10")


def verify_k3():
    for q in range(0, 13):
        S = {(x,y,-x-y) for x in range(-q,q+1) for y in range(-q,q+1)
             if abs(x+y) <= q}
        dim = 3*q*q+3*q+1
        trans = sum(1 for x,y,z in S if x == y)
        cycle = sum(1 for x,y,z in S if x == y == z)
        assert (len(S),trans,cycle) == (dim, 2*(q//2)+1, 1)
        triv = (dim+3*trans+2*cycle)//6
        sign = (dim-3*trans+2*cycle)//6
        std = (dim-cycle)//3
        assert triv == q*(q+1)//2+q//2+1
        assert sign == q*(q+1)//2-q//2
        assert std == q*(q+1)
        assert triv+sign+2*std == dim
    print("K3 graphic zonotope/S3: q=0..12 character and multiplicity formulas OK")


def verify_johnson():
    for n in range(4, 13):
        edges = list(combinations(range(n), 2))
        m = len(edges)
        deg = 2*(n-2)
        adj = [[int(len(set(a) & set(b)) == 1) for b in edges] for a in edges]
        assert all(sum(row) == deg for row in adj)
        # R^T R = A+2I exactly, and RR^T=(n-2)I+J.
        R = [[int(v in e) for e in edges] for v in range(n)]
        for i in range(m):
            for j in range(m):
                inner = sum(R[v][i]*R[v][j] for v in range(n))
                assert inner == adj[i][j] + (2 if i == j else 0)
        for i in range(n):
            for j in range(n):
                inner = sum(R[i][e]*R[j][e] for e in range(m))
                assert inner == (n-2 if i == j else 0) + 1
        assert 1+(n-1)+n*(n-3)//2 == m
    print("Johnson graphs J(n,2): n=4..12 exact incidence-matrix identities and multiplicities OK")


if __name__ == '__main__':
    verify_surface()
    verify_k3()
    verify_johnson()
    print("ALL EXACT CHECKS PASSED")
