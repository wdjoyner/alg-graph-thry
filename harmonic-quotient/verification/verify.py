"""Verify every tabulated harmonic quotient morphism in the manuscript."""
import json, itertools
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher

D = json.load(open('data.json'))

def build_graphs():
    g = {}
    for it in D['items']:
        if it['edges']:
            g[it['name']] = [tuple(e) for e in it['edges']]
    for ex in D['examples']:
        for lab, e in ex['edges']:
            if lab == 'E2':
                if ex['name'] in g and sorted(map(sorted, g[ex['name']])) != sorted(map(sorted, e)):
                    print('!! edge list in example differs from list item for', ex['name'])
                g.setdefault(ex['name'], [tuple(x) for x in e])
                break
    g['d4reg5a'] = list(itertools.combinations(range(5), 2))
    g['d5reg6a'] = list(itertools.combinations(range(6), 2))
    g['d4reg6a'] = [(0, 1), (0, 2), (0, 4), (0, 5), (1, 2), (1, 3), (1, 4), (2, 3), (2, 5), (3, 4), (3, 5), (4, 5)]
    return g

GR = build_graphs()

def G_of(name):
    G = nx.Graph(); G.add_edges_from(GR[name]); return G

def perm_dict(gen, n):
    p = list(range(n))
    for cyc in gen:
        for i, a in enumerate(cyc):
            p[a] = cyc[(i + 1) % len(cyc)]
    return p

def is_aut(G, p):
    return all(G.has_edge(p[u], p[v]) for u, v in G.edges())

def orbits(n, gens):
    parent = list(range(n))
    def f(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for p in gens:
        for i in range(n):
            a, b = f(i), f(p[i])
            if a != b: parent[a] = b
    cl = {}
    for i in range(n): cl.setdefault(f(i), []).append(i)
    return sorted(cl.values())

def image_graph(G, phi):
    H = nx.Graph(); H.add_nodes_from(set(phi.values()))
    for u, v in G.edges():
        if phi[u] != phi[v]: H.add_edge(phi[u], phi[v])
    return H

def harmonic_data(G, H, phi):
    """Return (ok, m, nu, deg, reasons)."""
    m, nu, bad = {}, {}, []
    for x in G.nodes():
        nu[x] = sum(1 for y in G[x] if phi[y] == phi[x])
        cnt = {w: 0 for w in H[phi[x]]}
        for y in G[x]:
            if phi[y] != phi[x]:
                if phi[y] not in cnt: bad.append(f'nbr {y} of {x} maps to non-adjacent'); continue
                cnt[phi[y]] += 1
        vals = set(cnt.values())
        if len(vals) > 1: bad.append(f'x={x}: counts {cnt}')
        m[x] = vals.pop() if vals else 0
    degs = set()
    for a, b in H.edges():
        degs.add(sum(1 for u, v in G.edges() if {phi[u], phi[v]} == {a, b}))
    return (not bad), m, nu, degs, bad

def genus(G): return G.number_of_edges() - G.number_of_nodes() + 1

def partition(phi):
    cl = {}
    for x, v in phi.items(): cl.setdefault(v, []).append(x)
    return sorted(sorted(c) for c in cl.values())

def relabel_iso(H, E1):
    """Is H identical (as labeled graph) to E1? else isomorphic?"""
    K = nx.Graph(); K.add_edges_from(E1)
    same = set(map(frozenset, H.edges())) == set(map(frozenset, K.edges())) and set(H.nodes()) == set(K.nodes())
    return same, nx.is_isomorphic(H, K)

if __name__ == '__main__':
    for ex in D['examples']:
        name = ex['name']
        G = G_of(name); n = G.number_of_nodes()
        out = []
        tab_parts = []
        for t in ex['tables']:
            rows = t['rows']
            phi = {r[0]: r[1] for r in rows}
            issues = []
            if sorted(phi) != list(range(n)): issues.append('table rows != vertex set')
            H = image_graph(G, phi)
            ok, m, nu, degs, bad = harmonic_data(G, H, phi)
            if not ok: issues.append('NOT HARMONIC: ' + '; '.join(bad[:4]))
            mt = {r[0]: r[2] for r in rows}; nt = {r[0]: r[3] for r in rows}
            dm = [x for x in phi if mt[x] != m[x]]; dn = [x for x in phi if nt[x] != nu[x]]
            if dm: issues.append('m wrong at ' + ', '.join(f'{x}:tab {mt[x]} true {m[x]}' for x in dm))
            if dn: issues.append('nu wrong at ' + ', '.join(f'{x}:tab {nt[x]} true {nu[x]}' for x in dn))
            if len(degs) != 1: issues.append(f'degree not constant {degs}')
            d = degs.pop() if degs else None
            if t['deg'] is not None and t['deg'] != d: issues.append(f"deg: tab {t['deg']} true {d}")
            if t['g1'] is not None and t['g1'] != genus(H): issues.append(f"genus G1: tab {t['g1']} true {genus(H)}")
            if t['g2'] is not None and t['g2'] != genus(G): issues.append(f"genus G2: tab {t['g2']} true {genus(G)}")
            # Riemann-Hurwitz with true data
            if ok and d:
                lhs = 2 * genus(G) - 2
                rhs = d * (2 * genus(H) - 2) + sum(2 * (m[x] - 1) + nu[x] for x in G)
                if lhs != rhs: issues.append(f'RH fails {lhs} vs {rhs}')
            tab_parts.append(partition(phi))
            # E1 preceding this table (nearest before)
            e1s = [e for p, e in ex['E1'] if p < t['pos']]
            e1note = ''
            if e1s:
                same, iso = relabel_iso(H, [tuple(x) for x in e1s[-1]])
                e1note = f' E1(prev) labeled-match={same} iso={iso}'
            out.append(f"  table@L{t['line']}: harmonic={ok} deg={d} g1={genus(H)} |V1|={H.number_of_nodes()} |E1|={H.number_of_edges()}{e1note}" +
                       ('' if not issues else '\n      ISSUES: ' + ' | '.join(issues)))
        for g in ex['groups']:
            ps = [perm_dict(c, n) for c in g['gens']]
            notaut = [i for i, p in enumerate(ps) if not is_aut(G, p)]
            orb = orbits(n, ps)
            phi = {x: i for i, o in enumerate(orb) for x in o}
            H = image_graph(G, phi)
            ok, m, nu, degs, bad = harmonic_data(G, H, phi)
            match = [i for i, tp in enumerate(tab_parts) if tp == orb]
            out.append(f"  G@L{g['line']}: gens={g['gens']} aut={'OK' if not notaut else 'NO gens '+str(notaut)} "
                       f"orbits={len(orb)} quotient harmonic={ok} |V1|={H.number_of_nodes()} |E1|={H.number_of_edges()} g1={genus(H)} matches table#{match}")
        print(f"{name} (L{ex['line']}) n={n} |E|={G.number_of_edges()} genus={genus(G)}")
        print('\n'.join(out))
