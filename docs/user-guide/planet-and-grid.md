# Planet, star and grid

## Planet

| Keyword | Meaning | Unit |
|---|---|---|
| `Rp` | Planet radius at pressure `Pp` | R<sub>Jup</sub> |
| `Mp` | Planet mass | M<sub>Jup</sub> |
| `loggP` | Surface gravity log<sub>10</sub>(g) — when given, the mass follows from `Rp` and `loggP` | cgs |
| `Pp` | Pressure level that corresponds to `Rp` (default 10 bar) | bar |
| `Dplanet` | Orbital distance | AU |
| `distance` | Distance to the system (for fluxes in Jy) | pc |

By default the gravity varies with height, g(r) = GM/r². Use `constant_g=.true.` to keep
it fixed. The mean molecular weight is computed from the composition unless
`fixMMW=.true.` (then `MMW` is used).

For rocky planets the radius can be computed from the mass with a simple interior model
(`Rp_from_interior=.true.`), using a core mass fraction `interior_f_core` and a water
fraction `interior_f_ice`.

## Star

| Keyword | Meaning | Unit |
|---|---|---|
| `Tstar` | Effective temperature | K |
| `Rstar` | Radius | R<sub>☉</sub> |
| `Mstar` | Mass | M<sub>☉</sub> |
| `logg` | Surface gravity, used to select the stellar model | cgs |
| `starfile` | File with a stellar spectrum (λ, flux at the stellar surface in W m<sup>-2</sup> Hz<sup>-1</sup>) | |
| `bbstar` | Use a blackbody instead of a stellar model | |
| `standardstar` | Set T, R, M from a spectral type (`O2` … `L1`, e.g. `G2`) | |

## Using the planet database

Instead of setting all parameters by hand you can read them from the planet database:

```ini
planetname='WASP-107b'
```

This sets the planet radius and mass, the orbital distance, period and eccentricity, and
the stellar temperature, radius, mass and log g. When the mass is known, a Gaussian
prior on the mass is switched on for retrievals (`massprior`, `Mp_prior`, `dMp_prior`).

The database is `$HOME/ARCiS/Data/allplanets-ascii.txt` by default and can be changed
with `parameterfile`. A `.csv` file in the format of the NASA Exoplanet Archive can be
used as well.

!!! warning "Order matters"
    The database values are set when `planetname` is read. Keywords that appear
    **after** `planetname` override the database values, keywords **before** it are
    overwritten.

## Atmospheric grid

The atmosphere is divided into `nr` layers, logarithmically spaced in pressure between
`pmin` (top) and `pmax` (bottom):

| Keyword | Default | Meaning |
|---|---|---|
| `nr` | 20 | Number of layers |
| `pmin` | 10<sup>-6</sup> bar | Top of the atmosphere |
| `pmax` | 10<sup>3</sup> bar | Bottom of the atmosphere |

For parameterised cloud layers, extra grid points are inserted just above and below the
cloud boundaries so that sharp cloud tops are resolved.

The structure can also be read from a file: with `gridTPfile=.true.` the pressure grid of
`TPfile` is used, see [Temperature structure](temperature.md#reading-a-structure-from-file).

## Wavelength grid

| Keyword | Default | Meaning |
|---|---|---|
| `lmin` | 1 µm | Minimum wavelength |
| `lmax` | 15 µm | Maximum wavelength |
| `specres` | 10 | Spectral resolution λ/Δλ of the output spectrum |
| `specres_LR` | 10 | Resolution of the low-resolution grid used in temperature computations |

!!! tip
    For self-consistent temperature structures (`computeT=.true.`) the wavelength range
    must be wide enough to capture the bulk of the stellar and planetary flux, otherwise
    energy balance is not correct. Something like `lmin=0.2`, `lmax=30` or wider is a
    good start.

In retrievals, use `useobsgrid=.true.` to only compute the spectrum at the wavelengths
where there are observations. This can save a lot of time.
