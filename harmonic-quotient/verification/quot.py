import sys, time, networkx as nx
from gaptools import harmonic_quotients, aut_group, gens_str, libgap
from counts import GR
names = sys.argv[1:]
for name in names:
    t0=time.time()
    try:
        Q = harmonic_quotients(name)
    except Exception as e:
        print(name, 'ERR', e); continue
    reps = []  # (graph, label, [count subgroups], set(partitions))
    for H, orb, Qg, m, nu, d in Q:
        for r in reps:
            if r[0].number_of_nodes()==Qg.number_of_nodes() and nx.is_isomorphic(r[0], Qg):
                r[1]+=1; r[2].add(tuple(map(tuple,orb))); break
        else:
            reps.append([Qg, 1, {tuple(map(tuple,orb))}])
    reps.sort(key=lambda r: -r[0].number_of_nodes())
    desc = '; '.join(f"{nx.to_graph6_bytes(r[0],header=False).decode().strip()}(|V|={r[0].number_of_nodes()},|E|={r[0].number_of_edges()}): {r[1]} subgroups/{len(r[2])} distinct" for r in reps)
    byV = {}
    for r in reps: byV[r[0].number_of_nodes()] = byV.get(r[0].number_of_nodes(),0)+r[1]
    print(f"{name}: total {len(Q)}  byV {dict(sorted(byV.items(), reverse=True))}  [{time.time()-t0:.0f}s]\n    {desc}", flush=True)
