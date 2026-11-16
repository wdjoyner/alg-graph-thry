"""GAP helpers: automorphism group of a graph and its subgroups."""
from sage.all__sagemath_gap import libgap
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
from verify import G_of, image_graph, harmonic_data, genus, partition

_cache = {}

def all_auts(G):
    n = G.number_of_nodes()
    return [tuple(m[i] for i in range(n)) for m in GraphMatcher(G, G).isomorphisms_iter()]

def gap_perm(p):
    return libgap.PermList([x + 1 for x in p])

def aut_group(name):
    if name in _cache: return _cache[name]
    G = G_of(name)
    auts = all_auts(G)
    A = libgap.Group(libgap.eval('()'))
    for p in auts:
        gp = gap_perm(p)
        if not libgap.IsSubset(A, libgap.Group(gp)):
            A = libgap.ClosureGroup(A, gp)
    _cache[name] = (G, A, len(auts))
    return _cache[name]

def gap_orbits(H, n):
    orbs = libgap.OrbitsDomain(H, libgap.eval(f'[1..{n}]'))
    return sorted(sorted(int(x) - 1 for x in o) for o in orbs)

def harmonic_quotients(name, include_trivial=False):
    """List of (subgroup, orbit partition, quotient graph, m, nu, deg) for all subgroups whose
    quotient map is harmonic and non-constant."""
    G, A, order = aut_group(name)
    n = G.number_of_nodes()
    out = []
    for H in libgap.AllSubgroups(A):
        if int(libgap.Size(H)) == 1 and not include_trivial: continue
        orb = gap_orbits(H, n)
        if len(orb) < 2: continue
        phi = {x: i for i, o in enumerate(orb) for x in o}
        Q = image_graph(G, phi)
        ok, m, nu, degs, bad = harmonic_data(G, Q, phi)
        if ok:
            out.append((H, orb, Q, m, nu, degs.pop() if degs else None))
    return out

def gens_str(H):
    gens = libgap.SmallGeneratingSet(H)
    s = []
    for g in gens:
        cyc = str(g)
        # convert 1-based cycle notation to 0-based
        import re
        cyc = re.sub(r'\d+', lambda mm: str(int(mm.group()) - 1), cyc)
        s.append(cyc)
    return ', '.join(s)
