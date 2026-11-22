"""Recompute (n,k,d) for every table row of toric_code7.tex (full-torus evaluation).

Each row: (label, q, normals, offsets, claimed (n,k,d)).  The exponent set is
the lattice point set of {u : <u,v_i> >= -d_i}.  k is the number of distinct
residues mod q-1 (the rank is also checked), d is computed exactly.
License: MIT.
"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from toric import lattice_points, toric_code_params

FAN1 = [(2, -1), (-1, 2), (-1, -1)]
FAN6 = [(2, -1), (-1, 1), (-1, 0)]
FAN4 = [(1, 0), (0, 1), (-1, -1)]          # P^2: Hansen type (b) with d3 = a
def FAN2(m): return [(1, 0), (-1, m), (0, -1)]

rows = []
# Hansen type (b) table (lines 305-320): simplex S_a
for q, a, cl in [(5,2,(16,6,8)),(5,4,(16,13,3)),(5,5,(16,15,2)),(7,2,(36,6,24)),(7,3,(36,10,18)),(8,2,(49,6,35))]:
    rows.append(("Hansen(b)", q, FAN4, (0,0,a), cl))
# Example fan1 table (lines 567-590)
for q,d1,d2,d3,n,k,d in [(5,0,0,3,16,4,10),(5,1,1,2,16,5,8),(5,1,1,3,16,7,6),(5,1,1,4,16,10,4),
    (5,2,3,1,16,9,6),(5,2,3,2,16,12,3),(5,2,3,3,16,14,2),(5,2,3,3,16,15,2),
    (7,1,2,0,36,3,30),(7,1,2,2,36,7,21),(7,1,2,3,36,9,20),(7,3,0,0,36,4,27),
    (8,0,0,3,49,4,40),(8,0,1,2,49,3,42),(8,0,3,3,49,10,28),(8,0,3,4,49,12,26)]:
    rows.append(("fan1", q, FAN1, (d1,d2,d3), (n,k,d)))
# Example fan2 tables (lines 701-724)
for q,d1,d2,d3,n,k,d in [(5,0,2,2,16,11,3),(5,0,2,3,16,15,2),(5,0,4,2,16,14,2),(5,1,0,0,16,2,12),
    (7,0,1,0,36,2,30),(8,1,0,0,49,2,42),(9,0,1,0,64,2,56)]:
    rows.append(("fan2 m=3", q, FAN2(3), (d1,d2,d3), (n,k,d)))
for q,d1,d2,d3,n,k,d in [(5,0,0,3,16,13,2),(5,3,3,2,16,14,2)]:
    rows.append(("fan2 m=5", q, FAN2(5), (d1,d2,d3), (n,k,d)))
# Example fan6 table (lines 761-788)
for q,d1,d2,d3,n,k,d in [(5,0,0,1,16,3,12),(5,0,0,2,16,6,8),(5,0,0,3,16,10,4),(5,0,0,4,16,13,3),
    (7,0,0,1,36,3,30),(7,0,0,2,36,6,24),(7,0,0,3,36,10,18),(7,0,0,4,36,15,12),
    (7,4,1,1,36,26,5),(7,4,1,2,36,30,4),(7,4,1,3,36,33,3),(7,4,1,4,36,35,2),
    (8,0,0,1,49,3,42),(8,0,0,2,49,6,35),(8,0,0,3,49,10,28),(8,0,0,4,49,15,21),
    (8,0,4,4,49,39,5),(8,2,4,4,49,46,3),(8,3,4,4,49,48,2),(8,4,1,4,49,43,4),
    (9,0,0,1,64,3,56),(9,0,0,2,64,6,48),(9,0,0,3,64,10,40)]:
    rows.append(("fan6", q, FAN6, (d1,d2,d3), (n,k,d)))
# Principal example (lines 465-481)
rows.append(("fan7 (principal)", 8, [(5,-1),(-1,5),(-1,-1)], (0,0,5), (49,11,28)))

out = []
for lab, q, nv, off, cl in rows:
    U = lattice_points(nv, off)
    t = time.time()
    n, k, d, w = toric_code_params(U, q)
    rec = dict(label=lab, q=q, offsets=off, npts=len(U), claimed=cl, computed=(n, k, d),
               match=(tuple(cl) == (n, k, d)), seconds=round(time.time()-t, 1))
    out.append(rec)
    print(json.dumps(rec), flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_tables.json"), "w"), indent=1)
print("DONE")
