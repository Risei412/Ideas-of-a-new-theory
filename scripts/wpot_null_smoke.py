#!/usr/bin/env python3
"""
Stage A null-identity smoke for WPOT (Blueprints-of-theories/23_*.md).

WHAT IS BEING TESTED
--------------------
Proposal 23 conjectures WP1 (word-domain passivity condition):

    a passive (thermal / KMS) realization of arbitrary bath dimension exists
      ==>  the word-domain Loewner matrix Pi_n is semidefinite.

Stage A does NOT try to build a violating construction. It fixes the null
identity first (guide 6.4 末尾: competitor null identity BEFORE inverse
design). If passive ensembles already break the claimed semidefiniteness,
WP1 is false as stated and proposal 23 is withdrawn (23 stop condition 1).

THE OBJECT
----------
For an alphabet U, a parametric letter u(theta), and prefix/suffix words
w, w' in U^{<=p}, define the symmetrized word response matrix

    G(theta)_{w,w'} = ( R(w u(theta) w') + R(w' u(theta) w) ) / 2

(real symmetric, |W| x |W|), and the block Loewner matrix

    L[(i,w),(j,w')] = ( G(theta_i) - G(theta_j) )_{w,w'} / (theta_i - theta_j)
    L[(i,w),(i,w')] = G'(theta_i)_{w,w'}                    (diagonal blocks)

which is the standard matrix-Loewner object whose semidefiniteness is
equivalent (Loewner 1934) to operator monotonicity of G on the grid.

SIGN CONVENTION IS FROZEN BEFORE RUNNING. CIRT's minimal witness (C2a) is
stated in ANTITONE form, -(S(w1)-S(w2))/(w1-w2) >= 0, because a thermal
response decays in the relevant parameter. Proposal 23 inherits that
convention, so the tested object is

    Pi := -L      and the null identity is    Pi >= 0.

A run is ALSO scored under Pi := +L, and a variant is only counted as
surviving if ONE FIXED SIGN works for every passive trial in that variant.
A variant where some trials need + and others need - is NOT a null identity
(the object has no definite sign) and is scored as a violation.

TWO VARIANTS OF "theta"
-----------------------
The blueprint says theta is "the intervention coupling strength, everything
else frozen" but does not fix how theta enters the generator. The two
readings are inequivalent and are both tested:

  A (hamiltonian): u(theta) = evolve system+bath unitarily for a fixed
      window under H_S + theta V_S + H_B + lambda A_S (x) B, bath in an
      exact Gibbs state. This is a passive realization with NO weak-coupling
      approximation: the bath is thermal and the global dynamics unitary.

  B (dissipative): u(theta) = exp(theta * L_th) where L_th is a GKSL
      generator satisfying KMS detailed balance w.r.t. a Gibbs state of
      H_S. theta is the duration of thermal contact. Other letters are
      fixed CPTP maps. This is the reading under which the frequency-domain
      family-N analogy (resolvent-like parameter) is closest.

CONTROLS (power check; these MUST violate, else the test is vacuous)
--------------------------------------------------------------------
  inverted : GKSL with population-inverted rates (no KMS detailed balance)
             -- an athermal bath, the physical negation of the hypothesis.
  gain     : non-CPTP gain term added to the generator.
  negweight: indefinite spectral weights on the thermal letter.

Usage:
    python3 scripts/wpot_null_smoke.py --trials 200
"""
import argparse
import numpy as np

# ---------------------------------------------------------------------------
# FROZEN DECISION RULE (fixed before the first run; do not edit after seeing
# results -- see guide 9 and p0-certificate-spec 3).
#
#   TOL_ABS   absolute slack on lambda_min, relative to the scale of Pi.
#   A trial VIOLATES if  lambda_min(Pi) < -TOL_ABS * max(1, ||Pi||_2)
#   for BOTH sign conventions (i.e. neither +L nor -L is PSD).
#   A variant PASSES only if violations == 0 across all passive trials AND
#   the surviving sign is the same for every passive trial.
#   A variant is VACUOUS (inconclusive, not a pass) if the controls do not
#   violate.
# ---------------------------------------------------------------------------
TOL_ABS = 1e-8


def herm(rng, n, scale=1.0):
    X = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    return scale * (X + X.conj().T) / 2


def gibbs(H, beta_th):
    w, V = np.linalg.eigh(H)
    p = np.exp(-beta_th * (w - w.min()))
    p /= p.sum()
    return (V * p) @ V.conj().T


# ---------------------------------------------------------------------------
# Variant A: unitary system + Gibbs bath, theta = hamiltonian intervention
# ---------------------------------------------------------------------------
def variant_a_response(rng, thetas, words, dS=2, dB=3, mode="passive"):
    """R(w u(theta) w') for the exact system+thermal-bath unitary model."""
    d = dS * dB
    HS = herm(rng, dS)
    VS = herm(rng, dS)
    HB = herm(rng, dB)
    A = herm(rng, dS)
    B = herm(rng, dB)
    lam = 0.6
    beta_th = float(rng.uniform(0.3, 2.0))

    Hfix = np.kron(HS, np.eye(dB)) + np.kron(np.eye(dS), HB) + lam * np.kron(A, B)
    if mode == "gain":
        Hfix = Hfix + 1j * 0.35 * np.eye(d)          # non-unitary gain
    rhoB = gibbs(HB, beta_th)
    if mode == "negweight":                           # indefinite bath weight
        w_, V_ = np.linalg.eigh(rhoB)
        w_ = w_.copy()
        w_[0] *= -1.0
        rhoB = (V_ * w_) @ V_.conj().T
    if mode == "inverted":                            # population-inverted bath
        rhoB = gibbs(HB, -beta_th)

    rhoS0 = gibbs(herm(rng, dS), 1.0)
    rho0 = np.kron(rhoS0, rhoB)
    E = np.kron(_povm(rng, dS), np.eye(dB))

    dt = 0.8
    # fixed (non-parametric) letters
    letters = {}
    for name in ("a", "b"):
        Hl = Hfix + herm(rng, d, 0.5)
        letters[name] = _expmi(Hl, dt)

    def u_theta(theta):
        return _expmi(Hfix + theta * np.kron(VS, np.eye(dB)), dt)

    def R(prefix, theta, suffix):
        U = u_theta(theta)
        for c in prefix:
            U = U @ letters[c]
        for c in suffix:
            U = letters[c] @ U
        rho = U @ rho0 @ U.conj().T
        return float(np.real(np.trace(E @ rho)))

    return _assemble(R, thetas, words)


# ---------------------------------------------------------------------------
# Variant B: KMS detailed-balance GKSL, theta = duration of thermal contact
# ---------------------------------------------------------------------------
def variant_b_response(rng, thetas, words, dS=3, mode="passive"):
    """R(w u(theta) w') where u(theta) = exp(theta L_th), L_th detailed balance."""
    HS = np.diag(np.sort(rng.uniform(0.0, 2.0, dS)))
    beta_th = float(rng.uniform(0.3, 2.0))
    L = _thermal_gksl(HS, beta_th, rng, mode)

    rho0 = gibbs(herm(rng, dS), 1.0)
    E = _povm(rng, dS)
    v0 = rho0.reshape(-1)
    eL = E.conj().T.reshape(-1)

    letters = {name: _cptp_super(rng, dS) for name in ("a", "b")}

    evals, evecs = np.linalg.eig(L)
    evecs_inv = np.linalg.inv(evecs)

    def u_theta(theta):
        return (evecs * np.exp(theta * evals)) @ evecs_inv

    def R(prefix, theta, suffix):
        M = u_theta(theta)
        for c in prefix:
            M = M @ letters[c]
        for c in suffix:
            M = letters[c] @ M
        return float(np.real(eL @ (M @ v0)))

    return _assemble(R, thetas, words)


def _thermal_gksl(HS, beta_th, rng, mode):
    """Vectorized GKSL generator; passive mode satisfies KMS detailed balance."""
    d = HS.shape[0]
    I = np.eye(d)
    Lsup = -1j * (np.kron(HS, I) - np.kron(I, HS.T))
    w = np.diag(HS).real
    for i in range(d):
        for j in range(d):
            if i == j:
                continue
            gam = float(rng.uniform(0.2, 1.0))
            if mode == "passive":
                # downhill rate g, uphill rate g*exp(-beta*dE): detailed balance
                dE = w[i] - w[j]
                rate = gam * (1.0 if dE < 0 else np.exp(-beta_th * dE))
            elif mode == "inverted":
                dE = w[i] - w[j]
                rate = gam * (1.0 if dE > 0 else np.exp(-beta_th * dE))
            elif mode == "negweight":
                rate = gam * (1.0 if (i + j) % 2 == 0 else -1.0)
            else:  # gain
                rate = gam
            Ljump = np.zeros((d, d))
            Ljump[i, j] = 1.0
            LdL = Ljump.conj().T @ Ljump
            Lsup = Lsup + rate * (
                np.kron(Ljump, Ljump.conj())
                - 0.5 * (np.kron(LdL, I) + np.kron(I, LdL.T))
            )
    if mode == "gain":
        Lsup = Lsup + 0.4 * np.eye(d * d)   # trace-increasing: not CPTP
    return Lsup


def _cptp_super(rng, d, nk=3):
    Ks = [rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))
          for _ in range(nk)]
    S = sum(K.conj().T @ K for K in Ks)
    Sm = np.linalg.inv(_sqrtm_h(S))
    Ks = [K @ Sm for K in Ks]
    return sum(np.kron(K, K.conj()) for K in Ks)


def _sqrtm_h(M):
    w, V = np.linalg.eigh((M + M.conj().T) / 2)
    return (V * np.sqrt(np.maximum(w, 1e-15))) @ V.conj().T


def _povm(rng, d):
    X = rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))
    M = X.conj().T @ X
    return M / np.linalg.eigvalsh(M).max()


def _expmi(H, t):
    w, V = np.linalg.eig(H)
    return (V * np.exp(-1j * t * w)) @ np.linalg.inv(V)


def _assemble(R, thetas, words):
    """G(theta) for each grid point, plus the derivative blocks."""
    nW = len(words)
    G = []
    for th in thetas:
        M = np.zeros((nW, nW))
        for a, (pa, sa) in enumerate(words):
            for b, (pb, sb) in enumerate(words):
                M[a, b] = 0.5 * (R(pa, th, sb) + R(pb, th, sa))
        G.append(M)
    h = 1e-5
    Gp = []
    for th in thetas:
        M = np.zeros((nW, nW))
        for a, (pa, sa) in enumerate(words):
            for b, (pb, sb) in enumerate(words):
                fp = 0.5 * (R(pa, th + h, sb) + R(pb, th + h, sa))
                fm = 0.5 * (R(pa, th - h, sb) + R(pb, th - h, sa))
                M[a, b] = (fp - fm) / (2 * h)
        Gp.append(M)
    return G, Gp


def loewner(G, Gp, thetas):
    m, nW = len(thetas), G[0].shape[0]
    L = np.zeros((m * nW, m * nW))
    for i in range(m):
        for j in range(m):
            blk = Gp[i] if i == j else (G[i] - G[j]) / (thetas[i] - thetas[j])
            L[i * nW:(i + 1) * nW, j * nW:(j + 1) * nW] = blk
    return (L + L.T) / 2


def score(L):
    """Return (psd_plus, psd_minus, lam_min_of_better_sign)."""
    scale = max(1.0, np.abs(L).max())
    ev = np.linalg.eigvalsh(L)
    lo_p, lo_m = ev.min(), (-ev).min()
    return (lo_p >= -TOL_ABS * scale, lo_m >= -TOL_ABS * scale, max(lo_p, lo_m))


def run(variant, mode, trials, seed, words, thetas):
    rng = np.random.default_rng(seed)
    n_plus = n_minus = n_viol = 0
    worst = np.inf
    for _ in range(trials):
        if variant == "A":
            G, Gp = variant_a_response(rng, thetas, words, mode=mode)
        else:
            G, Gp = variant_b_response(rng, thetas, words, mode=mode)
        p, m, lam = score(loewner(G, Gp, thetas))
        n_plus += p
        n_minus += m
        if not (p or m):
            n_viol += 1
        worst = min(worst, lam)
    return {"plus": n_plus, "minus": n_minus, "viol": n_viol,
            "worst": worst, "trials": trials}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260726)
    ap.add_argument("--grid", type=int, default=4)
    args = ap.parse_args()

    # words = (prefix, suffix) pairs with |prefix| + |suffix| <= 1  (p = 1, n = 3)
    words = [("", ""), ("a", ""), ("", "a"), ("b", "")]
    thetas_a = np.linspace(0.15, 1.05, args.grid)
    thetas_b = np.linspace(0.20, 1.40, args.grid)

    print("WPOT Stage A -- word-domain passivity null identity")
    print(f"trials={args.trials} grid={args.grid} words={len(words)} "
          f"tol={TOL_ABS}")
    print("frozen rule: PASS iff passive violations == 0 AND one fixed sign "
          "works for every passive trial; controls must violate.\n")

    for variant, thetas in (("A", thetas_a), ("B", thetas_b)):
        label = ("hamiltonian intervention, unitary sys+Gibbs bath"
                 if variant == "A" else
                 "thermal-contact duration, KMS detailed-balance GKSL")
        print(f"=== Variant {variant}: {label}")
        print(f"{'mode':<12}{'trials':>7}{'PSD(+L)':>9}{'PSD(-L)':>9}"
              f"{'violate':>9}{'worst lam':>13}")
        for k, mode in enumerate(("passive", "inverted", "gain", "negweight")):
            r = run(variant, mode, args.trials, args.seed + 1000 * k + hash(variant) % 97,
                    words, thetas)
            print(f"{mode:<12}{r['trials']:>7}{r['plus']:>9}{r['minus']:>9}"
                  f"{r['viol']:>9}{r['worst']:>13.3e}")
        print()


if __name__ == "__main__":
    main()
