# Instrument simulation

ARCiS can produce simulated observations including a rough estimate of the noise as a
function of wavelength.

!!! warning "Use at your own risk"
    This is **not** a replacement for a proper instrument simulation. It only includes
    photon noise and is meant to get a very rough estimate of the expected performance.

Instruments are numbered:

```ini
instrument1:name='NIRSPEC'
instrument1:ntrans=2
instrument2:name='MIRI'
instrument2:ntrans=1
```

| Sub-keyword | Meaning |
|---|---|
| `name` | `ARIEL`, `JWST`, `MIRI`, `NIRSPEC`, `WFC3`, `HWO`, or the name of a file with an instrument simulation in ExoSim format |
| `ntrans` | Number of transits to average. With `ntrans=0` the number of transits is chosen such that at each wavelength 7 scale heights are observed at 5σ |
| `tint` | Integration time [hours] |

For each instrument the files `obs_trans_<name>`, `obs_emis_<name>` and
`obs_emisR_<name>` are written, with columns wavelength [µm], value, error and spectral
resolution R. `obs_trans_noise_<name>` and `obs_emisR_noise_<name>` contain the same
spectra with random noise added. The header lists the transit time, number of transits
and integration time. The format matches the [observation file
format](retrieval.md#observation-files), so the output can be used directly as input for
a test retrieval.

For HWO, the exozodi level (in zodis) is set with `exozodi` (default 3).
