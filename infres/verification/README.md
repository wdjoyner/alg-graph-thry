# Verification script

`infres_checks.py` checks the main results of the note by exhaustive
enumeration. It uses only the Python 3 standard library.

    python3 infres_checks.py > checks_output.txt

A full run takes about four minutes.

## What is checked

For each of twenty triples (extension `W`, normal abelian subgroup `N`,
`Gamma`-group `A`), with `|W| <= 24` and `|A| <= 24`, the script enumerates
every 1-cocycle of `W`, of `Gamma = W/N` and of `N` with values in `A`, and
checks the following. Numbers refer to Draft 1 of the note.

| Tag | Statement |
| --- | --- |
| `[S]` | The factor set identity (2.4) of Lemma 2.2 |
| `[E]` | Theorem 3.4: inflation is injective, the kernel of restriction is the image of inflation, restriction lands in `Gamma`-invariant classes |
| `[T]` | Theorem 4.4, (a) <=> (b) <=> (c), and the bijection between cocycles `f` with `f|N = phi` and maps `c`; Lemma 3.3; Lemma 4.1(ii) |
| `[O]` | Proposition 4.3(i),(ii) and Theorem 4.4(d): `(u_b, beta_b)` is a Springer 2-cocycle in the centralizer, and neutrality of the obstruction class is equivalent to `phi` being a restriction |
| `[F]` | Proposition 4.7: the fiber of restriction through `[f]` is in bijection with `H^1(Gamma, C_phi)` for the `f`-twisted action |
| `[G]` | Theorem 5.7: the holonomy criterion on the Cayley graph of `Gamma`, for a standard presentation of `Gamma` |

The groups `Gamma` that occur are `Z/2`, `Z/3`, `Z/2 x Z/2` and `S_3`. Split
and non-split extensions, and trivial and non-trivial actions on `A`, all
occur.

## Reading the output

The table gives, for each case, the sizes of `H^1(Gamma,A)`, `H^1(W,A)` and
`H^1(N,A)`, the number of `Gamma`-invariant classes, the number of classes in
the image of restriction, and the number of homomorphisms `phi` with invariant
class that do / do not extend to a cocycle of `W`.

The first two rows are the toy example of the note (Examples 2.3, 3.6, 4.9,
4.11 and 5.9): `N = Z/4`, `Gamma = Z/2` acting by inversion, `A = Q_8` with
trivial action. For `W = D_4` the three classes with `phi(rho)` of order 4
are invariant and not in the image of restriction; for `W = Q_8` they are in
the image.

The script is released under the MIT license (see `LICENSE`).
