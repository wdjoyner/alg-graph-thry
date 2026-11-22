"""Toric surface codes on the full torus T(F_q) = (F_q^*)^r.

The code C_U attached to a finite set U of exponent vectors is spanned by the
evaluation vectors (t^u)_{t in T(F_q)}, u in U.  Torus points are written
t = (w^{i_1},...,w^{i_r}) for a fixed primitive element w, so the entry of the
row for u at point i is w^{<u,i>}.

License: MIT.
"""
import itertools
import os
import subprocess
from fractions import Fraction

from gf import GF, rank_and_rref

HERE = os.path.dirname(os.path.abspath(__file__))
MINDIST = os.path.join(HERE, "mindist")


def lattice_points(normals, offsets, box=60):
    """Integer points u with <u, v_i> >= -d_i for all i (2-dimensional)."""
    pts = []
    for x in range(-box, box + 1):
        for y in range(-box, box + 1):
            if all(v[0] * x + v[1] * y >= -d for v, d in zip(normals, offsets)):
                pts.append((x, y))
    return pts


def residues(U, q):
    return sorted({tuple(c % (q - 1) for c in u) for u in U})


def torus_points(q, r=2):
    return list(itertools.product(range(q - 1), repeat=r))


def gen_matrix(U, q, r=2, F=None, points=None):
    F = F or GF(q)
    pts = points or torus_points(q, r)
    rows = []
    for u in U:
        rows.append([F.pow_gen(sum(a * b for a, b in zip(u, i))) for i in pts])
    return rows


def run_mindist(rows, q, mode="bz", F=None):
    F = F or GF(q)
    n = len(rows[0])
    k = len(rows)
    lines = [f"{mode} {q} {n} {k}"]
    for a in range(q):
        lines.append(" ".join(str(F.add(a, b)) for b in range(q)))
    for a in range(q):
        lines.append(" ".join(str(F.mul(a, b)) for b in range(q)))
    for r in rows:
        lines.append(" ".join(map(str, r)))
    out = subprocess.run([MINDIST], input="\n".join(lines) + "\n",
                         capture_output=True, text=True, check=True).stdout
    res = {}
    for line in out.splitlines():
        parts = line.split()
        if parts[0] == "dimension":
            res["k"] = int(parts[1])
        elif parts[0] == "mindist":
            res["d"] = int(parts[1])
        elif parts[0] == "infosets":
            res["infosets"] = int(parts[1])
        elif parts[0] == "witness":
            res["witness"] = list(map(int, parts[1:]))
        elif parts[0] == "weightdist":
            res["wd"] = {int(a): int(b) for a, b in (p.split(":") for p in parts[1:])}
    return res


def toric_code_params(U, q, r=2):
    """Return (n, k, d, witness) for the full-torus code C_U, exactly."""
    F = GF(q)
    R = residues(U, q)
    rows = gen_matrix(R, q, r, F)
    res = run_mindist(rows, q, "bz", F)
    n = (q - 1) ** r
    assert res["k"] == len(R), (res["k"], len(R))
    return n, res["k"], res["d"], res.get("witness")


def det2(a, b):
    return a[0] * b[1] - a[1] * b[0]


def polygon_vertices(normals, offsets):
    """Vertices of {u : <u,v_i> >= -d_i} (rational), in counterclockwise order."""
    verts = set()
    m = len(normals)
    for i in range(m):
        for j in range(i + 1, m):
            a, b = normals[i], normals[j]
            D = det2(a, b)
            if D == 0:
                continue
            # solve a.u = -d_i, b.u = -d_j
            x = Fraction(-offsets[i] * b[1] + offsets[j] * a[1], D)
            y = Fraction(-a[0] * offsets[j] + b[0] * offsets[i], D)
            if all(v[0] * x + v[1] * y >= -d for v, d in zip(normals, offsets)):
                verts.add((x, y))
    verts = list(verts)
    if len(verts) < 3:
        return verts
    cx = sum(v[0] for v in verts) / len(verts)
    cy = sum(v[1] for v in verts) / len(verts)
    import math
    verts.sort(key=lambda v: math.atan2(float(v[1] - cy), float(v[0] - cx)))
    return verts


def area(verts):
    s = Fraction(0)
    for i in range(len(verts)):
        a, b = verts[i], verts[(i + 1) % len(verts)]
        s += a[0] * b[1] - a[1] * b[0]
    return abs(s) / 2
