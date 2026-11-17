# Verification script

`comm_tr_checks.py` rechecks the note's computational claims by exhaustive
computation with explicit 2x2 matrices over finite fields and exact group
multiplication tables. It does not need Sage or GAP.

Requirements: Python 3 and NumPy. Run it from this folder:

```
python3 comm_tr_checks.py > checks_output.txt
```

A full run takes about a minute.

| Section | What it checks |
| --- | --- |
| 1 | Which of GL(2,q), PGL(2,q), PSL(2,q) (q = 3, 5, 7) and SL(2,q) (q = 4, 8) have abelian centralizers of non-central elements |
| 2 | An induced-character value in S3 (see the revision log), and irreducibility at q = 2 |
| 3 | Mackey norms for split tori in PGL(2,q), q = 3, 5, 7, against q + 3 + delta |
| 4 | The F2-rank of the support vectors for PSL(2,q), q = 4, 8, 16 |
| 5 | Left versus right coset maps for conjugacy classes in S3 |
| 6 | The permutation characters of A5 and their rank |
| 7 | The explicit Z-combinations of induced characters giving the irreducible characters of A5 |
| 8 | The irreducibility criterion for every centralizer and character of S3, A4 and A5 |
| 9 | Mackey norms for the non-split torus in PGL(2,3) = S4, against q - 1 + delta |
| 10 | The class map from the commuting graph is harmonic, with m(x) = \|W(C)\|, for S3, A4, A5, PSL(2,8), GL(2,3), Q8 and D8, together with the Riemann-Hurwitz identity |
| 11 | The class map on the non-commuting graph of A5 is not harmonic |
| 12 | Collapsing the parts of the non-commuting graph is harmonic exactly when all parts have equal size |

Lines reading `False` in the output are expected negatives (for example,
"PGL(2,3): CT? False"). Each section prints its prediction next to the computed
value.
