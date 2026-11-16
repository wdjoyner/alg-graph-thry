# Verification scripts

These recheck the paper's claims without Sage. Run them from this folder.

Requirements: Python 3 with networkx, sympy and numpy; `passagemath-gap` (libgap) for
subgroup enumeration; `passagemath-nauty` (geng) for the census checks; gcc for `count.c`.

| Step | Command | What it checks |
| --- | --- | --- |
| 1 | `python3 parse.py ../regular-graph-harmonic-quotient-examples.tex` | Parses graphs, groups and tables into `data.json` |
| 2 | `python3 verify.py` | Every table: harmonicity, m, ν, deg, genus, Riemann–Hurwitz. Every stated G: automorphism? Do its orbits match a table? |
| 3 | `python3 fixes.py <names>` | Which subgroups realize each tabulated partition (GAP) |
| 4 | `python3 invariants.py` | Characteristic polynomial, diameter, girth, circumference, \|Aut\|, spanning trees, LCF |
| 5 | `gcc -O2 -o count count.c && python3 counts.py` | Morphism counts against the stated ones (`brute.py` is an independent check) |
| 6 | `python3 quot.py <names>` | All harmonic quotients via GAP AllSubgroups (`k55.py`: K₅,₅ via conjugacy classes) |
| 7 | `python3 fullgrp.py <names>` | The quotient by the full group Aut(Γ₂) |
| 8 | `python3 census.py` | The census statements (needs geng output files; see the script) |
| 9 | `python3 patch.py` | Rebuilds rev 1 from the archived original (each edit must match exactly once) |

Step 2 on rev 1 reports zero issues.
