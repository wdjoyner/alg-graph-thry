"""Independent verification of the three generator pairs printed in the 1997 manuscript.
Requires sympy. 1-based cycle notation from transtvy2(1).tex.
"""
from math import prod
from sympy.combinatorics import Permutation, PermutationGroup

def perm(n, *cycles):
    result = list(range(n))
    for cyc in cycles:
        for a,b in zip(cyc,cyc[1:]+cyc[:1]):
            result[a-1]=b-1
    return Permutation(result)

CASES = [
 (10,3,720, [((2,6,10,7),(3,9,4,5)), ((1,5),(3,8),(4,10),(7,9))]),
 (11,4,7920, [((1,2,3,4,5,6,7,8,9,10,11),), ((3,7,11,8),(4,10,5,6))]),
 (12,5,95040, [((2,3,5,9,8,10,6,11,4,7,12),), ((1,12),(2,11),(3,10),(4,9),(5,8),(6,7))]),
]
for n,k,expected,cycles in CASES:
    G=PermutationGroup(*[perm(n,*cs) for cs in cycles])
    order=G.order()
    orbit=G.orbit(tuple(range(k)),action='tuples')
    target=prod(range(n-k+1,n+1))
    print(f'n={n} k={k} group_order={order} tuple_orbit={len(orbit)} expected={target}')
    assert order==expected==target and len(orbit)==target
print('All three explicit generator checks passed.')
