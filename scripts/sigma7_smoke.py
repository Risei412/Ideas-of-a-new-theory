#!/usr/bin/env python3
"""
Step 2 smoke: what sigma_7 is reachable on ideal (noiseless) data?

Response model (SMRT/RISEI shape):
    R(w) = p^dag M_{w_k} ... M_{w_1} c        w = intervention word

Hankel matrix over prefix/suffix words of length <= 2:
    H[u, v] = R(u . v)                        words of length <= 4
    H_cal   = H[:1+m, :1+m]                   words of length <= 2

Certificate target (P0-D):  rank(H_cal) <= 6  and  sigma_7(H_full) > tau_H.

Reports the scale-free ratio sigma_7/sigma_1, which is what the construction
controls, alongside the absolute sigma_1 needed to clear tau_H.
"""
import argparse, itertools, math
import numpy as np


def words_upto(m, L):
    out = [()]
    for k in range(1, L + 1):
        out += list(itertools.product(range(m), repeat=k))
    return out


def response(word, Ms, c, p):
    v = c.copy()
    for u in word:                 # applied left to right in time
        v = Ms[u] @ v
    return float(p @ v)


def hankel(m, Ms, c, p, half=2):
    idx = words_upto(m, half)
    H = np.empty((len(idx), len(idx)))
    for i, u in enumerate(idx):
        for j, v in enumerate(idx):
            H[i, j] = response(u + v, Ms, c, p)
    return H, idx


def random_realization(r, m, rng, norm="opnorm"):
    """Random r-dimensional realization.

    norm='opnorm'   : ||M_u||_2 = 1  -- contraction, the physical (CPTP-like)
                      choice; guarantees |R(w)| <= 1 at every depth.
    norm='spectral' : spectral radius 1 -- non-normal products can grow, so
                      entries exceed 1. Kept only for comparison.
    """
    Ms = []
    for _ in range(m):
        A = rng.standard_normal((r, r))
        A /= (np.linalg.norm(A, 2) if norm == "opnorm"
              else max(abs(np.linalg.eigvals(A))))
        Ms.append(A)
    c = rng.standard_normal(r); c /= np.linalg.norm(c)
    p = rng.standard_normal(r); p /= np.linalg.norm(p)
    return Ms, c, p


def nested_sigma7(m, Ms0, Ms1, c, p, iters=60):
    """Continue along (1-t)Ms0 + t Ms1 to a point where det(H_cal) = 0,
    then return the singular values of the full Hankel there.

    This is the certificate geometry: rank(H_cal) <= 6 while sigma_7(H_full)
    stays above tau_H. Returns None if no sign change brackets a root.
    """
    def f(t):
        Ms = [(1 - t) * A + t * B for A, B in zip(Ms0, Ms1)]
        H, _ = hankel(m, Ms, c, p)
        return np.linalg.det(H[:1 + m, :1 + m]), H

    d0, _ = f(0.0)
    d1, _ = f(1.0)
    if np.sign(d0) == np.sign(d1):
        return None
    lo, hi = 0.0, 1.0
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        dm, _ = f(mid)
        if np.sign(dm) == np.sign(d0):
            lo = mid
        else:
            hi = mid
    _, H = f(0.5 * (lo + hi))
    return np.linalg.svd(H, compute_uv=False)


def tau_H(N, shots, conservative=False):
    """Perturbation bound ||dH||_2 for iid entry noise (random-matrix estimate)."""
    sigma_entry = (1.0 / math.sqrt(shots)) if conservative else (0.5 / math.sqrt(shots))
    return 2.0 * math.sqrt(N) * sigma_entry


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, default=6)
    ap.add_argument("--trials", type=int, default=200)
    ap.add_argument("--shots", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20260723)
    a = ap.parse_args()

    rng = np.random.default_rng(a.seed)
    m, ncal = a.m, 1 + a.m
    N = len(words_upto(m, 2))
    t_tight = tau_H(N, a.shots)
    t_cons = tau_H(N, a.shots, conservative=True)

    print(f"m={m}  Hankel {N}x{N}  (H_cal = {ncal}x{ncal})  shots/setting={a.shots}")
    print(f"tau_H = {t_tight:.4f} (tight, sigma_entry=1/(2*sqrt(n)))"
          f" / {t_cons:.4f} (conservative, 1/sqrt(n))")
    print(f"safety criterion sigma_7 >= 2*tau_H = {2*t_tight:.4f} / {2*t_cons:.4f}\n")

    print(f"{'rank r':>7}{'sigma_1':>11}{'sigma_7':>11}{'s7/s1':>11}"
          f"{'rank(H)':>9}{'需要 sigma_1':>14}")
    for r in (6, 7, 8, 10, 12):
        s1s, s7s, ratios, ranks = [], [], [], []
        for _ in range(a.trials):
            Ms, c, p = random_realization(r, m, rng)
            H, _ = hankel(m, Ms, c, p)
            s = np.linalg.svd(H, compute_uv=False)
            s1s.append(s[0]); s7s.append(s[6] if len(s) > 6 else 0.0)
            ratios.append(s[6] / s[0] if len(s) > 6 and s[0] > 0 else 0.0)
            ranks.append(int(np.linalg.matrix_rank(H, tol=1e-10)))
        med_ratio = float(np.median(ratios))
        need_s1 = (2 * t_tight / med_ratio) if med_ratio > 0 else float("inf")
        print(f"{r:>7}{np.median(s1s):>11.4f}{np.median(s7s):>11.3e}"
              f"{med_ratio:>11.3e}{int(np.median(ranks)):>9}{need_s1:>14.1f}")

    print("\n（sigma_1 は realization の正規化に比例。s7/s1 が構造で決まる不変量）")
