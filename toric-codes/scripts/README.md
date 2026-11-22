# Verification scripts

These scripts recheck every computational claim in `toric-codes.tex` by
exhaustive, exact computation over finite fields. They need Python 3 and a
C compiler, but not Sage, GAP or MAGMA. Compile the minimum-distance program
first, in this folder:

```
gcc -O3 -o mindist mindist.c
```

Then run any script from this folder, for example `python3 verify_tables.py`.
Saved outputs are in the `*_output.txt` and `*.json` files.

| Script | What it does | Run time |
| --- | --- | --- |
| `gf.py`, `toric.py` | Finite field arithmetic and generator matrices of toric codes (library modules) | – |
| `mindist.c` | Exact minimum distance by an information-set search with disjoint information sets, weight distributions for q = 2^e, and listing of words of given weight | – |
| `test_mindist.py` | Checks `mindist` against brute force on 300 random small codes | seconds |
| `verify_tables.py` | Recomputes all 55 table rows of the paper (output `verify_tables.json`) | a few minutes |
| `wd_principal.py` | Weight distribution of the [49,11,28] code over F_8, from all 8^11 codewords | a minute or two |
| `minwords_principal.py`, `minwords_explain.py` | The 833 minimum-weight words, their zero sets, and the 14 exceptional trinomials | minutes |
| `automorphisms_principal.py` | Lattice symmetries of the principal exponent set mod 7 | seconds |
| `verify_referee.py` | Counterexamples, fan determinants and weights, areas, and Cartier/ampleness checks | seconds |
| `verify_hansen.py` | Hansen's types (a)–(d) against exact computation. The saved run stopped at its time limit after 79 cases. | long |
| `gv_check.py` | Comparison with the finite Gilbert–Varshamov bound | seconds |
| `resolve_fan.py` | Minimal resolutions of fans and their weighted cycle graphs | seconds |
| `decode_example.py` | The worked decoding example (Example 7.8) and random trials | minutes |
| `decode_simplex_search.py` | Search for simplex-type error-correcting pairs | seconds |
| `decode_search.py` | Search over convex sets A in [0,4]^2. The saved run was stopped before completion. | hours |
| `decode_pair_check.py` | Verifies the t = 6 pair found by the search and tests the decoder with it | about 10 minutes |
