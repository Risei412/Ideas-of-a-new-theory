#!/usr/bin/env python3
"""
Step 3+4 construction: an explicit nested P0-D certificate.

Builds, in exact rational arithmetic, a matched pair on the same response
alphabet (m = 6):

  M_D   -- a genuine 6-state controlled HMM (competitor, calibration side)
  M_*   -- M_D extended by a 4-register chain (true response, full side)

By construction (see docs/p0-certificate-spec.md §4quater for the derivation):

  * R_*(w) == R_D(w) exactly for every word of depth <= 3  (calibration match)
  * the depth-4 deviation factors as a rank-1 outer product on the chosen
    7x7 prefix/suffix block:
        Delta(w1 w2 w3 w4) = alpha(w1, w2) * beta(w3, w4)
        B = B_D + alpha (x) beta,   rank(B_D) <= 6,   rank(B) <= 7
    and alpha, beta are chosen to align EXACTLY with B_D's zero singular
    direction (u7, v7), so B = B_D + s * u7 (x) v7 with the SAME singular
    vectors as B_D and a single changed singular value: sigma_7(B) = s
    exactly (to floating precision), sigma_i(B) = sigma_i(B_D) for i < 7.
    rank(B) = 7  <=>  s != 0  <=>  det(B) != 0.

Register chain (extra dims beyond the 6-state competitor):
  e1 (scalar)  : e1_t = g_{u_t} . x_{t-1}            (x_{t-1}: competitor state)
  e2 (2-vector): e2_t = H_{u_t} * e1_{t-1}            (outer product, e1 scalar)
  acc (scalar) : acc_t = K_{u_t} . e2_{t-1}           (dot product, e2 2-vector)
  readout adds  pi * acc_depth  to the competitor's own response.

g_u . c = 0 for every u (c = e_0, so g_u[0] = 0 suffices) forces e1_1 = 0,
which forces acc_3 = 0 identically -- this is what makes depth <= 3 match
the competitor with NO fitting, for any h/H, k/K, pi. Using a 2-dimensional
e2 (instead of a bare scalar relay) is what makes beta(w3,w4) = K_{w4}.H_{w3}
expressive enough to hit an arbitrary target on 7 chosen suffixes; a scalar
relay (beta = h_{w3}*k_{w4}, tried first) is provably infeasible for a
generic target because it forces beta(w3,w4)/beta(w3',w4) to be independent
of w4 -- see docs/p0-certificate-spec.md §4quater for the failed attempt.

Response convention (frozen 2026-07-25): R(w) = P(reference outcome | w) in
[0, 1] -- see spec §2 note. tau_H below uses the binomial bound
sigma_entry <= 1/(2 sqrt(n)) on that convention.
"""
import argparse, json
from fractions import Fraction as Fr

import numpy as np

M = 6                       # alphabet size (states 0..5, also used as controls)
STATES = 6                  # competitor dimension D_cl


def mixing_matrix(u):
    """A_u: column-stochastic, column j puts weight 9/10 on the shifted state
    (j+u+1) mod 6 and 1/50 on every other state (9/10 + 5*1/50 = 1).

    A pure permutation (weight 1 on the shift, 0 elsewhere) was tried first
    and rejected: it keeps every state vector a scaled basis vector, so
    R_D(word) collapses to a function of a single mod-6 sum and B_D
    degenerates well below rank 6. A weaker mix (2/3 primary) reaches rank 6
    but leaves B_D's smallest nonzero singular value too small (~0.06) for
    any depth-4 correction to lift sigma_7 of the full block above the noise
    threshold, since the correction only fills the block's exactly-zero 7th
    direction and cannot touch the other six (see docs/p0-certificate-spec.md
    §4quater for the swept comparison). A sharper mix keeps the state vector
    spread across all 6 coordinates (still rank 6) while conditioning the
    resulting Hankel block well enough (smallest nonzero singular value
    ~0.32) to clear the safety margin.
    """
    P = [[Fr(1, 50)] * STATES for _ in range(STATES)]
    for j in range(STATES):
        i = (j + u + 1) % STATES
        P[i][j] = Fr(9, 10)
    return P


def mat_vec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def transpose(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]


def to_float(x):
    return float(x.numerator) / float(x.denominator)


def build_competitor():
    """M_D: 6-state controlled HMM, columns of A_u stochastic (sum 1, hence
    substochastic in the spec's sense of column sum <= 1)."""
    c = [Fr(1)] + [Fr(0)] * (STATES - 1)          # start in state 0
    A = {u: mixing_matrix(u) for u in range(M)}
    # distinct per-state weights: p uniform would make R_D depend only on
    # depth (stochastic maps preserve the total mass sum), collapsing B_D to
    # rank 1. Distinct weights make R_D depend on which state holds the mass.
    p = [Fr(i + 1, 6) for i in range(STATES)]       # readout, values 1/6..1
    return c, A, p


def response_D(word, c, A, p):
    v = c
    for u in word:
        v = mat_vec(A[u], v)
    return dot(p, v)


def prefix_state_vec(c, A, w1, w2):
    """x(w1,w2) = A_{w2} A_{w1} c -- the state reached after the prefix."""
    v = mat_vec(A[w1], c)
    v = mat_vec(A[w2], v)
    return [to_float(x) for x in v]


def suffix_readout_vec(A, p, w3, w4):
    """y(w3,w4) = (A_{w4} A_{w3})^T p, so that B_D[i,j] = y_j . x_i."""
    v = mat_vec(transpose(A[w4]), p)
    v = mat_vec(transpose(A[w3]), v)
    return [to_float(x) for x in v]


PREFIXES = [(w1, w2) for w2 in (0, 1) for w1 in range(M) if w1 != w2]   # 10 candidates
SUFFIXES = [(w3, w4) for w3 in (2, 3) for w4 in range(M) if w4 != w3]   # 10 candidates


def pick_independent(pairs, vec_fn, n=7):
    """Greedily select n candidates maximizing the smallest singular value of
    the accumulated (state or readout) vector set.

    Taking the first n in list order is not safe: the competitor's
    realization is only 6-dimensional, and an arbitrary 7-subset of the 10
    candidates can collapse to rank < 6 (verified empirically), capping
    rank(B) below 7 regardless of the depth-4 correction.

    Maximizing rank alone is not enough either: a rank-6 B_D can still have
    a badly conditioned smallest *nonzero* singular value, which puts a
    ceiling on sigma_7(B) that the depth-4 correction cannot lift (verified
    empirically -- see docs/p0-certificate-spec.md §4quater). Greedily
    maximizing the smallest singular value of the accumulated set at every
    step pushes B_D towards a well-conditioned rank-6 block instead.
    """
    chosen, chosen_vecs = [], []
    remaining = list(pairs)
    while remaining and len(chosen) < n:
        best_idx, best_score = None, -1.0
        for idx, cand in enumerate(remaining):
            trial = np.array(chosen_vecs + [vec_fn(*cand)])
            s = np.linalg.svd(trial, compute_uv=False)
            score = s[-1]
            if score > best_score:
                best_score, best_idx = score, idx
        chosen.append(remaining.pop(best_idx))
        chosen_vecs.append(vec_fn(*chosen[-1]))
    return chosen


def build_block_D(c, A, p, prefixes, suffixes):
    return np.array([[to_float(response_D(list(pfx) + list(sfx), c, A, p)) for sfx in suffixes]
                      for pfx in prefixes])


def rationalize(x, max_den=10 ** 6):
    return Fr(x).limit_denominator(max_den)


def solve_g(c, A, prefixes, s_alpha, u7):
    """Solve g_0, g_1 (the only w2 values used by `prefixes`) exactly so that
    alpha(w1, w2) = g_{w2} . (A_{w1} c) hits s_alpha * u7[i] on prefixes[i].

    g_u is a length-6 vector with g_u[0] pinned to 0 (g_u . c = 0, c = e_0).
    For each w2 value, this is a linear system in the free 5 components of
    g_{w2}; solved with lstsq (exact if the equation count is <=5 and the
    target vectors are independent, which holds for this construction) and
    then rationalized. Unused controls get the zero vector.
    """
    g = {u: [Fr(0)] * STATES for u in range(M)}
    w2_values = sorted(set(w2 for _, w2 in prefixes))
    for w2 in w2_values:
        idxs = [i for i, (w1, ww2) in enumerate(prefixes) if ww2 == w2]
        rows = [mat_vec(A[prefixes[i][0]], c)[1:] for i in idxs]   # drop index 0 (pinned)
        rows = [[to_float(x) for x in r] for r in rows]
        targets = [s_alpha * u7[i] for i in idxs]
        sol, *_ = np.linalg.lstsq(np.array(rows), np.array(targets), rcond=None)
        for comp, val in zip(range(1, STATES), sol):
            g[w2][comp] = rationalize(val)
    return g


def solve_HK(prefixes, suffixes, s_beta, v7):
    """Solve H_u (2-vectors, u in {w3 values used}) and K_u (2-vectors, u in
    {w4 values used}) exactly so that beta(w3, w4) = K_{w4} . H_{w3} hits
    s_beta * v7[j] on suffixes[j].

    H_2, H_3 fixed to the orthogonal basis (1,0), (0,1) (any independent pair
    works; orthogonal keeps the K_u solves diagonal and exact by inspection).
    Each K_u then solves one linear equation per w3 branch it appears in --
    at most 2 equations in 2 unknowns, solved exactly with a rational
    Gaussian elimination (no lstsq / no rounding needed here).
    """
    w3_values = sorted(set(w3 for w3, _ in suffixes))
    assert len(w3_values) <= 2, "H_u basis is only set up for <=2 distinct w3 values"
    H = {u: [Fr(0), Fr(0)] for u in range(M)}
    basis = [Fr(1, 1), Fr(0, 1)], [Fr(0, 1), Fr(1, 1)]
    for w3, vec in zip(w3_values, basis):
        H[w3] = vec

    K = {u: [Fr(0), Fr(0)] for u in range(M)}
    w4_values = sorted(set(w4 for _, w4 in suffixes))
    for w4 in w4_values:
        eqs = []  # (H_w3 as list of Fr, target Fr)
        for j, (w3, ww4) in enumerate(suffixes):
            if ww4 == w4:
                eqs.append((H[w3], rationalize(s_beta * v7[j])))
        if len(eqs) == 1:
            Hv, tgt = eqs[0]
            # underdetermined (1 eq, 2 unknowns): pick the component aligned
            # with the nonzero entry of Hv, zero elsewhere.
            if Hv[0] != 0:
                K[w4] = [tgt / Hv[0], Fr(0)]
            else:
                K[w4] = [Fr(0), tgt / Hv[1]]
        elif len(eqs) == 2:
            (Ha, ta), (Hb, tb) = eqs
            det = Ha[0] * Hb[1] - Ha[1] * Hb[0]
            assert det != 0, "H_2, H_3 must be independent"
            # solve [[Ha0,Ha1],[Hb0,Hb1]] . [k0,k1]^T = [ta,tb]^T exactly
            k0 = (ta * Hb[1] - tb * Ha[1]) / det
            k1 = (Ha[0] * tb - Hb[0] * ta) / det
            K[w4] = [k0, k1]
        # len(eqs) == 0: control unused among our suffixes, leave K[w4] = 0
    return H, K


def alpha(w1, w2, c, A, g):
    return dot(g[w2], mat_vec(A[w1], c))


def beta(w3, w4, H, K):
    return dot(K[w4], H[w3])


def response_full(word, c, A, p, g, H, K, pi):
    """R_*(w) for any depth. Depths <=3 match R_D exactly (structurally, via
    g_u . c == 0); depth 4 adds the rank-1 term pi * alpha * beta."""
    base = response_D(word, c, A, p)
    if len(word) < 4:
        return base
    if len(word) == 4:
        w1, w2, w3, w4 = word
        return base + pi * alpha(w1, w2, c, A, g) * beta(w3, w4, H, K)
    raise ValueError("this construction is only specified up to depth 4")


def build_block_full(c, A, p, g, H, K, pi, prefixes, suffixes):
    return np.array([[to_float(response_full(list(pfx) + list(sfx), c, A, p, g, H, K, pi))
                       for sfx in suffixes] for pfx in prefixes])


def tau_H(n_dim, shots):
    sigma_entry = 0.5 / (shots ** 0.5)
    return 2.0 * (n_dim ** 0.5) * sigma_entry


def max_feasible_pi(c, A, p, g, H, K, all_depth4_words):
    """Largest pi (bisection over a rational grid) keeping R_*(w) in [0,1]
    for every measured depth-4 word (the 7x7 block plus spare words)."""
    lo, step = Fr(0), Fr(1, 4)
    best = Fr(0)
    for _ in range(50):
        cand = best + step
        ok = True
        for w in all_depth4_words:
            r = response_full(w, c, A, p, g, H, K, cand)
            if r < 0 or r > 1:
                ok = False
                break
        if ok:
            best = cand
        step /= 2
    return best


def spare_words(prefixes, suffixes, n=15):
    """Extra depth-4 held-out words (distinct-adjacent) outside the 7x7
    design grid, to fill budget_manifest.py's 64-word depth-4 split."""
    used = {tuple(p + s) for p in prefixes for s in suffixes}
    out = []
    for w1 in range(M):
        for w2 in range(M):
            if w1 == w2:
                continue
            for w3 in range(M):
                if w3 == w2:
                    continue
                for w4 in range(M):
                    if w4 == w3:
                        continue
                    w = (w1, w2, w3, w4)
                    if w not in used:
                        out.append(w)
                    if len(out) >= n:
                        return out
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, default=6)
    ap.add_argument("--shots", type=int, default=2000)
    ap.add_argument("--n_block", type=int, default=7)
    ap.add_argument("--out", default="scripts/p0d_certificate.json")
    args = ap.parse_args()
    assert args.m == M, "construction is currently frozen at m=6"

    c, A, p = build_competitor()
    prefixes = pick_independent(PREFIXES, lambda w1, w2: prefix_state_vec(c, A, w1, w2), args.n_block)
    suffixes = pick_independent(SUFFIXES, lambda w3, w4: suffix_readout_vec(A, p, w3, w4), args.n_block)

    B_D = build_block_D(c, A, p, prefixes, suffixes)
    U, S, Vt = np.linalg.svd(B_D)
    assert S[-1] < 1e-8, f"B_D is expected to be exactly rank {args.n_block - 1}, got sigma_min={S[-1]}"
    u7, v7 = U[:, -1], Vt[-1, :]

    tau = tau_H(args.n_block, args.shots)
    target = 2 * tau

    # alpha, beta aligned to the exact unit singular vectors (u7, v7); pi is
    # then the SOLE scale knob, and (with perfect alignment) sigma_7(B) = pi
    # exactly, since ||u7|| = ||v7|| = 1.
    g = solve_g(c, A, prefixes, 1.0, u7)
    H, K = solve_HK(prefixes, suffixes, 1.0, v7)

    spares = spare_words(prefixes, suffixes, n=15)
    all_words = [list(pfx) + list(sfx) for pfx in prefixes for sfx in suffixes] + [list(w) for w in spares]
    pi_max = max_feasible_pi(c, A, p, g, H, K, all_words)
    pi_use = pi_max * Fr(4, 5)   # 80% pad below the [0,1] boundary

    B = build_block_full(c, A, p, g, H, K, pi_use, prefixes, suffixes)
    sv = np.linalg.svd(B, compute_uv=False)
    sigma7 = float(sv[-1])

    print(f"prefixes = {prefixes}")
    print(f"suffixes = {suffixes}")
    print(f"singular values of B_D: {np.round(S, 6)}")
    print(f"pi_max (feasibility)   = {pi_max} ~= {to_float(pi_max):.6f}")
    print(f"pi used (80% pad)      = {pi_use} ~= {to_float(pi_use):.6f}")
    print(f"singular values of B (full block): {np.round(sv, 6)}")
    print(f"sigma_7(B) = {sigma7:.6f}")
    print(f"tau_H (n={args.n_block}, shots={args.shots}) = {tau:.6f}   safety target 2*tau_H = {target:.6f}")
    print("VERDICT:", "GO" if sigma7 >= target else "NO-GO", f"(margin x{sigma7/target:.2f})")

    # sanity: killing g (alpha == 0 everywhere) must degenerate rank back to <=6
    B_killed = build_block_full(c, A, p, {u: [Fr(0)] * STATES for u in range(M)}, H, K, pi_use, prefixes, suffixes)
    sv_killed = np.linalg.svd(B_killed, compute_uv=False)
    print(f"sanity (g=0): singular values -> {np.round(sv_killed, 6)}  "
          f"(expect sigma_7 ~ 0, since B_killed == B_D)")

    cert = {
        "m": M, "states": STATES, "n_block": args.n_block,
        "c": [str(x) for x in c],
        "A": {str(u): [[str(x) for x in row] for row in A[u]] for u in A},
        "p": [str(x) for x in p],
        "g": {str(u): [str(x) for x in g[u]] for u in range(M)},
        "H": {str(u): [str(x) for x in H[u]] for u in range(M)},
        "K": {str(u): [str(x) for x in K[u]] for u in range(M)},
        "pi": str(pi_use),
        "prefixes": prefixes,
        "suffixes": suffixes,
        "spare_depth4_words": spares,
        "shots_per_setting": args.shots,
        "tau_H": tau,
        "target_sigma7": target,
        "sigma7_achieved": sigma7,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(cert, f, ensure_ascii=False, indent=2)
    print(f"\nwrote certificate -> {args.out}")


if __name__ == "__main__":
    main()
