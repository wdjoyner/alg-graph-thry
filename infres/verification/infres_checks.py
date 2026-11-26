#!/usr/bin/env python3
"""
Brute-force checks for "Notes on the inflation-restriction sequence in
non-abelian cohomology" (Draft 1, corrected and expanded version, 2026).

For a list of small group extensions 1 -> N -> W -> Gamma -> 1 (N abelian)
and small Gamma-groups A, this script enumerates ALL 1-cocycles of W, Gamma
and N with values in A and checks, with no shortcuts:

  [S]  the factor-set identity (2.1) for sigma;
  [E]  exactness of 1 -> H^1(Gamma,A) -> H^1(W,A) -> H^1(N,A)^Gamma
       (inflation injective, kernel of res = image of inf, image of res
       consists of Gamma-invariant classes)                (Theorem 3.4);
  [T]  the extension criterion: a homomorphism phi: N -> A is the
       restriction of a cocycle iff there is c with c(g) in T_phi(g) and
       c(g) g(c(h)) = phi(sigma(g,h)) c(gh)                (Theorem 4.4),
       and f <-> c is a bijection;
  [O]  the same condition phrased as neutrality of the class
       d(phi) = (u * (phi o sigma)^-1, beta) in H^2(Gamma, C_phi, kappa_phi),
       including that (u, beta) is a Springer 2-cocycle     (Prop. 4.3);
  [F]  the fiber of res through [f] has |H^1(Gamma, C_phi with the
       f-twisted action)| elements                         (Prop. 4.7);
  [G]  the graph (holonomy) criterion on the Cayley graph of Gamma:
       cocycles restricting to phi correspond bijectively to gains
       c: S -> A, c(t) in T_phi(t), whose net gain around every defining
       relator r equals phi(net N-voltage of r)            (Theorem 5.7).

It also prints the data of the worked examples (N = Z/4, Gamma = Z/2,
W = D_4 or Q_8, A = Q_8).

Pure Python 3, no dependencies.  Run:  python3 infres_checks.py
"""
import itertools, sys

# ---------------------------------------------------------------- permutations
def mul(p, q):            # (p*q)(x) = p(q(x))
    return tuple(p[i] for i in q)
def inv(p):
    r = [0]*len(p)
    for i, x in enumerate(p): r[x] = i
    return tuple(r)
def ident(n): return tuple(range(n))
def cyc(n, *cycles):
    p = list(range(n))
    for c in cycles:
        for a, b in zip(c, c[1:] + c[:1]): p[a] = b
    return tuple(p)
def closure(gens, n):
    e = ident(n); seen = {e}; frontier = [e]
    while frontier:
        new = []
        for x in frontier:
            for g in gens:
                y = mul(x, g)
                if y not in seen: seen.add(y); new.append(y)
        frontier = new
    return sorted(seen)
def conj(b, a): return mul(mul(b, a), inv(b))      # b a b^-1

class Case:
    """Extension 1->N->W->Gamma->1 with a Gamma-group A.
    The action of w in W on A is conjugation by q(w), q: W -> Sym(m) a
    homomorphism trivial on N whose image normalizes A."""
    def __init__(self, name, nW, Wgens, Ngens, mA, Agens, qimgs, Sbar, relators):
        self.name = name
        self.W = closure(Wgens, nW); self.Wgens = Wgens; self.eW = ident(nW)
        self.N = closure(Ngens, nW)
        self.A = closure(Agens, mA); self.eA = ident(mA)
        Nset = set(self.N)
        assert all(mul(x, y) == mul(y, x) for x in self.N for y in self.N), "N abelian"
        assert all(conj(w, x) in Nset for w in self.W for x in self.N), "N normal"
        # q by BFS on words, then verify it is a homomorphism
        q = {self.eW: self.eA}; frontier = [self.eW]
        while frontier:
            new = []
            for x in frontier:
                for g, qg in zip(Wgens, qimgs):
                    y = mul(x, g)
                    if y not in q: q[y] = mul(q[x], qg); new.append(y)
            frontier = new
        assert all(q[mul(x, y)] == mul(q[x], q[y]) for x in self.W for y in self.W), "q hom"
        assert all(q[x] == self.eA for x in self.N), "N acts trivially"
        Aset = set(self.A)
        assert all(conj(q[w], a) in Aset for w in self.W for a in self.A), "q(W) normalizes A"
        self.q = q
        # Gamma = W/N as a list of cosets; section s with s(1)=1
        coset = {}; reps = []
        for w in [self.eW] + [w for w in self.W if w != self.eW]:
            if w not in coset:
                idx = len(reps); reps.append(w)
                for x in self.N: coset[mul(x, w)] = idx
        self.p = coset; self.s = reps; self.nG = len(reps)
        self.gmul = [[coset[mul(reps[g], reps[h])] for h in range(self.nG)] for g in range(self.nG)]
        self.ginv = [coset[inv(reps[g])] for g in range(self.nG)]
        self.sigma = [[mul(mul(reps[g], reps[h]), inv(reps[self.gmul[g][h]]))
                       for h in range(self.nG)] for g in range(self.nG)]
        self.Sbar = Sbar            # elements of W lifting generators of Gamma
        self.relators = relators    # words: lists of (index into Sbar, +1/-1)
    def act(self, g, a):            # g in Gamma (index) acting on a in A
        return conj(self.q[self.s[g]], a)
    def actW(self, w, a): return conj(self.q[w], a)
    def gN(self, g, x):             # Gamma acting on N
        return conj(self.s[g], x)

def cocycles(elems, gens, e, A, act):
    """All f: G -> A with f(xy) = f(x) x(f(y)); act(x,a) is the action."""
    out = []
    for vals in itertools.product(A, repeat=len(gens)):
        f = {e: A[0].__class__(range(len(A[0])))}
        f[e] = tuple(range(len(A[0])))
        frontier = [e]; ok = True
        while frontier and ok:
            new = []
            for x in frontier:
                for g, v in zip(gens, vals):
                    y = mul(x, g); val = mul(f[x], act(x, v))
                    if y in f:
                        if f[y] != val: ok = False; break
                    else: f[y] = val; new.append(y)
                if not ok: break
            frontier = new
        if ok and all(f[mul(x, y)] == mul(f[x], act(x, f[y])) for x in elems for y in elems):
            out.append(f)
    return out

def classes(cocs, elems, A, act):
    """Partition cocycles into cohomology classes: f' = a^-1 f(x) x(a)."""
    key = lambda f: tuple(f[x] for x in elems)
    seen = {}; cls = []
    for f in cocs:
        if key(f) in seen: continue
        idx = len(cls); cls.append(f)
        for a in A:
            ai = inv(a)
            seen[tuple(mul(mul(ai, f[x]), act(x, a)) for x in elems)] = idx
    return cls, (lambda f: seen[key(f)])

def run(case, report):
    C = case; A = C.A; eA = C.eA; G = range(C.nG); nG = C.nG
    tag = C.name
    # [S] factor set identity (2.1):  g1.sigma(g2,g3) sigma(g1,g2g3) = sigma(g1,g2) sigma(g1g2,g3)
    for g1 in G:
        for g2 in G:
            for g3 in G:
                lhs = mul(C.gN(g1, C.sigma[g2][g3]), C.sigma[g1][C.gmul[g2][g3]])
                rhs = mul(C.sigma[g1][g2], C.sigma[C.gmul[g1][g2]][g3])
                assert lhs == rhs, "[S]"
    # cocycle sets
    ZW = cocycles(C.W, C.Wgens, C.eW, A, C.actW)
    clsW, cidW = classes(ZW, C.W, A, C.actW)
    Gel = list(G)
    # Gamma-cocycles as dicts on indices
    ZG = []
    for f in ZW:
        if all(f[x] == eA for x in C.N):
            ZG.append(f)
    # every cocycle of Gamma, by brute force, to compare with those obtained by descent
    ZGam = []
    for vals in itertools.product(A, repeat=nG - 1):
        f = (eA,) + vals
        if all(f[C.gmul[g][h]] == mul(f[g], C.act(g, f[h])) for g in G for h in G):
            ZGam.append(f)
    infl = [{w: f[C.p[w]] for w in C.W} for f in ZGam]
    keyW = lambda f: tuple(f[x] for x in C.W)
    ZWkeys = {keyW(f) for f in ZW}
    assert all(keyW(f) in ZWkeys for f in infl), "[E] inflation of a cocycle is a cocycle"
    # classes of Gamma-cocycles
    def clsG_of(fs):
        seen = {}; n = 0
        for f in fs:
            if f in seen: continue
            for a in A:
                ai = inv(a)
                seen[tuple(mul(mul(ai, f[g]), C.act(g, a)) for g in G)] = n
            n += 1
        return seen, n
    seenG, nH1G = clsG_of(ZGam)
    # [E] inflation is injective on classes
    m = {}
    for f, F in zip(ZGam, infl):
        m.setdefault(cidW(F), set()).add(seenG[f])
    assert all(len(v) == 1 for v in m.values()), "[E] inf injective"
    assert len(m) == nH1G
    # Hom(N,A) and its classes, Gamma-action
    Ngens = [x for x in C.N if x != C.eW]
    HomN = cocycles(C.N, Ngens, C.eW, A, lambda x, a: a) if Ngens else [{C.eW: eA}]
    keyN = lambda f: tuple(f[x] for x in C.N)
    orbit = {}
    nH1N = 0
    for f in HomN:
        if keyN(f) in orbit: continue
        for a in A:
            orbit[tuple(conj(a, f[x]) for x in C.N)] = nH1N
        nH1N += 1
    def gact(g, f):   # (g.phi)(x) = g( phi(g^-1 x) )
        gi = C.ginv[g]
        return {x: C.act(g, f[C.gN(gi, x)]) for x in C.N}
    inv_cls = set()
    for f in HomN:
        if all(orbit[keyN(gact(g, f))] == orbit[keyN(f)] for g in G):
            inv_cls.add(orbit[keyN(f)])
    # [E] restriction
    res_img = {}
    for f in ZW:
        phi = {x: f[x] for x in C.N}
        res_img.setdefault(orbit[keyN(phi)], set()).add(cidW(f))
    assert set(res_img) <= inv_cls, "[E] res lands in invariants"
    triv = orbit[tuple(eA for _ in C.N)]
    assert res_img[triv] == set(m.keys()), "[E] exact at H^1(W,A)"
    # [T],[O],[F],[G] for each phi with invariant class
    n_ext = n_non = 0
    extra = []
    for phi in HomN:
        if orbit[keyN(phi)] not in inv_cls: continue
        Cphi = [a for a in A if all(conj(a, phi[x]) == phi[x] for x in C.N)]
        T = [[b for b in A if all(conj(b, C.act(g, phi[x])) == phi[C.gN(g, x)] for x in C.N)]
             for g in G]
        assert all(T[g] for g in G) and T[0] == Cphi
        # Lemma 4.1(ii): T(g) is a coset C b = b g(C)
        for g in G:
            b = T[g][0]
            assert set(T[g]) == {mul(c, b) for c in Cphi} == {mul(b, C.act(g, c)) for c in Cphi}
        size = 1
        for g in range(1, nG): size *= len(T[g])
        # cocycles restricting exactly to phi
        ext = [f for f in ZW if all(f[x] == phi[x] for x in C.N)]
        in_image = orbit[keyN(phi)] in res_img
        assert bool(ext) == in_image, "[T] (a)<=>(b)"
        for f in ext:                       # f(w) in T_phi(p(w)), f(x s(g)) = phi(x) c(g)
            assert all(f[w] in T[C.p[w]] for w in C.W)
            assert all(f[mul(x, C.s[g])] == mul(phi[x], f[C.s[g]]) for x in C.N for g in G)
        if size <= 300000:
            # [T] brute force over c
            sols = []
            for vals in itertools.product(*[T[g] for g in range(1, nG)]):
                c = (eA,) + vals
                if all(mul(c[g], C.act(g, c[h])) == mul(phi[C.sigma[g][h]], c[C.gmul[g][h]])
                       for g in G for h in G):
                    sols.append(c)
            assert {tuple(f[C.s[g]] for g in G) for f in ext} == set(sols), "[T] f <-> c bijection"
            assert len(sols) == len(ext)
            # [O] Springer cocycle (u, beta) in C_phi and neutrality of (u*(phi sigma)^-1, beta)
            b = [eA] + [T[g][0] for g in range(1, nG)]
            beta = lambda g, z: conj(b[g], C.act(g, z))
            u = [[mul(mul(b[g], C.act(g, b[h])), inv(b[C.gmul[g][h]])) for h in G] for g in G]
            Cset = set(Cphi)
            assert all(u[g][h] in Cset for g in G for h in G)
            assert all(beta(g, z) in Cset for g in G for z in Cphi)
            for g in G:
                for h in G:
                    for z in Cphi:
                        assert beta(g, beta(h, z)) == conj(u[g][h], beta(C.gmul[g][h], z))
                    for k in G:
                        assert mul(u[g][h], u[C.gmul[g][h]][k]) == \
                               mul(beta(g, u[h][k]), u[g][C.gmul[h][k]])
            # phi(N) central in C_phi and beta(g)phi(x) = phi(g x)
            assert all(mul(z, phi[x]) == mul(phi[x], z) for z in Cphi for x in C.N)
            assert all(beta(g, phi[x]) == phi[C.gN(g, x)] for g in G for x in C.N)
            d = [[mul(u[g][h], inv(phi[C.sigma[g][h]])) for h in G] for g in G]
            neutral = False
            for vals in itertools.product(Cphi, repeat=nG - 1):
                z = (eA,) + vals
                if all(mul(mul(mul(z[g], beta(g, z[h])), d[g][h]), inv(z[C.gmul[g][h]])) == eA
                       for g in G for h in G):
                    neutral = True; break
            assert neutral == in_image, "[O] neutral <=> in image of res"
        if in_image: n_ext += 1
        else: n_non += 1
        # [F] fibers
        if ext and len(Cphi) ** (nG - 1) <= 300000:
            fiber = res_img[orbit[keyN(phi)]]
            for f in ext:
                c = [f[C.s[g]] for g in G]
                bf = lambda g, z: conj(c[g], C.act(g, z))
                Z1 = []
                for vals in itertools.product(Cphi, repeat=nG - 1):
                    h = (eA,) + vals
                    if all(h[C.gmul[g][k]] == mul(h[g], bf(g, h[k])) for g in G for k in G):
                        Z1.append(h)
                seen = set(); n = 0
                for h in Z1:
                    if h in seen: continue
                    n += 1
                    for z in Cphi:
                        seen.add(tuple(mul(mul(inv(z), h[g]), bf(g, z)) for g in G))
                assert n == len(fiber), "[F] fiber size"
                # and the map h -> h*f hits every class of the fiber
                hit = {cidW({w: mul(h[C.p[w]], f[w]) for w in C.W}) for h in Z1}
                assert hit == fiber, "[F] fiber bijection"
        # [G] holonomy criterion on Cay(Gamma, Sbar)
        if C.Sbar:
            tg = [C.p[st] for st in C.Sbar]
            def lamW(word):
                w = C.eW
                for i, e in word: w = mul(w, C.Sbar[i] if e > 0 else inv(C.Sbar[i]))
                return w
            for r in C.relators:
                assert lamW(r) in set(C.N), "relator must hold in Gamma"
            def net_gain(cS, word):
                a = eA; g = 0
                for i, e in word:
                    if e > 0:
                        a = mul(a, C.act(g, cS[i])); g = C.gmul[g][tg[i]]
                    else:
                        g = C.gmul[g][C.ginv[tg[i]]]; a = mul(a, inv(C.act(g, cS[i])))
                return a
            good = set()
            for cS in itertools.product(*[T[t] for t in tg]):
                if all(net_gain(cS, r) == phi[lamW(r)] for r in C.relators):
                    good.add(cS)
            assert good == {tuple(f[st] for st in C.Sbar) for f in ext}, "[G]"
            assert len(good) == len(ext), "[G] uniqueness"
        if C.name in SHOW and len(Cphi) < len(A) and nG == 2:
            extra.append((orbit[keyN(phi)], len(Cphi), in_image))
    report.append((tag, len(C.W), len(C.N), nG, len(A), nH1G, len(clsW), nH1N,
                   len(inv_cls), len(res_img), n_ext, n_non))
    return extra

# ---------------------------------------------------------------- the groups
r4, s4 = cyc(4, (0, 1, 2, 3)), cyc(4, (1, 3))                    # D_4 on 4 points
qi = cyc(8, (0, 1, 2, 3), (4, 5, 6, 7)); qj = cyc(8, (0, 4, 2, 6), (1, 7, 3, 5))   # Q_8
R8 = cyc(8, tuple(range(8))); S8 = cyc(8, (1, 7), (2, 6), (3, 5))  # D_8 on 8 points
e3, e4, e8 = ident(3), ident(4), ident(8)
a4 = [cyc(4, (0, 1, 2)), cyc(4, (0, 1), (2, 3))]
s4gens = [cyc(4, (0, 1, 2, 3)), cyc(4, (0, 1))]
v4 = [cyc(4, (0, 1), (2, 3)), cyc(4, (0, 2), (1, 3))]
s3 = [cyc(3, (0, 1, 2)), cyc(3, (0, 1))]
assert len(closure([qi, qj], 8)) == 8 and mul(qi, qi) == mul(qj, qj) and mul(qi, qj) != mul(qj, qi)

P, M = +1, -1
cyc2 = [[(0, P), (0, P)]]
cyc3 = [[(0, P)] * 3]
V4rel = [[(0, P), (0, P)], [(1, P), (1, P)], [(0, P), (1, P), (0, M), (1, M)]]
S3rel = [[(0, P), (0, P)], [(1, P)] * 3, [(0, P), (1, P), (0, P), (1, P)]]

# natural map S_4 -> S_3 (action on the three pairings of {0,1,2,3})
pairings = [frozenset({frozenset({0, 1}), frozenset({2, 3})}),
            frozenset({frozenset({0, 2}), frozenset({1, 3})}),
            frozenset({frozenset({0, 3}), frozenset({1, 2})})]
def to_s3(p):
    return tuple(pairings.index(frozenset(frozenset(p[x] for x in blk) for blk in P_)) for P_ in pairings)
def s3_in_s4(t):          # S_3 as the stabilizer of the point 3 in S_4
    return tuple(t) + (3,)

SHOW = {"D4 / Q8 trivial", "Q8 / Q8 trivial"}
cases = [
    # name, nW, Wgens, Ngens, mA, Agens, q(Wgens), lifts of generators of Gamma, relators
    Case("D4 / Q8 trivial", 4, [r4, s4], [r4], 8, [qi, qj], [e8, e8], [s4], cyc2),
    Case("Q8 / Q8 trivial", 8, [qi, qj], [qi], 8, [qi, qj], [e8, e8], [qj], cyc2),
    Case("D4 / Z4 inversion", 4, [r4, s4], [r4], 4, [r4], [e4, s4], [s4], cyc2),
    Case("Q8 / Z4 inversion", 8, [qi, qj], [qi], 4, [r4], [e4, s4], [qj], cyc2),
    Case("D4 / D4 outer", 4, [r4, s4], [r4], 8, [mul(R8, R8), S8], [e8, mul(S8, R8)], [s4], cyc2),
    Case("Q8 / D4 outer", 8, [qi, qj], [qi], 8, [mul(R8, R8), S8], [e8, mul(S8, R8)], [qj], cyc2),
    Case("D4 / S3 trivial", 4, [r4, s4], [r4], 3, s3, [e3, e3], [s4], cyc2),
    Case("Q8 / S3 trivial", 8, [qi, qj], [qi], 3, s3, [e3, e3], [qj], cyc2),
    Case("D4 / S4 trivial", 4, [r4, s4], [r4], 4, s4gens, [e4, e4], [s4], cyc2),
    Case("Q8 / S4 trivial", 8, [qi, qj], [qi], 4, s4gens, [e4, e4], [qj], cyc2),
    Case("Z8 (N=Z4) / Q8 trivial", 8, [R8], [mul(R8, R8)], 8, [qi, qj], [e8], [R8], cyc2),
    Case("Z8 (N=Z4) / D4 trivial", 8, [R8], [mul(R8, R8)], 4, [r4, s4], [e4], [R8], cyc2),
    Case("Q8 (N=center) / Q8 trivial", 8, [qi, qj], [mul(qi, qi)], 8, [qi, qj], [e8, e8], [qi, qj], V4rel),
    Case("Q8 (N=center) / D4 trivial", 8, [qi, qj], [mul(qi, qi)], 4, [r4, s4], [e4, e4], [qi, qj], V4rel),
    Case("D4 (N=center) / Q8 trivial", 4, [r4, s4], [mul(r4, r4)], 8, [qi, qj], [e8, e8], [r4, s4], V4rel),
    Case("A4 (N=V4) / A4 trivial", 4, a4, v4, 4, a4, [e4, e4], [a4[0]], cyc3),
    Case("A4 (N=V4) / V4 by Z3", 4, a4, v4, 4, v4, [a4[0], e4], [a4[0]], cyc3),
    Case("S4 (N=V4) / S3 inner", 4, s4gens, v4, 3, s3, [to_s3(g) for g in s4gens],
         [cyc(4, (0, 1)), cyc(4, (0, 1, 2))], S3rel),
    Case("S4 (N=V4) / V4 by S3", 4, s4gens, v4, 4, v4,
         [s3_in_s4(to_s3(g)) for g in s4gens], [cyc(4, (0, 1)), cyc(4, (0, 1, 2))], S3rel),
    Case("S4 (N=V4) / A4 by S3", 4, s4gens, v4, 4, a4,
         [s3_in_s4(to_s3(g)) for g in s4gens], [cyc(4, (0, 1)), cyc(4, (0, 1, 2))], S3rel),
]

if __name__ == "__main__":
    report = []; shown = {}
    for c in cases:
        shown[c.name] = run(c, report)
        print("checked:", c.name, flush=True)
    hdr = ("case", "|W|", "|N|", "|G|", "|A|", "H1(G,A)", "H1(W,A)", "H1(N,A)",
           "invariant", "im(res)", "phi ext.", "phi not ext.")
    print()
    print("%-28s %4s %4s %4s %4s %8s %8s %8s %9s %8s %9s %12s" % hdr)
    for row in report:
        print("%-28s %4d %4d %4d %4d %8d %8d %8d %9d %8d %9d %12d" % row)
    print()
    print("Columns 'phi ext.' / 'phi not ext.' count homomorphisms phi: N -> A with")
    print("Gamma-invariant class that are / are not restrictions of cocycles of W.")
    print()
    for name in sorted(SHOW):
        print("Worked example,", name, ": invariant classes with C_phi != A:")
        for cls, nc, ok in sorted(set(shown[name])):
            print("   class %d   |C_phi| = %d   in image of res: %s" % (cls, nc, ok))
    print()
    print("ALL CHECKS PASSED")
