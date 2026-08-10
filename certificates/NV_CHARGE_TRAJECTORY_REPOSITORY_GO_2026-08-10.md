# NV Charge-Trajectory Control — Repository Creation Gate

**Date:** 2026-08-10 JST  
**Run:** RCI-20260810-REPO01  
**Verdict:** `GO_CREATE_REPOSITORY`  
**Proposed repository:** `NV-Charge-Trajectory-Control`

## Scope frozen by the gate
The programme is **not** a new general theory of repeat-until-success control, quantum trajectories, measurement feedback, dynamical Lie algebras, or joint-sector accessibility. It is a hardware-constrained NV programme asking for quantitative completion laws when stochastic optical charge trajectories and charge-dependent nuclear dynamics are physically tied together.

## Candidate killed before promotion
The broad claim that monitoring / selecting a charge trajectory creates quantum computational capability beyond the unconditional master equation is rejected. Generic trajectory dependence, unraveling dependence, repeat-until-success protocols, and measurement-based feedback are established frameworks. The surviving candidate is the narrower NV-specific completion-cost problem below.

## Registry-clean constraint residue
Two otherwise standard structures are coupled by NV physics:

1. a heralded first-success charge-control record (attempt count, charge dwell times, charge checks, recharge events), and
2. coherent nuclear-register evolution.

The coupling is forced because the nuclear Hamiltonian depends on NV charge/electronic state. Thus the classical charge transcript is side information about a definite conditional nuclear operation, not merely bookkeeping.

A minimal model writes a failed charge attempt as a known conditional phase `U = exp(-i phi Z/2)` on the stored nuclear qubit. If success occurs independently with probability `p`, the number of failures has `P(n)=p(1-p)^n`.

Discarding the transcript gives the exact coherence factor

`C(p,phi) = p / [1 - (1-p) exp(-i phi)]`.

For `0<p<1` and `phi` not a multiple of `2 pi`, `|C|<1`. Retaining `n` and applying the ideal feed-forward `U^{-n}` restores the coherence to 1 in this minimal model.

The continuous dwell-time analogue for exponential dwell rate `kappa` is

`C = kappa / (kappa + i Delta_omega)`.

These are not claimed as new mathematics. Their role is a minimal witness that charge-record resolution and nuclear fidelity become quantitatively linked once the NV charge dependence is frozen.

## Core principle
**Charge-transcript completion principle:** when the stored nuclear Hamiltonian depends on the NV charge state, a stochastic optical charge trajectory induces a transcript-conditioned nuclear operation; therefore the minimum classical charge information and feed-forward precision required to complete the stochastic process into a reusable nuclear-register operation are constrained by the same charge-dependent hyperfine dynamics.

## Core deletion
Set the charge-conditioned Hamiltonian mismatch to zero on the stored subspace, `Delta H = 0` (minimal phase model: `phi=0`). This preserves the stochastic retry process but removes the physical coupling between the charge transcript and nuclear operation.

## Cheapest core-dependent consequence
With `Delta H != 0`, discarding the retry transcript produces `|C|<1`, while ideal transcript-aware feed-forward restores unit coherence in the minimal unitary-backaction model. Under the deletion `Delta H=0`, both protocols give `C=1`; the transcript advantage disappears.

## Non-vacuous falsification control
`nv_charge_transcript_retry_witness.py` checks the exact geometric-series expression and verifies numerically that `phi=0` gives unit coherence for several success probabilities. It also reports illustrative timing-resolution bounds for Gaussian timestamp error,

`sigma_t <= sqrt[-2 ln(c_target)] / |Delta_omega|`.

The numerical 80 Hz example is illustrative only and is not a fitted device claim.

## Internal absorption map
- **DLA-Constrained Perturbative Depth Geometry:** absorbs deterministic switched-Hamiltonian / perturbative-depth claims. It does not own stochastic first-success transcript completion costs.
- **RISEI / SMRT:** absorb generic intervention-, sector-, and path-resolved response language. They do not by themselves supply an NV charge-readout / timing / retry-cost theorem.
- **VOCG:** generic nonfactorizable joint accessibility is already internally absorbed and is not claimed here.
- **RQ-62 stopped-operation completion:** kills the general completion framework but explicitly leaves a narrow residue requiring heralded first-success semantics, persistent retry memory, hardware-constrained grammars, and a quantitative completion cost. This programme instantiates that residue in NV charge physics.
- **RQ-74 charge-switch memory protection:** generic charge-path-independent memory protection is killed and is not revived here.

## External absorption boundary
Known work already covers NV charge-state control, spin-to-charge conversion, nuclear memories surviving optical resets / charge cycles, general repeat-until-success protocols, quantum trajectories, and measurement-feedback control. The programme therefore makes no priority claim on those ingredients.

The external residue to test is quantitative and hardware-specific: derive and experimentally parameterize the minimum charge-record fidelity, timing resolution, retry overhead, and allowable nonunitary backaction needed for transcript-aware completion of NV charge excursions on a nuclear register.

## Repository creation rule audit
1. **Internal absorption before large computation:** PASS.
2. **Registry-clean constraint residue:** PASS — charge transcript and nuclear operation are tied by charge-dependent hyperfine dynamics.
3. **Declared core-deletion operation:** PASS — `Delta H -> 0`.
4. **Cheapest consequence fails under deletion:** PASS — transcript-induced dephasing / correctability split vanishes.
5. **Non-vacuous falsification control:** PASS — analytic identity plus executable minimal witness.
6. **Explicit non-claims:** PASS.

## Repository GO sign
`GO_CREATE_REPOSITORY = PASS`

This GO authorizes a dedicated **development and falsification repository**. It does **not** certify PRL/PRX novelty or manuscript readiness.

## First repository spine
- `theory/`: discrete first-success theorem, continuous dwell-time resolvent, multi-axis / multi-nuclear extensions.
- `witness/`: analytic and numerical minimal models.
- `device_models/`: NV-/NV0 charge-dependent nuclear Hamiltonians and optical charge-cycle models.
- `completion_cost/`: charge-readout error, timestamp resolution, retry overhead, feed-forward cost.
- `benchmarks/`: parameters and observable protocols tied to primary NV literature.
- `absorption_audit/`: RUS, trajectory feedback, process-tensor / comb, DLA, RISEI / SMRT boundaries.
- `negative_results/`: deterministic-switch absorption and failed novelty routes.
- `construction_history.md`: this gate sequence and future verdict changes.

## Immediate post-GO gates
1. Generalize the scalar phase witness to a quantum instrument with nonunitary charge backaction and determine when transcript-only unitary correction is possible.
2. Add finite charge-state misclassification and finite timestamp resolution; derive a fidelity / overhead bound.
3. Instantiate with measured NV charge-cycling and nuclear-hyperfine parameters, then test whether the bound creates a nontrivial operating window for blue-light charge control.
4. Re-run manuscript-level novelty audit only after gates 1–3 close.
