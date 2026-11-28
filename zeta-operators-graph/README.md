# Zeta functions and associated operators: corrected edition (graph revision)

This folder contains a style-guided revision of David Joyner's corrected 1981 manuscript with a section on graph-theoretic connections.

- `zeta_operators_corrected_2026d.tex`: revised manuscript; 12-point Times, American English, introduction, literature review, background, notation, results and new graph section.
- `revision_log_2026d.tex`: changes, historical status table, verification caveats and AI attribution.
- `graph_checks.py`: independent finite examples of the graph identities.

The main graph structures are the prime-gap directed ray, weighted incidence boundaries for bounded Sobolev comparison, the exponent-vector lattice of generalized integers, and Fourier modes on residue cycles. All arguments in this corrected edition use tools available before 1981. The graph models do not prove graph-Laplacian isospectrality or the Riemann hypothesis.

For the companion **modern** comparison program, see [grosswald-schnitzer-graph](../grosswald-schnitzer-graph/).

Compile with `pdflatex` twice, in this folder. The document uses TikZ and newtx fonts.

The original typescript itself was not supplied for this revision. The analytic results carried over from the attached 2026c edition still need independent referee verification.
