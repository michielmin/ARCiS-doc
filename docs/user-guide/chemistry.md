# Composition and chemistry

## Free abundances

The simplest way to set the composition is to give constant volume mixing ratios for
each molecule:

```ini
H2=0.85
He=0.15
H2O=1d-4
CO=1d-5
CH4=1d-5
```

Any species from the [molecule list](../reference/molecules.md) can be used.
**Only the molecules that appear in the input are included in the opacity computation**,
and molecule names are case sensitive.

Useful related keywords:

* `H2+He=x` sets H<sub>2</sub>=0.85x and He=0.15x in one go.
* `trace:CO2=.false.` keeps a molecule in the structure (and mean molecular weight) but
  leaves it out of the radiative transfer — handy to see the contribution of a single
  species. `dotranshide=.true.` does this automatically for all species, writing
  `trans_hide_<molecule>` files.
* `background:N2=.true.` marks a gas as background that fills up the rest of the
  atmosphere.
* `Pswitch:H2O=1d-2` with `abun_switch:H2O=1d-6` gives a step in abundance: at pressures
  lower than `Pswitch` (higher up) the abundance is `abun_switch`.

## Equilibrium chemistry

With `chemistry=.true.` the composition is computed with the equilibrium chemistry code
GGchem ([Woitke et al. 2018](../citing.md)) from the elemental abundances:

```ini
chemistry=.true.
metallicity=0.5     ! log10 relative to solar
COratio=0.8
```

| Keyword | Default | Meaning |
|---|---|---|
| `metallicity` | 0 | log<sub>10</sub> of the metallicity relative to solar |
| `COratio` | 0.55 (solar) | C/O ratio |
| `NOratio`, `SiOratio`, `SOratio` | solar | N/O, Si/O and S/O ratios |
| `elementfile` | — | File with elemental abundances to use instead of solar |
| `elementlist` | `H He C N O Na Mg Si Fe Al Ca Ti S Cl K Li P V F Cr el` | Elements included |
| `condensates` | `.false.` | Remove condensing species from the gas phase |

The molecule keywords are still needed: they select which species contribute opacity.
Their values are overwritten by the chemistry.

!!! note "Condensation"
    `condensates=.true.` lets GGchem remove condensed material from the gas phase
    (rain-out). Leaving it `.false.` is the most stable choice. For cloud formation
    use a [cloud of type `CONDENSATION`](clouds.md), which computes the condensation
    including the cloud particles.

## Disequilibrium chemistry

With `diseq=.true.` the abundances of the species involved in the CH<sub>4</sub>–CO–
CO<sub>2</sub>–H<sub>2</sub>O and NH<sub>3</sub>–N<sub>2</sub> networks are quenched by
vertical mixing following [Kawashima & Min (2021)](../citing.md). It requires
`chemistry=.true.` and uses the global K<sub>zz</sub> profile. The species needed for the
disequilibrium network are added automatically.

## Vertical mixing (Kzz)

Vertical mixing is used by disequilibrium chemistry and by self-consistent clouds. By
default a constant `Kzz` is used (5×10<sup>8</sup> cm² s⁻¹). A pressure-dependent
profile is used when `Kzz_deep` and `Kzz_1bar` are set (`Kzz_1bar` is negative by
default, which switches the profile off).

For \(K_{zz}^{\rm contrast} > 1\):

\[
K_{zz}=\max\left[ K_{zz}^{\rm deep} ;\ \min\left[ K_{zz}^{\rm deep} K_{zz}^{\rm contrast} ;\
K_{zz}^{\rm 1bar} P^{-|\gamma_{K}|} \right] \right]
\]

For \(K_{zz}^{\rm contrast} < 1\):

\[
K_{zz}=\max\left[ K_{zz}^{\rm deep} K_{zz}^{\rm contrast} ;\ \min\left[ K_{zz}^{\rm deep} ;\
K_{zz}^{\rm 1bar} P^{|\gamma_{K}|} \right] \right]
\]

with P in bar.

| Keyword | Symbol | Default |
|---|---|---|
| `Kzz` | homogeneous K<sub>zz</sub> | 5×10<sup>8</sup> cm² s⁻¹ |
| `Kzz_deep` | \(K_{zz}^{\rm deep}\) | 10<sup>2</sup> cm² s⁻¹ |
| `Kzz_1bar` | \(K_{zz}^{\rm 1bar}\) | −1 (off) |
| `Kzz_contrast` | \(K_{zz}^{\rm contrast}\) | −1 (off) |
| `Kzz_P` | \(\gamma_K\) | 0.5 |
| `Kzz_max` | upper limit | 10<sup>12</sup> cm² s⁻¹ |

Clouds can use their own homogeneous K<sub>zz</sub> (`cloud1:Kzz`, with
`cloud1:globalKzz=.false.`) or follow the global profile (`cloud1:globalKzz=.true.`).
Disequilibrium chemistry always uses the global profile.

!!! question "To review"
    Additional options `complexKzz`, `computeKzz` (`SCKzz`) and `convectKzz` exist in
    the code. Their description still has to be added.

## Parameterised photochemistry

ARCiS can mimic photochemistry by converting molecules or atoms high in the atmosphere
into other molecules or haze. The conversion efficiency of a reaction is

\[
f_{\rm conversion} = f_{\rm eff}\, e^{-\tau_{\rm UV}},
\]

where \(\tau_{\rm UV}\) is computed from the UV opacity \(\kappa_{\rm UV}\) (`kappaUV`),
and \(f_{\rm eff}\) (`photoeff<n>`, default 1) is the maximum efficiency of reaction *n*.
\(f_{\rm conversion}\) is capped at 1, so \(f_{\rm eff}>1\) only means full conversion
extends to lower pressures.

**Atoms to molecules** — e.g. S + 2 O → SO<sub>2</sub>:

```ini
photoreac1:S=1
photoreac1:O=2
photoprod1:SO2=1
```

Atomic reactions are applied *before* the chemistry: the atoms are removed from the
elemental mixture and the products are added afterwards.

**Molecules to molecules** — e.g. H<sub>2</sub>S + 2 H<sub>2</sub>O → SO<sub>2</sub> + 3 H<sub>2</sub>:

```ini
photoreac1:H2S=1
photoreac1:H2O=2
photoprod1:SO2=1
photoprod1:H2=3
```

Molecular reactions are applied *after* the chemistry, so first the available amount of
H<sub>2</sub>S and H<sub>2</sub>O is computed. A reaction cannot mix atoms and molecules
as reactants.

**Haze production** — e.g. CH<sub>4</sub> → haze:

```ini
photoreac1:CH4=1
photohaze1=1      ! number of C atoms in haze per converted CH4
```

| Keyword | Meaning |
|---|---|
| `kappaUV` | UV opacity used to compute τ<sub>UV</sub> [cm² g⁻¹] |
| `gammaUV` | If set, `kappaUV = gammaUV × kappaT` |
| `photoeff<n>` | Maximum efficiency of reaction *n* |
| `photokappa<n>` | Scaling of κ<sub>UV</sub> for reaction *n* |
| `Pdestroy:<mol>` | Pressure above which a molecule is destroyed |

There is also an emulator for full photochemistry (`PhotoAI=.true.`), see
`Example/input_photochem.dat`.

## Planet formation

With `planetform=.true.` the elemental composition is computed from a simple planet
formation and migration model (SimAb, [Khorshid et al. 2022](../citing.md)), see the
*Planet formation link* section of the [keyword reference](../reference/keywords.md#planet-formation-link).
