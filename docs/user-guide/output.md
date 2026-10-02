# Output files

ARCiS writes its output to the directory given with `-o` (default `./outputARCiS/`). All
text files start with a header line (starting with `#`) describing the columns.

## Always written

| File | Content |
|---|---|
| `log.dat` | Log of the run, including the ARCiS version (git hash) |
| `input.dat` | Copy of the input file(s) followed by the command line keywords. Rerun the exact same model with `ARCiS input.dat -o newdir`. |
| `refs.tex` | LaTeX table with the references to cite for the options used in this run |
| `star` | Stellar flux: λ [µm], flux [Jy] |
| `irradiation` | Stellar irradiance at the planet: λ [µm], W m⁻² µm⁻¹ |
| `mixingratios.dat` | T [K], P [bar] and volume mixing ratios of all molecules per layer |
| `densityprofile.dat` | Radius, height, density, number density, T, … per layer |
| `Kzz.dat` | K<sub>zz</sub> [cm² s⁻¹] versus P [bar] |
| `opticaldepth.dat` | Optical depth of the atmosphere |
| `tau1depth` | Pressure where τ = 1 is reached as a function of wavelength |

## Spectra

| File | Content |
|---|---|
| `trans` | Transmission spectrum: λ [µm], (R<sub>p</sub>/R<sub>⋆</sub>)² |
| `emis` | Emission spectrum: λ [µm], planet flux [Jy] at distance `distance` |
| `emisR` | Planet-to-star contrast: λ [µm], F<sub>p</sub>/F<sub>⋆</sub> |
| `phase` | Emission at all phases `phase<n>` |
| `phasecurve` | Phase curve |
| `trans_split` | Morning, evening and total transmission (3D models) |
| `cloudtau` | Optical depth of the clouds versus wavelength |

When clouds are present, the spectrum files have extra columns for the clear and the
cloudy parts of the atmosphere.

## Optional output

| File | Written when |
|---|---|
| `clouddens01.dat`, … | Clouds are present: cloud density per layer for each cloud |
| `cloudstructure*.dat` | Self-consistent clouds: detailed cloud structure (particle sizes, composition) |
| `trans_hide_<mol>`, `trans_only_<mol>` | `dotranshide=.true.` |
| `contribution*` | `contrib=.true.` |
| `opacity_*` | `outputopacity=.true.` |
| `obs_trans_<instrument>`, … | Instrument simulation (`instrument<n>:name`) |
| `structure3D.dat`, `temp3D_P*`, … | 3D models with `output3D=.true.` |
| `lightcurve` | `computeLC=.true.` |

Retrieval output is described in [Retrievals](retrieval.md#output-of-a-retrieval).

!!! question "To review"
    This list was compiled from the source code (`WriteOutput.f`,
    `SetupStructure.f`, `Retrieval.f`). Please check that the most important files
    and their columns are described correctly, and which files are mainly for
    debugging.

## Reading the output in Python

```python
import numpy as np

# spectra: first column wavelength, second column the spectrum
lam, trans = np.loadtxt("output/trans", unpack=True, usecols=(0, 1))

# structure: header is "# T [K] P [bar] <molecule names>"
with open("output/mixingratios.dat") as f:
    molecules = f.readline().lstrip("#").split()[4:]
data = np.loadtxt("output/mixingratios.dat")
T, P = data[:, 0], data[:, 1]
H2O = data[:, 2 + molecules.index("H2O")]
```

The `python/` and `notebooks/` directories contain example notebooks for plotting
(`PlotARCiS.ipynb`, `PlotCloud.ipynb`).
