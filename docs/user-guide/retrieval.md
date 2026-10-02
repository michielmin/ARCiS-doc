# Retrievals

A retrieval needs three things in the input file: the **observations**, the
**retrieval parameters**, and `retrieval=.true.`.

```ini
obs1:type='trans'
obs1:file='wasp39b.dat'

fitpar:keyword='metallicity'
fitpar:min=-1
fitpar:max=3

fitpar:keyword='Rp'
fitpar:min=1.0
fitpar:max=1.5

retrieval=.true.
useobsgrid=.true.
npop=400
```

## Observations

Observations are numbered `obs1:`, `obs2:`, … and can be combined freely (e.g.
transmission from one instrument and emission from another).

| Sub-keyword | Meaning |
|---|---|
| `type` | Type of observation, see below |
| `file` | File with the data |
| `beta` | Weight of this data set: its errors are divided by `beta` (default 1) |
| `iphase` | For emission at several phases: index of the `phase<n>` this data set belongs to |
| `filter` | Filter curves for photometric points |

All sub-keywords are listed in the [keyword reference](../reference/keywords.md#obsn-sub-keywords).

### Observation types

| `type` | Data | Units (same as the output file) |
|---|---|---|
| `trans` | Transmission spectrum | (R<sub>p</sub>/R<sub>⋆</sub>)², as in `trans` |
| `emis` | Emission spectrum (planet flux) | Jy, as in `emis` |
| `emisR` | Planet-to-star contrast | F<sub>p</sub>/F<sub>⋆</sub>, as in `emisR` |
| `phase`, `phaseR` | Phase-resolved emission (absolute / relative) | |
| `transC`, `transM`, `transE` | Transmission variants (e.g. morning/evening limb in 3D) | |
| `lightcurve` | Spectroscopic light curve | |
| `tprofile`, `logtp` | Constraint on the temperature profile | |
| `prior` | Gaussian priors on the retrieval parameters (`fitpar:init`, `fitpar:spread`) | |

By default emission data (`emis`) are compared in log space (`logemis=.true.`); this
requires positive fluxes.

### Observation files

Spectra are plain text files with one wavelength bin per line:

| Column | Content | Required |
|---|---|---|
| 1 | Wavelength [µm] | yes |
| 2 | Observed value (units as in the matching output file) | yes |
| 3 | 1σ error | yes |
| 4 | Spectral resolution R = λ/Δλ of the bin | no (default `specres`) |
| 5 | Shape exponent *s* of the bin response | no (default 20) |

The model is binned onto each data point with a response
\(w\propto\exp\left(-\left|2R\,\Delta\lambda/\lambda\right|^{s}\right)\): large *s*
(the default 20) gives a top-hat bin, *s* = 2 a Gaussian.

Example (`Example/WASP-17b_Sing_2015_Nature.dat`):

```text
0.340   1.5610e-02  2.0740e-04   6.8
0.405   1.5060e-02  2.0372e-04  27.0
0.4275  1.4923e-02  1.9057e-04  57.0
```

Lines that cannot be read (e.g. a header) are skipped.

!!! tip "useobsgrid"
    Set `useobsgrid=.true.` to compute the spectrum only at the wavelengths of the
    data. This speeds up retrievals considerably. It is required for `fit_albedo`.

## Retrieval parameters

Each `fitpar:keyword=` line starts a new parameter; the following `fitpar:` lines
apply to it. **Any input keyword can be retrieved**, including molecule abundances,
cloud parameters (`cloud1:SigmaDot`), temperature-profile parameters and planet
parameters.

| Sub-keyword | Default | Meaning |
|---|---|---|
| `keyword` | | Input keyword to retrieve |
| `min`, `max` | 0, 1 | Prior range |
| `log` | `.false.` | Uniform prior in log space |
| `init` | centre of the range | Starting value (also the mean of a Gaussian prior). If the keyword is set elsewhere in the input file, that value is used. |
| `spread` | | Width of a Gaussian prior (with an `obs` of type `prior`) |

```ini
fitpar:keyword='H2O'
fitpar:min=1d-12
fitpar:max=1d0
fitpar:log=.true.

fitpar:keyword='cloud1:SigmaDot'
fitpar:min=1d-20
fitpar:max=1d-8
fitpar:log=.true.
```

Special parameters:

* `tprofile` sets up a free temperature profile, see
  [Temperature structure](temperature.md#free-profile).
* Retrieving `Tstar`, `Rstar` or `logg` recomputes the stellar spectrum.
* `Mp` with `massprior=.true.` (set automatically from the planet database) uses a
  Gaussian mass prior.

## Samplers

Select the sampler with `retrievaltype`:

| `retrievaltype` | Method |
|---|---|
| `MN` (default) | MultiNest nested sampling ([Feroz et al. 2009](../citing.md)) |
| `MC` / `MCMC` | Markov chain Monte Carlo |
| `OE` | Optimal estimation (gradient-based, quick) |
| `FULL` | MultiNest followed by MCMC |

### MultiNest options

| Keyword | Default | Meaning |
|---|---|---|
| `npop` | 30 | Number of live points |
| `efr` | 0.3 | Sampling efficiency |
| `ftol` | 0.5 | Evidence tolerance |
| `is_nest` | `.false.` | Importance nested sampling |
| `consteff` | `.false.` | Constant efficiency mode |
| `resume_nest` | `.false.` | Resume an interrupted run |
| `nestupdate` | 100 | Iterations between output updates |

!!! tip
    The default `npop=30` is only suitable for quick tests. Use a few hundred live
    points (e.g. `npop=400`) for production runs.

### MCMC options

| Keyword | Default | Meaning |
|---|---|---|
| `npop` | 30 | Number of walkers / burn-in |
| `npost` | 1000 | Number of posterior samples |
| `epsinit` | 0.1 | Initial step size |
| `computelogZ` | `.false.` | Compute the evidence by thermodynamic integration (see [MCMC evidence](../theory/mcmc-evidence.md)) |

## Noise and model errors

| Keyword | Meaning |
|---|---|
| `obs<n>:adderr` | Extra error added to a data set |
| `model_err_abs`, `model_err_rel` | Absolute / relative model error added in quadrature |
| `obs<n>:cov_a`, `obs<n>:cov_L` | Amplitude and correlation length of correlated noise |
| `fullcovmat` | Use the full covariance matrix |
| `faircoverage` | Weight data so that densely sampled regions do not dominate |

!!! question "To review"
    The correlated-noise model (`cov_*`, localised components `cov_*_loc`) and the
    scaling/offset options (`obs<n>:scaling`, `slope`, `offset`) need a description of
    the equations used.

## Output of a retrieval

| File | Content |
|---|---|
| `retrieval` | Best fit and uncertainties of all parameters |
| `bestfit.dat` | Input file of the best-fit model — rerun with `ARCiS bestfit.dat -o best` |
| `post_equal_weights.dat` | MultiNest posterior samples (equal weights) |
| `stats.dat`, `summary.txt`, `.txt` | Other MultiNest output |
| `posteriorMCMC.dat`, `MCMCstats` | MCMC posterior and statistics |
| `Wolk.dat` | All models computed during the retrieval (`writeWolk`) |
| `trans`, `emis`, … | Spectra of the best-fit model |
| `obs001`, `obs002`, … | Data and best-fit model at the data points |
| `limits.dat`, `trans_limits.dat`, `PT_limits`, … | Confidence intervals of spectra and structure |

## Post-processing

After a MultiNest run, the posterior can be post-processed by running ARCiS again in
the **same output directory** with `pew=.true.` (post equal weights):

```bash
ARCiS Retrieval.in -o out -s pew=.true.
```

This recomputes models for the posterior samples (`npew` of them, default all) and
writes confidence intervals of the spectra and the P–T structure, the median parameters
including derived C/O and metallicity (`retrieval`), an input file for the median probability model
(`mpm.dat`), and `pew_output.dat` for corner plots (see
`Example/makecornerplot_pew.py`).
