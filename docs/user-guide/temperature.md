# Temperature structure

ARCiS offers several ways to set the pressure–temperature (P–T) structure, from a fixed
profile to a fully self-consistent computation.

## Power-law / isothermal profile (default)

Without any other setting the temperature follows a power law in pressure:

\[
\log_{10} T = \log_{10} T_p + dT_p\,\log_{10}(P/1\,{\rm bar})
\]

| Keyword | Default | Meaning |
|---|---|---|
| `TP` | 600 K | Temperature at 1 bar |
| `dTP` | 0.1 | Slope; `dTP=0` gives an isothermal atmosphere |

## Parameterised profile (Guillot 2010)

With `par_tprofile=.true.` the analytic profile of Guillot (2010) for an irradiated
atmosphere is used:

\[
T^4 = \frac{3T_{\rm int}^4}{4}\left(\frac{2}{3}+\tau\right)
    + \frac{3T_{\rm irr}^4}{4}\,\beta\left[\frac{2}{3}+\frac{1}{\gamma\sqrt3}
    +\left(\frac{\gamma}{\sqrt3}-\frac{1}{\gamma\sqrt3}\right)e^{-\gamma\tau\sqrt3}\right]
\]

with \(\tau = \kappa_{\rm IR} P/g\) and \(T_{\rm irr}=T_\star\sqrt{R_\star/D}\).

| Keyword | Symbol | Default | Meaning |
|---|---|---|---|
| `TeffP` | \(T_{\rm int}\) | 600 K | Internal temperature of the planet |
| `kappaT` | \(\kappa_{\rm IR}\) | 3×10<sup>-4</sup> cm² g⁻¹ | Mean infrared opacity |
| `gammaT` | \(\gamma\) | 0.158 | Ratio of visible to infrared opacity |
| `betaT` | \(\beta\) | 1 | Fraction of the substellar irradiation (redistribution) |
| `gammaT2`, `alphaT` | | | Second visible channel and its weight (two-channel variant) |

The temperature is capped at 10 000 K. With `computeTeff=.true.` the internal temperature
is estimated from the irradiation following Thorngren & Fortney (2018), with a minimum of
85 K.

## Free profile

For retrievals a free P–T profile can be used. It is defined by `nTpoints` points that
are (by default) equally spaced in log P between `pmin` and `pmax`. The simplest way to
use it is to retrieve the keyword `tprofile`:

```ini
nTpoints=5
fitpar:keyword='tprofile'
```

This adds the temperature gradients at the points (and their pressures, with
`free_fitP=.true.`) as retrieval parameters. Options:

| Keyword | Meaning |
|---|---|
| `free_fitT` | Use temperatures at the points instead of gradients |
| `free_fitP` | Also retrieve the pressures of the points (default `.true.`) |
| `pos_dT` | Only allow positive gradients (no inversions) |
| `pos_dT_lowest` | Only force a positive gradient at the deepest point |
| `wiggle_err` | Penalise wiggles (curvature) in the profile; ≤0 switches this off |
| `logTprofile` | Sample temperatures logarithmically between `Tmin` and `Tmax` |

!!! question "Todo"
    The free profile can also be built from visible- and IR-channel points
    (`tauVpoint`, `tauIRpoint`, `dTVpoint`, `dTIRpoint`) and has a TauREx-like
    interpolation (`taurexprofile`). These options still need a description.

## Self-consistent temperature structure

With `computeT=.true.` ARCiS computes the temperature structure in radiative–convective
equilibrium, iterating between the structure (chemistry, clouds) and the radiative
transfer. The radiative transfer for the temperature is solved on a low-resolution
wavelength grid from 0.11 µm to 47 µm with a spectral resolution set by `specres_LR`.
The computation of the temperature structure always includes the effects of scattering.

| Keyword | Default | Meaning |
|---|---|---|
| `TeffP` | 600 K | Internal temperature |
| `betaT` | 1 | Irradiation factor (cosine of the incidence angle / redistribution) |
| `maxiter` | 6 | Maximum number of iterations |
| `miniter` | 3 | Minimum number of iterations |
| `epsiter` | 0.03 | Convergence criterion |
| `specres_LR` | 10 | Spectral resolution of the radiative transfer grid |
| `exp_ad` | 1.4 | Adiabatic exponent |
| `useEOS` | `.false.` | Adiabatic gradient from tabulated EOS |

With `par_tprofile=.true.` and `computeT=.true.` the Guillot profile is used as starting
point of the iteration.

`adiabatic_tprofile=.true.` limits the temperature gradient of any profile to the
adiabat.

## Reading a structure from file

```ini
TPfile='mystructure.dat'
```

The file has two columns: pressure [bar] and temperature [K]. The profile is
interpolated onto the ARCiS pressure grid. With `gridTPfile=.true.` the grid of the file
itself is used (`nr` must be at least the number of lines).

With `mixratfile=.true.` the file also contains the mixing ratios. The format is then

```text
3
H2O CO CH4
1e-6  1200  1e-4 1e-4 1e-6
1e-5  1210  1e-4 1e-4 1e-6
...
```

First line: number of molecules; second line: their names; then one line per layer with
P [bar], T [K] and the abundances. See `Example/input_read.in`.
