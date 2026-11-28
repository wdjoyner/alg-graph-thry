#!/usr/bin/env python3
"""Finite graph calculations; not a proof of infinite theorems."""
from itertools import product
import cmath
from math import prod

def primes(n):
    p=[]
    for x in range(2,300):
        if all(x%q for q in p if q*q<=x): p.append(x)
        if len(p)==n: return p

def graph_boundary(e):
    return [e[0]]+[e[j]-e[j-1] for j in range(1,len(e))]+[-e[-1]]

def verify():
    p=primes(22)
    z=1.7+0.4j
    for e in ([1]*21,[j%2 for j in range(21)],
              [int(4<=j<=11) for j in range(21)]):
        q=prod((1-p[j]**(-z))/(1-p[j+1]**(-z))
               for j,b in enumerate(e) if b)
        r=prod((1-p[j]**(-z))**c
               for j,c in enumerate(graph_boundary(e)))
        assert abs(q-r)<1e-10
    for q in (2,3):
        w=cmath.exp(2j*cmath.pi/q)
        for n in range(4*q):
            assert abs((1-q if n%q==0 else 1)
                       +sum(w**(j*n) for j in range(1,q)))<1e-10
    assert sum(1 for a,b in product(range(3),repeat=2)
               if a+b==2)==3
    print("Graph identities checked for finite examples.")
if __name__=="__main__": verify()
