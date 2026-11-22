# Representations of finite groups on the Riemann--Roch space of a toric variety

**Draft 4 (November 22, 2026)** by David Joyner. This directory belongs to
`wdjoyner/alg-graph-thry` on the `main` branch.

The manuscript studies finite-group actions on lattice-point bases of toric
Riemann--Roch spaces, induced permutation modules, fixed-point and weighted
character formulas, affine lattice symmetries and their monomial linearizations,
and graph-theoretic interpretations. Its examples include
a singular toric surface with an involution (both Cartier and non-Cartier divisors), graphic zonotopes, and the symmetric-
group representations identified by Johnson-graph eigenspaces.

The main paper reads as a self-contained mathematical article. The separate
**revision log** records the history, referee criticisms, responses, and
verification levels.

## Files

- `toric-repns.tex`: editable manuscript, with draft number on the title page.
- `toric-repns.pdf`: compiled Draft 4 (pdflatex, newtx Times, US Letter).
- `revision-log.tex`: detailed changes, historical criticisms, and verification.
- `verify_examples.py`: exact integer verification, including the non-Cartier quasipolynomial (Python standard library).
- `original/rr_toric_2002.tex`: archival source.
- `original/carbon_referee_report.txt`: archival referee report.
- `Makefile`: PDF build and verification commands.
- `referee/2026-11-22/`: Claude referee report on Draft 3 (`.tex`, `.pdf`) and its exact
  checks (`referee_checks.py`, needs `sympy`).
- `LICENSE-manuscript.txt`, `LICENSE-code.txt`: license declarations.

## Build

```sh
make pdf
make check
```

The compiled PDFs can be regenerated with `pdflatex` (three passes for cross-references).
The GitHub Actions workflow `.github/workflows/build-toric-repns-pdf.yml` builds
and commits the current manuscript PDF after the source changes. Draft 4
addresses both major findings in Claude's report, fixes two chart/translation
misprints, and clarifies the relation between Johnson graphs and root step sets.
Manuscript text is licensed CC BY 4.0; the verification script is MIT licensed.
