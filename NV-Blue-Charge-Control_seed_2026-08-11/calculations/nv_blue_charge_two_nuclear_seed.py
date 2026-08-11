"""Synthetic held-out benchmark seed: NV blue-charge control -> 2-nuclear-spin DLA geometry.

Purpose
-------
Test whether a four-level two-nuclear-spin effective Hamiltonian can realize
same full DLA su(4) but different marked perturbative depth d=2 versus d=3.
Blue light is NOT modeled as the perturbation epsilon. It is intended only as
a charge-sector preparation/heralding knob that selects different effective
nuclear Hamiltonian/control coefficients. The weak coherent perturbation
parameter epsilon belongs to MW/RF/effective Hamiltonian control.

This is an operator-class witness, not a fitted NV-/NV0 device model.
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import expm

H0 = np.diag([0.0, 1.0, 1.0, 3.0])


def V(control_d: float) -> np.ndarray:
    out = np.zeros((4, 4), dtype=complex)
    for (i, j), value in {
        (0, 1): 1.0,
        (0, 2): 2.0,
        (1, 3): 1.0,
        (2, 3): control_d,
        (1, 2): 0.7,
    }.items():
        out[i, j] = value
        out[j, i] = value
    return out


def _real_vec(a: np.ndarray) -> np.ndarray:
    return np.concatenate([a.real.ravel(), a.imag.ravel()])


def lie_closure_dim(generators: list[np.ndarray], tol: float = 1e-10) -> int:
    n = generators[0].shape[0]
    basis: list[np.ndarray] = []
    orth: list[np.ndarray] = []

    def add(a: np.ndarray) -> bool:
        a = (a - a.conj().T) / 2
        a = a - np.trace(a) * np.eye(n) / n
        w = _real_vec(a)
        for q in orth:
            w = w - np.dot(q, w) * q
        norm = np.linalg.norm(w)
        if norm <= tol:
            return False
        orth.append(w / norm)
        basis.append(a)
        return True

    for g in generators:
        add(g)

    changed = True
    while changed:
        changed = False
        current = list(basis)
        for i in range(len(current)):
            for j in range(i + 1, len(current)):
                comm = current[i] @ current[j] - current[j] @ current[i]
                if add(comm):
                    changed = True
                    if len(basis) == n * n - 1:
                        return len(basis)
    return len(basis)


def k2_path_coefficient(control_d: float) -> float:
    return 1.0 * 1.0 + 2.0 * control_d


def k3_path_coefficient(control_d: float) -> float:
    return 0.7 * (2.0 * 1.0 + 1.0 * control_d)


def transition_probability(epsilon: float, control_d: float, t: float = 1.0) -> float:
    u = expm(-1j * (H0 + epsilon * V(control_d)) * t)
    return float(abs(u[3, 0]) ** 2)


def fitted_probability_slope(control_d: float) -> float:
    eps = np.logspace(-4, -2.25, 8)
    probs = np.array([transition_probability(e, control_d) for e in eps])
    return float(np.polyfit(np.log(eps), np.log(probs), 1)[0])


def main() -> None:
    cases = {
        "generic_depth2": 1.0,
        "cancellation_depth3": -0.5,
    }
    for name, d in cases.items():
        dla = lie_closure_dim([1j * H0, 1j * V(d)])
        k2 = k2_path_coefficient(d)
        k3 = k3_path_coefficient(d)
        slope = fitted_probability_slope(d)
        print(
            f"{name}: control_d={d:+.3f}, DLA_dim={dla}, "
            f"K2_coeff={k2:+.6f}, K3_coeff={k3:+.6f}, "
            f"probability_slope={slope:.6f}"
        )

    assert lie_closure_dim([1j * H0, 1j * V(1.0)]) == 15
    assert lie_closure_dim([1j * H0, 1j * V(-0.5)]) == 15
    assert abs(k2_path_coefficient(-0.5)) < 1e-12
    assert abs(k3_path_coefficient(-0.5)) > 1e-12
    print("PASS: same su(4) DLA with marked depth 2 -> 3 and probability slope 4 -> 6.")


if __name__ == "__main__":
    main()
