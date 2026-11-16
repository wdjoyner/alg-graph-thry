"""Check every TikZ figure of the harmonic-quotient paper against the text.

Usage (from this folder):
    python3 check_figures.py [--reference OLD.tex]

This script does not use figlib.py or make_figures.py.  It reads the .tex and
the files in ../figures/ separately and checks, for each figure that \\inputs
TikZ files:

  1. Gamma_2: the drawn vertices are 0..n-1, each labeled by its own number,
     and the drawn edges are exactly the edge list in the text (E_2 in the
     example, or the edge list where the graph is defined).
  2. Gamma_2 is k-regular, with k matching "cubic/quartic/quintic" in the caption.
  3. The table: the one nearest to the figure in the source.  Vertex x of
     Gamma_2 is filled with color hq<phi(x)>, so each color class is a fiber,
     and the fiber sizes agree with the table.
  4. Gamma_1: the drawn vertices are the values of phi, vertex y is filled with
     hq<y>, and the drawn edges are the images phi(u)phi(v) of the edges of
     Gamma_2 with phi(u) != phi(v).  If the text lists E_1 for this morphism,
     the drawn edges are exactly E_1.
  5. Edge counts: |E_2| - |V_2| + 1 and |E_1| - |V_1| + 1 equal the genera in
     the text.  For every vertex y of Gamma_1 the sum of m(x) over the fiber
     of y equals deg(phi) in the text, and the caption's "degree d" is deg(phi).
  6. Readability: nodes do not overlap, no edge passes through a node it does
     not join, and the picture fits the box of the PNG it replaces.  A point
     other than a node where three or more edges cross is reported as a
     warning (WARN), not a failure.

With --reference, the figure labels and captions are also compared with an
older version of the .tex: they must be unchanged and in the same order.
Exit status 0 if every check passes (warnings allowed).
"""
import argparse
import itertools
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
TEX = os.path.join(ROOT, 'regular-graph-harmonic-quotient-examples.tex')
NODE_R = 0.23    # cm, half of minimum size=4.6mm in hq-style.tex
WORDS = {'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8}
REG = {'cubic': 3, 'quartic': 4, 'quintic': 5}

problems = []
warnings = []


def bad(fig, msg):
    problems.append('%s: %s' % (fig, msg))


def warn(fig, msg):
    warnings.append('%s: %s' % (fig, msg))


def nocomments(t):
    return '\n'.join(re.sub(r'(?<!\\)%.*$', '', ln) if not ln.lstrip().startswith('\\begin{example}%')
                     else ln for ln in t.split('\n'))


def pairs(s):
    return {frozenset((int(a), int(b))) for a, b in re.findall(r'\(\s*(\d+)\s*,\s*(\d+)\s*\)', s)}


def set_after(t, i):
    """Pairs in the first \\{ ... \\} that starts at or after offset i."""
    j = t.index('\\{', i)
    k = t.index('\\}', j)
    return pairs(t[j:k])


def read_tikz(path):
    s = open(path).read()
    nodes = {}
    for m in re.finditer(r'\\node\[hqv, fill=hq(\d+)\] \(v(\d+)\) at \(([-\d.]+),([-\d.]+)\) \{(\d+)\};', s):
        nodes[int(m.group(2))] = {'color': int(m.group(1)), 'xy': (float(m.group(3)), float(m.group(4))),
                                  'text': int(m.group(5))}
    edges = [frozenset((int(a), int(b))) for a, b in re.findall(r'\\draw\[hqe\] \(v(\d+)\) -- \(v(\d+)\);', s)]
    n_node_cmds = len(re.findall(r'\\node', s))
    n_draw_cmds = len(re.findall(r'\\draw', s))
    return nodes, edges, (n_node_cmds == len(nodes) and n_draw_cmds == len(edges))


def readability(fig, nodes, edges, box):
    P = {v: d['xy'] for v, d in nodes.items()}
    for u, w in itertools.combinations(P, 2):
        if math.dist(P[u], P[w]) < 2 * NODE_R + 0.05:
            bad(fig, 'nodes %d and %d overlap' % (u, w))
    for v in P:
        for e in edges:
            a, b = tuple(e)
            if v in e:
                continue
            (x1, y1), (x2, y2), (px, py) = P[a], P[b], P[v]
            L = (x2 - x1) ** 2 + (y2 - y1) ** 2
            t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / L))
            if math.hypot(px - x1 - t * (x2 - x1), py - y1 - t * (y2 - y1)) < NODE_R + 0.04:
                bad(fig, 'edge %d-%d passes through node %d' % (a, b, v))
    # points where three or more edges cross
    E = [tuple(e) for e in edges]
    pts = []
    for (a, b), (c, d) in itertools.combinations(E, 2):
        if len({a, b, c, d}) < 4:
            continue
        p, q, r, s = P[a], P[b], P[c], P[d]
        den = (q[0] - p[0]) * (s[1] - r[1]) - (q[1] - p[1]) * (s[0] - r[0])
        if abs(den) < 1e-12:
            continue
        t = ((r[0] - p[0]) * (s[1] - r[1]) - (r[1] - p[1]) * (s[0] - r[0])) / den
        u = ((r[0] - p[0]) * (q[1] - p[1]) - (r[1] - p[1]) * (q[0] - p[0])) / den
        if 0 < t < 1 and 0 < u < 1:
            pts.append(((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])), {(a, b), (c, d)}))
    for (x, ea), (y, eb) in itertools.combinations(pts, 2):
        if math.dist(x, y) < 0.03 and len(ea | eb) >= 3:
            warn(fig, 'three or more edges cross at (%.2f,%.2f)' % x)
            break
    xs = [p[0] for p in P.values()]
    ys = [p[1] for p in P.values()]
    w, h = box
    if max(xs) - min(xs) + 2 * NODE_R > w + 0.01 or max(ys) - min(ys) + 2 * NODE_R > h + 0.01:
        bad(fig, 'drawing larger than its %gcm x %gcm box' % box)


def boxes_from(ref_src, label):
    """The PNG boxes (width, height) of the figure with this label in the reference."""
    i = ref_src.index('\\label{%s}' % label)
    blk = ref_src[ref_src.rindex('\\begin{figure}', 0, i):i]
    out = []
    for o in re.findall(r'\\includegraphics\[([^\]]*)\]', blk):
        w = float(re.search(r'width=([\d.]+)cm', o).group(1))
        h = float(re.search(r'height=([\d.]+)cm', o).group(1))
        out.append((w, h))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tex', default=TEX)
    ap.add_argument('--reference', help='older .tex with the \\includegraphics version')
    a = ap.parse_args()
    raw = open(a.tex).read()
    t = nocomments(raw)
    ref = nocomments(open(a.reference).read()) if a.reference else None

    figs = list(re.finditer(r'\\begin\{figure\}.*?\\end\{figure\}', t, re.S))
    examples = [(m.start(), m.end(), m.group(1)) for m in
                re.finditer(r'\\begin\{example\}%\s*(\w+).*?\\end\{example\}', t, re.S)]
    tables = [(m.start(), m.end(), m.group(1)) for m in
              re.finditer(r'\\begin\{tabular\}\{c\|c\|c\|c\}(.*?)\\end\{tabular\}', t, re.S)]
    n_tikz = n_png = 0
    for fm in figs:
        ftxt = fm.group(0)
        label = re.search(r'\\label\{([^}]*)\}', ftxt).group(1)
        inputs = re.findall(r'\\input\{figures/([^}]*)\}', ftxt)
        if not inputs:
            n_png += 1
            continue
        n_tikz += 1
        fig = label[4:]
        if inputs != [fig + '-G2.tex', fig + '-G1.tex'] or '\\includegraphics' in ftxt:
            bad(fig, 'figure does not input exactly %s-G2.tex and -G1.tex' % fig)
            continue
        es, ee, name = [e for e in examples if e[0] <= fm.start() < e[1]][0]
        cap = re.search(r'\\caption\{(.*)\}\s*\\label', ftxt, re.S).group(1)

        # Gamma_2 from the text
        ex = t[es:ee]
        m = re.search(r'E_2\s*=', ex)
        if m:
            E2 = set_after(t, es + m.start())
        else:
            it = re.search(r'\\item\s*\{\\tt\s*%s\}' % name, t)
            E2 = set_after(t, it.end())
        V2 = sorted(set().union(*E2))
        # the nearest table
        cand = [tb for tb in tables if es <= tb[0] < ee]
        tb = min(cand, key=lambda tb: min(abs(tb[0] - fm.end()), abs(fm.start() - tb[1])))
        rows = [tuple(int(c.strip()) for c in r.replace('\\hline', '').split('&'))
                for r in tb[2].split('\\\\') if re.fullmatch(r'\s*\d+(\s*&\s*\d+){3}\s*', r.replace('\\hline', ''))]
        phi = {r[0]: r[1] for r in rows}
        mult = {r[0]: r[2] for r in rows}
        after = t[tb[1]:tb[1] + 400]
        g2 = int(re.search(r'genus\(\\Gamma_2\)\s*=\s*(\d+)', after).group(1))
        g1 = int(re.search(r'genus\(\\Gamma_1\)\s*=\s*(\d+)', after).group(1))
        deg = int(re.search(r'deg\(\\phi\)\s*=\s*(\d+)', after).group(1))

        # 1, 2: Gamma_2 drawing
        n2, e2, clean2 = read_tikz(os.path.join(ROOT, 'figures', fig + '-G2.tex'))
        if not clean2:
            bad(fig, 'G2 file has commands this checker does not understand')
        if sorted(n2) != V2 or any(d['text'] != v for v, d in n2.items()):
            bad(fig, 'G2 vertices or vertex numbers differ from the text')
        if len(e2) != len(set(e2)) or set(e2) != E2:
            bad(fig, 'G2 edges differ from the text: drawn %d, text %d' % (len(e2), len(E2)))
        degs = {sum(1 for e in E2 if v in e) for v in V2}
        k = [REG[w] for w in REG if w in cap]
        if len(degs) != 1 or (k and k[0] not in degs):
            bad(fig, 'Gamma_2 degrees %s do not match the caption' % degs)
        # 3: fibers and colors
        if sorted(phi) != V2:
            bad(fig, 'table rows %s are not the vertices of Gamma_2' % sorted(phi))
            continue
        for v, d in n2.items():
            if d['color'] != phi[v]:
                bad(fig, 'G2 vertex %d has color hq%d but phi(%d)=%d' % (v, d['color'], v, phi[v]))
        fib_drawn = sorted(sum(1 for d in n2.values() if d['color'] == c) for c in {d['color'] for d in n2.values()})
        fib_text = sorted(list(phi.values()).count(y) for y in set(phi.values()))
        if fib_drawn != fib_text:
            bad(fig, 'fiber sizes drawn %s, in the table %s' % (fib_drawn, fib_text))
        # 4: Gamma_1 drawing
        n1, e1, clean1 = read_tikz(os.path.join(ROOT, 'figures', fig + '-G1.tex'))
        if not clean1:
            bad(fig, 'G1 file has commands this checker does not understand')
        V1 = sorted(set(phi.values()))
        E1 = {frozenset((phi[u], phi[w])) for u, w in map(tuple, E2) if phi[u] != phi[w]}
        if sorted(n1) != V1 or any(d['text'] != v or d['color'] != v for v, d in n1.items()):
            bad(fig, 'G1 vertices, numbers or colors are wrong')
        if len(e1) != len(set(e1)) or set(e1) != E1:
            bad(fig, 'G1 edges are not the image of phi')
        blk = t[max(es, max([x[1] for x in cand if x[1] <= tb[0]], default=es)):tb[0]]
        m1 = list(re.finditer(r'E_1\s*=', blk))
        if m1:
            E1t = set_after(blk, m1[-1].start())
            if E1t != E1:
                bad(fig, 'E_1 in the text differs from the image of phi')
        # 5: counts
        if len(E2) - len(V2) + 1 != g2:
            bad(fig, 'genus(Gamma_2)=%d in the text, %d from the edges' % (g2, len(E2) - len(V2) + 1))
        if len(e1) - len(n1) + 1 != g1:
            bad(fig, 'genus(Gamma_1)=%d in the text, %d drawn' % (g1, len(e1) - len(n1) + 1))
        for y in V1:
            s = sum(mult[x] for x in V2 if phi[x] == y)
            if s != deg:
                bad(fig, 'sum of m over the fiber of %d is %d, deg(phi)=%d' % (y, s, deg))
        dm = re.search(r'degree\s+(\w+)', cap)
        if dm:
            dc = WORDS.get(dm.group(1), int(dm.group(1)) if dm.group(1).isdigit() else None)
            if dc != deg:
                bad(fig, 'caption says degree %s, deg(phi)=%d' % (dm.group(1), deg))
        # 6: readability
        box = boxes_from(ref, label) if ref else [(5.0, 5.0), (4.0, 4.0)]
        readability(fig + ' G2', n2, e2, box[0])
        readability(fig + ' G1', n1, e1, box[1])

    if ref:
        def caps(s):
            return [(re.search(r'\\label\{([^}]*)\}', f).group(1),
                     re.sub(r'\s+', ' ', re.search(r'\\caption\{(.*)\}\s*\\label', f, re.S).group(1)))
                    for f in re.findall(r'\\begin\{figure\}.*?\\end\{figure\}', s, re.S)]
        if caps(t) != caps(ref):
            bad('captions', 'figure labels or captions differ from the reference')
    print('%d figures drawn in TikZ, %d still use PNG files' % (n_tikz, n_png))
    for p in warnings:
        print('WARN', p)
    for p in problems:
        print('FAIL', p)
    print('all checks passed' if not problems else '%d problems' % len(problems))
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
