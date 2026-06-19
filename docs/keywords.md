### 5. `docs/keywords.md`

# Keywords

There are many keywords for a variety of different setups. Below are some very basic setups discussed.

## Base Properties

| Keyword      | Description                                      |
|---------------|--------------------------------------------------|
| Rp            | Radius of the planet in Jupiter radii.           |
| Mp            | Mass of the planet in Jupiter masses.            |
| Pp            | Atmospheric pressure corresponding to radius Rp. |
| Tstar         | Temperature of the host star in K.               |
| Rstar         | Radius of the host star in Solar radii.           |
| distance      | Distance to the system in parsec.                |
| Dplanet       | Distance of the planet to the star in AU.        |
| planetname    | Name of the planet to read from the database.     |

## Grid Setup

| Keyword      | Description                                      |
|---------------|--------------------------------------------------|
| pmin, pmax    | Minimum, maximum pressure considered.            |
| nr            | Number of pressure points.                       |
| lmin, lmax    | Minimum, maximum wavelength considered.         |
| specres       | Spectral resolution R in lambda/dlambda.         |
| specresdust   | Spectral resolution for cloud species.           |

## Abundances of the Molecules

| Keyword         | Description                                      |
|-----------------|--------------------------------------------------|
| H20=1d-4        | Example of setting homogeneous abundances.       |
| chemistry       | Logical determining if chemistry is computed.    |
| condensates     | Logical determining if condensates are included. |
| COratio         | C/O ratio of the atmosphere.                     |
| metallicity     | Metallicity of the atmosphere.                   |

## Opacities and Raytracing

| Keyword         | Description                                      |
|-----------------|--------------------------------------------------|
| cia             | Logical determining if CIA is taken into account.|
| maxtau          | Maximum optical depth considered.                |
| compute         | Logical determining if opacities need recomputing.|
| scattering      | Logical determining if scattering is included.   |
| scattstar       | Logical determining if scattering from star.     |

## Temperature Structure

| Keyword         | Description                                      |
|-----------------|--------------------------------------------------|
| computeT        | Logical determining if temperature is computed. |
| maxiter         | Maximum number of iterations.                    |
| betaT           | Cosine of the angle of incoming radiation.        |
| TeffP           | Effective temperature of the planet.             |
| Tp              | Temperature of the planet at 1 bar.              |
| dTp             | Temperature gradient.                             |

### Retrieval

#### Observations

| Keyword         | Description                                      |
|-----------------|--------------------------------------------------|
| obs1:type       | Can be "trans", "emis", or "emisR".           |
| obs1:file       | Filename with the observation.                    |
| obs1:beta       | Weight of this observation.                      |

#### Parameters

| Keyword         | Description                                      |
|-----------------|--------------------------------------------------|
| fitpar:keyword  | Keyword to be retrieved.                         |
| fitpar:min      | Minimum value considered.                        |
| fitpar:max      | Maximum value considered.                        |
| fitpar:log      | Logical determining if parameter is sampled log. |

