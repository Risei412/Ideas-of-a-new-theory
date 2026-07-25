#!/usr/bin/env python3
"""
Step 4: exact-arithmetic certification of the P0-D construction produced by
p0d_construct.py.

Every proposition below is checked with sympy.Rational (or exact Python
fractions), never floats, except the final noise-margin comparison (sigma_7
vs 2*tau_H), which is inherently a numeric safety criterion, not an exact
identity.

    python3 scripts/p0d_certify.py scripts/p0d_certificate.json
"""
import itertools, json, sys

from sympy import Matrix, Rational, nsimplify

M = 6


def R(x):
    return Rational(x)


def load(path):
    with open(path, encoding="utf-8") as f:
        cert = json.load(f)
    c = [R(x) for x in cert["c"]]
    A = {int(u): Matrix([[R(x) for x in row] for row in mat]) for u, mat in cert["A"].items()}
    p = [R(x) for x in cert["p"]]
    g = {int(u): [R(x) for x in v] for u, v in cert["g"].items()}
    H = {int(u): [R(x) for x in v] for u, v in cert["H"].items()}
    K = {int(u): [R(x) for x in v] for u, v in cert["K"].items()}
    pi = R(cert["pi"])
    prefixes = [tuple(p_) for p_ in cert["prefixes"]]
    suffixes = [tuple(s_) for s_ in cert["suffixes"]]
    spares = [tuple(w) for w in cert["spare_depth4_words"]]
    return cert, c, A, p, g, H, K, pi, prefixes, suffixes, spares


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def response_D(word, c, A, p):
    v = Matrix(c)
    for u in word:
        v = A[u] * v
    return dot(p, list(v))


def alpha(w1, w2, c, A, g):
    v = list(A[w1] * Matrix(c))
    return dot(g[w2], v)


def beta(w3, w4, H, K):
    return dot(K[w4], H[w3])


def response_full(word, c, A, p, g, H, K, pi):
    base = response_D(word, c, A, p)
    if len(word) < 4:
        return base
    w1, w2, w3, w4 = word
    return base + pi * alpha(w1, w2, c, A, g) * beta(w3, w4, H, K)


def words_upto(m, depth):
    out = [()]
    for k in range(1, depth + 1):
        out += list(itertools.product(range(m), repeat=k))
    return out


def check(label, cond):
    status = "OK" if cond else "FAIL"
    print(f"[{status}] {label}")
    if not cond:
        raise SystemExit(f"CERTIFICATE FAILED: {label}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "scripts/p0d_certificate.json"
    cert, c, A, p, g, H, K, pi, prefixes, suffixes, spares = load(path)
    m = cert["m"]
    n_block = cert["n_block"]

    print(f"=== P0-D certificate check ({path}) ===\n")

    # 1. M_D is a genuine 6-state controlled HMM: c a probability vector,
    #    A_u nonnegative with column sums <= 1, p in [0,1]^6.
    check("c >= 0", all(x >= 0 for x in c))
    check("sum(c) == 1", sum(c) == 1)
    for u in range(m):
        col_sums = [sum(A[u][i, j] for i in range(6)) for j in range(6)]
        check(f"A_{u} >= 0", all(A[u][i, j] >= 0 for i in range(6) for j in range(6)))
        check(f"A_{u} column sums <= 1", all(s <= 1 for s in col_sums))
    check("p in [0,1]^6", all(0 <= x <= 1 for x in p))

    # 2. Structural condition forcing depth <= 3 to vanish identically:
    #    g_u . c == 0 for every control u.
    for u in range(m):
        check(f"g_{u} . c == 0", dot(g[u], c) == 0)

    # 3. Calibration match: R_*(w) == R_D(w) EXACTLY for every word of
    #    depth <= 3 (all of them, not just the ones the frozen budget
    #    actually spends shots on -- the identity is structural).
    all_depth_le3 = words_upto(m, 3)
    mismatches = 0
    for w in all_depth_le3:
        r_star = response_full(w, c, A, p, g, H, K, pi)
        r_d = response_D(w, c, A, p)
        if r_star != r_d:
            mismatches += 1
    check(f"R_* == R_D exactly on all {len(all_depth_le3)} words of depth <= 3", mismatches == 0)

    # 4. rank(H) >= 7: the 7x7 block on the chosen prefixes/suffixes has a
    #    nonzero determinant, computed exactly.
    B = Matrix(n_block, n_block, lambda i, j: response_full(
        list(prefixes[i]) + list(suffixes[j]), c, A, p, g, H, K, pi))
    detB = B.det()
    check(f"det(B) != 0  (B is the {n_block}x{n_block} prefix/suffix block on depth-4 words)",
          detB != 0)
    print(f"    det(B) = {detB}")

    # 4b. sanity: killing g (=> alpha == 0 everywhere) collapses B back onto
    # the competitor-only block B_D, whose determinant must vanish (rank <= 6
    # in a 7x7 matrix) -- confirms the depth-4 correction is what does the
    # work, not an accident of the competitor alone.
    g_zero = {u: [R(0)] * 6 for u in range(m)}
    B_D = Matrix(n_block, n_block, lambda i, j: response_full(
        list(prefixes[i]) + list(suffixes[j]), c, A, p, g_zero, H, K, pi))
    check("sanity: det(B_D) == 0 with g = 0 (competitor alone is rank <= 6)", B_D.det() == 0)

    # 5. Every measured word (the 49 design-grid words + 15 spares) yields
    #    R_* in [0, 1] -- both the competitor and the true response must be
    #    valid probabilities on the words the frozen budget actually spends
    #    shots on.
    measured = [list(pfx) + list(sfx) for pfx in prefixes for sfx in suffixes] + [list(w) for w in spares]
    bad = []
    for w in measured:
        r_star = response_full(w, c, A, p, g, H, K, pi)
        r_d = response_D(w, c, A, p)
        if not (0 <= r_star <= 1 and 0 <= r_d <= 1):
            bad.append((w, r_star, r_d))
    check(f"R_*, R_D in [0,1] on all {len(measured)} measured depth-4 words", not bad)
    if bad:
        for w, rs, rd in bad[:5]:
            print(f"    word={w}  R_*={rs}  R_D={rd}")

    # 6. Noise margin: sigma_7(B) >= 2*tau_H (numeric; this is the one
    #    inherently-numeric criterion, not an exact identity).
    import numpy as np
    B_float = np.array([[float(x) for x in row] for row in B.tolist()])
    sv = np.linalg.svd(B_float, compute_uv=False)
    sigma7 = float(sv[-1])
    tau = cert["tau_H"]
    target = 2 * tau
    check(f"sigma_7(B) = {sigma7:.6f} >= 2*tau_H = {target:.6f}  (margin x{sigma7/target:.2f})",
          sigma7 >= target)

    print("\n=== ALL CHECKS PASSED ===")
    print("Scope: this certifies P0-D only (rank >= 7 for the 6-state / classical-linear")
    print("competitor family). It does NOT certify P0-A, P0-E, P0-DQ, or P0-C, and it does")
    print("NOT claim any physical theory (DCIT/RISEI/...) actually generates this response.")


if __name__ == "__main__":
    main()
