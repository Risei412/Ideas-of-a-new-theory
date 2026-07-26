"""
提案24（LKCT: Lifted-Kernel Crossover Theory）の予備スモーク。

目的: 保護核を持つ damping-shape operator D_0 に核持ち上げ摂動 eps*D_L を加えた
      2パラメータ族 A(Gamma, eps; z) = Gamma*(D_0 + eps*D_L) + B について、

  (T1) eps=0 端点: R(Gamma) -> R_inf、補正が +alpha_leak/Gamma（RISEI Schur-Zeno 整合）
  (T2) eps>0 固定端点: R = O(Gamma^{-1})（ガイド §4.2 no-go 7 の再現）
  (T3) 2-jet 公式 Delta_R ~= -u*kappa_lift + v*alpha_leak（u=Gamma*eps, v=1/Gamma）の
       精度と2次収束
  (T4) 保護回復稜線（restoration ridge）Gamma_ridge(eps) = sqrt(alpha_leak/(kappa_lift*eps))
       の「行列データのみからの盲予測」vs 数値ゼロ交差
  (T5) fan-identical pair: 指数構造（両端点の valuation・ブロック次元・D_0・B・p・c）が
       同一で、稜線の有無だけが異なる対の明示構成
       → 稜線の存在は tropical/fan データからは決定できないことの構成的証拠
  (T6) ランダム模型 500 例での稜線存在率（現象が測度ゼロでないことの確認）

注意: これは線形代数レベルのスモークである。GKSL/CPTP 物理実現は別工程（提案24 §5）。
      判定基準は実行前に固定: T1-T4 は相対誤差 < 5%、T5 は符号反転の成立、
      T6 は存在率が [5%, 95%] の内側（自明でも不可能でもない）。

seed: 20260726（§11.2 の seed 使い回し禁止に従い本提案用に新規割当。
      20260723 / 20260725 は既存候補で使用済み）
"""

import numpy as np

rng = np.random.default_rng(20260726)

K = 2   # protected (kernel) block dim
NF = 4  # fast block dim
N = K + NF


def build_model(rng):
    """D_0 (kernel dim K, semisimple), D_L (PSD lifting), B, p, c (P-supported)."""
    D0 = np.zeros((N, N))
    D0[K:, K:] = np.diag(rng.uniform(0.5, 2.0, NF))
    G = rng.standard_normal((N, N))
    DL = G @ G.T / N  # PSD; DL_PP generically PD -> lifts the kernel
    B = rng.standard_normal((N, N)) + 0.5 * np.eye(N)
    pP = rng.standard_normal(K)
    cP = rng.standard_normal(K)
    p = np.concatenate([pP, np.zeros(NF)])
    c = np.concatenate([cP, np.zeros(NF)])
    return D0, DL, B, p, c


def jet_data(D0, DL, B, p, c):
    """R_inf, kappa_lift, alpha_leak from matrix data only (no (Gamma,eps) scan)."""
    BPP = B[:K, :K]
    BPF = B[:K, K:]
    BFP = B[K:, :K]
    DF = D0[K:, K:]
    DLPP = DL[:K, :K]
    C_leak = BPF @ np.linalg.solve(DF, BFP)
    x = np.linalg.solve(BPP.T, p[:K])  # B_PP^{-T} p_P
    y = np.linalg.solve(BPP, c[:K])    # B_PP^{-1} c_P
    R_inf = p[:K] @ y
    kappa_lift = x @ (DLPP @ y)
    alpha_leak = x @ (C_leak @ y)
    return R_inf, kappa_lift, alpha_leak


def R(D0, DL, B, p, c, Gam, eps):
    A = Gam * (D0 + eps * DL) + B
    return p @ np.linalg.solve(A, c)


def find_zero_crossing(f, grid):
    vals = np.array([f(g) for g in grid])
    s = np.sign(vals)
    idx = np.where(s[:-1] * s[1:] < 0)[0]
    if len(idx) == 0:
        return None
    i = idx[0]  # first crossing
    # log-linear interpolation
    g1, g2, v1, v2 = grid[i], grid[i + 1], vals[i], vals[i + 1]
    t = v1 / (v1 - v2)
    return np.exp(np.log(g1) + t * (np.log(g2) - np.log(g1)))


def main():
    results = {}
    D0, DL, B, p, c = build_model(rng)
    R_inf, kap, alf = jet_data(D0, DL, B, p, c)
    print(f"model: R_inf={R_inf:+.6f}  kappa_lift={kap:+.6f}  alpha_leak={alf:+.6f}")

    # --- T1: eps=0 plateau + leakage slope alpha_leak ---
    Gam = 1e5
    dR = R(D0, DL, B, p, c, Gam, 0.0) - R_inf
    pred = alf / Gam
    e1 = abs(dR - pred) / abs(pred)
    results["T1"] = e1 < 0.05
    print(f"T1 eps=0 slope : dR={dR:+.3e} pred={pred:+.3e} relerr={e1:.2%} "
          f"-> {'PASS' if results['T1'] else 'FAIL'}")

    # --- T2: fixed eps>0, R = O(Gamma^{-1}) ---
    eps_fix = 1e-2
    r1 = R(D0, DL, B, p, c, 1e5, eps_fix)
    r2 = R(D0, DL, B, p, c, 1e6, eps_fix)
    ratio = r1 / r2  # should be ~10 if R ~ 1/Gamma
    results["T2"] = abs(ratio - 10.0) < 0.5
    print(f"T2 fixed-eps   : R(1e5)/R(1e6)={ratio:.3f} (expect ~10) "
          f"-> {'PASS' if results['T2'] else 'FAIL'}")

    # --- T3: 2-jet accuracy and 2nd-order convergence ---
    # point with u,v small and comparable: Gamma=1e4, eps chosen so u=v
    Gam3 = 1e4
    eps3 = 1.0 / Gam3**2          # u = Gam*eps = 1e-4 = v
    errs = []
    for s in (1.0, 0.5, 0.25):    # scale (u,v) jointly by s: Gam->Gam/s? no:
        # scale u,v by s keeping u=v: Gamma_s = Gam3/s, eps_s = s^2 * eps3
        Gs, es = Gam3 / s, eps3 * s * s
        u, v = Gs * es, 1.0 / Gs
        dR = R(D0, DL, B, p, c, Gs, es) - R_inf
        jet = -u * kap + v * alf
        errs.append(abs(dR - jet))
    order = np.log(errs[0] / errs[2]) / np.log(4.0)  # expect ~2
    e3 = errs[0] / abs(-Gam3 * eps3 * kap + alf / Gam3)
    results["T3"] = (e3 < 0.05) and (order > 1.5)
    print(f"T3 2-jet       : relerr={e3:.2%} conv-order={order:.2f} (expect ~2) "
          f"-> {'PASS' if results['T3'] else 'FAIL'}")

    # --- T4: ridge blind prediction (only if same-sign) ---
    if kap * alf > 0:
        offsets = []
        for eps4 in (1e-7, 1e-8, 1e-9):
            G_pred = np.sqrt(alf / (kap * eps4))
            grid = np.exp(np.linspace(np.log(G_pred / 30), np.log(G_pred * 30), 400))
            G_num = find_zero_crossing(
                lambda g: R(D0, DL, B, p, c, g, eps4) - R_inf, grid)
            off = abs(np.log(G_num / G_pred)) if G_num else np.inf
            offsets.append(off)
            print(f"   eps={eps4:.0e}: Gamma_pred={G_pred:.4e} Gamma_num="
                  f"{G_num:.4e} |log offset|={off:.4f}")
        results["T4"] = offsets[-1] < 0.05 and offsets[-1] <= offsets[0] + 1e-12
        print(f"T4 ridge blind : offsets shrink as eps->0: "
              f"{['%.4f' % o for o in offsets]} "
              f"-> {'PASS' if results['T4'] else 'FAIL'}")
    else:
        print("T4 ridge blind : model has kappa*alpha<0 (no ridge); "
              "covered by T5/T6 instead -> SKIP")
        results["T4"] = None

    # --- T5: fan-identical pair, ridge dichotomy by sign engineering ---
    # same D0, B, p, c; two PD liftings D_L^{(s)} with DL_PP = w w^T + delta*I,
    # w solving [x y]^T w = (1, s) for s = +1 / -1.
    BPP = B[:K, :K]
    x = np.linalg.solve(BPP.T, p[:K])
    y = np.linalg.solve(BPP, c[:K])
    M = np.column_stack([x, y]).T          # 2x2 (K=2)
    delta = 0.02
    FFblk = DL[K:, K:]                      # shared fast-block lifting
    pair = {}
    for s, lab in ((+1.0, "ridge"), (-1.0, "no-ridge")):
        w = np.linalg.solve(M, np.array([1.0, s]))
        DLs = np.zeros((N, N))
        DLs[:K, :K] = np.outer(w, w) + delta * np.eye(K)
        DLs[K:, K:] = FFblk
        _, kap_s, alf_s = jet_data(D0, DLs, B, p, c)
        exists = kap_s * alf_s > 0
        pair[lab] = (kap_s, alf_s, exists)
        print(f"   pair[{lab:8s}]: kappa={kap_s:+.4f} alpha={alf_s:+.4f} "
              f"ridge_exists={exists}")
    # alpha identical by construction (DL does not enter alpha_leak)
    same_alpha = abs(pair["ridge"][1] - pair["no-ridge"][1]) < 1e-12
    results["T5"] = pair["ridge"][2] and (not pair["no-ridge"][2]) and same_alpha
    print(f"T5 fan-id pair : dichotomy with identical alpha_leak "
          f"-> {'PASS' if results['T5'] else 'FAIL'}")

    # --- T4b: if T4 was skipped, run blind ridge prediction on the engineered
    #          ridge model from T5 (jet data from matrices only, then scan) ---
    if results["T4"] is None:
        w = np.linalg.solve(M, np.array([1.0, 1.0]))
        DLr = np.zeros((N, N))
        DLr[:K, :K] = np.outer(w, w) + delta * np.eye(K)
        DLr[K:, K:] = FFblk
        _, kr, ar = jet_data(D0, DLr, B, p, c)
        offsets = []
        for eps4 in (1e-7, 1e-8, 1e-9):
            G_pred = np.sqrt(ar / (kr * eps4))
            grid = np.exp(np.linspace(np.log(G_pred / 30), np.log(G_pred * 30), 400))
            G_num = find_zero_crossing(
                lambda g: R(D0, DLr, B, p, c, g, eps4) - R_inf, grid)
            off = abs(np.log(G_num / G_pred)) if G_num else np.inf
            offsets.append(off)
            print(f"   eps={eps4:.0e}: Gamma_pred={G_pred:.4e} Gamma_num="
                  f"{G_num:.4e} |log offset|={off:.4f}")
        results["T4"] = offsets[-1] < 0.05 and offsets[-1] <= offsets[0] + 1e-12
        print(f"T4b ridge blind (on T5 ridge model): offsets "
              f"{['%.4f' % o for o in offsets]} "
              f"-> {'PASS' if results['T4'] else 'FAIL'}")

    # --- T6: ensemble ridge-existence fraction ---
    n_exist = 0
    NENS = 500
    for _ in range(NENS):
        m = build_model(rng)
        _, k6, a6 = jet_data(*m)
        n_exist += (k6 * a6 > 0)
    frac = n_exist / NENS
    results["T6"] = 0.05 < frac < 0.95
    print(f"T6 ensemble    : ridge-existence fraction = {frac:.1%} (N={NENS}) "
          f"-> {'PASS' if results['T6'] else 'FAIL'}")

    print("\nverdict:", {k: v for k, v in results.items()})


if __name__ == "__main__":
    main()
