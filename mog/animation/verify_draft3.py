# SPDX-License-Identifier: MIT
from itertools import combinations, product
from collections import Counter, deque
X=set(range(12)); hands={frozenset(c) for c in combinations(X,6)}
M=((6,3,0,9),(5,2,7,10),(4,1,8,11))
P=((0,3,11,2),(5,9,8,10),(4,1,6,7)) # 11 represents infinity
T={(b,a,(a+b)%3,(a+2*b)%3) for a,b in product(range(3),repeat=2)}
def hexad(h):
    cols=[{r for r in range(3) if M[r][c] in h} for c in range(4)]
    if sorted(map(len,cols))==[0,1,2,3]: return False
    odd={c:next(iter(s if len(s)==1 else set(range(3))-s)) for c,s in enumerate(cols) if len(s) in (1,2)}
    return any(all(t[c]==r for c,r in odd.items()) for t in T)
H={h for h in hands if hexad(h)}
def steiner(hs):
    counts=Counter(frozenset(s) for h in hs for s in combinations(h,5))
    assert len(hs)==132 and len(counts)==792 and set(counts.values())=={1}
steiner(H)
def translate(x): return (x+1)%11 if x!=11 else 11
def invert(x): return 11 if x==0 else 0 if x==11 else -pow(x,-1,11)%11
Q=frozenset([0,1,3,4,5,9]); orbit={Q}; todo=deque([Q])
while todo:
    h=todo.popleft()
    for f in (translate,invert):
        k=frozenset(map(f,h))
        if k not in orbit: orbit.add(k); todo.append(k)
steiner(orbit)
rel={P[r][c]:M[r][c] for r,c in product(range(3),range(4))}
assert {frozenset(rel[x] for x in h) for h in orbit}==H
views={6:(5,11,3,8,2,4,9,10,7),1:(5,11,3,2,4,8,7,9,10),0:(8,10,3,9,11,4,5,2,7)}
def kitten(views):
    D=set(views); types=[set() for _ in range(4)]
    for p,v in views.items():
        lines=[[frozenset(v[3*r+c] for r,c in product(range(3),repeat=2) if (a*r+b*c)%3==k) for k in range(3)] for a,b in ((1,0),(0,1),(1,1),(1,2))]
        types[0].update(frozenset(D)|l for ls in lines for l in ls)
        types[1].update(l|m for ls in lines for l,m in combinations(ls,2))
        for i,j in ((0,1),(2,3)):
            for l,m in product(lines[i],lines[j]):
                cross=l|m
                types[2].add(cross|{p}); types[3].add(frozenset(set(v)-cross)| (D-{p}))
    assert [len(t) for t in types]==[12,12,54,54]
    assert sum(map(len,types))==len(set.union(*types))
    return types
projective_views={11:(6,10,3,2,7,4,5,9,8),0:(5,7,3,6,9,4,2,10,8),1:(5,7,3,9,4,6,8,2,10)}
types=kitten(views)
assert set.union(*types)==H
assert set.union(*kitten(projective_views))==orbit
assert {rel[d]:tuple(rel[x] for x in v) for d,v in projective_views.items()}==views
# signed vectors over F3, retaining support only
cols=[tuple(int(i%4==c) for i in range(12)) for c in range(4)]
tets=[tuple(int(i//4==t[i%4]) for i in range(12)) for t in T]
def support(*terms):
    return frozenset(M[i//4][i%4] for i in range(12) if sum(s*v[i] for s,v in terms)%3)
signed=[set() for _ in range(4)]
for c,d in combinations(cols,2):
    signed[0].add(support((1,c),(-1,d)))
    for t in tets: signed[3].add(support((1,c),(1,d),(-1,t)))
for c,t in product(cols,tets): signed[1].add(support((1,c),(1,t)))
for t,u in combinations(tets,2): signed[2].add(support((1,t),(-1,u)))
assert list(map(len,signed))==[6,36,36,54]
assert sum(map(len,signed))==len(set.union(*signed))
assert set.union(*signed)==H
for h in hands:
    neighbors={(h-{a})|{b} for a in h for b in X-h}
    assert len(neighbors)==36
    assert len(neighbors&H)==(0 if h in H else 6)
    if h not in H:
        assert any(sum(k)<sum(h) for k in neighbors&H)==(sum(h)>21)
example=frozenset([0,2,4,6,7,11])
exchanges=[(a,b) for a in sorted(example) for b in sorted(X-example) if (example-{a})|{b} in H]
assert [(a,b) for a,b in exchanges if b<a]==[(4,3),(7,5),(11,9)]
print('example hexad exchanges',exchanges)
assert min(map(sum,H))==21
legal={h for h in hands if sum(h)>=21}; losing=set()
for h in sorted(legal,key=sum):
    if not any((h-{a})|{b} in losing for a in h for b in X-h if b<a): losing.add(h)
assert losing==H
assert all(X-h in H for h in H)
print('types',list(map(len,types)))
print('hexad totals',sorted(Counter(map(sum,H)).items()))
print('all hands <=21',sum(sum(h)<=21 for h in hands),'below 21',sum(sum(h)<21 for h in hands),'equal 21',sum(sum(h)==21 for h in hands))
print('winning hands',len(legal-H),'eligible deals',sum(sum(h)>21 for h in hands))
