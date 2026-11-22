"""Full weight distribution of the [49,11,28]_8 toric code (independent check of d)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from toric import lattice_points, residues, gen_matrix, run_mindist
from gf import GF
F = GF(8)
U = lattice_points([(5, -1), (-1, 5), (-1, -1)], [0, 0, 5])
rows = gen_matrix(residues(U, 8), 8, 2, F)
res = run_mindist(rows, 8, "wd2", F)
print("k =", res["k"])
print("weight distribution:", res["wd"])
print("total codewords:", sum(res["wd"].values()), "= 8^11 =", 8**11)
print("minimum nonzero weight:", min(w for w in res["wd"] if w > 0))
