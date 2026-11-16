import networkx as nx, numpy as np, itertools
from verify import G_of
def chrom(G):
    n=G.number_of_nodes()
    for k in range(1,n+1):
        col={}
        order=sorted(G, key=lambda v:-G.degree(v))
        def bt(i):
            if i==n: return True
            v=order[i]
            for c in range(k):
                if all(col.get(w)!=c for w in G[v]):
                    col[v]=c
                    if bt(i+1): return True
                    del col[v]
            return False
        if bt(0): return k
def spec(G): return sorted(np.round(np.linalg.eigvalsh(nx.to_numpy_array(G)),6).tolist(), reverse=True)
def dreg(G): return nx.is_distance_regular(G)
def circ(n,L): return nx.circulant_graph(n,L)
C = {'d3reg6a?':None}
for nm,k in [('d4reg8a',4),('d4reg8b',4),('d4reg8c',2),('d4reg8d',3),('d4reg8e',3),('d4reg8f',4),('d4reg10e',3),('d4reg12d',3),('d4reg12e',3),
             ('d5reg8a',4),('d5reg8b',4),('d5reg8c',4),('d5reg10a',5),('d5reg10b',4),('d5reg10c',5),('d5reg10d',2),('d3reg12l',3)]:
    c=chrom(G_of(nm)); print(nm,'chromatic stated',k,'true',c, '' if c==k else '  <-- MISMATCH')
checks = [('d4reg8c', circ(8,[1,3])), ('d4reg10e', circ(10,[1,4])), ('d4reg10e', circ(10,[2,3])),
          ('d4reg12a', circ(12,[1,5])), ('d4reg12b', circ(12,[1,4])), ('d4reg12b', circ(12,[4,5])),
          ('d4reg12e', circ(12,[1,2])), ('d4reg12e', circ(12,[2,5])), ('d5reg10d', circ(10,[1,3,5])),
          ('d5reg10d', nx.complete_bipartite_graph(5,5)), ('d4reg8c', nx.complete_bipartite_graph(4,4)),
          ('d4reg12d', nx.from_graph6_bytes(b'K~zzzzzzz~~z')) ]
for nm,H in checks[:-1]: print(nm,'iso to', sorted(H.edges())[:3],'...', nx.is_isomorphic(G_of(nm),H))
# strong product C4 x P2
S = nx.strong_product(nx.cycle_graph(4), nx.path_graph(2)); print('d5reg8b ~ C4 strong P2:', nx.is_isomorphic(G_of('d5reg8b'),S))
# cuboctahedron = line graph of cube
print('d4reg12d ~ cuboctahedron (line graph of Q3):', nx.is_isomorphic(G_of('d4reg12d'), nx.line_graph(nx.hypercube_graph(3))))
print('d4reg9g ~ Paley(9):', nx.is_isomorphic(G_of('d4reg9g'), nx.paley_graph(9).to_undirected()))
print('d4reg6a ~ octahedral:', nx.is_isomorphic(G_of('d4reg6a'), nx.octahedral_graph()))
print('d5reg10a ~ K5 x K2 prism:', nx.is_isomorphic(G_of('d5reg10a'), nx.cartesian_product(nx.complete_graph(5), nx.path_graph(2))))
print('d4reg10f ~ K55 minus matching:', nx.is_isomorphic(G_of('d4reg10f'), circ(10,[1,3])))
print('d3reg12l ~ truncated tetrahedron:', nx.is_isomorphic(G_of('d3reg12l'), nx.truncated_tetrahedron_graph()))
print('d3reg12n ~ Franklin:', nx.is_isomorphic(G_of('d3reg12n'), nx.LCF_graph(12,[5,-5],6)))
print('d3reg10s ~ Petersen:', nx.is_isomorphic(G_of('d3reg10s'), nx.petersen_graph()))
print('d3reg8e ~ Wagner (Moebius M8):', nx.is_isomorphic(G_of('d3reg8e'), circ(8,[1,4])))
for nm in ['d3reg8d','d3reg10s','d4reg6a','d4reg9g','d4reg10f','d4reg12d','d5reg10d','d4reg10e','d4reg12a','d4reg8c']:
    print(nm,'distance regular:', dreg(G_of(nm)))
for nm in ['d3reg10n','d3reg12m','d4reg6a','d4reg9h','d3reg10s']:
    print(nm,'spectrum', spec(G_of(nm)))
