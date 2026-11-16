from verify import G_of, image_graph, harmonic_data, genus, perm_dict, orbits
import networkx as nx
def table_for(name, gens, labels=None):
    G = G_of(name); n = G.number_of_nodes()
    ps = [perm_dict(c, n) for c in gens]
    orb = orbits(n, ps)
    phi = {x: (labels[i] if labels else i) for i, o in enumerate(orb) for x in o}
    Q = image_graph(G, phi); ok, m, nu, degs, bad = harmonic_data(G, Q, phi)
    print(f'--- {name}  G=<{gens}>  harmonic={ok} deg={degs} g1={genus(Q)} E1={sorted(tuple(sorted(e)) for e in Q.edges())}')
    print('    degrees in quotient:', dict(Q.degree()))
    print('    x  : ' + ' '.join(f'{x:>2}' for x in range(n)))
    print('    phi: ' + ' '.join(f'{phi[x]:>2}' for x in range(n)))
    print('    m  : ' + ' '.join(f'{m[x]:>2}' for x in range(n)))
    print('    nu : ' + ' '.join(f'{nu[x]:>2}' for x in range(n)))
    return Q
# d3reg8e correct C4 table: label orbits so that quotient is the cycle 0-1-2-3-0
Q = table_for('d3reg8e', [[(0,7),(1,6),(2,5),(3,4)]])
# d4reg9a coantenna
Q = table_for('d4reg9a', [[(1,2),(4,5),(7,8)]])
print('    coantenna? complement of antenna; quotient graph6:', nx.to_graph6_bytes(Q, header=False).decode().strip())
# d4reg12d butterfly
Q = table_for('d4reg12d', [[(1,11),(3,4),(6,8),(9,10)], [(0,2),(1,11),(3,10),(4,9),(5,7),(6,8)]])
print('    butterfly iso:', nx.is_isomorphic(Q, nx.Graph([(0,1),(0,2),(1,2),(0,3),(0,4),(3,4)])))
# d3reg12h: stated G3 (gives 2 orbits) and <a> where a is first gen of the true G3
table_for('d3reg12h', [[(0,5),(1,2),(3,4),(6,11),(7,10),(8,9)]])
# d3reg10s stated G
Q=table_for('d3reg10s', [[(0,4),(1,3),(5,9),(6,8)], [(0,4),(1,9),(2,7),(3,5)]])
