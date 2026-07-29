"""CCRT（錐検閲応答理論・提案25）Stage-0 スモークテスト。

判定はすべて厳密有理数演算（判定経路に浮動小数点を使わない）。
seed 20260729（S2 のランダム埋め込みのみ使用。判定自体は決定的）。

検査する主張:

  [S1] 母集団保存（全ての状態で対角成分の時間微分が零）は jump 作用素の対角性を強制する。
       （3準位・1 jump の記号的 GKSL で恒等式として確認）
  [S2] 対角 jump ⇒ コヒーレンス減衰プロファイル
       γ_{jk} = (1/2)Σ_m |z_j^{(m)} − z_k^{(m)}|²
       は squared-Euclidean 核、すなわち条件付き負定値（cnd）。
       （有理埋め込み5例で cnd 判定 PASS を確認。逆向きは Schoenberg 埋め込み）
  [S3] 検閲: 「単一コヒーレンス (1,2) だけを殺し他ペアは殺さない」理想切断は
       n≥3 で cnd でない ⇒ jump 数・ancilla 次元によらず母集団保存 GKSL では実装不能。
       n=2 は実装可能（対照）。
  [S4] Z₆ 逆余弦族 h(τ)=A+2B cos(2πτ/6)、γ(τ)=1/h(τ)（循環プロファイル）:
       (A,B) 平面が許容領域（cnd 成立）と検閲領域（cnd 破れ）に分かれ、
       境界を有理区間で挟む。
  [S5] 対照（ablation）: 実装制約を落とした自由レート散逸子には検閲が存在しない
       （正値プロファイルは全て抽象線形散逸子として許される。構成により自明）。
  [S6] 背景救済と強度上限 κ*: 一様減衰床核 K_bg = (1−δ_{jk})（cnd 内部点）に
       単一辺切断 κ·E_{12} を加えた合成プロファイルは κ ≤ κ* でのみ cnd。
       n=3・一様床では κ* = 3 が厳密に成立（床の3倍まで）。

cnd 判定（厳密）: 対角零の対称核 K が cnd
  ⟺ Σ x_j x_k K_{jk} ≤ 0（Σx = 0 の全実ベクトル）
  ⟺ Gram_{ab} = K_{a,n} + K_{n,b} − K_{ab}（a,b = 1..n−1）が半正定値。
半正定値性は有理行列の全主小行列式 ≥ 0 で厳密判定する。
"""

from fractions import Fraction as F
from itertools import combinations
import random

import sympy as sp


# ---------- 厳密 PSD 判定 ----------
def all_principal_minors_nonneg(Mtx):
    """対称有理行列の厳密 PSD 判定: 全ての主小行列式 ≥ 0 ⟺ PSD。"""
    n = Mtx.rows
    for k in range(1, n + 1):
        for idx in combinations(range(n), k):
            if Mtx[list(idx), list(idx)].det() < 0:
                return False
    return True


def is_cnd(Kker):
    """Kker: 対角零・対称・有理の sympy Matrix。cnd ⟺ Gram が PSD。"""
    n = Kker.rows
    Gram = sp.zeros(n - 1, n - 1)
    for a in range(n - 1):
        for b in range(n - 1):
            Gram[a, b] = Kker[a, n - 1] + Kker[n - 1, b] - Kker[a, b]
    return all_principal_minors_nonneg(Gram)


# ---------- S1 ----------
def s1_population_preserving_forces_diagonal():
    """|m⟩⟨m| に対する散逸子の対角成分 (j≠m) が |L_jm|² に厳密一致することを確認。
    母集団保存はこれを全て零にするので L は対角に限る。"""
    n = 3
    L = sp.Matrix(n, n, lambda i, j: sp.Symbol(f"a{i}{j}", real=True)
                  + sp.I * sp.Symbol(f"b{i}{j}", real=True))
    for m in range(n):
        rho = sp.zeros(n, n)
        rho[m, m] = 1
        Dis = L * rho * L.H - sp.Rational(1, 2) * (L.H * L * rho + rho * L.H * L)
        for j in range(n):
            if j == m:
                continue
            if sp.simplify(Dis[j, j] - sp.Abs(L[j, m]) ** 2) != 0:
                return False
    return True


# ---------- S2 ----------
def s2_diagonal_gives_cnd():
    random.seed(20260729)
    for _ in range(5):
        n = 4
        zeta = [(F(random.randint(-9, 9), random.randint(1, 7)),
                 F(random.randint(-9, 9), random.randint(1, 7))) for _ in range(n)]
        Kker = sp.zeros(n, n)
        for j in range(n):
            for k in range(n):
                Kker[j, k] = sp.Rational((zeta[j][0] - zeta[k][0]) ** 2
                                         + (zeta[j][1] - zeta[k][1]) ** 2)
        if not is_cnd(Kker):
            return False
    return True


# ---------- S3 ----------
def s3_single_edge_censored():
    res = {}
    for n in (2, 3, 4, 5):
        Kker = sp.zeros(n, n)
        Kker[0, 1] = Kker[1, 0] = 1
        res[n] = is_cnd(Kker)
    return res  # 期待: {2: True, 3: False, 4: False, 5: False}


# ---------- S4 ----------
def z6_kernel(Acoef, Bcoef):
    cosv = [F(1), F(1, 2), F(-1, 2), F(-1), F(-1, 2), F(1, 2)]
    h = [Acoef + 2 * Bcoef * c for c in cosv]
    Kker = sp.zeros(6, 6)
    for j in range(6):
        for k in range(6):
            if j != k:
                Kker[j, k] = sp.Rational(F(1, 1) / h[(j - k) % 6])
    return Kker, h


def s4_z6_family():
    out = {}
    Kker, h = z6_kernel(F(1), F(1, 5))
    assert all(x > 0 for x in h)
    out["allowed(A=1,B=1/5)"] = is_cnd(Kker)          # 期待 True
    Kker, h = z6_kernel(F(1), F(49, 100))
    assert all(x > 0 for x in h)
    out["censored(A=1,B=49/100)"] = is_cnd(Kker)      # 期待 False
    lo, hi = F(1, 5), F(49, 100)
    for _ in range(8):
        mid = (lo + hi) / 2
        Kker, _ = z6_kernel(F(1), mid)
        if is_cnd(Kker):
            lo = mid
        else:
            hi = mid
    out["boundary_bracket_B*"] = (str(lo), str(hi))
    return out


# ---------- S6 ----------
def s6_strength_bound_exact():
    """n=3、K_bg = (1−δ)、切断 κ·E_{12}。合成核の cnd ⟺ κ ≤ 3 を厳密確認。"""
    kappa = sp.Symbol("kappa", nonnegative=True)
    # Gram（基点 j=3）: [[2, 1−κ], [1−κ, 2]] → PSD ⟺ (1−κ)² ≤ 4 ⟺ κ ≤ 3
    checks = []
    for kv, expect in [(F(2), True), (F(3), True), (F(31, 10), False), (F(100), False)]:
        Kker = sp.Matrix([[0, 1 + sp.Rational(kv), 1],
                          [1 + sp.Rational(kv), 0, 1],
                          [1, 1, 0]])
        checks.append(is_cnd(Kker) == expect)
    return all(checks)


if __name__ == "__main__":
    print("[S1] 母集団保存 ⇒ 対角 jump（恒等式検査）:",
          "PASS" if s1_population_preserving_forces_diagonal() else "FAIL")
    print("[S2] 対角 jump ⇒ cnd プロファイル（有理埋め込み5例）:",
          "PASS" if s2_diagonal_gives_cnd() else "FAIL")
    r3 = s3_single_edge_censored()
    ok3 = r3[2] and not r3[3] and not r3[4] and not r3[5]
    print(f"[S3] 単一辺切断の cnd: n=2:{r3[2]} n=3:{r3[3]} n=4:{r3[4]} n=5:{r3[5]}"
          f" ⇒ n≥3 検閲: {'PASS' if ok3 else 'FAIL'}")
    r4 = s4_z6_family()
    print("[S4] Z₆ 逆余弦族: 許容点:", r4["allowed(A=1,B=1/5)"],
          "/ 検閲点:", r4["censored(A=1,B=49/100)"],
          "/ 境界 B* ∈", r4["boundary_bracket_B*"])
    print("[S5] 対照: 自由レート散逸子（実装制約なし）に検閲なし（構成により自明）")
    print("[S6] 一様床 + 単一辺切断の強度上限 κ* = 3（厳密）:",
          "PASS" if s6_strength_bound_exact() else "FAIL")
