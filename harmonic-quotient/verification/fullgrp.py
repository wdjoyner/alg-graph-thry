import sys
from gaptools import aut_group, gap_orbits
from verify import image_graph, harmonic_data
for name in sys.argv[1:]:
    G, A, order = aut_group(name); n = G.number_of_nodes()
    orb = gap_orbits(A, n)
    if len(orb) < 2: print(name, 'full Aut: vertex-transitive (constant)'); continue
    phi = {x: i for i, o in enumerate(orb) for x in o}
    Q = image_graph(G, phi); ok = harmonic_data(G, Q, phi)[0]
    print(name, f'full Aut quotient: {len(orb)} vertices, harmonic={ok}')
