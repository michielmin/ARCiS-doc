# Examples

The repository contains example input files in `Example/` and regression tests in
`Tests/` (see [Tests](tests.md)). The test inputs are run regularly and are
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

