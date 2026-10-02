# Keyword reference

This page is **generated from the source code** (`Init.f`) by `docs/scripts/gen_reference.py`: the keywords, aliases and default values are always those of the current code. Descriptions come from `docs/reference/keyword_descriptions.yml`.

* Keywords are **case-insensitive**, molecule names are **case-sensitive**.
* A trailing number is an index: `phase2`, `tauVpoint3`.
* Keywords with sub-keywords use a colon: `cloud1:tau=10`, `obs2:file=…`.
* Values use Fortran list-directed input: `1d-4`, `.true.`, `'TEXT'`.

Markers: ✎ description inferred from the code and still to be verified; <span class="unused">no effect</span> keyword is read but its value is not used anywhere in the current code.

## Run control

| Keyword | Default | Description |
|---|---|---|
| `useomp`<br><small>`openmp`</small> | `.true.` | Use OpenMP parallelisation (only relevant when compiled with `multi=true`). |
| `retrieval` | `.false.` | Perform a retrieval instead of a single forward model. See [Retrievals](../user-guide/retrieval.md). |
| `opacitymode` | `.false.` | Do not compute a model, but compute and write opacity tables (FITS) on a P–T grid. See `np`, `nt`, `opacitydir`. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `makeai` | `.false.` | Compute a grid of models with random parameters drawn from the retrieval parameter ranges (e.g. as training set for machine-learning emulators). Number of models set by `nai`. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `nai` | 1000 | Number of models computed when `makeai=.true.`. |
| `parametergridfile` | *(empty)* | File with a list of parameter values to compute when `makeai=.true.`, instead of random draws. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `pew`<br><small>`postequalweights`</small> | `.false.` | Post-process an existing retrieval: recompute models for the posterior samples (`post_equal_weights`) and write spectra/structure confidence limits. |
| `npew` | -1 | Number of posterior samples used when `pew=.true.` (-1 = all). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `idum`<br><small>`seed`</small> | 42 | Seed for the random number generator (only used when `randomseed=.false.`). |
| `randomseed` | `.true.` | Initialise the random number generator from the system clock. Set to `.false.` (and set `idum`) for reproducible runs. |
| `iwolk` | 0 | Read line *iwolk* of `Wolk.dat` from a previous retrieval in the output directory and use those parameter values. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `writewolk` | `.true.` | Write the `Wolk.dat` file with all models evaluated during a retrieval. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `planetname` | *(empty)* | Read planet and star parameters (radius, mass, orbit, stellar T, R, M, log g) from the planet database (`parameterfile`). **Values are set at the moment this keyword is read**, so keywords appearing *after* `planetname` override the database. |
| `parameterfile`<br><small>`planetparameterfile`</small> | `$HOME/ARCiS/Data/allplanets-ascii.txt` | Planet database used by `planetname`. Can be the ARCiS ASCII format or a `.csv` file (e.g. the NASA Exoplanet Archive). |
| `standardstar` | *(empty)* | Set Tstar, Rstar and Mstar from a standard spectral type (O2 … L1, e.g. `G2`). <span class="review" title="Inferred from the code, to be checked">✎</span> |

## Planet and star

| Keyword | Default | Description |
|---|---|---|
| `rp` | 1 | Planet radius at pressure `Pp`. <small>[R<sub>Jup</sub>]</small> |
| `mp` | 1 | Planet mass. <small>[M<sub>Jup</sub>]</small> |
| `loggp` | 2.5 | Planet surface gravity log<sub>10</sub>(g). When given, the mass is computed from `Rp` and `loggP` (overrides `Mp`). <small>[cgs]</small> |
| `pp` | 10 | Pressure level corresponding to the radius `Rp`. <small>[bar]</small> |
| `constant_g` | `.false.` | Use a constant gravity throughout the atmosphere instead of g(r). |
| `fixmmw` | `.false.` | Fix the mean molecular weight to `mmw` instead of computing it from the composition. |
| `mmw` | 2.2 | Mean molecular weight used when `fixmmw=.true.`. <small>[amu]</small> |
| `rp_from_interior`<br><small>`interior`</small> | `.false.` | Compute the planet radius from the mass with a simple rocky/metal interior model (Birch–Murnaghan EOS), using `interior_f_core` and `interior_f_ice`. |
| `interior_f_core` | 0.325 | Core (metal) mass fraction for the interior model. |
| `interior_f_ice`<br><small>`interior_f_h2o`</small> | 0.005 | Ice (water) mass fraction for the interior model. |
| `tstar` | 5777 | Stellar effective temperature. <small>[K]</small> |
| `rstar` | 1 | Stellar radius. <small>[R<sub>☉</sub>]</small> |
| `mstar` | 1 | Stellar mass. <small>[M<sub>☉</sub>]</small> |
| `logg` | 4.5 | Stellar surface gravity log<sub>10</sub>(g), used to select the stellar model spectrum. <small>[cgs]</small> |
| `starfile` | *(empty)* | File with the stellar spectrum (wavelength, flux at the stellar surface in W m<sup>-2</sup> Hz<sup>-1</sup>). Default is a Kurucz model. |
| `bbstar` | `.false.` | Use a blackbody for the stellar spectrum. |
| `dp`<br><small>`dplanet`</small> | 1 | Orbital distance of the planet. <small>[AU]</small> |
| `projecteddp`<br><small>`projecteddplanet`</small> | `.false.` | Interpret `Dplanet` as the projected distance at phase `phase1`. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `distance` | 10 | Distance to the system (used for absolute fluxes in Jy). <small>[pc]</small> |
| `orbit` | -1 | Orbital elements, given as `orbit:P` (period, s; default computed from Kepler's law), `orbit:e`, `orbit:omega` and `orbit:inc` (degrees). Used for light curves. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `vrot` | 0 | Rotational velocity of the planet, for velocity-resolved spectra. <small>[cm/s]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `vrot_max`<br><small>`vrotmax`</small> | 0 | Maximum velocity of the velocity grid. <small>[cm/s]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `nvrot` | 0 | Number of velocity bins on each side of zero. <span class="review" title="Inferred from the code, to be checked">✎</span> |

## Atmospheric and spectral grid

| Keyword | Default | Description |
|---|---|---|
| `nr` | — | Number of pressure layers in the atmosphere. |
| `nrsurf` | — | Additional layers placed below `Psurf` (added to `nr`). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `psurf` | 10 | Pressure range (factor below `pmax`) where the `nrsurf` extra layers are placed. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `pmin` | 1e-06 | Pressure at the top of the atmosphere. <small>[bar]</small> |
| `pmax` | 1000 | Pressure at the bottom of the atmosphere. <small>[bar]</small> |
| `setsurfp`<br><small>`setsurfpressure`</small> | `.false.` | Set `pmax` to the sum of the given partial pressures (molecule keywords then act as partial pressures in bar). Used for secondary atmospheres with a surface. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `lmin` | 1 | Minimum wavelength. For temperature computations (`computeT`) the range must cover the bulk of the stellar and planetary emission. <small>[µm]</small> |
| `lmax` | 15 | Maximum wavelength. <small>[µm]</small> |
| `lam` | 1 | Alternative to `lmin`/`lmax`: `lam1` sets the minimum, `lam2` the maximum wavelength. <small>[µm]</small> |
| `specres` | 10 | Spectral resolution λ/Δλ of the computed spectrum. |
| `specreslr`<br><small>`specres_lr`, `specresrt`, `specres_rt`</small> | 10 | Spectral resolution of the low-resolution grid used for the temperature structure computation. |
| `specresfile` | *(empty)* | File with a wavelength-dependent spectral resolution. <span class="unused" title="Parsed by Init.f but not used anywhere else in the code">no effect</span> |
| `nrcloud`<br><small>`nrhr`</small> | 10 | Number of sub-layers used in the self-consistent cloud computations (internally converted to a refinement factor `nrcloud/nr`). |
| `nrstepchem` | 1 | Compute chemistry only every *n*-th layer inside the cloud formation loop, and interpolate in between (speed-up). |

## Composition and chemistry

| Keyword | Default | Description |
|---|---|---|
| `<molecule>`<br><small>e.g. `H2O`, `CO2`</small> | 0 | Any molecule from the [molecule list](molecules.md), e.g. `H2O=1d-4`, sets a constant volume mixing ratio. Only molecules that appear in the input are included in the opacity computation. **Molecule names are case sensitive.** Values are overwritten when `chemistry=.true.`; then the keyword only selects which molecules contribute opacity. |
| `h2+he` | 0 | Shortcut to set the H<sub>2</sub>+He background: 85% H<sub>2</sub>, 15% He of the given value. |
| `chemistry` | `.false.` | Compute the composition with equilibrium chemistry (GGchem). |
| `condensates` | `.false.` | Include condensation (and depletion of the gas phase) in the equilibrium chemistry. Most stable is to leave it `.false.`; use a cloud of type `CONDENSATION` for self-consistent clouds. |
| `metallicity` | 0 | Atmospheric metallicity, log<sub>10</sub> relative to solar. |
| `dmetallicity`<br><small>`dz`</small> | 0 | Metallicity gradient with pressure. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `coratio` | 0.549541 | C/O ratio of the atmosphere (default is solar). |
| `sioratio` | 0.0660693 | Si/O ratio (default solar). |
| `noratio` | 0.138038 | N/O ratio (default solar). |
| `soratio` | 0.0269153 | S/O ratio (default solar). |
| `inversecoratio` | `.false.` | Changes how the C/O ratio is imposed: by default C is adjusted, with this switch O is adjusted. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `elementfile` | *(empty)* | File with the elemental abundances to use instead of solar. |
| `elementlist` | `H He C N O Na Mg Si Fe Al Ca Ti S Cl K Li P V F Cr el` | List of elements included in the chemistry computation. |
| `diseq` | `.false.` | Include disequilibrium chemistry from vertical mixing (Kawashima & Min 2021). Uses the global K<sub>zz</sub> profile. |
| `dophotoai`<br><small>`usephotoai`, `photoai`</small> | — | Use the machine-learning photochemistry emulator (calls Python through a pipe). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `ggchem_piter` | `.true.` | Iterate on pressure in GGchem. Only set to `.false.` to reproduce old results. |
| `ggchem_tfast` | 700 | Temperature below which GGchem uses its slower, more robust mode. <small>[K]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `secondary_atmosphere` | `.false.` | Treat the atmosphere as a secondary (outgassed) atmosphere in the chemistry. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `waterworld` | `.false.` | Water-world setup: the surface pressure and composition follow from a water ocean in equilibrium with the atmosphere. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `fh2o` | 0.0002 | Water mass fraction for the water-world setup. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `simplerainout` | `.false.` | Remove condensing species below the condensation level in a simple way. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `mixp` | 0 | Below this pressure the atmosphere is assumed to be well mixed (chemistry only computed for P ≥ mixP). <small>[bar]</small> |
| `fixmol` | — | Fix a molecule's abundance: `fixmol1:name=H2O`, `fixmol1:abun=1d-4`, `fixmol1:P=…` (only above this pressure). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `pswitch` | — | Pressure at which the abundance of a molecule switches, e.g. `Pswitch:H2O=1d-2`; used together with `abun_switch`. <small>[bar]</small> |
| `abunswitch`<br><small>`abun_switch`</small> | — | Abundance of a molecule at pressures below `Pswitch`, e.g. `abun_switch:H2O=1d-6`. |
| `background`<br><small>`backgroundgas`</small> | — | Mark a molecule as background gas, e.g. `background:N2=.true.`; the background fills up the remainder of the atmosphere. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `dotrace`<br><small>`trace`</small> | — | Exclude (`.false.`) or include a molecule in the radiative transfer while keeping it in the structure, e.g. `trace:CO2=.false.`. |
| `isotope`<br><small>`f_isotope`</small> | — | Isotopologue setup: `isotope:CO=…` names the molecule to use as isotopologue, `f_isotope:CO=…` its fraction. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `useff`<br><small>`use_ff`</small> | — | Include free-free / bound-free continuum opacities (H<sup>-</sup> etc.). |
| `optec` | 0 | Volume mixing ratio of carbon atoms in optEC (amorphous hydrocarbon) haze. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `rad_optec` | 0.01 | Particle radius of the optEC haze. <small>[µm]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `eg_optec` | 1 | Band gap of the optEC material. <small>[eV]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `pah` | 0 | Abundance of PAHs. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `ncpah`<br><small>`nc_pah`</small> | 25 | Number of carbon atoms per PAH molecule. |

## Vertical mixing (Kzz)

| Keyword | Default | Description |
|---|---|---|
| `kzz` | 5e+08 | Homogeneous eddy diffusion coefficient. Used when `Kzz_1bar` is not set. <small>[cm² s⁻¹]</small> |
| `kzz_deep` | 100 | K<sub>zz</sub> in the deep atmosphere (see [Kzz profile](../user-guide/chemistry.md#vertical-mixing-kzz)). <small>[cm² s⁻¹]</small> |
| `kzz_1bar`<br><small>`kzz_up`</small> | -1 | K<sub>zz</sub> at 1 bar of the power-law part of the profile. A negative value switches the profile off. <small>[cm² s⁻¹]</small> |
| `kzz_p`<br><small>`kzz_pow`</small> | 0.5 | Power γ<sub>K</sub> of the pressure dependence. |
| `kzz_contrast` | -1 | Contrast between the minimum and maximum K<sub>zz</sub>. A negative value switches it off. |
| `kzz_offset` | 10000 | Minimum value added to K<sub>zz</sub>. <small>[cm² s⁻¹]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `kzz_max` | 1e+12 | Maximum allowed K<sub>zz</sub>. <small>[cm² s⁻¹]</small> |
| `complexkzz` | `.false.` | Use the more complex K<sub>zz</sub> parameterisation. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `computekzz` | `.false.` | Compute K<sub>zz</sub> self-consistently from the structure. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `convectkzz` | `.false.` | Increase K<sub>zz</sub> in convective regions (mixing-length estimate). <span class="review" title="Inferred from the code, to be checked">✎</span> |

## Photochemistry (parameterised)

| Keyword | Default | Description |
|---|---|---|
| `photoreac`<br><small>`photoreactant`, `photoprod`, `photoproduct`</small> | — | Reactant of a parameterised photochemical reaction, e.g. `photoreac1:CH4=1`. Also `photoprod1:<molecule>=n` for products. See [Photochemistry](../user-guide/chemistry.md#parameterised-photochemistry). |
| `photoeff` | 1 | Maximum efficiency f<sub>eff</sub> of reaction *n* (`photoeff1`). |
| `photokappa`<br><small>`photoscalekappa`</small> | 1 | Scaling of κ<sub>UV</sub> for reaction *n*. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `photohaze` | 0 | Convert reactants of reaction *n* into haze, with the given number of C atoms per molecule. |
| `kappauv` | -1 | UV opacity κ<sub>UV</sub> used to compute τ<sub>UV</sub>. <small>[cm² g⁻¹]</small> |
| `gammauv` | -1 | If ≥0, set κ<sub>UV</sub> = γ<sub>UV</sub> × `kappaT`. |
| `distruv` | `.false.` | In 3D models, distribute the UV over the whole planet instead of only the dayside. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `photdestroy`<br><small>`photodestroy`, `pdestroy`</small> | — | Pressure above which a molecule is photo-destroyed, e.g. `Pdestroy:NH3=1d-3`. <small>[bar]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |

## Temperature structure

| Keyword | Default | Description |
|---|---|---|
| `tp` | 600 | Temperature at 1 bar for the default power-law profile: log T = log T<sub>p</sub> + dT<sub>p</sub> log P. <small>[K]</small> |
| `dtp` | 0.1 | Slope dT<sub>p</sub> of the power-law profile (0 = isothermal). |
| `partprofile`<br><small>`par_tprofile`</small> | `.false.` | Use the parameterised (Guillot 2010) temperature profile set by `TeffP`, `kappaT`, `gammaT`, `betaT`. |
| `teffp`<br><small>`tplanet`</small> | 600 | Internal (intrinsic) temperature of the planet. <small>[K]</small> |
| `kappa`<br><small>`kappat`</small> | 0.0003 | Mean infrared opacity κ<sub>IR</sub> of the Guillot profile. <small>[cm² g⁻¹]</small> |
| `gamma`<br><small>`gammat`</small> | 0.158 | Ratio κ<sub>vis</sub>/κ<sub>IR</sub>. `gammaT2` sets a second visible channel (two-stream variant). |
| `beta`<br><small>`betat`</small> | 1 | Redistribution/irradiation factor β: the fraction of the substellar irradiation used (≈ cosine of incidence angle). |
| `alpha`<br><small>`alphat`</small> | 1 | Weight between the two visible channels when `gammaT2` is set. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `grey_isot` | `.false.` | Use an isothermal profile at the grey equilibrium temperature. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `computet` | `.false.` | Compute the temperature structure self-consistently (radiative–convective equilibrium). |
| `maxiter` | 6 | Maximum number of iterations for the self-consistent temperature structure. |
| `miniter` | 3 | Minimum number of iterations. |
| `epsiter` | 0.03 | Convergence criterion for the temperature iteration. |
| `exp_ad` | 1.4 | Adiabatic exponent (C<sub>p</sub>/C<sub>v</sub>). |
| `useeos`<br><small>`use_eos`</small> | `.false.` | Use a tabulated equation of state for the adiabatic gradient (requires `Data/EOS`). |
| `adiabatic`<br><small>`adiabatic_tprofile`</small> | `.false.` | Limit the temperature gradient to the adiabat. |
| `isofstar` | `.false.` | Assume isotropic incident stellar flux in the temperature computation. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `forceebalance` | `.false.` | Force exact energy balance by rescaling the emission (computes all wavelengths). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `computeteff` | `.false.` | Estimate the internal temperature from the irradiation (Thorngren & Fortney 2018), with a minimum of 85 K. |
| `tsurface` | -1 | Surface temperature used as a constraint in the temperature computation. <small>[K]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `tmin` | 2.7 | Minimum temperature allowed in the structure (also lower bound for retrieved free-profile temperatures). <small>[K]</small> |
| `tmax` | 10000 | Maximum temperature allowed (also upper bound for retrieved free-profile temperatures). <small>[K]</small> |
| `maxt`<br><small>`maxtprofile`</small> | 1e+06 | Temperatures in the profile are capped at this value. <small>[K]</small> |
| `tpfile` | *(empty)* | Read the P–T structure from file (columns: P [bar], T [K]). With `mixratfile=.true.` also mixing ratios. |
| `gridtpfile` | `.false.` | Use the pressure grid of `TPfile` as the atmospheric grid (then `nr` must match the file). |
| `mixratfile` | `.false.` | `TPfile` also contains mixing ratios. First line: number of molecules, second line: molecule names, then rows of P, T, abundances. |
| `free_tprofile` | `.false.` | Use a free temperature profile defined by temperature points (switched on automatically when retrieving `tprofile`). |
| `ntpoints`<br><small>`nfreet`</small> | — | Number of points of the free temperature profile. |
| `tpoint`<br><small>`dtpoint`</small> | 0.285714 | Value at point *n* of the free temperature profile (temperature gradient or temperature, see `free_fitT`). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `ppoint` | — | Pressure of point *n* of the free temperature profile. <small>[bar]</small> |
| `preftpoint`<br><small>`pref`</small> | — | Reference pressure of the free temperature profile. <small>[bar]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `free_fitt`<br><small>`freetp_fitt`, `freept_fitt`</small> | — | Free profile is parameterised by temperatures instead of temperature gradients (read in the pre-pass). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `free_fitp`<br><small>`freetp_fitp`, `freept_fitp`</small> | — | Also retrieve the pressures of the free profile points. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `free_fitdt`<br><small>`freetp_fitdt`, `freept_fitdt`</small> | — | Inverse of `free_fitT`. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `tauvpoint` | 1 | Optical depth of visible-channel point *n* of the free profile. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `tauirpoint` | 1 | Optical depth of IR-channel point *n* of the free profile. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `dtvpoint` | 0.285714 | Gradient at visible-channel point *n*. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `dtirpoint` | 0.285714 | Gradient at IR-channel point *n*. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `pos_dt` | `.false.` | Force positive temperature gradients in the free profile (no inversions). |
| `pos_dt_lowest` | `.false.` | Force a positive gradient only at the deepest point. |
| `wiggle_err` | -1 | Regularisation of the free temperature profile: penalises curvature in the likelihood (≤0 = off). |
| `logtprofile` | `.true.` | Sample free-profile temperatures logarithmically. |
| `taurexprofile` | `.false.` | Interpolate the free profile like TauREx (with smoothing). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `taurexsmooth` | 1.2 | Smoothing width (in dex of pressure) of the TauREx-like profile. |

## Opacities and radiative transfer

| Keyword | Default | Description |
|---|---|---|
| `opacitydir` | `$HOME/ARCiS/Data/Opacities` | Directory with the molecular opacity tables (FITS). |
| `usexs` | `.false.` | Use cross-section tables instead of correlated-k tables. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `ng` | 25 | Number of g-points in the correlated-k treatment. |
| `cia` | — | Include collision-induced absorption. `cia1:file=…` adds extra CIA files (HITRAN format); H2–H2 and H2–He are found automatically in `Data/CIA`. |
| `rayleigh` | `.true.` | Include Rayleigh scattering by the gas. |
| `scattering` | `.false.` | Include scattering of the thermal radiation of the planet. |
| `scattstar`<br><small>`starscatt`</small> | `.false.` | Include scattering of stellar light (reflected light). |
| `anisoscatt`<br><small>`anisostar`, `anisostarscatt`, `anisoscattstar`</small> | `.false.` | Use anisotropic scattering for the stellar light (otherwise isotropic). |
| `maxtau`<br><small>`max_tau`</small> | 50 | Maximum optical depth considered in the ray tracing. |
| `np` | 50 | Number of pressure points of the opacity table in `opacitymode`. |
| `nt` | 100 | Number of temperature points of the opacity table in `opacitymode`. |
| `outputopacity`<br><small>`writeopacity`</small> | `.false.` | Write the opacities per layer to the output directory. |
| `contrib`<br><small>`computecontrib`</small> | `.false.` | Compute and write contribution functions. |
| `dlmie` | `.false.` | Use the DLMie neural-network emulator for Mie computations. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudoverlap` | `.true.` | How partial cloud coverages of different cloud layers combine: overlapping (`.true.`) or independent. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `emisspec` | `.true.` | Compute the emission spectrum. |
| `transspec` | `.true.` | Compute the transmission spectrum. |
| `dotranshide` | `.false.` | Additionally compute transmission spectra with each molecule/cloud hidden in turn (`trans_hide_*` files). |
| `nrtatm` | -1 | Number of atmospheres used in the ray tracing of 3D models (-1 = all). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `nphot` | 2500 | Number of photon packages for the Monte Carlo scattering computation of the spectra (with `scattering`/`scattstar`). |
| `factrw` | 10 | Threshold (in optical depth per cell) above which the Monte Carlo scattering code uses a modified random walk. <span class="review" title="Inferred from the code, to be checked">✎</span> |

## Surface

| Keyword | Default | Description |
|---|---|---|
| `surfacetype` | `BLACK` | Type of surface at the bottom of the atmosphere: `BLACK`, `GREY`, `WHITE`, `PARAMETERISED`, `FILE`, `WATER`, `ICE`, `SNOW`, `GRASS`, `SAND`, `EARTH`, `PARLAND`, `GREYLAND`, `QUARTZ`, `FeO`, `LABRADORITE`, `MIXED`. See [Surface](../user-guide/radiative-transfer.md#surface). |
| `surfacealbedo` | 0.5 | Albedo of a grey surface. |
| `surfacefile` | — | File with the surface reflectance (wavelength [µm], reflectance [%]) for `surfacetype=FILE`. |
| `lambert`<br><small>`lambertsurf`, `lambertsurface`</small> | `.true.` | Treat the surface as a Lambertian reflector (otherwise a BRDF is used for anisotropic stellar scattering). |
| `fwater`<br><small>`focean`</small> | 0.7 | Fraction of the surface covered by water (`EARTH` surface). |
| `fice` | 0.05 | Fraction covered by ice. |
| `fsnow` | 0.2 | Fraction covered by snow. |
| `fgrass` | 0.5 | Fraction covered by vegetation. |
| `surf_lam` | 0.7 | Wavelengths of the steps in the `PARAMETERISED` surface albedo (`surf_lam1`, `surf_lam2`). <small>[µm]</small> |
| `surf_alb` | 0.15 | Albedo values of the `PARAMETERISED` surface below `surf_lam1`, between, and above `surf_lam2` (`surf_alb1..3`). |
| `lam_re`<br><small>`l_re`, `lamre`</small> | 0.7 | Wavelength of the red edge (alias for `surf_lam1`). <small>[µm]</small> |
| `lamstep`<br><small>`lam_step`</small> | 0.7 | Wavelength of step *n* in the surface albedo fit. <small>[µm]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `fit_albedo` | `.false.` | Fit the surface albedo non-parametrically (Gaussian process) during the retrieval. Requires `useobsgrid=.true.`. |
| `fit_albedo_gp` | `.false.` | Use a Gaussian-process prior for the albedo (`fit_albedo_GP3` for the three-segment variant). |
| `fit_albedo_sigma` | 0.25 | Amplitude of the GP prior on the albedo. |
| `fit_albedo_sigma_gp` | 0.25 | Amplitudes of the three GP segments (`fit_albedo_sigma_GP1..3`). |
| `fit_albedo_gp3_lam` | 0.7 | Segment boundaries for the three-segment GP (`fit_albedo_GP3_lam1/2`). <small>[µm]</small> |
| `fit_albedo_l` | 0.08 | Correlation length of the GP kernel. <small>[µm]</small> |
| `fit_albedo_l_step` | 0.02 | Width of the step in the albedo model. <small>[µm]</small> |
| `fit_albedo_step` | `.false.` | Include a step (red edge) in the albedo model. |
| `fit_albedo_sigma_step` | 0.25 | Prior width on the step height. |
| `fit_albedo_slope` | `.false.` | Include a linear slope in the albedo model. |
| `fit_albedo_sigma_slope` | 1 | Prior width on the slope. |
| `fit_albedo_ls` | `.false.` | Solve the albedo with plain least squares instead of a GP. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `fit_albedo_matern` | `.false.` | Use a Matérn kernel instead of a squared-exponential kernel. |
| `fit_albedo_remove_lin` | `.false.` | Remove the linear trend before fitting the GP. <span class="review" title="Inferred from the code, to be checked">✎</span> |

## Retrieval

| Keyword | Default | Description |
|---|---|---|
| `retpar`<br><small>`fitpar`</small> | — | Define a retrieval parameter (usually written as `fitpar:`). See the [`fitpar:` sub-keywords](#fitpar-sub-keywords). |
| `obs` | — | Define an observation. See the [`obsN:` sub-keywords](#obsn-sub-keywords). |
| `retrievaltype` | `MN` | Sampler: `MN`/`MultiNest` (nested sampling, default), `MC`/`MCMC`, `OE` (optimal estimation), `FULL` (MultiNest followed by MCMC). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `npop`<br><small>`nburn`</small> | 30 | MultiNest: number of live points. MCMC: number of walkers / burn-in. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `ngen` | 0 | Number of generations for the genetic/optimal-estimation algorithm. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `npost` | 1000 | Number of posterior samples in the MCMC chain. |
| `epsinit`<br><small>`epsinit_mcmc`</small> | 0.1 | Initial step size of the MCMC. |
| `mcmclogz`<br><small>`domcmclogz`, `computelogz`</small> | `.false.` | Compute the Bayesian evidence from the MCMC with thermodynamic integration (see [MCMC evidence](../theory/mcmc-evidence.md)). |
| `fmultinest`<br><small>`efr`</small> | 0.3 | MultiNest sampling efficiency (`efr`). |
| `tolmultinest`<br><small>`ftol`</small> | 0.5 | MultiNest evidence tolerance. |
| `ins_nest`<br><small>`is_nest`</small> | `.false.` | Use importance nested sampling in MultiNest. |
| `consteff` | `.false.` | Use MultiNest's constant efficiency mode. |
| `resume_nest` | `.false.` | Resume an interrupted MultiNest run from the files in the output directory. |
| `nestupdate` | 100 | Number of iterations between MultiNest output updates. |
| `useobsgrid` | `.false.` | Only compute the spectrum at wavelengths of the observations (strongly recommended for retrievals). |
| `model_err_abs` | 0 | Absolute model error added in quadrature to the observational errors. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `model_err_rel` | 0 | Relative model error added in quadrature. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `fullcovmat`<br><small>`corrnoise`</small> | `.true.` | Use the full covariance matrix (correlated noise, see `obsN:cov_*`). |
| `cov_a_loc` | 0 | Amplitude of localised correlated-noise component *n*. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cov_l_loc` | 1 | Correlation length of localised component *n*. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cov_lam_loc` | 0 | Central wavelength of localised component *n*. <small>[µm]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `adderr` | 0 | Extra error added to observations *n1..n2*. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `eps_dup`<br><small>`duplicate`, `eps_duplicate`</small> | 0.1 | Tolerance used to detect duplicate parameter vectors. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `logemis`<br><small>`log_emis`</small> | `.true.` | Compare emission spectra (`type=emis`) in log space. Turned off automatically with `scaleR`. |
| `doscaler`<br><small>`scaler`</small> | `.false.` | Analytically scale the planet radius to best fit the data in each likelihood evaluation. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `nscaler` | -1 | Number of points used for the radius scaling. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `massprior` | `.false.` | Apply a Gaussian prior on the planet mass (`Mp_prior`, `dMp_prior`; set automatically from the planet database). |
| `mp_prior` | — | Mean of the mass prior. <small>[M<sub>Jup</sub>]</small> |
| `dmp_prior` | — | Width of the mass prior. <small>[M<sub>Jup</sub>]</small> |
| `radprior` | `.false.` | Apply a Gaussian prior on the planet radius. |
| `rp_prior` | — | Mean of the radius prior. <small>[R<sub>Jup</sub>]</small> |
| `drp_prior` | — | Width of the radius prior. <small>[R<sub>Jup</sub>]</small> |
| `rp_range` | 20 | Allowed range of the radius (used in radius scaling). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `randomstart` | `.false.` | Start the optimiser/MCMC from a random point in parameter space. |
| `gene_cross` | `.false.` | Use cross-over in the genetic algorithm. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `nboot` | 1 | Number of bootstrap iterations for the optimal-estimation retrieval. |
| `faircoverage` | `.false.` | Down-weight wavelength regions covered by many data points so each spectral region contributes fairly. |
| `speclimits` | `.true.` | Write 1σ/2σ/3σ confidence limits of spectra after a retrieval. |
| `par3d` | — | Parameters varying over the planet in 3D retrievals. See `par3dN:` sub-keywords below. |
| `par3dsteepness`<br><small>`steepness3d`</small> | 0.0001 | Steepness of the transition between day- and nightside values of 3D parameters. |
| `mapcoratio` | — | Map retrieved C/O to atomic abundances without chemistry (in AI/retrieval output). <span class="review" title="Inferred from the code, to be checked">✎</span> |

## 3D models and phase curves

| Keyword | Default | Description |
|---|---|---|
| `do3d`<br><small>`run3d`</small> | `.false.` | Compute a 3D (pseudo-3D) model using the β-map (Chubb & Min 2022). |
| `n3d` | 10 | Number of 1D models (β-values) used to build the 3D planet. |
| `nlong` | 36 | Number of longitude cells. |
| `nlatt` | 19 | Number of latitude cells. |
| `night2day` | 0.5 | Day-to-night heat redistribution efficiency. |
| `fixnight2day`<br><small>`fixn2d`</small> | `.false.` | Compute `night2day` from a physical estimate instead of using the value given. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `pole2eq` | 1 | Pole-to-equator redistribution. |
| `hotspotshift` | -1e+05 | Shift of the hot spot in longitude (degrees). Default: computed from the wind. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `tidallock` | `.true.` | Assume a tidally locked planet. |
| `fday` | 1 | Fraction of the dayside that is irradiated. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `kxx` | 1 | Diffusion coefficient in longitude for the β-map. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `kyy` | 1 | Diffusion coefficient in latitude for the β-map. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `vxx` | 0 | Advection velocity in longitude for the β-map. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `powvxx`<br><small>`powv`, `vxx_pow`</small> | 0 | Latitude dependence of `vxx`. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `deepredist` | `.false.` | Redistribute heat in the deep atmosphere (only with `do3D`). |
| `deepredisttype` | `fixbeta` | Type of deep redistribution: `fixbeta` or `fixflux`. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `nalbedo_iter` | 1 | Number of albedo iterations ensuring energy conservation with day/night albedo differences (see [Albedo iteration](../theory/albedo-iteration.md)). |
| `phase` | — | Phase angle(s) for which emission spectra are computed: `phase1=180`, `phase2=90`, … (degrees; 180 = full dayside). |
| `nnu`<br><small>`nnustar`</small> | 10 | Number of frequencies for the stellar irradiation angles in 3D. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `output3d` | `.false.` | Write the full 3D structure output. |
| `readfull3d` | `.false.` | Read a full 3D structure (e.g. from a GCM) instead of the β-map. Requires `nlong × nlatt` 1D models. |
| `full3ddir`<br><small>`dirfull3d`</small> | — | Directory with the 3D structure files (sets `readFull3D=.true.`). |
| `makeimage` | `.false.` | Make an image of the planet. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `makemovie` | `.false.` | Make a sequence of images for a movie (implies `makeimage`). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `computelc` | `.false.` | Compute a light curve. <span class="review" title="Inferred from the code, to be checked">✎</span> |

## Planet formation link

| Keyword | Default | Description |
|---|---|---|
| `planetform` | `.false.` | Set the elemental composition from a planet formation model (SimAb, Khorshid et al. 2022). |
| `fdust` | 0.1 | Fraction of solids accreted. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `fplanet` | 0.1 | Fraction of planetesimals accreted. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `dmigrate` | 15 | Migration distance. <small>[AU]</small> |
| `rendmigrate` | -1 | Final orbital distance after migration (default: `Dplanet`). <small>[AU]</small> |
| `rstart`<br><small>`rcore`</small> | 15 | Deprecated: old way to set the formation location. Use `dmigrate`/`rendmigrate`. <small>[AU]</small> |
| `mstart`<br><small>`mcore`</small> | 10 | Initial core mass. <small>[M<sub>⊕</sub>]</small> |
| `sootline`<br><small>`solidc`, `fsolidc`</small> | 0 | Fraction of refractory carbon (soot line). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `mdotdisk` | 1e-07 | Disk accretion rate. <small>[M<sub>☉</sub>/yr]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `hydrogenloss` | 1 | Fraction of hydrogen retained (atmospheric escape). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `outflow` | `.false.` | Include an outflowing upper atmosphere. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `vfrag` | 1e+200 | Fragmentation velocity of cloud particles in the coagulation. <small>[cm/s]</small> |

## Rings and exozodi

| Keyword | Default | Description |
|---|---|---|
| `doring` | `.false.` | Add a ring around the planet. |
| `rring` | 1.5 | Inner radius of the ring. <small>[R<sub>p</sub>]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `drring` | 2 | Width of the ring. <small>[R<sub>p</sub>]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `tauring` | 0.5 | Optical depth of the ring. |
| `exozodi` | 3 | Exozodi level (in zodis) for the HWO noise estimate. |

## Clouds

| Keyword | Default | Description |
|---|---|---|
| `cloud` | — | Define cloud layers with `cloudN:` sub-keywords; see [Clouds](../user-guide/clouds.md) and the [`cloudN:` sub-keywords](#cloudn-sub-keywords). |
| `particledir`<br><small>`dirparticle`</small> | `./Particles/` | Directory for cached particle opacity files. <span class="review" title="Inferred from the code, to be checked">✎</span> |

## Instrument simulation

| Keyword | Default | Description |
|---|---|---|
| `instrument` | — | Rough noise simulation, see [`instrumentN:` sub-keywords](#instrumentn-sub-keywords) and [Instrument simulation](../user-guide/instrument-simulation.md). |

## Deprecated or without effect

| Keyword | Default | Description |
|---|---|---|
| `cutoff`<br><small>`cutoff_lor`</small> | 1e+200 | Line-wing cut-off for opacity computations from line lists (no longer done in ARCiS). <span class="unused" title="Parsed by Init.f but not used anywhere else in the code">no effect</span> |
| `cutoff_abs` | 1e+200 | Absolute line-wing cut-off (no longer used). <span class="unused" title="Parsed by Init.f but not used anywhere else in the code">no effect</span> |
| `eps`<br><small>`epsck`</small> | 0.25 | Accuracy parameter for the correlated-k tables (no longer used). <span class="unused" title="Parsed by Init.f but not used anywhere else in the code">no effect</span> |
| `epslines`<br><small>`eps_lines`</small> | 0 | Line strength threshold (no longer used). <span class="unused" title="Parsed by Init.f but not used anywhere else in the code">no effect</span> |
| `tiscale` | 1 | Scaling of the Ti abundance (currently not used). <span class="unused" title="Parsed by Init.f but not used anywhere else in the code">no effect</span> |
| `sinkz` | `.false.` | Sinking of heavy elements (currently not used). <span class="unused" title="Parsed by Init.f but not used anywhere else in the code">no effect</span> |
| `alphaz` | 1 | Parameter of `sinkZ` (currently not used). <span class="unused" title="Parsed by Init.f but not used anywhere else in the code">no effect</span> |
| `nspike` | 0 | Currently not used. <span class="unused" title="Parsed by Init.f but not used anywhere else in the code">no effect</span> |
| `chimax`<br><small>`chi2max`</small> | 1 | Currently not used. <span class="unused" title="Parsed by Init.f but not used anywhere else in the code">no effect</span> |
| `3daim`<br><small>`aim3d`</small> | `CONTRAST` | Aim of the 3D setup (currently not used). <span class="unused" title="Parsed by Init.f but not used anywhere else in the code">no effect</span> |
| `betapow` | 1 | Power of the β-map (currently not used). <span class="unused" title="Parsed by Init.f but not used anywhere else in the code">no effect</span> |
| `maxchemtime` | 1e+200 | Maximum time for the chemistry computation (currently not used). <span class="unused" title="Parsed by Init.f but not used anywhere else in the code">no effect</span> |
| `trend_compute`<br><small>`dotrend`</small> | `.false.` | Currently not used. <span class="unused" title="Parsed by Init.f but not used anywhere else in the code">no effect</span> |
| `compute` | — | No longer supported; prints a message and is ignored. |
| `nphase` | — | No longer supported; use `phase1`, `phase2`, … |
| `specresdust` | — | No longer in use. |

## cloudN: sub-keywords

Cloud layers are numbered: `cloud1:`, `cloud2:`, … `cloud0:` applies a setting to **all** cloud layers (`cloud:` without a number means `cloud1:`). Per-material keywords take a second index, e.g. `cloud1:abun02=0.3`. A molecule name as sub-keyword (e.g. `cloud1:H2O=…`) sets the condensation ratio of that species.

| Keyword | Default | Description |
|---|---|---|
| `cloudN:type` | *(empty)* | Cloud type: `CONDENSATION`, `DIFFUSE`, `WATER`, `FILE`, `FILEDRIFT`, `LAYER`, `SLAB`, `DECK`, `GAUSS`, `HALFGAUSS`, `HOMOGENEOUS`, `RING`. See [Clouds](../user-guide/clouds.md). |
| `cloudN:opacitytype` | `AUTO` | `PARAMETERISED`, `REFIND`, `MATERIAL`, `FILE`, `OPACITY`, or `AUTO` (`MATERIAL` for condensation clouds). |
| `cloudN:fixcloud` | 0 | Keep the cloud structure fixed after iteration *n*. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:file` | — | File with the cloud structure (`FILE`/`FILEDRIFT` types) or opacities. |
| `cloudN:fmax` | 0 | Irregularity parameter of the DHS particle shape model; 0 = homogeneous spheres (Mie). |
| `cloudN:blend` | `.true.` | Mix materials with effective medium theory (otherwise separate particles). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:porosity` | 0 | Porosity of the cloud particles. |
| `cloudN:hazetype` | `SOOT` | Material of the haze/nuclei particles (any built-in material, e.g. `SOOT`, `THOLIN`). |
| `cloudN:pressure`<br><small>`cloudN:p`</small> | 0.0001 | Pressure of maximum nucleation (`CONDENSATION`/`DIFFUSE`) or centre of a `GAUSS` cloud. <small>[bar]</small> |
| `cloudN:dp` | 10 | Width of the nucleation profile or `GAUSS` cloud (factor in pressure). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:ptop` | 0 | Top pressure of the cloud. <small>[bar]</small> |
| `cloudN:pbottom` | 1e+10 | Bottom pressure of the cloud. <small>[bar]</small> |
| `cloudN:ptau` | 1 | Pressure where the cloud reaches optical depth `tau` at `lam_ref` (`LAYER`, `DECK`). <small>[bar]</small> |
| `cloudN:prel`<br><small>`cloudN:prelative`</small> | `.false.` | Interpret `Pbottom` relative to the bottom of the atmosphere and `Ptop`/`Ptau` relative to `Pbottom`. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:xi` | 2 | Power-law of the cloud opacity with pressure (`LAYER`, `GAUSS`). |
| `cloudN:dlogp` | 2 | Pressure scale Φ over which a `DECK` cloud falls off. |
| `cloudN:tau` | 1 | Optical depth of the cloud at `lam_ref`. |
| `cloudN:lam_ref` | 1 | Reference wavelength for `tau`. <small>[µm]</small> |
| `cloudN:lam_kappa` | 1 | Transition wavelength λ<sub>0</sub> from grey to power law. <small>[µm]</small> |
| `cloudN:pow_kappa` | 4 | Power p of the parameterised opacity. |
| `cloudN:albedo` | 0.99 | Single scattering albedo of the parameterised opacity. |
| `cloudN:g` | — | Asymmetry parameter (Henyey–Greenstein) for `OPACITY`-type clouds. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:kappa_gauss` | 0 | Strength of an added Gaussian absorption feature. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:lam_gauss` | 7 | Central wavelength of the Gaussian feature. <small>[µm]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:dlam_gauss` | 0.2 | Width of the Gaussian feature. <small>[µm]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:rnuc` | 0.001 | Radius of the nuclei / smallest particles. <small>[µm]</small> |
| `cloudN:rnuc_phot` | 0.001 | Radius of photochemical haze nuclei. <small>[µm]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:pref` | 1 | Reference pressure P<sub>ref</sub> of the radius power law. <small>[bar]</small> |
| `cloudN:pow_rad` | 0 | Power γ of the radius variation with pressure: r<sub>eff</sub> = r<sub>nuc</sub> + r<sub>eff,0</sub>(P/P<sub>ref</sub>)<sup>γ</sup>. |
| `cloudN:n` | 1.5 | Real part of the refractive index (`REFIND`). |
| `cloudN:k` | 0.01 | Imaginary part of the refractive index (`REFIND`). |
| `cloudN:composition` | — | Composition string of the cloud. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:coverage` | 1 | Fraction of the planet covered by this cloud (patchy clouds). |
| `cloudN:haze` | `.false.` | Include the cloud nuclei (haze) in mass and opacity. |
| `cloudN:condensates` | `.true.` | Compute the condensates (set `.false.` for a pure haze cloud, `DIFFUSE` type). |
| `cloudN:condensenak`<br><small>`cloudN:naksilicates`</small> | `.true.` | Allow Na and K to condense into silicates. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:freeflow_nuc` | `.true.` | Free-flow lower boundary for nuclei instead of x<sub>n</sub> = 0. |
| `cloudN:freeflow_con` | `.true.` | Free-flow lower boundary for condensates instead of full evaporation. |
| `cloudN:computejn` | `.false.` | Compute the nucleation rate from classical nucleation theory instead of using `SigmaDot`. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:globalgasmix` | `.false.` | Use the global gas mixing for the condensable gas. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:mixrat` | 0 | Mass mixing ratio of cloud particles (`HOMOGENEOUS`). |
| `cloudN:kzz` | -1 | K<sub>zz</sub> for this cloud when `globalKzz=.false.`. <small>[cm² s⁻¹]</small> |
| `cloudN:globalkzz` | `.false.` | Use the global K<sub>zz</sub> profile of the atmosphere for this cloud. |
| `cloudN:sigmadot`<br><small>`cloudN:nucleation`</small> | 1e-17 | Nucleation rate (column-integrated) for `CONDENSATION`/`DIFFUSE` clouds. <small>[g cm⁻² s⁻¹]</small> |
| `cloudN:sigmadot_phot`<br><small>`cloudN:nuc_phot`</small> | 1e-17 | Nucleation rate of photochemical haze nuclei. <small>[g cm⁻² s⁻¹]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:xm_bot` | 0 | Mass mixing ratio of condensable material at the bottom boundary. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:reff` | 1 | Effective radius r<sub>eff,0</sub> of the size distribution (parameterised clouds). <small>[µm]</small> |
| `cloudN:veff` | 0.1 | Effective width v<sub>eff</sub> of the size distribution. |
| `cloudN:ns`<br><small>`cloudN:nsize`</small> | 1 | Number of particle sizes in the size distribution. |
| `cloudN:kappa` | 0.01 | κ<sub>0</sub> of the `PARAMETERISED` opacity. <small>[cm² g⁻¹]</small> |
| `cloudN:fstick` | 1 | Sticking efficiency in coagulation. |
| `cloudN:df`<br><small>`cloudN:fractaldim`</small> | 3 | Fractal dimension of aggregates. |
| `cloudN:rainout` | `.false.` | Remove material that is thermally stable at the bottom of the atmosphere from the gas. |
| `cloudN:srainout`<br><small>`cloudN:sat_bot`</small> | 1 | Saturation ratio at the bottom above which material is rained out. |
| `cloudN:computecryst` | `.false.` | Compute the crystallinity of silicates (`DIFFUSE`). |
| `cloudN:coagulation` | `.true.` | Include coagulation of cloud particles. |
| `cloudN:eqchemboundary` | `.false.` | Use equilibrium chemistry abundances as lower boundary condition (requires `chemistry=.true.`). |
| `cloudN:usefsed` | `.false.` | Use an f<sub>sed</sub> parameterisation (Rooney et al. 2022) for the sedimentation instead of the microphysics. |
| `cloudN:alpha`<br><small>`cloudN:fsed_alpha`, `cloudN:fsed`</small> | 1 | f<sub>sed</sub> value (alias `fsed`). |
| `cloudN:beta`<br><small>`cloudN:fsed_beta`</small> | 1e+20 | Pressure dependence of f<sub>sed</sub>. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:cryst` | 1 | Fixed crystallinity of silicates when `computecryst=.false.`. |
| `cloudN:x_slider` | 0 | Continuous mixing between materials: a value x between i and i+1 mixes material i and i+1 (for retrievals). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:abun` | 1 | Abundance of material *n* in the mixture. |
| `cloudN:xv_bot` | 1e-05 | Volume mixing ratio of condensate *n* at the bottom boundary. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `cloudN:rho_mat` | 3 | Material density of material *n*. <small>[g cm⁻³]</small> |
| `cloudN:material` | `AUTO` | Built-in material *n* (`MATERIAL` opacity), or a refractive index file. |
| `cloudN:condensate` | `SILICATE` | Condensate species *n* for `CONDENSATION` clouds, e.g. `cloud1:condensate01="MgSiO3"`. Without a number it is appended to the list. |
| `cloudN:lnkfile` | *(empty)* | Refractive index file *n* (λ [µm], n, k). |
| `cloudN:lnkfilex` | *(empty)* | Refractive index file *n* for the x crystal axis (also `lnkfiley`, `lnkfilez`). |
| `cloudN:lnkfiley` | *(empty)* | Refractive index file *n* for the y crystal axis. |
| `cloudN:lnkfilez` | *(empty)* | Refractive index file *n* for the z crystal axis. |

## obsN: sub-keywords

Observations are numbered `obs1:`, `obs2:`, …

| Keyword | Default | Description |
|---|---|---|
| `obsN:type` | — | Type of observation: `trans` (R<sub>p</sub>²/R<sub>*</sub>²), `emis` (flux, Jy), `emisR` (F<sub>p</sub>/F<sub>*</sub>), `phase`/`phaseR` (phase curve), `transC`/`transM`/`transE`, `lightcurve`, `tprofile`/`logtp`, `prior`. |
| `obsN:file` | — | File with the observed spectrum. Columns: wavelength [µm], value, error, and optionally spectral resolution R and the bin-shape exponent (see [Observations](../user-guide/retrieval.md#observation-files)). |
| `obsN:filter` | *(empty)* | File with filter transmission curves to convolve the model with (photometry). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `obsN:beta`<br><small>`obsN:weight`</small> | 1 | Weight of this observation in the likelihood (errors are divided by `beta`). |
| `obsN:scaling`<br><small>`obsN:scale`</small> | `.false.` | Fit a multiplicative scaling of this data set. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `obsN:fscale` | 1 | Fixed multiplicative scaling factor of this data set. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `obsN:dscale`<br><small>`obsN:sigscale`</small> | -1 | Prior width on the scaling. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `obsN:iphase` | 1 | Index of the phase angle (`phaseN`) this emission observation corresponds to. |
| `obsN:slope` | 0 | Linear slope added to the data. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `obsN:offset` | 0 | Offset added to the data. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `obsN:adderr` | 0 | Extra error added to this data set. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `obsN:c_l`<br><small>`obsN:cov_l`</small> | 1e-06 | Correlation length of the correlated noise kernel. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `obsN:c_a`<br><small>`obsN:cov_a`</small> | 0 | Amplitude of the correlated noise. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `obsN:c_b`<br><small>`obsN:cov_b`, `obsN:cov_offset`, `obsN:c_offset`</small> | 0 | Covariance term for a constant offset. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `obsN:c_s`<br><small>`obsN:cov_s`, `obsN:cov_scaling`, `obsN:c_scaling`, `obsN:cov_scale`, `obsN:c_scale`</small> | 0 | Covariance term for a scaling. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `obsN:cov_a_loc` | — | Amplitude of localised correlated noise component *n* (`obs1:cov_a_loc2=…`). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `obsN:cov_l_loc` | — | Correlation length of localised component *n*. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `obsN:cov_lam_loc` | — | Central wavelength of localised component *n*. <span class="review" title="Inferred from the code, to be checked">✎</span> |

## fitpar: sub-keywords

Retrieval parameters are not numbered: every `fitpar:keyword=` starts a new parameter and the following `fitpar:` lines apply to that parameter.

| Keyword | Default | Description |
|---|---|---|
| `fitpar:keyword`<br><small>`fitpar:parameter`</small> | — | Keyword to retrieve. Starts a new retrieval parameter; the following `fitpar:` lines apply to it. `tprofile` sets up a free temperature profile. |
| `fitpar:min`<br><small>`fitpar:xmin`</small> | 0 | Lower bound of the prior. |
| `fitpar:max`<br><small>`fitpar:xmax`</small> | 1 | Upper bound of the prior. |
| `fitpar:init`<br><small>`fitpar:x`</small> | -1e+200 | Initial value (default: centre of the range, or the value set in the input file). |
| `fitpar:spread`<br><small>`fitpar:width`, `fitpar:dx`</small> | -1 | Width of a Gaussian prior (used with an `obs` of type `prior`). <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `fitpar:log`<br><small>`fitpar:logscale`</small> | `.false.` | Sample the parameter logarithmically. |
| `fitpar:square`<br><small>`fitpar:squarescale`</small> | `.false.` | Sample uniformly in the square of the parameter. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `fitpar:opacity`<br><small>`fitpar:opacitycomp`</small> | `.true.` | Changing this parameter requires recomputing the opacities. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `fitpar:increase` | `.false.` | Force this parameter to be larger than the previous one. <span class="review" title="Inferred from the code, to be checked">✎</span> |

## instrumentN: sub-keywords



| Keyword | Default | Description |
|---|---|---|
| `instrumentN:name` | — | `ARIEL`, `JWST`, `MIRI`, `NIRSPEC`, `WFC3`, `HWO`, or a file name with an ExoSim-format instrument simulation. |
| `instrumentN:ntrans` | — | Number of transits. With 0, the number of transits is chosen such that 7 scale heights are detected at 5σ at each wavelength. |
| `instrumentN:tint` | — | Integration time. <small>[hours]</small> |
| `instrumentN:nobs`<br><small>`instrumentN:nr`</small> | — | Index of the observation this instrument is linked to. <span class="review" title="Inferred from the code, to be checked">✎</span> |

## par3dN: sub-keywords



| Keyword | Default | Description |
|---|---|---|
| `par3dN:keyword`<br><small>`par3dN:parameter`</small> | — | Keyword that varies across the planet. |
| `par3dN:min`<br><small>`par3dN:xmin`</small> | — | Value on the nightside. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `par3dN:max`<br><small>`par3dN:xmax`</small> | — | Value on the dayside. <span class="review" title="Inferred from the code, to be checked">✎</span> |
| `par3dN:log`<br><small>`par3dN:logscale`</small> | `.false.` | Interpolate logarithmically. |
| `par3dN:relative`<br><small>`par3dN:multiply`</small> | `.false.` | Values are multiplicative factors of the 1D value. <span class="review" title="Inferred from the code, to be checked">✎</span> |

## fixmolN: sub-keywords



| Keyword | Default | Description |
|---|---|---|
| `fixmolN:name` | — | Name of the molecule to fix. |
| `fixmolN:abun` | — | Fixed volume mixing ratio. |
| `fixmolN:p` | — | Fix only at pressures below this value. <small>[bar]</small> <span class="review" title="Inferred from the code, to be checked">✎</span> |

## orbit: sub-keywords



| Keyword | Default | Description |
|---|---|---|
| `orbit:p` | -1 | Orbital period (default from Kepler's third law). <small>[s]</small> |
| `orbit:e` | 0 | Eccentricity. |
| `orbit:omega` | 0 | Argument of periastron. <small>[deg]</small> |
| `orbit:inc` | 90 | Inclination. <small>[deg]</small> |
