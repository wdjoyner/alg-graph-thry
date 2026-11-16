"""Brute-force checks for comm_tr_expository.tex (Draft 1, 2026). Run: python3 -I comm_tr_checks.py"""
import itertools, cmath
from fractions import Fraction

# ---------- finite fields: prime p, or GF(2^k) via polynomial arithmetic ----------
class PrimeField:
    def __init__(self, p): self.p=p; self.q=p; self.elts=list(range(p))
    def add(s,a,b): return (a+b)%s.p
    def mul(s,a,b): return (a*b)%s.p
    def neg(s,a): return (-a)%s.p
    def inv(s,a): return pow(a,s.p-2,s.p)

class GF2k:
    POLY={2:0b111,3:0b1011,4:0b10011}
    def __init__(s,k): s.k=k; s.q=2**k; s.mod=s.POLY[k]; s.elts=list(range(s.q))
    def add(s,a,b): return a^b
    def neg(s,a): return a
    def mul(s,a,b):
        r=0
        while b:
            if b&1: r^=a
            b>>=1; a<<=1
            if a & s.q: a^=s.mod
        return r
    def inv(s,a):
        for b in s.elts:
            if s.mul(a,b)==1: return b

def mats(F):
    return [(a,b,c,d) for a,b,c,d in itertools.product(F.elts,repeat=4)]
def mmul(F,x,y):
    a,b,c,d=x; e,f,g,h=y
    return (F.add(F.mul(a,e),F.mul(b,g)),F.add(F.mul(a,f),F.mul(b,h)),
            F.add(F.mul(c,e),F.mul(d,g)),F.add(F.mul(c,f),F.mul(d,h)))
def det(F,x): a,b,c,d=x; return F.add(F.mul(a,d),F.neg(F.mul(b,c)))

def GL(F): return [m for m in mats(F) if det(F,m)!=0]
def SL(F): return [m for m in mats(F) if det(F,m)==1]

def projective(F, G):
    """Return group of cosets G/scalars as frozensets, with multiplication table indices."""
    scal=[(a,0,0,a) for a in F.elts if a!=0]
    seen={}; reps=[]
    for g in G:
        if g in seen: continue
        cls=frozenset(mmul(F,g,s) for s in scal)
        idx=len(reps); reps.append(g)
        for h in cls: seen[h]=idx
    n=len(reps)
    table=[[seen[mmul(F,reps[i],reps[j])] for j in range(n)] for i in range(n)]
    return n, table

def as_table(F, G):
    idx={g:i for i,g in enumerate(G)}
    return len(G), [[idx[mmul(F,x,y)] for y in G] for x in G]

class Group:
    def __init__(s,n,table):
        s.n=n; s.t=table
        s.e=[i for i in range(n) if all(table[i][j]==j for j in range(n))][0]
        s.inv=[[j for j in range(n) if table[i][j]==s.e][0] for i in range(n)]
    def m(s,a,b): return s.t[a][b]
    def conj(s,x,y): return s.m(s.m(s.inv[y],x),y)   # y^-1 x y
    def cent(s,g): return frozenset(x for x in range(s.n) if s.m(x,g)==s.m(g,x))
    def center(s): return frozenset(g for g in range(s.n) if len(s.cent(g))==s.n)
    def classes(s):
        seen=set(); out=[]
        for g in range(s.n):
            if g in seen: continue
            c=frozenset(s.conj(g,y) for y in range(s.n)); seen|=c; out.append(c)
        return out
    def is_abelian(s,H): return all(s.m(a,b)==s.m(b,a) for a in H for b in H)
    def normalizer(s,H): return frozenset(x for x in range(s.n) if frozenset(s.conj(h,x) for h in H)==H)

def commutation_transitive(G):
    Z=G.center()
    return all(G.is_abelian(G.cent(g)) for g in range(G.n) if g not in Z)

def rank_F2(vecs):
    rows=[int(''.join('1' if b else '0' for b in v),2) for v in vecs]
    r=0; basis=[]
    for v in rows:
        for b in basis: v=min(v,v^b)
        if v: basis.append(v); r+=1
    return r

print("=== 1. Which groups are commutation transitive (centralizers of noncentral elts abelian)? ===")
for p in [3,5,7]:
    F=PrimeField(p)
    G=Group(*as_table(F,GL(F)));  print(f"GL(2,{p}): CT-type? {commutation_transitive(G)}  |Z|={len(G.center())}")
    P=Group(*projective(F,GL(F))); print(f"PGL(2,{p}): CT? {commutation_transitive(P)}  |Z|={len(P.center())}")
    S=Group(*projective(F,SL(F))); print(f"PSL(2,{p}): CT? {commutation_transitive(S)}  |Z|={len(S.center())}")
for k in [2,3]:
    F=GF2k(k); S=Group(*as_table(F,SL(F)))
    print(f"SL(2,{2**k})=PSL: CT? {commutation_transitive(S)}  |Z|={len(S.center())}")

print("\n=== 2. Induced character formula: S3 = GL(2,2), C = A3, mu nontrivial ===")
F=PrimeField(2); G=Group(*as_table(F,GL(F)))
ords={}
def order(G,g):
    k=1; x=g
    while x!=G.e: x=G.m(x,g); k+=1
    return k
g3=[g for g in range(G.n) if order(G,g)==3][0]
C=G.cent(g3); assert len(C)==3
w=cmath.exp(2j*cmath.pi/3)
mu={G.e:1, g3:w, G.m(g3,g3):w*w}
def ind_char(G,C,mu,g):
    return sum(mu[G.conj(g,x)] for x in range(G.n) if G.conj(g,x) in C)/len(C)
N=G.normalizer(C)
paper=sum(mu[G.conj(g3,n)] for n in N)
print(f"true value at 3-cycle: {ind_char(G,C,mu,g3):.3f};  paper's formula: {paper:.3f};  |C|={len(C)}")
print(f"<Ind mu, Ind mu> = {sum(abs(ind_char(G,C,mu,g))**2 for g in range(G.n))/G.n:.3f}  (=1 => irreducible; refutes Corollary at q=2)")

print("\n=== 3. <Ind_T^G pi, Ind_T^G pi> for PGL(2,q), T split torus (Mackey count) ===")
for p in [3,5,7]:
    F=PrimeField(p); n,tab=projective(F,GL(F)); P=Group(n,tab)
    # split torus image: diag(a,1)
    reps={}
    gl=GL(F)
    # recover index of diag(a,1)
    scal=[(a,0,0,a) for a in F.elts if a]
    # rebuild map
    seen={}; rr=[]
    for g in gl:
        if g in seen: continue
        idx=len(rr); rr.append(g)
        for s_ in scal: seen[mmul(F,g,s_)]=idx
    T=[seen[(a,0,0,1)] for a in range(1,p)]
    # generator
    gen=[seen[(a,0,0,1)] for a in range(1,p) if len({pow(a,i,p) for i in range(1,p)})==p-1][0]
    Tl=[]; x=P.e
    for i in range(p-1): Tl.append(x); x=P.m(x,gen)
    for jchar in range(p-1):
        z=cmath.exp(2j*cmath.pi*jchar/(p-1))
        pi={Tl[i]:z**i for i in range(p-1)}
        val=sum(abs(ind_char(P,frozenset(Tl),pi,g))**2 for g in range(P.n))/P.n
        regular = (jchar*2)%(p-1)!=0
        print(f" q={p} char j={jchar}: <,> = {val:.3f}  (pi != pi^w: {regular}; predicted q+3+delta = {p+3+(0 if regular else 1)})")

print("\n=== 4. Conjecture: dim_F2 span{tau(Cent(g))} for PSL(2,2^k) ===")
for k in [2,3,4]:
    F=GF2k(k); G=Group(*as_table(F,SL(F)))
    cl=G.classes()
    vecs=set()
    for g in range(G.n):
        Cg=G.cent(g)
        vecs.add(tuple(bool(c & Cg) for c in cl))
    print(f"PSL(2,{2**k}): #classes={len(cl)}, distinct tau vectors={len(vecs)}, F2-rank={rank_F2(list(vecs))}")

print("\n=== 5. Bijection Conj(g,G) <-> G/Cent(g): x^-1 g x <-> x C (left cosets)? ===")
F=PrimeField(2); G=Group(*as_table(F,GL(F)))
t=[g for g in range(G.n) if order(G,g)==2][0]; C=G.cent(t)
bad=[(x,c) for x in range(G.n) for c in C if G.conj(t,G.m(x,c))!=G.conj(t,x)]
print(f"left-coset map well defined? {not bad}")
bad2=[(x,c) for x in range(G.n) for c in C if G.conj(t,G.m(c,x))!=G.conj(t,x)]
print(f"right-coset map Cent(g)x well defined? {not bad2}")

print("\n=== 6. Permutation characters 1_A^G for PSL(2,4)=A5 centralizers U,T,T',G: C-rank ===")
F=GF2k(2); G=Group(*as_table(F,SL(F))); cl=G.classes()
cents={}
for g in range(G.n):
    cents.setdefault(G.cent(g),g)
# up to conjugacy
reps=[]
for A in cents:
    if not any(len(A)==len(B) and any(frozenset(G.conj(a,x) for a in A)==B for x in range(G.n)) for B in reps):
        reps.append(A)
import numpy as np
rows=[]
for A in reps:
    row=[]
    for c in cl:
        g=next(iter(c))
        row.append(sum(1 for x in range(G.n) if G.conj(g,x) in A)/len(A))
    rows.append(row); print(f" |A|={len(A)}: 1_A^G on classes (sizes {[len(c) for c in cl]}): {row}")
print(" rank over C:", np.linalg.matrix_rank(np.array(rows)))

print("\n=== 7. A5 = SL(2,4): induced characters from centralizers, Brauer-type Z-combinations ===")
F=GF2k(2); G=Group(*as_table(F,SL(F)))
def cyc(G,g):
    out=[G.e]; x=g
    while x!=G.e: out.append(x); x=G.m(x,g)
    return out
def inner(G,f1,f2): return sum(f1[g]*f2[g].conjugate() for g in range(G.n))/G.n
def induce(G,C,mu): return [ind_char(G,C,mu,g) for g in range(G.n)]
g5=[g for g in range(G.n) if order(G,g)==5][0]; C5=cyc(G,g5)
g3=[g for g in range(G.n) if order(G,g)==3][0]; C3=cyc(G,g3)
g2=[g for g in range(G.n) if order(G,g)==2][0]; V=sorted(G.cent(g2))
z5=cmath.exp(2j*cmath.pi/5); z3=cmath.exp(2j*cmath.pi/3)
b =induce(G,frozenset(C5),{C5[i]:z5**i for i in range(5)})
bp=induce(G,frozenset(C5),{C5[i]:z5**(2*i) for i in range(5)})
d =induce(G,frozenset(C3),{C3[i]:z3**i for i in range(3)})
# nontrivial character of V4: -1 on g2 and on one other involution
other=[v for v in V if v not in (G.e,g2)][0]
lam={G.e:1,g2:-1,other:-1}; lam[G.m(g2,other)]=1
f =induce(G,frozenset(V),lam)
for name,ff in [("chi3 = f - b'",[x-y for x,y in zip(f,bp)]),
                ("chi3' = f - b",[x-y for x,y in zip(f,b)]),
                ("chi5 = d - f",[x-y for x,y in zip(d,f)]),
                ("chi4 = b + b' - d",[x+y-z for x,y,z in zip(b,bp,d)])]:
    print(f" {name}: degree {ff[G.e].real:.3f}, norm {inner(G,ff,ff).real:.3f}")
print(" norms of b,b',d,f:", [round(inner(G,x,x).real,3) for x in (b,bp,d,f)])

print("\n=== 8. Ind_C^G mu irreducible <=> C normal and mu != 1 (CT groups) ===")
def all_chars_cyclic(G,C):
    gen=[c for c in C if order(G,c)==len(C)]
    if not gen: return None
    L=cyc(G,gen[0]); n=len(L)
    return [{L[i]:cmath.exp(2j*cmath.pi*k*i/n) for i in range(n)} for k in range(n)]
def elem_ab_chars(G,C):
    # C elementary abelian 2-group or cyclic
    ch=all_chars_cyclic(G,C)
    if ch is not None: return ch
    Cl=sorted(C); gens=[]; span={G.e}
    for c in Cl:
        if c not in span:
            gens.append(c); span=span|{G.m(s,c) for s in span}
    out=[]
    for signs in itertools.product([1,-1],repeat=len(gens)):
        mu={G.e:1}
        for gi,sg in zip(gens,signs):
            for k in list(mu): mu[G.m(k,gi)]=mu[k]*sg
        out.append(mu)
    return out
tests=[("S3",GL(PrimeField(2)),PrimeField(2),'as'),("A4=PSL(2,3)",SL(PrimeField(3)),PrimeField(3),'proj'),
       ("A5=SL(2,4)",SL(GF2k(2)),GF2k(2),'as')]
for nm,M,Fd,mode in tests:
    G=Group(*(as_table(Fd,M) if mode=='as' else projective(Fd,M)))
    seen=[]
    for g in range(G.n):
        if g==G.e: continue
        C=G.cent(g)
        if C in seen: continue
        seen.append(C)
        normal = G.normalizer(C)==frozenset(range(G.n))
        chars=elem_ab_chars(G,C)
        irr=[abs(inner(G,induce(G,C,mu),induce(G,C,mu))-1)<1e-9 for mu in chars]
        triv=[all(abs(mu[c]-1)<1e-9 for c in C) for mu in chars]
        ok=all(i==(normal and not t) for i,t in zip(irr,triv))
    print(f" {nm}: criterion holds for all centralizers and characters: {ok}")

print("\n=== 9. Non-split torus in PGL(2,3) = S4 (cyclic of order 4): norms q-1+delta ===")
S4=list(itertools.permutations(range(4)))
pm=lambda a,b: tuple(a[b[i]] for i in range(4))
pinv=lambda a: tuple(sorted(range(4),key=lambda i:a[i]))
c4=(1,2,3,0); T4=[(0,1,2,3)]; x=c4
while x!=T4[0]: T4.append(x); x=pm(x,c4)
for j in range(4):
    pi={T4[i]:cmath.exp(2j*cmath.pi*j*i/4) for i in range(4)}
    def ch(g): return sum(pi[pm(pm(pinv(y),g),y)] for y in S4 if pm(pm(pinv(y),g),y) in pi)/4
    nrm=sum(abs(ch(g))**2 for g in S4)/24
    print(f" j={j}: norm {nrm:.3f}, predicted {2+(1 if (2*j)%4==0 else 0)}")

print("\n=== 10. Harmonic morphisms: commuting graph -> commuting conjugacy class graph ===")
def sub_table(F,mats_list):
    return as_table(F,mats_list)
def harmonic_report(name,G):
    Z=G.center(); V=[g for g in range(G.n) if g not in Z]
    cls={}
    for c in G.classes():
        if not (c<=Z):
            for g in c: cls[g]=c
    adj={x:{y for y in V if y!=x and G.m(x,y)==G.m(y,x)} for x in V}
    # class graph edges
    cedges=set()
    for x in V:
        for y in adj[x]:
            if cls[x]!=cls[y]: cedges.add(frozenset((cls[x],cls[y])))
    ok=True; info=set()
    for x in V:
        gx=cls[x]
        tgt=[e for e in cedges if gx in e]
        counts=[sum(1 for y in adj[x] if frozenset((gx,cls[y]))==e) for e in tgt]
        vert=sum(1 for y in adj[x] if cls[y]==gx)
        C=G.cent(x); W=len(G.normalizer(C))//len(C)
        if counts and len(set(counts))!=1: ok=False
        mx=counts[0] if counts else None
        if counts and mx!=W: ok=False
        if vert!=W-1: ok=False
        # component of x is C\Z: clique size, target clique size
        n=len(C)-len(Z); k=len({cls[c] for c in C if c not in Z})
        info.add((n,k,W,mx))
    print(f" {name}: |G|={G.n}, |Z|={len(Z)}, harmonic with m(x)=|W(Cent(x))| and v(x)=|W|-1 everywhere: {ok}")
    for n,k,W,mx in sorted(info):
        rh = (n*(n-3) == W*W*k*(k-3) + n*3*(W-1)) if k>=2 else None
        print(f"    component K_{n} -> K_{k}, |W|={W}, m(x)={mx}, degree={W*W if k>=2 else 0}, Riemann-Hurwitz identity: {rh}")
    return ok
F2=PrimeField(2); F3=PrimeField(3)
groups=[("S3=GL(2,2)",Group(*as_table(F2,GL(F2)))),
        ("A4=PSL(2,3)",Group(*projective(F3,SL(F3)))),
        ("A5=SL(2,4)",Group(*as_table(GF2k(2),SL(GF2k(2))))),
        ("PSL(2,8)",Group(*as_table(GF2k(3),SL(GF2k(3))))),
        ("GL(2,3)",Group(*as_table(F3,GL(F3)))),]
sl23=SL(F3); Gs=Group(*as_table(F3,sl23))
q8=[sl23[g] for g in range(Gs.n) if order(Gs,g) in (1,2,4)]
groups.append(("Q8 (in SL(2,3))",Group(*as_table(F3,q8))))
gl23=GL(F3); Gg=Group(*as_table(F3,gl23))
# D8: generated by diag(1,-1) and [[0,1],[1,0]] in GL(2,3)
gens=[(1,0,0,2),(0,1,1,0)]
S={(1,0,0,1)}; frontier=list(S)
while frontier:
    new=[]
    for a in frontier:
        for g in gens:
            b=mmul(F3,a,g)
            if b not in S: S.add(b); new.append(b)
    frontier=new
groups.append(("D8 (in GL(2,3))",Group(*as_table(F3,sorted(S)))))
for nm,G in groups: harmonic_report(nm,G)

print("\n=== 11. Non-commuting graph -> non-commuting class graph for A5: harmonic? ===")
G=Group(*as_table(GF2k(2),SL(GF2k(2)))); V=[g for g in range(G.n) if g!=G.e]
cls={}
for c in G.classes():
    for g in c: cls[g]=c
nadj={x:{y for y in V if G.m(x,y)!=G.m(y,x)} for x in V}
bad=0
for x in V:
    tg={}
    for y in nadj[x]:
        if cls[y]!=cls[x]: tg[cls[y]]=tg.get(cls[y],0)+1
    if len(set(tg.values()))>1: bad+=1
x=[g for g in V if order(G,g)==2][0]
tg={}
for y in nadj[x]:
    if cls[y]!=cls[x]: tg[order(G,next(iter(cls[y])))]=tg.get(order(G,next(iter(cls[y]))),0)+tg.get(None,0)+1
print(f" vertices where harmonicity fails: {bad} of {len(V)}")
cnt={}
for y in nadj[x]:
    if cls[y]!=cls[x]:
        key=(order(G,y),len(cls[y])); cnt[key]=cnt.get(key,0)+1
print(f" at an involution x: non-commuting neighbors by (order, class size): {cnt}")

print("\n=== 12. Non-commuting graph (complete multipartite) -> K_M collapsing each part C\\Z ===")
def collapse_parts_report(name,G):
    Z=G.center(); V=[g for g in range(G.n) if g not in Z]
    part={x:G.cent(x) for x in V}
    parts=set(part.values()); M=len(parts)
    ok=True; ms=set()
    for x in V:
        cnt={}
        for y in V:
            if G.m(x,y)!=G.m(y,x): cnt[part[y]]=cnt.get(part[y],0)+1
        if len(set(cnt.values()))>1: ok=False
        ms.add(tuple(sorted(cnt.values()))[:1])
    sizes=sorted({len(C)-len(Z) for C in parts})
    n=len(V); E=sum(1 for x in V for y in V if x<y and G.m(x,y)!=G.m(y,x))
    print(f" {name}: M={M} parts, part sizes {sizes}, harmonic: {ok}, predicted: {M==2 or len(sizes)==1}")
    if ok and len(sizes)==1:
        a=sizes[0]; g=E-n+1; gp=M*(M-1)//2-M+1
        print(f"    genus {g}, target genus {gp}, degree {a*a}; RH: {2*g-2} vs {a*a*(2*gp-2)+n*2*(a-1)}")
for nm,G in groups: collapse_parts_report(nm,G)
