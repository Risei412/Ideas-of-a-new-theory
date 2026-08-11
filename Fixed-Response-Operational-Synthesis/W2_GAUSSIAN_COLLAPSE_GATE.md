# W2 — Gaussian joint-body collapse / compression gate

## Verdict

**PASS as a blocking/collapse gate.**

The W0/W1 passive-Gaussian witness is scientifically valid, but it does **not**
yet justify a standalone repository for a new joint response-noise-QFI
realizability theory.

## 1. Fixed-response environmental-noise realization

For a passive Markov linear system, let the hidden bath coupling be
`C_h` and fix the deterministic hidden damping Gram matrix

    Gamma_h = C_h^† C_h > 0.

For a fixed hidden bath occupation/covariance matrix `N_h`, the injected
normally ordered noise matrix is

    K_h = C_h^† N_h C_h.

Writing

    C_h = U Gamma_h^(1/2),  U^† U = I,

gives the exact representation

    Gamma_h^(-1/2) K_h Gamma_h^(-1/2) = U^† N_h U.

Thus the reachable hidden-noise matrices at fixed deterministic damping are
exactly the Hermitian compressions of `N_h`, followed by congruence with
`Gamma_h^(1/2)`.

This explains W1 without invoking an internal state-space gauge.

## 2. Existing-math absorption

The compression problem `U^† N U` is classical matrix-analysis territory.
Cauchy/Fan-Pall interlacing and higher-rank numerical-range/compression theory
already characterize substantial parts, and in the Hermitian case the inverse
spectral problem is classical.

Therefore the statement

    "fixed damping permits a family of effective noise matrices"

is **not** a novelty candidate by itself.

## 3. QFI collapse in W0/W1

For the W0/W1 signal choice, the parameter changes only the coherent
displacement while the baseline passive Gaussian covariance is `V`.

With fixed detector-facing response, the displacement derivative `d` is fixed.
The Gaussian displacement information used in W0/W1 is

    F_disp = 4 d^† V^(-1) d

(up to quadrature/QFI normalization convention).

Therefore `F_disp` is a deterministic functional of the output covariance.
The joint set `(S_out, F_disp)` is only the graph of `F_disp[S_out]`; it is not
an independent two-object realizability body.

W0/W1 remain useful constructive witnesses, but they do not establish the
stronger target

    same response + same noise, different output-field QFI

or an independently variable `(noise,QFI)` body.

## 4. Repository consequence

A dedicated repository is justified only after one of the following survives:

A. **W3 independence witness**
   Construct two physical finite-dimensional/linear open systems with
   identical complete detector-facing baseline response and identical declared
   output noise spectrum, but different output-field QFI rate for the same
   declared signal.

B. **Completeness/obstruction theorem**
   Prove that known fluctuation-response-QFI inequalities are insufficient for
   physical realizability by exhibiting a target `(R,S,F_Q)` satisfying the
   known bounds but admitting no physical realization, then derive the missing
   constraint.

C. **Non-Gaussian synthesis theorem**
   Move beyond displacement-only passive Gaussian outputs and obtain a
   realizability body involving covariance/correlation tangents or higher
   output statistics that is not reducible to a Hermitian compression problem.

Until A/B/C passes, repository status is **HOLD**, not KILL.
