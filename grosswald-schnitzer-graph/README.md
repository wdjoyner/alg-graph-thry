Prime perturbations and Grosswald--Schnitzer spectral models.

## Files

- `grosswald_schnitzer_spectral_invariance_2026.tex` (Draft 2): the closed joint kernel of the zeta-associated dilation operators is the same for every Grosswald--Schnitzer perturbation (Theorem 2.1). Bounded comparison holds for some perturbations and fails for others (Theorem 2.2). Corollary 11.1 adds the RH consequence: unconditionally, the closed joint kernel on S_1 vanishes if and only if RH holds; with the November 2026 certified formal proof of RH, it is {0} on S_1. Revision log: `spectral_invariance_revision_log.tex`.
- `prime_perturbations_revised.tex` (Draft 3): exact classification of bounded diagonal comparison. The criterion is weighted transitions for endpoint shifts and weighted signed Euler-factor inventories for rationally independent frequencies. The prime-path graph interpretation lives here. Revision log: `prime_perturbations_revision_log.tex`.
- `graph_examples.py`: numerical checks of the graph examples.

The RH result of November 20--21, 2026 is cited from the Lean FRO/Mathlib joint statement and from Rubinstein's verification page, which describes the proof as found with Anthropic's Claude. RH does not imply operator similarity, self-adjointness, bounded Euler quotients, or zero simplicity. For the historical edition see ../zeta-operators-graph/.

The build workflow `.github/workflows/build-prime-perturbations-pdfs.yml` compiles both papers and the RH companion note on pushes to main. The mathematical results have been refereed by AI systems, not by independent human review.
