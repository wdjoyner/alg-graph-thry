import networkx as nx, subprocess, sympy as sp, numpy as np
from networkx.algorithms.isomorphism import GraphMatcher
def load(f): return [nx.from_graph6_bytes(l.strip()) for l in open(f,'rb') if l.strip()]
def ham(G):
    n=G.number_of_nodes(); adj={v:set(G[v]) for v in G}
    def dfs(v,seen,k):
        if k==n: return 0 in adj[v]
        return any(dfs(w,seen|{w},k+1) for w in adj[v] if w not in seen)
    return dfs(0,{0},1)
def vt_et(G):
    h = nx.weisfeiler_lehman_subgraph_hashes(G, iterations=3)
    if len(set(h[v][-1] for v in G))>1: return False, False, None
    A=[m for m in GraphMatcher(G,G).isomorphisms_iter()]
    vt = len({m[0] for m in A})==G.number_of_nodes()
    u,v=next(iter(G.edges())); et = len({frozenset((m[u],m[v])) for m in A})==G.number_of_edges()
    return vt, et, len(A)
def count(G,H):
    inp=f"{G.number_of_nodes()} {G.number_of_edges()} "+' '.join(f'{u} {v}' for u,v in G.edges())+f" {H.number_of_nodes()} {H.number_of_edges()} "+' '.join(f'{u} {v}' for u,v in H.edges())
    return int(subprocess.run(['./count'],input=inp,capture_output=True,text=True).stdout.split()[1])
def kappa(G):
    L=sp.Matrix(nx.laplacian_matrix(G).toarray().astype(int).tolist()); return int(L[1:,1:].det())
C3=nx.cycle_graph(3)
for f in ['c8','c10','c12','q10','q11','q12','p10']:
    Gs=load(f+'.g6'); res=[vt_et(G) for G in Gs]
    vt=[r for r in res if r[0]]; et=[r for r in res if r[1]]
    nh=sum(1 for G in Gs if not ham(G))
    extra=''
    if f in ('c10','c12'):
        extra=f" non-Ham circumferences/notes computed separately"
    if f in ('q10','q11'):
        c3=[count(G,C3) for G in Gs]; extra+=f"  #with C3-morphism={sum(1 for c in c3 if c>0)}"
        if f=='q10':
            dr=[G for G,r in zip(Gs,res) if r[0] and nx.is_distance_regular(G)]; extra+=f"  #vt&distance-regular={len(dr)}"
        if f=='q11':
            ks=[kappa(G) for G in Gs]; extra+=f"  #odd kappa={sum(1 for k in ks if k%2)}"
            triv=[(c,) for G,c in zip(Gs,c3) if c>0 and len(list(GraphMatcher(G,G).isomorphisms_iter()))==1]
            extra+=f"  trivial-aut graphs with C3 maps: {len(triv)} (counts {sorted(set(t[0] for t in triv))})"
    print(f, 'n_graphs',len(Gs),'#vt',len(vt),'vt aut sizes',sorted(r[2] for r in vt),'#et',len(et),'#non-Ham',nh, extra, flush=True)
