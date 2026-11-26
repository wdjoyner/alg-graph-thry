# **Referee report**

**Manuscript:** *Notes on the inflation-restriction sequence in non-abelian cohomology*\
**Author:** David Joyner\
**Version:** Draft 1, corrected and expanded version, November 26, 2026\
**Source:** [infres.tex](https://github.com/wdjoyner/alg-graph-thry/blob/main/infres/infres.tex?utm_source=chatgpt.com)\
**Recommendation:** Minor to moderate revision

## **1. Overall assessment**

This is a worthwhile mathematical paper. It brings together three subjects that are not ordinarily presented together:

- Non-abelian cohomology and the inflation-restriction sequence.
- Relative Weil groups and the construction of Langlands parameters.
- Voltage graphs, gain graphs and their holonomy.

The central mathematical result — that the obstruction to extending a homomorphism \\(\phi:N\to A\\) belongs to the non-abelian second cohomology of the centralizer \\(C\_\phi\\), rather than that of the ambient coefficient group \\(A\\) — is correct.

The description of the fibers of restriction by twisted non-abelian \\(H^1\\) is also correct. The graph-theoretic reformulation is mathematically substantive, rather than simply a graphical illustration of the preceding results.

I particularly like the progression from the dihedral and quaternion groups to the norm-one torus and the dihedral parameters in \\(\mathrm{SL}\_2(\mathbb C)\\). These examples help explain why the obstruction theory is necessary.

**I found no fundamental error in the principal theorems.** However, there are several mathematical qualifications, one incorrect assertion in the graph-theoretic discussion, and some opportunities to strengthen both the mathematical content and readability.

The revision is worth pursuing. I would not recommend a wholesale rewrite.

## **2. Mathematical correctness: summary**

| Result or topic                                              | Assessment                          |
| ------------------------------------------------------------ | ----------------------------------- |
| Factor sets and extension classes                            | Correct                             |
| Non-abelian inflation-restriction                            | Correct                             |
| Invariant conjugacy classes versus equivariant homomorphisms | Correct                             |
| Centralizer obstruction class                                | Correct                             |
| Independence of choices                                      | Correct                             |
| Neutrality criterion                                         | Correct                             |
| Fibers of restriction                                        | Correct                             |
| Norm-one torus example                                       | Correct, with a minor wording issue |
| Dihedral Langlands parameters                                | Correct                             |
| Necessity of the centralizer                                 | Correct                             |
| Derived graph construction                                   | Correct                             |
| Reconstruction of the extension from the covering            | Requires qualification              |
| Holonomy criterion                                           | Correct                             |
| Cyclic twisted norm equation                                 | Correct                             |
| Harmonic morphism interpretation                             | Requires qualification              |
| Continuous cohomology                                        | Correct under stated conventions    |
| Langlands parameter interpretation                           | Requires minor qualifications       |

## **3. Mathematical issues requiring revision**

### **M1. Clarify the reconstruction of the extension from the graph covering**

**Location:** Section 5.1, immediately after Proposition `prop:derived`.

The manuscript states that the extension \\(W\\) is encoded by the covering

\\[ \operatorname{Cay}(W,S) \longrightarrow \operatorname{Cay}(\Gamma,\overline S). \\]

This is too strong without specifying the additional structure retained on the covering.

An ordinary graph covering need not determine the group extension. The generator labels, the identification of the voltage group with \\(N\\), and the action of \\(\Gamma\\) on \\(N\\) are important.

Moreover, the covering may be disconnected because the chosen lifts of the generators of \\(\Gamma\\) need not generate \\(W\\).

The precise algebraic reconstruction is particularly attractive. Let

\\[ \mathcal F=\langle\overline S\rangle\_{\mathrm{free}}, \qquad \mathcal R=\ker(\mathcal F\to\Gamma). \\]

Given the \\(\Gamma\\)-module \\(N\\) and the equivariant homomorphism

\\[ \nu:\mathcal R\longrightarrow N, \\]

one can reconstruct the extension as

\\[ W\cong \frac{N\rtimes\mathcal F} {\\{(\nu(r)^{-1},r):r\in\mathcal R\\}}, \\]

where the action of \\(\mathcal F\\) on \\(N\\) factors through \\(\Gamma\\).

Indeed, the map

\\[ N\rtimes\mathcal F\longrightarrow W, \qquad (x,v)\longmapsto x\lambda_W(v) \\]

is a surjective homomorphism with precisely the indicated kernel.

**Recommendation:** Replace the informal reconstruction assertion with a proposition giving this explicit quotient construction. This would strengthen the graph-theoretic portion of the paper and establish exactly what information is required to recover the extension.

### **M2. The norm-one torus example understates injectivity**

**Location:** Example `ex:torus1`.

The manuscript states:

> so \\(\mathrm{res}\\) is injective on the fiber of the base point.

This formulation is awkward. Restriction is constant on a fiber, and exactness implies that the fiber over the base point is a singleton.

Furthermore, because the coefficient group in this example is abelian, restriction is a group homomorphism with trivial kernel. Consequently, it is injective on its entire domain.

Replace the sentence by:

> Since \\(\widehat T\\) is abelian, the inflation-restriction sequence is a sequence of abelian groups. The equality \\(H^1(\Gamma,\widehat T)=1\\) therefore implies that the restriction map is injective.

The subsequent computation of its image is correct.

### **M3. An implicit hypothesis in the central-homomorphism corollary**

**Location:** Corollary `cor:central`, part (ii).

The corollary assumes that

\\[ \phi(N)\subseteq Z(A). \\]

Part (ii) then characterizes extendibility by the equation

\\[ c(g)\\,{}^gc(h)c(gh)^{-1} =\phi(\sigma(g,h)). \\]

Strictly speaking, one also needs the equivariance of \\(\phi\\).

For a central homomorphism, the transporter condition is equivalent to

\\[ {}^g\phi(x)=\phi({}^gx). \\]

The displayed factor-set equation alone does not imply this condition.

For example, take a split extension, so that \\(\sigma=1\\). The choice \\(c=1\\) satisfies the factor-set equation regardless of whether \\(\phi\\) is equivariant.

A concrete counterexample is

\\[ W=S_3,\qquad N=C_3,\qquad \Gamma=C_2,\qquad A=C_3, \\]

where \\(\Gamma\\) acts trivially on \\(A\\), but acts by inversion on \\(N\\).

The identity homomorphism \\(\phi:C_3\to C_3\\) is central but not equivariant. It cannot extend to \\(S_3\\), although \\(c=1\\) satisfies the displayed equation.

**Recommendation:** Begin part (ii) with:

> Suppose, in addition, that \\(\phi\\) is \\(\Gamma\\)-equivariant.

This is a genuine, but easily repairable, omission in the statement.

### **M4. Specify the category of graphs in the harmonic morphism remark**

**Location:** Remark `rem:harmonic`.

The manuscript allows directed graphs with loops and multiple edges. Forgetting orientations can produce undirected multigraphs with loops.

The theory of harmonic morphisms in the cited Baker–Norine framework is formulated for finite graphs without loops, though multiple edges are permitted.

The assertion that a covering is harmonic is essentially correct, but the reference does not automatically cover the full generality of the graphs used here.

There are three possible repairs:

- Restrict the remark to finite, loopless graphs.
- Explicitly extend the definition of harmonic morphism to locally finite multigraphs with loops, using incidences or half-edges.
- Work in the category of directed graphs and define harmonicity separately for incoming and outgoing edges.

I favor the second approach because the paper uses potentially infinite coefficient and kernel groups.

This is a useful opportunity to clarify how the graph-theoretic results relate to your broader work on harmonic morphisms.

### **M5. Distinguish abstract extension cohomology from Galois cohomology**

**Location:** Sections 2.4 and 6.

The definition of Springer's non-abelian \\(H^2\\) given in the manuscript is appropriate for abstract groups and their extension theory.

Nevertheless, Springer's theory in Galois cohomology includes additional algebraic and topological structure. A reader familiar with Galois cohomology may wonder whether the paper is working with algebraic kernels, continuous kernels, or abstract outer actions.

I suggest adding a paragraph such as:

> Throughout this note, non-abelian \\(H^2\\) is used in its abstract group-extension interpretation. A kernel is a homomorphism into the outer automorphism group of the coefficient group. In the applications to relative Weil groups, the quotient group \\(\Gamma\\) is finite and discrete, so continuity of the cochains on \\(\Gamma\\) introduces no additional restrictions.

The distinction is terminological and conceptual, rather than a defect in the obstruction theorem.

### **M6. Refine the introductory statement about dual-group actions**

**Location:** Section 1.1.

The statement that the action on the dual group is trivial exactly when \\(G\\) is an inner form of a split group should explicitly refer to the standard pinned action used in the construction of the \\(L\\)-group.

The action is determined by the Galois action on the based root datum, rather than by an arbitrary choice of action on \\(\widehat G\\).

This can be fixed by introducing the pinned action in the background section and referring to it consistently thereafter.

## **4. Verification of the principal obstruction theorem**

The most important result in the paper is Theorem `thm:main`. I checked the algebra underlying its five equivalent conditions.

Let

\\[ 1\longrightarrow N\longrightarrow W \longrightarrow\Gamma\longrightarrow1 \\]

be the extension and \\(A\\) a \\(\Gamma\\)-group. Given a homomorphism \\(\phi:N\to A\\) with invariant conjugacy class, write

\\[ C\_\phi=Z_A(\phi(N)). \\]

For \\(g\in\Gamma\\), the transporter is

\\[ T\_\phi(g)= \left\\{ b\in A: b\\,{}^g\phi(x)b^{-1} =\phi({}^gx) \right\\}, \\]

where the defining identity is required for every \\(x\in N\\).

The corresponding stabilizer extension is

\\[ 1\longrightarrow C\_\phi \longrightarrow E\_\phi \longrightarrow\Gamma \longrightarrow1. \\]

The central extension-morphism problem of Section 4.

The key observation is

\\[ \phi(N)\subseteq Z(C\_\phi). \\]

Because \\(N\\) is abelian, this inclusion holds. It permits the factor set of \\(W\\) to be transported into the center of the centralizer.

Choosing transporter representatives \\(b(g)\\), the manuscript defines

\\[ \beta_b(g)=\operatorname{Int}(b(g))\circ\alpha(g) \big|\_{C\_\phi} \\]

and

\\[ u_b(g,h)=b(g)\\,{}^gb(h)b(gh)^{-1}. \\]

The proposed obstruction is

\\[ \partial\phi= \left[ u_b(\phi\circ\sigma)^{-1},\beta_b \right]. \\]

All the essential steps are correct:

- The pair \\((u_b,\beta_b)\\) represents the stabilizer extension.
- The image of the factor set is a central \\(2\\)-cocycle.
- Multiplication by its inverse produces another legitimate non-abelian \\(2\\)-cocycle.
- Changing the section or the transporter representatives changes the representative but not its class.
- Neutrality is equivalent to the existence of the desired \\(1\\)-cocycle.

The sign and inverse conventions are consistent.

**Verdict:** The main obstruction theorem should be retained. No correction to its central formula is necessary.

## **5. A potentially stronger formulation of the main theorem**

I recommend adding a choice-free construction of the obstruction extension itself.

At present, the paper constructs the obstruction using sections, factor sets and transporter representatives. This is perfectly valid, but there is a more geometric construction that fits the philosophy of the revised manuscript.

Form the fiber product

\\[ P\_\phi=W\times\_\Gamma E\_\phi. \\]

Its elements are pairs \\((w,e)\\) with the same image in \\(\Gamma\\).

Inside \\(P\_\phi\\), consider

\\[ D\_\phi= \left\\{ (x,(\phi(x),1)):x\in N \right\\}. \\]

The transporter identity implies that \\(D\_\phi\\) is normal in \\(P\_\phi\\).

Define

\\[ \mathcal O\_\phi=P\_\phi/D\_\phi. \\]

There is an exact sequence

\\[ 1\longrightarrow C\_\phi \longrightarrow\mathcal O\_\phi \longrightarrow\Gamma \longrightarrow1. \\]

Indeed, the kernel before taking the quotient is \\(N\times C\_\phi\\), and the quotient identifies \\((x,c)\\) with the centralizer element \\(c\phi(x)^{-1}\\).

Using the sections \\(s(g)\\) and \\((b(g),g)\\), the factor set of this quotient extension is precisely

\\[ u_b(g,h)\phi(\sigma(g,h))^{-1}. \\]

Consequently,

\\[ [\mathcal O\_\phi]=\partial\phi. \\]

The main theorem can therefore be reformulated as follows:

**Proposed theorem.** The following conditions are equivalent:

1. The homomorphism \\(\phi\\) extends to a \\(1\\)-cocycle of \\(W\\).
2. The obstruction class \\(\partial\phi\\) is neutral.
3. The canonical obstruction extension \\(\mathcal O\_\phi\\) splits.

A choice-free construction of the obstruction class using a fiber product and quotient.

This addition would have several advantages:

- It makes the independence of choices geometrically transparent.
- It provides a conceptual explanation for the inverse appearing in the obstruction formula.
- It makes the relationship with classical extension theory clearer.
- It suggests an answer to the first open question in Section 7.

I regard this as the most valuable possible mathematical addition to Draft 2.

## **6. The first open question may already be solvable**

**Location:** Question `q:nonab`.

The manuscript asks for the appropriate obstruction when \\(N\\) is no longer abelian.

I believe the question can be answered by a modification of the fiber-product construction above.

In fact, the hypothesis that \\(N\\) is abelian can be dropped by constructing a different stabilizer group.

For arbitrary normal \\(N\\), define

\\[ B\_\phi= \left\\{ (a,w)\in A\rtimes W: a\\,{}^{p(w)}\phi(x)a^{-1} =\phi(wxw^{-1}) \quad\forall x\in N \right\\}. \\]

Here the action of \\(W\\) on \\(A\\) still factors through \\(\Gamma\\).

Assume the conjugacy class of \\(\phi\\) is invariant under the induced action of \\(\Gamma\\) on \\(\operatorname{Hom}(N,A)/A\\).

Then the projection \\(B\_\phi\to W\\) is surjective, with kernel \\(C\_\phi\\).

The subgroup

\\[ D\_\phi=\\{(\phi(x),x):x\in N\\} \\]

is normal in \\(B\_\phi\\). Indeed, conjugating an element of \\(D\_\phi\\) by \\((a,w)\in B\_\phi\\) gives

\\[ (\phi(wxw^{-1}),wxw^{-1}), \\]

which again lies in \\(D\_\phi\\).

Taking the quotient gives

\\[ 1\longrightarrow C\_\phi \longrightarrow B\_\phi/D\_\phi \longrightarrow\Gamma \longrightarrow1. \\]

Notice that this construction does not require \\(\phi(N)\\) to be contained in \\(C\_\phi\\).

The resulting extension defines an obstruction class

\\[ \partial\_{\mathrm{gen}}\phi \in H^2(\Gamma,C\_\phi,\kappa\_\phi). \\]

A cocycle \\(f\\) extending \\(\phi\\) gives a homomorphic section

\\[ w\longmapsto(f(w),w) \\]

of \\(B\_\phi\to W\\). Modulo \\(D\_\phi\\), this induces a splitting of the obstruction extension.

Conversely, suppose the obstruction extension splits. Let \\(L\\) be the inverse image in \\(B\_\phi\\) of the image of a splitting

\\[ \Gamma\longrightarrow B\_\phi/D\_\phi. \\]

Then the projection

\\[ L\longrightarrow W \\]

is an isomorphism: it is surjective because its image contains \\(N\\) and maps onto \\(\Gamma\\), and it is injective because its kernel lies in \\(C\_\phi\\) and has trivial intersection with \\(L\\).

Its inverse has the form

\\[ w\longmapsto(f(w),w) \\]

for a cocycle \\(f\\) satisfying \\(f|\_N=\phi\\).

Thus one obtains the following generalization.

**Proposed general theorem.** Let \\(N\\) be an arbitrary normal subgroup of \\(W\\), with \\(\Gamma=W/N\\), and suppose that \\(A\\) is a \\(\Gamma\\)-group. A homomorphism \\(\phi:N\to A\\) with invariant conjugacy class extends to a \\(1\\)-cocycle of \\(W\\) if and only if the extension

\\[ 1\longrightarrow C\_\phi \longrightarrow B\_\phi/D\_\phi \longrightarrow\Gamma \longrightarrow1 \\]

splits.

This also recovers the abelian-kernel theorem: in that case \\(B\_\phi\\) identifies with the fiber product \\(W\times\_\Gamma E\_\phi\\).

I recommend developing this into a new section rather than leaving the generalization as an open question.

The argument is sufficiently short that it should not make the manuscript substantially longer. It also separates the genuinely necessary hypotheses from the special assumptions appropriate to relative Weil groups.

## **7. Assessment of the examples**

### **7.1. Dihedral and quaternion groups**

These are excellent examples.

For the extensions

\\[ 1\to C_4\to D_4\to C_2\to1 \\]

and

\\[ 1\to C_4\to Q_8\to C_2\to1, \\]

the choice \\(A=Q_8\\) and \\(\phi(\rho)=i\\) demonstrates several different phenomena simultaneously.

**Dihedral extension**

Four components, each a directed 2-cycle.\\(s^2=1\\)

Obstruction: −1. No extension.

**Quaternion extension**

Two components, each a directed 4-cycle.\\(s^2=\rho^2\\)

Obstruction: +1. Extension exists.

What is particularly interesting is that the split extension \\(D_4\\) produces a non-neutral obstruction, whereas the non-split extension \\(Q_8\\) produces a neutral obstruction.

This is initially counterintuitive and deserves explicit emphasis.

The obstruction is not simply measuring whether \\(W\\) splits. It measures the compatibility between the extension \\(W\\) and the stabilizer extension \\(E\_\phi\\).

### **7.2. Norm-one torus**

The computation is correct and provides a useful arithmetic application.

In particular, the distinction between

\\[ \chi|\_{\mathrm N\_{E/F}(E^\times)}=1 \\]

and

\\[ \chi|\_{F^\times}=1 \\]

is essential.

The first condition gives invariance; the second gives extendibility.

I suggest explicitly displaying the obstruction as a homomorphism

\\[ \partial: \operatorname{Hom}\bigl( E^\times/\mathrm N\_{E/F}(E^\times), \mathbb C^\times \bigr) \longrightarrow \\{\pm1\\}. \\]

This would make the relationship to the ordinary transgression particularly clear.

### **7.3. Dihedral parameters in&#x20;**\\(\mathrm{SL}\_2(\mathbb C)\\)

This is arguably the strongest arithmetic example in the paper.

The condition

\\[ \chi|\_{F^\times}=\omega\_{E/F} \\]

is correctly derived from the square of the Weyl representative

\\[ w_0= \begin{pmatrix} 0&1\\\ -1&0 \end{pmatrix}, \qquad w_0^2=-I. \\]

The comparison with \\(\mathrm{GL}\_2(\mathbb C)\\) is also correct.

In \\(\mathrm{GL}\_2\\), the off-diagonal entries can be independently adjusted, whereas in \\(\mathrm{SL}\_2\\), the determinant-one constraint forces the square of every relevant transporter representative to equal \\(-I\\).

This example illustrates how the obstruction detects structural properties of the dual group.

I recommend adding the familiar induced-representation determinant formula

\\[ \det\left(\operatorname{Ind}\_{W_E}^{W_F}\chi\right) = \omega\_{E/F}\\,\chi|\_{F^\times}, \\]

where characters are identified via local class field theory.

The formula provides an independent verification of the obstruction criterion.

### **7.4. Unramified extensions**

The argument using divisibility of complex maximal tori is correct.

There is room to go further, however. After establishing existence of a solution to

\\[ c^n=t^m, \\]

one could describe the conjugacy classes of solutions using the fiber theorem.

For regular semisimple \\(t\\), the centralizer is a maximal torus \\(T\\), and the twisted action in this split example is trivial. The fiber is therefore parametrized by

\\[ H^1(C_n,T) =\operatorname{Hom}(C_n,T) \cong T[n]. \\]

If \\(T\\) has rank \\(r\\), this gives

\\[ |T[n]|=n^r. \\]

This would be a short and informative additional computation.

## **8. Assessment of the graph-theoretic contribution**

Section 5 is the part of the paper I would most encourage developing further.

The voltage graph construction is correct, and the proof of the equivalence between the existence of an extending cocycle and the prescribed-holonomy condition is sound.

In particular, the reduction from all relations to a set of normally generating relators is justified by the transporter identity. That is an important point and is proved correctly.

### **8.1. Make the relation module more prominent**

The manuscript briefly observes that the monodromy homomorphism

\\[ \nu:\mathcal R\longrightarrow N \\]

factors through the abelianization

\\[ \mathcal R\_{\mathrm{ab}} =\mathcal R/[\mathcal R,\mathcal R]. \\]

There is a natural graph-theoretic interpretation:

\\[ \mathcal R\_{\mathrm{ab}} \cong H_1\bigl(\operatorname{Cay} (\Gamma,\overline S),\mathbb Z\bigr). \\]

Here the Cayley graph is considered as a one-dimensional CW complex, with generator labels and distinct oriented edge cells retained.

Indeed, it is the covering of the bouquet associated with the subgroup \\(\mathcal R\\) of the free group \\(\mathcal F\\). Its fundamental group is \\(\mathcal R\\).

This gives a direct relationship between:

| Group-theoretic object                          | Graph-theoretic object                      |
| ----------------------------------------------- | ------------------------------------------- |
| Free group \\(\mathcal F\\)                     | Fundamental group of the bouquet            |
| Relation subgroup \\(\mathcal R\\)              | Fundamental group of the Cayley graph       |
| Relation module \\(\mathcal R\_{\mathrm{ab}}\\) | Integral first homology of the Cayley graph |
| Map \\(\nu:\mathcal R\to N\\)                   | Voltage monodromy                           |
| Centralizer obstruction                         | Obstruction to prescribed gain holonomy     |
| Change of section                               | Voltage switching                           |

This dictionary deserves its own subsection.

### **8.2. Introduce the cellular chain sequence**

For a finite group \\(\Gamma\\) and a finite generating set \\(\overline S\\), the cellular chain groups of the Cayley graph give an exact sequence of \\(\mathbb Z[\Gamma]\\)-modules

\\[ 0\longrightarrow\mathcal R\_{\mathrm{ab}} \longrightarrow\mathbb Z[\Gamma]^{|\overline S|} \xrightarrow{\partial_1} \mathbb Z[\Gamma] \xrightarrow{\epsilon} \mathbb Z \longrightarrow0. \\]

The boundary map on a generator edge is

\\[ \partial_1(e\_{g,t})=gt-g. \\]

This connects the graph construction with the classical computation of group cohomology via dimension shifting.

For instance, the two short exact sequences obtained by introducing the augmentation ideal yield

\\[ H^2(\Gamma,N) \cong \frac{ \operatorname{Hom}\_\Gamma(\mathcal R\_{\mathrm{ab}},N) }{ \operatorname{im}\bigl( \operatorname{Hom}\_\Gamma( \mathbb Z[\Gamma]^{|\overline S|},N) \bigr) }, \\]

where the denominator denotes the restrictions to the relation module.

This is a concrete algebraic explanation of why the extension class can be expressed using voltage monodromy and why changing the lifts of generators changes its representative.

It would significantly strengthen the connection between graph theory and cohomology.

### **8.3. Add a noncyclic example**

Most of the detailed examples use \\(\Gamma=C_2\\), and the more general unramified example still has cyclic quotient.

Consequently, the reader never sees the full power of the simultaneous relator criterion.

I recommend adding an example with

\\[ \Gamma=C_2\times C_2 =\langle u,v\mid u^2=v^2=[u,v]=1\rangle. \\]

A particularly simple choice is the central extension

\\[ 1\longrightarrow\\{\pm1\\} \longrightarrow Q_8 \longrightarrow C_2\times C_2 \longrightarrow1. \\]

Generator-labeled Cayley digraph of the Klein four-group. Unlike the cyclic examples, the commutator relator imposes an additional compatibility condition.

Choose lifts \\(s_u=i\\) and \\(s_v=j\\). The three defining relators have voltages

\\[ \nu(u^2)=-1,\qquad \nu(v^2)=-1,\qquad \nu([u,v])=-1. \\]

For trivial action on \\(A\\), the holonomy criterion becomes

\\[ \begin{aligned} c(u)^2&=\phi(-1),\\\ c(v)^2&=\phi(-1),\\\ [c(u),c(v)]&=\phi(-1). \end{aligned} \\]

Taking \\(A=Q_8\\) and \\(\phi\\) to be the natural inclusion, one obtains the solution \\(c(u)=i,\ c(v)=j\\).

Taking \\(A=\mathbb C^\times\\) and \\(\phi(-1)=-1\\), the first two equations are individually solvable, but the third is impossible because \\(\mathbb C^\times\\) is abelian.

This demonstrates that satisfying the cyclic norm equations separately is insufficient. Compatibility around the commutator cycle matters.

I strongly recommend including this example.

### **8.4. Develop the connection to harmonic morphisms**

The final open question concerning harmonic morphisms that are not coverings is interesting and worth retaining.

The fundamental difficulty is that a covering admits unique path lifting, whereas a general harmonic morphism does not.

As a result, one cannot immediately associate a single monodromy element with each closed walk.

Possible directions include:

- Branched graph coverings and local ramification indices.
- Graphs of groups in the sense of Bass–Serre theory.
- Groupoid-valued voltage assignments.
- Gain functions whose holonomy is defined only up to a vertex stabilizer.

Of these, **graphs of groups** seem especially promising. They naturally accommodate the nontrivial stabilizers that occur when a group acts non-freely on a graph.

This could become the subject of a subsequent paper rather than an extensive addition to the present manuscript.

## **9. Readability and exposition**

The manuscript is considerably more readable than a typical specialized note on non-abelian cohomology. The background material, running examples, explicit proofs and glossary are all helpful.

Nevertheless, I recommend the following improvements.

| Priority | Proposed change                                                                  |
| -------- | -------------------------------------------------------------------------------- |
| High     | Introduce a commutative extension diagram before defining the obstruction class. |
| High     | Add a dedicated notation subsection near the beginning.                          |
| High     | Introduce the choice-free obstruction extension.                                 |
| High     | Explain the relation module using graph homology.                                |
| Medium   | Add the Klein four-group example.                                                |
| Medium   | Expand the related-literature discussion thematically.                           |
| Medium   | Expand the glossary entries.                                                     |
| Medium   | Distinguish graph coverings from general harmonic morphisms.                     |
| Low      | Modernize the LaTeX font package if desired.                                     |
| Low      | Standardize notation for dihedral groups, identities and conjugation.            |

### **9.1. Improve the motivation for the centralizer**

The introduction announces that the obstruction belongs to \\(H^2\\) of the centralizer. However, a reader encountering non-abelian cohomology for the first time may not immediately understand why.

I suggest inserting the following reasoning early in the introduction.

Suppose \\(f\\) and \\(f'\\) are two extensions of the same homomorphism \\(\phi\\). Their values at an element \\(w\\) both satisfy the same transporter identity. Therefore,

\\[ f'(w)f(w)^{-1}\in C\_\phi. \\]

Thus the centralizer measures the freedom in choosing an extension.

It is natural that:

- \\(H^2\\) of the centralizer measures the obstruction to existence.
- Twisted \\(H^1\\) of the centralizer measures the ambiguity of extensions.

This explanation prepares the reader for both of the major results.

### **9.2. Add a notation subsection**

The manuscript uses a substantial amount of notation. A consolidated table would be helpful.

| Symbol                 | Meaning                              |
| ---------------------- | ------------------------------------ |
| \\(N\\)                | Kernel of the extension              |
| \\(W\\)                | Extension group                      |
| \\(\Gamma\\)           | Quotient group                       |
| \\(A\\)                | Coefficient group                    |
| \\(\alpha\\)           | Action of \\(\Gamma\\) on \\(A\\)    |
| \\(s\\)                | Set-theoretic section                |
| \\(\sigma\\)           | Factor set                           |
| \\(\phi\\)             | Homomorphism from \\(N\\) to \\(A\\) |
| \\(T\_\phi(g)\\)       | Transporter over \\(g\\)             |
| \\(C\_\phi\\)          | Centralizer of \\(\phi(N)\\)         |
| \\(E\_\phi\\)          | Stabilizer extension                 |
| \\(\kappa\_\phi\\)     | Induced outer action                 |
| \\(\partial\phi\\)     | Obstruction class                    |
| \\(\mathcal O\_\phi\\) | Proposed obstruction extension       |
| \\(\mathcal F\\)       | Free group on quotient generators    |
| \\(\mathcal R\\)       | Relation subgroup                    |
| \\(\nu\\)              | Voltage monodromy                    |
| \\(\theta_c\\)         | Gain function                        |

This would be particularly helpful when reading Sections 4 and 5 independently.

### **9.3. Expand the glossary**

The existing glossary is substantial, but many entries are essentially definitions.

Consistent with your mathematical manuscript style guide, I would expand each entry by another sentence or two explaining its mathematical significance or relationship to another concept in the paper.

Additional glossary entries could include:

| Proposed entry         | Reason for inclusion                             |
| ---------------------- | ------------------------------------------------ |
| Augmentation ideal     | Connects graph chains with group cohomology      |
| Based root datum       | Explains the pinned Galois action                |
| Baer sum               | Explains the twisting of extension classes       |
| Class formation        | Provides context for relative Weil groups        |
| Fiber product          | Underlies the canonical obstruction construction |
| Graph homology         | Connects Cayley graphs to relation modules       |
| Holonomy               | Central concept in Section 5                     |
| Local reciprocity      | Underlies the Weil-group examples                |
| Monodromy              | Connects closed walks with extension data        |
| Outer automorphism     | Necessary for understanding kernels              |
| Pinned action          | Relevant to the dual-group action                |
| Relation module        | Connects group presentations with graph theory   |
| Switching equivalence  | Graph-theoretic analog of changing sections      |
| Twisted norm           | Important in the cyclic quotient case            |
| Twisting of cohomology | Explains the fibers of restriction               |

### **9.4. Expand the literature review**

The current literature review is appropriate but compressed.

I would divide it into four short subsections:

1. Classical inflation-restriction and group extension theory.
2. Non-abelian cohomology and neutral classes.
3. Weil groups and Langlands parameters.
4. Voltage graphs, relation modules and harmonic morphisms.

In particular, the literature on relation modules and group presentations is a natural bridge between the second and fourth topics.

Useful references to investigate include Kenneth Brown's *Cohomology of Groups*, Jean-Pierre Serre's *Trees*, and the literature on relation modules of group presentations.

I have not conducted an exhaustive literature search, so I would avoid asserting that the central obstruction criterion or its presentation-theoretic reformulation is new.

## **10. Suggested revised organization**

I recommend the following organization for Draft 2.

**1. Introduction**

Motivation, main results, notation, conventions and literature review.

**2. Background**

Group extensions, relative Weil groups, non-abelian H¹ and H².

**3. Inflation and restriction**

Invariant classes, transporters and exactness.

**4. The obstruction to extending a homomorphism**

Stabilizer extension, obstruction class, canonical obstruction extension, neutrality criterion, fibers and arithmetic examples.

**5. Extensions with non-abelian kernel**

New

Generalized stabilizer group, quotient obstruction extension and general extendibility theorem.

**6. A graph-theoretic formulation**

Voltage graphs, derived graphs, reconstruction, relation modules, graph homology, gain holonomy, cyclic and noncyclic examples.

**7. Topology and Langlands parameters**

Continuity and arithmetic applications.

**8. Open problems and further directions**

Root data, non-abelian continuation of the exact sequence, graphs of groups and harmonic morphisms.

**Acknowledgments, glossary and bibliography**

The title could remain unchanged. Alternatively, to emphasize the additional geometric material, I would consider:

*Inflation-restriction in non-abelian cohomology: centralizer obstructions, Weil groups, and voltage graphs*

This more accurately communicates the scope of the revised paper.

## **11. Suggested revision checklist**

### **Draft 2 action plan**

0 of 15 complete

**Mathematical corrections**

Correct the reconstruction assertion and give an explicit quotient construction.

Correct the norm-one torus injectivity statement.

Add the equivariance hypothesis to the central-homomorphism corollary.

Clarify the category of graphs used for harmonic morphisms.

Distinguish abstract extension cohomology from Galois cohomology.

Clarify the pinned dual-group action.

**New mathematical material**

Introduce the canonical obstruction extension.

Prove the generalization to non-abelian kernels.

Develop the relation-module and graph-homology interpretation.

Add the Klein four-group example.

Compute the fibers in the regular semisimple unramified example.

**Expository improvements**

Add extension diagrams and a notation subsection.

Expand the glossary and literature review.

Update the abstract, introduction and revision log.

Compile the revised manuscript and check references and figures.

&#x20;Copy revision checklist

## **12. Final evaluation**

Mathematical correctness

9/10

Readability

8.5/10

Quality of examples

9/10

Organization

8.5/10

Graph-theoretic development

8/10

Completeness of exposition

8/10

**Overall assessment**

# **8.5/10**

Qualitative referee assessment of the current draft.

The existing mathematical results are largely sound. The identified errors are repairable without altering the principal conclusions.

However, I would recommend more than simply correcting the errors. Two mathematical developments in particular could make Draft 2 a substantially stronger paper:

1. **Removing the abelian-kernel hypothesis** through the canonical quotient obstruction extension.
2. **Developing the relation-module and graph-homology interpretation** of inflation-restriction.

Together, these additions would move the manuscript beyond a corrected exposition of the original 1990s note toward a more general, geometrically motivated treatment of non-abelian inflation-restriction.

**Scope of verification:** I retrieved the LaTeX source directly from GitHub and examined the principal proofs and examples. I did not independently compile the manuscript, execute its existing verification script, or verify every bibliographic reference. No repository files have been modified.

My recommendation is to proceed to Draft 2, incorporating both the corrections and the proposed mathematical extensions.