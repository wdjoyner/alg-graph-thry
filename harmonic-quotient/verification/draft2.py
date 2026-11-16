"""Transform Draft 1 (rev 1) of the harmonic-quotient paper into Draft 2 (style-guide pass).
Each literal edit must match exactly once (or the stated number of times)."""
import re, sys
SRC = '/home/claude/alg-graph-thry/harmonic-quotient/regular-graph-harmonic-quotient-examples.tex'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/d2/regular-graph-harmonic-quotient-examples.tex'
D2 = '/home/claude/d2/'
T = open(SRC).read()
log = []

def sub(old, new, count=1):
    global T
    c = T.count(old)
    assert c == count, (c, old[:90])
    T = T.replace(old, new)
    log.append((old[:50], new[:50]))

def rsub(pat, rep, flags=0, expect=None):
    global T
    T, n = re.subn(pat, rep, T, flags=flags)
    if expect is not None: assert n == expect, (n, pat)
    log.append((pat, f'{n} regex replacements'))
    return n

# -------------------------------------------------------------- split off the Sage transcript
end = T.index('\\end{document}') + len('\\end{document}')
transcript = T[end:]
T = T[:end] + '\n'
open(D2 + 'd4reg11f-sage-session.txt', 'w').write(transcript.lstrip('\n'))

# -------------------------------------------------------------- preamble
pre_end = T.index('\\begin{document}')
T = r"""\documentclass[12pt,letterpaper]{article}
% Draft 2, 2026-11-16. Original draft: wdj and C. Melles, 2023-03-26.
% Draft 1 (2026-11-15): corrections from a computational referee check.
% Draft 2 (2026-11-16): revision to the authors' style guide. See revision-log.tex.
\usepackage[T1]{fontenc}
\IfFileExists{newtxmath.sty}{\usepackage{newtxtext,newtxmath}}{\usepackage{mathptmx}}
\usepackage[letterpaper,margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{float}
\usepackage{graphicx}
\usepackage{url}
\usepackage{fancyvrb}
\usepackage{makeidx}
\usepackage{cprotect}
\usepackage{microtype}
\usepackage[hidelinks]{hyperref}
\def\UrlBreaks{\do\/\do\_\do\.\do\-}

\newtheorem{theorem}{Theorem}[section]
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{conjecture}[theorem]{Conjecture}
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{example}[theorem]{Example}
\newtheorem{remark}[theorem]{Remark}
\newtheorem{revremark}{Remark}
\renewcommand{\therevremark}{2026.\arabic{revremark}}

\DeclareMathOperator{\Aut}{Aut}
\DeclareMathOperator{\genus}{genus}
\DeclareMathOperator{\Jac}{Jac}

\def\ppp{{\mathbb{P}}}
\def\hhh{{\mathbb{H}}}
\def\aaa{{\mathbb{A}}}
\def\fff{{\mathbb{F}}}
\def\qqq{\mathbb{Q}}
\def\rrr{\mathbb{R}}
\def\ccc{\mathbb{C}}
\def\zzz{\mathbb{Z}}
\def\nnn{\mathbb{N}}

\makeindex

""" + T[pre_end:]

# -------------------------------------------------------------- title block and new front matter
a = T.index('\\author{David Joyner and Caroline Melles}')
b = T.index('\\section{Definitions}')
title = r"""\title{Harmonic quotient morphisms of regular graphs: examples\thanks{The
original draft of this paper is an unpublished manuscript by the authors,
dated March 26, 2023. Draft~1 (November 15, 2026) corrected errors found by
a computational referee check. Draft~2 (November 16, 2026) revises the paper
to the authors' style guide. The repository
\url{https://github.com/wdjoyner/alg-graph-thry}, folder
{\tt harmonic-quotient}, contains all drafts, a revision log and the
verification scripts.}}
\author{David Joyner\\ {\small\tt wdjoyner@gmail.com} \and Caroline Melles}
\date{Original draft: March 26, 2023. Corrected draft: November 16, 2026 (Draft 2).}
\maketitle

"""
T = T[:a] + title + open(D2 + 'front.tex').read() + T[b + len('\\section{Definitions}'):]

# -------------------------------------------------------------- background tail + notation before constructions
c = T.index('\\section{Several (new?) regular graph constructions}')
T = T[:c] + open(D2 + 'mid.tex').read() + '\n' + T[c:]
sub("""\\section{Several (new?) regular graph constructions}


These are, to the best of our knowledge, original. In any case, they are
mentioned, as an aside, more for amusement of the interested reader than anything else.
""", """\\section{Several (new?) regular graph constructions}
\\label{sec:constructions}

This section gives three ways to build regular graphs from smaller regular
graphs. They are not used later.

These are, to the best of our knowledge, original. In any case, they are
mentioned, as an aside, more for amusement of the interested reader than anything else.

\\begin{revremark}
\\label{rem:constructions}
The claim that constructions (A), (B) and (C) are new was not checked
against the literature in 2026. Each construction does produce a
$k$-regular graph, with the stated number of vertices, when $k\\leq n$.
\\end{revremark}
""")

# -------------------------------------------------------------- section and subsection orientation
sub("\\section{Cubic cases}\n\\label{sec:cubic-examples}\n",
    "\\section{Cubic cases}\n\\label{sec:cubic-examples}\n\nThis section treats connected cubic graphs with $6$, $8$, $10$ and $12$\n"
    "vertices. Each subsection lists the graphs with their invariants and\n"
    "harmonic morphism counts, and then works out harmonic quotients in a\nseries of examples.\n\n")
sub("\\section{Quartic cases}\n", "\\section{Quartic cases}\n\\label{sec:quartic-examples}\n\nThis section treats connected quartic graphs with $5$ to $12$ vertices.\n"
    "For $9$ or more vertices only a selection of the graphs is included.\n"
    "Each subsection lists the graphs and then works out harmonic quotients\nin a series of examples.\n\n")
sub("\\section{Quintic cases}\n", "\\section{Quintic cases}\n\\label{sec:quintic-examples}\n\nThis section treats connected quintic graphs with $6$, $8$ and $10$\n"
    "vertices. For $10$ vertices only a selection of the graphs is included.\n\n")

kind = None
out = []
lines = T.split('\n')
i = 0
selected = {('cubic', 12), ('quartic', 9), ('quartic', 10), ('quartic', 11), ('quartic', 12), ('quintic', 10)}
adj = {'cubic': 'cubic', 'quartic': 'quartic', 'quintic': 'quintic'}
while i < len(lines):
    ln = lines[i]
    out.append(ln)
    if ln.startswith('\\section{Cubic'): kind = 'cubic'
    elif ln.startswith('\\section{Quartic'): kind = 'quartic'
    elif ln.startswith('\\section{Quintic'): kind = 'quintic'
    m = re.match(r'\\subsection\{\$(\d+)\$ vertices\}', ln)
    if m and kind:
        n = int(m.group(1))
        while i + 1 < len(lines) and lines[i + 1].startswith('\\label'):
            i += 1; out.append(lines[i])
        which = 'a selection of the' if (kind, n) in selected else 'the'
        out.append('')
        out.append(f'This subsection describes {which} connected {adj[kind]} graphs on ${n}$ vertices.')
        out.append('It records their invariants and harmonic morphism counts, and then')
        out.append('works out harmonic quotient morphisms in examples.')
        out.append('')
    if ln.startswith('\\subsubsection{Examples}'):
        while i + 1 < len(lines) and lines[i + 1].startswith('\\label'):
            i += 1; out.append(lines[i])
        out.append('')
        out.append('Each example below takes one graph from the list above and describes')
        out.append('its harmonic quotient morphisms.')
        out.append('')
    i += 1
T = '\n'.join(out)

rsub(r'\\subsection\{\$(\d+)\$ vertices\}', r'\\subsection{\\texorpdfstring{$\1$}{\1} vertices}')
sub("""The quotient morphism $\\phi:\\Gamma_2\\to \\Gamma_1=P_3$ 
associated to the subgroup $G = \\langle (0,2)(3,9)(4,8)(5,7), (0,5)(1,6)(2,7)(3,8)(4,9) \\rangle$
is tabulated below. 
$\\phi:\\Gamma_2\\to \\Gamma_1$.
""", """The quotient morphism $\\phi:\\Gamma_2\\to \\Gamma_1=P_3$
associated to the subgroup
\\[
G = \\langle (0,2)(3,9)(4,8)(5,7), (0,5)(1,6)(2,7)(3,8)(4,9) \\rangle
\\]
is tabulated below.
""")

# -------------------------------------------------------------- label every example
def add_label(m):
    name, rest = m.group(1), m.group(2)
    if f'\\label{{example:{name}}}' in rest[:300]:
        return m.group(0)
    return m.group(0).replace(m.group(1) + m.group(2), name + m.group(2), 1) if False else \
        f'\\begin{{example}}% {name}\n\\label{{example:{name}}}' + rest
rsub(r'\\begin\{example\}%\s*(\w+)(.{0,0})', lambda m: m.group(0), re.S)  # no-op probe
new = []
pos = 0
for m in re.finditer(r'\\begin\{example\}%\s*(\w+)\n', T):
    name = m.group(1)
    new.append(T[pos:m.end()])
    if f'\\label{{example:{name}}}' not in T[m.end():m.end() + 400]:
        new.append(f'\\label{{example:{name}}}\n')
    pos = m.end()
new.append(T[pos:])
T = ''.join(new)

# -------------------------------------------------------------- operators
rsub(r'(?<![\\A-Za-z])Aut\(', r'\\Aut(')
rsub(r'\{\\rm genus\}', r'\\genus')
rsub(r'(?<![\\A-Za-z])deg\(\\phi\)', r'\\deg(\\phi)')
rsub(r'(?<![\\A-Za-z])Barbell\(', r'\\mathrm{Barbell}(')

# -------------------------------------------------------------- citations
sub('\\cite{graph6}', '\\cite{Mc26}', T.count('\\cite{graph6}'))
sub('\\cite{ISGCI}', '\\cite{dR26}', T.count('\\cite{ISGCI}'))
sub('\\cite{Me17}', '\\cite{MM19}', T.count('\\cite{Me17}'))
n38 = T.count('by \\S 3.8 of \\cite{MJ22}')
sub('by \\S 3.8 of \\cite{MJ22}', 'by Lemma~\\ref{lemma:diameter}', n38)

# -------------------------------------------------------------- semicolons introduced in Draft 1
sub("(the cube and the Wagner graph) are vertex transitive; only the cube is",
    "(the cube and the Wagner graph) are vertex transitive. Only the cube is")
sub("(The other harmonic quotient is for $G=\\Aut(\\Gamma_2)$, of order $4$; it is a",
    "(The other harmonic quotient is for $G=\\Aut(\\Gamma_2)$, of order $4$. It is a")
sub("$2$ distinct morphisms) or to $P_2$ ($13$ groups, one of them $\\Aut(\\Gamma_2)$;",
    "$2$ distinct morphisms) or to $P_2$ ($13$ groups, one of them $\\Aut(\\Gamma_2)$,")
sub("$G=\\Aut(\\Gamma_2)$, of order $4$; it is a quotient to $P_3$, with fibers",
    "$G=\\Aut(\\Gamma_2)$, of order $4$. It is a quotient to $P_3$, with fibers")
sub("for some $G$, where $\\Gamma_1=K_{2,3}$; both subgroups",
    "for some $G$, where $\\Gamma_1=K_{2,3}$. Both subgroups")
sub("The remaining $13$ (one of them for $G=\\Aut(\\Gamma_2)$; all give the same morphism) are",
    "The remaining $13$ (one of them for $G=\\Aut(\\Gamma_2)$, all giving the same morphism) are")
sub("$G=\\Aut(\\Gamma_2)=\\langle (0,5)(1,6)(2,8)(3,4)\\rangle$; the quotient",
    "$G=\\Aut(\\Gamma_2)=\\langle (0,5)(1,6)(2,8)(3,4)\\rangle$. The quotient")
sub("same morphism); the others are $120$ quotients to $C_4$ with two pendant",
    "same morphism). The others are $120$ quotients to $C_4$ with two pendant")
sub("subgroup\\footnote{Here $\\Aut(\\Gamma_2)$ has trivial center; $G$ is a cyclic",
    "subgroup\\footnote{Here $\\Aut(\\Gamma_2)$ has trivial center. The group $G$ is a cyclic")
sub("$G=\\Aut(\\Gamma_2)=\\langle (0,5)(1,6)(2,7)(3,8)(4,9)\\rangle$.\nIt is a degree two quasicover",
    "$G=\\Aut(\\Gamma_2)=\\langle (0,5)(1,6)(2,7)(3,8)(4,9)\\rangle$.\nIt is a degree two quasicover")

# -------------------------------------------------------------- matchstick claims, X37, weed
sub("""This is a matchstick graph.
% (see Example \\ref{example:cubic-matchstick}).""",
"""This is a matchstick graph (see Remark~\\ref{rem:matchstick}).""")
sub("""Note all three of these graphs (namely, $\\Gamma_2$, $K_4$, and the diamond graph)
are matchstick graphs.""",
"""Note that the diamond graph is a matchstick graph. The graph $K_4$ is not,
since the plane contains no four points at mutual distance $1$.

\\begin{revremark}
\\label{rem:matchstick}
The statements that {\\tt d3reg8a} (this example) and
{\\tt d4reg12e} (Example~\\ref{example:d4reg12e}) are matchstick graphs were
not verified in 2026. Both graphs are planar, which is necessary. The
$3$-sun $S_3$ of Example~\\ref{example:d4reg9a} is a matchstick graph. Draw
a unit equilateral triangle and attach a unit equilateral triangle to each
of its sides.
\\end{revremark}""")
sub("This example, which is a matchstick graph,\n",
    "This example, which is a matchstick graph (see Remark~\\ref{rem:matchstick}),\n")
sub("the $X_{37}$ graph\\footnote{This quotient graph is isomorphic to the twin-$C_5$ graph below, so the six quotients described in this and the next paragraph all have the same isomorphism type.}.\n",
    "the $X_{37}$ graph (see Remark~\\ref{rem:x37}).\n")
# place the X37 remark after the figure that follows
k = T.index('the $X_{37}$ graph (see Remark~\\ref{rem:x37}).')
f = T.index('\\end{figure}', k) + len('\\end{figure}')
T = T[:f] + """

\\begin{revremark}
\\label{rem:x37}
The ISGCI name $X_{37}$ was not checked in 2026. The quotient graph of this
paragraph is isomorphic to the twin-$C_5$ graph of the next paragraph. So
the six quotients described in the two paragraphs all have the same
isomorphism type.
\\end{revremark}
""" + T[f:]
sub("""(where the horizontal multiplicity, as a function of the
  vertices of $\\Gamma$, is the constant $1$). One of these has a weed
  with $6$ roots.}""", """(where the horizontal multiplicity, as a function of the
  vertices of $\\Gamma$, is the constant $1$). One of these has a weed
  with $6$ roots (see Remark~\\ref{rem:weed}).}""")
sub("yielding a weed with three roots.}", "yielding a weed with three roots (see Remark~\\ref{rem:weed}).}")
# weed remark: after the enumerate that holds the d3reg12h item
k = T.index('weed\n  with $6$ roots (see Remark~\\ref{rem:weed})')
f = T.index('\\end{enumerate}', k) + len('\\end{enumerate}')
T = T[:f] + """

\\begin{revremark}
\\label{rem:weed}
The term ``weed'' (with a number of ``roots'') comes from \\cite{MJ22} and is
not defined in this paper. The two statements that use it were not
verified in 2026.
\\end{revremark}
""" + T[f:]

# -------------------------------------------------------------- small typos
sub("There are are $85$", "There are $85$")
sub("it's automorphism group is much larger", "its automorphism group is much larger")

# -------------------------------------------------------------- back matter and bibliography
a = T.index('\\begin{thebibliography}')
b = T.index('\\end{thebibliography}') + len('\\end{thebibliography}')
T = T[:a] + open(D2 + 'back.tex').read() + '\n' + open(D2 + 'biblio.tex').read() + T[b:]

open(OUT, 'w').write(T)
print(len(log), 'edits;', 'transcript chars', len(transcript))
