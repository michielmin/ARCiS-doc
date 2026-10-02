# Python interface

ARCiS can be compiled into a Python module, `pyARCiS`, using `f2py`. This lets you
initialise a model from an input file and then change keywords and recompute spectra
from Python — for parameter studies, plotting, or driving your own sampler.

## Building

```bash
make gfort=true multi=true pylib
```

This builds `libARCiS.a`, compiles the module with `numpy.f2py` and installs it with
`pip install -e .` in the source directory. It requires Python 3 with numpy.

## Basic usage

```python
import numpy as np
import matplotlib.pyplot as plt
import pyARCiS

# initialise from an input file; output goes to 'output'
# an optional third argument passes command line options
pyARCiS.pyinit("input.dat", "output")

# arrays sized by ARCiS
lam   = np.empty(pyARCiS.pyex.nlam)
trans = np.empty(pyARCiS.pyex.nlam)
P     = np.empty(pyARCiS.pyex.nr)
T     = np.empty(pyARCiS.pyex.nr)

pyARCiS.pyverbose(False)

for logH2O in np.linspace(-9, -1, 9):
    pyARCiS.pysetvalue("H2O", 10**logH2O)   # set a keyword (numeric value)
    pyARCiS.pycomputemodel()                # compute the model
    pyARCiS.pygettrans(lam, trans)          # fetch the transmission spectrum
    plt.plot(lam, trans)

plt.xscale("log")
plt.show()
```

!!! warning "What can be changed after initialisation"
    Changing **physical parameters** (abundances, radius, mass, chemistry parameters,
    …) and **retrieval parameters** after `pyinit` is fine. Changing parameters that
    define the **setup** (number of layers, chemistry on/off, spectral resolution, …)
    is usually **not**. `pyinit` can only be called once per Python session.

## Functions

f2py exposes the routines in lowercase.

| Function | Description |
|---|---|
| `pyinit(inputfile, outputdir[, cline])` | Initialise ARCiS from an input file. Can only be called once. |
| `pysetkeyword(key, value)` | Set a keyword from two strings, e.g. `pysetkeyword("chemistry", ".true.")` |
| `pysetvalue(key, value)` | Set a keyword to a float value |
| `pycomputemodel()` | Compute the model with the current settings |
| `pywritefiles()` | Write the standard output files to the output directory |
| `pyrunarcis()` | Run ARCiS as from the command line (forward model or retrieval, as set in the input) |
| `pywritebestfit()` | Write the best-fit output |
| `pygetlam(lam)` | Wavelength grid [µm] |
| `pygettrans(lam, trans)` | Transmission spectrum |
| `pygetemis(lam, emis, iphase)` | Emission spectrum at phase index `iphase` |
| `pygetstar(lam, star)` | Stellar spectrum |
| `pygetpt(P, T)` | Pressure–temperature structure |
| `pygetobsn(i)` | Number of data points of observation *i* |
| `pygetobs(i, lam, obs, dobs, model)` | Data, errors and (last retrieval) model of observation *i* |
| `pygetretrievalnames(i)` | Name of retrieval parameter *i* |
| `pytransformretpar(x, i)` | Map a unit-cube value *x* to the value of retrieval parameter *i* |
| `pymapretrieval(var)` | Set all retrieval parameters from a vector of values (log<sub>10</sub> for log-scaled parameters) |
| `pyverbose(flag)` | Switch screen output on or off |
| `pysetoutputmode(flag)` | Switch output mode |

The array sizes are available as `pyARCiS.pyex.nlam`, `pyex.nr`, `pyex.nret` and
`pyex.nobs`.

## Your own retrieval loop

With an input file that defines `fitpar` parameters, the interface provides the prior
transform, so an external sampler only needs a likelihood:

```python
import numpy as np
import pyARCiS

pyARCiS.pyinit("Retrieval.in", "output")
pyARCiS.pyverbose(False)
nret = pyARCiS.pyex.nret
lam   = np.empty(pyARCiS.pyex.nlam)
trans = np.empty(pyARCiS.pyex.nlam)

# your data
lobs, yobs, dyobs = np.loadtxt("WASP-17b_Sing_2015_Nature.dat", usecols=(0, 1, 2), unpack=True)

def prior_transform(cube):
    # unit cube -> parameter values (log10 of the value for log-scaled parameters)
    return np.array([pyARCiS.pytransformretpar(c, i + 1) for i, c in enumerate(cube)])

def loglike(theta):
    pyARCiS.pymapretrieval(np.asarray(theta, dtype=float))
    pyARCiS.pycomputemodel()
    pyARCiS.pygettrans(lam, trans)
    model = np.interp(lobs, lam, trans)   # simple interpolation, no binning
    return -0.5 * np.sum(((yobs - model) / dyobs) ** 2)
```

`pytransformretpar(x, i)` maps a unit-cube value to parameter *i*: uniform between
`min` and `max`, and for `log=.true.` parameters it returns log<sub>10</sub> of the value.
`pymapretrieval` takes these values and sets all keywords.

!!! question "To review"
    * `python/ARCiS_retrieval.ipynb` calls `pyARCiS.pygetlike()`, which does not exist
      in `MainPy.f90`. Either the notebook or the interface needs updating.
    * `pygetobs` returns the model at the data points as stored by the last retrieval
      likelihood evaluation; `pycomputemodel` alone does not seem to update it. A
      `pygetlike`-style function that computes the ARCiS likelihood (with binning and
      covariances) would make external samplers much easier.
