# Input files

An ARCiS input file is a plain text file with one `keyword=value` per line. Everything
ARCiS does is set by these keywords; the full list is in the
[Keyword reference](../reference/keywords.md).

```ini
* comment lines start with * or #
H2O=1d-4
Rp=1.2d0          ! trailing comments after numbers and logicals are fine
chemistry=.true.
planetname='WASP-107b'
cloud1:type='LAYER'
cloud1:tau=10d0
```

## Syntax rules

**Order does not matter, except that the last value wins.** Keywords can appear
anywhere in the file. If a keyword appears more than once, the last occurrence is used.
Command line keywords (`-s key=value`) are read after the file and thus override it.

**Keywords are case-insensitive**: `COratio`, `coratio` and `CORATIO` are the same.
**Molecule names are case-sensitive**: `H2O` sets water, `h2o` stops with *Keyword
not recognised*.

**Unknown keywords stop the run.** ARCiS prints `Keyword not recognised: <key>` (or
`Unknown cloud keyword: <key>`) and stops. This catches typos early.

**Values** are read with Fortran list-directed input:

| Type | Examples |
|---|---|
| Real | `1d-4`, `1e-4`, `0.0001`, `3.5` |
| Integer | `25` |
| Logical | `.true.`, `.false.`, `T`, `F` |
| String | `'WASP-107b'`, `"trans"`, or unquoted `trans` |

Strings may be quoted with single or double quotes; the quotes are stripped.

**Comments.** Lines whose first character is `*` or `#` are comments. A trailing
comment after `!` works for numbers and logicals because Fortran stops reading after the
first value. **Do not put trailing comments after string values** (file names, types,
names): for many of them the comment becomes part of the string, and for quoted strings
the closing quote is no longer recognised.

!!! warning "Indentation"
    A line that starts with a space is silently ignored. Do not indent keywords.

## Indices

A number at the end of a keyword is an index. This is used for lists:

```ini
phase1=180
phase2=90
tauVpoint3=1d-2
```

Leading zeros are allowed (`material01`, `abun02`).

## Sub-keywords

Objects such as clouds, observations and retrieval parameters have their own set of
keywords, written as `object<number>:subkey=value`:

```ini
cloud1:type='CONDENSATION'
cloud1:condensate01='MgSiO3'
cloud1:condensate02='Fe'

obs1:type='trans'
obs1:file='wasp39b_nirspec.dat'
obs2:type='emisR'
obs2:file='wasp39b_miri.dat'
```

Some special cases:

* `cloud0:` applies the setting to **all** cloud layers. Note that `cloud:` without a
  number is the same as `cloud1:`.
* Per-material cloud settings take a second index: `cloud1:abun02=0.3`.
* Molecule-specific settings use the molecule as sub-key: `Pswitch:H2O=1d-2`,
  `trace:CO2=.false.`, `photoreac1:CH4=1`.
* Retrieval parameters (`fitpar:`) are **not numbered**. Each `fitpar:keyword=…` line
  starts a new parameter and the following `fitpar:` lines apply to it:

```ini
fitpar:keyword='metallicity'
fitpar:min=-1
fitpar:max=3

fitpar:keyword='Rp'
fitpar:min=0.8
fitpar:max=1.5
```

## Combining files

Any extra argument on the command line that is not `-o` or `-s` is read as an additional
input file, after the main file. This makes it easy to keep, for example, a planet setup
and a retrieval setup in separate files:

```bash
ARCiS planet.in -o out retrieval_setup.in
```

All files are concatenated into `<outputdir>/input.dat`.

## Order matters for `planetname`

`planetname` is special: the planet and star parameters are read from the database
**at the moment the keyword is processed**. Values set *before* `planetname` are
overwritten by the database, values set *after* it override the database:

```ini
planetname='WASP-107b'
Rp=0.94          ! overrides the database radius
```

## Things that are computed for you

* Planet mass from `loggP` when `loggP` is given (instead of `Mp`).
* Orbital period from Kepler's law when `orbit:P` is not set.
* `kappaUV` from `gammaUV × kappaT` when `gammaUV` is set.
* The number of molecules, clouds, observations and retrieval parameters is counted
  from the input before anything else is read, so arrays are sized automatically.
