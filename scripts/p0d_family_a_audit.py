#!/usr/bin/env python3
"""
Family-A audit of the certified P0-D response.

The P0-D certificate (scripts/p0d_certificate.json) proves rank(H) >= 7, which
excludes classical/linear realizations of dimension <= 6 (competitor family D).
This script asks the separate question posed by docs/reduction-targets.md §A:

    does the same response carry ANY evidence against family A
    (hidden-ancilla GKSL, D_hidden <= 6)?

Family A's target object is the reachable-observable space

    K = span{ O, L_u^*(O), L_v^* L_u^*(O), ... }

whose response-side avatar is the row space of the generalized Hankel matrix,
saturated as the word depth grows. Any admissible enlarged-GKSL realization
with system dimension d and hidden dimension D_hidden obeys the coarse bound

    dim K <= (d * D_hidden)^2 .

So family A is excluded only if dim K > (d * D_hidden)^2. This script computes
dim K exactly (rational arithmetic, no floating-point rank tolerance) and
compares it against the frozen family-A budget.

    python3 scripts/p0d_family_a_audit.py scripts/p0d_certificate.json

IMPORTANT (docs/p0d-derivability-audit.md §3): a NEGATIVE outcome here means
"the certificate provides no evidence against family A", NOT "the response has
been reduced to family A". Establishing an actual reduction would require
exhibiting an admissible D_hidden <= 6 dilation, which this script does not do.
"""
import argparse
import itertools
import os
import sys

from sympy import Matrix

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # run from anywhere
from p0d_certify import load, response_full, response_D

D_HIDDEN_BUDGET = 6          # frozen family-A budget (docs/p0-certificate-spec.md §1)
SYSTEM_DIMS = (2, 3, 4, 5)   # qubit, qutrit, ...


def hankel_rank_at_depth(half, c, A, p, g, H, K, pi, m, use_full=True):
    """Exact rank of the Hankel block indexed by all words of length <= half.

    Entries are R(u . v), so the deepest word used is 2 * half. The
    construction is only specified up to depth 4, so half <= 2.
    """
    idx = [()]
    for k in range(1, half + 1):
        idx += list(itertools.product(range(m), repeat=k))
    resp = (lambda w: response_full(list(w), c, A, p, g, H, K, pi)) if use_full \
        else (lambda w: response_D(list(w), c, A, p))
    M = Matrix(len(idx), len(idx), lambda i, j: resp(idx[i] + idx[j]))
    return M.rank(), len(idx)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cert", nargs="?", default="scripts/p0d_certificate.json")
    a = ap.parse_args()

    cert, c, A, p, g, H, K, pi, prefixes, suffixes, spares = load(a.cert)
    m = cert["m"]

    print(f"=== Family-A audit of {a.cert} ===\n")

    # dim K: saturate the Hankel row space as the word depth grows. The
    # construction is specified up to depth 4, so half = 0, 1, 2 (words of
    # length <= 4). Saturation at half = 2 is what we report as dim K.
    print("Hankel rank vs prefix/suffix length (exact rational rank):")
    print(f"{'half':>6}{'block':>10}{'rank R_*':>11}{'rank R_D':>11}")
    dim_K = 0
    for half in (0, 1, 2):
        r_full, n = hankel_rank_at_depth(half, c, A, p, g, H, K, pi, m, use_full=True)
        r_comp, _ = hankel_rank_at_depth(half, c, A, p, g, H, K, pi, m, use_full=False)
        print(f"{half:>6}{f'{n}x{n}':>10}{r_full:>11}{r_comp:>11}")
        dim_K = max(dim_K, r_full)

    print(f"\ndim K (saturated reachable-observable dimension of R_*) = {dim_K}")
    print("  (the competitor M_D alone saturates at 6 -- that is the P0-D separation)")

    # Family-A budget comparison.
    print(f"\nFamily-A budget  dim K <= (d * D_hidden)^2  with D_hidden <= {D_HIDDEN_BUDGET}:")
    print(f"{'d':>4}{'system':>10}{'(d*6)^2':>10}{'dim K':>8}{'  verdict'}")
    excluded_any = False
    for d in SYSTEM_DIMS:
        budget = (d * D_HIDDEN_BUDGET) ** 2
        excluded = dim_K > budget
        excluded_any = excluded_any or excluded
        name = {2: "qubit", 3: "qutrit", 4: "ququart", 5: "ququint"}.get(d, f"d={d}")
        verdict = "EXCLUDES family A" if excluded else f"no evidence (need > {budget})"
        print(f"{d:>4}{name:>10}{budget:>10}{dim_K:>8}   {verdict}")

    # Minimum system dimension that can host the certificate at all.
    d_min = next(d for d in range(2, 64) if d * d >= dim_K)
    print(f"\nSmallest system dimension whose Liouville space can host dim K = {dim_K}:"
          f"  d = {d_min}  (d^2 = {d_min * d_min})")
    print(f"At that d, the family-A budget is ({d_min}*{D_HIDDEN_BUDGET})^2 = "
          f"{(d_min * D_HIDDEN_BUDGET) ** 2}, i.e. "
          f"{(d_min * D_HIDDEN_BUDGET) ** 2 / dim_K:.1f}x larger than dim K.")

    print("\n=== VERDICT ===")
    if excluded_any:
        print("The certificate excludes family A for at least one system dimension.")
    else:
        print("The P0-D certificate provides NO EVIDENCE against family A.")
        print("dim K falls below the family-A budget at every system dimension checked,")
        print("so the necessary condition dim K > (d*D_hidden)^2 is not met anywhere.")
        print()
        print("This is NOT a proof that the response reduces to family A -- no explicit")
        print("D_hidden <= 6 dilation has been constructed here. It says only that the")
        print("rank-7 obstruction is far too small to constrain hidden-ancilla models.")
        print("See docs/p0d-derivability-audit.md for what this implies for P0 overall.")


if __name__ == "__main__":
    main()
