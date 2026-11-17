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