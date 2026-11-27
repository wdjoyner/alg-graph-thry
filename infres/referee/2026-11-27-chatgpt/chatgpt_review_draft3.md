I agree with all four suggestions. Having looked at the attached Draft 3 of `infres.tex`, I think these changes would substantially improve its readability and, more importantly, give the paper a stronger mathematical narrative.

The present draft has three complementary perspectives:

- **Algebraic:** group extensions, non-abelian cohomology, centralizers, and obstruction theory.
- **Geometric and combinatorial:** Cayley graphs, voltage graphs, relation modules, monodromy, and gain functions.
- **Arithmetic:** relative Weil groups and Langlands parameters.

At present, the geometric perspective arrives relatively late, in Section 7, after most of the principal algebraic results have been established. Given that voltage graphs appear in the title, I would introduce this perspective much earlier and develop it alongside the algebraic perspective.

## **1. Move the literature review into the Introduction**

I agree. I would retain both existing subdivisions of the literature review:

- Sources earlier than the original manuscript.
- Later sources.

These would become subsubsections of the Introduction's literature review subsection.

I would also organize the discussion, where appropriate, around the three mathematical perspectives identified above. This would help readers distinguish classical non-abelian obstruction theory from its graph-theoretic formulation and its arithmetic applications.

The paper's explicit statement that it is expository and makes no claim of originality should be preserved.

## **2. Move the notation subsection into the Introduction**

The current draft already contains a fairly comprehensive notation table in Section 3. It would be straightforward to relocate this to the Introduction.

However, I would expand the notation subsection beyond a table of symbols. In particular, I would precede the table with several paragraphs explaining the fundamental objects and their relationships:

\\[ 1\longrightarrow N \xrightarrow{i} W \xrightarrow{p}\Gamma \longrightarrow 1. \\]

Here:

| Symbol                 | Interpretation                                                                           |
| ---------------------- | ---------------------------------------------------------------------------------------- |
| \\(W\\)                | The group extension under investigation                                                  |
| \\(N\\)                | The normal subgroup of \\(W\\) forming the kernel of \\(p\\)                             |
| \\(\Gamma\\)           | The quotient group \\(W/N\\)                                                             |
| \\(A\\)                | The coefficient group, equipped with a \\(\Gamma\\)-action                               |
| \\(\phi\\)             | A homomorphism from \\(N\\) to \\(A\\) that one wishes to extend to a cocycle on \\(W\\) |
| \\(C\_\phi\\)          | The centralizer in \\(A\\) of the image of \\(\phi\\)                                    |
| \\(\mathcal O\_\phi\\) | The canonical obstruction extension                                                      |

I would also explicitly distinguish the use of \\(W\\) as an abstract group extension from its particular arithmetic realization as a relative Weil group.

This is especially important for graph theorists reading the paper who may not be familiar with local class field theory.

## **3. Move part of the graph theory material earlier**

I particularly like this suggestion. However, I would split the current Section 7 into two sections rather than move it in its entirety.

### **Early section: Group extensions and their associated graphs**

Place this immediately before the current inflation-restriction section. It would contain:

- Cayley digraphs and quotient graphs.
- Voltage assignments and derived graphs.
- Reconstruction of group extensions from monodromy.
- Relation modules and the homology of Cayley graphs.
- Changes of section and changes of lifts.
- Harmonic morphisms associated with group extensions.
- The algebra–graph theory dictionary.

These topics concern the structure of the extension \\(W\\) itself and do not require the main centralizer obstruction theorem.

### **Later section: A graph-theoretic formulation of the obstruction**

Retain the material that depends on the non-abelian cohomology results:

- Transporters and gain functions.
- Gains with prescribed holonomy.
- The graph-theoretic extension criterion.
- Twisted norm equations for cyclic groups.
- Examples involving simultaneous relator conditions.

I would also split the running graph example accordingly, introducing its voltage graph early and returning to it later when discussing gains and holonomy.

This would allow the reader to understand the geometry before encountering the cohomological obstruction, and ultimately see why the two formulations are equivalent.

## **4. Substantially expand the summary of results**

I think this is the most important expository change. The current summary is accurate and concise, but reads more like a catalogue of theorems than a synthesis of the mathematics.

I would expand it into several descriptive subsections, addressing the following topics.

### **4.1. The relationship between&#x20;**\\(W\\)**&#x20;and&#x20;**\\(\Gamma\\)

The group \\(W\\) is an extension of \\(\Gamma\\) by \\(N\\). As a set, after choosing a section, it can be identified with \\(N\times\Gamma\\). Its group structure, however, contains more information than this Cartesian product.

For abelian \\(N\\), that additional information consists of the action of \\(\Gamma\\) on \\(N\\) and a factor set

\\[ \sigma:\Gamma\times\Gamma\longrightarrow N. \\]

The multiplication is given by

\\[ (x,g)(y,h) = \bigl(x\\,{}^gy\\,\sigma(g,h),gh\bigr). \\]

Geometrically, the quotient homomorphism \\(p:W\to\Gamma\\) induces a covering of Cayley digraphs.

Conceptual schematic of the covering. Each vertex downstairs corresponds to an entire N-fiber upstairs. Only selected edges and vertices are shown.

Each vertex \\(g\in\Gamma\\) corresponds to the fiber

\\[ p^{-1}(g)=Ns(g). \\]

The factor set describes how edges connect these fibers. Closed walks in the base graph need not lift to closed walks upstairs. Their failure to close is measured by an element of \\(N\\), namely their net voltage.

This provides a very concrete geometric interpretation of the group extension.

An important qualification already present in the manuscript should be emphasized: the unlabeled covering graph alone does not determine \\(W\\). One needs the monodromy together with the \\(\Gamma\\)-module structure of \\(N\\).

Also, the chosen lifts of the generators of \\(\Gamma\\) need not generate \\(W\\), so the covering graph is not necessarily connected.

### **4.2. Three descriptions of a group extension**

One of the most attractive features of this paper is that it provides three equivalent descriptions of an extension with abelian kernel:

**Group extension**

\\(\displaystyle 1\to N\to W\to\Gamma\to1\\)

**Cohomological description**

\\(\displaystyle [\sigma]\in H^2(\Gamma,N)\\)

Factor sets modulo coboundaries

**Graph-theoretic description**

\\(\displaystyle \nu:H_1(X,\mathbb Z)\to N\\)

Equivariant monodromy modulo changes of generator lifts

Here the Γ-module N is fixed and X is the Cayley graph of Γ for a chosen generating set.

The manuscript already proves the particularly attractive formula

\\[ H^2(\Gamma,N)\cong \frac{ \operatorname{Hom}\_\Gamma(H_1(X,\mathbb Z),N) }{ \operatorname{im}(\operatorname{res}) }, \\]

where

\\[ X=\operatorname{Cay}(\Gamma,\overline S) \\]

and the denominator consists of restrictions of equivariant homomorphisms from the edge module.

I would give this formula much greater prominence in both the Introduction and the summary.

It establishes a direct relationship between group cohomology and the integral cycle structure of a graph. This is a particularly appealing result for readers coming from algebraic graph theory.

### **4.3. The obstruction to extending a homomorphism**

Given a homomorphism

\\[ \phi:N\longrightarrow A, \\]

the main problem of the paper is to determine whether there exists a cocycle

\\[ f:W\longrightarrow A \\]

such that \\(f|\_N=\phi\\).

I would explain that there are two successive requirements:

First, the conjugacy class of \\(\phi\\) must be invariant under \\(\Gamma\\). This is a compatibility condition between the action of \\(\Gamma\\) on \\(N\\) and its action on \\(A\\).

Second, the corresponding transporter elements must satisfy compatibility conditions reflecting the multiplication in \\(W\\).

The centralizer

\\[ C\_\phi=\operatorname{Cent}\_A(\phi(N)) \\]

measures the freedom in choosing these transporter elements. Consequently, it is the natural coefficient group for the obstruction.

The obstruction class

\\[ \partial\phi\in H^2(\Gamma,C\_\phi,\kappa\_\phi) \\]

is neutral precisely when the desired extension exists.

The summary should emphasize that this is not simply a technical modification of classical inflation-restriction theory. Replacing \\(A\\) by the centralizer is mathematically essential.

### **4.4. The geometric interpretation of the obstruction**

The graph-theoretic version of the main theorem is arguably the most intuitive formulation in the paper.

For each defining relator \\(r\\) of \\(\Gamma\\), there are two quantities:

| Quantity                | Meaning                                         |
| ----------------------- | ----------------------------------------------- |
| \\(\nu(r)\in N\\)       | Net voltage determined by the extension \\(W\\) |
| \\(\phi(\nu(r))\in A\\) | Prescribed holonomy                             |
| \\(\theta_c(r)\in A\\)  | Actual holonomy determined by the chosen gains  |

The extension criterion is the equality

\\[ \boxed{\theta_c(r)=\phi(\nu(r))} \\]

for every defining relator, with the generator gains chosen from the appropriate transporters.

In other words, the problem of extending a homomorphism from \\(N\\) to a cocycle on \\(W\\) becomes a problem of labeling the edges of a graph subject to prescribed holonomy constraints.

This gives an alternative conceptual route to the main theorem, as well as a potentially useful computational formulation when \\(\Gamma\\) is finitely presented.

### **4.5. A worked arithmetic interpretation**

I would repeat a small portion of the running example in the summary because it illustrates nearly every major result of the paper.

For

\\[ E=\mathbb Q_3(i),\qquad F=\mathbb Q_3, \\]

the Galois group is \\(C_2\\), whereas its relative Weil group satisfies

\\[ 1\to E^\times\to W\_{E/F}\to C_2\to1. \\]

A lift \\(s\\) of the nontrivial Galois automorphism satisfies \\(s^2=3\\).

The closed walk downstairs lifts to a walk from 1 to 3 upstairs. Its monodromy is 3.

The defining relation downstairs is \\(\tau^2=1\\), but its lift upstairs satisfies \\(s^2=3\\). Thus the extension criterion is

\\[ c\\,{}^\tau c=\phi(3). \\]

For the trivial coefficient action on \\(\mathrm{SL}\_2(\mathbb C)\\) and the regular diagonal homomorphisms considered in the paper, this reduces to

\\[ c^2=-I=\phi(3). \\]

This example unifies the algebraic, geometric, and arithmetic perspectives in a particularly economical way.

## **5. Proposed revised table of contents**

I would recommend the following structure for Draft 4.

**1. Introduction**

1.1 Setting and motivation

1.2 Notation and conventions

1.3 A first example

1.4 Overview of the main results

1.5 Standing assumptions and scope

1.6 Literature review

1.7 What is proved here and what is cited

1.8 Organization

**2. Algebraic background**

2.1 Extensions and factor sets

2.2 The relative Weil group

2.3 Non-abelian first cohomology

2.4 Springer's non-abelian second cohomology

2.5 Running example: the relative Weil group

**3. Group extensions and their associated graphs**

3.1 Cayley graphs, voltage graphs, and derived graphs

3.2 Coverings and reconstruction of extensions

3.3 Relation modules and graph homology

3.4 Monodromy and changes of lifts

3.5 Harmonic morphisms and the algebra–geometry dictionary

3.6 Running example: the Weil group covering

**4. Inflation and restriction**

**5. The obstruction to extending a homomorphism**

**6. Extensions with non-abelian kernel**

**7. A graph-theoretic formulation of the obstruction**

7.1 Transporters and gain functions

7.2 Gains with prescribed holonomy

7.3 Cyclic quotients and twisted norm equations

7.4 Non-cyclic quotients and simultaneous constraints

7.5 Running example: gains on the Weil group covering

**8. Topology and Langlands parameters**

**9. Summary of results and open questions**

9.1 The relationship between W and Γ

9.2 Algebraic, cohomological, and geometric descriptions

9.3 Inflation, restriction, and the centralizer obstruction

9.4 Holonomy and the extension problem

9.5 Arithmetic interpretation and applications

9.6 Open questions

**Glossary**

**Acknowledgments**

**References**

A useful incidental benefit of this organization is that Sections 4–9 retain their present section numbers, although individual theorem and example numbers would change.

## **6. Additional improvements I would recommend**

There are a few further opportunities that fit naturally into this revision:

- **Distinguish the two kinds of obstructions.** The obstruction to splitting \\(W\\) and the obstruction to extending \\(\phi\\) are related but distinct. A nonsplit \\(W\\) can admit extensions of particular homomorphisms \\(\phi\\).
- **Emphasize the abelian-kernel hypothesis.** The centralizer obstruction theorem works for arbitrary normal subgroups, whereas the relation-module and first-homology formulation presented here assumes an abelian kernel.
- **Add more TikZ diagrams.** In particular, illustrate quotient fibers, lifting closed walks, voltage switching, and the distinction between split and nonsplit extensions.
- **Develop the&#x20;**\\(D_4\\)**&#x20;and&#x20;**\\(Q_8\\)**&#x20;examples early.** These provide accessible finite-group illustrations of the extension theory before the reader encounters the arithmetic examples.
- **Expand the discussion of harmonic morphisms.** Explain why unique path lifting is essential to the present monodromy construction and why extending the theory to more general harmonic morphisms is a natural open problem.

## **Overall assessment**

I would make all four proposed changes for Draft 4.

I would not simply move sections around, however. I would use the reorganization to make the geometry a central organizing principle of the exposition:

\\[ \boxed{ \begin{gathered} \text{Group extensions}\\\ \updownarrow\\\ \text{Voltage graphs and monodromy}\\\ \updownarrow\\\ \text{Cohomology and obstruction theory}\\\ \updownarrow\\\ \text{Gain graphs and prescribed holonomy} \end{gathered} } \\]

This would make the paper more accessible to algebraic graph theorists, representation theorists, and researchers interested in local Langlands parameters.

The mathematical material needed for this reorganization is largely already present in Draft 3. Most of the work would be expository: restructuring sections, resolving dependencies, expanding explanations, and adding diagrams, rather than proving new theorems.