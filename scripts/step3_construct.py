#!/usr/bin/env python3
"""
Step 3: explicitly construct the nested pair (M_D, F_full) for the P0-D certificate.

The full process is itself a genuine 7-state controlled sub-Markov model:

    V_u >= 0 entrywise,  column sums <= 1,   c = ( b_0 , 0 ),  p = ( 1_6 , 0 )

so R(w) = p^T V_{w_k} ... V_{w_1} c lies in [0,1] for EVERY word, not just the
measured ones -- the construction corresponds to a physically realizable
process by fiat. (An earlier sign-free version produced R(w) < 0 on unmeasured
depth-4 words and was discarded.)

Writing V_u in blocks with S = 6 visible states and one hidden state,

    V_u = [ T_u   x_u ]
          [ f_u^T g_u ]

the calibration identity

    R(w) = 1^T T_{w_k} ... T_{w_1} b_0        for every |w| <= 2

holds *structurally* provided p_7 = 0 and f_u . b_0 = 0 for every u (verified
symbolically). With everything nonnegative, f_u . b_0 = 0 is exactly the
support condition

    supp(f_u)  disjoint from  supp(b_0),

so we split the visible states into SIGMA (carrying b_0) and its complement
(carrying the f_u). Consequences:

  (i)   M_D = (T_u, b_0) is a genuine 6-state sub-Markov model -- T_u is a
        submatrix of a substochastic matrix, so it is automatically
        nonnegative with column sums <= 1 -- and it reproduces the entire
        calibration set exactly. No fitting, no LP.
  (ii)  rank(H_cal) <= 6 is automatic: for |w| <= 1 the reachability vectors
        all lie in the 6-dim subspace {x_7 = 0}. No root finding is needed
        (unlike sigma7_smoke.py, which had to bisect for det(H_cal) = 0).
  (iii) the deviation first appears at |w| = 3 via (1^T x_t) * (f_v^T T_u b_0);
        the certificate is read at depth 4 on the 8x8 witness submatrix H_wit,
        which is what the frozen budget funds (64 depth-4 protocols).

Objective: maximize sigma_7(H_wit), target 2*tau_H(8) = 0.1265 at 2000
shots/setting.
"""
import argparse
import itertools
import math

import numpy as np
from scipy.linalg import qr

S = 6          # visible / classical states of the competitor M_D
R_DIM = 7      # dimension of the full realization
SIGMA = (0, 1, 2, 3)          # states carrying b_0        (set by --sigma-size)
SIGMA_C = (4, 5)              # states carrying the f_u (hidden-state entry)


def set_sigma(nsig):
    """Split the visible states into supp(b_0) and supp(f_u).

    They must be disjoint: that is exactly the nonnegative form of the ansatz
    condition f_u . b_0 = 0. The split is what forces the hidden state to be
    reached through a two-step bottleneck b_0 -> SIGMA_C -> hidden, which is
    the structural reason sigma_7 is parametrically small.
    """
    global SIGMA, SIGMA_C
    SIGMA = tuple(range(nsig))
    SIGMA_C = tuple(range(nsig, S))


def words_upto(m, L):
    out = [()]
    for k in range(1, L + 1):
        out += list(itertools.product(range(m), repeat=k))
    return out


class Params:
    """V (m,7,7) nonneg substochastic with V[u][6, SIGMA] = 0; b0 on SIGMA;
    pv (S,) readout on the visible states (p_7 = 0 always)."""

    def __init__(self, V, b0, pv):
        self.V, self.b0, self.pv = V, b0, pv

    def copy(self):
        return Params(self.V.copy(), self.b0.copy(), self.pv.copy())


def project(P, signed=False):
    np.clip(P.V, 0.0, None, out=P.V)
    P.V[:, S, list(SIGMA)] = 0.0                 # f_u vanishes on supp(b_0)
    cs = P.V.sum(axis=1)                         # (m, 7) column sums
    bad = cs > 1.0
    if bad.any():
        scale = np.where(bad, 1.0 / np.maximum(cs, 1e-15), 1.0)
        P.V *= scale[:, None, :]
    np.clip(P.b0, 0.0, None, out=P.b0)
    P.b0[list(SIGMA_C)] = 0.0
    P.b0[list(SIGMA)] = np.maximum(P.b0[list(SIGMA)], 1e-6)
    P.b0 /= P.b0.sum()
    if signed:
        np.clip(P.pv, -1.0, 1.0, out=P.pv)     # +/-1-valued observable
    else:
        P.pv[:] = 1.0                          # survival readout, R(w) in [0,1]
    return P


def vectors(P, m, half=2):
    c = np.concatenate([P.b0, [0.0]])
    p = np.concatenate([P.pv, [0.0]])
    idx = words_upto(m, half)
    A = np.empty((len(idx), R_DIM))
    B = np.empty((len(idx), R_DIM))
    for i, w in enumerate(idx):
        a, b = c.copy(), p.copy()
        for u in w:
            a = P.V[u] @ a
        for u in reversed(w):
            b = P.V[u].T @ b
        A[i], B[i] = a, b
    return A, B, idx


def select_minor(blk, k):
    U, _, Vt = np.linalg.svd(blk, full_matrices=False)
    rows = qr(U[:, :k].T, pivoting=True)[2][:k]
    cols = qr(Vt[:k, :], pivoting=True)[2][:k]
    return np.sort(rows), np.sort(cols)


def evaluate(P, m, k=8):
    A, B, idx = vectors(P, m)
    H = A @ B.T
    d2 = [i for i, w in enumerate(idx) if len(w) == 2]
    blk = H[np.ix_(d2, d2)]
    rows, cols = select_minor(blk, k)
    Wit = blk[np.ix_(rows, cols)]
    sv = np.linalg.svd(Wit, compute_uv=False)
    ncal = 1 + m
    Hcal = H[:ncal, :ncal]
    return sv[6], {
        "sv": sv,
        "rank_cal": int(np.linalg.matrix_rank(Hcal, tol=1e-10)),
        "rank_wit": int(np.linalg.matrix_rank(Wit, tol=1e-10)),
        "min_all": float(H.min()), "max_all": float(H.max()),
        "rows": [idx[d2[i]] for i in rows], "cols": [idx[d2[j]] for j in cols],
        "H": H, "idx": idx, "Wit": Wit,
    }


def readout_range(signed):
    """Width of the achievable range of R(w); sets the binomial noise scale."""
    return 2.0 if signed else 1.0


def calibration_residual(P, m):
    """max |R(w) - P_{M_D}(w)| over |w| <= 2 -- structural identity, so ~1e-16."""
    A, B, idx = vectors(P, m)
    H = A @ B.T
    pos = {w: i for i, w in enumerate(idx)}
    T = P.V[:, :S, :S]
    err = 0.0
    for u in words_upto(m, 1):
        for v in words_upto(m, 1):
            x = P.b0.copy()
            for t in (u + v):
                x = T[t] @ x
            err = max(err, abs(H[pos[u], pos[v]] - P.pv @ x))
    return err


def random_params(m, rng, signed=False):
    V = rng.random((m, R_DIM, R_DIM)) ** 2
    b0 = rng.random(S)
    pv = rng.standard_normal(S) if signed else np.ones(S)
    return project(Params(V, b0, pv), signed)


def hill_climb(P, m, k, rng, iters, signed=False, step0=0.10):
    best = P.copy()
    best_val, _ = evaluate(best, m, k)
    step = step0
    improved = 0
    for t in range(iters):
        cand = best.copy()
        cand.V += step * rng.standard_normal(cand.V.shape) * 0.25
        cand.b0 += step * rng.standard_normal(cand.b0.shape) * 0.05
        if signed:
            cand.pv += step * rng.standard_normal(cand.pv.shape) * 0.5
        project(cand, signed)
        val, _ = evaluate(cand, m, k)
        if val > best_val:
            best_val, best, improved = val, cand, improved + 1
        if t and t % 500 == 0:
            step *= 0.75
    return best, best_val, improved


def tau_H(N, shots, rng_width=1.0):
    """Operator-norm noise scale. Entry SE <= rng_width/(2 sqrt(shots))."""
    return 2.0 * math.sqrt(N) * (0.5 * rng_width / math.sqrt(shots))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, default=6)
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--restarts", type=int, default=12)
    ap.add_argument("--iters", type=int, default=2500)
    ap.add_argument("--seed", type=int, default=20260726)
    ap.add_argument("--save", type=str, default="")
    ap.add_argument("--sigma-size", type=int, default=4,
                    help="|supp(b_0)|; the rest of the visible states carry f_u")
    ap.add_argument("--signed", action="store_true",
                    help="allow a +/-1-valued readout (R(w) in [-1,1]); the "
                         "noise threshold doubles with the dynamic range")
    a = ap.parse_args()

    m, k = a.m, a.k
    set_sigma(a.sigma_size)
    rng = np.random.default_rng(a.seed)
    width = readout_range(a.signed)
    thr = 2 * tau_H(k, 2000, width)
    print(f"m={m}  visible states S={S}  realization dim r={R_DIM}")
    print(f"supp(b_0) = {SIGMA}   supp(f_u) = {SIGMA_C}")
    print(f"readout: {'signed, R(w) in [-1,1]' if a.signed else 'survival, R(w) in [0,1]'}"
          f"  -> entry SE <= {width}/(2 sqrt(n))")
    print(f"witness {k}x{k} (depth-2 rows/cols -> {k*k} depth-4 words)")
    print(f"target sigma_7(H_wit) >= 2*tau_H({k}) = {thr:.4f} @2000 shots/setting")
    print(f"scale-free requirement: sigma_7 / range >= {thr/width:.4f}\n")

    best, best_val, best_info = None, -np.inf, None
    for rs in range(a.restarts):
        P = random_params(m, rng, a.signed)
        P, val, imp = hill_climb(P, m, k, rng, a.iters, a.signed)
        print(f"  restart {rs:2d}: sigma_7 = {val:.5f}  ({imp:4d} improvements)")
        if val > best_val:
            best, best_val = P, val
    _, best_info = evaluate(best, m, k)

    info = best_info
    print(f"\nbest sigma_7(H_wit) = {best_val:.5f}   "
          f"{'CLEAR' if best_val >= thr else 'FAIL'} vs {thr:.4f}"
          f"   ({best_val/thr:.2f}x)")
    print(f"  scale-free  sigma_7/range = {best_val/width:.5f}  "
          f"(requirement {thr/width:.4f})")
    print(f"  rank(H_cal) = {info['rank_cal']}  (must be <= 6)")
    print(f"  rank(H_wit) = {info['rank_wit']}  (must be >= 7)")
    print(f"  singular values of H_wit: {np.array2string(info['sv'], precision=4)}")
    print(f"  R(w) range over the WHOLE 43x43 Hankel: "
          f"[{info['min_all']:.6f}, {info['max_all']:.6f}]  (must be within the readout range)")
    print(f"  calibration residual    : {calibration_residual(best, m):.3e}")
    print(f"  b0 = {np.array2string(best.b0, precision=4)}")

    if a.save:
        np.savez(a.save, V=best.V, b0=best.b0, sigma7=best_val, m=m, k=k,
                 pv=best.pv, signed=a.signed,
                 sigma=np.array(SIGMA), sigma_c=np.array(SIGMA_C))
        print(f"\nsaved -> {a.save}")
