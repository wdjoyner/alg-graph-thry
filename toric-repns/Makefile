LATEX=pdflatex
LATEXFLAGS=-interaction=nonstopmode -halt-on-error

.PHONY: all pdf check clean
all: pdf

pdf: toric-repns.pdf revision-log.pdf

toric-repns.pdf: toric-repns.tex
	$(LATEX) $(LATEXFLAGS) toric-repns.tex
	$(LATEX) $(LATEXFLAGS) toric-repns.tex
	$(LATEX) $(LATEXFLAGS) toric-repns.tex

revision-log.pdf: revision-log.tex
	$(LATEX) $(LATEXFLAGS) revision-log.tex
	$(LATEX) $(LATEXFLAGS) revision-log.tex

check:
	python3 verify_examples.py

clean:
	rm -f *.aux *.log *.out *.toc
