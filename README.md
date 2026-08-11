# Fixed-Response-Operational-Synthesis

Repository-ready research starter for the question:

> Given a fixed complete detector-facing response and fixed baseline output noise, what output-field information/covariance-correlation tangents are physically realizable for the same declared signal, and what is the minimal open-system realization of each reachable boundary point?

## Status

**Repository creation gate: GO WITH CLAIM RESTRICTION.**

This is not yet a PRL-novelty PASS. The repository exists to test a sharply delimited inverse-synthesis problem.

## What is already established

- **W0 PASS**: a fixed monitored transfer admits a nontrivial noise-information design set in a passive Gaussian witness.
- **W1 PASS**: the freedom survives removal of internal-state realization gauge; deterministic `A` and monitored coupling are literally identical.
- **W2 blocking PASS**: displacement-only passive Gaussian QFI collapses to a functional of baseline covariance, so a naive joint `(noise,QFI)` body is not an independent object.
- **W3 PASS**: same complete baseline response, same baseline output noise, and same coherent response derivative can coexist with a ~357x change in output QFI for the same declared signal, through a physically distinct environmental covariance tangent.

## Claim boundary

Do **not** claim novelty for:

- same response but different noise;
- same baseline but different QFI;
- transfer-function realization;
- power-spectrum identification;
- Gaussian QFI depending on covariance tangents;
- `C^† N C` compression itself;
- reservoir engineering in general.

The surviving target is the **physical realizability and constructive synthesis of admissible parameter tangents under fixed response/noise/resource constraints**, including missing inequalities and minimal realization complexity.

## First blocking gates

1. `W4`: generator-linked signal witness (dissipative-rate or Hamiltonian signal), avoiding bath-temperature-only Rayleigh-quotient absorption.
2. `B0`: test completeness of known fluctuation-response-QFI necessary bounds; search for a target that satisfies known bounds but is not physically realizable.
3. `S0`: minimal-synthesis lower bound and saturating construction for system dimension / environmental channel rank.
4. `X0`: non-Gaussian finite-level GKSL holdout not reducible to Hermitian compression theory.

## Layout

- `code/` executable witnesses
- `results/` frozen JSON certificates
- `gates/` blocking and decision records
- `literature/` repository-blocking novelty audit
- `references/` seed bibliography

## Naming policy

Keep the repository descriptive. Do not promote a theory name or acronym until a general theorem or obstruction survives W4/B0/S0/X0.
