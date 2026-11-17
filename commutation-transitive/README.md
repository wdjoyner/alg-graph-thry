# The representation theory of finite commutation transitive groups

David Joyner.

An expository note on finite groups in which commuting is a transitive relation
on non-central elements (commutation transitive groups), or on non-identity
elements (commutative transitive, or CT, groups). It covers the classification
of finite CT groups and the characters induced from centralizers, with an exact
irreducibility criterion and a spanning theorem via Brauer induction. It also
shows that the class map from the commuting graph onto the commuting conjugacy
class graph is a harmonic morphism. Several natural "naive conjectures" are
stated along the way and settled, most of them by explicit counterexamples.

Current version: **Draft 3. Corrected and expanded version** (November 17, 2026).

## Files

| File | What it is |
| --- | --- |
| `commutation-transitive-groups.tex` / `.pdf` | The note (current draft) |
| `revision-log.tex` / `.pdf` | Changes from the 2000 manuscript to Draft 1, Draft 1 to Draft 2, and Draft 2 to Draft 3, all comparisons with the 2000 manuscript, the numbering concordances, AI usage, and sources consulted and not consulted |
| `referee/` | Referee reports: on the 2000 manuscript (`2026-11-16/`) and on the hand-edited Draft 1 (`2026-11-17/`) |
| `verification/` | A script that rechecks the note's computational claims, and its output (MIT license) |

To compile: run `pdflatex` three times on `commutation-transitive-groups.tex`,
then twice on `revision-log.tex`. The revision log takes its theorem numbers
from the note's `.aux` file through the `xr` package, so compile the note first.
The preamble uses `mathptmx`.

## Verification

```
cd verification
python3 comm_tr_checks.py
```

The script needs Python 3 and NumPy, and runs in about a minute. Its output is in
`verification/checks_output.txt`. See `verification/README.md` for what each
section checks.

## Revision history

| Date | Version | Notes |
| --- | --- | --- |
| 2000-08-05 | Preliminary version (original) | Unpublished. The frozen copy formerly in `archive/` was removed on 2026-11-17; it remains in the git history at commit `dd94a1d` |
| 2026-11-16 | Referee report | See `referee/2026-11-16/` |
| 2026-11-16 | Draft 1 | Corrected and expanded expository version, including the new section on harmonic morphisms and the commuting graph; see `revision-log.pdf` (commit `dd94a1d`) |
| 2026-11-17 | Referee report | On the author's hand-edited Draft 1; see `referee/2026-11-17/` |
| 2026-11-17 | Draft 2 | Comparisons with the 2000 manuscript moved to the revision log, naive conjectures made precise and numbered, corrections from the referee report; see `revision-log.pdf` (commit `d05ec8c`) |
| 2026-11-17 | Draft 3 | Self-contained glossary, TikZ figures of harmonic collapses, new example (Frobenius group of order 21), repository named in the Acknowledgments; see `revision-log.pdf` |

## License

The LaTeX source is licensed under CC BY 4.0, and the script under MIT. See
`LICENSE`.
