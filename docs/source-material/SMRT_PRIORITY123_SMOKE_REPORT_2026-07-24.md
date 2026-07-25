# SMRT Priority 1–3 implementation and smoke-test report

Date: 2026-07-24  
Protocol: `smrt-priority123-smoke-v1`

## Executive decision

All implemented smoke gates passed.

\[
\boxed{
\text{Priority 1: PASS}\qquad
\text{Priority 2: PASS}\qquad
\text{Priority 3: PASS}
}
\]

This authorizes a production run for Priority 1 and Priority 2. It also
authorizes production-scale ensemble calculations for the canonical Phase-N
rational witness. A publication-grade Priority-3 claim using the original
full GKSL Phase-N model remains conditional on restoring the transferred
Phase-N implementation, which was received as a zero-byte file.

The smoke calculation is not called a blind validation. The smoke model,
predictor, and numerical tests were co-developed in the same implementation
turn. A distinct four-mode held-out model has therefore been frozen for the
production run and has not yet been numerically evaluated.

## Input-integrity boundary

The following supplied files were nonempty and were used:

- `01-SMRT_operationally_integrated_theorem_package.tex`
- `03-physical_hidden_transition_gksl-1-.md`
- `04-gates_summary_phaseH-1-.json`

The following local attachment copies were zero bytes:

- the specified `kyubey_inspired_style.md`;
- the Phase N/H runner files;
- the Phase N result JSON;
- the two-scale polyhedral theorem TeX;
- the supplied hidden-model Python source;
- the scaling-assumption revision;
- the undergraduate PDF.

The implementation therefore uses the readable operational theorem package,
the Phase-H report/result, and the Phase-N piecewise law stated in the
conversation. It does not claim to have re-executed the missing original
Phase-N code.

## Shared implementation

The package implements:

- bivariate polynomial arithmetic in \((\Gamma,\kappa)\);
- exact determinant and adjugate transfer numerators;
- weighted Newton-degree prediction along
  \(\kappa=\kappa_0\Gamma^q\);
- removal of non-dominant monomial intersections;
- finite-window exponent fitting;
- a full GKSL Liouvillian generator and trace-constrained linear-response
  solve;
- a common EIT/ATS/CPT/no-go benchmark interface;
- coefficient, intervention-prefactor, finite-window, and measurement-noise
  ensembles;
- a degenerate-face negative control.

The exact predictor has no computer-algebra dependency. NumPy is the only
non-standard runtime dependency.

## Priority 1 — second GKSL architecture

### Smoke architecture

The smoke model consists of a physical ground state plus three coherently
coupled modes. Native amplitude damping and the operational pure-dephasing
intervention act on two modes, while the third is protected. All jump rates
are nonnegative and the Hamiltonian is Hermitian.

The preregistered law was

\[
\nu(q)=
\begin{cases}
2-q,&0\le q\le1,\\
1,&q\ge1.
\end{cases}
\]

The exact weighted-degree predictor returned one dominant breakpoint,

\[
q_\ast=1.
\]

### Smoke results

| Quantity | Result | Gate |
|---|---:|---:|
| maximum exponent-fit error | \(1.1280\times10^{-2}\) | \(<3.5\times10^{-2}\) |
| minimum log-fit \(R^2\) | \(0.9999991\) | diagnostic |
| reduced vs full-GKSL maximum error | \(3.4711\times10^{-18}\) | \(<10^{-10}\) |
| Hamiltonian Hermiticity residual | \(0\) | \(<10^{-12}\) |
| trace-preservation residual | numerical zero | \(<10^{-12}\) |
| nonnegative rates | true | required |

All Priority-1 smoke gates passed.

### Held-out production model

The production protocol uses a different four-mode ring architecture, a
different native/intervention support pattern, and a cross-mode readout. The
exact predictor, evaluated before any numerical response data, gives

\[
\nu(q)=
\begin{cases}
3-q,&0\le q\le1,\\
2,&q\ge1,
\end{cases}
\qquad q_\ast=1.
\]

The frozen production-registration hash is

`0ba74e2f7463e5ce500335bb0b37cb289253443ebb3c51b64b25d7c3fe3d1d37`.

`run_production.py` has passed syntax/import checks but has not been executed.

## Priority 2 — EIT/ATS/CPT/no-go common benchmark

One Lambda-type weak-probe interface was used for all four cases. The
mechanism gate uses the control strength relative to the non-Hermitian dressed
splitting threshold and the presence or absence of the second-tone source.
Thus the labels are checked from model structure rather than accepted from the
case names.

| Case | Mechanism audit | Predicted order | Maximum fit error | Result |
|---|---|---:|---:|---|
| EIT | below dressed-splitting threshold | \(2\) | \(1.50\times10^{-4}\) | PASS |
| ATS | above dressed-splitting threshold | \(2\) | \(1.48\times10^{-2}\) | PASS |
| CPT | nonzero second-tone source | \(1\) | \(6.43\times10^{-4}\) | PASS |
| no-go | sector decoupled | \(\infty\) | exact zero | PASS |

This is enough to qualify the common scaling pipeline. It is not, by itself, a
new universal EIT-versus-ATS discrimination theorem. A publication figure
should still show the corresponding frequency-domain lineshapes and pole
structure so that the spectroscopic regimes are visible rather than merely
named.

## Priority 3 — Phase-N fan robustness and finite window

Because the transferred original Phase-N runner was empty, the smoke harness
uses the canonical rational representative

\[
R(\Gamma,\kappa)=
\frac{\Gamma^2\kappa+\kappa^2}
{\Gamma^6+\Gamma^4\kappa^2}.
\]

Its numerator and denominator Newton faces give exactly

\[
\nu(q)=
\begin{cases}
4-q,&0\le q\le1,\\
2+q,&1\le q\le2,\\
4,&q\ge2,
\end{cases}
\]

with dominant breakpoints \(q=1,2\).

The smoke ensemble used 24 samples with lognormal coefficient perturbations,
\(\kappa_0\in[0.5,2]\), a finite \(\Gamma\) window from \(10^2\) to \(10^6\),
and relative log-noise \(\sigma=10^{-3}\).

| Quantity | Result | Gate |
|---|---:|---:|
| 95th-percentile exponent error | \(1.7955\times10^{-2}\) | \(<0.15\) |
| maximum exponent error | \(3.3305\times10^{-2}\) | diagnostic |
| fan-detection probability | \(1.000\) | \(>0.90\) |
| recovered dominant breakpoints | \(1,2\) | exact |
| degenerate-face negative control | correctly rejected | required |

All canonical Priority-3 smoke gates passed.

The production configuration raises the ensemble to 1000 samples, widens
\(\kappa_0\) to \([0.25,4]\), widens the \(\Gamma\) range to
\([10^2,10^8]\), and raises the noise level to \(3\times10^{-3}\).

## Production authorization

| Priority | Production status | Remaining condition |
|---|---|---|
| 1 | ready; held-out protocol frozen | run once without altering registration |
| 2 | ready for scaling benchmark | add frequency-domain visualization for the paper |
| 3 canonical witness | ready | run the 1000-sample profile |
| 3 original full GKSL Phase N | blocked | restore the missing Phase-N source and connect its response function |

The correct global judgment is therefore:

\[
\boxed{
\text{implementation-ready for production}
\neq
\text{all publication claims already certified}.
}
\]

The production entry point deliberately reports
`publication_claim_ready=false` while the Priority-3 backend is the canonical
rational witness. This prevents a successful ensemble run from being
misreported as a full-GKSL robustness validation.

## Reproduction

From the package directory:

```bash
python -m unittest -v test_smoke.py
python run_smoke.py
```

After confirming that `production_preregistration.json` still matches the
recorded SHA-256:

```bash
python run_production.py
```

Do not edit the production registration after inspecting production response
values. Any necessary modification creates a new protocol version and a new
hash.
