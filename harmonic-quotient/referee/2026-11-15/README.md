# Referee check, 2026-11-15

A computational referee check of the 2023-03-26 version. All repairs below are applied
in rev 1 (`../../regular-graph-harmonic-quotient-examples.tex`). `corrections.diff`
shows every changed line. The full report, with line numbers and tables, is the Claude
doc "Referee report: Harmonic quotient morphisms of regular graphs — examples":
https://claude.ai/artifact/7mrugUZx8v87mKdhPnZB7D

## Main findings

- **Copied tables and groups.** The d3reg8e table is d3reg8d's and is not harmonic on
  d3reg8e. The φ columns of the d4reg9a coantenna and d4reg12d butterfly tables come
  from neighbouring tables. The m column of d4reg11f's C₆+C₄+C₄ table belongs to the
  DrG map: in the Sage transcript, the `for x in L:` loop overwrites `f0` and `Gamma1`.
  Stated groups in d3reg10k, d3reg10r, d3reg10s and d3reg12h (G₁, G₃) do not give
  their tables.
- **Morphism counts.** 16 of 491 stated counts are wrong. The 6-vertex counts break the
  diameter bound (diameter 2 rules out P₄ and P₅). d4reg11f → P₃ is 18, not 9466.
- **Quotient totals.** The enumeration skips G = Aut(Γ₂). This accounts for every total
  that is one too small (19 examples). Fix the subgroup loop in `has_harmonic_quotient`.
- **Degree.** deg(φ) = Σ m_φ(x) over a fiber. Nine tables gave |G| or the fiber size
  instead; Riemann–Hurwitz confirms the corrected values.
- **Invariants.** 5 characteristic-polynomial coefficients, 2 girths, d4reg12a's
  critical group (393216 = 2¹⁷·3), the summary-table LCF entries for d3reg8a/b and
  d3reg12g, two census totals (17 and 52), and the statement of Tait's conjecture.

## Open items

- Regenerate the quotient totals after fixing `has_harmonic_quotient`.
- Find the source of the d3reg6a/b and d4reg11f/g counts.
- Confirm the name X₃₇ in d3reg12n (the graph is isomorphic to twin-C₅).
