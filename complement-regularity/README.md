# Complement–regularity

Project for David Joyner's *Which S_m have a complement in S_n?* (original 1997, revised 2007).

**Current version: Draft 5 (2026-11-17).** `complement-regularity.tex` and `complement-regularity.pdf`.

## Contents

- `complement-regularity.tex`, `complement-regularity.pdf`: the corrected and expanded paper.
- `transtvy2-original-1997-revised-2007.tex`: the original source.
- `revision_log.md`: cumulative revision log (Drafts 3–5), including sources not yet consulted in full.
- `scripts/verify_generators.py`, `scripts/verify_generators.g`: checks of the explicit degree 10, 11, and 12 generator pairs from the original manuscript (SymPy run; GAP script not yet executed).
- `scripts/verify_graph_section.py`: numerical checks for Section 6 (needs networkx, numpy, sympy, python-igraph); `scripts/verify_graph_section_output.txt` is its output.
- `scripts/make_t42_figure.py`: generates the TikZ for Figure 2.

## Draft 5

Section 6 (graphs) was expanded by Anthropic's Claude: Cayley representations of arrangement graphs with explicit connection sets, coset graphs, the Johnson-graph analogue of the complement problem, adjacency spectra, and harmonic morphisms arising as group quotients. Using the literature (Yin–Feng–Zhou–Guo 2021), the draft notes that six arrangement graphs are Cayley graphs although the corresponding S_(n-k) has no complement in S_n.

## Pending

- Check the quoted statements against the original sources listed in `revision_log.md`.
- Run the GAP script.
- Precise source verification of the classification of sharply multiply transitive groups.
