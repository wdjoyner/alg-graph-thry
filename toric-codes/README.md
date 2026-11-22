# Toric codes over finite fields

Project for David Joyner's *Toric codes over finite fields*, published in
*Applicable Algebra in Engineering, Communication and Computing* **15** (2004),
63–79 (preprint arXiv:math/0208155).

**Current version: Draft 2 of the corrected and expanded version
(2026-11-22).** `toric-codes.tex` and `toric-codes.pdf`.

## Contents

- `toric-codes.tex`, `toric-codes.pdf`: the corrected and expanded paper (29 pages).
- `original/toric_code7.tex`: the 2003 manuscript source (dated September 1, 2003).
- `referee/2026-11-22/toric_codes_referee_report.tex`: the referee report on
  the 2003 manuscript by OpenAI's ChatGPT. It uses the newtx fonts, so no PDF
  is included here.
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

## Pending

- Check the copyright position before treating this corrected version of the
  published paper as public (style guide, rule 8.6).
- Compile once with the newtx fonts installed. Only the mathptmx fallback has
  been compiled.
- Check the page citations carried over from 2003 (Fulton, Stichtenoth,
  MacWilliams–Sloane) against the sources.
- Decide whether Section 8 stays in the paper or moves to a companion note.
