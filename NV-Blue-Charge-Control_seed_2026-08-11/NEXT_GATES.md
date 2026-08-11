# Next gates

## NV-DLA-H1: device-level realizability
Replace synthetic coefficients by measured/credible hyperfine tensors and allowed MW/RF/electron-mediated controls.

PASS:
- both settings remain full `su(4)`;
- a reachable `d=2 -> 3` cancellation exists;
- the probability scaling distinction remains experimentally resolvable with decoherence and finite calibration error.

FAIL:
- cancellation requires unphysical independent matrix elements;
- realistic controls collapse DLA or destroy the marked-depth distinction;
- charge-induced non-Hermitian dynamics cannot be excluded during the DLA measurement window.

## TP-16 N1: quantum-instrument completion theorem
For conditional nuclear Kraus operators `K_r`, characterize when transcript-only unitary correction is possible. A natural exact condition on the protected code is `K_r^† K_r = p_r I` for every accepted record branch. Add:
- charge-state misclassification;
- timestamp error;
- nonunitary jump backaction;
- retry overhead;
- worst-case fidelity bound.

Downgrade/absorb if the result is only a parameter substitution into known feedback/RUS theory and yields no new NV-specific operating boundary.
