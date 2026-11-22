/* mindist.c -- exact minimum distance of a linear code over GF(q).
 *
 * Mode "bz": Brouwer-Zimmermann style search with pairwise disjoint
 * information sets.  Correctness: let G_1,...,G_m be systematic generator
 * matrices on pairwise disjoint information sets I_1,...,I_m.  A nonzero
 * codeword c equals sum_{i in I_j} c_i * (row i of G_j).  If c restricted to
 * I_j has weight <= w for some j, then c (up to a scalar) is among the
 * combinations of at most w rows of G_j that are enumerated at stage w.
 * Otherwise wt(c) >= m(w+1).  Hence after finishing stage w every codeword
 * not yet seen has weight >= m(w+1), and the search stops once the smallest
 * weight found is <= m(w+1).  Scalars are removed by fixing the coefficient
 * of the first chosen row to 1.
 *
 * Mode "wd2": full weight distribution for q = 2^e, n <= 64, by a binary
 * Gray code over an F_2-basis of the code (bit-sliced arithmetic).
 *
 * Input (stdin): mode q n k, then the q*q addition table, the q*q
 * multiplication table, then k rows of n field elements (integers 0..q-1).
 * For wd2 the field must be GF(2^e) with addition = XOR of the encodings.
 *
 * License: MIT.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int q, n, k;
static int ADD[64][64], MUL[64][64], INV[64];
static int G[64][256];

static int best;          /* smallest weight found */
static int LISTW = -1;    /* list mode: print words of this weight */
static int bestvec[256];
static long long nodes;

static int rank_rref(int rows, int cols, int M[][256], int *piv, const int *colorder) {
    int r = 0;
    for (int cc = 0; cc < cols && r < rows; cc++) {
        int c = colorder ? colorder[cc] : cc;
        int p = -1;
        for (int i = r; i < rows; i++) if (M[i][c]) { p = i; break; }
        if (p < 0) continue;
        if (p != r) for (int j = 0; j < n; j++) { int t = M[r][j]; M[r][j] = M[p][j]; M[p][j] = t; }
        int iv = INV[M[r][c]];
        for (int j = 0; j < n; j++) M[r][j] = MUL[iv][M[r][j]];
        for (int i = 0; i < rows; i++) if (i != r && M[i][c]) {
            int f = M[i][c];
            /* M[i] -= f*M[r]  ->  M[i] + (neg f)*M[r] */
            int nf = 0; for (int x = 0; x < q; x++) if (ADD[f][x] == 0) { nf = x; break; }
            for (int j = 0; j < n; j++) M[i][j] = ADD[M[i][j]][MUL[nf][M[r][j]]];
        }
        piv[r] = c;
        r++;
    }
    return r;
}

/* systematic matrices */
static int NS;                 /* number of info sets */
static int SYS[16][64][256];
static int SCALED[16][64][64][256]; /* [set][row][scalar][col] -- allocated statically for small sizes */

static int vec[16][256];       /* partial sums by depth */

static int weight(const int *v) { int w = 0; for (int j = 0; j < n; j++) w += (v[j] != 0); return w; }

static void rec(int s, int depth, int start, int maxdepth) {
    for (int r = start; r < k; r++) {
        int cmin = (depth == 0) ? 1 : 1, cmax = (depth == 0) ? 1 : q - 1;
        for (int c = cmin; c <= cmax; c++) {
            /* scalar index: c is a field element; for depth 0 use element 1 */
            int coef = (depth == 0) ? 1 : c;
            if (coef == 0) continue;
            int *prev = (depth == 0) ? NULL : vec[depth - 1];
            int *cur = vec[depth];
            int *row = SCALED[s][r][coef];
            if (prev) for (int j = 0; j < n; j++) cur[j] = ADD[prev[j]][row[j]];
            else memcpy(cur, row, sizeof(int) * n);
            nodes++;
            if (depth + 1 == maxdepth) {
                int w = weight(cur);
                if (w < best) { best = w; memcpy(bestvec, cur, sizeof(int) * n); }
                if (w == LISTW) { printf("word"); for (int j = 0; j < n; j++) printf(" %d", cur[j]); printf("\n"); }
            } else {
                rec(s, depth + 1, r + 1, maxdepth);
            }
        }
    }
}

static void mode_bz(void) {
    /* find disjoint information sets */
    int used[256] = {0};
    NS = 0;
    for (;;) {
        static int M[64][256];
        for (int i = 0; i < k; i++) memcpy(M[i], G[i], sizeof(int) * n);
        int order[256], no = 0;
        for (int j = 0; j < n; j++) if (!used[j]) order[no++] = j;
        int piv[64];
        int r = rank_rref(k, no, M, piv, order);
        if (r < k) break;
        if (NS >= 16) break;
        /* reorder rows so row i has pivot piv[i] (already) */
        for (int i = 0; i < k; i++) { memcpy(SYS[NS][i], M[i], sizeof(int) * n); used[piv[i]] = 1; }
        NS++;
    }
    if (NS == 0) { fprintf(stderr, "rank deficient\n"); exit(1); }
    for (int s = 0; s < NS; s++)
        for (int r = 0; r < k; r++)
            for (int c = 0; c < q; c++)
                for (int j = 0; j < n; j++) SCALED[s][r][c][j] = MUL[c][SYS[s][r][j]];
    best = n + 1;
    int lower = 0;
    for (int w = 1; w <= k; w++) {
        for (int s = 0; s < NS; s++) rec(s, 0, 0, w);
        lower = NS * (w + 1);
        fprintf(stderr, "stage %d: best %d lower %d nodes %lld\n", w, best, lower, nodes);
        if (best <= lower) break;
    }
    if (lower > best) lower = best;
    printf("infosets %d\n", NS);
    printf("mindist %d\n", best);
    printf("witness");
    for (int j = 0; j < n; j++) printf(" %d", bestvec[j]);
    printf("\n");
}

static void mode_wd2(void) {
    int e = 0; while ((1 << e) < q) e++;
    if ((1 << e) != q || n > 64) { fprintf(stderr, "wd2 needs q=2^e, n<=64\n"); exit(1); }
    int B = e * k;
    uint64_t *planes = calloc((size_t)B * e, sizeof(uint64_t));
    for (int i = 0; i < k; i++)
        for (int t = 0; t < e; t++) {
            int s = 1 << t;            /* the field element w^t in the encoding */
            for (int j = 0; j < n; j++) {
                int v = MUL[s][G[i][j]];
                for (int b = 0; b < e; b++) if (v >> b & 1) planes[(size_t)(i * e + t) * e + b] |= (1ULL << j);
            }
        }
    uint64_t cur[8] = {0};
    long long *wd = calloc(n + 1, sizeof(long long));
    wd[0] = 1;
    uint64_t total = 1ULL << B;
    for (uint64_t g = 1; g < total; g++) {
        int bit = __builtin_ctzll(g);
        uint64_t orv = 0;
        for (int b = 0; b < e; b++) { cur[b] ^= planes[(size_t)bit * e + b]; orv |= cur[b]; }
        wd[__builtin_popcountll(orv)]++;
    }
    printf("weightdist");
    for (int w = 0; w <= n; w++) if (wd[w]) printf(" %d:%lld", w, wd[w]);
    printf("\n");
}

int main(void) {
    char mode[16];
    if (scanf("%15s %d %d %d", mode, &q, &n, &k) != 4) return 1;
    for (int a = 0; a < q; a++) for (int b = 0; b < q; b++) scanf("%d", &ADD[a][b]);
    for (int a = 0; a < q; a++) for (int b = 0; b < q; b++) scanf("%d", &MUL[a][b]);
    for (int a = 1; a < q; a++) for (int b = 1; b < q; b++) if (MUL[a][b] == 1) INV[a] = b;
    for (int i = 0; i < k; i++) for (int j = 0; j < n; j++) scanf("%d", &G[i][j]);
    /* reduce to a basis */
    static int M[64][256]; int piv[64];
    for (int i = 0; i < k; i++) memcpy(M[i], G[i], sizeof(int) * n);
    int r = rank_rref(k, n, M, piv, NULL);
    for (int i = 0; i < r; i++) memcpy(G[i], M[i], sizeof(int) * n);
    k = r;
    printf("dimension %d\n", k);
    if (!strcmp(mode, "bz")) mode_bz();
    else if (!strcmp(mode, "wd2")) mode_wd2();
    else if (!strcmp(mode, "rank")) {}
    else if (!strcmp(mode, "list")) {
        int S; if (scanf("%d %d", &LISTW, &S) != 2) return 1;
        /* reuse bz setup but run fixed stages 1..S */
        int used[256] = {0}; NS = 0;
        for (;;) {
            static int M2[64][256];
            for (int i = 0; i < k; i++) memcpy(M2[i], G[i], sizeof(int) * n);
            int order[256], no = 0;
            for (int j = 0; j < n; j++) if (!used[j]) order[no++] = j;
            int piv2[64];
            int rr = rank_rref(k, no, M2, piv2, order);
            if (rr < k || NS >= 16) break;
            for (int i = 0; i < k; i++) { memcpy(SYS[NS][i], M2[i], sizeof(int) * n); used[piv2[i]] = 1; }
            NS++;
        }
        for (int s = 0; s < NS; s++) for (int r2 = 0; r2 < k; r2++) for (int c = 0; c < q; c++)
            for (int j = 0; j < n; j++) SCALED[s][r2][c][j] = MUL[c][SYS[s][r2][j]];
        best = n + 1;
        for (int w = 1; w <= S; w++) for (int s = 0; s < NS; s++) rec(s, 0, 0, w);
        printf("infosets %d\n", NS);
    }
    return 0;
}
