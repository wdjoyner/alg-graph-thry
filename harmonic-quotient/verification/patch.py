"""Apply verified corrections to a copy of the manuscript.  Every edit must match exactly once
inside its scope (an example block, a list item, or the whole file)."""
import re, sys
SRC = '../archive/regular-graph-harmonic-quotient-examples_2023-03-26.tex'
OUT = '../regular-graph-harmonic-quotient-examples.tex'
T = open(SRC).read()
log = []

def span(scope):
    if scope is None: return 0, len(T)
    kind, name = scope
    if kind == 'ex':
        m = re.search(r'\\begin\{example\}%\s*' + name + r'\b.*?\\end\{example\}', T, re.S)
    else:  # list item
        m = re.search(r'\{\\tt\s*' + name + r'\}(?:\\newline)?.*?(?=\\item|\\end\{enumerate\})', T, re.S)
    assert m, scope
    return m.start(), m.end()

def sub(scope, old, new, after=None, nth=None):
    """Replace `old` by `new` inside scope; if `after` is given, search only after that anchor
    (first occurrence of old after the anchor)."""
    global T
    a, b = span(scope)
    blk = T[a:b]
    base = 0
    if after is not None:
        k = blk.find(after); assert k >= 0 and blk.count(after) == 1, ('anchor', scope, after)
        base = k
        k2 = blk.find(old, base); assert k2 >= 0, ('old-after', scope, old)
        # stop at next \end{tabular} or next anchor-like boundary if table edit
        pos = k2
    else:
        c = blk.count(old)
        assert c == 1, (f'count={c}', scope, old[:80])
        pos = blk.find(old)
    T = T[:a] + blk[:pos] + new + blk[pos + len(old):] + T[b:]
    log.append(f'{scope}: {old[:60]!r} -> {new[:60]!r}')

def row(x, phi, m, nu):
    return f'  {x}   &    {phi}   &        {m}         &  {nu}   \\\\'

def replace_table(scope, after, new_rows):
    """Replace the body rows of the first tabular after anchor `after` in scope."""
    global T
    a, b = span(scope)
    blk = T[a:b]
    k = blk.find(after); assert k >= 0 and blk.count(after) == 1, ('anchor', scope, after)
    tb = blk.find('\\begin{tabular}', k)
    t0 = blk.find('\\\\', tb) + 2          # end of header row
    rest = blk[t0:]
    if rest.lstrip(' ').startswith('\\hline'):
        t0 += rest.find('\\hline') + len('\\hline')
    t1 = blk.find('\\end{tabular}', t0)
    body = '\n' + '\n'.join(new_rows) + '\n'
    T = T[:a] + blk[:t0] + body + blk[t1:] + T[b:]
    log.append(f'{scope}: table after {after[:40]!r} replaced')

# ---------------------------------------------------------------- general text
sub(None, """Indeed, in 1880 P.G. Tait conjectured
(roughly speaking) that every $2$-connected cubic graph is Hamiltonian.
While it's known this conjecture is false, the counterexamples are exceptional
(e.g., the Petersen graph).""",
"""Indeed, P.G. Tait conjectured (1884) that every $3$-connected planar
cubic graph is Hamiltonian. This conjecture is false (Tutte, 1946), but the
counterexamples are exceptional: the smallest ones have $38$ vertices.
(The non-Hamiltonian Petersen graph is $3$-connected and cubic, but it is not
planar, so it is not a counterexample to Tait's conjecture.)""")

# ---------------------------------------------------------------- d3reg6
sub(None, """It has $360$ non-trivial harmonic morphisms to $St_4$, $36$ non-trivial harmonic
morphisms to $P_3$, $102$ to $P_4$, $12$ to $P_5$,
$6$ non-trivial harmonic morphisms""", """It has
$6$ non-trivial harmonic morphisms""")
sub(None, """quasicover with constant vertical multiplicity $1$.} to $C_3$,
There are no non-trivial harmonic morphisms to $P_6$, to the
diamond graph (with $4$ vertices), nor are there any to $K_4$.""",
"""quasicover with constant vertical multiplicity $1$.} to $C_3$.
There are no non-trivial harmonic morphisms to $St_4$, $P_3$, $P_4$, $P_5$, $P_6$, to the
diamond graph (with $4$ vertices), nor are there any to $K_4$.
(Since the diameter is $2$, there are none to $P_k$ for $k\\geq 4$.)""")
sub(None, """It has $444$ non-trivial harmonic morphisms\\footnote{At least one of these is a
harmonic quotient morphism to $St_4$. That morphism is a homomorphism.}
to $St_4$, $48$ non-trivial harmonic
morphisms to $P_3$, $72$ to $P_4$, $72$ to $P_5$,
$36$ non-trivial harmonic morphisms""",
"""It has $12$ non-trivial harmonic morphisms\\footnote{At least one of these is a
harmonic quotient morphism to $St_4$. That morphism is a homomorphism.}
to $St_4$, $12$ non-trivial harmonic
morphisms to $P_3$,
$36$ non-trivial harmonic morphisms""")
sub(None, """quasicover with constant vertical multiplicity $1$.} to $C_3$,
There are no non-trivial harmonic morphisms to $P_6$, to the
diamond graph, nor are there any to $K_4$.""",
"""quasicover with constant vertical multiplicity $1$.} to $C_3$.
There are no non-trivial harmonic morphisms to $P_4$, $P_5$, $P_6$, to the
diamond graph, nor are there any to $K_4$.
(Since the diameter is $2$, there are none to $P_k$ for $k\\geq 4$.)""")

# ---------------------------------------------------------------- d3reg8
sub(None, """There are five $3$-regular graphs with $8$ vertices, two of which are
vertex transitive but none are edge transitive.""",
"""There are five $3$-regular graphs with $8$ vertices, two of which
(the cube and the Wagner graph) are vertex transitive; only the cube is
edge transitive.""")
sub(None, "  d3reg8a & (8, [4,-2,4,2], 2) & 16", "  d3reg8a & (8, [2,2,-2,-2], 2) & 16")
sub(None, "  d3reg8b & (8, [2,2,-2,-2], 2) & 4", "  d3reg8b & (8, [4,-2,4,2], 2) & 4")
sub(('ex', 'd3reg8a'), "In this case, there are $13$ non-constant", "In this case, there are $14$ non-constant")
sub(('ex', 'd3reg8a'), "and $6$ are\\footnote{All these are also the same",
    "and $7$ are\\footnote{All these are also the same")
sub(('ex', 'd3reg8a'), "really only $1$ distinct harmonic quotient morphism to $P_2$.}",
    "really only $1$ distinct harmonic quotient morphism to $P_2$. One of the $7$ groups is $Aut(\\Gamma_2)$ itself.}")
sub(('ex', 'd3reg8b'), """In this case, there is only $1$ harmonic quotient morphism
$\\pi: \\Gamma_2\\to \\Gamma_2/G$, for some subgroup
$G$ of $Aut(\\Gamma_2)$.""",
"""In this case, there are only $2$ harmonic quotient morphisms
$\\pi: \\Gamma_2\\to \\Gamma_2/G$, for some subgroup
$G$ of $Aut(\\Gamma_2)$. For $G=Aut(\\Gamma_2)$ (of order $4$) the quotient is
$P_3$, with fibers $\\{0,4\\}$, $\\{1,3,5,7\\}$, $\\{2,6\\}$.""")
replace_table(('ex', 'd3reg8b'), "is isomorphic to the diamond graph.",
              [row(x, p, 1, n) for x, p, n in zip(range(8), [2, 1, 3, 0, 2, 1, 3, 0], [1, 0, 1, 0, 1, 0, 1, 0])])
sub(('ex', 'd3reg8d'), "really only $17$ distinct harmonic quotient morphisms to $P_2$.}",
    "really only $11$ distinct harmonic quotient morphisms to $P_2$.}")
sub(('ex', 'd3reg8d'), """Figure \\ref{fig:harmonic-quotient_d3reg8d-C4_11320023} and
tabulated above.""", """Figure \\ref{fig:harmonic-quotient_d3reg8d-C4_11320023} and
tabulated below.""")
sub(('ex', 'd3reg8d'), "\\caption{The Wagner graph  $\\Gamma_2$ ({\\tt d3reg8d})", "\\caption{The cube graph  $\\Gamma_2$ ({\\tt d3reg8d})")
sub(('ex', 'd3reg8e'), """Figure \\ref{fig:harmonic-quotient_d3reg8e-C4_03211230} and
tabulated above.""", """Figure \\ref{fig:harmonic-quotient_d3reg8e-C4_03211230} and
tabulated below.""")
replace_table(('ex', 'd3reg8e'), "When $G=\\langle (0,7)(1,6)(2,5)(3,4) \\rangle$",
              [row(x, p, 1, 1) for x, p in zip(range(8), [0, 3, 2, 1, 1, 2, 3, 0])])

# ---------------------------------------------------------------- d3reg10
sub(None, "x^{10} - 15x^8 - 4x^7 + 63x^6 + 63x^5 - 61x^4", "x^{10} - 15x^8 - 4x^7 + 63x^6 + 36x^5 - 61x^4")
sub(None, "x^{10} - 15x^8 + 71x^6 - 15x^5 - 133x^4", "x^{10} - 15x^8 + 71x^6 - 16x^5 - 133x^4")
sub(None, "are no on-trivial harmonic morphisms to $P_k$, for $k\\geq 5$.", "are no non-trivial harmonic morphisms to $P_k$, for $k\\geq 5$.")
sub(('ex', 'd3reg10e'), "  4   &    3   &        1         &  0   \\\\", "  4   &    3   &        1         &  1   \\\\")
sub(('ex', 'd3reg10f'), """This graph has no non-constant harmonic quotient
morphisms $\\pi: \\Gamma_2\\to \\Gamma_2/G$, for some subgroup
$G$ of $Aut(\\Gamma_2)$.""",
"""This graph has exactly one non-constant harmonic quotient
morphism $\\pi: \\Gamma_2\\to \\Gamma_2/G$, for a subgroup
$G$ of $Aut(\\Gamma_2)$, namely for
$G=Aut(\\Gamma_2)=\\langle (0,5)(1,6)(2,7)(3,8)(4,9)\\rangle$.
It is a degree two quasicover of a graph with $5$ vertices and $7$ edges
(isomorphic to $\\overline{P_2\\cup P_3}$).""")
sub(('ex', 'd3reg10k'), """This graph has only $1$ non-constant harmonic quotient
morphisms""", """This graph has only $2$ non-constant harmonic quotient
morphisms""")
sub(('ex', 'd3reg10k'), """Note that vertices $3$ and $4$ are those with degree $3$.""",
"""Note that vertices $3$ and $4$ are those with degree $3$.
(The other harmonic quotient is for $G=Aut(\\Gamma_2)$, of order $4$; it is a
quotient to $P_3$, with fibers $\\{0,1,5,6\\}$, $\\{2,4,7,9\\}$, $\\{3,8\\}$.)""")
sub(('ex', 'd3reg10k'), """associated to the subgroup
$G=\\langle (0,1,2)(3,9,7)(4,5,6)\\rangle$
is tabulated below.""", """associated to this subgroup
is tabulated below.""")
sub(('ex', 'd3reg10m'), "This graph has only $4$ non-constant", "This graph has only $5$ non-constant")
sub(('ex', 'd3reg10m'), """For the remaining two subgroups,
the quotient""", """For the remaining three subgroups (one of which is $Aut(\\Gamma_2)$),
the quotient""")
sub(('ex', 'd3reg10m'), "to $P_3$ and both quotient morphisms are the same.", "to $P_3$ and all three quotient morphisms are the same.")
sub(('ex', 'd3reg10n'), "This graph has $31$ non-constant", "This graph has $32$ non-constant")
sub(('ex', 'd3reg10n'), """Eight of these groups yield the same harmonic quotient morphism to
$K_{2,3}$""", """Two of these groups yield (two distinct) harmonic quotient morphisms to
$K_{2,3}$""")
sub(('ex', 'd3reg10n'), "One of these is tabulated below and the uncolored graphs is",
    "One of these is tabulated below and the uncolored graphs are")
sub(('ex', 'd3reg10n'), """The remaining harmonic quotient morphisms are either to $P_3$ or to
$P_2$.""", """Six further groups (each of order $2$) yield six distinct degree two
harmonic quotient morphisms to the genus $3$ graph $\\overline{P_2\\cup P_3}$
($5$ vertices, $7$ edges).

The remaining $19$ harmonic quotient morphisms are to $P_3$ ($6$ groups,
$2$ distinct morphisms) or to $P_2$ ($13$ groups, one of them $Aut(\\Gamma_2)$;
all give the same morphism).""")
replace_table(('ex', 'd3reg10o'), "harmonic quotient morphism to the genus $3$ graph",
              [row(x, p, 1, n) for x, p, n in zip(range(10), [4, 2, 0, 3, 2, 4, 1, 3, 0, 1], [1, 0, 0, 0, 0, 1, 0, 0, 0, 0])])
sub(('ex', 'd3reg10o'), "This is tabulated below (and agrees with a table in a previous example).", "This is tabulated below.", after="harmonic quotient morphism to the genus $3$ graph")
sub(('ex', 'd3reg10p'), """This graph has only $1$ non-constant harmonic quotient
morphisms""", """This graph has only $2$ non-constant harmonic quotient
morphisms""")
sub(('ex', 'd3reg10p'), """harmonic quotient morphism to the house graph
$\\Gamma_1 = (V_1,E_1) = K_{2,3}$""", """harmonic quotient morphism to the house graph
$\\Gamma_1 = (V_1,E_1)$""")
sub(('ex', 'd3reg10p'), """(0, 1), (0, 3), (1, 2), (1, 4), (2, 4), (3, 4)
\\}.
\\]
This is tabulated below.""", """(0, 1), (0, 3), (1, 2), (1, 4), (2, 4), (3, 4)
\\}.
\\]
This is tabulated below. (The other harmonic quotient is for
$G=Aut(\\Gamma_2)$, of order $4$; it is a quotient to $P_3$, with fibers
$\\{0,3,5,8\\}$, $\\{1,2,6,7\\}$, $\\{4,9\\}$.)""")
sub(('ex', 'd3reg10r'), "G = \\langle (0,2)(1,9)(3,6)(4,7)(5,8), (0,9)(1,2)(3,5)(6,8) \\rangle",
    "G = \\langle (0,1)(2,9)(3,8)(4,7)(5,6) \\rangle")
sub(('ex', 'd3reg10r'), "(the same table as in the previus example)", "(the same table as in the previous example)")
sub(('ex', 'd3reg10s'), "$G = \\langle (0,4)(1,3)(5,9)(6,8), (0,4)(1,9)(2,7)(3,5) \\rangle$",
    "$G = \\langle (2,6)(3,8)(4,5)(7,9), (0,1)(2,4)(5,6)(7,9) \\rangle$")

# ---------------------------------------------------------------- d3reg12
sub(None, """including those $4$ which are vertex transitive and
those $4$ that are not Hamiltonian.""", """including those $4$ which are vertex transitive and
four of the five that are not Hamiltonian.""")
sub(None, "  d3reg12g & (12, [3, 3, 3, -3, -3, -3], 2) & 4 & 7  \\\\",
    "  d3reg12g & (12, [4,2,3,-2,-4,-3,2,3,-2,2,-3,-2], 1) & 4 & 7  \\\\")
sub(('item', 'd3reg12a'), "However, there are $12$ non-trivial harmonic morphisms to $P_3$.",
    "However, there are $8$ non-trivial harmonic morphisms to $P_3$.")
sub(None, "+ 213x^4 + 93x^3 - 60x^2", "+ 213x^4 + 92x^3 - 60x^2")
sub(('item', 'd3reg12g'), """It has $12$ non-trivial harmonic morphisms to $St_4$,
$6$ non-trivial harmonic morphisms to $C_3$, but no
non-trivial harmonic morphisms to $P_3$, $P_4$, $C_4$, or to $K_4$.""",
"""It has $6$ non-trivial harmonic morphisms to $C_3$, but no
non-trivial harmonic morphisms to $St_4$, $P_3$, $P_4$, $C_4$, or to $K_4$.""")
sub(('item', 'd3reg12j'), "are no non-trivial harmonic morphisms to $P_k$, for $k\\geq 6$.",
    "are no non-trivial harmonic morphisms to $P_k$, for $k\\geq 5$.")
sub(('item', 'd3reg12m'), "are no non-trivial harmonic morphisms to $P_k$, for $k\\geq 6$.",
    "are no non-trivial harmonic morphisms to $P_k$, for $k\\geq 5$.")
sub(None, "+ 512x^3 - 192x^2 \\, .", "+ 512x^3 + 192x^2 \\, .")
sub(None, "x^{12} - 18x^{10} + 105x^8 - 236x^6 + 144x^4", "x^{12} - 18x^{10} + 105x^8 - 232x^6 + 144x^4")
sub(('ex', 'd3reg12h'), "This graph has $52$ non-constant", "This graph has $53$ non-constant")
sub(('ex', 'd3reg12h'), "Four of these $52$ are distinct", "Four of these $53$ are distinct")
sub(('ex', 'd3reg12h'), "Four of the remaining $48$ are distinct", "Four of the remaining $49$ are distinct")
sub(('ex', 'd3reg12h'), "Four of the remaining $44$ are distinct", "Four of the remaining $45$ are distinct")
sub(('ex', 'd3reg12h'), "Eight of the remaining $40$ are non-constant", "Eight of the remaining $41$ are non-constant")
sub(('ex', 'd3reg12h'), "G_1=\\langle (0,11)(1,10)(2,7)(3,8)(4,9)(5,6) \\rangle",
    "G_1=\\langle (0,11)(1,8)(2,7)(3,10)(4,9)(5,6) \\rangle")
sub(('ex', 'd3reg12h'), "One of these quotients, for the subgroup\\footnote{Note the $G_2$ is a normal subgroup of $G_3$. Also note that $C_3$ is a quotient graph of the barbell\ngraph $Barbell(3,0)$.}",
    "One of these quotients, for the subgroup\\footnote{Note that $G_2\\not\\subset G_3$. However, the first generator $a$ of $G_3$ generates a subgroup of index $2$ (hence normal) in $G_3$, and $\\Gamma_2/\\langle a\\rangle$ is also isomorphic to $Barbell(3,0)$. Also note that $C_3$ is a quotient graph of the barbell\ngraph $Barbell(3,0)$.}")
sub(('ex', 'd3reg12h'), "G_3=\\langle (0,5)(1,2)(3,4)(6,11)(7,8)(9,10), (0,6)(1,9)(2,8)(3,7)(4,10)(5,11) \\rangle",
    "G_3=\\langle (0,5)(1,2)(3,4)(6,11)(7,10)(8,9), (0,11)(1,8)(2,9)(3,10)(4,7)(5,6) \\rangle")
sub(('ex', 'd3reg12h'), "with a degree two harmonic quotient morphism to and quasicover of, $\\Gamma_1=C_3=\\Gamma_2/G_3$.}",
    "with a degree four harmonic quotient morphism to and quasicover of, $\\Gamma_1=C_3=\\Gamma_2/G_3$.}")
sub(('ex', 'd3reg12h'), "\\label{fig:harmonic-quotient_d3reg12h+C3}\n\\end{figure}\n",
    "\\label{fig:harmonic-quotient_d3reg12h+C3}\n\\end{figure}\n\nThe remaining $33$ (one of which is $G=Aut(\\Gamma_2)$) all give the same\nharmonic quotient morphism, to $P_2$.\n")
sub(('ex', 'd3reg12j'), "This graph has $14$ non-constant", "This graph has $15$ non-constant")
sub(('ex', 'd3reg12j'), "One of the remaining $12$ is a non-constant", "One of the remaining $13$ is a non-constant")
sub(('ex', 'd3reg12j'), "Two of the remaining $11$ are distinct", "Two of the remaining $12$ are distinct")
sub(('ex', 'd3reg12j'), """All the quotient morphisms to $P_4$ in the above table are the same,
and all those to $P_2$ are the same.""", """The table omits one subgroup, $G=Aut(\\Gamma_2)$ itself, whose quotient is
also $P_2$. All the quotient morphisms to $P_4$ in the above table are the same,
and all those to $P_2$ are the same.""")
sub(('ex', 'd3reg12m'), "grid graph, $Grid(2,1)$.", "grid graph $P_2\\times P_3$ (the $2\\times 3$ grid, or domino graph).")
sub(('ex', 'd3reg12n'), "with a degree two harmonic quotient morphism to and quasicover of the codomino graph, $\\Gamma_1=\\Gamma_2/G_2$.}",
    "with a degree two harmonic quotient morphism to and quasicover of the co-twin-$C_5$ graph, $\\Gamma_1=\\Gamma_2/G$.}")
sub(('ex', 'd3reg12n'), "the $X_{37}$ graph.\n", "the $X_{37}$ graph\\footnote{This quotient graph is isomorphic to the twin-$C_5$ graph below, so the six quotients described in this and the next paragraph all have the same isomorphism type.}.\n")

# ---------------------------------------------------------------- quartic
sub(None, """the octahedral graph (also known as the graph of the
Fano diagram).""", """the octahedral graph (also known as $K_{2,2,2}$).""")
sub(('ex', 'd4reg6a'), """Of the remaining $53$, $14$ are (not necessarily distinct)
harmonic quotient morphisms to the cycle graph $C_3$. As we
know from the paragraph above, all of these morphisms to $C_3$ are
$2$-multicovers.

The remaining $39$ are (not necessarily distinct)""",
"""Of the remaining $53$, $6$ are
harmonic quotient morphisms to the cycle graph $C_3$ (all six give the same
morphism). As we
know from the paragraph above, all of these morphisms to $C_3$ are
$2$-multicovers. Another $9$ are harmonic quotient morphisms to $P_3$
($3$ distinct morphisms).

The remaining $38$ are (not necessarily distinct)""")
sub(('ex', 'd4reg7b'), "There are $27$ (not necessarily distinct)", "There are $28$ (not necessarily distinct)")
sub(('ex', 'd4reg7b'), """Two of these $27$ are distinct harmonic quotient morphisms""",
    """Two of these $28$ are harmonic quotient morphisms""")
sub(('ex', 'd4reg7b'), """for some $G$, where $\\Gamma_1=K_{2,3}$.""",
    """for some $G$, where $\\Gamma_1=K_{2,3}$; both subgroups
($\\langle (1,6)(3,4)\\rangle$ and $\\langle (1,6),(3,4)\\rangle$) give the same morphism.""")
sub(('ex', 'd4reg7b'), "Two of the remaining $25$ are distinct", "Two of the remaining $26$ are distinct")
sub(('ex', 'd4reg7b'), "Three of the remaining $23$ are", "Three of the remaining $24$ are")
sub(('ex', 'd4reg7b'), "Six of the remaining $20$ are", "Eight of the remaining $21$ are")
sub(('ex', 'd4reg7b'), "The remaining $14$ are (not necessarily distinct)", "The remaining $13$ (one of them for $G=Aut(\\Gamma_2)$; all give the same morphism) are")
sub(('ex', 'd4reg7b'), "is the path graph of length $2$.", "is the path graph on $2$ vertices.")
sub(('ex', 'd4reg7b'), "is the path graph of length $3$.", "is the path graph on $3$ vertices (all eight give the same morphism).")
sub(('item', 'd4reg8c'), "girth $3$, circumference $8$,\nchromatic number $2$,", "girth $4$, circumference $8$,\nchromatic number $2$,")
sub(('ex', 'd4reg8c'), """$\\pi: \\Gamma_2\\to \\Gamma_2/G = P_3$, for some $G$.
}""", """$\\pi: \\Gamma_2\\to \\Gamma_2/G = P_3$, for some $G$.
The remaining $1327$ consist of $12$ quotients with $6$ vertices,
$18$ quotients to the star graph $St_5$, and $1297$ quotients to $P_2$.
}""")
sub(('ex', 'd4reg8d'), "There are $11$ (not necessarily distinct)", "There are $12$ (not necessarily distinct)")
sub(('ex', 'd4reg8d'), "Of the remaining $9$, $3$ are", "Of the remaining $10$, $3$ are")
sub(('ex', 'd4reg8d'), "Of the remaining $6$, $636$ are (not necessarily distinct)",
    "The remaining $7$ (one of them for $G=Aut(\\Gamma_2)$) are (not necessarily distinct)")
sub(('ex', 'd4reg8e'), """There is exactly one harmonic quotient morphism
$\\pi: \\Gamma_2\\to \\Gamma_1=\\Gamma_2/G$,
for some subgroup $G$ of $Aut(\\Gamma_2)$.
Tabulated below, this is a quotient morphism""",
"""There are exactly two harmonic quotient morphisms
$\\pi: \\Gamma_2\\to \\Gamma_1=\\Gamma_2/G$,
for some subgroup $G$ of $Aut(\\Gamma_2)$.
For $G=Aut(\\Gamma_2)$ (of order $4$) the quotient is $C_3$, with fibers
$\\{0,1,2,4\\}$, $\\{3,6\\}$, $\\{5,7\\}$.
The other, tabulated below, is a quotient morphism""")
sub(('ex', 'd4reg8f'), "There are two (identical) harmonic quotient morphisms",
    "There are three (identical) harmonic quotient morphisms")
sub(('ex', 'd4reg8f'), """and the other is

\\[
G_2 = \\langle (1,2)(3,4)(6,7), (0,4,3)(5,7,6) \\rangle.
\\]
Each has cardinality $6$.""", """another is

\\[
G_2 = \\langle (1,2)(3,4)(6,7), (0,4,3)(5,7,6) \\rangle,
\\]
and the third is $Aut(\\Gamma_2)$, of order $12$.
The first two have cardinality $6$.""")
sub(None, "Below, we include $8$ of these $16$ as examples.", "Below, we include $9$ of these $16$ as examples.")
sub(('ex', 'd4reg9a'), "There are $11$ harmonic quotient morphisms", "There are $12$ harmonic quotient morphisms")
replace_table(('ex', 'd4reg9a'), "G = \\langle (1,2)(4,5)(7,8) \\rangle.",
              [row(x, p, m, n) for x, p, m, n in zip(range(9), [1, 3, 3, 0, 2, 2, 4, 5, 5], [2, 1, 1, 2, 1, 1, 2, 1, 1], [0, 1, 1, 0, 1, 1, 0, 0, 0])])
sub(('ex', 'd4reg9a'), "One of the remaining $8$ is a harmonic quotient homomorphism", "One of the remaining $9$ is a harmonic quotient homomorphism")
replace_table(('ex', 'd4reg9a'), "G = \\langle (0,6)(1,5)(2,4) \\rangle.",
              [row(x, p, m, 0) for x, p, m in zip(range(9), [3, 2, 1, 0, 1, 2, 3, 5, 4], [1, 1, 1, 2, 1, 1, 1, 2, 2])])
sub(('ex', 'd4reg9a'), "  {\\rm genus}(\\Gamma_1) =6,", "  {\\rm genus}(\\Gamma_1) =4,")
sub(('ex', 'd4reg9a'), "All the $7$ remaining harmonic quotients map to $P_2$ or $P_3$ or the",
    "All the $8$ remaining harmonic quotients (one of them for $G=Aut(\\Gamma_2)$) map to $P_2$ or $P_3$ or the")
replace_table(('ex', 'd4reg9a'), "G = \\langle (1,2)(4,5)(7,8), (0,6)(1,4)(2,5)(7,8) \\rangle,",
              [row(x, p, m, n) for x, p, m, n in zip(range(9), [1, 2, 2, 0, 2, 2, 1, 3, 3], [2, 1, 1, 4, 1, 1, 2, 2, 2], [0, 1, 1, 0, 1, 1, 0, 0, 0])])
sub(('ex', 'd4reg9b'), """There are no harmonic quotient morphisms
$\\pi: \\Gamma_2\\to \\Gamma_1=\\Gamma_2/G$,
for some subgroup $G$ of $Aut(\\Gamma_2)$.""",
"""There is exactly one harmonic quotient morphism
$\\pi: \\Gamma_2\\to \\Gamma_1=\\Gamma_2/G$, namely for
$G=Aut(\\Gamma_2)=\\langle (0,5)(1,6)(2,8)(3,4)\\rangle$; the quotient
has $5$ vertices and $8$ edges.""")
sub(('ex', 'd4reg9c'), "this is a multicover\nof degree $3$ and multiplicity $2$.", "this is a multicover\nof degree $6$ and multiplicity $2$.")
sub(('ex', 'd4reg9c'), "deg(\\phi) =3.", "deg(\\phi) =6.")
sub(('ex', 'd4reg9c'), "with a degree three harmonic quotient homomorphism (in fact, a multicover) to the cycke graph",
    "with a degree six harmonic quotient homomorphism (in fact, a multicover) to the cycle graph")
sub(('ex', 'd4reg9e'), "There are $5$ harmonic quotient morphisms", "There are $6$ harmonic quotient morphisms")
sub(('ex', 'd4reg9e'), "Three of these $5$ are quotients", "Three of these $6$ are quotients")
sub(('ex', 'd4reg9e'), """The remaining two are
(identical morphisms but with different subgroups)""", """The remaining three are
(identical morphisms but with different subgroups, one of which is $Aut(\\Gamma_2)$)""")
sub(('ex', 'd4reg9g'), "  {\\rm genus}(\\Gamma_1) =6,", "  {\\rm genus}(\\Gamma_1) =4,")
sub(('ex', 'd4reg9g'), "Of the remaining $56$, $9$ are", "Of the remaining $53$, $9$ are")
sub(('ex', 'd4reg9g'), "Of the remaining $47$, $8$ are", "Of the remaining $44$, $8$ are")
sub(('ex', 'd4reg9g'), "All of the remaining $39$ are", "All of the remaining $36$ are")
sub(None, "Of all these, $11$ have a non-trivial harmonic morphism to $C_3$.",
    "Of all these, $17$ have a non-trivial harmonic morphism to $C_3$.")
sub(('ex', 'd4reg10b'), """There is only $1$ harmonic quotient morphism
$\\pi: \\Gamma_2\\to \\Gamma_1=\\Gamma_2/G$, for some $G$. 
It happens to be a quasicover of a wheel graph, as shown below.""",
"""There are only $2$ harmonic quotient morphisms
$\\pi: \\Gamma_2\\to \\Gamma_1=\\Gamma_2/G$, for some $G$.
For $G=Aut(\\Gamma_2)$ (of order $4$) the quotient is $C_3$, with fibers
$\\{0,7\\}$, $\\{1,3,6,8\\}$, $\\{2,4,5,9\\}$.
The other happens to be a quasicover of a wheel graph, as shown below.""")
sub(('ex', 'd4reg10d'), """There is $8$ (not necessarily distinct) harmonic quotient morphism""",
    """There are $8$ (not necessarily distinct) harmonic quotient morphisms""")
sub(('ex', 'd4reg10d'), "Six of the remaining $7$ morphisms are to the", "Five of the remaining $7$ morphisms are to the")
sub(('ex', 'd4reg10d'), "The $8$th and last of these harmonic quotient morphisms is to $P_2$.",
    "The last two of these harmonic quotient morphisms are to $P_2$ (and are the same morphism).")
sub(('ex', 'd4reg10e'), """This multicover example is tabulated below.""",
    """This multicover example is tabulated below. (All $158$ subgroups with a
$5$-vertex quotient give this same morphism.)""")
sub(('ex', 'd4reg10e'), "  {\\rm genus}(\\Gamma_1) =1,\n\\]\n\\[\ndeg(\\phi) =2.", "  {\\rm genus}(\\Gamma_1) =1,\n\\]\n\\[\ndeg(\\phi) =4.")
sub(('ex', 'd4reg10f'), "arise as a quotient with\n$3$ vertices isomorphic to the graph $P_2$.",
    "arise as a quotient with\n$2$ vertices isomorphic to the graph $P_2$.")
sub(None, "Of all $265$ graphs, only $48$ have", "Of all $265$ graphs, only $52$ have")
sub(None, """If we counted correctly (``by hand''),
there are $100$""", """There are $100$""")
sub(('item', 'd4reg11f'), """There are $9466$ non-trivial harmonic morphisms from $\\Gamma$ to $P_3$ and
$16014$ non-trivial harmonic morphisms from $\\Gamma$ to $P_4$.""",
"""There are $18$ non-trivial harmonic morphisms from $\\Gamma$ to $P_3$ and
none to $P_4$.""")
sub(('item', 'd4reg11f'), """however, there are $3488$ non-trivial harmonic morphisms
from $\\Gamma$ to $C_4$.""", """however, there are $16$ non-trivial harmonic morphisms
from $\\Gamma$ to $C_4$.""")
sub(('item', 'd4reg11g'), "There are $8642$ non-trivial harmonic morphisms from $\\Gamma$ to $P_3$.",
    "There are $18$ non-trivial harmonic morphisms from $\\Gamma$ to $P_3$.")
sub(('item', 'd4reg11g'), """There are $2304$ non-trivial harmonic morphisms
from $\\Gamma$ to $C_4$ but none to $K_4$.""", """There are no non-trivial harmonic morphisms
from $\\Gamma$ to $C_4$ or to $K_4$.""")
sub(('ex', 'd4reg11f'), "  4   &    0   &        2         &  0   \\\\", "  4   &    0   &        1         &  0   \\\\",
    after="\\index{$C_6+C_4+C_4$ graph}")
sub(('ex', 'd4reg11f'), "  9   &    2   &        4         &  0   \\\\", "  9   &    2   &        2         &  0   \\\\",
    after="\\index{$C_6+C_4+C_4$ graph}")
sub(('ex', 'd4reg11f'), "  10   &   0   &        2         &  0  \\\\", "  10   &   0   &        1         &  0  \\\\",
    after="\\index{$C_6+C_4+C_4$ graph}")
sub(('ex', 'd4reg11f'), "with a degree two harmonic quotient morphism to the graph ${\\tt DrG}",
    "with a degree four harmonic quotient morphism to the graph ${\\tt DrG}")
sub(('item', 'd4reg12a'), "critical group of size $293216 = 2^5 7^2 11\\cdot 17$,",
    "critical group of size $393216 = 2^{17}\\cdot 3$,")
sub(('ex', 'd4reg12a'), """All of the $1482$ quotients $\\Gamma_1=\\Gamma_2/G$ having $6$ vertices
are isomorphic to this cycle graph $C_6$.""",
"""Of the $1482$ quotients $\\Gamma_1=\\Gamma_2/G$ having $6$ vertices,
$1330$ are isomorphic to this cycle graph $C_6$ (and all $1330$ give this
same morphism); the others are $120$ quotients to $C_4$ with two pendant
edges at one vertex, $24$ to $\\overline{C_4\\cup K_2}$, and $8$ to the
octahedral graph.""")
sub(('ex', 'd4reg12a'), "  {\\rm genus}(\\Gamma_1) =1,\n\\]\n\\[\ndeg(\\phi) =2.", "  {\\rm genus}(\\Gamma_1) =1,\n\\]\n\\[\ndeg(\\phi) =4.")
sub(('ex', 'd4reg12a'), "with a degree two harmonic quotient morphism to the graph $C_6=",
    "with a degree four harmonic quotient morphism to the graph $C_6=")
sub(('ex', 'd4reg12a'), """All of the $1482$ quotients $\\Gamma_1=\\Gamma_2/G$ having $4$ vertices
are isomorphic to this cycle graph $C_4$.""",
"""Of the $2294$ quotients $\\Gamma_1=\\Gamma_2/G$ having $4$ vertices,
$170$ are isomorphic to this cycle graph $C_4$, $48$ to the diamond graph,
and $2076$ to the path graph $P_4$.""")
sub(('ex', 'd4reg12a'), "deg(\\phi) =3.", "deg(\\phi) =6.")
sub(('ex', 'd4reg12a'), "with a degree three harmonic quotient morphism to the graph $C_4=",
    "with a degree six harmonic quotient morphism to the graph $C_4=")
sub(('ex', 'd4reg12a'), """All of the $1634$ quotients $\\Gamma_1=\\Gamma_2/G$ having $3$ vertices
are isomorphic to this cycle graph $P_3$.""",
"""Of the $1634$ quotients $\\Gamma_1=\\Gamma_2/G$ having $3$ vertices,
$1309$ are isomorphic to the path graph $P_3$ and $325$ to the cycle graph $C_3$.""")
sub(('ex', 'd4reg12a'), "are isomorphic to this cycle graph $P_2$.", "are isomorphic to the path graph $P_2$.")
sub(('ex', 'd4reg12c'), """the quotient morphism $\\pi$ (a quasicover) maps to the $6$ vertex prism graph
$\\pi: \\Gamma_2\\to \\Gamma_1=\\Gamma_2/G $, as tabulated below.
The uncolored graphs""", """the quotient morphism $\\pi$ (a quasicover) maps to the $6$ vertex graph {\\tt Ejmw}
$\\pi: \\Gamma_2\\to \\Gamma_1=\\Gamma_2/G $, as tabulated below.
The uncolored graphs""")
sub(('ex', 'd4reg12c'), "$\\Gamma_1$ has $4$ vertices, satisfy $\\Gamma_4=St_4$.", "$\\Gamma_1$ has $4$ vertices, satisfy $\\Gamma_1=St_4$.")
sub(('ex', 'd4reg12c'), "$\\Gamma_1$ has $3$ vertices, satisfy $\\Gamma_4=C_3$.", "$\\Gamma_1$ has $3$ vertices, satisfy $\\Gamma_1=C_3$.")
replace_table(('ex', 'd4reg12d'), "G = \\langle (1,11)(3,4)(6,8)(9,10), (0,2)(1,11)(3,10)(4,9)(5,7)(6,8) \\rangle ,",
              [row(x, p, m, 0) for x, p, m in zip(range(12), [1, 4, 1, 0, 0, 2, 3, 2, 3, 0, 0, 4], [2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2])])
sub(('ex', 'd4reg12d'), """The remaining $6$ satisfy $\\Gamma_1=C_3$, the cycle graph.
The quotients in this case $\\pi: \\Gamma_2\\to C_3=\\Gamma_2/G$
are multicovers of degree 4 and multiplicity $m=2$.""",
"""The remaining $12$ satisfy $\\Gamma_1=C_3$, the cycle graph
($8$ distinct morphisms).
The quotients in this case $\\pi: \\Gamma_2\\to C_3=\\Gamma_2/G$
are multicovers of degree $8$ and multiplicity $m=2$.""")
sub(('ex', 'd4reg12d'), "  {\\rm genus}(\\Gamma_1) =1,\n\\]\n\\[\ndeg(\\phi) =4.", "  {\\rm genus}(\\Gamma_1) =1,\n\\]\n\\[\ndeg(\\phi) =8.")
sub(('ex', 'd4reg12d'), "is a degree four $2$-multicover of $\\Gamma_1=C_3$.}", "is a degree eight $2$-multicover of $\\Gamma_1=C_3$.}")
sub(('ex', 'd4reg12e'), "of degree 4 and multiplicity $m=2$.", "of degree $8$ and multiplicity $m=2$.")
sub(('item', 'd4reg12f'), "girth $3$, circumference $12$,\ncritical group of size $401408", "girth $4$, circumference $12$,\ncritical group of size $401408")
sub(('ex', 'd4reg12f'), "It has $75$  non-trivial harmonic quotient morphisms", "It has $76$  non-trivial harmonic quotient morphisms")
sub(('ex', 'd4reg12f'), "and $22$ in the case $\\Gamma_1$ has $2$ vertices", "and $23$ in the case $\\Gamma_1$ has $2$ vertices")
sub(('ex', 'd4reg12f'), """Of the $30$ non-trivial harmonic quotient morphisms
$\\pi: \\Gamma_2\\to \\Gamma_1=\\Gamma_2/G$, in the case where
$\\Gamma_1$ has $6$ vertices""", """Of the $30$ non-trivial harmonic quotient morphisms
$\\pi: \\Gamma_2\\to \\Gamma_1=\\Gamma_2/G$, in the case where
$\\Gamma_1$ has $4$ vertices""")
sub(('ex', 'd4reg12f'), "these quotients to the ath graph $P_4$", "these quotients to the path graph $P_4$")
sub(('ex', 'd4reg12f'), "  {\\rm genus}(\\Gamma_1) =0,\n\\]\n\\[\ndeg(\\phi) =4.", "  {\\rm genus}(\\Gamma_1) =0,\n\\]\n\\[\ndeg(\\phi) =8.")
sub(('ex', 'd4reg12f'), "a degree 4 harmonic quotient to the path graph", "a degree 8 harmonic quotient to the path graph")
sub(('ex', 'd4reg12f'), "All $22$ of the non-trivial harmonic quotient morphisms", "All $23$ of the non-trivial harmonic quotient morphisms")

# ---------------------------------------------------------------- quintic
sub(('item', 'd5reg8a'), """There are no non-trivial harmonic morphisms from $\\Gamma$ to $P_3$, $P_4$,
$C_3$, $C_4$, or to $K_4$.""", """There are $6$ non-trivial harmonic morphisms from $\\Gamma$ to $P_3$,
but none to $P_4$, $C_3$, $C_4$, or to $K_4$.""")
sub(('ex', 'd5reg8a'), "It has $6$  non-trivial harmonic quotient morphisms", "It has $7$  non-trivial harmonic quotient morphisms")
sub(('ex', 'd5reg8a'), "and $4$ in the case $\\Gamma_1$ has $2$ vertices", "and $5$ in the case $\\Gamma_1$ has $2$ vertices (one of them for $G=Aut(\\Gamma_2)$)")
sub(('ex', 'd5reg8b'), "  {\\rm genus}(\\Gamma_1) =1,\n\\]\n\\[\ndeg(\\phi) =2.", "  {\\rm genus}(\\Gamma_1) =1,\n\\]\n\\[\ndeg(\\phi) =4.")
sub(('ex', 'd5reg8b'), "\\caption{The quartic graph $\\Gamma_2$ ({\\tt d5reg8b}) is a degree two quasi-multicover",
    "\\caption{The quintic graph $\\Gamma_2$ ({\\tt d5reg8b}) is a degree four quasi-multicover")
sub(('ex', 'd5reg8b'), """All of the quotient morphisms in case
$\\Gamma_1$ has $3$ vertices are to $\\Gamma_1=C_3$. 
However, these are not quasi-multicovers.""",
"""Of the $116$ quotient morphisms in case
$\\Gamma_1$ has $3$ vertices, $24$ are to $\\Gamma_1=C_3$ ($8$ distinct morphisms)
and $92$ are to $P_3$ ($2$ distinct morphisms).
The quotients to $C_3$ are not quasi-multicovers.""")
sub(('ex', 'd5reg8b'), "\\caption{The quartic graph $\\Gamma_2$ ({\\tt d5reg8b}) has a degree four",
    "\\caption{The quintic graph $\\Gamma_2$ ({\\tt d5reg8b}) has a degree four")
sub(('ex', 'd5reg10c'), "  {\\rm genus}(\\Gamma_1) =1,\n\\]\n\n\\[\ndeg(\\phi) =2.", "  {\\rm genus}(\\Gamma_1) =1,\n\\]\n\n\\[\ndeg(\\phi) =4.")
sub(('ex', 'd5reg10c'), "  {\\rm genus}(\\Gamma_1) =0,\n\\]\n\n\\[\ndeg(\\phi) =4.", "  {\\rm genus}(\\Gamma_1) =0,\n\\]\n\n\\[\ndeg(\\phi) =8.")
sub(('ex', 'd5reg10c'), "is a degree two quasi-$2$-multicover", "is a degree four quasi-$2$-multicover")
sub(('ex', 'd5reg10d'), """subgroup\\footnote{In this example, the subgroup $G$
is actually the center of $Aut(\\Gamma_2)$.}""", """subgroup\\footnote{Here $Aut(\\Gamma_2)$ has trivial center; $G$ is a cyclic
group of order $5$ acting on one side of the bipartition and fixing the other.}""")
sub(('ex', 'd5reg10d'), "subgroup of $Aut(\\Gamma_2)$ or order $2$.", "a subgroup of $Aut(\\Gamma_2)$ of order $2$.")
sub(None, "%last edited by wdj 2023-03-26", "%last edited by wdj 2023-03-26; corrections from a computational referee check, 2026-11-15")

open(OUT, 'w').write(T)
print(len(log), 'edits applied')
