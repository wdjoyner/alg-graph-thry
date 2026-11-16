import networkx as nx, time
from gaptools import aut_group, gap_orbits, libgap
from verify import image_graph, harmonic_data
t0=time.time()
G, A, o = aut_group('d5reg10d'); n=10
tally = {}
for cl in libgap.ConjugacyClassesSubgroups(A):
    H = libgap.Representative(cl); sz = int(libgap.Size(cl))
    if int(libgap.Size(H)) == 1: continue
    orb = gap_orbits(H, n)
    if len(orb) < 2: continue
    phi = {x:i for i,b in enumerate(orb) for x in b}; Q = image_graph(G, phi)
    if harmonic_data(G, Q, phi)[0]:
        key = (len(orb), Q.number_of_edges(), tuple(sorted(d for _,d in Q.degree())))
        tally[key] = tally.get(key, 0) + sz
print('K55 harmonic quotients (subgroups):', sum(tally.values()), tally, f'{time.time()-t0:.0f}s')
