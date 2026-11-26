# Notes on the inflation-restriction sequence in non-abelian cohomology

David Joyner and Claude (an AI system developed by Anthropic).

Let `1 -> N -> W -> Gamma -> 1` be a group extension with `N` abelian, for
example the relative Weil group `W_{E/F}` of a finite Galois extension of
p-adic fields (`N = E^x`, `Gamma = Gal(E/F)`), and let `A` be a group with an
action of `Gamma`, for example a complex dual group. The note gives a
self-contained account of the non-abelian inflation-restriction sequence

    1 -> H^1(Gamma, A) -> H^1(W, A) -> H^1(N, A)^Gamma

and determines the image of restriction: a homomorphism `phi: N -> A` with
`Gamma`-invariant conjugacy class is the restriction of a 1-cocycle of `W`
exactly when an obstruction class in Springer's non-abelian `H^2` of `Gamma`,
with coefficients in the centralizer of `phi(N)`, is neutral. It also
describes the fibers of restriction, shows by examples that the centralizer
cannot be replaced by `A`, and recasts the criterion in terms of voltage
graphs and gain graphs on the Cayley graph of `Gamma`.

Current version: **Draft 1. Corrected and expanded version** (November 26, 2026).

## Files

| File | What it is |
| --- | --- |
| `infres.tex` / `.pdf` | The note (current draft) |
| `revision-log.tex` / `.pdf` | Response to the referee report, all comparisons with the original manuscript, original versus new results, AI usage, sources consulted and not consulted, open items |
| `original/infres.tex` | The original, undated AMS-TeX manuscript, unchanged |
| `referee/2026-11-26/` | Referee report on the original (Gemini, "Carbon"), as received |
| `verification/` | A script that checks the main results by brute force on twenty small examples, and its output (MIT license) |

To compile: run `pdflatex` three times on `infres.tex`, then twice on
`revision-log.tex`. The revision log takes its theorem numbers from the
note's `.aux` file through the `xr` package, so compile the note first.
The preamble uses `mathptmx` and TikZ.

## Verification

```
cd verification
python3 infres_checks.py
```

The script needs only Python 3 and runs in about four minutes. Its output is
in `verification/checks_output.txt`. See `verification/README.md`.
