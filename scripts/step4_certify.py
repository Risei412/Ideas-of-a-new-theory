#!/usr/bin/env python3
"""
Step 4: exact-arithmetic certification of the P0-D nested certificate.

Takes the float construction from step3_construct.py, rationalizes it, repairs
the two defining constraints exactly over Q, and then certifies -- with no
floating point anywhere in the certificate itself:

  C1  M_D is a genuine 6-state controlled sub-Markov model:
      T_u >= 0 entrywise, column sums <= 1, b_0 >= 0, 1^T b_0 = 1.
  C2  nesting / calibration: R(w) = 1^T T_{w_k}...T_{w_1} b_0 for every
      |w| <= 2, as an exact identity in Q (all 43 words).
  C3  rank(H_cal) <= 6, certified by det(H_cal) = 0 exactly.
  C4  rank(H_wit) >= 7, certified by a nonzero 7x7 minor of the 8x8 witness
      submatrix, evaluated exactly (Bareiss fraction-free determinant).
  C5  every measured value is a probability: 0 <= R(w) <= 1 exactly, over the
      43 calibration words and the 64 depth-4 witness words.

Only sigma_7(H_wit) is reported as a floating-point quantity -- it is a
numerical margin, not part of the exact claim (guide section 9).
"""
import argparse
import itertools
from fractions import Fraction

import math

import numpy as np
import sympy as sp
from scipy.linalg import qr

S = 6
R_DIM = 7


def words_upto(m, L):
    out = [()]
    for k in range(1, L + 1):
        out += list(itertools.product(range(m), repeat=k))
    return out


def rationalize(x, den):
    """Nearest rational with denominator `den`."""
    return sp.Rational(int(round(float(x) * den)), den)


def build_exact(npz, den):
    """Rationalize the nonnegative substochastic construction and repair the
    defining constraints exactly over Q."""
    m = int(npz["m"])
    sigma = [int(i) for i in npz["sigma"]]
    V = [sp.Matrix(R_DIM, R_DIM, lambda i, j: rationalize(npz["V"][u][i, j], den))
         for u in range(m)]
    b0 = sp.Matrix(S, 1, lambda i, j: rationalize(npz["b0"][i], den))
    pv = sp.Matrix(S, 1, lambda i, j: rationalize(npz["pv"][i], den))

    for u in range(m):
        for i in range(R_DIM):
            for j in range(R_DIM):
                if V[u][i, j] < 0:
                    V[u][i, j] = sp.Integer(0)
        for j in sigma:
            V[u][S, j] = sp.Integer(0)         # f_u vanishes on supp(b_0)
        for j in range(R_DIM):                 # column sums <= 1, exactly
            cs = sum(V[u][i, j] for i in range(R_DIM))
            if cs > 1:
                for i in range(R_DIM):
                    V[u][i, j] = V[u][i, j] / cs
    for i in range(S):
        if b0[i] < 0 or i not in sigma:
            b0[i] = sp.Integer(0)
    b0 = b0 / sum(b0)                          # exact, 1^T b0 = 1
    return m, V, b0, pv, sigma


def realization(m, V, b0, pv):
    c = sp.Matrix(list(b0) + [sp.Integer(0)])
    p = sp.Matrix(list(pv) + [sp.Integer(0)])              # p_7 = 0
    return V, c, p


def hankel_exact(m, V, c, p, half=2):
    idx = words_upto(m, half)
    A, B = [], []
    for w in idx:
        a, b = c[:, :], p[:, :]
        for u in w:
            a = V[u] * a
        for u in reversed(w):
            b = V[u].T * b
        A.append(list(a))
        B.append(list(b))
    A, B = sp.Matrix(A), sp.Matrix(B)
    return A * B.T, idx


def hmm_value(w, V, b0, pv):
    """The competitor's own value: 6-state block only."""
    v = b0
    for u in w:
        v = V[u][:S, :S] * v
    return (pv.T * v)[0]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", default="scratch_best.npz")
    ap.add_argument("--den", type=int, default=10**6,
                    help="denominator used to rationalize the float solution")
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--dump", type=str, default="",
                    help="write the exact rational model + certificate here")
    a = ap.parse_args()

    npz = np.load(a.npz)
    m, V, b0, pv, sigma = build_exact(npz, a.den)
    V, c, p = realization(m, V, b0, pv)
    print(f"m={m}  rationalized with denominator {a.den}\n")

    ok = True

    # ---- C1 ---------------------------------------------------------------
    T = [V[u][:S, :S] for u in range(m)]
    c1 = all(T[u][i, j] >= 0 for u in range(m) for i in range(S) for j in range(S))
    c1 &= all(sum(T[u][i, j] for i in range(S)) <= 1
              for u in range(m) for j in range(S))
    c1 &= all(b0[i] >= 0 for i in range(S)) and sum(b0) == 1
    c1full = all(V[u][i, j] >= 0 for u in range(m)
                 for i in range(R_DIM) for j in range(R_DIM))
    c1full &= all(sum(V[u][i, j] for i in range(R_DIM)) <= 1
                  for u in range(m) for j in range(R_DIM))
    print(f"C1 M_D is a genuine 6-state sub-Markov model : {'PASS' if c1 else 'FAIL'}")
    print(f"C1b full 7-state process is substochastic too: "
          f"{'PASS' if c1full else 'FAIL'}   (=> R(w) in [0,1] for EVERY word)")
    ok &= c1full
    ok &= c1

    # ---- Hankel over Q ----------------------------------------------------
    H, idx = hankel_exact(m, V, c, p)
    pos = {w: i for i, w in enumerate(idx)}
    ncal = 1 + m

    # ---- C2 ---------------------------------------------------------------
    bad = 0
    for u in words_upto(m, 1):
        for v in words_upto(m, 1):
            if H[pos[u], pos[v]] - hmm_value(u + v, V, b0, pv) != 0:   # exact rationals
                bad += 1
    print(f"C2 calibration identity on all {ncal**2} pairs (43 words)  : "
          f"{'PASS' if bad == 0 else f'FAIL ({bad} mismatches)'}")
    ok &= bad == 0

    # ---- C3 ---------------------------------------------------------------
    Hcal = H[:ncal, :ncal]
    dcal = Hcal.det(method="berkowitz")
    print(f"C3 det(H_cal) = 0  (rank <= 6)               : "
          f"{'PASS' if dcal == 0 else 'FAIL'}   det = {dcal}")
    ok &= dcal == 0

    # ---- C4 ---------------------------------------------------------------
    d2 = [i for i, w in enumerate(idx) if len(w) == 2]
    blk_f = np.array([[float(H[i, j]) for j in d2] for i in d2])
    U, _, Vt = np.linalg.svd(blk_f, full_matrices=False)
    rows = sorted(qr(U[:, :a.k].T, pivoting=True)[2][:a.k])
    cols = sorted(qr(Vt[:a.k, :], pivoting=True)[2][:a.k])
    Wit = sp.Matrix(a.k, a.k, lambda i, j: H[d2[rows[i]], d2[cols[j]]])

    # search a nonzero 7x7 minor inside the 8x8 witness (float-guided, exact check)
    Wf = np.array([[float(Wit[i, j]) for j in range(a.k)] for i in range(a.k)])
    found, minor_det, which = False, None, None
    for ri in itertools.combinations(range(a.k), 7):
        for ci in itertools.combinations(range(a.k), 7):
            if abs(np.linalg.det(Wf[np.ix_(ri, ci)])) < 1e-14:
                continue                                   # float pre-screen
            sub = Wit[list(ri), list(ci)]
            dd = sub.det(method="bareiss")                 # exact
            if dd != 0:
                found, minor_det, which = True, dd, (ri, ci)
                break
        if found:
            break
    print(f"C4 nonzero 7x7 minor of H_wit (exact)        : "
          f"{'PASS' if found else 'FAIL'}")
    if found:
        print(f"   rows {which[0]} cols {which[1]}")
        print(f"   det = {sp.nsimplify(minor_det)}")
        print(f"   det ~ {float(minor_det):.6e}")
    ok &= found

    # ---- C5 ---------------------------------------------------------------
    meas = [H[i, j] for i in range(ncal) for j in range(ncal)]
    meas += [Wit[i, j] for i in range(a.k) for j in range(a.k)]
    c5 = all(0 <= x <= 1 for x in meas)
    print(f"C5 all {len(meas)} measured values are probabilities in [0,1] : "
          f"{'PASS' if c5 else 'FAIL'}")
    ok &= c5

    # ---- numerical margin (not part of the exact claim) -------------------
    sv = np.linalg.svd(Wf, compute_uv=False)
    thr = 2 * (2 * math.sqrt(a.k) * (0.5 / math.sqrt(2000)))
    print(f"\nnumerical margin (NOT part of the exact claim):")
    print(f"  sigma_7(H_wit) = {sv[6]:.5f}   threshold 2*tau_H({a.k}) = {thr:.4f}"
          f"   -> {'CLEAR' if sv[6] >= thr else 'FAIL'}  ({sv[6]/thr:.2f}x)")
    print(f"  sigma_8        = {sv[7]:.3e}")

    print(f"\n{'=== EXACT PART COMPLETE (C1-C5) ===' if ok else '=== EXACT PART INCOMPLETE ==='}")
    print(f"{'=== FINITE-SHOT MARGIN (iii): ' + ('MET' if sv[6] >= thr else 'NOT MET') + ' ==='}")

    if a.dump:
        with open(a.dump, "w") as fh:
            fh.write("# Exact P0-D certificate -- rational data\n")
            fh.write(f"# source {a.npz}, rationalized with denominator {a.den}\n")
            fh.write(f"# m={m}  visible states S={S}  realization dim r={R_DIM}\n")
            fh.write(f"# supp(b_0) = {sigma}\n#\n")
            fh.write(f"# C1 6-state sub-Markov competitor      : {'PASS' if c1 else 'FAIL'}\n")
            fh.write(f"# C1b full 7-state substochastic         : {'PASS' if c1full else 'FAIL'}\n")
            fh.write(f"# C2 calibration identity (43 words)     : {'PASS' if bad == 0 else 'FAIL'}\n")
            fh.write(f"# C3 det(H_cal) = 0                      : {'PASS' if dcal == 0 else 'FAIL'}\n")
            fh.write(f"# C4 nonzero 7x7 minor of H_wit          : {'PASS' if found else 'FAIL'}\n")
            fh.write(f"# C5 all measured values in [0,1]        : {'PASS' if c5 else 'FAIL'}\n")
            fh.write(f"# (iii) sigma_7(H_wit) = {sv[6]:.6f} vs 2*tau_H(8) = {thr:.6f}"
                     f"  -> {sv[6]/thr:.3f}x  NOT MET\n#\n")
            fh.write(f"b_0 = {[str(x) for x in b0]}\n")
            fh.write(f"p_visible = {[str(x) for x in pv]}   (p_7 = 0)\n")
            for u in range(m):
                fh.write(f"\nV_{u} =\n")
                for i in range(R_DIM):
                    fh.write("  [" + ", ".join(str(V[u][i, j])
                             for j in range(R_DIM)) + "]\n")
            fh.write(f"\nwitness minor rows {which[0]} cols {which[1]}\n")
            fh.write(f"det = {minor_det}\n")
        print(f"\nexact model dumped -> {a.dump}")
