# Opacities and radiative transfer

## Molecular opacities

Molecular opacities are read from precomputed tables in `opacitydir` (default
`$HOME/ARCiS/Data/Opacities/`), based on the ExoMolOP database
([Chubb et al. 2021](../citing.md)). By default correlated-k tables are used with `ng`
g-points (default 25); `useXS=.true.` switches to cross-section tables.

Only molecules that appear in the input file are read. Molecule tables are binned to the
ARCiS wavelength grid set by `lmin`, `lmax` and `specres`.

## Continuum opacities

| Keyword | Default | Meaning |
|---|---|---|
| `cia` | `.true.` | Collision-induced absorption. H<sub>2</sub>–H<sub>2</sub> and H<sub>2</sub>–He are found automatically in `$HOME/ARCiS/Data/CIA` (or `$HOME/HITRAN`). |
| `cia<n>:file` | | Additional CIA file in HITRAN `.cia` format |
| `rayleigh` | `.true.` | Rayleigh scattering by the gas |
| `useff` | | Free-free and bound-free opacities (H<sup>-</sup> etc.) |

If CIA is on but no CIA files are found, ARCiS stops and asks to rerun with
`cia=.false.`.

## Spectra

ARCiS computes transmission and emission spectra by ray tracing through the
atmosphere.

| Keyword | Default | Meaning |
|---|---|---|
| `transspec` | `.true.` | Compute the transmission spectrum |
| `emisspec` | `.true.` | Compute the emission spectrum |
| `maxtau` | 50 | Maximum optical depth considered in the ray tracing |
| `phase<n>` | 180 | Phase angles for emission / reflection (degrees, 180 = full dayside) |
| `contrib` | `.false.` | Write contribution functions |
| `dotranshide` | `.false.` | Also compute transmission spectra with each species/cloud left out |

## Scattering

| Keyword | Default | Meaning |
|---|---|---|
| `scattering` | `.false.` | Include scattering of the planet's own thermal emission |
| `scattstar` | `.false.` | Include scattering of stellar light (reflected light) |
| `anisoscattstar` | `.false.` | Anisotropic scattering of stellar light (otherwise isotropic) |
| `Nphot` | 2500 | Number of photon packages for the Monte Carlo scattering computation |

!!! Tip "Scattering"
	Scattering in ARCiS is computed differntly in 3D mode and 1D mode. When running in the default 1D mode
	scattering is computed with Monte Carlo radiative transfer, which is slow and noisy.
	It is therefore strongly recommended to use 3D mode for accurate scattering results 
	(see [3D models and phasecurves](3d.md)).

Reflected light needs `scattstar=.true.`; for an accurate phase dependence use `anisoscattstar=.true.`.

## Surface

For planets with a surface, the bottom of the atmosphere (`pmax`) is the surface. Its
reflectance is set with `surfacetype`:

| `surfacetype` | Meaning |
|---|---|
| `BLACK` (default) | Black surface |
| `GREY` | Grey surface with albedo `surfacealbedo` |
| `WHITE` | Fully reflecting surface |
| `PARAMETERISED` | Three-step albedo: `surf_alb1` below `surf_lam1`, `surf_alb2` up to `surf_lam2`, `surf_alb3` beyond |
| `FILE` | Reflectance from `surfacefile` (wavelength [µm], reflectance [%]) |
| `WATER`, `ICE`, `SNOW`, `GRASS`, `SAND` | Single surface type, spectra from `Data/Surface/` |
| `EARTH` | Mixture: ocean fraction `fwater`, of which a fraction `fice` is ice-covered; on land a fraction `fsnow` is snow, of the rest a fraction `fgrass` is vegetation and the remainder sand |
| `PARLAND` | Ocean (`fwater`) plus land with the `PARAMETERISED` three-step albedo |
| `GREYLAND` | Ocean (`fwater`) plus grey land with albedo `surfacealbedo` |
| `QUARTZ`, `FeO`, `LABRADORITE`, `MIXED` | Rocky surfaces computed from refractive indices with a Hapke model (`MIXED`: 60% enstatite, 30% forsterite, 10% quartz) |

With `lambertsurface=.false.` and anisotropic stellar scattering, the ocean is treated
with a wind-roughened Fresnel surface (glint) and the other surfaces with a
bidirectional reflectance model, instead of Lambertian surfaces.

### Retrieving the surface albedo

`fit_albedo=.true.` retrieves the surface albedo non-parametrically: in each likelihood
evaluation the albedo spectrum is solved for with a Gaussian-process prior (with an
optional step for the vegetation red edge and a linear slope). This requires
`useobsgrid=.true.`. The GP options are listed under *Surface* in the
[keyword reference](../reference/keywords.md#surface). This mode is currently still under construction
and will be published soon and rolled out as a standard feature.

