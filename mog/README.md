# MINIMOGs and Mathematical Blackjack

**David Joyner — Draft 2, corrected and expanded version (2026).**

Original manuscript: May 29, 2000.

## Paper summary

This expository paper studies the small Witt design, the Steiner system S(5,6,12). Its 132 six-element blocks, called hexads, have the defining property that every five-element subset of a twelve-point set belongs to exactly one hexad.

The paper develops three equivalent descriptions of this exceptional design: the orbit of a six-point set under PSL(2,11) on the projective line, Curtis's kitten (three affine-plane pictures over the field with three elements), and Conway's MINIMOG (a 3-by-4 array governed by the ternary [4,2,3] tetracode). These constructions connect finite geometry, coding theory, and the symmetry of the Mathieu group M12.

A graph-theoretic treatment identifies the hexads as a maximum independent set of the Johnson graph J(12,6). The partition into hexads and nonhexads is equitable, with quotient matrix [[0,36],[6,30]]. Both counting and spectral arguments establish the sharp independence bound of 132.

The paper also explains mathematical blackjack, an impartial game in which players exchange one of six shared cards labeled 0 through 11 for a smaller unchosen card, keeping the total at least 21. Under the shuffle labeling, the hexads are precisely the losing positions and form the kernel of the directed game graph. If initial deals with total at most 21 are rejected, the probability that the first player has a winning strategy is 773/894 (approximately 86.47%).

The exposition is intended for readers familiar with elementary algebra and combinatorics. It includes worked examples, geometric diagrams, background material, a literature review, a glossary, and questions for further investigation.

## Files

- [mog.pdf](mog.pdf): compiled manuscript.
- [mog.tex](mog.tex): editable LaTeX source (CC BY 4.0).
- [revision-log.pdf](revision-log.pdf) and [revision-log.tex](revision-log.tex): revision history and verification limitations (CC BY 4.0).
- [verify.py](verify.py): exact finite verification (MIT).

## Reproducing the computations

Run `python3 verify.py` with Python 3.8 or newer. The script checks the projective orbit, Steiner system axioms, kitten and MINIMOG constructions, signed patterns, and the classification of legal game positions. No SageMath installation is required.

Compile the TeX files using `pdflatex` (three passes for the main paper to resolve the table of contents and references). A TeX distribution containing the newtx fonts and TikZ is required.
