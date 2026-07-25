#!/usr/bin/env python3
"""
Smoke test for CIRT Theorem C4 (ancilla closedness).

Context. Blueprints-of-theories/19_causal_interface_realizability_theory_proposal.md
§0 records that seven consecutive RISEI candidates died to the same escape:
combinatorial/algebraic obstructions (lattice, Mobius, RANK, codimension,
polytope) vanish once auxiliary degrees of freedom are added. §4.5 claims the
one obstruction that does NOT vanish is causality/passivity, because the
Herglotz / positive-real class is closed under Schur complement and passive
interconnection (Theorem C4, stated as unproven: "C4 is false => the theory
ends"). This script hits C4 numerically before any further design work.

Conventions (CIRT §3.2, §4.1). The interface datum is a matrix Herglotz
function h with Im h(z) >= 0 for Im z > 0, and (gamma, S) = (2 Im h, -Re h).
A finite passive ancilla chain composes as

    h_up(z) = - V ( z I - H + h_down(z) )^{-1} V^dag ,

terminated by h = 0 at the innermost level (a bare Hermitian bath block).
Each level contributes a Hermitian H and an arbitrary coupling V.

Checks performed:

  (a) Herglotz closure       -- Im h_S(z) >= 0 on a grid in the upper half-plane
  (b) C2a operator antitone  -- -(S(w1)-S(w2))/(w1-w2) >= 0 for point pairs
                                inside a transparent window (a real interval
                                disjoint from the chain's spectrum)
  (c) C2 block Loewner       -- the full n-point block Loewner matrix L >= 0
  (d) counterexample target  -- can any passive chain reproduce the CIRT §4.4
                                datum M = [[1,2],[2,1]] (diag > 0, spec {-1,3})?
  (e) POWER CONTROLS         -- the same checks on deliberately non-physical
                                interfaces. These MUST fail, otherwise the
                                checks above are vacuous. Two are needed
                                because they have different sensitivities:
                                  gain     : anti-Hermitian gain term. Breaks
                                             Im h >= 0 and the block Loewner L,
                                             but NOT C2a.
                                  negweight: indefinite spectral measure
                                             h(w) = sum_j s_j P_j/(t_j - w)
                                             with some s_j = -1. This is what
                                             breaks C2a, i.e. it is the only
                                             control that powers the minimal
                                             witness of CIRT §4.2.

Usage:
    python3 scripts/cirt_c4_smoke.py --depth 4 --trials 200
"""
import argparse

import numpy as np

TOL = 1e-9


def herm(rng, n, scale=1.0):
    X = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    return scale * (X + X.conj().T) / 2


def build_chain(rng, port_dim, depth, sizes=None, passive=True):
    """A finite ancilla chain: list of (H_k, V_k) from outermost to innermost.

    V_k maps level k+1 into level k (V_1 maps the first ancilla into the
    system ports). passive=False flips the sign of the innermost coupling
    weight, producing an indefinite spectral measure -- a non-physical
    'bath' used only as the power control in check (e).
    """
    sizes = sizes or [int(rng.integers(2, 5)) for _ in range(depth)]
    levels, prev = [], port_dim
    for k, n in enumerate(sizes):
        V = rng.standard_normal((prev, n)) + 1j * rng.standard_normal((prev, n))
        if not passive and k == len(sizes) - 1:
            # break positivity of the terminal spectral weight: an
            # anti-Hermitian gain term makes Im h < 0 somewhere.
            H = herm(rng, n) + 1j * 0.7 * np.eye(n)
        else:
            H = herm(rng, n)
        levels.append((H, V))
        prev = n
    return {"kind": "chain", "levels": levels}


def build_spectral(rng, port_dim, n_poles, passive=True):
    """A directly-specified interface h(z) = sum_j s_j P_j / (t_j - z).

    With every s_j = +1 and P_j = v_j v_j^dag >= 0 this is a bona fide matrix
    Herglotz function (a finite-rank stationary bath). Setting some s_j = -1
    makes the spectral measure indefinite: still real-analytic off the poles,
    but no longer a passive bath. That is exactly what CIRT §4.2's minimal
    witness is supposed to detect, so it is the control that powers check (b).
    """
    ts = np.sort(rng.uniform(-4, 4, size=n_poles))
    Ps, signs = [], []
    for j in range(n_poles):
        v = rng.standard_normal((port_dim, 1)) + 1j * rng.standard_normal((port_dim, 1))
        Ps.append(v @ v.conj().T)
        signs.append(1.0 if passive else (-1.0 if j % 2 == 0 else 1.0))
    return {"kind": "spectral", "ts": ts, "Ps": Ps, "signs": signs}


def model_h(z, model):
    """h(z) for either model kind."""
    if model["kind"] == "spectral":
        out = np.zeros_like(model["Ps"][0])
        for t, P, s in zip(model["ts"], model["Ps"], model["signs"]):
            out = out + s * P / (t - z)
        return out
    h = None
    for H, V in reversed(model["levels"]):
        n = H.shape[0]
        W = z * np.eye(n) - H + (h if h is not None else 0.0)
        h = -V @ np.linalg.solve(W, V.conj().T)
    return h


def model_spectrum(model):
    """Real points carrying the poles of h.

    A real interval disjoint from this set is a transparent window in CIRT's
    sense (supp mu disjoint from W).
    """
    if model["kind"] == "spectral":
        return model["ts"]
    levels = model["levels"]
    sizes = [H.shape[0] for H, _ in levels]
    total = sum(sizes)
    Hf = np.zeros((total, total), dtype=complex)
    off = [0]
    for s in sizes:
        off.append(off[-1] + s)
    for k, (H, _) in enumerate(levels):
        Hf[off[k]:off[k + 1], off[k]:off[k + 1]] = H
    for k in range(1, len(levels)):
        # levels[k][1] has shape (sizes[k-1], sizes[k]): it maps level k into
        # level k-1. levels[0][1] couples the ports to level 0 and is not part
        # of the ancilla operator whose spectrum carries the poles.
        V = levels[k][1]
        Hf[off[k - 1]:off[k], off[k]:off[k + 1]] = V
        Hf[off[k]:off[k + 1], off[k - 1]:off[k]] = V.conj().T
    return np.linalg.eigvalsh((Hf + Hf.conj().T) / 2)


def min_eig_herm(A):
    return float(np.min(np.linalg.eigvalsh((A + A.conj().T) / 2)))


def check_herglotz(model, rng, n_pts=12):
    """(a) Im h(z) >= 0 on a grid in the open upper half-plane."""
    worst = np.inf
    for _ in range(n_pts):
        z = complex(rng.uniform(-6, 6), rng.uniform(0.05, 3.0))
        h = model_h(z, model)
        worst = min(worst, min_eig_herm((h - h.conj().T) / 2j))
    return worst


def transparent_points(model, n_points, rng, margin=1.0):
    """n distinct real points in a transparent window: strictly above every
    pole, so the whole segment between any two of them is pole-free
    (CIRT §4.1 requires [w_a, w_b] to lie inside W)."""
    top = float(np.max(model_spectrum(model)))
    return np.sort(top + margin + rng.uniform(0.1, 4.0, size=n_points))


def lamb_shift(model, w):
    """S(w) = -Re h(w). On the transparent window h is real symmetric."""
    return -np.real(model_h(complex(w, 0.0), model))


def check_c2a(model, omegas):
    """(b) minimum eigenvalue of -(S(w1)-S(w2))/(w1-w2) over all point pairs."""
    worst, worst_M = np.inf, None
    for i in range(len(omegas)):
        for j in range(i + 1, len(omegas)):
            w1, w2 = omegas[i], omegas[j]
            M = -(lamb_shift(model, w1) - lamb_shift(model, w2)) / (w1 - w2)
            e = min_eig_herm(M)
            if e < worst:
                worst, worst_M = e, M
    return worst, worst_M


def check_c2_loewner(model, omegas, dz=1e-5):
    """(c) full block Loewner matrix L >= 0, with L_aa from a difference quotient."""
    n, p = len(omegas), lamb_shift(model, omegas[0]).shape[0]
    L = np.zeros((n * p, n * p), dtype=complex)
    for a in range(n):
        for b in range(n):
            wa, wb = omegas[a], omegas[b]
            if a == b:
                blk = (np.real(model_h(complex(wa + dz, 0), model))
                       - np.real(model_h(complex(wa - dz, 0), model))) / (2 * dz)
            else:
                blk = (np.real(model_h(complex(wa, 0), model))
                       - np.real(model_h(complex(wb, 0), model))) / (wa - wb)
            L[a * p:(a + 1) * p, b * p:(b + 1) * p] = blk
    return min_eig_herm(L)


TARGET_M = np.array([[1.0, 2.0], [2.0, 1.0]])   # CIRT §4.4: diag > 0, spec {-1, 3}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--depth", type=int, default=4, help="max ancilla chain depth")
    ap.add_argument("--trials", type=int, default=200)
    ap.add_argument("--ports", type=int, default=2, help="system port dimension p")
    ap.add_argument("--points", type=int, default=3, help="frequency points in the window")
    ap.add_argument("--seed", type=int, default=20260725)
    a = ap.parse_args()

    rng = np.random.default_rng(a.seed)
    print(f"=== CIRT Theorem C4 smoke (ports p={a.ports}, depth<= {a.depth}, "
          f"{a.trials} trials/depth) ===\n")
    print(f"CIRT §4.4 target datum M = [[1,2],[2,1]]: spec = "
          f"{np.round(np.linalg.eigvalsh(TARGET_M), 4)}, min eig = "
          f"{min_eig_herm(TARGET_M):+.4f}\n")

    def make(mode, depth):
        if mode == "passive-chain":
            return build_chain(rng, a.ports, depth, passive=True)
        if mode == "passive-spectral":
            return build_spectral(rng, a.ports, depth + 1, passive=True)
        if mode == "ctrl-gain":
            return build_chain(rng, a.ports, depth, passive=False)
        return build_spectral(rng, a.ports, depth + 1, passive=False)

    MODES = ("passive-chain", "passive-spectral", "ctrl-gain", "ctrl-negweight")
    print(f"{'mode':>17}{'depth':>7}{'min Im h':>13}{'min eig C2a':>14}"
          f"{'min eig L':>13}{'viol':>7}{'  by check (Imh/C2a/L)'}")

    tally = {m: [0, 0, 0, 0] for m in MODES}   # total, by-Imh, by-C2a, by-L
    for mode in MODES:
        for depth in range(1, a.depth + 1):
            w_im, w_c2a, w_L, viol = np.inf, np.inf, np.inf, 0
            n_im = n_c2a = n_L = 0
            for _ in range(a.trials):
                model = make(mode, depth)
                try:
                    im = check_herglotz(model, rng)
                    om = transparent_points(model, a.points, rng)
                    c2a, _ = check_c2a(model, om)
                    L = check_c2_loewner(model, om)
                except np.linalg.LinAlgError:
                    continue
                w_im, w_c2a, w_L = min(w_im, im), min(w_c2a, c2a), min(w_L, L)
                n_im += im < -TOL
                n_c2a += c2a < -TOL
                n_L += L < -TOL
                if im < -TOL or c2a < -TOL or L < -TOL:
                    viol += 1
            t = tally[mode]
            t[0] += viol; t[1] += n_im; t[2] += n_c2a; t[3] += n_L
            print(f"{mode:>17}{depth:>7}{w_im:>13.2e}{w_c2a:>14.2e}"
                  f"{w_L:>13.2e}{viol:>7}   {n_im}/{n_c2a}/{n_L}")

    passive_viol = sum(tally[m][0] for m in MODES if m.startswith("passive"))
    ctrl_imh = sum(tally[m][1] for m in MODES if m.startswith("ctrl"))
    ctrl_c2a = sum(tally[m][2] for m in MODES if m.startswith("ctrl"))
    ctrl_L = sum(tally[m][3] for m in MODES if m.startswith("ctrl"))
    control_viol = sum(tally[m][0] for m in MODES if m.startswith("ctrl"))

    print(f"\ncontrol power: Im h caught {ctrl_imh}, C2a caught {ctrl_c2a}, "
          f"L caught {ctrl_L}")

    print("\n=== VERDICT ===")
    if min(ctrl_imh, ctrl_c2a, ctrl_L) == 0:
        print("INCONCLUSIVE: at least one check never fired on any control, so that")
        print("check has no demonstrated power. Do not read the passive result as")
        print("evidence for C4 until every check is powered by some control.")
        print(f"  Im h: {ctrl_imh}   C2a: {ctrl_c2a}   L: {ctrl_L}")
    elif passive_viol == 0:
        print(f"GO (smoke): {passive_viol} violations across all passive chains, while the")
        print(f"non-passive control produced {control_viol}. The checks demonstrably detect")
        print("violations, and passive ancilla chains never produced one. Consistent with")
        print("C4: no finite passive ancilla chain reproduced the CIRT §4.4 datum, whose")
        print(f"min eigenvalue {min_eig_herm(TARGET_M):+.3f} would have to appear as a negative")
        print("C2a eigenvalue.")
        print()
        print("This is the ABSENCE OF A COUNTEREXAMPLE, not a proof of C4.")
        print("C4 remains unproven; see THEORY_PROPOSAL_GUIDE.md §9.")
    else:
        print(f"NO-GO: {passive_viol} violations found among PASSIVE chains.")
        print("A passive ancilla chain broke Herglotz closure or the C2 Loewner condition.")
        print("If reproducible this refutes C4, and CIRT's claim to escape the")
        print("shared-ancilla trap fails. Record the counterexample as the primary finding.")


if __name__ == "__main__":
    main()
