"""Write each minimum-weight word of the [49,11,28]_8 code as a polynomial in the
11 monomials, and report the supports of the exceptional words (zero sets in
directions not parallel to an edge of the triangle).  License: MIT."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gf import GF, solve_linear
from toric import lattice_points, residues, gen_matrix, torus_points
q = 8; m = 7; F = GF(q)
U = residues(lattice_points([(5,-1),(-1,5),(-1,-1)],[0,0,5]), q)
G = gen_matrix(U, q, 2, F); pts = torus_points(q)
Zs = json.load(open("minwords_principal.json"))
def key(Z, d):
    a, b = d
    return {(b*pts[i][0] - a*pts[i][1]) % m for i in Z}
for Z in Zs:
    # find coefficient vector c with c.G vanishing on Z (11 unknowns, 21 equations): nullspace dim 1
    A = [[G[u][i] for u in range(len(U))] for i in Z]
    x, null = solve_linear(F, A, [0]*len(A))
    assert len(null) == 1
    supp = [U[u] for u in range(len(U)) if null[0][u]]
    is_edge = any(len(key(Z, d)) == 3 for d in [(1,0),(0,1),(1,1)])
    if not is_edge:
        print("zero-set direction (1,2) or (1,4); polynomial support:", supp)
