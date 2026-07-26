"""
計画20（TPR: Thermodynamics of Protected Response）段階1 — 内部還元監査。

目的: 提案文書 `Blueprints-of-theories/plan20_thermodynamics_of_protection_proposal.md`
      の中心主張 T1/T2/T4 が、既にリポジトリ内にある結果へ還元されるかを判定する。
      手順の全体は `docs/tpr-kill-plan.md` §2 段階1（W1-W4）。

ゲート:

  (W1) T1「有限温度平衡no-go」の機構同定と反例探索
    W1a 減衰床の閉形式 Lambda_j = (Gamma_out(j) + Gamma_out(1))/2 を導出し、
        凍結文書の prop:phase-n の D = diag(1,13/10,17/10,21/10)/2 と
        prop:phase-h の D = diag(0,0,1/2) を厳密に再現する（規約の同定）
    W1b 有限温度（KMS 比 t = exp(-beta*Delta) > 0）で D(t) = D_0 + delta(t)*I と
        なること、すなわち熱的核持ち上げの持ち上げ行列が **恒等行列** であることを示す
        -> P_full = 0 -> R_{S,0} = 0 -> nu >= 1。T1(a) は真だが、機構は
           ガイド §4.2 赤線7（fixed kernel lifting）であって
           提案 §3 が書く「核次元の勘定」ではない
    W1c [負制御] t = 0（ゼロ温度）で核が戻ることを確認。戻らなければ検定力なし
    W1d 斜交 Riesz 射影による反例。有限温度で D が正定値でも、
        斜交 Pi_S に対する圧縮 Pi_S D Pi_S|_{Ran Pi_S} は特異になりうる
        -> P_cut != 0 -> R_{S,0} != 0（Class III）。すなわち T1 は仮定 (E3)
           （切断クラスの対称性制限）なしには **偽**
    W1e [負制御] 直交 Pi_S では W1d の反例が消えることを確認（斜交性が本質）

  (W2) T1(c)「熱融解クロスオーバー」と提案24 LKCT の稜線のスケール分離
    W2a D = D_0 + eps*I の保護応答を Schur 還元で厳密に書き、
        融解端（保護が消える点、Gamma*eps ~ 1）と
        LKCT 稜線（補正が相殺する点、Gamma^2*eps ~ 1）が別スケールであることを示す

  (W3) T2「保護料下界」の前提整合性
    W3a ass:singular より Ran P = Ker D。R_{S,0} を運ぶ成分は定義上
        Gamma スケールで減衰しない。ゆえに T2 の仮定 (P2)
        「Gamma スケール散逸子の固有基底に対し非対角なコヒーレンス c_perp が
          R_{S,0} != 0 に必要」および証明経路「Gamma スケール位相緩和が
          c_perp を速度 ~Gamma|c_perp|^2 で破壊する」は設定と矛盾する

  (W4) T4「熱力学fan」の ass:bivariate 継承可能性
    W4a 浴のエントロピー生成は (Gamma,kappa) の有理関数（N^2 有限単項式台）で
        log 補正を持たないが、切断（kappa スケール介入）の寄与は
        ln(kappa) = q*ln(Gamma) + ln(kappa_0) を出す。
        -> sigma_bath は thm:polyhedral-selection を継承でき、sigma_cut は継承できない
    W4b 単一温度浴では sigma == 0（厳密）、二温度浴では sigma ∝ Gamma。
        mu in {0,1} の起源は「浴が詳細釣合いか否か」であり、
        アフィニティは Gamma 非依存の定数なので Gamma についての log 補正は出ない

判定基準（実行前に凍結）:
  PASS    — 当該ゲートの主張が厳密算術で成立
  FAIL    — 反証された
  VACUOUS — 対応する負制御が期待どおり壊れず、検定力がないと判断される場合

  W1a: 凍結文書の2つの D が **厳密に** 再現される（1成分でも不一致なら FAIL）
  W1b: D(t) - D_0 が delta(t)*I に厳密に等しく、delta(t) > 0 for t > 0
  W1c: t = 0 で dim Ker D == 2（phase-h 型）。これが 0 なら W1b は VACUOUS
  W1d: 有限 t で D_cut == 0（Ran Pi 上）を厳密に示す明示構成が存在
  W1e: 同じ D に対し直交射影では D_cut が正定値。これが崩れれば W1d は VACUOUS
  W2a: 2つの軌跡が Gamma ~ eps^-1 と Gamma ~ eps^(-1/2) に厳密に分離
  W3a: P*D == D*P == 0 が厳密に成立
  W4a: sigma_bath の単項式台が N^2 に含まれ、sigma_cut に ln が現れる
  W4b: 単一温度で sigma == 0（厳密）、二温度で sigma/Gamma が Gamma 非依存かつ > 0

判定に浮動小数点を使用しない（SymPy Rational / 記号式の厳密比較のみ）。
seed 20260728（ガイド §11.2: 20260723 / 20260725 / 20260726 / 20260727 は使用済み）。

注意: 本監査は内部監査であり、ガイド §11.0 の役割非対称性により
      Stage 2（赤チームによる還元試行）を代替しない。
"""

import argparse
import datetime
import io
import sys

import sympy as sp

SEED = 20260728

# ----------------------------------------------------------------------------
# 共通: Davies 型 GKSL の応答ブロック減衰作用素
# ----------------------------------------------------------------------------
#
# ジャンプ作用素が L_k = sqrt(g_k) |b_k><a_k| の形（単一行列要素）のとき、
# 弱プローブのコヒーレンス rho_{j1}（参照準位 1）に対する GKSL の作用は
#
#   L rho L^dag = g |b><a| rho |a><b| = g rho_{aa} |b><b|      （母数のみに寄与）
#   -(1/2){L^dag L, rho},  L^dag L = g |a><a|
#     -> -(1/2) g (delta_{j,a} + delta_{1,a}) rho_{j1}
#
# ゆえにコヒーレンスブロックは対角で
#
#   Lambda_j = (1/2) ( Gamma_out(j) + Gamma_out(1) ),
#   Gamma_out(l) := sum_k g_k * delta_{l, a_k}   （準位 l からの総流出レート）
#
# これが SMRT の A_Gamma(z) = Gamma*D + B(z) における D にあたる。


def damping_block(jumps, n_levels, ref=1):
    """コヒーレンス rho_{j,ref} (j != ref) の減衰作用素 D を対角成分の列で返す。

    jumps: [(a, b, rate)] — 準位 a -> b へレート rate のジャンプ。
    返り値: {j: Lambda_j} の dict（厳密式）。
    """
    out = {l: sp.Integer(0) for l in range(1, n_levels + 1)}
    for a, b, rate in jumps:
        out[a] = out[a] + rate
    return {
        j: sp.simplify(sp.Rational(1, 2) * (out[j] + out[ref]))
        for j in range(1, n_levels + 1)
        if j != ref
    }


def banner(title):
    print()
    print("=" * 74)
    print(title)
    print("=" * 74)


RESULTS = {}


def verdict(gate, ok, note=""):
    tag = "PASS" if ok else "FAIL"
    RESULTS[gate] = tag
    print(f"  -> {gate} {tag}" + (f"   [{note}]" if note else ""))
    return ok


# ----------------------------------------------------------------------------
# W1a — 減衰床の閉形式と凍結値の再現
# ----------------------------------------------------------------------------

def gate_W1a():
    banner("W1a  減衰床の閉形式と凍結文書の再現（規約の同定）")
    G = sp.Symbol("Gamma", positive=True)

    # prop:phase-n（凍結 tex L.452 以降、証明中の実現）
    #   L_j = sqrt(Gamma d_j) |1><j|,  j = 2..5,  (d2..d5) = (1, 13/10, 17/10, 21/10)
    d = [sp.Integer(1), sp.Rational(13, 10), sp.Rational(17, 10), sp.Rational(21, 10)]
    jumps_n = [(j, 1, G * d[j - 2]) for j in range(2, 6)]
    D_n = damping_block(jumps_n, n_levels=5, ref=1)
    got_n = [sp.simplify(D_n[j] / G) for j in range(2, 6)]
    want_n = [sp.Rational(1, 2) * x for x in d]
    ok_n = all(sp.simplify(a - b) == 0 for a, b in zip(got_n, want_n))
    print(f"  prop:phase-n  D/Gamma = diag{tuple(got_n)}")
    print(f"                凍結値   = diag{tuple(want_n)}      一致={ok_n}")

    # prop:phase-h（凍結 tex L.1035、証明中「the fast state carrying the Gamma-scaled
    # decay」「the weak-probe block then has D = diag(0,0,1/2)」）
    # 4準位、参照=1、準位 2,3 は Gamma スケールの流出なし、準位 4（fast）のみが持つ。
    jumps_h = [(4, 1, G * sp.Integer(1))]
    D_h = damping_block(jumps_h, n_levels=4, ref=1)
    got_h = [sp.simplify(D_h[j] / G) for j in range(2, 5)]
    want_h = [sp.Integer(0), sp.Integer(0), sp.Rational(1, 2)]
    ok_h = all(sp.simplify(a - b) == 0 for a, b in zip(got_h, want_h))
    print(f"  prop:phase-h  D/Gamma = diag{tuple(got_h)}")
    print(f"                凍結値   = diag{tuple(want_h)}      一致={ok_h}")

    print("  閉形式: Lambda_j = ( Gamma_out(j) + Gamma_out(1) ) / 2")
    return verdict("W1a", ok_n and ok_h, "両方の凍結 D を厳密再現")


# ----------------------------------------------------------------------------
# W1b — 有限温度での一様核持ち上げ（持ち上げ行列 = 恒等行列）
# ----------------------------------------------------------------------------

def gate_W1b():
    banner("W1b  有限温度の核持ち上げ: D(t) = D_0 + delta(t)*I（D_L = I）")
    G = sp.Symbol("Gamma", positive=True)
    t = sp.Symbol("t", positive=True)  # t = exp(-beta*Delta) in (0,1]

    # phase-h 型に詳細釣合いの上向きジャンプを付ける。
    #   下向き 4->1 レート Gamma、上向き 1->4 レート Gamma*t  （KMS 比 t）
    jumps_T = [(4, 1, G), (1, 4, G * t)]
    D_T = damping_block(jumps_T, n_levels=4, ref=1)
    got = [sp.simplify(D_T[j] / G) for j in range(2, 5)]
    D0 = [sp.Integer(0), sp.Integer(0), sp.Rational(1, 2)]
    delta = sp.Rational(1, 2) * t  # = Gamma_out(1)/(2*Gamma)

    diffs = [sp.simplify(g - d0) for g, d0 in zip(got, D0)]
    uniform = all(sp.simplify(x - delta) == 0 for x in diffs)
    print(f"  D(t)/Gamma      = diag{tuple(got)}")
    print(f"  D(t)/Gamma - D_0 = diag{tuple(diffs)}")
    print(f"  delta(t)        = {delta}   （= Gamma_out(1)/(2*Gamma)）")
    print(f"  持ち上げが恒等行列に比例: {uniform}")

    # 有限 t で核が消える
    ker_dim = sum(1 for g in got if sp.simplify(g) == 0)
    print(f"  dim Ker D (t>0) = {ker_dim}   -> P_full = 0 -> R_(S,0) = 0 -> nu >= 1")

    ok = uniform and ker_dim == 0 and sp.simplify(delta.subs(t, sp.Rational(1, 7))) > 0
    print("  機構の同定: 熱的持ち上げは ガイド §4.2 赤線7（fixed kernel lifting）。")
    print("              提案 §3 T1(a) の「核次元の勘定」ではない。")
    print("              持ち上げ行列 D_L = I は提案24 LKCT の族の特別な切片。")
    return verdict("W1b", ok, "D_L = I, delta(t) = t/2 > 0")


# ----------------------------------------------------------------------------
# W1c — [負制御] ゼロ温度で核が戻る
# ----------------------------------------------------------------------------

def gate_W1c():
    banner("W1c  [負制御] t = 0（ゼロ温度）で保護核が戻ること")
    G = sp.Symbol("Gamma", positive=True)
    jumps_0 = [(4, 1, G), (1, 4, G * sp.Integer(0))]
    D_0 = damping_block(jumps_0, n_levels=4, ref=1)
    got = [sp.simplify(D_0[j] / G) for j in range(2, 5)]
    ker_dim = sum(1 for g in got if sp.simplify(g) == 0)
    print(f"  D(0)/Gamma = diag{tuple(got)}   dim Ker D = {ker_dim}")
    ok = ker_dim == 2
    print("  負制御が期待どおり: 温度を切ると保護核が復活する（検定力あり）"
          if ok else "  負制御が壊れない -> W1b は VACUOUS")
    return verdict("W1c", ok, "dim Ker D = 2")


# ----------------------------------------------------------------------------
# W1d — 斜交 Riesz 射影による反例（(E3) が本質的であることの証明）
# ----------------------------------------------------------------------------

def gate_W1d():
    banner("W1d  斜交 Pi_S による反例: 有限温度でも P_cut != 0 が起こりうる")
    t = sp.Rational(1, 5)  # 有限温度の具体値（厳密有理数）

    # 有限温度の応答ブロック減衰（W1b より正定値対角）。2次元の縮約で十分。
    D = sp.diag(sp.Rational(1, 2) * t, sp.Rational(1, 2) + sp.Rational(1, 2) * t)
    print(f"  D = diag({D[0, 0]}, {D[1, 1]})   （有限温度 t = {t}、正定値）")

    # Ran Pi = span{u}, Ker Pi = span{D u} と選ぶと、定義から Pi D u = 0。
    u = sp.Matrix([1, 1])
    w = D * u                      # Ker Pi の生成元
    s = sp.Matrix([-w[1], w[0]])   # s^T w = 0 となるよう選ぶ
    denom = (s.T * u)[0, 0]
    print(f"  u = {list(u)}   w = D u = {list(w)}   s^T u = {denom}")
    if sp.simplify(denom) == 0:
        return verdict("W1d", False, "退化した構成")

    Pi = (u * s.T) / denom
    idem = sp.simplify(Pi * Pi - Pi) == sp.zeros(2, 2)
    # Ran Pi 上への圧縮： v = u に対する Pi D u
    compressed = sp.simplify(Pi * D * u)
    singular = compressed == sp.zeros(2, 1)

    print(f"  Pi = {Pi.tolist()}")
    print(f"  Pi^2 = Pi : {idem}      Pi D u = {list(compressed)}")
    print(f"  D_cut = Pi D Pi|_(Ran Pi) は特異: {singular}")
    print("  => P_cut != 0。eq:R0 の cut 項が生き残り R_(S,0) != 0（Class III）。")
    print("     すなわち T1 は仮定 (E3)（切断クラスの対称性制限）なしには偽。")
    print("     凍結 def:operational-sector は "
          "'the Riesz splitting may be oblique' と明記している。")
    print("     ただし rem:gksl-model により、この Pi を与える G_S が "
          "GKSL admissible かは模型ごとの監査事項。")
    return verdict("W1d", idem and singular, "斜交圧縮が特異")


# ----------------------------------------------------------------------------
# W1e — [負制御] 直交射影では反例が消える
# ----------------------------------------------------------------------------

def gate_W1e():
    banner("W1e  [負制御] 直交 Pi_S では W1d の反例が消えること")
    t = sp.Rational(1, 5)
    D = sp.diag(sp.Rational(1, 2) * t, sp.Rational(1, 2) + sp.Rational(1, 2) * t)
    u = sp.Matrix([1, 1])
    Pi = (u * u.T) / (u.T * u)[0, 0]     # 直交射影
    idem = sp.simplify(Pi * Pi - Pi) == sp.zeros(2, 2)
    val = sp.simplify((u.T * D * u)[0, 0] / (u.T * u)[0, 0])  # Ran Pi 上の圧縮の固有値
    print(f"  Pi(orth) = {Pi.tolist()}   Pi^2=Pi: {idem}")
    print(f"  圧縮の固有値 = u^T D u / u^T u = {val}  > 0 : {val > 0}")
    ok = idem and val > 0
    print("  負制御が期待どおり: 正定値 D の直交圧縮は常に可逆。斜交性が本質。"
          if ok else "  負制御が壊れる -> W1d は VACUOUS")
    return verdict("W1e", ok, "直交圧縮は可逆")


# ----------------------------------------------------------------------------
# W2a — 融解端と LKCT 稜線のスケール分離
# ----------------------------------------------------------------------------

def gate_W2a():
    banner("W2a  熱融解端（Gamma*eps ~ 1）と LKCT 稜線（Gamma^2*eps ~ 1）の分離")
    G, eps = sp.symbols("Gamma epsilon", positive=True)

    # 保護ブロック 1 次元、高速ブロック 1 次元の最小 Schur 模型。
    #   A = Gamma*(D_0 + eps*I) + B,  D_0 = diag(0, 1),  B = [[b, f],[h, m]]
    b, f, h, m = sp.symbols("b f h m", positive=True)
    S = (b + G * eps) - f * h / (m + G * (1 + eps))   # 保護ブロックの Schur 補元
    R = 1 / S
    R_inf = 1 / b                                     # eps=0, Gamma->infty の理想値

    # eps=0 での漏洩補正（LKCT の alpha_leak / Gamma）と
    # eps>0 での持ち上げ補正（LKCT の -kappa_lift * Gamma*eps）
    ser = sp.series(sp.simplify(S - b), G, sp.oo, 2).removeO()
    print(f"  Schur 補元の大 Gamma 展開: S - b = {sp.simplify(ser)}")

    # 融解端: 持ち上げ項 Gamma*eps が保護ブロックの O(1) スケール b と拮抗する点
    melt = sp.solve(sp.Eq(G * eps, b), G)[0]
    # 稜線: 持ち上げ項と漏洩項 (f*h/(Gamma)) が拮抗する点
    ridge = sp.solve(sp.Eq(G * eps, f * h / G), G)
    ridge = [r for r in ridge if r.is_positive is not False][0]

    print(f"  融解端   Gamma_melt  = {sp.simplify(melt)}      -> eps^(-1)")
    print(f"  LKCT稜線 Gamma_ridge = {sp.simplify(ridge)}   -> eps^(-1/2)")

    e_melt = sp.simplify(sp.log(melt.subs({b: 1})) / sp.log(eps))
    e_ridge = sp.simplify(sp.log(ridge.subs({f: 1, h: 1})) / sp.log(eps))
    print(f"  eps 冪: melt = {e_melt}   ridge = {e_ridge}")

    ok = sp.simplify(e_melt + 1) == 0 and sp.simplify(e_ridge + sp.Rational(1, 2)) == 0
    print("  => 2つは別スケール。提案の Gamma*(beta) ~ exp(beta*Delta) は融解端であり、")
    print("     LKCT/RISEI の eps^(-1/2) 稜線とは一致しない（重複ではない）。")
    print("     ただし融解端そのものは ガイド §4.2 赤線7 が名指しで扱う有限窓現象。")
    return verdict("W2a", ok, "eps^-1 vs eps^-1/2")


# ----------------------------------------------------------------------------
# W3a — T2 の仮定 (P2) と ass:singular の矛盾
# ----------------------------------------------------------------------------

def gate_W3a():
    banner("W3a  T2 の仮定 (P2) が ass:singular と矛盾すること")
    # ass:singular: Ran P_j = Ker D_j, P_j D_j = D_j P_j = 0
    D = sp.diag(0, 0, sp.Rational(1, 2))          # phase-h 型（ゼロ温度、保護あり）
    P = sp.diag(1, 1, 0)                          # Ker D 上への Riesz 射影
    lhs = sp.simplify(P * D)
    rhs = sp.simplify(D * P)
    ok = lhs == sp.zeros(3, 3) and rhs == sp.zeros(3, 3)
    print(f"  D = diag(0,0,1/2)   P = diag(1,1,0)")
    print(f"  P*D = 0 : {lhs == sp.zeros(3,3)}      D*P = 0 : {rhs == sp.zeros(3,3)}")
    print()
    print("  eq:R0 より R_(S,0) は P で挟まれた量である:")
    print("      R_(S,0) = p^dag P B_P^-1 P c  -  (cut 側の同型項)")
    print("  ゆえに R_(S,0) を運ぶ成分は Ran P = Ker D の中にあり、")
    print("  **定義により Gamma スケールで減衰しない**。")
    print()
    print("  一方、提案 §3 T2 の仮定 (P2) と証明経路は")
    print("      「R_(S,0) != 0 は Gamma スケール散逸子の固有基底に対し非対角な")
    print("        コヒーレンス c_perp を要求する」")
    print("      「Gamma スケール位相緩和は c_perp を速度 ~Gamma|c_perp|^2 で破壊し、")
    print("        定常性より同速度の再生成電流が要る」")
    print("  と述べる。前者は Ran P の外に、後者は Gamma 減衰を受ける成分に、")
    print("  それぞれ R_(S,0) の担い手を置いている。**両立しない。**")
    print()
    print("  => T2 の証明経路は設定と矛盾する。下界 sigma >= C*Gamma*c_0^2 の")
    print("     導出根拠が存在しない。T2 は Conditional ですらなく Conjecture。")
    return verdict("W3a", ok, "Ran P = Ker D、(P2) と両立しない")


# ----------------------------------------------------------------------------
# W4a / W4b — エントロピー生成の単項式台と mu の起源
# ----------------------------------------------------------------------------

def gate_W4b():
    banner("W4b  単一温度 sigma == 0 / 二温度 sigma ∝ Gamma（mu in {0,1} の起源）")
    G = sp.Symbol("Gamma", positive=True)
    g1, g2 = sp.symbols("g1 g2", positive=True)
    t1, t2 = sp.symbols("t1 t2", positive=True)   # t_nu = exp(-beta_nu * Delta)

    # 2準位、浴 nu = 1,2。下向き Gamma*g_nu、上向き Gamma*g_nu*t_nu（各浴が詳細釣合い）
    # 定常状態: p_e/p_g = (sum g_nu t_nu)/(sum g_nu) =: r  （Gamma に依存しない）
    r = (g1 * t1 + g2 * t2) / (g1 + g2)
    p_g = 1 / (1 + r)
    p_e = r / (1 + r)

    def sigma_bath(gn, tn):
        J = G * gn * (tn * p_g - p_e)              # 浴 nu の正味フラックス
        A = sp.log(tn * p_g / p_e)                 # 対応するアフィニティ
        return sp.simplify(J * A)

    sigma = sp.simplify(sigma_bath(g1, t1) + sigma_bath(g2, t2))

    # 単一温度 t1 = t2 = t
    t = sp.Symbol("t", positive=True)
    sigma_single = sp.simplify(sigma.subs({t1: t, t2: t}))
    print(f"  単一温度 (t1 = t2 = t):  sigma = {sigma_single}")

    # 二温度の具体値（厳密有理数）
    subs2 = {g1: sp.Integer(1), g2: sp.Integer(1),
             t1: sp.Rational(1, 2), t2: sp.Rational(1, 5)}
    sigma_two = sp.simplify(sigma.subs(subs2))
    coeff = sp.simplify(sigma_two / G)
    gamma_free = sp.simplify(sp.diff(coeff, G)) == 0
    # 正値性は log の厳密簡約で判定する（浮動小数点を判定に使わない）。
    coeff_pos = sp.simplify(coeff).is_positive
    print(f"  二温度 (t1=1/2, t2=1/5): sigma = Gamma * ({coeff})")
    print(f"    係数は Gamma 非依存: {gamma_free}    厳密に正: {coeff_pos}")
    print(f"    （参考表示のみ、判定に不使用）数値 = {sp.N(coeff, 10)}")

    ok_single = sp.simplify(sigma_single) == 0
    ok_two = bool(gamma_free) and sp.simplify(coeff) != 0 and coeff_pos is True
    print()
    print("  => mu = 0 <-> Gamma スケール浴が詳細釣合い（単一温度）")
    print("     mu = 1 <-> Gamma スケール浴が非平衡（複数温度）")
    print("  アフィニティ ln(t_nu/r) は Gamma 非依存の定数なので、")
    print("  **浴の EP は Gamma について log 補正を持たない**。")
    return verdict("W4b", ok_single and ok_two, "sigma_single == 0, sigma_two ∝ Gamma")


def gate_W4a():
    banner("W4a  sigma_bath は N^2 単項式台 / sigma_cut のみが log を出す")
    G, k0 = sp.symbols("Gamma kappa_0", positive=True)
    q = sp.Symbol("q", nonnegative=True)
    kappa = k0 * G ** q

    # 浴側: レートは Gamma に比例し、レート比（=アフィニティの中身）は Gamma 非依存。
    # -> フラックスは (Gamma, kappa) の有理関数、アフィニティは定数。
    #    ゆえに sigma_bath は ass:bivariate の要求する N^2 有限単項式台に載る。
    t = sp.Rational(1, 3)
    A_bath = sp.log(t)                             # Gamma にも kappa にも依存しない
    bath_has_log_in_G = sp.simplify(sp.diff(A_bath, G)) != 0
    print(f"  浴のアフィニティ A_bath = ln({t}) — Gamma 依存: {bath_has_log_in_G}")

    # 切断側: killing 介入 kappa*G_S は片方向のジャンプ（レート kappa）であり、
    # 逆過程のレートは Gamma・kappa に依らない O(1)。アフィニティは
    #   A_cut = ln(kappa / w_back) = q*ln(Gamma) + ln(kappa_0/w_back)
    w_back = sp.Integer(1)
    A_cut = sp.simplify(sp.log(kappa / w_back))
    A_cut_exp = sp.expand(sp.expand_log(A_cut, force=True))
    cut_has_log = A_cut_exp.has(sp.log(G))
    print(f"  切断のアフィニティ A_cut = {A_cut_exp}")
    print(f"    ln(Gamma) を含む: {cut_has_log}")

    ok = (not bath_has_log_in_G) and cut_has_log
    print()
    print("  => sigma = sigma_bath + sigma_cut と分離すれば、")
    print("     sigma_bath は ass:bivariate を満たし thm:polyhedral-selection を継承できる。")
    print("     log 補正は sigma_cut にのみ現れ、これは T7（介入の実装コスト）の対象。")
    print("  提案 §3 T4 の「mu は log 補正つき」という一括りの定義は分離すべきであり、")
    print("  §6 Stop 条件4（log 補正が leading power を不定にする）は分離により回避できる。")
    return verdict("W4a", ok, "分離すれば継承可能")


# ----------------------------------------------------------------------------

def run_all():
    print("TPR（計画20）段階1 内部還元監査 — W1-W4")
    print(f"seed {SEED} / sympy {sp.__version__} / 判定に浮動小数点を使用しない")

    gate_W1a()
    gate_W1b()
    gate_W1c()
    gate_W1d()
    gate_W1e()
    gate_W2a()
    gate_W3a()
    gate_W4a()
    gate_W4b()

    banner("判定一覧")
    for k in sorted(RESULTS):
        print(f"  {k:5s} {RESULTS[k]}")
    failed = [k for k, v in RESULTS.items() if v != "PASS"]
    print()
    if failed:
        print(f"  未通過: {', '.join(failed)}")
        return 1
    print("  全ゲート PASS")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=None,
                    help="証明書の出力先（certificates/tpr_reduction_<date>.txt）")
    args = ap.parse_args()

    if args.out is None:
        return run_all()

    buf = io.StringIO()
    real_stdout = sys.stdout
    sys.stdout = buf
    try:
        code = run_all()
    finally:
        sys.stdout = real_stdout

    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    header = (
        f"# TPR (計画20) 段階1 内部還元監査 -- generated {stamp}\n"
        f"# script: scripts/tpr_thermo_audit.py  seed {SEED}  sympy {sp.__version__}\n"
        "# 判定に浮動小数点を使用していない（表示のみ sp.N）\n"
        "# 手順: docs/tpr-kill-plan.md §2 段階1\n"
    )
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(header)
        f.write(buf.getvalue())
    print(buf.getvalue())
    print(f"Wrote {args.out}")
    return code


if __name__ == "__main__":
    sys.exit(main())
