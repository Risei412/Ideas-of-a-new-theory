# Next gates

## W4 — Generator-linked signal gate

Replace bath-temperature modulation by a declared signal that changes a GKSL generator parameter (Hamiltonian or dissipative rate). Require:

- same complete baseline detector response;
- same baseline output noise;
- same declared signal resource/activity budget;
- different output-field QFI;
- no internal-state, bath-state, Lindblad-representation, or detector gauge explanation.

PASS only if the effect is not a direct Gaussian tangent/compression corollary.

## B0 — Bound completeness gate

Take the strongest known finite-frequency response-noise-QFI necessary bounds. Search for a target triplet satisfying those bounds but violating physical realizability. Outcomes:

- counterexample -> derive missing inequality/obstruction;
- no counterexample + constructive proof -> sufficiency/completeness theorem;
- standard control theorem already supplies sufficiency -> absorb/kill.

## S0 — Minimal synthesis gate

For an admissible target, determine the minimum:

- internal mode/Hilbert dimension;
- environmental channel rank;
- monitored-channel rank;
- signal-channel activity/resource.

Need both a lower bound and a construction that saturates it.

## X0 — Non-Gaussian holdout

Construct the smallest finite-level GKSL witness where the target cannot be reduced to a Gaussian covariance-compression problem. Prefer qubit/qutrit + two monitored/hidden channels.
