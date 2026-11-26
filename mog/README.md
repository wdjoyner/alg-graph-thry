# MINIMOGs and Mathematical Blackjack

David Joyner. Draft 2, corrected and expanded version of the manuscript dated May 29, 2000.

The paper describes the small Witt design using the projective line, Curtis's kitten and the tetracode, and gives graph-theoretic interpretations of mathematical blackjack. The new material includes a sharp independence bound for the Johnson graph, an equitable quotient, directed kernels, and the corrected conditional probability of a winning initial deal.

- `mog.tex`: editable paper (CC BY 4.0)
- `mog.pdf`: compiled paper
- `revision-log.tex` and `revision-log.pdf`: revision history and verification limitations (CC BY 4.0)
- `verify.py`: exact finite verification (MIT)

Run `python3 verify.py` with Python 3.8 or newer. Compile the TeX files using `pdflatex` (three passes for the main paper, to resolve the table of contents and references). No SageMath installation is required for the verification script.
