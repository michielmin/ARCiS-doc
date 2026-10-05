# Tests

The `Tests/` directory contains regression tests: a set of input files with reference
output. `dotest.py` runs ARCiS on each input and compares selected output files with the
reference, column by column, within a relative tolerance.

## Running the tests

ARCiS must be installed and on the `PATH`, with the data files in `$HOME/ARCiS/Data`.

```bash
cd Tests
python dotest.py
```

For each test ARCiS writes its output to `run_<name>/` and prints `PASS` or `FAIL` for
every compared file, with the maximum relative error.

## Test cases

| Name | Input | Compared files | Tolerance | What it tests |
|---|---|---|---|---|
| `TRAPPIST-1b_CO2` | `MalikCO2.dat` | `mixingratios.dat` | 5×10⁻² | Self-consistent T, CO<sub>2</sub> atmosphere on a rocky planet |
| `LHS_3844b_H2O` | `MalikH2O.dat` | `mixingratios.dat` | 5×10⁻² | Self-consistent T, H<sub>2</sub>O atmosphere |
| `SAG26_tau0.1/1.0/10.0` | `SAG26_tau*.in` | `phase` | 10⁻² | Reflected light with anisotropic scattering by a cloud layer (benchmark) |
| `test_read` | `test_read.dat` | `trans`, `emisR`, `mixingratios.dat` | 10⁻⁶ | Reading a structure from file |
| `test1` | `test1.dat` | `trans`, `emisR` | 10⁻⁶ | Hot Jupiter with equilibrium chemistry |
| `test2` | `test2.dat` | `emisR`, `mixingratios.dat` | 10⁻⁶ | As `test1`, with scattering and a 3D setup |
| `Earth` | `Earth.in` | `emisR`, `cloudstructure0010.dat`, `phase` | 10⁻³ | Earth-like planet with water clouds and surface |

## Adding a test

1. Add an input file to `Tests/`.
2. Run it with a trusted version of ARCiS and store the output as
   `Tests/ref_<name>/`.
3. Add an entry to the `tests` list in `dotest.py` with the input file, the reference
   directory, the files to compare and the tolerance.

