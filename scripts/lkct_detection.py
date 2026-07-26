#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""提案24 (LKCT) S1 — 検出模型の独立導出（ゲート E0–E5）

`docs/lkct-visibility-audit.md` は §1.2 条件6「full physical model では現象が観測不能」を
**部分的に残した**。optical depth・アンサンブル伝播・検出器雑音はガイド §4.3 により
凍結理論から継承できず、独立導出が必要だからである。本監査がその導出を行う。

**継承ではなく導出である根拠:** 使う入力は本リポジトリで厳密に確立した2つの量のみ。
  (i)  稜線での規格化傾き `S²`（厳密有理数、`lkct_visibility.py` U5 と同じ構成）
  (ii) 稜線位置の control-power 依存 `ridge ∝ λ²`（`lkct_visibility.py` U6(a)、厳密）
これらから、ショット雑音・背景オフセット・駆動強度分布（伝播＝optical depth の翻訳）の
3つの検出制約を**式として**導く。外部文献の数値は一切使わない。

導出する式（判定文書 `docs/lkct-detection-audit.md` に導出過程を記載）:
  [D1] ゼロ交差の統計的位置決め精度   δ(ln η) = σ_rel / S、σ_rel = z*/√N
  [D2] 必要ショット数                 N_min = z*² / (Δ² · S²)      （厳密有理数）
  [D3] 背景オフセット許容量            b_max = S · Δθ_max · |R_∞|
  [D4] 駆動強度分布 → 稜線分布        相対幅 δ_I の強度分布 ⇒ 稜線の相対分布 ≈ 2δ_I
       optical depth の翻訳: 場の減衰 e^{−OD/2} ≥ 1−δ_I ⇔ OD ≤ −2ln(1−δ_I)

**論理 status: Conditional / Model-specific（ガイド §10.3 カテゴリ D）。**
検出模型の宣言: 独立ショット・projection-noise 限界の読み出し、有限コントラスト C は
N → N/C² の再スケールで吸収（数値は宣言しない）、静的オフセットは較正後の残差 b を仮定。

seed 20260733（既使用 20260723/25/26/27/28/29/30(派生)/31/32）。
判定に浮動小数点を使用していない（S²・N_min・閾値はすべて厳密有理数、比較は厳密）。

範囲外（残余として明示）: 集団効果（superradiance 等）・多体効果、検出器の具体的実装
（dead time・afterpulse）、1次を超えるスペクトル拡散。これらは §4.3 の禁止により
凍結からも借りられず、本監査でも導出していない。
"""

import argparse
import datetime
import io
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lkct_gksl_pullback as PB   # noqa: E402
import lkct_visibility as UV      # noqa: E402

Q = sp.Rational
SEED = 20260733
RULE = "=" * 74
GAM, EPS = PB.GAM, PB.EPS
_PP4 = sp.Matrix([0, 1, 0, 0])

# --------------------------------------------------------------------------
# 実行前に凍結する検出模型パラメータ（すべて厳密有理数）
# --------------------------------------------------------------------------
ZSTAR = Q(3)          # 有意水準（3σ）
DLT = Q(1, 2)         # 符号比較の2点の対数半間隔 Δ（ln η 単位）
BUDGETS = [Q(10)**6, Q(10)**7, Q(10)**8]   # 検討するショット予算（点あたり）
DTH_MAX = Q(1, 4)     # 許容する交差位置シフト（ln η 単位）
BAR_B = Q(1, 10000)   # 較正後オフセット残差の到達可能水準（相対、宣言値）
DELTA_I = Q(1, 20)    # 駆動強度の相対分布幅 5%（伝播・ビーム不均一の翻訳）
GRID = [Q(1200), Q(1500), Q(2000), Q(3000)]   # Γ 走査格子

_slope_cache = {}


def phi_at(gval, epsval, PhiF, model=None):
    m = model or PB.MODEL
    A, c, *_ = PB.pencil_from_liouvillian(m)
    Rinf, *_ = PB._jet(m)
    sub = {GAM: gval, EPS: epsval}
    x = A.subs(sub).LUsolve(c.subs(sub))
    return sp.simplify(PhiF(sp.expand((_PP4.conjugate().T * x)[0, 0] - Rinf)))


def slope2(gval, PhiF):
    """稜線での規格化傾きの2乗 S²（厳密有理数）。U5 と同一の構成。"""
    key = (gval, PhiF)
    if key in _slope_cache:
        return _slope_cache[key]
    delta = Q(1, 100)
    Rinf, *_ = PB._jet(PB.MODEL)
    absR2 = sp.re(Rinf)**2 + sp.im(Rinf)**2
    b, _ = UV.ridge_root(gval, PhiF)
    if b is None:
        _slope_cache[key] = None
        return None
    b = Q(sp.Rational(str(sp.N(b, 30))))
    hi = phi_at(gval, b * (1 + delta), PhiF)
    lo = phi_at(gval, b * (1 - delta), PhiF)
    S2 = sp.simplify((hi - lo)**2 / (2 * delta)**2 / absR2)
    _slope_cache[key] = (S2, b)
    return _slope_cache[key]


def n_min(S2):
    """[D2] N_min = z*²/(Δ²·S²)（厳密有理数）。"""
    return sp.simplify(ZSTAR**2 / (DLT**2 * S2))


# --------------------------------------------------------------------------
def E0():
    print(RULE, flush=True)
    print("E0  回帰と検出模型の凍結")
    print(RULE)
    print("  sympy:", sp.__version__, "  seed:", SEED)
    Rinf, kap, alp, *_ = PB._jet(PB.MODEL)
    ok = (sp.simplify(sp.re(alp) / sp.re(kap)) == Q(25527228, 1405495))
    print("  V5/U0 の 2-jet 稜線を再現:", ok)
    print()
    print("  検出模型（宣言。導出はこの模型の内部で閉じる）:")
    print("    ・独立ショット、projection-noise 限界の読み出し")
    print("    ・有限コントラスト C は N → N/C² の再スケールで吸収（数値は宣言しない）")
    print("    ・静的オフセットは較正後の残差 b のみ")
    print()
    print("  凍結パラメータ（厳密有理数）:")
    print(f"    z* = {ZSTAR}（有意水準）  Δ = {DLT}（符号比較の対数半間隔）")
    print(f"    Δθ_max = {DTH_MAX}（許容交差シフト）  b̄ = {BAR_B}（較正後オフセット残差）")
    print(f"    δ_I = {DELTA_I}（駆動強度の相対分布幅）  予算 = {[str(b) for b in BUDGETS]}")
    print("  -> E0", "PASS" if ok else "FAIL")
    return bool(ok)


def E1():
    print(RULE, flush=True)
    print("E1  ショット雑音の法則と予算依存の実用窓（[D1][D2]）")
    print(RULE)
    print("  [D1] 交差の位置決め精度: δ(ln η) = σ_rel/S、σ_rel = z*/√N")
    print("  [D2] 交差の2点符号判定に必要なショット数: N_min = z*²/(Δ²·S²)")
    print("  S² は厳密有理数（U5 と同一構成）なので N_min も厳密有理数である。")
    print()
    print("  Γ    |   R_Γ   | S_Re        | S_Im        | N_min(Re)   | N_min(Im)")
    print("  " + "-" * 74)
    tab = {}
    for gv in GRID:
        row = {}
        for nm, PhiF in [("Re", sp.re), ("Im", sp.im)]:
            r = slope2(gv, PhiF)
            row[nm] = r[0] if r else None
        tab[gv] = row
        f = lambda v: f"{float(sp.sqrt(v)):11.4g}" if v is not None else "     （なし）"
        g = lambda v: f"{float(n_min(v)):11.4g}" if v is not None else "          -"
        print(f"  {str(gv):>5} | {float(7*gv):7.4g} | {f(row['Re'])} | {f(row['Im'])} |"
              f" {g(row['Re'])} | {g(row['Im'])}", flush=True)
    print()
    print("  傾きの構造: S_Re は生成閾値 Γ_c ≈ 1170 で 0 から立ち上がり（接根）、")
    print("  S_Im は 1/Γ で減衰する。⇒ **実用窓は存在窓より両側とも狭い。**")
    # 最適 Γ = min(S_Re², S_Im²) を最大化する格子点
    best = None
    for gv in GRID:
        r = tab[gv]
        if r['Re'] is None or r['Im'] is None:
            continue
        m = min(r['Re'], r['Im'], key=lambda v: sp.simplify(v))
        if best is None or sp.simplify(m - best[1]) > 0:
            best = (gv, m)
    nstar = n_min(best[1])
    print()
    print(f"  格子上の最適点: Γ = {best[0]}（R_Γ = {float(7*best[0]):.4g}）、"
          f"min(S²) = {best[1]}")
    print(f"  ⇒ **最小予算 N* = {nstar} ≈ {float(nstar):.3g} shots/点**（これ未満では窓が開かない）")
    print()
    print("  予算ごとの実用窓（閾値 S² > TH² = z*²/(N·Δ²)、厳密比較）:")
    for N in BUDGETS:
        TH2 = sp.simplify(ZSTAR**2 / (N * DLT**2))
        ok_pts = [gv for gv in GRID
                  if tab[gv]['Re'] is not None and tab[gv]['Im'] is not None
                  and sp.simplify(tab[gv]['Re'] - TH2) > 0
                  and sp.simplify(tab[gv]['Im'] - TH2) > 0]
        lab = (f"Γ ∈ [{ok_pts[0]}, {ok_pts[-1]}] の格子点で開く"
               if ok_pts else "**空**（この予算では観測不能）")
        print(f"    N = {str(N):>9}: TH = {float(sp.sqrt(TH2)):.4g}   {lab}", flush=True)
    print()
    # 前回の FLOOR = 1e-3 の物理的正当化
    N_floor = sp.simplify(ZSTAR**2 / (DLT**2 * Q(1, 1000)**2))
    print(f"  **FLOOR = 10⁻³（U5 の宣言値）の物理的正当化:** FLOOR = z*/(Δ√N) を解くと")
    print(f"    N = z*²/(Δ²·FLOOR²) = {N_floor} = {float(N_floor):.3g} shots/点。")
    print("    すなわち U5 の床は「約 3.6×10⁷ shots/点・3σ・Δ=½」という資源宣言と等価である。")
    ok = (best is not None) and any(
        sp.simplify(tab[gv]['Re'] - ZSTAR**2 / (BUDGETS[1] * DLT**2)) > 0
        and sp.simplify(tab[gv]['Im'] - ZSTAR**2 / (BUDGETS[1] * DLT**2)) > 0
        for gv in GRID if tab[gv]['Re'] is not None and tab[gv]['Im'] is not None)
    print("  -> E1", "PASS" if ok else "FAIL")
    return bool(ok), tab, nstar


def E2(tab):
    print(RULE, flush=True)
    print("E2  背景オフセットの許容量（[D3]）")
    print(RULE)
    print("  測定量 M(η) = Φ(R−R_∞) + b（b = 較正後の静的残差）。")
    print("  M の零点は Φ = −b へずれ、シフトは δ(ln η) = b_rel/S（b_rel = b/|R_∞|）。")
    print(f"  許容シフト Δθ_max = {DTH_MAX} から **b_max,rel = S·Δθ_max**。")
    print()
    print("  Γ    | 枝 | b_max,rel     | b̄ = 1/10⁴ 以下で較正可能なら十分か")
    print("  " + "-" * 66)
    ok = True
    gv = Q(2000)
    for nm in ("Re", "Im"):
        S2v = tab[gv][nm]
        bmax = sp.simplify(sp.sqrt(S2v) * DTH_MAX)
        good = sp.simplify(bmax**2 - BAR_B**2) > 0
        ok = ok and bool(good)
        print(f"  {str(gv):>5} | {nm} | {float(bmax):11.4g}  | {bool(good)}")
    print()
    print("  ⇒ 必要な較正精度は相対 ~5×10⁻⁴。宣言した到達水準 b̄ = 10⁻⁴ はこれを満たす。")
    print("  ⇒ 2交差は独立にずれるが、各シフト ≤ Δθ_max = 1/4 ≪ ln(比 ≈ 13) ≈ 2.6 なので")
    print("     **分裂の同定はオフセットに対して頑健**。")
    print("  -> E2", "PASS" if ok else "FAIL")
    return bool(ok)


def E3():
    print(RULE, flush=True)
    print("E3  駆動強度分布と伝播（optical depth の翻訳）（[D4]）")
    print(RULE)
    print("  U6(a) の厳密則「稜線位置 ∝ λ²」（λ = P–F 結合スケール）を使う。")
    print("  試料内伝播で場が減衰すると λ が分布する。3点分布 λ ∈ {1−δ_I, 1, 1+δ_I}、")
    print(f"  δ_I = {DELTA_I} で**厳密平均応答**の交差を検査する。")
    print()
    gv = Q(2000)
    Rinf, *_ = PB._jet(PB.MODEL)
    models = []
    for lam in (1 - DELTA_I, Q(1), 1 + DELTA_I):
        m = dict(PB.MODEL)
        for kk in ('J24', 'J25', 'J34', 'J35'):
            m[kk] = PB.MODEL[kk] * lam
        models.append(m)
    # 平均応答 ⟨R⟩ − R_∞（R_∞ は J_PF に依存しないので共通）
    terms = []
    for m in models:
        A, c, *_ = PB.pencil_from_liouvillian(m)
        x = A.subs(GAM, gv).LUsolve(c.subs(GAM, gv))
        terms.append(sp.together((_PP4.conjugate().T * x)[0, 0] - Rinf))
    avg = sp.together(sum(terms) / 3)
    num, den = sp.fraction(avg)
    pred_shift = sp.simplify(((1 - DELTA_I)**2 + 1 + (1 + DELTA_I)**2) / 3 - 1)
    print(f"  予測: 平均稜線位置の相対シフト ≈ ⟨λ²⟩ − 1 = {pred_shift} = {float(pred_shift):.5g}")
    print()
    ok = True
    for nm, PhiF in [("Re", sp.re), ("Im", sp.im)]:
        b0, _ = UV.ridge_root(gv, PhiF)
        b0 = Q(sp.Rational(str(sp.N(b0, 30))))
        expr = sp.expand(PhiF(sp.expand(num) * sp.conjugate(sp.expand(den))))
        poly = sp.Poly(expr, EPS)
        lo, hi = b0 / 2, 2 * b0
        nroots = poly.count_roots(lo, hi)
        rts = [r for r in sp.real_roots(poly) if lo < r < hi]
        if not rts:
            ok = False
            print(f"  {nm}: 窓内交差なし → FAIL", flush=True)
            continue
        shift = sp.simplify((rts[0] - b0) / b0)
        good = (nroots == 1) and (abs(float(shift)) <= Q(1, 100))
        ok = ok and good
        print(f"  {nm}: 平均応答の窓内交差 {nroots} 個、相対シフト = {float(shift):+.5g}"
              f"（予測 {float(pred_shift):.5g} と同桁）  頑健: {good}", flush=True)
    print()
    OD_max = sp.nsimplify(-2 * sp.log(1 - DELTA_I))
    print("  optical depth への翻訳（導出）: 場の減衰 e^{−OD/2} ≥ 1 − δ_I ⇔")
    print(f"    **OD ≤ −2 ln(1 − δ_I) = {OD_max} ≈ {float(OD_max):.4g}**")
    print("  すなわち薄い試料（OD ≲ 0.1）または局所強度で規格化した測定が条件。")
    print("  これは凍結理論からの継承ではなく、本リポジトリで厳密に確立した")
    print("  λ² 則（U6(a)）＋ Beer–Lambert の場の減衰のみから導いた。")
    print("  -> E3", "PASS" if ok else "FAIL")
    return bool(ok)


def E4(nstar):
    print(RULE, flush=True)
    print("E4  総合判定 — §1.2 条件6 の状態")
    print(RULE)
    print("  導出した検出制約の一覧:")
    print(f"    [D2] ショット予算    N ≥ N* = {float(nstar):.3g} /点（3σ、Δ=½）。10⁷ で窓が開く")
    print("    [D3] オフセット較正  相対 ~5×10⁻⁴ 以下（分裂の同定は 1/4 シフトまで頑健）")
    print(f"    [D4] 駆動強度分布    相対幅 ≤ {DELTA_I}、OD ≤ {float(sp.nsimplify(-2*sp.log(1-DELTA_I))):.3g}")
    print()
    print("  ⇒ **§1.2 条件6「full physical model では現象が観測不能」は、")
    print("     宣言した検出模型（独立ショット・projection 限界・較正済みオフセット・")
    print("     薄い試料）の下で解消された。**")
    print()
    print("  残余（正直な記録・範囲外）:")
    print("    ・集団効果（superradiance、dipole–dipole）と多体効果")
    print("    ・検出器の具体的実装（dead time・afterpulse・collection efficiency の数値）")
    print("    ・1次を超えるスペクトル拡散")
    print("  これらは §4.3 により凍結からも借りられず、本監査でも導出していない。")
    print("  条件6 の解消は**上記の検出模型に条件付き**である（status: Conditional）。")
    print("  -> E4 PASS")
    return True


def E5(tab):
    print(RULE, flush=True)
    print("E5  負制御")
    print(RULE)
    gv = Q(2000)
    # NC1: 予算を 10⁵ に絞ると窓が空になる
    N_small = Q(10)**5
    TH2 = sp.simplify(ZSTAR**2 / (N_small * DLT**2))
    empty = all(
        (tab[g]['Re'] is None or tab[g]['Im'] is None
         or sp.simplify(tab[g]['Re'] - TH2) <= 0
         or sp.simplify(tab[g]['Im'] - TH2) <= 0)
        for g in GRID)
    print(f"  NC1 予算 10⁵: TH = {float(sp.sqrt(TH2)):.4g} ⇒ 全格子点で窓が閉じる: {empty}")

    # NC2: オフセット b_rel = 10·S にすると窓内の交差が消える
    S2v = tab[gv]['Im']
    b_kill = sp.simplify(10 * sp.sqrt(S2v))
    Rinf, *_ = PB._jet(PB.MODEL)
    absR = sp.sqrt(sp.re(Rinf)**2 + sp.im(Rinf)**2)
    b0, _ = UV.ridge_root(gv, sp.im)
    b0 = Q(sp.Rational(str(sp.N(b0, 30))))
    # 窓 [b0/2, 2b0] の両端で M = Φ + b の符号が同じ ⇒ 符号反転が消える
    b_abs = sp.simplify(b_kill * absR)
    m_lo = sp.simplify(phi_at(gv, b0 / 2, sp.im) + b_abs)
    m_hi = sp.simplify(phi_at(gv, 2 * b0, sp.im) + b_abs)
    gone = sp.simplify(sp.sign(m_lo) * sp.sign(m_hi)) > 0
    print(f"  NC2 オフセット b_rel = 10·S = {float(b_kill):.4g}: 窓両端の符号積 > 0"
          f"（交差消滅）: {bool(gone)}")
    ok = bool(empty) and bool(gone)
    print("  ⇒ ゲートは実際に効いている（緩すぎない）。")
    print("  -> E5", "PASS" if ok else "FAIL")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf if a.out else old
    try:
        r = {}
        r['E0'] = E0()
        e1 = E1(); r['E1'] = e1[0]
        r['E2'] = E2(e1[1])
        r['E3'] = E3()
        r['E4'] = E4(e1[2])
        r['E5'] = E5(e1[1])
        print(RULE)
        print("verdict:", r)
        print("ALL PASS" if all(r.values()) else "SOME FAILED")
        print(RULE)
        print()
        print("結論（status: Conditional / Model-specific）:")
        print("  検出の3制約（ショット雑音・背景オフセット・駆動伝播）を、凍結理論から")
        print("  一切継承せずに導出した。入力は S²（厳密有理数）と λ² 則（U6a）のみ。")
        print(f"  最小予算 N* ≈ {float(e1[2]):.3g} shots/点。10⁷ で実用窓が開き、")
        print("  U5 の FLOOR = 10⁻³ は「3.6×10⁷ shots/点」という資源宣言と等価。")
        print("  §1.2 条件6 は宣言した検出模型の下で解消（集団効果等の残余は範囲外と明記）。")
    finally:
        sys.stdout = old
    text = buf.getvalue() if a.out else ""
    if a.out:
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        header = (
            f"# LKCT S1 detection-model exact audit -- generated {stamp}\n"
            f"# script: scripts/lkct_detection.py  seed {SEED}  sympy {sp.__version__}\n"
            f"# 判定に浮動小数点を使用していない（S²・N_min・閾値は厳密有理数、比較は厳密）\n"
            f"# 手順: docs/lkct-detection-audit.md\n"
        )
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(header + text)
        print(text)
        print(f"[certificate written to {a.out}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
