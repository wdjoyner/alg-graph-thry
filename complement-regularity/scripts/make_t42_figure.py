import networkx as nx, math, itertools
"""Emit the TikZ nodes and edges for Figure 2 (T(4,2) as the cuboctahedron, colored by fibers over J(4,2))."""
def T(n,k):
    V=list(itertools.permutations(range(n),k)); G=nx.Graph(); G.add_nodes_from(V)
    for x in V:
        for i in range(k):
            for c in range(n):
                if c not in x: G.add_edge(x,x[:i]+(c,)+x[i+1:])
    return G
G=T(4,2)
H=nx.Graph(); pos={}
for i in range(4):
    pos[('A',i)]=(1.0,45+90*i); pos[('C',i)]=(3.3,45+90*i); pos[('B',i)]=(2.0,90*i)
for i in range(4):
    H.add_edge(('A',i),('A',(i+1)%4)); H.add_edge(('C',i),('C',(i+1)%4))
    for t in 'AC': H.add_edge(('B',i),(t,i)); H.add_edge(('B',i),(t,(i-1)%4))
m=next(nx.isomorphism.GraphMatcher(G,H).isomorphisms_iter())
cols={frozenset(p):c for p,c in zip(itertools.combinations(range(4),2),['blue!25','orange!35','green!30','red!25','violet!25','yellow!45'])}
idx={v:i for i,v in enumerate(G)}
for v in G:
    r,a=pos[m[v]]
    print(r"\node[fill=%s] (c%d) at (%d:%.1f) {$%d%d$};"%(cols[frozenset(v)],idx[v],a,r,v[0]+1,v[1]+1))
print(r"\draw "+" ".join("(c%d)--(c%d)"%(idx[a],idx[b]) for a,b in G.edges())+";")
