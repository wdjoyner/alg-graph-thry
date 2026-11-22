"""Check Hansen's Theorem (types (a)-(d)) against exact computation for small q,
and the Alon-Furedi/footprint formulas used in the revised paper.  License: MIT."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from toric import toric_code_params
def pts_a(a): return [(i,j) for i in range(a+1) for j in range(2*a+1) if i <= j <= 2*a-i]
def pts_b(a): return [(i,j) for i in range(a+1) for j in range(a+1) if i+j <= a]
def pts_c(a,b): return [(i,j) for i in range(a+1) for j in range(b+1)]
def pts_d(a,b,m): return [(i,j) for i in range(a+1) for j in range(b+a*m+1) if j <= b + m*i]
bad = 0
for q in (5, 7, 8, 9):
    n = (q-1)**2
    for a in range(1, q):
        if q > 2*a+1:
            r = toric_code_params(pts_a(a), q); exp = (n, (a+1)**2, n-2*a*(q-1))
            print("(a)", q, a, r[:3], exp, r[:3]==exp); bad += r[:3]!=exp
        if q > a+1:
            r = toric_code_params(pts_b(a), q); exp = (n, (a+1)*(a+2)//2, n-a*(q-1))
            print("(b)", q, a, r[:3], exp, r[:3]==exp); bad += r[:3]!=exp
        for b in range(1, q):
            if q > max(a,b)+1 and a <= b and (a+1)*(b+1) <= 20:
                r = toric_code_params(pts_c(a,b), q); exp = (n, (a+1)*(b+1), (q-1-a)*(q-1-b))
                print("(c)", q, a, b, r[:3], exp, r[:3]==exp); bad += r[:3]!=exp
            for m in range(1, 4):
                if q > max(a, b, b+a*m)+1 and len(pts_d(a,b,m)) <= 16:
                    r = toric_code_params(pts_d(a,b,m), q)
                    exp = (n, (a+1)*(b+1)+m*a*(a+1)//2, min((q-a-1)*(q-b-1), (q-1)*(q-b-a*m-1)))
                    print("(d)", q, a, b, m, r[:3], exp, r[:3]==exp); bad += r[:3]!=exp
print("mismatches:", bad)
