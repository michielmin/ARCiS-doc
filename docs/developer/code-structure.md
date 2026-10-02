# Code structure

ARCiS is written in Fortran (mostly fixed-form `.f` with extended line length, some
`.f90`). All global variables live in modules in `Modules.f`, most notably
`GlobalSetup`; changing `Modules.f` triggers a recompilation of everything.

## Program flow

`Main.f` drives a run:

```text
getcommandline          read command line arguments
GetOutputDir            create the output directory (-o)
Init                    read keywords, set defaults, allocate, read data   (Init.f)
ReadObs                 read observations, if any                          (Retrieval.f)
then one of:
  opacitymode    → SetupOpacities + WriteOpacityFITS
  pew            → PostEqualWeights                                        (PostEqualWeights.f)
  makeai         → MakeAI                                                  (MakeAI.f)
  retrieval      → DoRetrieval                                             (Retrieval.f)
  otherwise      → ComputeModel → WriteStructure → WriteOutput
```

`ComputeModel` (`ComputeModel.f`) computes one forward model: structure, chemistry,
clouds, temperature iteration and the spectra. For 3D models it calls `Run3D`.

## How keywords are read

All input handling is in `Init.f`:

1. `GetKeywords` reads the input file(s) and command line into a linked list of
   `SettingKey` records. `get_key_value` splits each line into `key1` (lower case,
   trailing number removed → `nr1`), the part after `:` (`key2`, `nr2`) and the value.
2. `CountStuff` makes a first pass to count molecules, clouds, observations, retrieval
   parameters, etc., and allocates arrays. A few keywords (`nr`, `nTpoints`, `pmin`,
   `pmax`, …) are read here because array sizes depend on them.
3. `SetDefaults` sets the default values of all parameters.
4. `ReadAndSetKey` is called for every keyword; it is one large `select case` on
   `key1`, delegating to `ReadCloud`, `ReadObsSpec`, `ReadRetrieval`, etc. for
   keywords with sub-keys. Unknown keywords stop the program.
5. `ConvertUnits` converts input units (R<sub>Jup</sub>, AU, µm, …) to cgs.

### Adding a new keyword

1. Declare the variable in `Modules.f` (usually in `GlobalSetup`).
2. Set its default in `SetDefaults` (or in `Cloud(i)%…` defaults for cloud keywords).
3. Add a `case("mykey","alias")` to `ReadAndSetKey` (or to `ReadCloud`, …).
4. Document it: add a description to `docs/reference/keyword_descriptions.yml` and
   regenerate the reference (see [Writing documentation](documentation.md)).

## Source files

| Area | Files |
|---|---|
| Main program, input | `Main.f`, `Init.f`, `InputOutput.f`, `Modules.f`, `Version.f` |
| Forward model | `ComputeModel.f`, `SetupStructure.f` (structure, P–T profiles, K<sub>zz</sub>) |
| Radiative transfer | `Raytrace.f` (spectra), `MCRad.f` (Monte Carlo scattering), `ComputeT.f` (temperature structure), `BDREF.f` (surface BRDFs) |
| Opacities | `SetupOpacities.f`, `OpacityFITS.f`, `CIA.f`, `ComputePAH.f` (optEC/PAH) |
| Chemistry | `GGchemARCiS.f` + `ggchem/` (GGchem), `easy_chem*.f90`, `diseq_*.f90` (disequilibrium), `PhotoAI.f`, `EOS.f`, `nasa_polynomial.f` |
| Clouds | `SetupCloud.f` (cloud types), `CondensationCloud.f`, `DiffuseCloud.f`, `WaterCloud.f`, `ComputePart.f` (particle opacities: Mie, DHS, blending), `DLMie.f`, `*Data.f` (built-in refractive indices) |
| 3D | `Run3D.f` (β-map, 3D setup), `ReadFull3D.f`, `LightCurve.f` |
| Retrieval | `Retrieval.f`, `MultiNestARCiS.f`, `params_multinest.f90`, `MCMC_ARCiS.f`, `Genetic.f`, `mrqmin.f`, `amoeba.f`, `PostEqualWeights.f`, `MakeAI.f` |
| Output | `WriteOutput.f`, `writeFITS.f`, `ConvertColors.f` (images), `MakeBibList.f90` (`refs.tex`) |
| Planet formation | `Formation.f` |
| Python interface | `MainPy.f90`, `SupportPy.f`, `setup.py`, `pyIO.f90` + `pybridge.c` (calling Python from Fortran) |
| Numerical libraries | `Lapack.f`, `dlsei.f`, `truncated_normal.f`, `Subroutines.f` |

## Other directories

| Directory | Contents |
|---|---|
| `Example/` | Example input files and data |
| `Tests/` | Regression tests, see [Tests](tests.md) |
| `doc/` | Old LaTeX documentation (superseded by this site) |
| `docs/` | This documentation (mkdocs) |
| `python/`, `notebooks/` | Notebooks for the Python interface and plotting |
| `plotscripts/` | Plotting scripts |
| `ggchem/` | GGchem equilibrium chemistry |
