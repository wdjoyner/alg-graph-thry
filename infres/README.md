# Inflation-restriction in non-abelian cohomology: centralizer obstructions, Weil groups, and voltage graphs

David Joyner and Claude (an AI system developed by Anthropic).

An expository paper. No originality is claimed for its results. Until Draft 2
the title was "Notes on the inflation-restriction sequence in non-abelian
cohomology", which is the title of the original manuscript.

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
graphs and gain graphs on the Cayley graph of `Gamma`. Draft 2 adds a
choice-free obstruction extension, the generalization to a non-abelian normal
subgroup `N`, and the description of the extension `W` by its monodromy on the
first homology of the Cayley graph of `Gamma` (the relation module).

A detailed running example, the Weil group of `Q_3(i)/Q_3` with coefficients
in `C^x` and `SL_2(C)`, is carried through Sections 2 to 8, at the end of
each section.

Current version: **Draft 5. Corrected and expanded version** (November 27, 2026).
Draft 3 brought the paper into the house style (`joyner-math-paper-style-guide.md`,
in the repository `wdjoyner/trace-formulas`). ChatGPT reviewed Draft 3 and prepared
Draft 4, which moves notation and literature review into the Introduction and
introduces the graph theory (new Section 3) before the obstruction theory. Draft 5
(Claude) adds motivation, following notes by Gemini ("Carbon"): Section 1.1, the
openings of Sections 3 to 8, Remark 8.3 and Section 9.1. Draft 5 adds no new result.
Gemini refereed the original manuscript and ChatGPT refereed Draft 1.

## Files

| File | What it is |
| --- | --- |
| `infres.tex` / `.pdf` | The note (current draft) |
| `revision-log.tex` / `.pdf` | Responses to both referee reports, all comparisons with the original manuscript, changes between drafts with numbering concordances, conformance to the style guide, original versus new results, AI usage, sources consulted and not consulted, open items |
| `original/infres.tex` | The original, undated AMS-TeX manuscript, unchanged |
| `referee/2026-11-26/` | Referee report on the original (Gemini, "Carbon"), as received |
| `referee/2026-11-26-chatgpt/` | Referee report on Draft 1 (ChatGPT), as received |
| `referee/2026-11-27-chatgpt/` | Review of Draft 3 (ChatGPT), as received; Draft 4 carries it out |
| `referee/2026-11-27-carbon/` | Notes on motivating the paper (Gemini, "Carbon"), as received; used in Draft 5 |
| `LICENSE-manuscript.txt` | CC BY 4.0 license for the manuscript, LaTeX sources and revision log |
| `verification/` | A script that checks the main results by brute force on twenty-seven small examples, five of them with non-abelian `N`, and its output (MIT license) |

To compile: run `pdflatex` three times on `infres.tex`, then twice on
`revision-log.tex`. The revision log takes its theorem numbers from the
note's `.aux` file through the `xr` package, so compile the note first.
The preamble uses `mathptmx` and TikZ.

## Verification

```
cd verification
python3 infres_checks.py
```

The script needs only Python 3 and runs in about six minutes. Its output is
in `verification/checks_output.txt`. See `verification/README.md`.
