"""Draw the figures of the harmonic-quotient paper in TikZ, inside the .tex.

Usage (from this folder):
    python3 make_figures.py [--only STEM,STEM,...] [--tex FILE]

Each figure of the paper shows Gamma_2 above Gamma_1.  For each selected
figure (default: all) this script replaces its two drawings, whether they are
still \\includegraphics of a PNG or blocks written by an earlier run, by
    % BEGIN make_figures.py G2 box=5x5cm was=graphics/foo.png
    \\begin{tikzpicture} ... \\end{tikzpicture}%
    % END make_figures.py G2
and the same for G1.  Vertex x of Gamma_2 is filled with color hq<phi(x)>
and vertex y of Gamma_1 with hq<y>, so a vertex of Gamma_1 and its fiber
have the same color.  The colors and node styles go in the preamble, between
"% BEGIN make_figures.py styles" and "% END make_figures.py styles".
Nothing else in the .tex is changed.  Edit the layouts here, not in the .tex:
the next run overwrites every block.

Gamma_2 and phi are read from the .tex by figlib.py.  Gamma_1 is the image
graph of phi.  Layouts:
  * if the graph is Hamiltonian, its vertices go on a circle in the order of a
    Hamiltonian cycle.  If 0,1,...,n-1 is a Hamiltonian cycle (as for every
    graph given in LCF notation) that cycle is used.  Otherwise the cycle
    with the fewest edge crossings is used.  The first vertex is at the top
    and the order runs counterclockwise, as in Sage's circular layout.
  * otherwise, the positions in HAND below if there are any, and if not the
    Kamada-Kawai, planar or spring layout (40 seeds) that scores best.
A graph in HAND uses its hand-tuned positions even if it is Hamiltonian.
Run check_figures.py afterwards.
"""
import argparse
import math
import os
import re
import sys

import networkx as nx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, '..', 'regular-graph-harmonic-quotient-examples.tex')

# Colors of the vertices of Gamma_1.  The first four follow the colored PNGs
# of the 2023 draft (0 white, 1 green, 2 blue, 3 red), lightened so that a
# black vertex number stays legible.
PALETTE = ['FFFFFF', '6CC56C', '7BA7E0', 'EE7B7B', 'F2D24B', 'F5A35C',
           'B99AE0', '7FD4D4', 'C8A27C', 'B0B0B0']

STYLE = r"""\definecolor{hq%d}{HTML}{%s}"""
TIKZSET = r"""\tikzset{
  hqgraph/.style={line cap=round},
  hqv/.style={circle, draw=black, line width=0.4pt, inner sep=0pt,
              minimum size=4.6mm, font=\scriptsize},
  hqe/.style={line width=0.5pt},
}"""


def rows(*rs):
    """Vertices in horizontal rows, top row first, evenly spaced."""
    pos = {}
    for k, r in enumerate(rs):
        for i, v in enumerate(r):
            pos[v] = (i - (len(r) - 1) / 2, -3.2 * k)
    return pos


def octahedron(outer, inner):
    """Outer triangle at 90, 210, 330 degrees (radius 1); inner triangle
    at 150, 270, 30 degrees and radius 0.26, so inner[i] faces the edge
    opposite outer[i]."""
    pos = {}
    for k, v in enumerate(outer):
        a = math.radians(90 + 120 * k)
        pos[v] = (math.cos(a), math.sin(a))
    for k, v in enumerate(inner):
        a = math.radians(150 + 120 * k)
        pos[v] = (0.26 * math.cos(a), 0.26 * math.sin(a))
    return pos


# Hand-tuned positions, keyed by (example, 'G2') or (figure stem, 'G1').
# Units are arbitrary: every layout is rescaled to fit its box.
HAND = {
    # K_{5,5}: the two color classes in two rows (a circle puts five
    # diameters through the center).
    ('d5reg10d', 'G2'): rows([1, 2, 5, 6, 8], [0, 3, 4, 7, 9]),
    # d4reg11a is not Hamiltonian: vertex 0 joins two copies of K_5 minus an
    # edge.  Each half is drawn with one crossing (the least possible, since
    # each half with vertex 0 contracts to K_5), the right half mirroring the left.
    # (Stretching vertically keeps the crossings and makes the picture taller.)
    ('d4reg11a', 'G2'): {v: (x, 1.8 * y) for v, (x, y) in {
        0: (0, 0), 1: (-0.86, 0.77), 2: (-1.25, 0.05), 3: (-1.93, 0.08),
        8: (-2.38, -0.99), 9: (-2.2, 0.89),
        5: (0.86, 0.77), 4: (1.25, 0.05), 6: (1.93, 0.08),
        10: (2.38, -0.99), 7: (2.2, 0.89)}.items()},
    # The octahedron, drawn as two nested triangles.
    ('harmonic-quotient_d4reg12b+circ6-1245', 'G1'):
        octahedron(outer=(0, 1, 3), inner=(5, 4, 2)),
    ('harmonic-quotient_d4reg12d+octahedral', 'G1'):
        octahedron(outer=(0, 1, 2), inner=(5, 4, 3)),
    # Planar quotients for which no automatic layout was both crossing-free
    # and uncrowded.  Found by a search over grid positions, then checked by
    # eye.  FKMiw: outer face 0,3,6,4, inner vertices placed to keep them
    # clear of the edges.
    ('harmonic-quotient_d4reg7b+fan5', 'G1'):
        {0: (-1.2, 0), 1: (0.6, 1), 2: (-0.3, 0), 3: (0.6, -1), 4: (1.6, 0)},
    ('harmonic-quotient_d4reg10a+K5me', 'G1'):
        {0: (1, 2), 1: (3, 0), 2: (0, 2), 3: (2, 2), 4: (3, 4)},
    ('harmonic-quotient_d4reg11f+FCdzo', 'G1'):
        {0: (0, 3), 1: (1, 1), 2: (2, 0), 3: (2, 1), 4: (3, 2), 5: (1, 2), 6: (0, 1)},
    ('harmonic-quotient_d4reg12a+v8e12ds44442222', 'G1'):
        {0: (1, 2), 1: (3, 2), 2: (0, 2), 3: (2, 0), 4: (2, 1), 5: (2, 3), 6: (4, 2), 7: (2, 2)},
    ('harmonic-quotient_d4reg12b+FKMiw', 'G1'):
        {0: (-1.5, 0), 1: (-0.8, 0.1), 2: (0.55, -0.28), 3: (0, 1.3), 4: (0, -1.3), 5: (0, -0.48), 6: (1.5, 0)},
}

NODE_CM = 0.46


def hamiltonian_cycles(G):
    """All Hamiltonian cycles through vertex min(V), each listed once."""
    V = sorted(G.nodes())
    n, s = len(V), V[0]
    path, seen, out = [s], {s}, []

    def rec():
        u = path[-1]
        if len(path) == n:
            if G.has_edge(u, s) and path[1] < path[-1]:
                out.append(list(path))
            return
        for w in sorted(G[u]):
            if w not in seen:
                seen.add(w)
                path.append(w)
                rec()
                path.pop()
                seen.discard(w)
    if n >= 3:
        rec()
    return out


def circle_crossings(order, edges):
    idx = {v: i for i, v in enumerate(order)}
    ch = [tuple(sorted((idx[a], idx[b]))) for a, b in edges]
    c = 0
    for i in range(len(ch)):
        a, b = ch[i]
        for j in range(i + 1, len(ch)):
            p, q = ch[j]
            if len({a, b, p, q}) == 4 and ((a < p < b) != (a < q < b)):
                c += 1
    return c


def circle_layout(order, edges=()):
    """Vertices on the unit circle in the given order, counterclockwise from the top.

    If three or more edges would pass through one point, the angles are moved
    by a few degrees (the first pattern in JIGGLE that removes every such
    point), so that the reader can tell the edges apart.
    """
    n = len(order)
    best = None
    for k, pat in enumerate(JIGGLE):
        pos = {v: (math.cos(math.pi / 2 + 2 * math.pi * i / n + pat(i, n)),
                   math.sin(math.pi / 2 + 2 * math.pi * i / n + pat(i, n)))
               for i, v in enumerate(order)}
        tp = figlib.triple_points(pos, edges)
        if best is None or tp < best[0]:
            best = (tp, k, pos)
        if tp == 0:
            break
    return best[2], best[1]


# Angle offsets (radians) tried in turn by circle_layout; the first is none.
D = math.radians(4)
JIGGLE = [lambda i, n: 0.0,
          lambda i, n: D * ((i % 2) * 2 - 1) / 2,
          lambda i, n: D * ((i % 3) - 1),
          lambda i, n: D * math.sin(2 * math.pi * i / n * 3 + 0.5),
          lambda i, n: D * ((i * 7) % 5 - 2) / 2,
          lambda i, n: D * ((i * 5) % 7 - 3) / 2,
          lambda i, n: 1.5 * D * ((i * 3) % 4 - 1.5) / 1.5]


def seg_point_dist(p, a, b):
    ax, ay = b[0] - a[0], b[1] - a[1]
    L = ax * ax + ay * ay
    t = max(0.0, min(1.0, ((p[0] - a[0]) * ax + (p[1] - a[1]) * ay) / L))
    return math.hypot(p[0] - a[0] - t * ax, p[1] - a[1] - t * ay)


def normalize(pos):
    """Center, scale to diameter 2 and rotate the longer axis horizontal."""
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
    pos = {v: (p[0] - cx, p[1] - cy) for v, p in pos.items()}
    sxx = sum(p[0] ** 2 for p in pos.values())
    syy = sum(p[1] ** 2 for p in pos.values())
    sxy = sum(p[0] * p[1] for p in pos.values())
    th = 0.5 * math.atan2(2 * sxy, sxx - syy)
    c, s = math.cos(-th), math.sin(-th)
    pos = {v: (c * p[0] - s * p[1], s * p[0] + c * p[1]) for v, p in pos.items()}
    r = max(math.hypot(*p) for p in pos.values()) or 1.0
    return {v: (p[0] / r, p[1] / r) for v, p in pos.items()}


def score(pos, edges):
    """Smaller is better: crowding (nodes too close to each other or to an
    edge they are not on), then crossings, then concurrent edges, then the
    smallest distance between nodes."""
    near = 0
    for v, p in pos.items():
        for a, b in edges:
            if v not in (a, b) and seg_point_dist(p, pos[a], pos[b]) < 0.22:
                near += 1
    V = list(pos)
    dists = [math.dist(pos[u], pos[w]) for i, u in enumerate(V) for w in V[i + 1:]]
    near += sum(1 for d in dists if d < 0.42)
    return (near, figlib.crossings(pos, edges), figlib.triple_points(pos, edges), -round(min(dists), 2))


def faces(emb):
    """The faces of a planar embedding, as vertex lists."""
    seen, out = set(), []
    for u, v in emb.edges():
        if (u, v) not in seen:
            out.append(emb.traverse_face(u, v, mark_half_edges=seen))
    return out


def tutte_layouts(G):
    """Tutte (barycentric) drawings, one for each face as the outer face.

    The outer face is a regular polygon and every other vertex is the average
    of its neighbors.  For a 3-connected planar graph this is a drawing
    without crossings and with convex faces.
    """
    ok, emb = nx.check_planarity(G)
    if not ok:
        return []
    V = sorted(G.nodes())
    out = []
    for f in faces(emb):
        if len(f) < 3 or len(set(f)) < len(f):
            continue
        pos = circle_layout(f)[0]
        inner = [v for v in V if v not in pos]
        if inner:
            idx = {v: i for i, v in enumerate(inner)}
            A = [[0.0] * len(inner) for _ in inner]
            bx, by = [0.0] * len(inner), [0.0] * len(inner)
            for v in inner:
                i = idx[v]
                A[i][i] = G.degree(v)
                for w in G[v]:
                    if w in idx:
                        A[i][idx[w]] -= 1
                    else:
                        bx[i] += pos[w][0]
                        by[i] += pos[w][1]
            import numpy as np
            X = np.linalg.solve(np.array(A), np.array([bx, by]).T)
            for v in inner:
                pos[v] = tuple(X[idx[v]])
        out.append(pos)
        # The barycentric drawing crowds the inner vertices toward the
        # center, so also offer copies with the inner vertices pushed out.
        for k in (1.25, 1.5, 1.75, 2.0, 2.5, 3.0):
            out.append({v: (p if v in f else (k * p[0], k * p[1])) for v, p in pos.items()})
    return out


def force_layout(G, E):
    """The best of Kamada-Kawai, planar, Tutte and 40 spring layouts (see score)."""
    cands = [nx.kamada_kawai_layout(G)]
    cands += [nx.spring_layout(G, seed=s, iterations=200) for s in range(40)]
    if nx.check_planarity(G)[0]:
        P = nx.planar_layout(G)
        cands += [nx.kamada_kawai_layout(G, pos=P), P]
        T = tutte_layouts(G)
        cands += T + [nx.kamada_kawai_layout(G, pos=t) for t in T]
    cands = [normalize({v: tuple(p) for v, p in c.items()}) for c in cands]
    return min(cands, key=lambda p: score(p, E))


def layout(G, key):
    """Return (positions, description).

    key is (example, 'G2') for Gamma_2 and (figure stem, 'G1') for Gamma_1.
    A Gamma_1 whose circle drawing has two or more crossings is drawn without
    crossings instead, if it is planar and a crossing-free layout without crowding is
    found (the small quotient graphs are easier to recognize that way: the
    prism, the octahedron, the wheel).
    """
    V = sorted(G.nodes())
    E = sorted(tuple(sorted(e)) for e in G.edges())
    if key in HAND:
        return dict(HAND[key]), 'hand-tuned'
    n = len(V)
    if n <= 2:
        return {V[0]: (-1.0, 0.0), V[-1]: (1.0, 0.0)}, 'segment'
    jig = ['', ', angles adjusted to separate concurrent edges']
    if all(G.has_edge(V[i], V[(i + 1) % n]) for i in range(n)):
        order, desc = V, 'circle, cycle 0,1,...,%d' % (n - 1)
    else:
        cyc = hamiltonian_cycles(G)
        order = min(cyc, key=lambda o: (circle_crossings(o, E), o)) if cyc else None
        if order:
            desc = 'circle, Hamiltonian cycle %s' % ','.join(map(str, order))
    if order:
        cr = circle_crossings(order, E)
        if key[1] == 'G1' and cr > 1 and nx.check_planarity(G)[0]:
            pos = force_layout(G, E)
            if score(pos, E)[:2] == (0, 0):
                return pos, 'crossing-free (planar; a circle would have %d crossings)' % cr
        pos, k = circle_layout(order, E)
        return pos, desc + ' (%d crossings%s)' % (cr, jig[k > 0])
    pos = force_layout(G, E)
    return pos, 'force-directed (%d crossings)' % figlib.crossings(pos, E)


def fit(pos, w, h):
    """Scale and translate positions (in cm) so that the nodes fit a w x h box."""
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    spanx, spany = (max(xs) - min(xs)) or 1e-9, (max(ys) - min(ys)) or 1e-9
    s = min((w - NODE_CM) / spanx, (h - NODE_CM) / spany)
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return {v: ((p[0] - cx) * s, (p[1] - cy) * s) for v, p in pos.items()}


def block(which, box, png, pos, edges, color, notes):
    w, h = box
    out = ['%% BEGIN %s %s box=%gx%gcm was=%s' % (figlib.MARK, which, w, h, png)]
    out += ['% ' + n for n in notes]
    out.append(r'\begin{tikzpicture}[hqgraph]')
    for v in sorted(pos):
        x, y = pos[v]
        out.append(r'\node[hqv, fill=hq%d] (v%d) at (%.3f,%.3f) {%d};' % (color[v], v, x, y, v))
    for a, b in edges:
        out.append(r'\draw[hqe] (v%d) -- (v%d);' % (a, b))
    out.append(r'\end{tikzpicture}%')
    out.append('%% END %s %s' % (figlib.MARK, which))
    return '\n'.join(out)


def build(f):
    """The two blocks of figure f, and a one-line report."""
    phi = {r[0]: r[1] for r in f['rows']}
    E2 = f['edges2']
    V1, E1 = figlib.image_graph(E2, phi)
    G2, G1 = nx.Graph(E2), nx.Graph()
    G1.add_nodes_from(V1)
    G1.add_edges_from(E1)
    p2, how2 = layout(G2, (f['example'], 'G2'))
    p1, how1 = layout(G1, (f['stem'], 'G1'))
    (b2, b1), (png2, png1) = f['boxes'], f['images']
    p2, p1 = fit(p2, *b2), fit(p1, *b1)
    n2 = ['Gamma_2 = %s (%s); vertex x has color hq<phi(x)>, phi from the table.'
          % (f['example'], f['edges2_source']), 'Layout: %s.' % how2]
    n1 = ['Gamma_1 = image of phi; vertex y has color hq<y>.', 'Layout: %s.' % how1]
    return (block('G2', b2, png2, p2, E2, phi, n2), block('G1', b1, png1, p1, E1, {y: y for y in V1}, n1),
            '%s | G2 %s | G1 %s' % (f['stem'], how2, how1))


def set_styles(T):
    defs = '\n'.join(STYLE % (i, c) for i, c in enumerate(PALETTE))
    blk = ('%% BEGIN %s styles\n%% Vertex y of Gamma_1 and its fiber in Gamma_2 have color hq<y>.\n'
           '%s\n%s\n%% END %s styles\n' % (figlib.MARK, defs, TIKZSET, figlib.MARK))
    m = re.search(r'%% BEGIN %s styles\n.*?%% END %s styles\n' % (re.escape(figlib.MARK), re.escape(figlib.MARK)),
                  T, re.S)
    if m:
        return T[:m.start()] + blk + T[m.end():]
    anchor = '\\begin{document}'
    i = T.index(anchor)
    return T[:i] + blk + '\n' + T[i:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default='')
    ap.add_argument('--tex', default=TEX)
    a = ap.parse_args()
    allfigs = figlib.read_figures(a.tex)
    ncol = max(max(r[1] for r in f['rows']) for f in allfigs) + 1
    assert ncol <= len(PALETTE), 'not enough colors'
    figs = allfigs
    if a.only:
        want = a.only.split(',')
        figs = [f for f in allfigs if f['stem'] in want]
        assert len(figs) == len(want), 'unknown stem in --only'
    T = open(a.tex).read()
    if '\\usepackage{tikz}' not in T:
        T = T.replace('\\usepackage{graphicx}\n', '\\usepackage{graphicx}\n\\usepackage{tikz}\n', 1)
    T = set_styles(T)
    for f in figs:
        g2, g1, report = build(f)
        lab = '\\label{%s}' % f['label']
        end = T.index(lab)
        beg = T.rindex('\\begin{figure}', 0, end)
        d = figlib.drawings(T[beg:end + len(lab)])
        new = T[beg:beg + d[0]['start']] + g2 + T[beg + d[0]['end']:beg + d[1]['start']] + g1 \
            + T[beg + d[1]['end']:end]
        T = T[:beg] + new + T[end:]
        print(report)
    open(a.tex, 'w').write(T)


if __name__ == '__main__':
    main()
