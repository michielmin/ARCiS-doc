# Clouds

ARCiS has two families of clouds:

* **self-consistent clouds**, where the cloud structure follows from nucleation,
  condensation, diffusion, sedimentation and coagulation;
* **parameterised clouds**, where the cloud location and optical depth are set directly.

Any number of cloud layers can be defined. Each layer is set with `cloudN:` keywords,
where *N* is the layer number:

```ini
cloud1:type='CONDENSATION'
cloud1:SigmaDot=1d-12
cloud2:type='DECK'
cloud2:Ptop=1d-2
```

`cloud0:` sets a value for all layers. The full list of cloud keywords and their
defaults is in the [keyword reference](../reference/keywords.md#cloudn-sub-keywords).

Partial cloud coverage is set per layer with `cloudN:coverage` (fraction of the planet,
default 1). The spectrum is then the weighted sum of the cloudy and clear columns.

## Self-consistent cloud formation

### Condensation clouds (recommended)

```ini
cloud1:type='CONDENSATION'
```

The clouds are formed by diffusion and sedimentation, following detailed condensation
physics using the Gibbs free energies of the condensates [Huang et al. (2024)](https://doi.org/10.1051/0004-6361/202451112).
Multiple condensates can grow on the same particles, and each condensate takes the atoms
it needs from the gas consistently.

| Keyword | Default | Meaning |
|---|---|---|
| `type` | | `CONDENSATION` |
| `condensate<n>` | | Condensate species *n* (see list below). Without a number, the species is appended. |
| `SigmaDot` | 10<sup>-17</sup> | Column-integrated nucleation rate [g cm⁻² s⁻¹] |
| `P` | 10<sup>-4</sup> bar | Pressure of maximum nucleation |
| `dP` | 10 | Width of the nucleation profile (factor in pressure) |
| `Kzz` | | K<sub>zz</sub> for this cloud [cm² s⁻¹]; only used when > 0 and `globalKzz=.false.` |
| `globalKzz` | `.false.` | Use the global K<sub>zz</sub> profile. The global profile is also used when `Kzz` is not set. |
| `coagulation` | `.true.` | Compute coagulation of cloud particles |
| `rainout` | `.false.` | Remove material that is (partly) stable at the bottom boundary from the gas |
| `Srainout` | 1 | Saturation ratio at the bottom above which material rains out |
| `haze` | `.false.` | Include the mass and opacity of the cloud nuclei |
| `hazetype` | `SOOT` | Material of the nuclei (any built-in material) |
| `freeflow_con` | `.true.` | Free-flow lower boundary for condensates (instead of full evaporation) |
| `freeflow_nuc` | `.true.` | Free-flow lower boundary for nuclei (instead of x<sub>n</sub> = 0) |
| `usefsed` | `.false.` | Use an f<sub>sed</sub> sedimentation parameterisation |
| `fsed` | 1 | Value of f<sub>sed</sub> |
| `fmax` | 0 | Irregularity parameter of the DHS shape model (0 = Mie spheres) |

When `cloud<n>:globalKzz=.true.` the profile will be used as described in [Composition and chemistry](../user-guide/chemistry.md)

Available condensates:

| Group | Species |
|---|---|
| Silicates | `SiO2`, `MgSiO3`, `Mg2SiO4`, `SiO`, `FeSiO3`, `Fe2SiO4`, `CaSiO3`, `NaAlSi3O8` |
| Oxides | `MgO`, `FeO`, `Fe2O3`, `Fe3O4`, `Al2O3`, `TiO2`, `CaTiO3`, `MgAl2O4`, `CaO` |
| Sulfides | `FeS`, `Na2S`, `ZnS`, `MnS` |
| Salts | `NaCl`, `KCl`, `NH4Cl`, `NaNO3` |
| Metals | `Fe`, `Zn`, `Mn`, `Cr`, `Ni`, `W` |
| Ices and others | `H2O`, `NH3`, `NH4SH`, `CH4`, `H2SO4`, `SiC`, `S` |

In addition, when the crystalline silicates `FORSTERITE`, `ENSTATITE`, `FAYALITE`, or `FERROSILITE` 
are added to the species list along with their amorphous counterparts, the crystallinity of that 
silicate component is computed from the temperature dependent crystallization timescale assuming 
silicate condense amorphous.

The refractive indices are taken from `$HOME/ARCiS/Data/refind/`; new condensates may
require an update of the data directory. Some species use the optical properties of a
related material (e.g. CaSiO<sub>3</sub> uses MgSiO<sub>3</sub>, NH<sub>4</sub>SH uses
NH<sub>3</sub>, all Ti oxides use TiO<sub>2</sub>).

Example: a silicate cloud following the global K<sub>zz</sub> profile:

```ini
cloud1:type='CONDENSATION'
cloud1:SigmaDot=1d-12
cloud1:condensate01='SiO2'
cloud1:condensate02='MgSiO3'
cloud1:condensate03='Mg2SiO4'
```

Every condensate adds computing time.

### Diffuse clouds (old scheme)

```ini
cloud1:type='DIFFUSE'
```

The cloud model of [Ormel & Min (2019)](../citing.md), as used in
[Min et al. (2020)](../citing.md). The cloud species condense one by one following a
prescribed condensation sequence. This has the disadvantage that different materials can
take the same atoms from the gas. Use `CONDENSATION` for new work.

Specific keywords: `SigmaDot`, `Kzz`, `globalKzz`, `coagulation`, `rainout`, `haze`,
`hazetype`, `condensates` (switch off for a pure haze), `computecryst` (compute the
crystallinity of silicates) and `cryst` (fixed crystallinity, default 1). The opacities
are always computed with DHS and effective medium theory.

```ini
cloud1:type='DIFFUSE'
cloud1:globalKzz=.false.
cloud1:Kzz=1d8
cloud1:SigmaDot=1d-12
cloud1:computecryst=.true.
```

A `WATER` type exists for water clouds with the same machinery.

## Cloud structure from a file

```ini
cloud1:type='FILE'
cloud1:file='mycloud.dat'
```

All parameters of the cloud are read from the file. The type `FILEDRIFT` reads a cloud
structure in the output format of the DRIFT cloud code.

!!! question "Todo"
    The file formats for `FILE` and `FILEDRIFT` are still to be documented.

## Parameterised clouds

The parameterised cloud types set where the cloud is and how optically thick it is at a
reference wavelength `lam_ref` (default 1 µm). The optical properties of the particles
are set separately, see [Cloud opacities](#cloud-opacities). For the underlying
equations see also the note on [cloud parameterisation (PDF)](../assets/CloudParameterisation.pdf).

### `LAYER`

Cloud between `Ptop` and `Pbottom` with an opacity that increases with pressure as a
power law \(P^{\xi}\), normalised to reach optical depth `tau` at pressure `Ptau`.

| Keyword | Default | Meaning |
|---|---|---|
| `Ptop` | 0 | Top of the cloud [bar] |
| `Pbottom` | 10<sup>10</sup> | Bottom of the cloud [bar] |
| `Ptau` | 1 bar | Pressure where optical depth `tau` is reached (if < 0: `Pbottom`) |
| `tau` | 1 | Optical depth at `lam_ref` |
| `xi` | 2 | Power law of the opacity with pressure |
| `lam_ref` | 1 µm | Reference wavelength |

### `SLAB`

Cloud between `Ptop` and `Pbottom` with a mass fraction that varies linearly with
pressure, with total optical depth `tau` at `lam_ref`.

### `DECK`

A deck with infinite extent below. The cloud is parameterised through the gradient of the
optical depth,

\[
\frac{\partial \tau}{\partial P}=C\,\exp\left(\frac{P-P_\tau}{\Phi}\right).
\]

In hydrostatic equilibrium \(\partial\tau/\partial P = \kappa/g\), with
\(\kappa = f_{\rm cloud}\kappa_{\rm cloud}\), so that 

\[
f_{\rm cloud}=\frac{g}{\kappa_{\rm cloud}}\,C\,\exp\left(\frac{P-P_\tau}{\Phi}\right),
\]

where \(C\) is set by requiring \(\tau=1\) at \(P_\tau\). At low pressures
\(f_{\rm cloud}\) becomes constant, so the cloud extends with a constant mass fraction to
the top of the atmosphere.

| Keyword | Default | Meaning |
|---|---|---|
| `Ptau` | 1 bar | Pressure where τ = 1 at `lam_ref` |
| `dlogP` | 2 | Pressure scale Φ over which the cloud optical depth falls off |
| `lam_ref` | 1 µm | Reference wavelength |

### `GAUSS` and `HALFGAUSS`

A layer with a Gaussian profile in log P around `P` with width `dP`, total optical depth
`tau` at `lam_ref`, and opacity power law `xi`. `HALFGAUSS` has a much steeper fall-off
below the centre.

| Keyword | Default | Meaning |
|---|---|---|
| `P` | 10<sup>-4</sup> bar | Central pressure |
| `dP` | 10 | Width (σ in ln P) |
| `tau` | 1 | Optical depth at `lam_ref` |
| `xi` | 2 | Power law of the opacity with pressure |

### `HOMOGENEOUS`

Not really a cloud, but a homogeneous component of the atmosphere: a constant mass
mixing ratio `mixrat` of particles at all pressures above `Ptop`.

### `RING`

Uses the cloud particle setup to give the particles of a planetary ring (see `doRing`).

## Cloud opacities

The opacity type is set with `cloudN:opacitytype`:

| `opacitytype` | Meaning |
|---|---|
| `PARAMETERISED` | Parameterised opacity law |
| `REFIND` | Particles with a constant refractive index *n + ik* |
| `MATERIAL` | Particles made of real materials (built-in or from lnk-files) |
| `FILE`, `OPACITY` | Precomputed particle opacities |
| `AUTO` (default) | `MATERIAL` for `CONDENSATION` clouds |

### Parameterised opacity

To be used when there is no information on the composition (e.g. no mid-infrared
features):

\[
\kappa_{\rm ext}=\frac{\kappa_0}{1+\left(\lambda/\lambda_0\right)^{p}}
\]

\(\lambda_0\) marks the transition from grey to a power law, which happens around
\(\lambda\sim 2\pi r\). For Rayleigh scattering \(p=4\), for small absorbing particles
\(p\approx 2\). The single-scattering albedo \(\omega\) is wavelength independent.

| Keyword | Default | Meaning |
|---|---|---|
| `kappa` | 0.01 | \(\kappa_0\) [cm² g⁻¹] |
| `lam_kappa` | 1 µm | \(\lambda_0\) |
| `pow_kappa` | 4 | \(p\) |
| `albedo` | 0.99 | \(\omega\) |

### Particle size distribution

For `REFIND` and `MATERIAL` the particles have a size distribution (Hansen
distribution)

\[
n(r)\,{\rm d}r\propto r^{\frac{1-3v_{\rm eff}}{v_{\rm eff}}}
\exp\left(-\frac{r}{r_{\rm eff}v_{\rm eff}}\right),\qquad r > r_{\rm nuc},
\]

with an effective radius varying with pressure:

\[
r_{\rm eff}=r_{\rm nuc}+r_{\rm eff,0}\left(\frac{P}{P_{\rm ref}}\right)^{\gamma}.
\]

| Keyword | Default | Meaning |
|---|---|---|
| `reff` | 1 µm | \(r_{\rm eff,0}\) |
| `veff` | 0.1 | \(v_{\rm eff}\), dimensionless width |
| `pow_rad` | 0 | \(\gamma\) (> 0: larger particles deeper down) |
| `Pref` | 1 bar | \(P_{\rm ref}\) |
| `rnuc` | 0.001 µm | Smallest particle radius |
| `nsize` | 1 | Number of sizes in the distribution |
| `fmax` | 0 | Irregularity (DHS); 0 = homogeneous spheres (Mie) |
| `porosity` | 0 | Porosity |

The particle shape is modelled with a distribution of hollow spheres (DHS,
[Min et al. 2005](../citing.md)) with irregularity parameter `fmax`.

### Constant refractive index

```ini
cloud1:opacitytype='REFIND'
cloud1:n=1.5
cloud1:k=0.01
```

Works best for narrow wavelength ranges where the refractive index does not vary much.

### Real materials

```ini
cloud1:opacitytype='MATERIAL'
```

Materials are numbered; each is a built-in material or read from a refractive index file
(three columns: wavelength [µm], n, k). For a file, set `material<n>='FILE'` and give the
file with `lnkfile<n>`:

| Keyword | Meaning |
|---|---|
| `material<n>` | Built-in material name, or `FILE` to read `lnkfile<n>` |
| `lnkfile<n>` | Refractive index file (isotropic) |
| `lnkfilex<n>`, `lnkfiley<n>`, `lnkfilez<n>` | Files for the three crystal axes (all three must be given) |
| `abun<n>` | Abundance of material *n* in the mixture |
| `rho_mat<n>` | Material density [g cm⁻³] |

Pure forsterite with anisotropic optical constants:

```ini
cloud1:opacitytype='MATERIAL'
cloud1:material='FILE'
cloud1:lnkfilex='forsterite_x.lnk'
cloud1:lnkfiley='forsterite_y.lnk'
cloud1:lnkfilez='forsterite_z.lnk'
```

A mixture of a built-in material and anisotropic forsterite:

```ini
cloud1:opacitytype='MATERIAL'
cloud1:material01='ENSTATITE'
cloud1:material02='FILE'
cloud1:lnkfilex02='forsterite_x.lnk'
cloud1:lnkfiley02='forsterite_y.lnk'
cloud1:lnkfilez02='forsterite_z.lnk'
cloud1:abun01=0.4
cloud1:abun02=0.6
```

Built-in materials: `ENSTATITE`, `FORSTERITE`, `ASTROSIL`/`OLIVINE`, `PYROXENE`,
`SiO2`/`QUARTZ`, `A-SiO2`, `SiO`, `SiC`, `IRON`, `CORRUNDUM`, `FeO`, `MgO`,
`RUTILE`/`BROOKITE`/`TiO2`, `WATER`, `H2SO4`, `CARBON`, `SOOT`, `ORGANICS`, `THOLIN`,
`optEC`.

## Examples

A parameterised cloud layer reaching τ = 1 at 1 bar with a steep opacity increase:

```ini
cloud1:type='LAYER'
cloud1:Ptop=1d-3
cloud1:Ptau=1d0
cloud1:xi=4
cloud1:opacitytype='PARAMETERISED'
cloud1:kappa=100
cloud1:pow_kappa=2
cloud1:albedo=0.1
```

A patchy water cloud on an Earth-like planet (from `Tests/Earth.in`):

```ini
cloud1:type='CONDENSATION'
cloud1:condensate='H2O'
cloud1:Kzz=1d8
cloud1:coverage=0.35
cloud1:usefsed=.true.
cloud1:fsed=2d0
cloud1:globalGasMix=.true.
```
