"""Finite field arithmetic GF(q) for small q (prime or prime power).

Elements are integers 0..q-1. For q = p^e an element is the integer
sum c_i p^i, where c_0 + c_1 w + ... is a polynomial in a root w of a fixed
primitive polynomial. The same encoding is used by mindist.c.

License: MIT.
"""

# Primitive polynomials, lowest coefficient first, monic of degree e.
PRIM = {
    4: [1, 1, 1],          # x^2 + x + 1
    8: [1, 1, 0, 1],       # x^3 + x + 1
    9: [2, 1, 1],          # x^2 + x + 2
    16: [1, 1, 0, 0, 1],   # x^4 + x + 1
    25: [2, 1, 1],         # x^2 + x + 2
    27: [1, 2, 0, 1],      # x^3 + 2x + 1
}


def factor_prime_power(q):
    for p in range(2, q + 1):
        if q % p == 0:
            e, r = 0, q
            while r % p == 0:
                r //= p
                e += 1
            assert r == 1, "q must be a prime power"
            return p, e


class GF:
    def __init__(self, q):
        self.q = q
        self.p, self.e = factor_prime_power(q)
        p, e = self.p, self.e
        if e == 1:
            # find a primitive root
            for g in range(2 if q > 2 else 1, q):
                seen, x = set(), 1
                for _ in range(q - 1):
                    x = x * g % q
                    seen.add(x)
                if len(seen) == q - 1:
                    self.gen = g
                    break
            self.exp = [1] * (q - 1)
            for i in range(1, q - 1):
                self.exp[i] = self.exp[i - 1] * self.gen % q
        else:
            poly = PRIM[q]

            def to_vec(a):
                return [(a // p ** i) % p for i in range(e)]

            def to_int(v):
                return sum(c * p ** i for i, c in enumerate(v))

            def mul_w(v):  # multiply polynomial by w, reduce by poly
                w = [0] + v[:-1]
                top = v[-1]
                return [(w[i] - top * poly[i]) % p for i in range(e)]

            self.exp = [0] * (q - 1)
            v = [1] + [0] * (e - 1)
            for i in range(q - 1):
                self.exp[i] = to_int(v)
                v = mul_w(v)
            assert len(set(self.exp)) == q - 1, "polynomial not primitive"
            self.gen = self.exp[1]
        self.log = [None] * q
        for i, a in enumerate(self.exp):
            self.log[a] = i
        # addition table
        self.addt = [[0] * q for _ in range(q)]
        for a in range(q):
            for b in range(q):
                if e == 1:
                    self.addt[a][b] = (a + b) % q
                else:
                    s, pw = 0, 1
                    for i in range(e):
                        s += (((a // pw) % p + (b // pw) % p) % p) * pw
                        pw *= p
                    self.addt[a][b] = s
        self.negt = [0] * q
        for a in range(q):
            for b in range(q):
                if self.addt[a][b] == 0:
                    self.negt[a] = b

    def add(self, a, b):
        return self.addt[a][b]

    def sub(self, a, b):
        return self.addt[a][self.negt[b]]

    def neg(self, a):
        return self.negt[a]

    def mul(self, a, b):
        if a == 0 or b == 0:
            return 0
        return self.exp[(self.log[a] + self.log[b]) % (self.q - 1)]

    def inv(self, a):
        assert a != 0
        return self.exp[(-self.log[a]) % (self.q - 1)]

    def pow_gen(self, k):
        return self.exp[k % (self.q - 1)]

    def elements_star(self):
        return list(self.exp)


def rank_and_rref(F, rows):
    """Row-reduce a list of row vectors over F. Returns (rank, rref rows, pivots)."""
    M = [list(r) for r in rows]
    if not M:
        return 0, [], []
    ncols = len(M[0])
    pivots = []
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(M)):
            if M[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = F.inv(M[r][c])
        M[r] = [F.mul(inv, x) for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [F.sub(x, F.mul(f, y)) for x, y in zip(M[i], M[r])]
        pivots.append(c)
        r += 1
        if r == len(M):
            break
    return r, M[:r], pivots


def solve_linear(F, A, b):
    """Return one solution x of A x = b (A list of rows) or None; plus nullspace basis."""
    m = len(A)
    ncols = len(A[0]) if m else 0
    aug = [list(A[i]) + [b[i]] for i in range(m)]
    rank, R, piv = rank_and_rref(F, aug)
    if ncols in piv:
        return None, None
    x = [0] * ncols
    for i, c in enumerate(piv):
        x[c] = R[i][ncols]
    free = [c for c in range(ncols) if c not in piv]
    null = []
    for fc in free:
        v = [0] * ncols
        v[fc] = 1
        for i, c in enumerate(piv):
            v[c] = F.neg(R[i][fc])
        null.append(v)
    return x, null


def nullspace(F, A, ncols):
    if not A:
        return [[1 if i == j else 0 for i in range(ncols)] for j in range(ncols)]
    x, null = solve_linear(F, A, [0] * len(A))
    return null
