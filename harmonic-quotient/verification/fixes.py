"""For every tabulated map, find subgroups of Aut whose orbit partition equals the table's
partition; for every stated G, report its orbit partition; print corrected rows where needed."""
import json, sys, time
from verify import D, G_of, image_graph, harmonic_data, genus, partition, perm_dict, orbits
from gaptools import aut_group, gap_orbits, gens_str, libgap

only = sys.argv[1:]
for ex in D['examples']:
    name = ex['name']
    if only and name not in only: continue
    if not ex['tables']: continue
    t0 = time.time()
    G, A, order = aut_group(name)
    n = G.number_of_nodes()
    subs = [H for H in libgap.AllSubgroups(A) if int(libgap.Size(H)) > 1]
    byp = {}
    for H in subs:
        byp.setdefault(tuple(map(tuple, gap_orbits(H, n))), []).append(H)
    print(f'== {name}: |Aut|={order}, #nontrivial subgroups={len(subs)} ({time.time()-t0:.1f}s)')
    for i, t in enumerate(ex['tables']):
        phi = {r[0]: r[1] for r in t['rows']}
        part = tuple(map(tuple, partition(phi)))
        Hs = byp.get(part, [])
        print(f'  table#{i} L{t["line"]}: partition {list(part)} realized by {len(Hs)} subgroups'
              + (f'; e.g. <{gens_str(min(Hs, key=lambda h: int(libgap.Size(h))))}> order {min(int(libgap.Size(h)) for h in Hs)}' if Hs else ''))
    for g in ex['groups']:
        ps = [perm_dict(c, n) for c in g['gens']]
        orb = orbits(n, ps)
        print(f'  G L{g["line"]}: orbits {orb}')
