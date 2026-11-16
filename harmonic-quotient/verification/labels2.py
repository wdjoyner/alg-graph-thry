import networkx as nx
from labels import tab
sun3 = nx.Graph([(0,1),(1,2),(0,2),(3,0),(3,1),(4,1),(4,2),(5,0),(5,2)])
twinC5 = nx.cycle_graph(5); twinC5.add_edges_from([(5,1),(5,4)])   # false twin of vertex 0
cotwin = nx.complement(twinC5)
K33me = nx.complete_bipartite_graph(3,3); K33me.remove_edge(0,3)
chouse = nx.complement(nx.Graph([(0,1),(1,2)]+[]).copy()); chouse = nx.complement(nx.disjoint_union(nx.path_graph(3), nx.empty_graph(2)))
print('d4reg9a S3 is 3-sun:', nx.is_isomorphic(tab('d4reg9a',1), sun3))
print('d4reg9g S3 is 3-sun:', nx.is_isomorphic(tab('d4reg9g',0), sun3))
print('d3reg12n tab0 co-twin-C5:', nx.is_isomorphic(tab('d3reg12n',0), cotwin), ' codomino:', nx.is_isomorphic(tab('d3reg12n',0), nx.complement(nx.grid_2d_graph(2,3))))
print('d3reg12n tab2 twin-C5:', nx.is_isomorphic(tab('d3reg12n',2), twinC5))
print('d3reg12n tab1 == tab2 type?', nx.is_isomorphic(tab('d3reg12n',1), tab('d3reg12n',2)))
print('d3reg12h tab1 K33-e:', nx.is_isomorphic(tab('d3reg12h',1), K33me))
print('d4reg9h complete house:', nx.is_isomorphic(tab('d4reg9h',0), chouse))
print('d4reg12c Ejmw = prism with C4 face -> K4?')
P = nx.circular_ladder_graph(3); P.add_edges_from([(0,4),(1,3)])
print('   ', nx.is_isomorphic(tab('d4reg12c',1), P))
