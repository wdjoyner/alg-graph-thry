# alg-graph-thry

Papers by David Joyner and collaborators in algebra, algebraic graph theory and coding theory, most of them older manuscripts corrected and expanded with AI assistance in 2026, together with a SageMath module for harmonic morphisms of graphs. Each paper has its own folder with the LaTeX source, the PDF, a revision log and verification scripts; each folder's README gives the files and the current draft.

## Papers

| Folder | Paper | Summary |
|---|---|---|
| [`commutation-transitive/`](commutation-transitive/) | *The representation theory of finite commutation transitive groups* (D. Joyner; manuscript of 2000) | An expository note on finite groups in which commuting is a transitive relation on noncentral elements, or on nonidentity elements (CT groups). It covers the classification of finite CT groups and the characters induced from centralizers, with an exact irreducibility criterion and a spanning theorem via Brauer induction, and shows that the class map from the commuting graph onto the commuting conjugacy class graph is a harmonic morphism. Several natural conjectures are settled, mostly by counterexamples. |
| [`complement-regularity/`](complement-regularity/) | *Which S_m have a complement in S_n?* (D. Joyner; 1997, revised 2007) | Characterizes complements to S_m in S_n through sharply multiply transitive groups and classifies them, gives an exact three-factor decomposition of S₁₂, and shows that a complement to S_{n−k} makes the arrangement graph a Cayley graph; harmonic morphisms arising as group quotients, such as the covering of the Johnson graph by the arrangement graph. |
| [`harmonic-quotient/`](harmonic-quotient/) | *Harmonic quotient morphisms of regular graphs: examples* (D. Joyner and C. Melles) | Many examples of harmonic morphisms from regular graphs of degree 3, 4 and 5 with up to 12 vertices onto small graphs, with emphasis on quotient morphisms Γ → Γ/G by subgroups G of the automorphism group. |
| [`infres/`](infres/) | *Inflation-restriction in non-abelian cohomology: centralizer obstructions, Weil groups, and voltage graphs* (D. Joyner and Claude) | For an extension 1 → N → W → Γ → 1 with N abelian, such as a relative Weil group, and a Γ-group A, an account of the non-abelian inflation-restriction sequence. A homomorphism N → A with Γ-invariant conjugacy class extends to a 1-cocycle of W exactly when an obstruction in Springer's non-abelian H² with coefficients in its centralizer is neutral; the paper describes the fibers of restriction, shows that the centralizer cannot be replaced by A, and recasts the criterion in terms of voltage graphs. Expository. |
| [`mog/`](mog/) | *MINIMOGs and Mathematical Blackjack* (D. Joyner; manuscript of 2000) | Three descriptions of the Steiner system S(5,6,12) (via PSL(2,11), Curtis's kitten, and Conway's MINIMOG), the hexads as a maximum independent set of the Johnson graph J(12,6), and the game of mathematical blackjack, whose losing positions are exactly the hexads. |
| [`toric-codes/`](toric-codes/) | *Toric codes over finite fields* (D. Joyner; AAECC 15 (2004)) | Codes from toric surfaces over 𝔽_q: dimension and duality, minimum distances of Hansen's families via an Alon–Füredi-type counting lemma, counterexamples to two natural lower bounds, an error-correcting-pair decoding algorithm, and the [49,11,28] code over 𝔽₈ verified exhaustively. |
| [`toric-repns/`](toric-repns/) | *Representations of finite groups on the Riemann–Roch space of a toric variety* (D. Joyner; 2002) | Finite-group actions on lattice-point bases of toric Riemann–Roch spaces: induced permutation modules, fixed-point and weighted character formulas, affine lattice symmetries and their monomial linearizations, and graph-theoretic interpretations, with examples including a singular toric surface with an involution, graphic zonotopes, and Johnson-graph eigenspaces. |

The status of each paper (current draft, refereeing, open points) is in its folder's README and revision log. Most are AI-assisted working drafts that have not been independently refereed.

## SageMath module

`alg-graph-thry2.sage` contains functions for oriented graphs and harmonic morphisms, following the work of Biggs and of Baker–Norine (harmonic morphism checks, walks, cycle bases, zeta polynomials of graphs and more). Its manual is `alg-graph2-python-module_manual.tex` / `.pdf`.

## License

See [`LICENSE`](LICENSE) and the license files in the individual folders.
