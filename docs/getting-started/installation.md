# Installation

## Requirements

| Requirement | Notes |
|---|---|
| Fortran compiler | `gfortran` or Intel `ifort`. Other compilers may work but are not tested. |
| [cfitsio](https://heasarc.gsfc.nasa.gov/fitsio/) | Reading and writing binary FITS files (opacity tables). |
| LAPACK | Linear algebra (`-llapack`). |
| [MultiNest](https://github.com/JohannesBuchner/MultiNest) | Needed for Bayesian retrievals. Can be left out with `multinest=false`. |
| ARCiS data files | Opacities, refractive indices, CIA, stellar spectra, planet database. See [Data files](#data-files). |
| Python 3 + numpy *(optional)* | Only for the Python interface (`make pylib`). |

## Installing the dependencies

=== "macOS (Homebrew)"

    ```bash
    brew install gcc cfitsio cmake
    ```

=== "Linux (Debian/Ubuntu)"

    ```bash
    sudo apt install gfortran libcfitsio-dev liblapack-dev cmake
    ```

Next, build and install MultiNest:

```bash
git clone https://github.com/JohannesBuchner/MultiNest.git
cd MultiNest/build
cmake ..
make
sudo make install
```

## Building ARCiS

```bash
mkdir ARCiS; cd ARCiS
git clone https://github.com/michielmin/ARCiS.git ./src
cd src
make gfort=true multi=true
```

This creates the `ARCiS` executable. Put it somewhere on your `PATH`, or use
`make install`, which moves it to `$HOME/bin`.

### Build options

Options are passed to `make` as `option=value`:

| Option | Effect |
|---|---|
| `gfort=true` | Use `gfortran` (default compiler is `ifort`). |
| `multi=true` | Enable OpenMP parallelisation (recommended). |
| `multinest=false` | Build without MultiNest (no nested-sampling retrievals). |
| `debug=true` | Debug build with bounds checking and backtraces. |
| `prof=true` | Profiling flags. |
| `mcmc=true` | Link the external `mcmcrun` library (macOS only). |

Other targets: `make clean` removes object files, `make pylib` builds the
[Python interface](../user-guide/python.md).

!!! note "Library locations"
    The Makefile looks for cfitsio in `/opt/homebrew/lib` (Apple Silicon Homebrew) and
    for other libraries in `$HOME/lib`, `/usr/local/lib` and `/usr/local/modules`. If your
    libraries live elsewhere, adjust `LIBS_FITS` and `LIBS` in the `Makefile`.

!!! warning "CPU-specific flags"
    With `gfort=true` on Linux the code is compiled with `-march=haswell`. On older CPUs
    or on clusters with mixed hardware, change this flag in the `Makefile`.

## Data files

ARCiS expects its data in `$HOME/ARCiS/Data/`. The data can be downloaded from
[exoclouds.com](http://www.exoclouds.com); contact the developers for access.

| Directory / file | Contents |
|---|---|
| `Opacities/` | Molecular opacity tables (FITS, k-tables and cross sections). Can be changed with `opacitydir`. |
| `refind/` | Refractive indices of cloud materials. |
| `CIA/` | Collision-induced absorption (HITRAN `.cia` format). |
| `Surface/` | Surface reflectance spectra (water, ice, snow, grass, sand). |
| `EOS/` | Equation-of-state tables (for `useEOS`). |
| `latex/` | Reference list used to write `refs.tex` with the papers to cite for each run. |
| `allplanets-ascii.txt` | Planet database for `planetname`. |

When new features are added (e.g. new condensates), the data directory may need to be
updated as well.

## Pre-installed versions

### University of Groningen (Kapteyn)

ARCiS is installed on the Kapteyn computers. You only need to link the shared data
directory once:

```bash
cd
mkdir ARCiS
cd ARCiS
ln -s /dataserver/users/formingworlds/ARCiSData ./Data
```

After that, load ARCiS with

```bash
module load ARCiS
```

The version of ARCiS used is printed at the top of `log.dat` for every run.
