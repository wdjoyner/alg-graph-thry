# Harmonic quotient morphisms of regular graphs: examples

David Joyner and Caroline Melles.

Many examples of harmonic morphisms from regular graphs (degree 3, 4 and 5, up to
12 vertices) to small graphs, with emphasis on harmonic quotient morphisms
Γ₂ → Γ₂/G for subgroups G of Aut(Γ₂).

Current version: **Draft 3** (November 16, 2026).

## Files

| File | What it is |
| --- | --- |
| `regular-graph-harmonic-quotient-examples.tex` / `.pdf` | The paper (current draft) |
| `revision-log.tex` / `.pdf` | Every change from draft to draft, the numbering concordance, and open items |
| `graphics/` | The 104 PNG figures recovered from the 2023 PDF. No longer used by the paper; kept until the TikZ figures are approved |
| `archive/` | Frozen copy of the original 2023 version (tex and pdf) |
| `referee/` | Referee reports and the diffs they produced |
| `verification/` | Scripts that recheck every table, count and invariant, and that draw and check the figures (MIT license) |
| `sage/` | Sage session transcripts formerly appended to the `.tex` file |

To compile: `pdflatex`, then `makeindex`, then `pdflatex` twice. The preamble uses
`newtx` when it is installed and falls back to `mathptmx`. The `.tex` file is
self-contained: the figures are TikZ code inside it, so no other files are needed.

## Figures

Every figure is generated from the edge lists and tables in the `.tex` by
`verification/make_figures.py`, which writes the TikZ code into the `.tex` between
`% BEGIN make_figures.py ...` and `% END make_figures.py ...` comments. To change a
layout, edit that script (the `HAND` table) and rerun it; do not edit the TikZ blocks
by hand, since the next run overwrites them. Then run `verification/check_figures.py`,
which reads the drawings back and checks them against the text.

```
cd verification
python3 make_figures.py
python3 check_figures.py
```

In each figure, a vertex of Γ₁ and its fiber in Γ₂ have the same color.

## Revision history

| Date | Version | Notes |
| --- | --- | --- |
| 2023-03-26 | Draft 0 (original) | Last edited by wdj; see `archive/` |
| 2026-11-15 | Draft 1 | Corrections from a computational referee check; see `referee/2026-11-15/` (commit `295fd16`) |
| 2026-11-16 | Draft 2 | Revision to the authors' style guide; see `revision-log.pdf` |
| 2026-11-16 | Draft 3 | All 63 figures redrawn in TikZ from the data in the text; see `revision-log.pdf` |

## License

The LaTeX source and figures are licensed under CC BY 4.0, and the scripts under
MIT. See `LICENSE`.
