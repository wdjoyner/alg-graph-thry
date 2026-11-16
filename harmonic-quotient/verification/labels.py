import networkx as nx
from verify import D, G_of, image_graph
def tab(name, k):
    ex = [e for e in D['examples'] if e['name']==name][0]
    phi = {r[0]: r[1] for r in ex['tables'][k]['rows']}
    return image_graph(G_of(name), phi)
print('d3reg10m P3 degrees:', dict(tab('d3reg10m',1).degree()))
print('d3reg10o St4 degrees:', dict(tab('d3reg10o',2).degree()))
print('d4reg8f P3 degrees:', dict(tab('d4reg8f',0).degree()))
print('d3reg10s St4 degrees:', dict(tab('d3reg10s',0).degree()))
print('d5reg8a St4 degrees:', dict(tab('d5reg8a',0).degree()))
# H-tree: d3reg10n G=<(0,8,2)(3,5,7)>
from verify import perm_dict, orbits
G=G_of('d3reg10n'); o=orbits(10,[perm_dict([(0,8,2),(3,5,7)],10)]); phi={x:i for i,b in enumerate(o) for x in b}
Q=image_graph(G,phi); print('H-tree iso:', nx.is_isomorphic(Q, nx.Graph([(0,1),(0,3),(0,5),(1,2),(1,4)])))
# coantenna: complement of house + pendant at the roof apex
ant = nx.Graph([(0,1),(1,2),(2,3),(3,0),(0,4),(1,4),(4,5)])
print('coantenna iso:', nx.is_isomorphic(nx.complement(ant), tab.__globals__['image_graph'](G_of('d4reg9a'), {x:v for x,v in zip(range(9),[0,1,1,2,3,3,4,5,5])})))
# named quotient graphs from tables
named = {
 'diamond': nx.Graph([(0,1),(0,2),(1,2),(1,3),(2,3)]), 'K4': nx.complete_graph(4), 'C4': nx.cycle_graph(4),
 'house': nx.house_graph(), 'K23': nx.complete_bipartite_graph(2,3), 'C5': nx.cycle_graph(5),
 'prism': nx.circular_ladder_graph(3), 'K33': nx.complete_bipartite_graph(3,3),
 'barbell30': nx.barbell_graph(3,0), 'C3': nx.cycle_graph(3), 'C6': nx.cycle_graph(6),
 'K5': nx.complete_graph(5), 'K5-e': nx.Graph([e for e in nx.complete_graph(5).edges() if e!=(0,1)]),
 'W5': nx.wheel_graph(5), 'oct': nx.octahedral_graph(), 'paw': nx.Graph([(0,1),(1,2),(0,2),(2,3)]),
 'butterfly': nx.Graph([(0,1),(0,2),(1,2),(0,3),(0,4),(3,4)]), 'St4': nx.star_graph(3), 'St6': nx.star_graph(5),
 'P3': nx.path_graph(3), 'P4': nx.path_graph(4), 'bull': nx.Graph([(0,1),(1,2),(0,2),(0,3),(1,4)]),
 'codomino': None, 'gem': nx.Graph([(0,1),(1,2),(2,3),(4,0),(4,1),(4,2),(4,3)]),
 'circ6_1245': nx.circulant_graph(6,[1,2]), 'banner': nx.Graph([(0,1),(1,2),(2,3),(3,0),(0,4)]),
 'R(E@JW)': nx.from_graph6_bytes(b'E@JW'), 'EL~o': nx.from_graph6_bytes(b'EL~o'), 'E@~o': nx.from_graph6_bytes(b'E@~o'),
 'EUjo': nx.from_graph6_bytes(b'EUjo'), 'EUYo': nx.from_graph6_bytes(b'EUYo'), 'D]w': nx.from_graph6_bytes(b'D]w'),
 'DF{': nx.from_graph6_bytes(b'DF{'), 'Dh{': nx.from_graph6_bytes(b'Dh{'), 'D~k': nx.from_graph6_bytes(b'D~k'),
 'EJ~o': nx.from_graph6_bytes(b'EJ~o'), 'FCdzo': nx.from_graph6_bytes(b'FCdzo'), 'DrG': nx.from_graph6_bytes(b'DrG'),
 'H??E\\hw': nx.from_graph6_bytes(b'H??E\\hw'), 'G?r@xw': nx.from_graph6_bytes(b'G?r@xw'), 'FKMiw': nx.from_graph6_bytes(b'FKMiw'),
 'E]~o': nx.from_graph6_bytes(b'E]~o'), 'Ejmw': nx.from_graph6_bytes(b'Ejmw'), 'G?qipk': nx.from_graph6_bytes(b'G?qipk'),
 'FB]lg': nx.from_graph6_bytes(b'FB]lg'), 'FKLkw': nx.from_graph6_bytes(b'FKLkw'),
}
# codomino: two squares sharing an edge (domino) complement? codomino = complement of domino
named['codomino'] = nx.complement(nx.grid_2d_graph(2,3))
named['X37']=None
def ident(Q):
    return [k for k,v in named.items() if v is not None and nx.is_isomorphic(Q,v)]
for ex in D['examples']:
    for k,t in enumerate(ex['tables']):
        Q = tab(ex['name'],k)
        print(f"{ex['name']} table#{k} L{t['line']}: |V1|={Q.number_of_nodes()} |E1|={Q.number_of_edges()} ->", ident(Q), nx.to_graph6_bytes(Q,header=False).decode().strip())
