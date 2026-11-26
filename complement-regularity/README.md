# Complement–regularity

Project for David Joyner's *Which S_m have a complement in S_n?* (original 1997, revised 2007).

**Current version: Draft 6 (2026-11-18).** `complement-regularity.tex` and `complement-regularity.pdf`.

## Summary

The paper asks for which m the standard subgroup S_m of S_n has a complement: a subgroup H with S_n = S_m·H and S_m ∩ H trivial. It characterizes such complements through sharply multiply transitive permutation groups, and gives the resulting classification with its explicit exceptions in low degree. It also gives an exact three-factor decomposition of S₁₂, motivated by storing permutations. The last section turns to graphs: a complement to S_{n−k} makes the arrangement graph on ordered k-tuples a Cayley graph with an explicit connection set. It discusses coset graphs, Johnson graphs, adjacency spectra, and the harmonic morphisms (in the sense of Baker and Norine) that arise as group quotients, among them the k!-fold covering of the Johnson graph by the arrangement graph. From the literature, six arrangement graphs are Cayley graphs even though the corresponding S_{n−k} has no complement.

## Contents

- `complement-regularity.tex`, `complement-regularity.pdf`: the corrected and expanded paper.
- `transtvy2-original-1997-revised-2007.tex`: the original source.
- `revision-log.tex`, `revision-log.pdf`: cumulative revision log (Drafts 3–6), including the response to the referee report on Draft 5, a numbering concordance, and the sources not yet consulted in full. It replaces the earlier `revision_log.md`.
- `scripts/verify_generators.py`, `scripts/verify_generators.g`: checks of the explicit degree 10, 11, and 12 generator pairs from the original manuscript (SymPy run; GAP script not yet executed).
- `scripts/verify_graph_section.py`: numerical checks for Section 6 (needs networkx, numpy, sympy, python-igraph); `scripts/verify_graph_section_output.txt` is its output.
- `scripts/make_t42_figure.py`: generates the TikZ for Figure 2.
- `scripts/verify_examples_draft6.py`: checks the worked examples added in Draft 6 (needs sympy).

## Draft 5

Section 6 (graphs) was expanded by Anthropic's Claude: Cayley representations of arrangement graphs with explicit connection sets, coset graphs, the Johnson-graph analogue of the complement problem, adjacency spectra, and harmonic morphisms arising as group quotients. Using the literature (Yin–Feng–Zhou–Guo 2021), the draft notes that six arrangement graphs are Cayley graphs although the corresponding S_(n-k) has no complement in S_n.

## Draft 6

Revised by Anthropic's Claude in response to a referee report on Draft 5 by Google's Gemini, written against the house style guide: ten-part structure, table of contents, literature review split at 1997, background and notation sections, new worked examples, unverified items marked as Remarks 2026.1 to 2026.6. No mathematical error was found in Draft 5.

## Pending

- Compile once with the newtx fonts installed; only the mathptmx fallback has been compiled.

- Check the quoted statements against the original sources listed in the revision log.
- Run the GAP script.
- Precise source verification of the classification of sharply multiply transitive groups.
