# The representation theory of finite commutation transitive groups

David Joyner.

An expository note on finite groups in which commuting is a transitive relation
on non-central elements (commutation transitive groups), or on non-identity
elements (commutative transitive, or CT, groups). It covers the classification
of finite CT groups and the characters induced from centralizers, with an exact
irreducibility criterion and a spanning theorem via Brauer induction. It also
shows that the class map from the commuting graph onto the commuting conjugacy
class graph is a harmonic morphism. Several false claims of the 2000 draft are
kept as worked counterexamples.

Current version: **Draft 1. Corrected and expanded version** (November 16, 2026).

## Files

| File | What it is |
| --- | --- |
| `commutation-transitive-groups.tex` / `.pdf` | The note (current draft) |
| `revision-log.tex` / `.pdf` | Changes from the 2000 draft, the numbering concordance, AI usage, and sources consulted and not consulted |
| `archive/` | Frozen copy of the original preliminary version (`comm_tr6.tex`, dated 8-5-2000) |
| `referee/` | The referee report on the original |
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
| 2000-08-05 | Preliminary version (original) | See `archive/` |
| 2026-11-16 | Referee report | See `referee/2026-11-16/` |
| 2026-11-16 | Draft 1 | Corrected and expanded expository version, including the new section on harmonic morphisms and the commuting graph; see `revision-log.pdf` (commit `dd94a1d`) |

## License

The LaTeX source is licensed under CC BY 4.0, and the script under MIT. See
`LICENSE`.
