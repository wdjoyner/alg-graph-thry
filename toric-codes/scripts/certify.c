/* certify.c -- independent verifier for the F_8 claims of toric-codes.tex.
   Shares no code with mindist.c. License: MIT.

   Input on stdin:  mode k n, then k rows of n field elements 0..7, where the
   integer c0 + 2 c1 + 4 c2 encodes c0 + c1 w + c2 w^2 with w^3 = w + 1.

   mode "wd":  enumerates all 8^k codewords as F_2-combinations of the 3k
               vectors w^b * row_i (b = 0,1,2) in Gray-code order, with each
               codeword stored bit-sliced as three 64-bit masks, and prints the
               weight distribution.  Requires n <= 64.
   mode "sepT" (T = 1..9): checks that every T columns of the k x n matrix are
               linearly independent, i.e. that the dual of the row space has
               minimum distance > T.  Prints the number of T-subsets checked
               and the number of dependent ones. */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

static int MUL[8][8];
static void init_field(void) {
    for (int a = 0; a < 8; a++) for (int b = 0; b < 8; b++) {
        int r = 0, x = a;
        for (int i = 0; i < 3; i++) {            /* r += x * (bit i of b) */
            if (b >> i & 1) r ^= x;
            x <<= 1; if (x & 8) x ^= 0xB;          /* reduce by w^3 + w + 1 */
        }
        MUL[a][b] = r;
    }
}
static int G[64][64], K, N;

static void mode_wd(void) {
    int m = 3 * K;
    uint64_t B[3 * 64][3];
    for (int i = 0; i < K; i++) for (int b = 0; b < 3; b++) {
        uint64_t *v = B[3 * i + b]; v[0] = v[1] = v[2] = 0;
        for (int j = 0; j < N; j++) {
            int c = MUL[1 << b][G[i][j]];
            for (int p = 0; p < 3; p++) if (c >> p & 1) v[p] |= 1ULL << j;
        }
    }
    uint64_t cur[3] = {0, 0, 0};
    unsigned long long A[65]; memset(A, 0, sizeof A);
    A[0] = 1;
    unsigned long long total = 1ULL << m;
    for (unsigned long long g = 1; g < total; g++) {
        int t = __builtin_ctzll(g);
        cur[0] ^= B[t][0]; cur[1] ^= B[t][1]; cur[2] ^= B[t][2];
        A[__builtin_popcountll(cur[0] | cur[1] | cur[2])]++;
    }
    printf("weightdist");
    for (int w = 0; w <= N; w++) if (A[w]) printf(" %d:%llu", w, A[w]);
    printf("\n");
}

static int rank_cols(int *cols, int t) {       /* rank of K x t submatrix */
    int M[64][9];
    for (int i = 0; i < K; i++) for (int j = 0; j < t; j++) M[i][j] = G[i][cols[j]];
    int r = 0;
    for (int c = 0; c < t && r < K; c++) {
        int p = -1;
        for (int i = r; i < K; i++) if (M[i][c]) { p = i; break; }
        if (p < 0) continue;
        for (int j = 0; j < t; j++) { int x = M[r][j]; M[r][j] = M[p][j]; M[p][j] = x; }
        int inv = 0; for (int x = 1; x < 8; x++) if (MUL[M[r][c]][x] == 1) inv = x;
        for (int j = 0; j < t; j++) M[r][j] = MUL[inv][M[r][j]];
        for (int i = 0; i < K; i++) if (i != r && M[i][c]) {
            int f = M[i][c];
            for (int j = 0; j < t; j++) M[i][j] ^= MUL[f][M[r][j]];
        }
        r++;
    }
    return r;
}

static void mode_sep(int t) {
    int cols[9];
    for (int i = 0; i < t; i++) cols[i] = i;
    unsigned long long checked = 0, dependent = 0;
    for (;;) {
        checked++;
        if (rank_cols(cols, t) < t) dependent++;
        int i = t - 1;
        while (i >= 0 && cols[i] == N - t + i) i--;
        if (i < 0) break;
        cols[i]++;
        for (int j = i + 1; j < t; j++) cols[j] = cols[j - 1] + 1;
    }
    printf("sep %d checked %llu dependent %llu\n", t, checked, dependent);
}

int main(void) {
    char mode[16];
    if (scanf("%15s %d %d", mode, &K, &N) != 3 || K > 64 || N > 64) return 1;
    for (int i = 0; i < K; i++) for (int j = 0; j < N; j++)
        if (scanf("%d", &G[i][j]) != 1) return 1;
    init_field();
    if (!strcmp(mode, "wd")) mode_wd();
    else if (!strncmp(mode, "sep", 3)) mode_sep(atoi(mode + 3));
    else return 1;
    return 0;
}
