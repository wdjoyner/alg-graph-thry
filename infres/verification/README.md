# Verification script

`infres_checks.py` checks the main results of the note by exhaustive
enumeration. It uses only the Python 3 standard library.

    python3 infres_checks.py > checks_output.txt

A full run takes about six minutes. To run only the cases whose name contains
a given string, pass it as an argument, for example
`python3 infres_checks.py "N=Q8"`.

## What is checked

For each of twenty-seven triples (extension `W`, normal subgroup `N`,
`Gamma`-group `A`), with `|W| <= 24` and `|A| <= 24`, the script enumerates
every 1-cocycle of `W`, of `Gamma = W/N` and of `N` with values in `A`, and
checks the following. Numbers refer to Draft 2 of the note. In five of the
triples `N` is non-abelian; for those only `[E]`, `[T]`, `[B]` and `[F]` apply,
and they check Theorem 5.2 and Proposition 5.4.

| Tag | Statement |
| --- | --- |
| `[S]` | The factor set identity (2.4) of Lemma 2.2 |
| `[E]` | Theorem 3.4: inflation is injective, the kernel of restriction is the image of inflation, restriction lands in `Gamma`-invariant classes |
| `[T]` | Theorem 4.4, (a) <=> (b) <=> (c), and the bijection between cocycles `f` with `f|N = phi` and maps `c`; Lemma 3.3; Lemma 4.1(ii) |
| `[O]` | Proposition 4.3(i),(ii) and Theorem 4.4(d): `(u_b, beta_b)` is a Springer 2-cocycle in the centralizer, and neutrality of the obstruction class is equivalent to `phi` being a restriction |
| `[B]` | Lemma 5.1: the stabilizer `B_phi` of `phi` in the semidirect product of `A` and `W` is a group of order `|C_phi| |W|`, and the graph `D_phi` of `phi` is normal in it |
| `[F]` | Proposition 4.8 (and 5.4): the fiber of restriction through `[f]` is in bijection with `H^1(Gamma, C_phi)` for the `f`-twisted action |
| `[G]` | Theorem 6.9: the holonomy criterion on the Cayley graph of `Gamma`, for a standard presentation of `Gamma` |

The groups `Gamma` that occur are `Z/2`, `Z/3`, `Z/2 x Z/2` and `S_3`. Split
and non-split extensions, and trivial and non-trivial actions on `A`, all
occur.

## Reading the output

The table gives, for each case, the sizes of `H^1(Gamma,A)`, `H^1(W,A)` and
`H^1(N,A)`, the number of `Gamma`-invariant classes, the number of classes in
the image of restriction, and the number of homomorphisms `phi` with invariant
class that do / do not extend to a cocycle of `W`.

The first two rows are the toy example of the note (Examples 2.3, 3.6, 4.10,
4.12 and 6.11): `N = Z/4`, `Gamma = Z/2` acting by inversion, `A = Q_8` with
trivial action. For `W = D_4` the three classes with `phi(rho)` of order 4
are invariant and not in the image of restriction; for `W = Q_8` they are in
the image.

The row `S3 (N=C3) / C3 trivial` is the counterexample quoted in the proof of
Corollary 4.7. The rows with `N=center` of `Q8` are Example 6.13 (the Klein
four-group). The rows `Q8xZ2 (N=Q8)` and `Q8oZ4 (N=Q8)` are Example 5.5.

The script is released under the MIT license (see `LICENSE`).
