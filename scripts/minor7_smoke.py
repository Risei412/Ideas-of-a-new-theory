#!/usr/bin/env python3
"""
Step 2bis smoke: move the finite-shot certificate from sigma_7(H_full) to the
smallest singular value of a single 7x7 submatrix of H_full.

Why: the 43x43 Hankel needs every word of length <= 4 (1555 words, 1296 of them
at depth 4). The frozen held-out budget funds 64 depth-4 protocols. A 7x7 minor
whose row and column words all have length 2 needs exactly 49 depth-4 words, so
it fits -- and it is the same object the exact-arithmetic minor certificate
(proposal 21, step B) already has to evaluate.

Two effects pull in opposite directions:
  - interlacing:  sigma_min(S) <= sigma_7(H_full)      -> harder on construction
  - noise:        tau_H ~ 2 sqrt(7) vs 2 sqrt(43)      -> lower threshold
This script measures which one wins.

Response model, normalization and nesting condition are identical to
sigma7_smoke.py:  R(w) = p^dag V_{w_k} ... V_{w_1} c,  ||V_u||_2 = 1,
nested certificate requires det(H_short) = 0 with H_short indexed by |w| <= 1.
"""
import argparse
import itertools
import math

import numpy as np
from scipy.linalg import qr


def words_upto(m, L):
    out = [()]
    for k in range(1, L + 1):
        out += list(itertools.product(range(m), repeat=k))
    return out


def response(word, Vs, c, p):
    v = c.copy()
    for u in word:
        v = Vs[u] @ v
    return float(p @ v)


def hankel(m, Vs, c, p, half=2):
    """H[u,v] = R(u.v), built from the realization factorization.

    With M_w = V_{w_k} ... V_{w_1} (letters applied left to right in time),
    concatenation gives M_{u.v} = M_v M_u, hence

        R(u.v) = p^T M_v M_u c = (M_v^T p) . (M_u c),

    so H = A B^T with A[u,:] = M_u c and B[v,:] = M_v^T p. This is exact and
    replaces |idx|^2 word evaluations by 2|idx| matrix-vector products. It also
    makes rank(H) <= r manifest.
    """
    idx = words_upto(m, half)
    A = np.empty((len(idx), c.size))
    B = np.empty((len(idx), p.size))
    for i, w in enumerate(idx):
        a, b = c.copy(), p.copy()
        for u in w:
            a = Vs[u] @ a
        for u in reversed(w):              # M_w^T p = V_{w_1}^T ... V_{w_k}^T p
            b = Vs[u].T @ b
        A[i], B[i] = a, b
    return A @ B.T, idx


def random_realization(r, m, rng):
    Vs = []
    for _ in range(m):
        A = rng.standard_normal((r, r))
        A /= np.linalg.norm(A, 2)          # opnorm (contraction) normalization
        Vs.append(A)
    c = rng.standard_normal(r); c /= np.linalg.norm(c)
    p = rng.standard_normal(r); p /= np.linalg.norm(p)
    return Vs, c, p


def depth2_block(H, idx, m):
    """Rows/cols restricted to words of length exactly 2.

    Every entry of this block is a depth-4 word, and distinct (row, col) pairs
    give distinct words, so a k x k minor costs exactly k^2 depth-4 protocols.
    """
    sel = [i for i, w in enumerate(idx) if len(w) == 2]
    return H[np.ix_(sel, sel)], sel


def select_minor(B, k=7):
    """Pick k rows and k columns of B by maximal-volume heuristic.

    Pivoted QR on the leading rank-k singular subspaces; this is the standard
    cheap surrogate for the maximum-volume submatrix.
    """
    U, _, Vt = np.linalg.svd(B, full_matrices=False)
    rows = qr(U[:, :k].T, pivoting=True)[2][:k]
    cols = qr(Vt[:k, :], pivoting=True)[2][:k]
    return np.sort(rows), np.sort(cols)


def minor_sigma7(H, idx, m, k=7):
    """sigma_7 of the selected k x k depth-2/depth-2 minor, plus the indices.

    rank >= 7 of the minor certifies rank(H_full) >= 7. For k = 7 this is the
    smallest singular value; for k = 8 it is the second smallest, and
    interlacing gives sigma_7(S_8) >= sigma_7(S_7) for S_7 a submatrix of S_8,
    so a larger minor can only help the numerator -- at the cost of a slightly
    larger noise threshold (2 sqrt(k) scaling) and k^2 depth-4 protocols.
    """
    B, sel = depth2_block(H, idx, m)
    rows, cols = select_minor(B, k)
    S = B[np.ix_(rows, cols)]
    return float(np.linalg.svd(S, compute_uv=False)[6]), (sel, rows, cols)


def det_short(H, m):
    """det of the nested block H_short: rows/cols are words of length <= 1."""
    return float(np.linalg.det(H[: 1 + m, : 1 + m]))


def project_nested(Vs, direction, m, c, p, span=1.0, samples=41, iters=60):
    """Move along `direction` until det(H_short) = 0. Returns None if unbracketed."""
    def at(s):
        return [A + s * D for A, D in zip(Vs, direction)]

    def f(s):
        H, _ = hankel(m, at(s), c, p)
        return det_short(H, m)

    grid = np.linspace(-span, span, samples)
    vals = [f(s) for s in grid]
    br = None
    for i in range(len(grid) - 1):
        if np.sign(vals[i]) != np.sign(vals[i + 1]):
            # prefer the bracket closest to s = 0 (smallest move)
            cand = (grid[i], grid[i + 1])
            if br is None or min(abs(cand[0]), abs(cand[1])) < min(abs(br[0]), abs(br[1])):
                br = cand
    if br is None:
        return None
    lo, hi = br
    flo = f(lo)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if np.sign(f(mid)) == np.sign(flo):
            lo = mid
        else:
            hi = mid
    return at(0.5 * (lo + hi))


def renorm(Vs):
    return [A / np.linalg.norm(A, 2) for A in Vs]


def tau_H(N, shots):
    """||dH||_2 estimate for iid entry noise, sigma_entry <= 1/(2 sqrt(shots))."""
    return 2.0 * math.sqrt(N) * (0.5 / math.sqrt(shots))


def nested_point(r, m, rng, c, p, tries=12):
    """Draw a random realization and project it onto {det H_short = 0}."""
    for _ in range(tries):
        Vs, _, _ = random_realization(r, m, rng)
        d, _, _ = random_realization(r, m, rng)
        out = project_nested(renorm(Vs), d, m, c, p)
        if out is not None:
            return renorm(out), d
    return None, None


def hill_climb(Vs, direction, m, c, p, rng, iters, k=7, step=0.05):
    """Perturb -> re-project onto det(H_short)=0 -> keep if sigma_min improved."""
    H, idx = hankel(m, Vs, c, p)
    best_val, _ = minor_sigma7(H, idx, m, k)
    best = Vs
    improved = 0
    for _ in range(iters):
        pert = [A + step * rng.standard_normal(A.shape) for A in best]
        out = project_nested(renorm(pert), direction, m, c, p)
        if out is None:
            continue
        out = renorm(out)
        H, idx = hankel(m, out, c, p)
        if abs(det_short(H, m)) > 1e-8:      # projection failed numerically
            continue
        val, _ = minor_sigma7(H, idx, m, k)
        if val > best_val:
            best_val, best, improved = val, out, improved + 1
    return best, best_val, improved


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, default=6)
    ap.add_argument("--r", type=int, default=7)
    ap.add_argument("--samples", type=int, default=40)
    ap.add_argument("--iters", type=int, default=120)
    ap.add_argument("--k", type=int, default=7)
    ap.add_argument("--seed", type=int, default=20260726)
    a = ap.parse_args()

    m, r, k = a.m, a.r, a.k
    rng = np.random.default_rng(a.seed)
    N_full = len(words_upto(m, 2))

    print(f"m={m}  r={r}   H_full {N_full}x{N_full}   minor {k}x{k} (depth-2 rows/cols)")
    print(f"depth-4 words: all = {m**4},  needed by one {k}x{k} minor = {k*k}"
          f"   (frozen held-out budget: 64)\n")

    print("threshold 2*tau_H:")
    for N, label in ((N_full, f"{N_full}x{N_full}"), (k, f"{k}x{k}")):
        row = [f"{2*tau_H(N, s):.4f} @{s}" for s in (2000, 1395, 1304)]
        print(f"  {label:>7}: " + "   ".join(row))
    print()

    # ---- random sampling on the nested set -------------------------------
    c = rng.standard_normal(r); c /= np.linalg.norm(c)
    p = rng.standard_normal(r); p /= np.linalg.norm(p)

    smins, s7s = [], []
    for _ in range(a.samples):
        Vs, _ = nested_point(r, m, rng, c, p)
        if Vs is None:
            continue
        H, idx = hankel(m, Vs, c, p)
        val, _ = minor_sigma7(H, idx, m, k)
        smins.append(val)
        s7s.append(float(np.linalg.svd(H, compute_uv=False)[6]))

    smins, s7s = np.array(smins), np.array(s7s)
    print(f"nested random sample (n={len(smins)}):")
    print(f"  sigma_7(minor)      :  median {np.median(smins):.4f}   "
          f"95% {np.quantile(smins, .95):.4f}   max {smins.max():.4f}")
    print(f"  sigma_7(H_full):       median {np.median(s7s):.4f}   "
          f"95% {np.quantile(s7s, .95):.4f}   max {s7s.max():.4f}")
    print(f"  interlacing minor <= sigma_7(H_full) holds: {bool(np.all(smins <= s7s + 1e-9))}")
    for shots in (2000, 1395):
        thr = 2 * tau_H(k, shots)
        print(f"  random pass rate vs minor threshold {thr:.4f} @{shots} shots: "
              f"{100*np.mean(smins >= thr):.1f}%")
    print()

    # ---- optimize --------------------------------------------------------
    best_val, best_Vs, best_dir = -1.0, None, None
    for _ in range(8):
        Vs, d = nested_point(r, m, rng, c, p)
        if Vs is None:
            continue
        H, idx = hankel(m, Vs, c, p)
        val, _ = minor_sigma7(H, idx, m, k)
        if val > best_val:
            best_val, best_Vs, best_dir = val, Vs, d
    print(f"best of random restarts: sigma_7(minor) = {best_val:.4f}")

    opt, opt_val, improved = hill_climb(best_Vs, best_dir, m, c, p, rng, a.iters, k)
    H, idx = hankel(m, opt, c, p)
    s_full = np.linalg.svd(H, compute_uv=False)
    print(f"after projected hill climbing ({a.iters} iters, {improved} improvements):")
    print(f"  sigma_7(minor)       = {opt_val:.4f}")
    print(f"  sigma_7(H_full)      = {s_full[6]:.4f}")
    print(f"  det(H_short)         = {det_short(H, m):.3e}   (nesting held)")
    print(f"  rank(H_full)         = {np.linalg.matrix_rank(H, tol=1e-10)}")
    print()
    print(f"verdict vs {k}x{k} thresholds:")
    for shots in (2000, 1395, 1304):
        thr = 2 * tau_H(k, shots)
        print(f"  {shots:>5} shots/setting: threshold {thr:.4f}  -> "
              f"{'CLEAR' if opt_val >= thr else 'FAIL'}")
