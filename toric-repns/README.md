# Toric Riemann–Roch representations: corrected and graph-theoretic draft

This is **Draft 2 (November 22, 2026)** of David Joyner's 2002 manuscript
**“Representations of finite groups on the Riemann–Roch space of a toric variety.”**

## Files

- `toric-repns.tex`: corrected and expanded manuscript (the draft number appears on the title page).
- `revision-log.tex`: corrections, provenance, verification, literature review, and theorem concordance.
- `verify_examples.py`: exact integer tests of the worked examples (Python standard library only).
- `original/rr_toric_2002.tex`: supplied original manuscript.
- `original/carbon_referee_report.txt`: Carbon's referee report.
- `LICENSE-manuscript.txt` and `LICENSE-code.txt`: licensing information.
- `Makefile`: build the two PDFs and run the verification script.

The compiled PDF is reproducible from the LaTeX source; the GitHub text-file upload
used for this revision did not include binary PDF files.

## Corrected results and graph theory

The original orbit-sum is a decomposition into **induced permutation modules**,
not irreducible representations. The manuscript proves irreducible multiplicity and
weighted monomial trace formulas and repairs the singular toric surface example.
New sections treat commuting adjacency operators, symmetry-twisted walks,
graphic zonotopes, and the Johnson-graph decomposition of the edge permutation
representation of the symmetric group. These classical connections are credited
to the relevant literature and not claimed as new discoveries.

## Compile and verify

```bash
make pdf
make check
```

Alternatively, run `pdflatex -interaction=nonstopmode -halt-on-error toric-repns.tex`
three times and `pdflatex -interaction=nonstopmode -halt-on-error revision-log.tex` twice.

## Licensing

- Manuscript and other prose: Creative Commons Attribution 4.0 International (CC BY 4.0).
- `verify_examples.py`: MIT license.

Original manuscript: June 23, 2002. Corrected and expanded Draft 2: November 22, 2026.
Directory: `wdjoyner/alg-graph-thry/toric-repns` on `main`.
