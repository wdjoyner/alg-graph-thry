# Grosswald--Schnitzer prime perturbations and graph models

Two revised mathematical working notes, developed from the November 1, 2026 drafts:

* [prime_perturbations_revised.tex](prime_perturbations_revised.tex) -- endpoint perturbations and their operator-equivalence classes; expanded with a weighted directed-path incidence model, discrete Stokes formula, graph variation stability bound, signed-frequency graphs and a generalized-integer transfer graph.
* [grosswald_schnitzer_spectral_invariance_2026.tex](grosswald_schnitzer_spectral_invariance_2026.tex) -- Hardy/Smirnov spectral-invariance note; extended with the same graph section.
* [gs_invariance_summation_operators_graph_appendix.tex](gs_invariance_summation_operators_graph_appendix.tex) -- standalone LaTeX section for inclusion in a *separate, later* manuscript bearing that title. It is **not** a revision of the later paper itself: its exact LaTeX source was not accessible.
* [graph_examples.py](graph_examples.py) -- Python 3 demonstration and finite checks.

## Main graph claims

For endpoint perturbation flow e on the infinite prime ray, the vertex divergence is (\partial e)_j = e_j-e_{j-1}. The Euler quotient is the product over prime vertices with these signed exponents, and cancellation is expressed by the discrete-Stokes formula. Finite weighted boundary variation yields a quantitative analytic-multiplier bound.

The generalized-integer graph has exponent vectors as vertices and a directed edge for multiplication by each generator. Its weighted *vertex* generating function is the generalized Euler product; counting paths instead would be incorrect. The dilation-series transfer formula is justified on X_sigma only for sigma>1.

## Caveats

These graph facts do **not** establish similarity of full summation-operator pairs, ordinary graph-Laplacian isospectrality, or a convergent prime-series realization on the critical strip. Earlier Hardy-space invariance and equivalence results are reproduced from the working drafts and still require independent mathematical review. The precise source of the later \`gs_invariance_summation_operators\` draft was not available for editing; the appendable section is provided as a bridge.

## Compile and test

    pdflatex -interaction=nonstopmode prime_perturbations_revised.tex
    pdflatex -interaction=nonstopmode grosswald_schnitzer_spectral_invariance_2026.tex
    python3 graph_examples.py

Both TeX papers are self-contained; the appendix is intended to be included by \`\\input\` in a different document (load tikz in that document's preamble).
