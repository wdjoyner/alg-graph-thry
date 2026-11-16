import subprocess, networkx as nx
from counts import GR, T
from verify import image_graph, harmonic_data
from gaptools import aut_group, libgap
def maps(name, t):
    G = nx.Graph(GR[name]); H = T[t]
    inp = f"{G.number_of_nodes()} {G.number_of_edges()} "+' '.join(f'{u} {v}' for u,v in G.edges())+f" {H.number_of_nodes()} {H.number_of_edges()} "+' '.join(f'{u} {v}' for u,v in H.edges())
    out = subprocess.run(['./countp','-p'],input=inp,capture_output=True,text=True).stdout.strip().split('\n')
    res = []
    for l in out[:-1]:
        phi = dict(enumerate(map(int, l.split())))
        ok, m, nu, d, _ = harmonic_data(G, H, phi)
        res.append((tuple(sorted(set(m.values()))), tuple(sorted(set(nu.values()))), tuple(d)))
    return res
from collections import Counter
for name, t, claim in [('d3reg8a','K4','all covers'),('d3reg8d','K4','all covers'),('d3reg12l','K4','all covers of degree 3'),
                       ('d4reg8c','C4','all multicovers'),('d4reg8c','K4','all quasicovers'),('d4reg8d','K4','all quasicovers'),
                       ('d4reg9e','C3','all quasicovers m=1 nu=2'),('d4reg9g','C3','some quasicovers m=1 nu=2'),
                       ('d3reg12m','C3','all quasicovers m=1 nu=1'),('d4reg12a','C3','all multicovers m=2 nu=0'),
                       ('d4reg12a','C4','some multicovers m=2 nu=0'),('d4reg12b','C3','all multicovers m=2 nu=0'),
                       ('d4reg12b','C4','all quasicovers m=1 nu=2'),('d5reg8b','C4','all m=2 nu=1'),('d5reg6a','C3','all m=2 nu=1 deg 4'),
                       ('d4reg6a','C3','2-multicovers deg 4'),('d3reg6a','C3','one quotient, quasicover nu=1'),('d3reg6b','C3','quasicover nu=1'),
                       ('d3reg12h','C3','some quasicovers')]:
    c = Counter(maps(name, t)); print(f'{name}->{t} [{claim}]: (m-values, nu-values, deg) -> count:', dict(c))
