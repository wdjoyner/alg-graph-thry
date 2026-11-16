"""Read the figures of the harmonic-quotient paper from its LaTeX source.

For every figure environment that draws Gamma_2 and Gamma_1 this module finds
  * the figure label, caption and the two image placements,
  * the example it belongs to and the edge list of Gamma_2,
  * the table (x, phi(x), m(x), nu(x)) that the figure depicts.

The table belonging to a figure is the first table that starts after the first
\\ref to the figure's label and before the next figure (the text says "...
tabulated below and depicted in Figure \\ref{...}" or "... depicted in Figure
\\ref{...} and tabulated below").  If there is none, it is the last table
before that \\ref ("... tabulated below. ... depicted in Figure \\ref{...}").
check_figures.py uses a different rule (the nearest table) and checks that
the two rules agree.

Gamma_1 is not read from the text.  It is the image graph of phi: its vertices
are the values of phi and its edges are the pairs {phi(u), phi(v)} with
uv an edge of Gamma_2 and phi(u) != phi(v).
"""
import re
import itertools

PAIR = re.compile(r'\(\s*(\d+)\s*,\s*(\d+)\s*\)')


def strip_comments(tex):
    """Blank out % comments but keep every character offset and line number."""
    out = []
    for ln in tex.split('\n'):
        m = re.search(r'(?<!\\)%', ln)
        if m:
            # keep the "% d3reg8a" marker after \begin{example}
            if re.match(r'\s*\\begin\{example\}%', ln):
                out.append(ln)
            else:
                out.append(ln[:m.start()] + ' ' * (len(ln) - m.start()))
        else:
            out.append(ln)
    return '\n'.join(out)


def edge_list_after(text, start):
    """The first set \\{ (a,b), ... \\} with at least three pairs after `start`."""
    for m in re.finditer(r'\\\{(.*?)\\\}', text[start:], re.S):
        prs = [(int(a), int(b)) for a, b in PAIR.findall(m.group(1))]
        if len(prs) >= 3:
            return prs, start + m.start()
    return None, None


def lcf_edges(n, shifts, reps):
    """Edges of Sage's graphs.LCFGraph(n, shifts, reps)."""
    E = {tuple(sorted((i, (i + 1) % n))) for i in range(n)}
    seq = list(shifts) * reps
    for i, s in enumerate(seq):
        E.add(tuple(sorted((i, (i + s) % n))))
    return sorted(E)


def graph_edges(src, name, example_start, example_end):
    """Edge list of the graph called `name`, and how it was found.

    Order of preference: the edge list E_2 written inside the example, then
    the edge list in the numbered list item that defines the graph, then the
    LCF command in that list item.
    """
    body = src[example_start:example_end]
    m = re.search(r'E_2\s*=\s*\\\{', body)
    if m:
        e, _ = edge_list_after(src, example_start + m.start())
        return sorted(tuple(sorted(x)) for x in e), 'E_2 in the example'
    it = re.search(r'\\item\s*\{\\tt\s*' + name + r'\}(.*?)(?=\\item|\\end\{enumerate\})', src, re.S)
    if it is None:
        raise ValueError('no list item for ' + name)
    e, _ = edge_list_after(src[:it.end()], it.start())
    if e:
        return sorted(tuple(sorted(x)) for x in e), 'edge list in the list item'
    lcf = re.search(r'LCFGraph\(\s*(\d+)\s*,\s*\[([-\d,\s]+)\]\s*,\s*(\d+)\s*\)', it.group(1))
    if lcf:
        n, sh, r = int(lcf.group(1)), [int(x) for x in lcf.group(2).split(',')], int(lcf.group(3))
        return lcf_edges(n, sh, r), 'LCF command in the list item'
    raise ValueError('no edges for ' + name)


def tables_in(src, a, b):
    """All phi tables between offsets a and b: list of (start, end, rows)."""
    res = []
    for m in re.finditer(r'\\begin\{tabular\}\{c\|c\|c\|c\}(.*?)\\end\{tabular\}', src[a:b], re.S):
        rows = []
        for r in m.group(1).split('\\\\'):
            cells = [c.replace('\\hline', '').strip() for c in r.split('&')]
            if len(cells) == 4 and all(re.fullmatch(r'\d+', c) for c in cells):
                rows.append(tuple(int(c) for c in cells))
        res.append((a + m.start(), a + m.end(), rows))
    return res


def caption_of(fig_text):
    m = re.search(r'\\caption\{', fig_text)
    i, depth = m.end(), 1
    while depth:
        depth += {'{': 1, '}': -1}.get(fig_text[i], 0)
        i += 1
    return fig_text[m.end():i - 1]


MARK = 'make_figures.py'
BEGIN_RE = re.compile(r'% BEGIN ' + re.escape(MARK) + r' (G[12]) box=([\d.]+)x([\d.]+)cm was=(\S+)\n')


def drawings(fig_raw):
    """The two drawings of a figure environment (raw text, comments kept).

    Each is either an \\includegraphics[height=..,width=..]{png} or a block
        % BEGIN make_figures.py G2 box=5x5cm was=graphics/foo.png
        ...
        % END make_figures.py G2
    written by make_figures.py.  Returns dicts with keys kind ('png' or
    'tikz'), png, box (width, height in cm), start, end (offsets in fig_raw).
    """
    out = []
    for m in re.finditer(r'\\includegraphics\[([^\]]*)\]\{([^}]*)\}', fig_raw):
        w = re.search(r'width=([\d.]+)cm', m.group(1))
        h = re.search(r'height=([\d.]+)cm', m.group(1))
        out.append({'kind': 'png', 'png': m.group(2), 'box': (float(w.group(1)), float(h.group(1))),
                    'start': m.start(), 'end': m.end()})
    for m in BEGIN_RE.finditer(fig_raw):
        e = re.compile(r'% END ' + re.escape(MARK) + ' ' + m.group(1) + r'(?=\n)').search(fig_raw, m.end())
        out.append({'kind': 'tikz', 'png': m.group(4), 'box': (float(m.group(2)), float(m.group(3))),
                    'start': m.start(), 'end': e.end(), 'which': m.group(1)})
    out.sort(key=lambda d: d['start'])
    if len(out) != 2:
        raise ValueError('a figure must have exactly two drawings')
    return out


def read_figures(tex_path):
    raw = open(tex_path).read()
    src = strip_comments(raw)
    examples = [(m.start(), m.end(), m.group(1))
                for m in re.finditer(r'\\begin\{example\}%\s*(\w+).*?\\end\{example\}', src, re.S)]
    figs = []
    for fm in re.finditer(r'\\begin\{figure\}.*?\\end\{figure\}', src, re.S):
        ftxt = fm.group(0)
        imgs = drawings(raw[fm.start():fm.end()])
        label = re.search(r'\\label\{(fig:[^}]*)\}', ftxt).group(1)
        ex = [e for e in examples if e[0] <= fm.start() < e[1]]
        if len(ex) != 1:
            raise ValueError('figure outside an example: ' + label)
        es, ee, name = ex[0]
        ref = src.find('\\ref{' + label + '}', es, ee)
        unreferenced = ref < 0
        if unreferenced:
            ref = fm.start()
        nxt = src.find('\\begin{figure}', fm.end())
        stop = ee if nxt < 0 else min(ee, nxt)
        alltabs = tables_in(src, es, ee)
        after = [t for t in alltabs if ref < t[0] < stop]
        before = [t for t in alltabs if t[0] < ref]
        if after:
            table = after[0]
        elif before:
            table = before[-1]
        else:
            raise ValueError('no table for ' + label)
        edges, how = graph_edges(src, name, es, ee)
        figs.append({
            'label': label,
            'stem': label[len('fig:'):],
            'example': name,
            'line': src[:fm.start()].count('\n') + 1,
            'table_line': src[:table[0]].count('\n') + 1,
            'images': [i['png'] for i in imgs],
            'boxes': [i['box'] for i in imgs],
            'caption': caption_of(ftxt),
            'edges2': edges,
            'edges2_source': how,
            'rows': table[2],
            'unreferenced': unreferenced,
        })
    return figs


def image_graph(edges2, phi):
    V1 = sorted(set(phi.values()))
    E1 = sorted({tuple(sorted((phi[u], phi[v]))) for u, v in edges2 if phi[u] != phi[v]})
    return V1, E1


def crossings(pos, edges):
    """Number of pairs of edges whose straight segments cross (shared ends excluded)."""
    def ccw(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    n = 0
    for (a, b), (c, d) in itertools.combinations(edges, 2):
        if len({a, b, c, d}) < 4:
            continue
        p, q, r, s = pos[a], pos[b], pos[c], pos[d]
        if ccw(p, q, r) * ccw(p, q, s) < 0 and ccw(r, s, p) * ccw(r, s, q) < 0:
            n += 1
    return n


def triple_points(pos, edges, tol=0.02):
    """Number of points (not vertices) where three or more edges meet.

    tol is in the units of pos; use it on normalized layouts (diameter 2).
    """
    E = [tuple(e) for e in edges]
    pts = []
    for (a, b), (c, d) in itertools.combinations(E, 2):
        if len({a, b, c, d}) < 4:
            continue
        p, q, r, s = pos[a], pos[b], pos[c], pos[d]
        den = (q[0] - p[0]) * (s[1] - r[1]) - (q[1] - p[1]) * (s[0] - r[0])
        if abs(den) < 1e-12:
            continue
        t = ((r[0] - p[0]) * (s[1] - r[1]) - (r[1] - p[1]) * (s[0] - r[0])) / den
        u = ((r[0] - p[0]) * (q[1] - p[1]) - (r[1] - p[1]) * (q[0] - p[0])) / den
        if 0 < t < 1 and 0 < u < 1:
            pts.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    n = 0
    for x, y in itertools.combinations(pts, 2):
        if abs(x[0] - y[0]) < tol and abs(x[1] - y[1]) < tol:
            n += 1
    return n
