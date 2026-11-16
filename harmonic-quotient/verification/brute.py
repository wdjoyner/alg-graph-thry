import numpy as np, networkx as nx, sys
from counts import GR, T
def brute(E2, H, chunk=1<<20):
    G = nx.Graph(E2); n = G.number_of_nodes(); k = H.number_of_nodes()
    A = nx.to_numpy_array(H, nodelist=range(k)).astype(bool)
    total = 0; N = k**n
    for start in range(0, N, chunk):
        idx = np.arange(start, min(N, start+chunk), dtype=np.int64)
        M = np.empty((len(idx), n), dtype=np.int8)
        t = idx.copy()
        for i in range(n): M[:, i] = t % k; t //= k
        ok = np.ones(len(idx), bool)
        for u, v in G.edges():
            ok &= (M[:,u]==M[:,v]) | A[M[:,u], M[:,v]]
        for x in range(n):
            nbrs = list(G[x])
            cnt = np.stack([sum((M[:,y]==w) for y in nbrs) for w in range(k)], axis=1)  # N x k
            px = M[:,x]
            for p in range(k):
                sel = ok & (px==p)
                ws = [w for w in range(k) if A[p,w]]
                if len(ws) > 1:
                    c = cnt[sel][:, ws]
                    good = (c == c[:, :1]).all(axis=1)
                    tmp = ok[sel]; tmp &= good; ok[sel] = tmp
        surj = np.array([np.isin(np.arange(k), row).all() for row in M[ok]]) if ok.any() else np.array([])
        total += int(surj.sum()) if len(surj) else 0
    return total
for name, t in [(a.split(':')[0], a.split(':')[1]) for a in sys.argv[1:]]:
    print(name, t, brute(GR[name], T[t]), flush=True)
