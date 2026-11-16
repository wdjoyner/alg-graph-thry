import subprocess, networkx as nx, re
from verify import GR, G_of
GR['d3reg6a'] = list(nx.circulant_graph(6,[2,3]).edges()); GR['d3reg6b'] = list(nx.complete_bipartite_graph(3,3).edges())
T = {'P3': nx.path_graph(3), 'P4': nx.path_graph(4), 'P5': nx.path_graph(5), 'P6': nx.path_graph(6), 'St4': nx.star_graph(3),
     'C3': nx.cycle_graph(3), 'C4': nx.cycle_graph(4), 'K4': nx.complete_graph(4),
     'diamond': nx.Graph([(0,1),(0,2),(1,2),(1,3),(2,3)])}
S = """d3reg6a: St4 360, P3 36, P4 102, P5 12, C3 6, P6 0, diamond 0, K4 0
d3reg6b: St4 444, P3 48, P4 72, P5 72, C3 36, P6 0, diamond 0, K4 0
d3reg8a: St4 0, P4 0, C3 0, C4 0, P3 2, diamond 8, K4 48
d3reg8b: P3 2, diamond 4, St4 0, P4 0, C3 0, C4 0, K4 0
d3reg8c: St4 6, P3 6, diamond 0, P4 0, C3 0, C4 0, K4 0
d3reg8d: diamond 24, C4 24, P3 12, K4 24, P4 0, C3 0, St4 0
d3reg8e: C4 8, P3 4, C3 0, St4 0, P4 0, K4 0
d3reg10a: P3 8, P4 0, St4 0, C3 0, C4 0, K4 0
d3reg10b: diamond 0, St4 0, P3 0, C3 0, C4 0, K4 0
d3reg10c: P3 8, C3 6, diamond 0, St4 0, P4 0, C4 0, K4 0
d3reg10d: St4 12, P3 12, C3 12, diamond 0, P4 0, C4 0, K4 0
d3reg10e: P3 4, St4 0, P4 0, C3 0, C4 0, K4 0
d3reg10f: P3 2, St4 0, P4 0, C3 0, C4 0, K4 0
d3reg10g: St4 6, P3 6, P4 0, C3 0, C4 0, K4 0
d3reg10h: P3 2, St4 0, P4 0, C3 0, C4 0, K4 0
d3reg10i: St4 6, P3 6, P4 0, C3 0, C4 0, K4 0
d3reg10j: P3 6, St4 0, P4 0, C3 0, C4 0, K4 0
d3reg10k: P3 6, St4 0, P4 0, C3 0, C4 0, K4 0
d3reg10l: St4 0, P4 0, C3 0, C4 0, K4 0, P3 6
d3reg10m: P3 2, St4 0, P4 0, C4 0, K4 0
d3reg10n: St4 18, P3 22, P4 8, C3 0, C4 0, K4 0, P5 0
d3reg10o: St4 6, P3 8, P4 0, C3 0, C4 0, K4 0
d3reg10p: P3 2, St4 0, P4 0, C3 0, C4 0, K4 0
d3reg10q: P3 10, St4 0, P4 0, C3 0, C4 0, K4 0
d3reg10r: P3 10, St4 0, P4 0, C3 0, C4 0, K4 0
d3reg10s: St4 30, P3 30, P4 0, C3 0, C4 0, K4 0
d3reg12a: St4 0, P4 0, C3 0, C4 0, K4 0, P3 12
d3reg12b: St4 0, P4 0, C4 0, K4 0, P3 14, C3 6
d3reg12c: St4 0, P4 0, C3 0, C4 0, K4 0, P3 6
d3reg12d: St4 12, P3 22, C3 12, P4 0, C4 0, K4 0
d3reg12e: St4 0, P4 0, C4 0, K4 0, P3 4, C3 6
d3reg12f: P3 12, C3 36, St4 12, P4 0, C4 0, K4 0
d3reg12g: St4 12, C3 6, P3 0, P4 0, C4 0, K4 0
d3reg12h: C3 168, St4 48, P3 56, P4 0, C4 0, K4 0
d3reg12i: C3 42, P3 12, St4 12, P4 0, C4 0, K4 0
d3reg12j: P3 24, C3 24, P4 2, St4 0, C4 0, K4 0, P5 0
d3reg12k: St4 0, C3 0, C4 0, P4 0, K4 0, P3 4
d3reg12l: P3 12, C3 6, P4 6, K4 24, C4 0, St4 0
d3reg12m: C4 0, K4 0, P3 30, P4 6, St4 12, C3 36, P5 0
d3reg12n: P3 42, St4 18, C3 0, C4 0, P4 0, K4 0
d4reg5a: C3 0, K4 0, St4 0, P4 0, C4 0
d4reg6a: St4 0, P4 0, C4 0, K4 0, P3 6, C3 6
d4reg7a: St4 0, P3 0, P4 0, C3 0, C4 0, K4 0
d4reg7b: C3 0, C4 0, P4 0, K4 0, St4 6, P3 8
d4reg8a: St4 0, P3 0, P4 0, C4 0, K4 0, C3 12
d4reg8b: K4 24, C3 36, St4 0, P3 0, P4 0, C4 0
d4reg8c: P3 36, C4 72, K4 576, St4 48, C3 0, P4 0
d4reg8d: St4 0, P4 0, C4 0, P3 4, C3 6, K4 48
d4reg8e: St4 0, P3 0, P4 0, C4 0, K4 0, C3 6
d4reg8f: St4 0, P4 0, C3 0, C4 0, K4 0, P3 2
d4reg9a: St4 0, P4 0, C4 0, K4 0, P3 2, C3 24
d4reg9b: St4 0, P3 0, P4 0, C3 0, C4 0, K4 0
d4reg9c: St4 0, P3 0, P4 0, C4 0, K4 0, C3 6
d4reg9d: P4 0, C3 0, C4 0, K4 0, P3 2
d4reg9e: St4 0, P4 0, C4 0, K4 0, C3 6, P3 6
d4reg9f: St4 0, P3 0, P4 0, C4 0, K4 0, C3 6
d4reg9g: St4 0, P4 0, C4 0, K4 0, P3 18, C3 78
d4reg9h: C3 0, C4 0, P4 0, K4 0, P3 8
d4reg9i: St4 0, P3 0, P4 0, C4 0, K4 0, C3 6
d4reg10a: P4 0, C3 0, C4 0, K4 0, P3 2
d4reg10b: P4 0, C4 0, K4 0, P3 4, C3 12
d4reg10c: P3 0, P4 0, C4 0, K4 0, C3 6
d4reg10d: P3 0, C3 0, C4 0, K4 0
d4reg10e: C3 0, P4 0, K4 0, P3 40, C4 80
d4reg10f: P4 0, C4 0, K4 0, C3 90, P3 20
d4reg11a: P4 0, C3 0, C4 0, K4 0, P3 10
d4reg11b: P3 0, P4 0, C4 0, K4 0, C3 6
d4reg11c: P3 0, P4 0, C3 0, C4 0, K4 0
d4reg11d: P3 0, P4 0, C3 0, C4 0, K4 0
d4reg11e: P3 0, P4 0, C4 0, K4 0, C3 6
d4reg11f: P3 9466, P4 16014, C3 0, K4 0, C4 3488
d4reg11g: P3 8642, C4 2304, K4 0
d4reg12a: C3 6, C4 272, P3 82, P4 6, K4 0
d4reg12b: C3 6, C4 8, P3 10, P4 0, K4 0
d4reg12c: P3 12, C3 36, P4 0, C4 0, K4 0
d4reg12d: C3 240, P3 20, C4 24, P4 0, K4 0
d4reg12e: C3 42, P3 6, C4 0, P4 0, K4 0
d4reg12f: C4 48, P3 32, P4 2, C3 0, K4 0
d5reg6a: C3 90
d5reg8a: P3 0, P4 0, C3 0, C4 0, K4 0
d5reg8b: P3 4, C3 48, C4 8, P4 0, K4 0
d5reg8c: C3 12, P3 0, P4 0, C4 0, K4 0
d5reg10a: P3 0, P4 0, C3 0, C4 0, K4 0
d5reg10b: P3 0, P4 0, C3 0, C4 0, K4 0
d5reg10c: P3 10, C3 60, P4 0, C4 0, K4 0
d5reg10d: P4 0, C3 0, C4 0, K4 0, P3 100"""
def run(E2, H):
    G = nx.Graph(E2); n=G.number_of_nodes()
    inp = f"{n} {G.number_of_edges()} " + ' '.join(f'{u} {v}' for u,v in G.edges()) + f" {H.number_of_nodes()} {H.number_of_edges()} " + ' '.join(f'{u} {v}' for u,v in H.edges())
    out = subprocess.run(['./count'], input=inp, capture_output=True, text=True).stdout.split()
    return int(out[0]), int(out[1])
bad = 0
for line in S.split('\n'):
    name, rest = line.split(':')
    res = []
    for tok in rest.split(','):
        t, c = tok.split(); c = int(c)
        nc, su = run(GR[name], T[t])
        flag = '' if su == c else f'  <-- stated {c}'
        if nc != su: flag += f' (nonconstant non-surjective: {nc-su})'
        if flag: bad += 1
        res.append(f'{t}={su}{flag}')
    print(name, ', '.join(res))
print('mismatches:', bad)
