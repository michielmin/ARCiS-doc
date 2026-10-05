# Quick start

## Your first model

Create a file `simple.in`:

```ini
* H2/He atmosphere with a few molecules
H2=0.85
He=0.15
H2O=1d-4
CO=1d-5
CH4=1d-5

* planet and star
Rp=1d0          ! Jupiter radii
Mp=1d0          ! Jupiter masses
Pp=10d0         ! pressure at Rp [bar]
Dplanet=0.05    ! AU
Tstar=5777d0
Rstar=1d0

* isothermal atmosphere of 1200 K
TP=1200d0
dTP=0d0

* grids
nr=25
pmin=1d-7
pmax=1d+3
lmin=0.25d0
lmax=5d0
specres=150

```

and run

```bash
ARCiS simple.in -o output
```

The output directory now contains, among others, the transmission spectrum `trans`, the
emission spectrum `emis`, the planet-to-star contrast `emisR` and the atmospheric
structure `mixingratios.dat`. Plot the transmission spectrum with, e.g.,

```python
import numpy as np
import matplotlib.pyplot as plt

lam, depth = np.loadtxt("output/trans", unpack=True)[:2]
plt.plot(lam, depth)
plt.xscale("log")
plt.xlabel("Wavelength [µm]")
plt.ylabel(r"$(R_p/R_\star)^2$")
plt.show()
```

See [Output files](../user-guide/output.md) for all files and their columns.

## Command line

```text
ARCiS <inputfile> [-o <outputdir>] [-s key=value ...] [<extra input files> ...]
```

| Argument | Meaning |
|---|---|
| `<inputfile>` | Input file. Must be the **first** argument. |
| `-o <dir>` | Output directory (created if needed). Default: `./outputARCiS/`. |
| `-s key=value` | Set or override a keyword. Can be repeated. |
| any other argument | Read as an additional input file. |

Keywords are processed in order: first the input file, then the command line arguments
one by one. **The last value encountered wins.** This makes it easy to run variations of a
model without editing the input file:

```bash
ARCiS simple.in -o hot  -s TP=2000
ARCiS simple.in -o wide -s lmax=30 -s specres=50
```

ARCiS copies the input file, followed by the command line keywords, to
`<outputdir>/input.dat`, so every run can be reproduced exactly with

```bash
ARCiS <outputdir>/input.dat -o rerun
```

## Next steps

* Use equilibrium chemistry instead of fixed abundances:
  [Composition and chemistry](../user-guide/chemistry.md).
* Use a realistic temperature profile:
  [Temperature structure](../user-guide/temperature.md).
* Add clouds: [Clouds](../user-guide/clouds.md).
* Fit data: [Retrievals](../user-guide/retrieval.md).
* More complete examples are in the `Example/` directory of the repository, see
  [Examples](examples.md).

!!! tip "Runtime"
    The runtime of a single forward model ranges from ~0.01 s to ~15 minutes,
    depending mostly on the spectral resolution, the number of layers, chemistry,
    self-consistent clouds and temperature computation, and 3D setups.
