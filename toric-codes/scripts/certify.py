"""Independent certificate for the F_8 computations of toric-codes.tex.

Rebuilds every generator matrix from scratch (its own F_8 arithmetic and its
own lattice-point enumeration; it imports neither gf.py nor toric.py) and
uses certify.c, which shares no code with mindist.c, to check:

  1. the weight distribution of the [49,11,28]_8 code (Table 1), by
     enumerating all 8^11 codewords;
  2. the three error-correcting-pair conditions for the t = 6 pair of
     Example 7.8: A0 + B0 lies in P0, d(C_{A0}) = 28 (so a nonzero f in V_{A0}
     has at most 21 < 28 zeros), and every 6 columns of the generator matrix
     of C_{B0} are independent (so d(C_{B0}^perp) > 6).

Field: F_8 = F_2[w]/(w^3 + w + 1); w is primitive.  Torus point (i, j) is
(w^i, w^j), ordered with i outer and j inner, i, j = 0..6.

Usage (from this folder):
    gcc -O3 -o certify certify.c
    python3 certify.py
License: MIT."""
import hashlib, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "certify")


def mul(a, b):                       # F_8 product, bits = coefficients of w^i
    r = 0
    for i in range(3):
        if b >> i & 1:
            r ^= a
        a <<= 1
        if a & 8:
            a ^= 0b1011
    return r


POW = [1]
for _ in range(6):
    POW.append(mul(POW[-1], 0b010))  # powers of w
assert sorted(POW) == list(range(1, 8)), "w is not primitive"

PTS = [(i, j) for i in range(7) for j in range(7)]


def gen_matrix(U):
    """Rows ev(x^u) for u in U (exponents taken mod 7)."""
    return [[POW[(u[0] * i + u[1] * j) % 7] for (i, j) in PTS] for u in U]


def run(mode, rows):
    text = f"{mode} {len(rows)} {len(rows[0])}\n" + "\n".join(
        " ".join(map(str, r)) for r in rows) + "\n"
    t0 = time.time()
    out = subprocess.run([EXE], input=text, capture_output=True, text=True,
                         check=True).stdout.strip()
    return out, time.time() - t0


def wd(rows):
    out, sec = run("wd", rows)
    return {int(a): int(b) for a, b in (p.split(":") for p in out.split()[1:])}, sec


# The principal exponent set: lattice points of 5x-y>=0, -x+5y>=0, x+y<=5.
Q = [(x, y) for x in range(-10, 11) for y in range(-10, 11)
     if 5 * x - y >= 0 and -x + 5 * y >= 0 and x + y <= 5]
assert len(Q) == 11 and len({(a % 7, b % 7) for a, b in Q}) == 11

TABLE1 = {0: 1, 28: 833, 29: 2058, 30: 21952, 31: 105644, 32: 412629,
          33: 1184036, 34: 3980515, 35: 11983293, 36: 34115123, 37: 82757668,
          38: 181602036, 39: 361137840, 40: 626918936, 41: 969862341,
          42: 1290940427, 43: 1471503957, 44: 1397799774, 45: 1095370500,
          46: 665332878, 47: 296872674, 48: 84948752, 49: 13080725}

print("Field polynomial w^3 + w + 1; powers of w:", POW)
print("Q =", sorted(Q))
G = gen_matrix(Q)
print("SHA-256 of generator matrix of C_Q:",
      hashlib.sha256(repr(G).encode()).hexdigest())
A, sec = wd(G)
print(f"1. weight distribution of C_Q ({sec:.0f} s):", A)
print("   total =", sum(A.values()), "= 8^11:", sum(A.values()) == 8 ** 11)
print("   minimum nonzero weight:", min(w for w in A if w))
print("   agrees with Table 1:", A == TABLE1)

# Error-correcting pair of Example 7.8 (t = 6).
negQ = {(-a % 7, -b % 7) for a, b in Q}
P0 = {p for p in PTS if p not in negQ}
A0 = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2), (3, 2)]
B0 = [(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 5), (1, 6), (2, 0),
      (2, 1), (2, 6), (3, 0), (4, 0), (5, 0), (6, 0)]
sums = {((a[0] + b[0]) % 7, (a[1] + b[1]) % 7) for a in A0 for b in B0}
print("2. |P0| =", len(P0), " A0 + B0 inside P0:", sums <= P0)
WA, sec = wd(gen_matrix(A0))
dA = min(w for w in WA if w)
print(f"   (A) dim V_A0 = {len(A0)} > 6, residues distinct:",
      len({(a % 7, b % 7) for a, b in A0}) == len(A0))
print(f"   (C) d(C_A0) = {dA}, so at most {49 - dA} zeros; {49 - dA} < 28:",
      49 - dA < 28)
out, sec = run("sep6", gen_matrix(B0))
print(f"   (B) {out} ({sec:.0f} s)")
print("   every 6 columns independent, so d(C_B0^perp) > 6:",
      out.endswith("dependent 0"))
out7, sec = run("sep7", gen_matrix(B0))
print(f"   for comparison, 7 columns: {out7} ({sec:.0f} s)")
