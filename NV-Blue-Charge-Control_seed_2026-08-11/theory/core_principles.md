# Core principles

## DLA side
Global controllability and marked weak-coupling accessibility depth are distinct invariants. The operational target is a fixed full-DLA chamber with different marked perturbative depths.

Synthetic four-level witness:
- two nuclear spin-1/2 qubits;
- full `su(4)` DLA in both parameter settings;
- generic setting: second-order path survives, `d=2`;
- cancellation setting: second-order path cancels while third-order exchange-assisted path survives, `d=3`;
- transition probability scales as `epsilon^4` versus `epsilon^6`.

## Charge-trajectory side
**Charge-transcript completion principle:** if the nuclear Hamiltonian depends on NV charge/electronic state, a stochastic optical charge trajectory induces a transcript-conditioned nuclear operation. The minimum record fidelity, timing precision and feed-forward needed to complete that stochastic process into a reusable nuclear-register operation are constrained by the same charge-dependent hyperfine dynamics.

Minimal first-success coherence factor:

`C(p,phi) = p / [1 - (1-p) exp(-i phi)]`.

Core deletion: `Delta H -> 0`, or `phi -> 0`, removes the transcript-dependent nuclear effect.

## Boundary between programmes
- DLA owns deterministic coherent Hamiltonian geometry.
- TP-16 owns stochastic charge transcript / retry / completion-cost physics.
- Blue-light charge preparation can connect the two experimentally without identifying blue power with the DLA perturbation amplitude.
