"""Shared data for the diagrams. Permutations are image tuples."""
from itertools import combinations, permutations, product
from math import factorial

def compose(g, h):
    return tuple(g[i] for i in h)


def inverse(g):
    return tuple(g.index(i) for i in range(len(g)))


def cycles(n, *parts):
    images = list(range(n))
    for part in parts:
        for a, b in zip(part, part[1:] + part[:1]):
            images[a] = b
    return tuple(images)


def apply(g, points):
    return tuple(g[i] for i in points)


CUBE_VERTICES = tuple(product((-1,1), repeat=3))
CUBE_EDGES = tuple((a,b) for a,b in combinations(CUBE_VERTICES,2)
                   if sum(x != y for x,y in zip(a,b)) == 1)


I3 = cycles(3)
SWAP = cycles(3, (0, 1))
ROTATE = cycles(3, (0, 1, 2))
S3_GRID = tuple(tuple(compose(h, c) for c in (I3, ROTATE, inverse(ROTATE)))
                for h in (I3, SWAP))

INF = 11
BASE = (0, 1, INF, 2)
CYCLE = cycles(12, tuple(range(2, 11)))
POWERS = [cycles(12)]
for _ in range(8):
    POWERS.append(compose(CYCLE, POWERS[-1]))
G = cycles(12, (0, 1))
U = tuple((1 - x) % 11 for x in range(11)) + (INF,)
TAU = POWERS[8]
H = cycles(12, (3, 10), (4, 9), (5, 8), (6, 7))

AFFINE = {(b, (a+b) % 5): (a,b) for a in range(1,5) for b in range(5)}
AFFINE_TARGET = (3, 2)
AFFINE_BASE = (0, 1)
D = ((2,0), (3,0), (4,0), (2,4), (3,3), (4,2))
EXTRA = ((9,4), (33,4), (8,5), (9,6), (32,29), (33,30))
FAMILIES = (
    ("n − 1", "1", "Every n", "Cₙ"),
    ("2", "n − 2", "Every n", "Aₙ"),
    ("n − 2", "2", "n is a prime power", "AGL₁(n)"),
    ("n − 3", "3", "n − 1 is a prime power", "PGL₂(n − 1)"),
)
MATHIEU = ((11, 4, 7, 7920), (12, 5, 7, 95040))
DEGREE_12 = (1, 3, 5, 10)
LIFTS = (((1,2), (1,3)), ((2,1), (3,1)))


def affine_mul(left, right):
    a, b = left
    c, d = right
    return a*c % 5, (a*d+b) % 5


def arrangement(symbols):
    vertices = tuple(permutations(symbols, 2))
    edges = tuple((x,y) for x,y in combinations(vertices, 2)
                  if sum(a != b for a,b in zip(x,y)) == 1)
    return vertices, edges


def forget(v):
    return tuple(sorted(v))


T5, E5 = arrangement(range(5))
T4, E4 = arrangement(range(1,5))
J4 = tuple(combinations(range(1,5), 2))
JE4 = tuple((a,b) for a,b in combinations(J4, 2) if len(set(a) & set(b)) == 1)


def projective_group():
    """Enumerate invertible matrices modulo scalars by their actions."""
    group = set()
    for a,b,c,d in product(range(11), repeat=4):
        if (a*d-b*c) % 11 == 0:
            continue
        p = []
        for x in range(12):
            num,den = (a,c) if x == INF else (a*x+b, c*x+d)
            p.append(num*pow(den,-1,11) % 11 if den % 11 else INF)
        group.add(tuple(p))
    return group


def prime_power(n):
    for p in range(2,n+1):
        if n % p == 0:
            while n % p == 0:
                n //= p
            return n == 1
    return False


def allowed_by_classification(n, k):
    """Apply the cited degree restrictions to a numerical pair."""
    return (k in (1,n-2,n-1)
            or k == 2 and prime_power(n)
            or k == 3 and prime_power(n-1)
            or (n,k) in {(11,4),(12,5)})


def verify():
    assert len(CUBE_EDGES) == 12
    assert all(sum(v in edge for edge in CUBE_EDGES) == 3 for v in CUBE_VERTICES)
    assert set(sum(S3_GRID, ())) == set(permutations(range(3)))
    assert S3_GRID[1][2] == cycles(3, (0,2))
    assert len(AFFINE) == 20 and AFFINE[AFFINE_TARGET] == (4,3)
    rates = tuple(AFFINE.values())
    maps = [tuple((a*x+b) % 5 for x in range(5)) for a,b in rates]
    stabilizer = [p for p in permutations(range(5)) if p[:2] == (0,1)]
    assert len({compose(f,h) for f in maps for h in stabilizer}) == factorial(5)
    for pair in T5:
        assert set(apply(f,pair) for f in maps) == set(T5)
    projective = projective_group()
    assert U in projective and len(projective) == 1320
    assert len({apply(p, BASE[:3]) for p in projective}) == 1320
    assert len(POWERS) == len(set(POWERS)) == 9
    assert compose(CYCLE, POWERS[-1]) == cycles(12)
    assert all(apply(c,BASE[:3]) == BASE[:3] for c in POWERS)
    assert len({apply(compose(p,c),BASE) for p,c in product(projective,POWERS)}) == 11880
    assert apply(H,BASE) == BASE and compose(U,compose(TAU,H)) == G
    assert inverse(U)[G[2]] == TAU[2] == 10
    assert 1320 * 9 * factorial(8) == factorial(12)
    assert all(factorial(n)//factorial(n-k) == order and n-k == m
               for n,k,m,order in MATHIEU)
    assert DEGREE_12 == tuple(k for k in range(1,11)
                              if allowed_by_classification(12,k))
    assert len(set(EXTRA)) == 6 and all(not allowed_by_classification(n,k)
                                        for n,k in EXTRA)
    edge_set = {frozenset(e) for e in E5}
    reverse = {affine: pair for pair,affine in AFFINE.items()}
    assert edge_set == {frozenset((v, reverse[affine_mul(AFFINE[v],d)]))
                        for v,d in product(T5,D)}
    assert all(any(affine_mul(d,e) == (1,0) for e in D) for d in D)
    translated_edges = {
        frozenset(tuple((p+1)%5 for p in v) for v in e)
        for e in E5 if AFFINE_BASE in e
    }
    assert translated_edges == {frozenset(e) for e in E5 if (1,2) in e}
    assert len(T5) == 20 and len(E5) == 60
    assert len(T4) == 12 and len(E4) == 24 and len(J4) == 6 and len(JE4) == 12
    assert all(edge in E4 for edge in LIFTS)
    je = {frozenset(e) for e in JE4}
    assert all(frozenset(map(forget,e)) in je for e in E4)
    for subset in J4:
        assert sum(forget(v) == subset for v in T4) == 2
    for x in T4:
        neighbors = [v for v in T4 if tuple(sorted((x,v))) in E4]
        images = [forget(v) for v in neighbors]
        assert len(images) == len(set(images)) == 4
        assert set(images) == {y for y in J4 if frozenset((forget(x),y)) in je}
    print("Exact animation checks passed (permutations, quadruples, edges, fibers).")


if __name__ == "__main__":
    verify()
