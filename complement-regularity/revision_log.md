# Revision log — Draft 3 (2026-11-17)

Source: `original-transtvy2.tex` (1997 manuscript, revised 2007). Corrected edition: `complement-regularity.tex`.

## Original results retained
- The complement–sharp-transitivity criterion.
- The existence classification for standard symmetric subgroups.
- The motivation from permutation storage and the three-factor decomposition of S_12.

## Corrections
- Modernized LaTeX and typography to 12pt Times, letter paper, one-inch margins.
- Corrected the false claim that a point stabilizer in any subgroup G of S_n is S_(n-k).
- Replaced the defective right-translation proof with coset-action constructions.
- Distinguished unique ordered factorization from iterated subgroup factorization.
- Replaced incomplete case-by-case order exclusions by an explicitly cited classification input.
- Corrected the table to remove nonexistent prime-power cases in degrees 6, 10, and 12; in particular 6, 10, 12 are not prime powers.
- Added a proof of the PGL_2(11) C_9 S_8 factorization.
- Replaced informal density language with a natural-density-zero corollary.

## New outline (not claimed as completed research)
- Arrangement graphs and regular Cayley representations.
- Coset graphs and complements to vertex stabilizers.
- Johnson graphs and sharply homogeneous actions.
- Permutation-module and spectral questions.

## Verification and limitations
- The LaTeX file was compiled twice with pdflatex successfully, with no overfull boxes or unresolved citations/references in the final build.
- External classification theorem was not checked against specific source pages in this revision. Precise citations remain to be verified.
- The original GAP permutation-generator computations have not been rerun.
- AI review does not independently certify the mathematical results.
- ChatGPT performed mathematical review, revision drafting, and the graph outline.

## Numbering concordance
Original unsectioned theorem numbering was replaced by section-wise numbering. Central complement criterion is now Proposition 3.2; classification is now Theorem 4.2. Cross-references were updated.

## Draft 4 — November 17, 2026
- Archived the newly attached `transtvy2(1).tex` as `transtvy2-original-1997-revised-2007.tex`; its differences from the earlier attachment are minor textual edits, not a newly verified mathematical revision.
- Expanded graph theory with formal definitions, proved Cayley/coset/Johnson criteria, examples, TikZ diagrams, a Fourier-spectral proposition, and an expanded glossary.
- Reconstructed generator verification scripts from the original manuscript: `scripts/verify_generators.py` (SymPy) and `scripts/verify_generators.g` (GAP).
- Ran the Python/SymPy script: orders and full ordered-tuple orbits confirmed for the manuscript's explicit degree 10, 11, and 12 generator pairs. GAP is not installed here; the GAP script remains unexecuted.
- The global classification input still needs precise independent literature/theorem verification; no claim of complete independent classification verification is made.

## Draft 5 — November 17, 2026

Changes made by Anthropic's Claude.

### Scope

Only Section 6 (graphs) was rewritten. Sections 3–5 are unchanged. Outside Section 6 the edits are limited to keeping the paper consistent with the new section: title (Draft 5), abstract, one sentence each in Sections 1 and 2, the summary, the glossary (9 new entries), the acknowledgments, and the bibliography (14 new entries).

### What is new in Section 6

| Item | Status |
|---|---|
| Prop. 6.2 (regular subgroup ⇒ Cayley graph) | Proof rewritten; the Draft 4 proof was garbled about left/right conventions. Attributed to Sabidussi. |
| Examples 6.4, 6.5 (C_6 has two regular groups; Petersen graph has none) | New, proved in the text. |
| Prop. 6.7 (basic properties of T(n,k), arc-transitivity under S_n × S_k) | New, proved in the text. |
| Theorem 6.8 (Aut T(n,k) ≅ S_n × S_k) | Quoted from Yin–Feng–Zhou–Guo. |
| Prop. 6.10 and Table 2 (connection set = union of k subgroups of order n−k+1) | New, proved in the text. Draft 4 had only the bare statement. |
| Prop. 6.14 (regular subgroups L × M of S_n × S_k) | New, proved in the text. May overlap with constructions in Yin et al., which was not consulted in full. |
| Theorem 6.16 (which T(n,k) are Cayley) | Quoted from Yin–Feng–Zhou–Guo. |
| Cor. 6.17 (converse of Draft 4's Prop. 6.6 fails for six pairs) | New observation; the six regular subgroups were machine-checked. |
| Prop. 6.19, Example 6.20 (D ∩ K as connection set; rank 7 for pairs) | New, proved in the text. Left/right coset wording of Draft 4 corrected. |
| Prop. 6.26 (complements of S_k × S_{n−k}) | New here; proof depends on Livingstone–Wagner and Kantor as external input. Agrees with Dobson–Malnič. |
| Draft 4's J(5,2) example | Strengthened: J(5,2) is not a Cayley graph at all. |
| Props. 6.30, 6.31 (projection formula; spectrum of T(q,2)) | New, proved in the text. |
| Section 6.7 (harmonic morphisms) | New: quotient criterion, covering T(n,k) → J(n,k), quotients of Cayley graphs, a ramified quotient onto a star, a non-harmonic projection, Jacobians. |

### Draft 4 "questions for a later draft" now answered by the literature

- Aut(T(n,k)) and the classification of Cayley arrangement graphs: Yin–Feng–Zhou–Guo (2021).
- Which Johnson graphs are Cayley: Dobson–Malnič (2015), after Godsil (1980).

### Sources not consulted in full

Statements were taken from abstracts, secondary sources, or memory, and need checking against the originals before publication:

- Yin–Feng–Zhou–Guo, J. Graph Theory 98 (2021): abstract only. Exact hypotheses of Theorems 6.8 and 6.16 unverified.
- Dobson–Malnič (2015), Godsil (1980): abstract and secondary description only; treatment of n = 2k not checked.
- Livingstone–Wagner (1965), Kantor (1972): quoted from memory. Kantor's k = 2 case may belong to an earlier paper of his.
- Day–Tripathi (1992), Chiang–Chen (1998), Zhou (2011): via secondary description.
- Chen–Ghorbani–Wong (2014): abstract only; volume and pages not confirmed (DOI given).
- Araujo–Bratten (arXiv 1612.04747): abstract only.
- Baker–Norine (2009): definition, degree, Riemann–Hurwitz formula, and Jacobian surjectivity quoted from memory.
- Melles–Joyner (2026): cited as a general reference; conventions not compared.
- Brouwer–Cohen–Neumaier (1989): Johnson eigenvalues quoted from memory, confirmed numerically for n ≤ 6.

### Computational status

Python only (NetworkX, python-igraph, NumPy, SymPy); no GAP or Sage. The checks are listed in Remark 6.42 of the paper and are reproduced by `scripts/verify_graph_section.py`; its output from the run for this draft is `scripts/verify_graph_section_output.txt`. `scripts/make_t42_figure.py` generates the TikZ for Figure 2. Table 1 of the paper was not rechecked in this draft.

### Noticed but not changed

- Prop. 3.4: "the coordinate projections for G = HK and G = HK, respectively" repeats the same factorization; both projections do use G = HK, so the phrase is redundant rather than wrong.
- Remark 4.4 still says that no computational verification of the table is claimed, although the Draft 4 entry above records a SymPy check of the degree 10, 11, and 12 generator pairs; the remark was left as it stood.
- Proof of Prop. 3.4 calls H\G the "left coset space" and G/K the "right coset space"; Section 6 now uses "left cosets gH".
