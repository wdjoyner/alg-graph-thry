import networkx as nx
from gaptools import aut_group, gap_orbits, gens_str, libgap, harmonic_quotients
from verify import G_of, perm_dict, orbits, image_graph, harmonic_data
def gp(name, gens):
    G, A, o = aut_group(name); n = G.number_of_nodes()
    from gaptools import gap_perm
    return libgap.Group([gap_perm(perm_dict(c, n)) for c in gens])
for name, gens in [('d5reg10a', [[(0,8),(1,5),(2,7),(3,6),(4,9)]]), ('d5reg10c', [[(0,9),(1,2),(3,5),(4,6),(7,8)]]), ('d5reg10d', [[(1,5,8,2,6)]])]:
    G, A, o = aut_group(name); Z = libgap.Centre(A)
    print(name, '|Z(Aut)|=', libgap.Size(Z), ' stated G == centre:', libgap.Size(Z)==libgap.Size(gp(name,gens)) and libgap.IsSubset(Z, gp(name,gens)))
G, A, o = aut_group('d5reg10b'); Z = libgap.Centre(A); print('d5reg10b |Z|=', libgap.Size(Z), 'gens', gens_str(Z))
n=10; orb = gap_orbits(Z, n); phi={x:i for i,b in enumerate(orb) for x in b}; Gr=G_of('d5reg10b'); Q=image_graph(Gr,phi); ok,m,nu,d,_=harmonic_data(Gr,Q,phi)
print('   quotient by centre: K5?', nx.is_isomorphic(Q,nx.complete_graph(5)), 'harmonic', ok, 'm', set(m.values()), 'nu', set(nu.values()), 'deg', d)
print('d3reg8c second G order', libgap.Size(gp('d3reg8c', [[(1,2),(3,5)],[(0,2,1),(3,5,7)]])))
print('d4reg8f G1,G2 orders', libgap.Size(gp('d4reg8f', [[(1,2)],[(0,4,3),(5,7,6)]])), libgap.Size(gp('d4reg8f', [[(1,2),(3,4),(6,7)],[(0,4,3),(5,7,6)]])))
# d3reg12j table of subgroups
rows = [([[(0,6),(1,7),(2,8),(3,9),(4,10),(5,11)]],'prism'),([[(0,6),(1,8),(2,7),(3,10),(4,9),(5,11)]],'prism'),
 ([[(0,5),(1,4),(2,3),(6,11),(7,10),(8,9)]],'barbell'),([[(0,11),(1,9),(2,10),(3,7),(4,8),(5,6)]],'codomino'),
 ([[(0,11),(1,10),(2,9),(3,8),(4,7),(5,6)]],'codomino'),
 ([[(0,5),(1,4),(2,3),(6,11),(7,10),(8,9)],[(0,6),(1,7),(2,8),(3,9),(4,10),(5,11)]],'C3'),
 ([[(0,5),(1,4),(2,3),(6,11),(7,10),(8,9)],[(0,6),(1,8),(2,7),(3,10),(4,9),(5,11)]],'C3'),
 ([[(1,2),(3,4),(7,8),(9,10)],[(0,11),(1,10,2,9),(3,8,4,7),(5,6)]],'P4'),
 ([[(1,2),(3,4),(7,8),(9,10)],[(0,11),(1,9),(2,10),(3,7),(4,8),(5,6)]],'P4'),
 ([[(7,8),(9,10)],[(1,2),(3,4)],[(0,11),(1,9),(2,10),(3,7),(4,8),(5,6)]],'P4'),
 ([[(1,2),(3,4),(7,8),(9,10)],[(0,5),(1,3),(2,4),(6,11),(7,9),(8,10)],[(0,6),(1,7),(2,8),(3,9),(4,10),(5,11)]],'P2'),
 ([[(1,2),(3,4),(7,8),(9,10)],[(0,5),(1,3),(2,4),(6,11),(7,10),(8,9)],[(0,6),(1,7),(2,8),(3,9),(4,10),(5,11)]],'P2'),
 ([[(1,2),(3,4),(7,8),(9,10)],[(0,5),(1,3),(2,4),(6,11),(7,9),(8,10)],[(0,6),(1,8,2,7),(3,10,4,9),(5,11)]],'P2'),
 ([[(1,2),(3,4),(7,8),(9,10)],[(0,5),(1,3),(2,4),(6,11),(7,10),(8,9)],[(0,6),(1,8,2,7),(3,10,4,9),(5,11)]],'P2')]
Gr = G_of('d3reg12j')
from verify import is_aut
for gens, lab in rows:
    ps=[perm_dict(c,12) for c in gens]; aut=all(is_aut(Gr,p) for p in ps); orb=orbits(12,ps); phi={x:i for i,b in enumerate(orb) for x in b}
    Q=image_graph(Gr,phi); ok=harmonic_data(Gr,Q,phi)[0]
    print('d3reg12j row', lab, 'aut', aut, '|V1|', len(orb), '|E1|', Q.number_of_edges(), 'harmonic', ok)
for name in ['d4reg12d','d4reg12e']:
    for H, orb, Q, m, nu, d in harmonic_quotients(name):
        if len(orb)==3 and Q.number_of_edges()==3:
            print(name, 'C3 quotient m', sorted(set(m.values())), 'nu', sorted(set(nu.values())), 'deg', d, 'fiber sizes', sorted(len(o) for o in orb)); break
for H, orb, Q, m, nu, d in harmonic_quotients('d4reg12e'):
    if len(orb)==6: print('d4reg12e oct quotient: cover?', set(m.values()), set(nu.values()))
