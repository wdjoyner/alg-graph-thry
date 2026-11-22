# Toric codes over finite fields

Project for David Joyner's *Toric codes over finite fields*, published in
*Applicable Algebra in Engineering, Communication and Computing* **15** (2004),
63–79 (preprint arXiv:math/0208155).

**Current version: Draft 4 of the corrected and expanded version
(2026-11-22).** `toric-codes.tex` and `toric-codes.pdf`.

## Contents

- `toric-codes.tex`, `toric-codes.pdf`: the corrected and expanded paper (37 pages).
- `original/toric_code7.tex`: the 2003 manuscript source (dated September 1, 2003).
- `referee/2026-11-22/toric_codes_referee_report.tex`: the earlier referee report on
  the 2003 manuscript by OpenAI's ChatGPT; it uses newtx fonts and has no PDF here.
- `referee/2026-11-22/toric-codes-referee-2026-11-22.tex` and `.pdf`:
  a new correctness and readability report on the attached Draft 1, with
  separate findings affecting the newer Draft 3 tropical section.
- `.github/workflows/build-toric-codes-pdfs.yml`: builds the current
  manuscript and the new referee report, then commits both compiled PDFs.
- `revision-log.tex`, `revision-log.pdf`: the revision log. It contains the
  point-by-point response to the referee report, the list of changes, the
  error discussion moved out of the paper in Draft 2, a
  numbering concordance, the verification level of each main claim, and the
  sources not consulted.
- `scripts/`: the verification scripts and their outputs (see `scripts/README.md`).

## Draft 1

Revised by Anthropic's Claude in response to the ChatGPT referee report,
following the house style guide. Each claim in the report was checked
independently. Changes in brief:

- The two conjectures of 2004 are false. They are replaced by
  counterexamples and by proved upper and lower bounds on the minimum
  distance.
- The injectivity lemma is replaced by an exact criterion: the dimension of
  a full-torus code is the number of residues of its lattice points modulo
  q − 1. A duality theorem is added.
- Hansen's types (a)–(c) are reproved with a grid lemma of Alon–Füredi type.
- All 55 table rows were recomputed exactly. They agree with the 2004 values
  except one duplicated row. The [49,11,28] code over F_8 is certified by two
  independent exhaustive computations, and its weight distribution is given.
- The decoding algorithm is repaired as an error-correcting-pair algorithm.
  It decodes the [49,11,28] code up to 5 errors in a worked example, and up
  to 6 errors with a pair found by computer search.
- New Section 8 covers graph-theoretic connections: the discrete torus as a
  Cayley graph, the Combinatorial Nullstellensatz, fans as weighted cycle
  graphs, tropical curves and harmonic morphisms, and Kitaev's toric code.

## Draft 2

At David's request, all discussion of errors in the 2004 version was moved
out of the paper into the revision log (Section 5 of the log). Where the
mathematics was worth keeping, it is now stated as a natural question arising
from a nearby theorem or from generalizing an example. For instance,
Section 6.3 is now "Two estimates that fail". No theorem, example or
computation changed.

## Draft 3

- Removed Section 8.5 (Kitaev's toric code) and Section 8.6 (the Hamming
  graph and linear programming bounds).
- Expanded Section 8.4 on tropical curves and harmonic morphisms. It now
  proves that coordinate projections of tropical curves are harmonic
  morphisms to a line, of degree equal to the vertical extent of the Newton
  polygon. A worked example (with a figure) shows the tropical curve of a
  polynomial with Newton polygon [0,2]^2, whose projection is a degree-2
  harmonic morphism to a tree that folds its hexagonal cycle two-to-one; a
  finite model satisfies the Baker–Norine Riemann–Hurwitz formula. A fiber
  bound connects the degree of the projection to zeros of sections, hence to
  minimum distances.
- Expanded the glossary to about three sentences per entry, with new entries
  for the tropical material.

## Draft 4

Response to the second ChatGPT referee report
(`referee/2026-11-22/toric-codes-referee-2026-11-22.tex`). Made from Draft 3.
Every finding was checked independently; the point-by-point response is
Section 8 of the revision log. Theorem numbers are unchanged.

- M1: Example 5.13 now uses the unimodular map (x,y) -> (2x-y, y-x), which
  takes the triangle to a translate of the simplex S_s. The old shear did not.
- M2: Proposition 8.5 repaired. Tropical edges now get length
  (lattice length)/(weight), so the dilation factor weight·|a| really is the
  slope of the projection. A new paragraph works the referee's example
  (1+x+y)^2.
- M3 not accepted: with the min convention the paper uses, tropical ends do
  point along inward normals (Trop(1+x+y) has rays (1,0), (0,1), (-1,-1)).
  The report's rays belong to the max convention. This example is now in
  the paper.
- M4: Example 8.6 corrected to Hansen type (c) with a = b = 2.
- M5: Example 6.6 now refutes estimate (i) for every prime power q >= 5, not
  just q = 9.
- M6: Proposition 8.1 now says generalized toric codes are the cyclic codes,
  with an example showing standard toric codes are a proper subfamily (r = 1).
  Cayley graph restricted to q >= 4.
- M7: new Section 9.1 on reproducibility (field, indexing, commands,
  checksums), `scripts/CHECKSUMS.txt`, and an independent verifier
  (`scripts/certify.py`, `scripts/certify.c`) that shares no code with
  `mindist.c`. It reproduces Table 1 and checks the t = 6 decoding pair.
- Exposition: shorter abstract, rational polytope versus lattice polygon in
  Example 5.8, Acknowledgments mention the second report.

## Pending

- Check the copyright position before treating this corrected version of the
  published paper as public (style guide, rule 8.6).
- Compile once with the newtx fonts installed. Only the mathptmx fallback has
  been compiled.
- Check the page citations carried over from 2003 (Fulton, Stichtenoth,
  MacWilliams–Sloane) against the sources.
- Decide whether Section 8 stays in the paper or moves to a companion note
  (the second referee report also raises this).
- Optionally rerun `verify_tables.py` on a second machine. Draft 4
  independently reverified only the principal code and the t = 6 pair.
