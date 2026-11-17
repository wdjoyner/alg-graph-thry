"""Numerical checks for Section 6 of complement-regularity.tex (Draft 5).

Requires: networkx, numpy, sympy, python-igraph.  Runs in a few minutes.
The checks are those listed in the remark "Verification status" of the paper:
arrangement-graph basics and |Aut|, spectra, the Johnson covering, Cayley
connection sets, harmonic quotients, sharply k-homogeneous groups, and the
six regular subgroups L x M of S_n x S_k.  Every printed test should end in True.
"""
from collections import Counter, deque
import itertools, math, numpy as np, networkx as nx, igraph as ig
from math import comb, factorial
def T(n,k):
    V=list(itertools.permutations(range(n),k)); G=nx.Graph(); G.add_nodes_from(V)
    for x in V:
        s=set(x)
        for i in range(k):
            for c in range(n):
                if c not in s:
                    y=x[:i]+(c,)+x[i+1:]; G.add_edge(x,y)
    return G
def J(n,k):
    V=[frozenset(s) for s in itertools.combinations(range(n),k)]; G=nx.Graph(); G.add_nodes_from(V)
    for a in V:
        for b in V:
            if len(a&b)==k-1: G.add_edge(a,b)
    return G
def autcount(G):
    H=nx.convert_node_labels_to_integers(G); g=ig.Graph(n=H.number_of_nodes(),edges=list(H.edges())); return g.count_automorphisms()
def spec(G):
    A=nx.to_numpy_array(G); w=np.linalg.eigvalsh(A); w=np.round(w,6)
    from collections import Counter
    return dict(sorted(Counter(w.tolist()).items(),reverse=True))
print("A: basic + Aut + diameter")
for n,k in [(3,2),(4,2),(4,3),(5,2),(5,3),(5,4),(6,2),(6,3),(6,4),(7,2),(7,3)]:
    G=T(n,k); N=factorial(n)//factorial(n-k)
    assert G.number_of_nodes()==N and all(d==k*(n-k) for _,d in G.degree())
    print(n,k,"V",N,"conn",nx.is_connected(G),"diam",nx.diameter(G),"floor(3k/2)",3*k//2,"Aut",autcount(G),"n!k!",factorial(n)*factorial(k))
print("B:", nx.is_isomorphic(T(4,2), nx.line_graph(nx.hypercube_graph(3))), nx.is_isomorphic(J(4,2), nx.octahedral_graph()), nx.is_isomorphic(T(3,2),nx.cycle_graph(6)))
print("E: T(n,2) spectra")
for n in range(4,10):
    s=spec(T(n,2)); exp={2*n-4:1,n-2:n-1,n-4:n-1,-2:n*n-3*n+1}
    from collections import Counter
    e=Counter()
    for a,b in exp.items(): e[float(a)]+=b
    print(n,s, s==dict(sorted(e.items(),reverse=True)))
print("F: least eig & spectra")
for n,k in [(5,3),(6,3),(6,4),(5,4),(7,3)]:
    s=spec(T(n,k)); print(n,k,s)
print("G: Johnson inclusion, spanning trees")
def ntrees(G):
    import sympy
    L=nx.laplacian_matrix(G).toarray().astype(int); M=sympy.Matrix(L[1:,1:]); return M.det()
for n,k in [(3,2),(4,2),(5,2),(5,3),(6,2),(6,3)]:
    sj=spec(J(n,k)); st=spec(T(n,k))
    form={}
    for j in range(0,min(k,n-k)+1):
        form[float((k-j)*(n-k-j)-j)]=comb(n,j)-(comb(n,j-1) if j>0 else 0)
    ok=all(st.get(a,0)>=b for a,b in sj.items())
    print(n,k,"J spec",sj,"formula ok",sj==dict(sorted(form.items(),reverse=True)),"included",ok)
for n,k in [(3,2),(4,2),(5,2)]:
    a=ntrees(T(n,k)); b=ntrees(J(n,k)); print("trees",n,k,a,b,a%b==0, a//b)

# ---- finite fields GF(2^m)
class GF2m:
    def __init__(s,m,poly): s.m=m; s.q=1<<m; s.poly=poly
    def mul(s,a,b):
        r=0
        while b:
            if b&1: r^=a
            b>>=1; a<<=1
            if a>>s.m: a^=s.poly
        return r
    def inv(s,a):
        r=1
        for _ in range(s.q-2): r=s.mul(r,a)
        return r
def closure(gens):
    idt=tuple(range(len(gens[0]))); seen={idt}; dq=deque([idt])
    while dq:
        g=dq.popleft()
        for h in gens:
            x=tuple(h[g[i]] for i in range(len(g)))
            if x not in seen: seen.add(x); dq.append(x)
    return seen
def orbit(x,gens,act):
    seen={x}; dq=deque([x])
    while dq:
        y=dq.popleft()
        for g in gens:
            z=act(g,y)
            if z not in seen: seen.add(z); dq.append(z)
    return seen
# ---- C/D: AGL_1(p) connection set on T(p,2)
for p in [5,7]:
    K=[(a,b) for a in range(1,p) for b in range(p)]
    v=(0,1); G=T(p,2)
    D=[(a,b) for (a,b) in K if G.has_edge(v,(b%p,(a+b)%p))]
    stab0=[(a,0) for a in range(2,p)]; stab1=[(a,(1-a)%p) for a in range(2,p)]
    print("AGL1",p,"D",sorted(D),"=union stabilizers", set(D)==set(stab0+stab1))
    mul=lambda f,g:((f[0]*g[0])%p,(f[0]*g[1]+f[1])%p)   # f∘g
    C=nx.Graph(); C.add_nodes_from(K)
    for x in K:
        for d in D: C.add_edge(x,mul(x,d))
    # explicit iso x -> x.v
    ok=all(G.has_edge((x[1]%p,(x[0]+x[1])%p),(y[1]%p,(y[0]+y[1])%p)) for x,y in C.edges()) and C.number_of_edges()==G.number_of_edges()
    print("  Cayley iso via x->xv:",ok)
# ---- H: quotient by translations for p=5,7 ; q=4 via A_4 skip
for p in [5,7]:
    G=T(p,2); cnt=Counter()
    for (x,y) in G.edges():
        d1=(x[1]-x[0])%p; d2=(y[1]-y[0])%p; cnt[frozenset((d1,d2))]+=1
    print("transl quotient",p,"vertical",sum(v for k,v in cnt.items() if len(k)==1),"pairs",len(cnt),"edges per pair /p:",set(v//p for v in cnt.values()), comb(p-1,2))
# ---- I: S_{n-1} quotient to star, Riemann-Hurwitz
for n,k in [(3,2),(4,2),(5,2),(5,3),(6,3)]:
    G=T(n,k); top=n-1
    cls=lambda x: (x.index(top)+1) if top in x else 0
    okm=True; vert=0
    for x in G:
        c=Counter(cls(y) for y in G[x] if cls(y)!=cls(x))
        if cls(x)==0: okm&=(len(c)==k and set(c.values())=={1})
        else: okm&=(dict(c)=={0:n-k})
    vert=sum(1 for x,y in G.edges() if cls(x)==cls(y))
    gT=G.number_of_edges()-G.number_of_nodes()+1
    deg=factorial(n-1)//factorial(n-1-k)
    N0=factorial(n-1)//factorial(n-1-k); Ni=k*factorial(n-1)//factorial(n-k)
    rhs=deg*(0-2)+ Ni*2*(n-k-1) + 2*vert
    print("star",n,k,"mult ok",okm,"RH",2*gT-2,rhs,2*gT-2==rhs)
# ---- K: sharply homogeneous
p=7; sq={(a*a)%p for a in range(1,p)}
L=[(a,b) for a in sq for b in range(p)]
print("F21 on pairs:",len({frozenset(((a*0+b)%p,(a+b)%p)) for a,b in L}),comb(7,2),len(L))
F8=GF2m(3,0b1011)
L8=[(a,b) for a in range(1,8) for b in range(8)]
print("AGL1(8) on 3-sets:",len({frozenset(F8.mul(a,x)^b for x in (0,1,2)) for a,b in L8}),comb(8,3),len(L8))
F32=GF2m(5,0b100101)
def frob(x,i):
    for _ in range(i): x=F32.mul(x,x)
    return x
L32=[(a,b,i) for a in range(1,32) for b in range(32) for i in range(5)]
print("AGammaL1(32) on 3-sets:",len({frozenset(F32.mul(a,frob(x,i))^b for x in (0,1,2)) for a,b,i in L32}),comb(32,3),len(L32))
# ---- L: orbitals of S_5 on pairs
n=5; V=list(itertools.permutations(range(n),2)); base=(0,1)
H=[g for g in itertools.permutations(range(n)) if g[0]==0 and g[1]==1]
orbs=set(frozenset((g[x[0]],g[x[1]]) for g in H) for x in V)
print("rank S_5 on pairs:",len(orbs),sorted(len(o) for o in orbs))
# ---- J: twisted regular subgroups
def pgl_gens(F,q):
    INF=q
    def mob(a,b,c,d):
        out=[]
        for x in range(q+1):
            if x==INF: num,den=a,c
            else: num,den=F.mul(a,x)^b, F.mul(c,x)^d
            out.append(INF if den==0 else F.mul(num,F.inv(den)))
        return tuple(out)
    return [mob(2,0,0,1),mob(1,1,0,1),mob(0,1,1,0)]
g8=pgl_gens(F8,8); P8=closure(g8); print("|PSL2(8)|",len(P8))
def act_tuple(gs,x):
    g,s=gs; y=tuple(g[t] for t in x); return tuple(y[s[i]] for i in range(len(y)))
def test(Lgens,Lorder,Mgens,Morder,n,k,name):
    idn=tuple(range(n)); idk=tuple(range(k))
    gens=[(g,idk) for g in Lgens]+[(idn,s) for s in Mgens]
    base=tuple(range(k)); O=orbit(base,gens,act_tuple)
    N=factorial(n)//factorial(n-k)
    print(name,"orbit",len(O),"|V|",N,"|L x M|",Lorder*Morder,"regular:",len(O)==N==Lorder*Morder)
def sym_gens_fixing_last(k,j):  # S_j on first j coords of k
    if j<2: return []
    a=list(range(k)); a[0],a[1]=1,0
    b=list(range(1,j))+[0]+list(range(j,k))
    return [tuple(a),tuple(b)]
test(g8,504,sym_gens_fixing_last(4,3),6,9,4,"PSL2(8) x S3 on T(9,4):")
test(g8,504,sym_gens_fixing_last(6,5),120,9,6,"PSL2(8) x S5 on T(9,6):")
# AGL1(8) x S5 on T(8,5)
a8=[tuple(F8.mul(2,x) for x in range(8)),tuple(x^1 for x in range(8))]
test(a8,56,sym_gens_fixing_last(5,5),120,8,5,"AGL1(8) x S5 on T(8,5):")
test(a8,56,sym_gens_fixing_last(3,3),6,8,3,"AGL1(8) x S3 on T(8,3):")
# PGammaL2(32)
g32=pgl_gens(F32,32)+[tuple([F32.mul(x,x) for x in range(32)]+[32])]
P=closure(g32); print("|PGammaL2(32)|",len(P),33*32*31*5)
X=frozenset((0,1,32))
S=[g for g in P if frozenset(g[x] for x in X)==X]
print("3-set stabilizer order",len(S),"fixed-point-free off X:",all(all(g[x]!=x for x in range(33) if x not in X) for g in S if g!=tuple(range(33))))
Y=frozenset((0,1,2,32))
orbY=orbit(Y,g32,lambda g,y: frozenset(g[t] for t in y)); print("4-set orbit",len(orbY),comb(33,4))
SY=[g for g in P if frozenset(g[x] for x in Y)==Y]
print("4-set stabilizer order",len(SY),"regular on Y:",all(all(g[x]!=x for x in Y) for g in SY if g!=tuple(range(33))))
test(g32,163680,sym_gens_fixing_last(4,3),6,33,4,"PGammaL2(32) x S3 on T(33,4):")
