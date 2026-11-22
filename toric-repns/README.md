# Representations of finite groups on the Riemann--Roch space of a toric variety

**Draft 3 (November 22, 2026)** by David Joyner. This directory belongs to
`wdjoyner/alg-graph-thry` on the `main` branch.

The manuscript studies finite-group actions on lattice-point bases of toric
Riemann--Roch spaces, induced permutation modules, fixed-point and weighted
character formulas, and graph-theoretic interpretations. Its examples include
a singular toric surface with involution, graphic zonotopes, and the symmetric-
group representations identified by Johnson-graph eigenspaces.

The main paper reads as a self-contained mathematical article. The separate
**revision log** records the history, referee criticisms, responses, and
verification levels.

## Files

- `toric-repns.tex`: editable manuscript, with draft number on the title page.
- `revision-log.tex`: detailed changes, historical criticisms, and verification.
- `verify_examples.py`: exact integer verification (Python standard library).
- `original/rr_toric_2002.tex`: archival source.
- `original/carbon_referee_report.txt`: archival referee report.
- `Makefile`: PDF build and verification commands.
- `LICENSE-manuscript.txt`, `LICENSE-code.txt`: license declarations.

## Build

```sh
make pdf
make check
```

The compiled PDFs can be regenerated with `pdflatex`; the GitHub connector
used for this update supports source files but not uploading binary PDFs.
Manuscript text is licensed CC BY 4.0; the verification script is MIT licensed.
