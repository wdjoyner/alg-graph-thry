"""Lattice symmetries of the principal exponent set mod 7, giving permutation and
monomial automorphisms of the [49,11,28]_8 code.  License: MIT."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from toric import lattice_points, residues
m = 7
U = set(residues(lattice_points([(5,-1),(-1,5),(-1,-1)],[0,0,5]), 8))
def act(A, u): return ((A[0]*u[0] + A[1]*u[1]) % m, (A[2]*u[0] + A[3]*u[1]) % m)
exact, affine = [], []
for A in itertools.product(range(m), repeat=4):
    if (A[0]*A[3] - A[1]*A[2]) % m == 0: continue
    img = {act(A, u) for u in U}
    if img == U: exact.append(A)
    for t in itertools.product(range(m), repeat=2):
        if {((a+t[0]) % m, (b+t[1]) % m) for a, b in img} == U:
            affine.append((A, t))
print("A in GL_2(Z/7) with A(U) = U:", len(exact), exact)
print("affine maps u -> Au + t with image U:", len(affine))
print("=> |PAut| >= 49 *", len(exact), "=", 49*len(exact), "; monomial automorphisms >= 49 *", len(affine), "=", 49*len(affine))
