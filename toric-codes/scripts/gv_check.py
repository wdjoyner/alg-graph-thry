"""Compare each recomputed table row with the finite Gilbert-Varshamov bound
(largest d guaranteed by sum_{i<=d-2} C(n-1,i)(q-1)^i < q^(n-k)) and with the
asymptotic GV curve R = 1 - H_q(d/n).  License: MIT."""
import json, math, os
rows = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_tables.json")))
def d_gv(n, k, q):
    d = 1
    while True:
        s = sum(math.comb(n-1, i) * (q-1)**i for i in range(0, d-1))
        if s < q**(n-k): d += 1
        else: return d - 1
def Hq(x, q):
    if x <= 0: return 0.0
    if x >= 1: return math.log(q-1, q)
    return x*math.log(q-1, q) - x*math.log(x, q) - (1-x)*math.log(1-x, q)
seen = set(); beat = 0; tot = 0
for r in rows:
    n, k, d = r["computed"]; q = r["q"]
    if (q, n, k, d) in seen: continue
    seen.add((q, n, k, d)); tot += 1
    g = d_gv(n, k, q)
    curve = (k/n) > 1 - Hq(d/n, q) if d/n < (q-1)/q else None
    beat += d > g
    print(f"{r['label']:16s} q={q} [{n},{k},{d}]  finite GV d={g}  beats finite GV: {d>g}  above GV curve: {curve}")
print("distinct parameter sets:", tot, " beating the finite GV bound:", beat)
