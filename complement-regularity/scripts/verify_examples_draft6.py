"""Checks for the worked examples added in Draft 6 of complement-regularity.tex.

Example 5.6: the maps R_x and L_x for S_3 = S_2 C_3, and the homomorphism property.
Example 7.2: the coordinates of the transposition (0 1) in S_12 = P C H.
Requires sympy.
"""
from sympy.combinatorics import Permutation as P
import itertools
# S3 example; act on {0,1,2} standing for {1,2,3}; product g*h means apply h first -> sympy: (h*g) applies h first
def mul(g,h): return h*g   # g∘h
e=P(2); t=P([1,0,2]); c=P([1,2,0])   # t=(1 2), c=(1 2 3): 1->2->3->1
H=[e,t]; K=[e,c,mul(c,c)]
names={}
def cyc(p):
    s=''.join('('+' '.join(str(i+1) for i in cy)+')' for cy in p.cyclic_form) ; return s or '1'
def dec(g):
    for h in H:
        for k in K:
            if mul(h,k)==g: return h,k
for x in [P([2,1,0]), c, t]:
    print("x=",cyc(x)," R_x:",[(cyc(k),cyc(dec(mul(k,x**-1))[1])) for k in K]," L_x:",[(cyc(h),cyc(dec(mul(x,h))[0])) for h in H])
# check homomorphism
G=[P(list(p)) for p in itertools.permutations(range(3))]
R=lambda x:tuple(K.index(dec(mul(k,x**-1))[1]) for k in K)
L=lambda x:tuple(H.index(dec(mul(x,h))[0]) for h in H)
comp=lambda a,b:tuple(a[b[i]] for i in range(len(a)))
print(all(R(mul(x,y))==comp(R(x),R(y)) and L(mul(x,y))==comp(L(x),L(y)) for x in G for y in G))
# three-factor example: points 0..10, 11=inf
INF=11
g=list(range(12)); g[0],g[1]=1,0
p=[(1-x)%11 for x in range(11)]+[INF]; pinv=p
sig=list(range(12))
for x in range(2,11): sig[x]=x+1 if x<10 else 2
def powr(s,j):
    r=list(range(12))
    for _ in range(j): r=[s[r[i]] for i in range(12)]
    return r
e_=pinv[g[2]]; j=[j for j in range(9) if powr(sig,j)[2]==e_][0]; cc=powr(sig,j)
ccinv=[cc.index(i) for i in range(12)]
h=[ccinv[pinv[g[x]]] for x in range(12)]
print("e",e_,"j",j,"h",h, P(h).cyclic_form)
print([p[cc[h[x]]] for x in range(12)]==g, 1320*9*40320, __import__('math').factorial(12))
