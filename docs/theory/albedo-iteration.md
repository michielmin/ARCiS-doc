# Albedo iteration in 3D setups

This note explains the albedo iterations that ensure that the total energy is conserved,
also when the albedo differs between the day- and nightside of the planet.

The 3D scheme uses a β-map that is not aware of whether a local P–T point is on the
day- or nightside. This becomes a problem when the nightside has a different
reflectivity than the dayside, because the nightside cannot reflect stellar radiation.

## Equations

As explained in [Chubb & Min (2022)](../citing.md), the β-map represents a way of
redistributing heat from the day- to the nightside. The static β-map is

\[
\beta_\star=\cos\Lambda\cos\Phi
\]

on the dayside and \(\beta_\star=0\) on the nightside, with Λ and Φ the longitude and
latitude. The β-map is computed from a diffusion equation using \(\beta_\star\) as source
term. Both β and \(\beta_\star\) are normalised such that

\[
\int_{\rm planet}\beta=\int_{\rm planet}\beta_\star=\int_{\rm day}\beta_\star=1 .
\tag{1}
\]

The total amount of reflected light from the planet is

\[
f_{\rm ref}=\int_{\rm day}\beta_\star\,\omega .
\]

If the albedo ω is constant over the planet, the fraction of starlight reflected that
enters the P–T structure computation is

\[
f_{\rm ref}'=\int_{\rm planet}\beta\,\omega=\omega \int_{\rm planet}\beta
= \int_{\rm day}\beta_\star\,\omega =\omega .
\]

This only works for a constant albedo. If the albedo differs between day- and nightside,
\(f_{\rm ref}' \ne f_{\rm ref}\) and the energy balance is incorrect.

To solve this, the β-map is scaled with a constant γ, \(\beta'=\gamma\beta\). The emission
used for the P–T structure is then

\[
\gamma-\int_{\rm planet}\gamma\,\beta\,\omega .
\]

For the correct energy balance this must equal \(1-f_{\rm ref}\):

\[
\gamma-\int_{\rm planet}\gamma\,\beta\,\omega = 1-\int_{\rm day}\beta_\star\,\omega ,
\]

which gives

\[
\gamma=\frac{1-\int_{\rm day}\beta_\star\,\omega}{1-\int_{\rm planet}\beta\,\omega}.
\]

For constant ω, Eq. (1) gives γ = 1, as expected.

## Iteration

To compute γ, the albedo must be known everywhere on the planet. ARCiS starts with
γ = 1, computes the albedo everywhere, and uses it to compute a new estimate of γ.
Usually this is enough and γ does not change after one iteration. With self-consistent
cloud formation the albedo can depend strongly on the P–T structure, and more iterations
may be needed. The number of iterations is set with `nalbedo_iter` (default 1).
