/* Count non-constant harmonic morphisms Gamma2 -> Gamma1 (simple graphs), Baker-Norine sense:
   vertex map phi with phi(u)=phi(v) or phi(u)~phi(v) for every edge uv, and for every x the number
   of neighbours y of x with phi(y)=w is the same m(x) for every neighbour w of phi(x).
   Input on stdin: n2 m2 edges... n1 m1 edges...   Output: nonconstant count, surjective count. */
#include <stdio.h>
#include <string.h>
int n2, n1, adj2[32][32], deg2[32], nb2[32][32], adj1[16][16], deg1[16], nb1[16][16];
int order[32], pos[32], phi[32];
long long cnt_nc = 0, cnt_surj = 0;
/* check vertex x if x and all its neighbours assigned (positions <= upto) */
static int check_vertex(int x) {
    int c[16]; memset(c, 0, sizeof c);
    int p = phi[x];
    for (int i = 0; i < deg2[x]; i++) { int y = nb2[x][i]; if (phi[y] != p) c[phi[y]]++; }
    int m = -1;
    for (int j = 0; j < deg1[p]; j++) { int w = nb1[p][j]; if (m < 0) m = c[w]; else if (c[w] != m) return 0; }
    return 1;
}
/* partial feasibility at x: counts so far must be completable */
static int partial_ok(int x, int k) {
    int c[16]; memset(c, 0, sizeof c);
    int p = phi[x], rem = 0;
    for (int i = 0; i < deg2[x]; i++) { int y = nb2[x][i]; if (pos[y] > k) rem++; else if (phi[y] != p) c[phi[y]]++; }
    int mx = 0, s = 0;
    for (int j = 0; j < deg1[p]; j++) { int w = nb1[p][j]; if (c[w] > mx) mx = c[w]; s += c[w]; }
    return deg1[p] * mx - s <= rem;
}
static void rec(int k) {
    if (k == n2) {
        int used[16] = {0}, nu = 0, first = phi[0], nc = 0;
        for (int i = 0; i < n2; i++) { if (!used[phi[i]]) { used[phi[i]] = 1; nu++; } if (phi[i] != first) nc = 1; }
        if (nc) { cnt_nc++; if (nu == n1) cnt_surj++; }
        return;
    }
    int x = order[k];
    for (int v = 0; v < n1; v++) {
        phi[x] = v;
        int ok = 1;
        for (int i = 0; i < deg2[x] && ok; i++) {
            int y = nb2[x][i];
            if (pos[y] < k && phi[y] != v && !adj1[phi[y]][v]) ok = 0;
        }
        if (!ok) continue;
        /* check every assigned vertex z in closed nbhd of x */
        int zs[33], nz = 0; zs[nz++] = x;
        for (int i = 0; i < deg2[x]; i++) if (pos[nb2[x][i]] < k) zs[nz++] = nb2[x][i];
        for (int t = 0; t < nz && ok; t++) {
            int z = zs[t], full = 1;
            for (int i = 0; i < deg2[z]; i++) if (pos[nb2[z][i]] > k) { full = 0; break; }
            if (full) ok = check_vertex(z); else ok = partial_ok(z, k);
        }
        if (ok) rec(k + 1);
    }
}
int main(void) {
    int m2, m1, a, b;
    scanf("%d %d", &n2, &m2);
    for (int i = 0; i < m2; i++) { scanf("%d %d", &a, &b); adj2[a][b] = adj2[b][a] = 1; nb2[a][deg2[a]++] = b; nb2[b][deg2[b]++] = a; }
    scanf("%d %d", &n1, &m1);
    for (int i = 0; i < m1; i++) { scanf("%d %d", &a, &b); adj1[a][b] = adj1[b][a] = 1; nb1[a][deg1[a]++] = b; nb1[b][deg1[b]++] = a; }
    /* BFS order from 0 */
    int seen[32] = {0}, h = 0, t = 0; order[t++] = 0; seen[0] = 1;
    while (h < t) { int v = order[h++]; for (int i = 0; i < deg2[v]; i++) { int w = nb2[v][i]; if (!seen[w]) { seen[w] = 1; order[t++] = w; } } }
    for (int i = 0; i < n2; i++) pos[order[i]] = i;
    rec(0);
    printf("%lld %lld\n", cnt_nc, cnt_surj);
    return 0;
}
