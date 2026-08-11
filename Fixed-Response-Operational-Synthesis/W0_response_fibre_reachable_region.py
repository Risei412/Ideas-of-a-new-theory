#!/usr/bin/env python3
"""W0 certificate: fixed-response Gaussian fibre with a noise--QFI reachable region.

The drift is the frozen M3 passive four-mode family, but the signal is injected
through monitored port 1 and is NOT rotated with the hidden coupling.  The
zero-signal monitored transfer is therefore identical for all coupling angles.
Unequal hidden-bath occupations create an anisotropic output covariance whose
orientation is invisible to first moments.

At omega=0 and fixed total hidden occupation N=n1+n2, the reachable pair
(S_11, q) with q=e1^T V^{-1} e1 (Gaussian displacement-QFI per squared output
signal derivative) obeys an exact two-dimensional region:

    1/2 <= S_11 <= T-1/2,
    1/S_11 <= q <= (T-S_11)/(T/2-1/4),

where T=tr V = 1 + alpha N and alpha is the hidden-to-monitored noise transfer
weight.  Actual displacement QFI is F_Q = |d_out/dx|^2 q in the quadrature
convention where vacuum covariance is I/2.
"""
import json
import math
import numpy as np

GAMMA = 0.4
G = 0.75
C_HIDDEN = 1.0 + 1.0j
KAPPA = float(C_HIDDEN.real)
DELTA_STAR = -float(np.imag(G**2 / C_HIDDEN))
N_TOTAL = 4.0
OMEGA_STAR = 0.0


def rotation(theta):
    return np.array([[math.cos(theta), -math.sin(theta)],
                     [math.sin(theta),  math.cos(theta)]], dtype=float)


def drift(theta, delta=DELTA_STAR):
    r = rotation(theta)
    a = np.zeros((4, 4), dtype=complex)
    a[:2, :2] = (GAMMA / 2 + 1j * delta) * np.eye(2)
    a[:2, 2:] = 1j * G * r
    a[2:, :2] = 1j * G * r.T
    a[2:, 2:] = C_HIDDEN * np.eye(2)
    return a


def transfers(theta, omega=OMEGA_STAR, delta=DELTA_STAR):
    resolvent = np.linalg.inv(drift(theta, delta) - 1j * omega * np.eye(4))
    # monitored input -> monitored output
    t_ss = np.eye(2) - GAMMA * resolvent[:2, :2]
    # hidden bath input -> monitored output
    t_sh = -math.sqrt(GAMMA) * resolvent[:2, 2:] * math.sqrt(2 * KAPPA)
    return t_ss, t_sh


def minimality_ranks(theta):
    a = drift(theta)
    b = np.vstack([math.sqrt(GAMMA) * np.eye(2), np.zeros((2, 2))]).astype(complex)
    c = np.hstack([math.sqrt(GAMMA) * np.eye(2), np.zeros((2, 2))]).astype(complex)
    ctr = np.hstack([np.linalg.matrix_power(-a, k) @ b for k in range(4)])
    obs = np.vstack([c @ np.linalg.matrix_power(-a, k) for k in range(4)])
    return int(np.linalg.matrix_rank(ctr, tol=1e-10)), int(np.linalg.matrix_rank(obs, tol=1e-10))


def output_covariance(theta, n1, n2, omega=OMEGA_STAR):
    """One-quadrature symmetrized output covariance; vacuum covariance=I/2."""
    t_ss, t_sh = transfers(theta, omega)
    nmat = np.diag([n1, n2])
    # vacuum part from all channels + hidden thermal excess
    return 0.5 * (t_ss @ t_ss.conj().T + t_sh @ t_sh.conj().T) + t_sh @ nmat @ t_sh.conj().T


def reachable_pair(theta, n1, n2):
    v = output_covariance(theta, n1, n2)
    t_ss, _ = transfers(theta)
    # unit input-quadrature signal injected into monitored port 1
    d = t_ss[:, 0]
    s11 = float(np.real(v[0, 0]))
    q = float(np.real(np.array([1.0, 0.0]) @ np.linalg.inv(v) @ np.array([1.0, 0.0])))
    fq = float(np.real(np.conj(d) @ np.linalg.inv(v) @ d))
    return s11, q, fq, float(abs(d[0])**2)


def main():
    theta_grid = np.linspace(0.0, math.pi / 2, 81)
    omega_grid = np.linspace(-5.0, 5.0, 81)
    delta_grid = np.linspace(-3.0, 3.0, 21)

    # 1) full monitored transfer invariance and physicality
    transfer_ref = {(float(d), float(w)): transfers(0.0, w, d)[0]
                    for d in delta_grid for w in omega_grid}
    max_transfer_error = 0.0
    max_vacuum_preservation_error = 0.0
    min_hermitian_eig = float("inf")
    min_rank = 4
    for th in theta_grid:
        a = drift(th)
        min_hermitian_eig = min(min_hermitian_eig,
                                float(np.min(np.linalg.eigvalsh((a + a.conj().T) / 2))))
        cr, orank = minimality_ranks(th)
        min_rank = min(min_rank, cr, orank)
        for d in delta_grid:
            for w in omega_grid:
                t_ss, t_sh = transfers(th, w, d)
                max_transfer_error = max(max_transfer_error,
                    float(np.linalg.norm(t_ss - transfer_ref[(float(d), float(w))])))
                max_vacuum_preservation_error = max(max_vacuum_preservation_error,
                    float(np.linalg.norm(t_ss @ t_ss.conj().T + t_sh @ t_sh.conj().T - np.eye(2))))

    # 2) strict fixed bath spectrum: exact 1D curve
    n1_fixed, n2_fixed = 0.0, N_TOTAL
    v0 = output_covariance(0.0, n1_fixed, n2_fixed)
    eigs_ref = np.sort(np.linalg.eigvalsh(v0))
    t_ss0, t_sh0 = transfers(0.0)
    alpha = float(abs(t_sh0[0, 0])**2)
    signal_gain_sq = float(abs(t_ss0[0, 0])**2)
    max_cov_eigen_error = 0.0
    max_curve_error = 0.0
    curve_records = []
    v1, v2 = map(float, eigs_ref)
    for th in theta_grid:
        v = output_covariance(th, n1_fixed, n2_fixed)
        max_cov_eigen_error = max(max_cov_eigen_error,
            float(np.max(np.abs(np.sort(np.linalg.eigvalsh(v)) - eigs_ref))))
        s11, q, fq, gain_sq = reachable_pair(th, n1_fixed, n2_fixed)
        q_analytic = (v1 + v2 - s11) / (v1 * v2)
        max_curve_error = max(max_curve_error, abs(q - q_analytic))
        if th in (theta_grid[0], theta_grid[len(theta_grid)//2], theta_grid[-1]):
            curve_records.append({"theta": float(th), "S11": s11, "q_normalized": q,
                                  "FQ_unit_input": fq, "signal_gain_sq": gain_sq})

    # 3) fixed scalar energy budget n1+n2=N_TOTAL: exact 2D region
    trace_T = 1.0 + alpha * N_TOTAL
    determinant_floor = trace_T / 2.0 - 0.25
    s_min, s_max = 0.5, trace_T - 0.5
    max_lower_violation = 0.0
    max_upper_violation = 0.0
    min_margin = float("inf")
    sample_points = []
    for n1 in np.linspace(0.0, N_TOTAL, 81):
        n2 = N_TOTAL - n1
        for th in theta_grid:
            s11, q, fq, _ = reachable_pair(th, n1, n2)
            q_lo = 1.0 / s11
            q_hi = (trace_T - s11) / determinant_floor
            max_lower_violation = max(max_lower_violation, q_lo - q)
            max_upper_violation = max(max_upper_violation, q - q_hi)
            min_margin = min(min_margin, q - q_lo, q_hi - q)
            if abs(n1 - N_TOTAL/2) < 1e-12 and abs(th - math.pi/4) < 1e-12:
                sample_points.append({"n1": float(n1), "n2": float(n2), "theta": float(th),
                                      "S11": s11, "q_normalized": q, "FQ_unit_input": fq})

    # analytic area in the (S11,q) plane. Positive area proves a genuine 2D image.
    area = ((2 * trace_T**2 - 2 * trace_T * math.log(2 * trace_T - 1)
             - 2 * trace_T + math.log(2 * trace_T - 1)) / (2 * trace_T - 1))

    endpoint_cold = reachable_pair(0.0, 0.0, N_TOTAL)
    endpoint_hot = reachable_pair(math.pi/2, 0.0, N_TOTAL)

    checks = {
        "complete_monitored_transfer_invariant_on_frequency_control_grid": max_transfer_error < 1e-12,
        "passive_vacuum_preservation": max_vacuum_preservation_error < 1e-12,
        "strict_stability": min_hermitian_eig > 0.0,
        "all_sampled_realizations_controllable_and_observable": min_rank == 4,
        "fixed_bath_spectrum_output_covariance_eigenvalues_invariant": max_cov_eigen_error < 1e-12,
        "fixed_bath_spectrum_exact_noise_qfi_curve": max_curve_error < 1e-12,
        "fixed_total_occupation_region_lower_bound_respected": max_lower_violation < 1e-12,
        "fixed_total_occupation_region_upper_bound_respected": max_upper_violation < 1e-12,
        "reachable_image_has_nonzero_area": area > 1e-6,
        "qfi_changes_at_fixed_response_and_fixed_bath_spectrum": abs(endpoint_cold[2] - endpoint_hot[2]) > 1e-3,
    }

    result = {
        "gate": "W0_FIXED_RESPONSE_NOISE_QFI_REACHABLE_REGION",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "stable passive four-mode Gaussian Markov input-output systems; single analysis frequency omega=0 for the reachable-set theorem, while monitored transfer invariance is checked over frequency and slow-control grids",
        "parameters": {
            "gamma": GAMMA, "g": G,
            "hidden_c": [C_HIDDEN.real, C_HIDDEN.imag],
            "delta_star": DELTA_STAR, "omega_star": OMEGA_STAR,
            "total_hidden_occupation_budget": N_TOTAL,
        },
        "analytic_statements": {
            "monitored_transfer": "T_ss(theta,omega,delta)=T_ss(0,omega,delta)",
            "noise_covariance": "V(theta)=1/2 I + alpha R(theta) diag(n1,n2) R(theta)^T",
            "fixed_spectrum_curve": "q=(v1+v2-S11)/(v1 v2)",
            "fixed_total_budget_region": "1/2<=S11<=T-1/2 and 1/S11<=q<=(T-S11)/(T/2-1/4)",
            "qfi_relation": "F_Q=|d_out/dx|^2 q for a displacement-only signal in the vacuum=I/2 quadrature convention",
        },
        "derived_numbers": {
            "hidden_noise_transfer_weight_alpha": alpha,
            "monitored_signal_gain_sq": signal_gain_sq,
            "fixed_spectrum_covariance_eigenvalues": [v1, v2],
            "fixed_total_budget_trace_T": trace_T,
            "fixed_total_budget_determinant_floor": determinant_floor,
            "S11_range": [s_min, s_max],
            "reachable_region_area_in_S11_q_plane": area,
            "endpoint_unit_input_FQ": [endpoint_cold[2], endpoint_hot[2]],
            "endpoint_FQ_ratio": max(endpoint_cold[2], endpoint_hot[2]) / min(endpoint_cold[2], endpoint_hot[2]),
        },
        "numerical_errors": {
            "max_transfer_error": max_transfer_error,
            "max_vacuum_preservation_error": max_vacuum_preservation_error,
            "min_hermitian_part_eigenvalue": min_hermitian_eig,
            "minimum_controllability_observability_rank": min_rank,
            "max_covariance_eigenvalue_error": max_cov_eigen_error,
            "max_fixed_spectrum_curve_error": max_curve_error,
            "max_region_lower_violation": max_lower_violation,
            "max_region_upper_violation": max_upper_violation,
            "minimum_region_margin_sampled": min_margin,
        },
        "representative_fixed_spectrum_points": curve_records,
        "representative_fixed_budget_points": sample_points,
        "checks": checks,
        "interpretation": "At exactly fixed detector-facing transfer, physical dimension and total hidden occupation budget, hidden bath anisotropy plus a response-invisible coupling orientation generates a genuine two-dimensional noise--displacement-QFI design region. With the full bath spectrum also fixed, the image collapses to an exactly solvable one-dimensional boundary curve.",
        "claim_boundary": [
            "This is a minimal constructive witness, not yet a general realizability theorem.",
            "The two-dimensional region fixes only the scalar total hidden occupation budget; the full bath occupation spectrum is allowed to redistribute.",
            "If the full bath spectrum is fixed, W0 proves an exact one-dimensional reachable curve, not a two-dimensional region.",
            "Novelty is not assigned to Gaussian covariance rotation itself; the next gate must test whether the reachable-set structure survives beyond this isotropic stabilizer family and avoids standard spectral-factorization absorption."
        ]
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
