# Citing ARCiS

Please cite the paper describing the ARCiS framework in any publication that uses ARCiS:

* Min, M., Ormel, C. W., Chubb, K., Helling, Ch., Kawashima, Y. (2020).
  *The ARCiS framework for exoplanet atmospheres. Modelling philosophy and retrieval.*
  A&A 642, A28. [doi:10.1051/0004-6361/201937377](https://doi.org/10.1051/0004-6361/201937377)

ARCiS contains parts from different developers. Depending on the options you use, please
also cite:

| Component | Reference |
|---|---|
| Cloud formation framework | Ormel & Min (2019), *ARCiS framework for exoplanet atmospheres. The cloud transport model*, A&A 622, A121. [doi:10.1051/0004-6361/201833678](https://doi.org/10.1051/0004-6361/201833678) |
| Optical properties of cloud particles (DHS) | Min, Hovenier & de Koter (2005), A&A 432, 909. [doi:10.1051/0004-6361:20041920](https://doi.org/10.1051/0004-6361:20041920); Toon & Ackerman (1981), Appl. Opt. 20, 3657. [doi:10.1364/AO.20.003657](https://doi.org/10.1364/AO.20.003657) |
| Refractive indices of cloud species | See the references in Min et al. (2020) |
| Molecular opacities | Chubb et al. (2021), *The ExoMolOP database*, A&A 646, A21. [doi:10.1051/0004-6361/202038350](https://doi.org/10.1051/0004-6361/202038350), and references therein |
| MultiNest retrievals | Feroz & Hobson (2008), MNRAS 384, 449. [doi:10.1111/j.1365-2966.2007.12353.x](https://doi.org/10.1111/j.1365-2966.2007.12353.x); Feroz, Hobson & Bridges (2009), MNRAS 398, 1601. [doi:10.1111/j.1365-2966.2009.14548.x](https://doi.org/10.1111/j.1365-2966.2009.14548.x); Feroz et al. (2019), OJAp 2, 10. [doi:10.21105/astro.1306.2144](https://doi.org/10.21105/astro.1306.2144) |
| Equilibrium chemistry (GGchem) | Woitke et al. (2018), A&A 614, A1. [doi:10.1051/0004-6361/201732193](https://doi.org/10.1051/0004-6361/201732193) |
| Disequilibrium chemistry | Kawashima & Min (2021), A&A 656, A90. [doi:10.1051/0004-6361/202141548](https://doi.org/10.1051/0004-6361/202141548) |
| 3D structures and phase curves | Chubb & Min (2022), A&A 665, A2. [doi:10.1051/0004-6361/202142800](https://doi.org/10.1051/0004-6361/202142800) |
| Planet formation (SimAb) | Khorshid et al. (2022), A&A 667, A147. [doi:10.1051/0004-6361/202141455](https://doi.org/10.1051/0004-6361/202141455) |

!!! tip "References for your run"
    Every run writes `refs.tex` to the output directory: a LaTeX table with the
    references for the options and data (e.g. refractive indices) that were actually
    used in that model.

A BibTeX file with these references is in the repository at `doc/refs.bib`.
