"""
提案24（LKCT）Step 1-2 / Gate N1: 三準位 Λ 系 GKSL の weak-probe 感受率と回復曲線。

目的（`docs/dark-ridge-calculation-plan.md` §24 Q1-Q3 の Priority 0 部分）:

  真の定常状態 rho^(0) を含む完全な Liouvillian 解に対し、

      F_disp(beta, gamma12) = Re( chi - chi_inf ) = 0
      F_abs (beta, gamma12) = Im( chi - chi_inf ) = 0

  の正の解（回復曲線）が存在するかを判定する。

なぜ凍結EIT §9.6 の閉形式では足りないか:
  §9.6 は rho^(0) = |g1><g1| を前提とする。実際の Λ 系では branching (Gamma1, Gamma2) と
  control による optical pumping で定常分布が g2 側へ移り、population inversion による
  利得（Im chi < 0）が起こりうる。吸収側稜線を禁じているのが受動性なのか単に
  rho^(0) の仮定なのかは、真の定常状態でしか分からない。

規約:
  - vectorization は列ではなく行スタック（C order）。`scripts/wpot_null_smoke.py`
    `_thermal_gksl` と同じ: L rho L^dag  <->  kron(L, conj(L))。
  - 判定に浮動小数点を使わない（`scripts/lkct_exact_audit.py` と同じ規律）。
    パラメータはすべて Rational、chi は Q(i) 係数の有理関数として扱う。
  - 符号規約: Im chi > 0 を吸収とする（control off・共鳴で Im chi = 1/(2*gamma_31) > 0 を確認）。

seed 不使用（決定論的スキャンのみ。乱数を使わない）。
"""

from __future__ import annotations

import itertools

import sympy as sp

# ---------------------------------------------------------------- 基本記号

I3 = sp.eye(3)
G1, G2, GAM12, OMC, DP, DELTA = sp.symbols(
    "Gamma_1 Gamma_2 gamma_12 Omega_c Delta_p delta", positive=True
)
BETA = sp.Symbol("beta", positive=True)  # beta = |Omega_c|^2 / 4

# 感受率の全体符号（§5.3: 零点位置に影響しない定数）。
# 本実装の probe 規約では rho^(1)_{eg1} = -(i/2) gamma_g / D となり、そのままでは
# Im chi < 0（利得）になってしまう。凍結EIT §9.6 と符号を揃え、
# 「Im chi > 0 = 吸収」（§4.3 の規約テスト）を満たすよう C_chi = -1 を採る。
C_CHI = sp.Integer(-1)

# 基底の順序: 0 = |g1>, 1 = |g2>, 2 = |e>
G1K, G2K, EK = 0, 1, 2


def ket_bra(a: int, b: int) -> sp.Matrix:
    M = sp.zeros(3, 3)
    M[a, b] = 1
    return M


# ---------------------------------------------------------------- モデル構築


def hamiltonian(delta_p, delta2, omega_c):
    """回転枠の H0（計算計画 §4.1）。probe は摂動として別扱い。"""
    return (
        -delta_p * ket_bra(EK, EK)
        - delta2 * ket_bra(G2K, G2K)
        + omega_c / 2 * ket_bra(EK, G2K)
        + omega_c / 2 * ket_bra(G2K, EK)
    )


def jump_operators(gamma1, gamma2, gamma12):
    """励起状態崩壊 2 本 + ground-state pure dephasing 1 本（§4.2）。"""
    return [
        sp.sqrt(gamma1) * ket_bra(G1K, EK),
        sp.sqrt(gamma2) * ket_bra(G2K, EK),
        sp.sqrt(gamma12 / 2) * (ket_bra(G1K, G1K) - ket_bra(G2K, G2K)),
    ]


def superop_commutator(H):
    """-i[H, .] を行スタック vectorization で。"""
    return -sp.I * (sp.Matrix(sp.kronecker_product(H, I3)) - sp.Matrix(sp.kronecker_product(I3, H.T)))


def superop_dissipator(L):
    LdL = L.conjugate().T @ L
    return (
        sp.Matrix(sp.kronecker_product(L, L.conjugate()))
        - sp.Rational(1, 2) * sp.Matrix(sp.kronecker_product(LdL, I3))
        - sp.Rational(1, 2) * sp.Matrix(sp.kronecker_product(I3, LdL.T))
    )


def liouvillian(delta_p, delta2, omega_c, gamma1, gamma2, gamma12):
    Lsup = superop_commutator(hamiltonian(delta_p, delta2, omega_c))
    for L in jump_operators(gamma1, gamma2, gamma12):
        Lsup = Lsup + superop_dissipator(L)
    return sp.simplify(Lsup)


def probe_superop():
    """V rho = -i[V_p, rho], V_p = (1/2)|e><g1|（§4.1、Omega_p の1次係数）。"""
    return superop_commutator(ket_bra(EK, G1K) / 2)


def vec_index(a: int, b: int) -> int:
    return 3 * a + b


# ---------------------------------------------------------------- 応答の計算


def _solve_with_trace(Lsup, rhs, trace_value):
    """trace 行を置換した constrained linear solve（計算計画 §5.2 の優先順位1）。"""
    A = sp.Matrix(Lsup)
    b = sp.Matrix(rhs)
    row = 0  # 置換する行（trace 制約で差し替える）
    for j in range(9):
        A[row, j] = 0
    for a in range(3):
        A[row, vec_index(a, a)] = 1
    b[row] = trace_value
    return A.LUsolve(b)


def susceptibility(params, rho0=None):
    """chi = rho^(1)_{e,g1}（C_chi = 1）。params は Rational/記号の dict。

    rho0 を渡すと定常状態を解かずにその状態を零次として使う（凍結EIT §9.6 との照合用）。
    """
    Lsup = liouvillian(
        params["Delta_p"], params["delta"], params["Omega_c"],
        params["Gamma_1"], params["Gamma_2"], params["gamma_12"],
    )
    if rho0 is None:
        rho0 = _solve_with_trace(Lsup, sp.zeros(9, 1), sp.Integer(1))
    rhs = -(probe_superop() @ rho0)
    rho1 = _solve_with_trace(Lsup, rhs, sp.Integer(0))
    return C_CHI * sp.together(sp.expand(rho1[vec_index(EK, G1K)])), rho0


# ---------------------------------------------------------------- 規約テスト


def rational_point(**over):
    p = {
        "Gamma_1": sp.Rational(1, 2),
        "Gamma_2": sp.Rational(1, 2),
        "gamma_12": sp.Rational(1, 100),
        "Omega_c": sp.Rational(3, 1),
        "Delta_p": sp.Rational(1, 5),
        "delta": sp.Rational(1, 7),
    }
    p.update(over)
    return p


def gate_s0():
    """S0 規約テスト（§4.3）と T0-T2（§18）。すべて exact。"""
    out = []
    p = rational_point()
    Lsup = liouvillian(p["Delta_p"], p["delta"], p["Omega_c"],
                       p["Gamma_1"], p["Gamma_2"], p["gamma_12"])

    # T0a: trace preservation  <=>  L^dagger(I) = 0  <=>  sum over "diagonal" rows
    tr_row = sp.zeros(1, 9)
    for a in range(3):
        tr_row += Lsup[vec_index(a, a), :]
    out.append(("T0a trace preservation", sp.simplify(tr_row) == sp.zeros(1, 9)))

    # T0b: Hermiticity preservation. rho -> rho^dag は vec 上で swap+conj。
    P = sp.zeros(9, 9)
    for a in range(3):
        for b in range(3):
            P[vec_index(a, b), vec_index(b, a)] = 1
    out.append(("T0b hermiticity preservation",
                sp.simplify(P @ Lsup.conjugate() @ P - Lsup) == sp.zeros(9, 9)))

    # T1: dephasing convention  d/dt rho_{g1g2} = -gamma_12 rho_{g1g2}
    Ldeph = superop_dissipator(jump_operators(0, 0, GAM12)[2])
    row = sp.simplify(Ldeph[vec_index(G1K, G2K), :])
    expected = sp.zeros(1, 9)
    expected[0, vec_index(G1K, G2K)] = -GAM12
    out.append(("T1 dephasing convention", sp.simplify(row - expected) == sp.zeros(1, 9)))

    # T2: dark state. gamma_12 = 0, delta = 0 で dark vector が定常。
    p2 = rational_point(gamma_12=sp.Integer(0), delta=sp.Integer(0), Delta_p=sp.Integer(0))
    L2 = liouvillian(p2["Delta_p"], p2["delta"], p2["Omega_c"],
                     p2["Gamma_1"], p2["Gamma_2"], p2["gamma_12"])
    dark = sp.zeros(9, 1)
    dark[vec_index(G1K, G1K)] = 1  # Omega_p = 0 のとき |g1> は control に結合しない
    out.append(("T2 dark state stationary", sp.simplify(L2 @ dark) == sp.zeros(9, 1)))

    # T3/T4: 凍結EIT §9.6 の閉形式との厳密照合（rho^(0) = |g1><g1| を固定した場合）。
    #   rho_eg1^(1) = (i/2) * gamma_g / [ (gamma_31 - i Delta_p) gamma_g + beta ]
    # 係数 (i Omega_p/2) のうち Omega_p は本実装では展開係数なので (i/2)。
    #   chi = (i/2) * gamma_g / [ (gamma_31 - i Delta_p) gamma_g + beta ],  gamma_g = gamma_12 - i delta
    # ただし gamma_31 は Gamma_e/2 ではなく Gamma_e/2 + gamma_12/4 になる:
    # ground-state dephasing L_phi は rho_{e g1} も gamma_12/4 で減衰させるためである。
    rho0_fixed = sp.zeros(9, 1)
    rho0_fixed[vec_index(G1K, G1K)] = 1
    p4 = dict(zip(
        ["Gamma_1", "Gamma_2", "gamma_12", "Omega_c", "Delta_p", "delta"],
        [G1, G2, GAM12, OMC, DP, DELTA],
    ))
    chi4, _ = susceptibility(p4, rho0=rho0_fixed)
    gamma_g = GAM12 - sp.I * DELTA
    for label, gamma31 in [
        ("Gamma_e/2 + gamma_12/4", (G1 + G2) / 2 + GAM12 / 4),
        ("Gamma_e/2 (naive)", (G1 + G2) / 2),
    ]:
        closed = (sp.I / 2) * gamma_g / ((gamma31 - sp.I * DP) * gamma_g + OMC**2 / 4)
        agree = sp.simplify(sp.cancel(chi4 - closed)) == 0
        out.append((f"T4 凍結EIT §9.6 閉形式と一致 [gamma_31 = {label}]"
                    + ("" if agree else "  <- 不一致は想定どおり"),
                    agree if "naive" not in label else not agree))

    # T3: 符号規約。control off・共鳴で Im chi = 1/(2 gamma_31) > 0（吸収）。
    # Omega_c = 0 では定常状態が非一意（g1/g2 population が独立に保存）なので、
    # T4 で確立した閉形式に代入して確認する。
    chi3 = sp.simplify(chi4.subs({OMC: 0, DP: 0, DELTA: 0}))
    out.append(("T3 sign convention (Im chi > 0 = absorption)",
                sp.simplify(chi3 - sp.I / (2 * ((G1 + G2) / 2 + GAM12 / 4))) == 0))

    return out


# ---------------------------------------------------------------- 回復曲線


def recovery_conditions(base):
    """
    beta = Omega_c^2/4 と gamma_12 を自由に残し、chi - chi_inf の Re/Im の
    分子（exact な多項式）を返す。
    """
    p = dict(base)
    p["Omega_c"] = 2 * sp.sqrt(BETA)
    p["gamma_12"] = GAM12
    chi, rho0 = susceptibility(p)
    chi = sp.simplify(sp.expand(chi))

    # chi_inf := lim_{beta -> oo} chi(beta, gamma_12 = 0)
    chi_dark = sp.simplify(chi.subs(GAM12, 0))
    chi_inf = sp.simplify(sp.limit(chi_dark, BETA, sp.oo))

    d = sp.simplify(sp.together(chi - chi_inf))
    num, den = sp.fraction(sp.cancel(d))
    num = sp.expand(num)
    den = sp.expand(den)

    re_num = sp.expand(sp.re(num) * sp.re(den) + sp.im(num) * sp.im(den))
    im_num = sp.expand(sp.im(num) * sp.re(den) - sp.re(num) * sp.im(den))
    return {
        "chi": chi,
        "chi_dark": chi_dark,
        "chi_inf": chi_inf,
        "F_disp_num": sp.simplify(re_num),   # Re(chi - chi_inf) の分子
        "F_abs_num": sp.simplify(im_num),    # Im(chi - chi_inf) の分子
        "rho0": rho0,
    }


def positive_roots_in_gamma(poly_expr, beta_value):
    """固定 beta で F(gamma_12) = 0 の正の実根を exact に数える。"""
    e = sp.simplify(poly_expr.subs(BETA, beta_value))
    if e == 0:
        return "identically zero"
    p = sp.Poly(sp.expand(sp.numer(sp.cancel(sp.together(e)))), GAM12)
    if p.degree() == 0:
        return []
    roots = sp.real_roots(p)
    return [r for r in roots if r.is_positive]


def classify(base, betas):
    res = recovery_conditions(base)
    disp, absb = [], []
    for b in betas:
        disp.append(positive_roots_in_gamma(res["F_disp_num"], b))
        absb.append(positive_roots_in_gamma(res["F_abs_num"], b))
    has_d = any(isinstance(r, list) and r for r in disp)
    has_a = any(isinstance(r, list) and r for r in absb)
    cls = {(True, True): "D+A", (True, False): "D only",
           (False, True): "A only", (False, False): "none"}[(has_d, has_a)]
    return cls, res, disp, absb


# ---------------------------------------------------------------- 実行


def no_go_proof():
    """
    Gate N1/N2/N3 の記号的証明（スキャンではなく全パラメータに対する恒等式）。

    P1: Omega_p = 0 の定常状態は厳密に |g1><g1|（optical pumping の sink）。
        => 凍結EIT §9.6 の閉形式は近似ではなく厳密であり、population inversion は起きない。
    P2: Im chi の分子は gamma_31|gamma_g|^2 + beta*gamma_12 であり、
        gamma_12 > 0, beta > 0, Gamma_e > 0 で厳密に正。=> 吸収回復曲線は存在しない。
    P3: Re chi = 0  <=>  beta*delta = Delta_p (gamma_12^2 + delta^2)。
        gamma_12 -> 0 で beta = Delta_p*delta（ac-Stark シフトによる分散零点）。
    """
    out = []
    syms = dict(zip(
        ["Gamma_1", "Gamma_2", "gamma_12", "Omega_c", "Delta_p", "delta"],
        [G1, G2, GAM12, OMC, DP, DELTA],
    ))

    # --- P1
    Lsup = liouvillian(DP, DELTA, OMC, G1, G2, GAM12)
    rho0 = _solve_with_trace(Lsup, sp.zeros(9, 1), sp.Integer(1))
    target = sp.zeros(9, 1)
    target[vec_index(G1K, G1K)] = 1
    out.append(("P1 定常状態 rho^(0) = |g1><g1|（厳密・全パラメータ）",
                sp.simplify(sp.Matrix(rho0) - target) == sp.zeros(9, 1)))

    # --- chi の厳密閉形式（P1 より rho^(0) は上の target）
    chi, _ = susceptibility(syms, rho0=target)
    chi = sp.cancel(sp.together(chi))
    gamma31 = (G1 + G2) / 2 + GAM12 / 4
    gamma_g = GAM12 - sp.I * DELTA
    beta_v = OMC**2 / 4
    D = (gamma31 - sp.I * DP) * gamma_g + beta_v
    out.append(("    chi = (i/2) gamma_g / [(gamma_31 - i Delta_p) gamma_g + beta], "
                "gamma_31 = Gamma_e/2 + gamma_12/4",
                sp.simplify(chi - (sp.I / 2) * gamma_g / D) == 0))

    # chi_inf = lim_{beta->oo} chi(beta, gamma_12=0) = 0
    out.append(("    chi_inf = 0（beta -> oo, gamma_12 = 0）",
                sp.limit(chi.subs(GAM12, 0), OMC, sp.oo) == 0))

    # --- P2 / P3: chi = (i/2) gamma_g conj(D) / |D|^2
    numerator = sp.expand(sp.re(sp.expand(gamma_g * sp.conjugate(D)))
                          + sp.I * sp.im(sp.expand(gamma_g * sp.conjugate(D))))
    re_part = sp.simplify(sp.re(sp.expand(gamma_g * sp.conjugate(D))))
    im_part = sp.simplify(sp.im(sp.expand(gamma_g * sp.conjugate(D))))
    del numerator

    # Im chi ∝ Re(gamma_g conj D)
    expected_abs = gamma31 * (GAM12**2 + DELTA**2) + beta_v * GAM12
    out.append(("P2 Im chi の分子 = gamma_31(gamma_12^2 + delta^2) + beta*gamma_12",
                sp.simplify(re_part - expected_abs) == 0))
    # 厳密正値性: (Gamma_1, Gamma_2, gamma_12, Omega_c, delta) の多項式として
    # 全係数が正 => gamma_12 > 0 かつ Gamma_e > 0 なら値は厳密に正。
    coeffs = sp.Poly(sp.expand(expected_abs), G1, G2, GAM12, OMC, DELTA).coeffs()
    out.append((f"P2 その分子は全単項式係数が正 {coeffs} => gamma_12 > 0 で厳密に正"
                " => 吸収回復曲線は存在しない",
                all(c > 0 for c in coeffs)))

    # Re chi ∝ -Im(gamma_g conj D)
    expected_disp = DP * (GAM12**2 + DELTA**2) - beta_v * DELTA
    out.append(("P3 Re chi の分子 = -(Delta_p(gamma_12^2 + delta^2) - beta*delta)",
                sp.simplify(im_part - expected_disp) == 0))
    ridge = sp.solve(sp.Eq(expected_disp, 0), OMC**2 / 4)
    out.append((f"P3 分散稜線: beta = {sp.simplify(ridge[0]) if ridge else '解なし'}"
                f"  -> gamma_12 -> 0 で beta = Delta_p*delta（ac-Stark 零点）",
                bool(ridge)))
    return out, chi


def main():
    print("=" * 72)
    print("Gate N1: 三準位 Λ 系 GKSL の回復曲線 (exact arithmetic)")
    print("=" * 72)

    print("\n[Stage 0] 規約テスト")
    ok = True
    for name, passed in gate_s0():
        print(f"  {'PASS' if passed else 'FAIL'}  {name}")
        ok = ok and bool(passed)
    if not ok:
        print("\nGate S0 不合格。以降へ進まない。")
        return 1

    print("\n[Gate N1/N2/N3] 記号的証明（スキャンではなく恒等式）")
    proofs, _ = no_go_proof()
    for name, passed in proofs:
        print(f"  {'PASS' if passed else 'FAIL'}  {name}")
        ok = ok and bool(passed)
    if not ok:
        print("\n記号的証明が不合格。スキャン結果を信用しない。")
        return 1

    betas = [sp.Rational(1, 4), sp.Integer(1), sp.Integer(4), sp.Integer(25), sp.Integer(100)]

    print("\n[Stage 1-4] 基準点での chi と回復条件")
    base = rational_point()
    del base["Omega_c"], base["gamma_12"]
    cls, res, disp, absb = classify(base, betas)
    print(f"  chi_dark(gamma_12=0)      = {res['chi_dark']}")
    print(f"  chi_inf (beta -> oo)      = {res['chi_inf']}")
    print(f"  定常 population (g1,g2,e) = "
          f"{[sp.nsimplify(res['rho0'][vec_index(a, a)]) for a in range(3)]}")
    for b, d, a in zip(betas, disp, absb):
        print(f"  beta={b}:  F_disp 正根={d}   F_abs 正根={a}")
    print(f"  => class = {cls}")

    print("\n[Stage 6] パラメータスキャン（4軸、exact）")
    branchings = [(sp.Rational(1, 4), sp.Rational(3, 4)),
                  (sp.Rational(1, 2), sp.Rational(1, 2)),
                  (sp.Rational(9, 10), sp.Rational(1, 10))]
    detunings_p = [sp.Integer(0), sp.Rational(1, 5), sp.Integer(-1), sp.Integer(2)]
    detunings_2 = [sp.Integer(0), sp.Rational(1, 7), sp.Integer(-1)]
    tally = {}
    for (g1v, g2v), dp, d2 in itertools.product(branchings, detunings_p, detunings_2):
        pt = {"Gamma_1": g1v, "Gamma_2": g2v, "Delta_p": dp, "delta": d2}
        cls, _, _, _ = classify(pt, betas)
        tally[cls] = tally.get(cls, 0) + 1
        print(f"  G1={g1v} G2={g2v} Dp={dp} d2={d2}  ->  {cls}")
    print(f"\n  集計: {tally}")

    print("\n[判定]")
    if tally.get("D+A", 0) or tally.get("A only", 0):
        print("  吸収側の正の回復曲線が存在する点がある。GO 候補。")
    else:
        print("  吸収側の正の回復曲線はスキャン全点で存在しない。")
        print("  => 三準位 no-go（クラス D only / none）。Delta_split は定義されない。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
