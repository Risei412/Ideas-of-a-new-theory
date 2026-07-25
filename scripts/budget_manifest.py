#!/usr/bin/env python3
"""
Budget manifest generator for the P0 certificate campaign.

Enumerates every measurement as a (protocol, readout setting) pair — the atomic
budget unit — and reports the shot cost under the frozen policy.

Frozen policy (docs/p0-certificate-spec.md §4.5):
  - N_cal   <= 120,000 shots   (calibration only)
  - N_held  >= 128,000 shots   (independent; depth-4 x 64 protocols minimum)
  - 2000 shots is a per-setting CAP, not a flat value
  - m = 6 primary, m = 8 stress
  - protocol != measurement setting

Depth-4 selection (revised 2026-07-25, spec §4quater): the original version
of this script chose the 64 depth-4 protocols by `rng.shuffle`. That does not
reliably contain a prefix-suffix-closed 7x7 Hankel block (49 words), so the
rank-7 certificate built in p0d_construct.py/p0d_certify.py would generically
NOT be measurable under the frozen budget -- exactly the failure mode spec
§1 warns about ("just slicing data points into a table does not give a
Hankel submatrix"). Depth-4 words are now the P0D_PREFIXES x P0D_SUFFIXES
design grid (49 words) used by the certificate, plus 15 additional seed-fixed
spare words for m=6; for other m the script falls back to the old random
selection with a warning, since the certificate is currently frozen at m=6.

Usage:
    python3 scripts/budget_manifest.py --m 6 --settings 2 --out docs/budget-manifest.csv
"""
import argparse, csv, itertools, math, random, sys

SEED = 20260723           # frozen held-out sampling seed
CAP_PER_SETTING = 2000    # per-setting shot cap
N_CAL_MAX = 120_000
N_HELD_MIN = 128_000
RHO = 1.5                 # depth-2 calibration graph redundancy
N_DEPTH3_CAL = 24
N_DEPTH4_HELD = 64

# P0-D certificate design grid (scripts/p0d_construct.py, m=6 only): a
# prefix-suffix-closed 7x7 block, guaranteed measurable as a genuine Hankel
# submatrix. Kept as a literal copy (not an import) so this script has no
# hard dependency on p0d_construct.py / numpy at manifest-generation time.
P0D_PREFIXES = [(4, 0), (1, 0), (2, 0), (3, 0), (5, 1), (5, 0), (0, 1)]
P0D_SUFFIXES = [(2, 0), (2, 3), (2, 1), (2, 4), (2, 5), (3, 1), (3, 0)]

# shots per setting by split (two-tier allocation; all <= CAP_PER_SETTING)
SHOTS = {
    "cal":            2000,   # calibration
    "held_depth4":    2000,   # rank-revealing depth-4
    "held_aux":       1000,   # auxiliary held-out (depth-2/3 unused)
}


def words(m, depth, distinct_adjacent=True):
    """Ordered intervention words of the given depth."""
    out = []
    for w in itertools.product(range(m), repeat=depth):
        if distinct_adjacent and any(w[i] == w[i + 1] for i in range(len(w) - 1)):
            continue
        out.append(w)
    return out


def hankel_entries(w):
    """(prefix, suffix) splits the word populates in the Hankel matrix."""
    return [("".join(map(str, w[:i])) or "e", "".join(map(str, w[i:])) or "e")
            for i in range(len(w) + 1)]


def build(m, n_settings):
    rng = random.Random(SEED)
    rows, pid = [], 0

    def emit(word, split, n_set, shots_each):
        nonlocal pid
        pid += 1
        for s in range(n_set):
            rows.append({
                "id": f"P{pid:04d}S{s}",
                "split": split,
                "depth": len(word),
                "word": "-".join(map(str, word)),
                "order_index": s,
                "readout_setting": f"R{s}",
                "shots": shots_each,
                "hankel_entries": ";".join(f"{a}|{b}" for a, b in hankel_entries(word)),
            })

    # depth-1: all, calibration
    for w in words(m, 1):
        emit(w, "cal", n_settings, SHOTS["cal"])

    # depth-2: rho=1.5 connected graph, both orders -> calibration; rest -> held-out
    n_edges = math.ceil(RHO * (m - 1))
    all_edges = [(i, j) for i in range(m) for j in range(i + 1, m)]
    tree = [(i, i + 1) for i in range(m - 1)]                       # spanning tree
    extra = [e for e in all_edges if e not in tree]
    rng.shuffle(extra)
    cal_edges = tree + extra[: n_edges - len(tree)]
    cal_d2 = {p for (i, j) in cal_edges for p in ((i, j), (j, i))}  # both orders
    for w in words(m, 2):
        split = "cal" if w in cal_d2 else "held_aux"
        emit(w, split, n_settings, SHOTS["cal" if split == "cal" else "held_aux"])

    # depth-3: 24 seed-fixed -> calibration; rest -> held-out
    d3 = words(m, 3)
    rng.shuffle(d3)
    cal_d3 = set(d3[:N_DEPTH3_CAL])
    for w in d3:
        split = "cal" if w in cal_d3 else "held_aux"
        emit(w, split, n_settings, SHOTS["cal" if split == "cal" else "held_aux"])

    # depth-4: 64 held-out, rank-revealing. For m=6 use the P0-D certificate's
    # prefix-suffix-closed 7x7 design grid (49 words) plus 15 seed-fixed spare
    # words, so the measured set actually contains a Hankel submatrix (see
    # module docstring). For other m, no certificate design exists yet; fall
    # back to the old random selection with a warning.
    if m == 6:
        grid = [p_ + s_ for p_ in P0D_PREFIXES for s_ in P0D_SUFFIXES]
        assert len(grid) == 49 and len(set(grid)) == 49
        d4_rest = [w for w in words(m, 4) if w not in set(grid)]
        rng.shuffle(d4_rest)
        d4 = grid + d4_rest[: N_DEPTH4_HELD - len(grid)]
    else:
        print(f"WARNING: no P0-D design grid for m={m}; depth-4 protocols are "
              f"randomly selected and are NOT guaranteed to contain a Hankel "
              f"submatrix. The certificate scripts are frozen at m=6.", file=sys.stderr)
        d4 = words(m, 4)
        rng.shuffle(d4)
        d4 = d4[:N_DEPTH4_HELD]
    for w in d4:
        emit(w, "held_depth4", n_settings, SHOTS["held_depth4"])

    return rows


def summarize(rows, m, n_settings):
    agg = {}
    for r in rows:
        k = r["split"]
        a = agg.setdefault(k, {"settings": 0, "shots": 0, "protocols": set()})
        a["settings"] += 1
        a["shots"] += r["shots"]
        a["protocols"].add((r["depth"], r["word"]))
    cal = agg.get("cal", {"shots": 0})["shots"]
    d4 = agg.get("held_depth4", {"shots": 0})["shots"]
    aux = agg.get("held_aux", {"shots": 0})["shots"]

    print(f"\n=== m={m}, settings/protocol={n_settings} ===")
    print(f"{'split':>14}{'protocols':>11}{'settings':>10}{'shots':>12}")
    for k in ("cal", "held_depth4", "held_aux"):
        if k in agg:
            a = agg[k]
            print(f"{k:>14}{len(a['protocols']):>11}{a['settings']:>10}{a['shots']:>12,}")
    print(f"{'-'*47}")
    print(f"{'calibration':>14}{'':>11}{'':>10}{cal:>12,}  "
          f"{'OK' if cal <= N_CAL_MAX else 'OVER'} (cap {N_CAL_MAX:,})")
    print(f"{'held(depth4)':>14}{'':>11}{'':>10}{d4:>12,}  "
          f"{'OK' if d4 >= N_HELD_MIN else 'below min'} (min {N_HELD_MIN:,})")
    print(f"{'標準設計計':>13}{'':>11}{'':>10}{cal + d4:>12,}   (calibration + depth-4)")
    print(f"{'全held-out込':>12}{'':>11}{'':>10}{cal + d4 + aux:>12,}")
    return cal, d4, aux


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, default=6)
    ap.add_argument("--settings", type=int, default=2)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    rows = build(a.m, a.settings)
    summarize(rows, a.m, a.settings)

    if a.out:
        with open(a.out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"\nwrote {len(rows)} rows -> {a.out}")
