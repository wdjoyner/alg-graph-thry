# Harmonic quotient morphisms of regular graphs: examples

David Joyner and Caroline Melles.

Many examples of harmonic morphisms from regular graphs (degree 3, 4 and 5, up to
12 vertices) to small graphs, with emphasis on harmonic quotient morphisms
Γ₂ → Γ₂/G for subgroups G of Aut(Γ₂).

Current version: **Draft 2** (November 16, 2026).

## Files

| File | What it is |
| --- | --- |
| `regular-graph-harmonic-quotient-examples.tex` / `.pdf` | The paper (current draft) |
| `revision-log.tex` / `.pdf` | Every change from draft to draft, the numbering concordance, and open items |
| `graphics/` | The 104 figure files (recovered from the 2023 PDF) |
| `archive/` | Frozen copy of the original 2023 version (tex and pdf) |
| `referee/` | Referee reports and the diffs they produced |
| `verification/` | Scripts that recheck every table, count and invariant (MIT license) |
| `sage/` | Sage session transcripts formerly appended to the `.tex` file |

To compile: `pdflatex`, then `makeindex`, then `pdflatex` twice. The preamble uses
`newtx` when it is installed and falls back to `mathptmx`.

## Revision history

| Date | Version | Notes |
| --- | --- | --- |
| 2023-03-26 | Draft 0 (original) | Last edited by wdj; see `archive/` |
| 2026-11-15 | Draft 1 | Corrections from a computational referee check; see `referee/2026-11-15/` (commit `295fd16`) |
| 2026-11-16 | Draft 2 | Revision to the authors' style guide; see `revision-log.pdf` |

## License

The LaTeX source and figures are licensed under CC BY 4.0, and the scripts under
MIT. See `LICENSE`.
