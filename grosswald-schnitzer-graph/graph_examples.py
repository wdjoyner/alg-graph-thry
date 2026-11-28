#!/usr/bin/env python3
"""Finite graph-incidence / Euler-factor checks (not an infinite theorem proof)."""
import cmath
import math
from collections import Counter
from itertools import product

def primes(n):
    out=[]
    m=2
    while len(out)<n:
        if all(m%p for p in out if p*p<=m):
            out.append(m)
        m+=1
    return out

def boundary(e):
    return [e[0]]+[e[j]-e[j-1] for j in range(1,len(e))]+[-e[-1]]

def q_direct(e, ps, s):
    ans=1+0j
    for j,bit in enumerate(e):
        if bit:
            ans *= (1-ps[j]**(-s))/(1-ps[j+1]**(-s))
    return ans

def q_boundary(e, ps, s):
    return math.prod((1-ps[j]**(-s))**c for j,c in enumerate(boundary(e)))

def variation(e, ps, delta):
    return sum(abs(c)*ps[j]**(-delta) for j,c in enumerate(boundary(e)))

def count_monoid(generators, max_total_degree):
    counts=Counter()
    for exps in product(range(max_total_degree+1),repeat=len(generators)):
        if sum(exps)<=max_total_degree:
            val=math.prod(a**r for a,r in zip(generators,exps))
            counts[val]+=1
    return counts

def main():
    N=36
    ps=primes(N+1)
    patterns={
        "all moved": [1]*N,
        "alternating": [j%2==0 for j in range(N)],
        "block 3:9": [2<=j<=8 for j in range(N)],
        "isolated": [j in (7,17,31) for j in range(N)],
    }
    s=1.45+0.62j
    for label, bits in patterns.items():
        e=[int(v) for v in bits]
        a=q_direct(e,ps,s)
        b=q_boundary(e,ps,s)
        assert abs(a-b)<1e-9, (label,a,b)
        print(f"{label:12s}  boundary support={sum(bool(c) for c in boundary(e)):2d}"
              f"  V_1/2={variation(e,ps,0.5):.4f}"
              f"  V_1/4={variation(e,ps,0.25):.4f}")
    assert abs(q_direct([1]*N,ps,s)-(1-2**(-s))/(1-ps[N]**(-s)))<1e-9
    assert count_monoid([3,3],2)[9]==3
    # Check the finite Euler product as a weighted exponent-vertex sum.
    gs=[3,5]
    z=2.2+0.3j
    finite=sum((gs[0]**(-z))**a*(gs[1]**(-z))**b
               for a in range(24) for b in range(24))
    exact=1/((1-gs[0]**(-z))*(1-gs[1]**(-z)))
    assert abs(finite-exact)<1e-9
    print("All finite-product, incidence and collision tests passed.")

if __name__=="__main__":
    main()
