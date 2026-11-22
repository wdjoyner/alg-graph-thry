"""Checks for Section 8.2 (Draft 5): the Alon-Fueredi minimum in the cases
used in the paper, the coloring counts of Example 8.6, the cube covering of
Example 8.5, and the Reed-Muller distance formula.  Exact, brute force.
License: MIT."""
import itertools
from math import prod


def af_min(a, d, lower=None):
    """min prod y over lower_j <= y_j <= a_j, sum y >= sum a - d."""
    lower = lower or [1] * len(a)
    best = None
    for y in itertools.product(*[range(l, aj + 1) for l, aj in zip(lower, a)]):
        if sum(y) >= sum(a) - d:
            p = prod(y)
            best = p if best is None else min(best, p)
    return best


print("== Lemma 4.2(i): AF minimum on (F_q^*)^r equals c^(r-1)(c-l), c=q-1")
ok = all(af_min([c] * r, l) == c ** (r - 1) * (c - l)
         for c in range(1, 9) for r in range(1, 4) for l in range(0, c))
print("   all c<=8, r<=3, 0<=l<=c-1:", ok)

print("== Lemma 4.2(ii): generalized AF minimum equals prod(c-d_j)")
ok = all(af_min([c] * r, sum(dj), [c - x for x in dj]) == prod(c - x for x in dj)
         for c in range(1, 8) for r in range(1, 4)
         for dj in itertools.product(range(c), repeat=r))
print("   all c<=7, r<=3, d_j<=c-1:", ok)
c = 7
print("   total degree only, r=2, d1=d2=1, c=7: AF gives", af_min([c, c], 2),
      "= c(c-2) =", c * (c - 2), "< (c-1)^2 =", (c - 1) ** 2)

print("== Reed-Muller: AF minimum on F_q^m equals (q-b) q^(m-a-1)")
ok = True
for q in (2, 3, 4, 5, 7):
    for m in (1, 2, 3):
        for l in range(0, m * (q - 1) + 1):
            a, b = divmod(l, q - 1)
            dgm = (q - b) * q ** (m - a - 1) if a < m else 1
            ok &= af_min([q] * m, l) == dgm
print("   q in {2,3,4,5,7}, m<=3, all l:", ok)


def colorings(n, edges, k):
    return sum(1 for col in itertools.product(range(k), repeat=n)
               if all(col[i] != col[j] for i, j in edges))


print("== Example 8.6: colorings versus the AF bound")
cases = [("K3, 3 colors", 3, [(0, 1), (1, 2), (0, 2)], 3),
         ("path P3, 3 colors", 3, [(0, 1), (1, 2)], 3)]
cases += [(f"path P{n}, 2 colors", n, [(i, i + 1) for i in range(n - 1)], 2)
          for n in range(2, 8)]
for name, n, E, k in cases:
    print(f"   {name}: AF bound {af_min([k] * n, len(E))}, actual {colorings(n, E, k)}")

print("== Example 8.5: hyperplane covers of {0,1}^n minus one point")
for n in (2, 3):
    pts = list(itertools.product((0, 1), repeat=n))
    # all hyperplanes c.x = t with small integer coefficients
    hyps = set()
    for cvec in itertools.product(range(-2, 3), repeat=n):
        if any(cvec):
            for t in range(-4, 5):
                hyps.add((cvec, t))
    hyps = list(hyps)
    covers = lambda H, p: any(sum(ci * pi for ci, pi in zip(h[0], p)) == h[1] for h in H)
    best = None
    for m in range(1, n + 1):
        for H in itertools.combinations(hyps, m):
            if not covers(H, pts[0]) and all(covers(H, p) for p in pts[1:]):
                best = m
                break
        if best:
            break
    print(f"   n={n}: fewest hyperplanes (coefficients in [-2,2]) covering all but 0: {best}")
