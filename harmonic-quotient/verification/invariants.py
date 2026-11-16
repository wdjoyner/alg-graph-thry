"""Check stated invariants of each graph: charpoly, diameter, girth, circumference, |Aut|,
#spanning trees, transitivity, LCF descriptions."""
import re, json
import networkx as nx, sympy as sp
from networkx.algorithms.isomorphism import GraphMatcher
from verify import D, GR, G_of, genus

x = sp.symbols('x')

def charpoly(G):
    n = G.number_of_nodes()
    A = sp.Matrix(nx.to_numpy_array(G, nodelist=range(n), dtype=int).astype(int).tolist())
    return sp.expand(A.charpoly(x).as_expr())

def tex2poly(s):
    s = s.replace('\\,', '').replace('\\.', '')
    s = re.sub(r'[,.\s]+$', '', s.strip())
    s = re.sub(r'\^\{(\d+)\}', r'^\1', s)
    s = s.replace('^', '**')
    s = re.sub(r'(\d)\s*x', r'\1*x', s)
    s = s.replace(' ', '')
    s = re.sub(r'[,.]$', '', s)
    return sp.expand(sp.sympify(s))

def kappa(G):
    n = G.number_of_nodes()
    L = sp.Matrix(nx.laplacian_matrix(G, nodelist=range(n)).toarray().astype(int).tolist())
    return int(L[1:, 1:].det())

def circumference(G):
    n = G.number_of_nodes(); best = 0
    adj = {v: set(G[v]) for v in G}
    for s in range(n):
        stack = [(s, [s], {s})]
        while stack:
            v, path, seen = stack.pop()
            for w in adj[v]:
                if w == s and len(path) >= 3: best = max(best, len(path))
                elif w > s and w not in seen:
                    stack.append((w, path + [w], seen | {w}))
        if best == n: return n
    return best

def auts(G):
    n = G.number_of_nodes()
    return [tuple(m[i] for i in range(n)) for m in GraphMatcher(G, G).isomorphisms_iter()]

def transitivity(G, A):
    vt = len({p[0] for p in A}) == G.number_of_nodes()
    u, v = next(iter(G.edges()))
    eorb = {frozenset((p[u], p[v])) for p in A}
    et = len(eorb) == G.number_of_edges()
    aorb = {(p[u], p[v]) for p in A}
    at = len(aorb) == 2 * G.number_of_edges()
    return vt, et, at

def lcf(n, L, r):
    G = nx.cycle_graph(n)
    for i in range(n):
        G.add_edge(i, (i + L[i % len(L)]) % n)
    return G

def parse_lcf(s):
    m = re.match(r'\(?\s*(\d+)\s*,\s*\[([-\d,\s]+)\]\s*,\s*(\d+)\s*\)?', s)
    if not m: return None
    return int(m.group(1)), [int(t) for t in m.group(2).split(',')], int(m.group(3))

if __name__ == '__main__':
    items = {it['name']: it for it in D['items']}
    summ = {s['name']: s for s in D['summary']}
    for name in sorted(GR, key=lambda s: (s[1], int(re.findall(r'reg(\d+)', s)[0]), s)):
        G = G_of(name); n = G.number_of_nodes(); A = auts(G)
        vt, et, at = transitivity(G, A)
        cp = charpoly(G); kap = kappa(G)
        info = dict(n=n, diam=nx.diameter(G), girth=nx.girth(G), circ=circumference(G), aut=len(A), crit=kap,
                    genus=genus(G), vt=vt, et=et, at=at, bip=nx.is_bipartite(G))
        issues = []
        it = items.get(name)
        if it:
            if it['charpoly']:
                try:
                    if tex2poly(it['charpoly']) != cp: issues.append(f'charpoly stated {it["charpoly"].strip()} TRUE {cp}')
                except Exception as e: issues.append(f'charpoly parse fail {e}')
            for k, kk in [('diameter', 'diam'), ('girth', 'girth'), ('circumference', 'circ'), ('aut', 'aut'), ('crit', 'crit')]:
                if it[k] is not None and it[k] != info[kk]: issues.append(f'{k} stated {it[k]} TRUE {info[kk]}')
            if it['sage']:
                p = parse_lcf(it['sage'])
                if p and not nx.is_isomorphic(lcf(*p), G): issues.append(f'Sage LCF {it["sage"]} NOT isomorphic to this graph')
        s = summ.get(name)
        if s:
            if s['aut'] != len(A): issues.append(f'summary |Aut| {s["aut"]} TRUE {len(A)}')
            if s['genus'] != genus(G): issues.append(f'summary genus {s["genus"]} TRUE {genus(G)}')
            if s['crit']:
                cnum = int(re.match(r'\s*(\d+)', s['crit']).group(1))
                if cnum != kap: issues.append(f'summary crit {cnum} TRUE {kap}')
                fac = s['crit'].split('=')[-1]
                # evaluate factorization like 2^63\cdot 31 -> ambiguous juxtaposition; just report
            p = parse_lcf(s['lcf'])
            if p and not nx.is_isomorphic(lcf(*p), G): issues.append(f'summary LCF {s["lcf"]} NOT isomorphic to this graph')
        print(name, info, '\n   ISSUES: ' + ' || '.join(issues) if issues else '')
