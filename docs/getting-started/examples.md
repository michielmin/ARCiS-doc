# Examples

The repository contains example input files in `Example/` and regression tests in
`Tests/` (see [Tests](../developer/tests.md)). The test inputs are run regularly and are
the most reliable starting point.

| File | What it shows |
|---|---|
| `Example/input.dat` | Hot Jupiter with equilibrium chemistry and a parameterised (Guillot) temperature profile. Planet parameters from the database (`planetname=WASP-107b`). |
| `Example/simple.dat` | Free (constant) abundances and an isothermal profile — the simplest possible model. |
| `Example/WASP-17b.in` | As `input.dat`, with a self-consistent `DIFFUSE` cloud. |
| `Example/Retrieval.in` | Retrieval of the WASP-17b HST/STIS+WFC3 transmission spectrum (Sing et al. 2016) with chemistry and parameterised T profile, using MultiNest. |
| `Example/simple_retrieval.dat` | Free-chemistry retrieval of the same data. |
| `Example/input_read.in` | Read a full P–T–abundance structure from a file (`TPfile` with `mixratfile`). |
| `Example/input_photochem.dat` | Equilibrium chemistry with the photochemistry emulator (`PhotoAI`). |
| `Example/makecornerplot_pew.py` | Corner plot of a retrieval from `pew_output.dat`. |
| `Tests/test1.dat` | Hot Jupiter forward model with chemistry (regression test). |
| `Tests/Earth.in` | Earth-like planet with a condensation water cloud, surface and phase curve. |
| `Tests/SAG26_tau*.in` | Reflected-light benchmark: 3D, anisotropic scattering, parameterised cloud layer. |
| `Tests/Malik*.dat` | Self-consistent temperature structures of rocky planets with secondary atmospheres. |

!!! warning "Outdated examples"
    `Example/Earth.in` still uses an old cloud setup (`cloud1:column`,
    `cloud1:standard`, `cloud1:amin`, …) that the current code does not recognise,
    so ARCiS stops with *Unknown cloud keyword*. Use `Tests/Earth.in` instead.

## A walk through `Example/Retrieval.in`

```ini
* molecules that are included in the opacities
H2=0.85
He=0.15
H2O=1d-4
...
* read Rp, Mp, star and orbit from the database
planetname=WASP-017b
* abundances from equilibrium chemistry
chemistry=.true.
COratio=0.55
metallicity=0.2

* the data
obs1:type="trans"
obs1:file=WASP-17b_Sing_2015_Nature.dat

* Guillot temperature profile
par_tprofile=.true.

* retrieval parameters
fitpar:keyword="COratio"
fitpar:min=0.1d0
fitpar:max=1.5d0
...
* MultiNest with 200 live points, only computing the wavelengths of the data
retrieval=.true.
retrievaltype='MN'
npop=200
useobsgrid=.true.
```

Run it with

```bash
cd Example
ARCiS Retrieval.in -o retrieval_WASP17b
```

and make a corner plot of the posterior with

```bash
python makecornerplot_pew.py retrieval_WASP17b
```

(`pew_output.dat` is written by a post-processing run with `pew=.true.`; see
[Retrievals](../user-guide/retrieval.md#post-processing)).
