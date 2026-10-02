# MCMC computation of the Bayesian evidence

With `retrievaltype='MCMC'` and `computelogZ=.true.`, ARCiS computes the Bayesian
evidence by thermodynamic integration:

\[
\log Z = \int_0^1 \left\langle\log L\right\rangle_\beta \, {\rm d}\beta ,
\]

where \(\left\langle\log L\right\rangle_\beta\) is the average log-likelihood of an MCMC
chain constructed with the tempered probability \(p^\beta\) instead of \(p\).

The integral is computed numerically by sampling β at *N* points (*i* = 1…*N*):

\[
\beta_i=\beta_{\rm min}\left(\frac{1}{\beta_{\rm min}}\right)^{\frac{i-1}{N-1}} .
\]

The weights \(w_i\) follow from the trapezoidal rule for the integral over β from 0 to 1.

The uncertainty on \(\log Z\) is

\[
\sigma_{\log Z}^2={\rm Var}(\log Z) = \sum_{i=1}^N w_i^2\,
\frac{{\rm Var}_\beta(\log L)}{N_{\rm post}} ,
\]

where \(N_{\rm post}\) is the number of samples in the posterior chain (`npost`).
