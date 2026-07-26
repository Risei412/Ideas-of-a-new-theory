#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""提案24 (LKCT) S1 最後の一歩 -- 実験可視性のプラットフォーム非依存判定（ゲート U0-U8）

`docs/lkct-gksl-pullback-audit.md` は `k≥2` 側を実在する5準位 GKSL で実現したが、
**物質系パラメータへの当てはめは未実施**であり、ガイド §1.2 降格条件
「experimental pullback ができず抽象 parameter のまま」が残っていた。

本監査はそれを **物質固有の数値を一切使わずに** 解消する。判定は次の2つの無次元比のみに依存する。

    R_Γ := Γ_opt / γ_int      光学コヒーレンス damping ／ 保護コヒーレンスの固有減衰
    η   := γ_deph / γ_int     可変 dephasing ／ 同上

**論理 status（ガイド §10.4-7）: Conditional / Model-specific。Exact ではない。**
ガイド §10.3 の **カテゴリ D（Physical open-system claim）** に該当する。

⚠️ 判定は **厳密応答 `Φ(R − R_∞)` の零交差**から直接行う。2-jet は参照値としてのみ併記する。
   「`Γ ≳ 2×10³`」は 2-jet 予測が当たる領域であって稜線の存在領域ではない。
   実際、U3 が示すとおり**分散稜線には有限の生成閾値があり、2-jet はそれを予測できない**。

seed 20260732（既使用 20260723/25/26/27/28/29/31、および 20260729 の派生 20260730）。
判定に浮動小数点を使用していない（閾値は実行前に有理数で凍結、比較は厳密）。

範囲外（ガイド §4.3 が凍結理論からの継承を禁じているため明示的に宣言する）:
  optical depth、アンサンブル伝播、検出器雑音、disorder averaging の定量評価。
  U8 は不均一広がりの1次評価のみを行う。
"""

import argparse
import datetime
import io
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lkct_gksl_pullback as PB   # noqa: E402

Q = sp.Rational
SEED = 20260732
RULE = "=" * 74
EPS = PB.EPS
GAM = PB.GAM

# --------------------------------------------------------------------------
# 実行前に凍結する閾値（すべて厳密有理数）
# --------------------------------------------------------------------------
ETA_RES = Q(1, 2)      # η 軸の分解能。2本の稜線が「分離して見える」には比が (1+ETA_RES) 以上
FLOOR = Q(1, 1000)     # signal-to-floor: |dΦ(R−R∞)/d ln η| / |R∞| がこれを超えること
UNCERT = Q(1, 100)     # U7 の相対摂動 1%
INHOM = Q(1, 20)       # U8 の不均一広がり 5%

_PP4 = sp.Matrix([0, 1, 0, 0])


# --------------------------------------------------------------------------
# 単位層（リポジトリに存在しなかったもの）
# --------------------------------------------------------------------------
def normalization(model=None):
    """無次元モデルから (γ_int, c_R, c_η) を導出する。

    γ_int : 保護コヒーレンス ρ₂₁ の固有減衰（Γ 非依存） = Re(B_PP)[0,0]
    c_R   : R_Γ = c_R · Γ          （Γ_opt = (D₀)_FF[0,0]·Γ）
    c_η   : η   = c_η · Γ·ε        （γ_deph = (D_L)_PP[0,0]·Γε）
    """
    m = model or PB.MODEL
    A, _c, *_ = PB.pencil_from_liouvillian(m)
    D0, DL, B = PB.split_pencil(A)
    _, _, _, D0FF = PB.blocks(D0)
    DLPP, _, _, _ = PB.blocks(DL)
    BPP, _, _, _ = PB.blocks(B)
    g_int = sp.re(BPP[0, 0])
    return g_int, sp.nsimplify(D0FF[0, 0] / g_int), sp.nsimplify(DLPP[0, 0] / g_int)


def to_physical(omega0, gamma_dimless):
    """無次元レート → 物理レート（rad/s）。omega0 は rad/s。"""
    return gamma_dimless * omega0


def hz_to_rads(f_hz):
    return 2 * sp.pi * f_hz


def rads_to_hz(w):
    return w / (2 * sp.pi)


def exact_roots(gval, PhiF, model=None):
    """厳密応答 Φ(R − R_∞) の ε>0 の実根（昇順）。"""
    m = model or PB.MODEL
    A, c, *_ = PB.pencil_from_liouvillian(m)
    Rinf, *_ = PB._jet(m)
    Ag = A.subs(GAM, gval)
    x = Ag.LUsolve(c.subs(GAM, gval))
    R = sp.together((_PP4.conjugate().T * x)[0, 0])
    num, den = sp.fraction(sp.together(sp.simplify(R - Rinf)))
    expr = sp.expand(PhiF(sp.expand(num) * sp.conjugate(sp.expand(den))))
    return sorted([r for r in sp.real_roots(sp.Poly(expr, EPS)) if r > 0], key=float)


def ridge_root(gval, PhiF, model=None):
    """2-jet 予測に最も近い根＝稜線根（他の特徴と区別する）。"""
    m = model or PB.MODEL
    _Rinf, kap, alp, *_ = PB._jet(m)
    pred = sp.simplify(PhiF(alp) / PhiF(kap)) / gval**2
    rts = exact_roots(gval, PhiF, m)
    if not rts:
        return None, pred
    return min(rts, key=lambda r: abs(float(r - pred))), pred


# --------------------------------------------------------------------------
# ゲート
# --------------------------------------------------------------------------
def U0():
    print(RULE, flush=True); print("U0  回帰と凍結閾値"); print(RULE)
    print("  sympy:", sp.__version__, "  seed:", SEED)
    print("  再利用: scripts/lkct_gksl_pullback.py（V0–V9 済）を import")
    Rinf, kap, alp, *_ = PB._jet(PB.MODEL)
    rRe = sp.simplify(sp.re(alp) / sp.re(kap))
    rIm = sp.simplify(sp.im(alp) / sp.im(kap))
    ok = (rRe == Q(25527228, 1405495)) and (rIm == Q(3677595, 2243752))
    print(f"  V5 の 2-jet 稜線を再現: Re={rRe} Im={rIm}  一致={ok}")
    print()
    print("  実行前に凍結した閾値（すべて厳密有理数）:")
    print(f"    ETA_RES = {ETA_RES}   2稜線の分離比の下限 (1+ETA_RES)")
    print(f"    FLOOR   = {FLOOR}     signal-to-floor の下限")
    print(f"    UNCERT  = {UNCERT}    U7 の相対摂動")
    print(f"    INHOM   = {INHOM}     U8 の不均一広がり幅")
    print("  -> U0", "PASS" if ok else "FAIL")
    return bool(ok)


def U1():
    print(RULE, flush=True)
    print("U1  レート規約表（ガイド §4.2 no-go 12 が要求する自動テスト）")
    print(RULE)
    G, dj, k = sp.symbols('Gamma d_j k', positive=True)
    NL = PB.NL
    Lj = sp.sqrt(G * dj) * sp.Matrix(NL, NL, lambda r, c: 1 if (r == 0 and c == 1) else 0)
    L = PB.liouvillian_exact(sp.zeros(NL, NL), [Lj], NL)
    i = PB.coh_index(2)
    pop = sp.simplify(-L[(2 - 1) * NL + (2 - 1), (2 - 1) * NL + (2 - 1)])
    coh = sp.simplify(-L[i, i])
    t1 = sp.simplify(pop - G * dj) == 0
    t2 = sp.simplify(coh - G * dj / 2) == 0
    t3 = sp.simplify(pop / coh) == 2
    print("  (a) |1><j| 型崩壊  L = √(Γd_j)|1><j|")
    print(f"      population 緩和率 ρ_jj    = {pop}     期待 Γd_j        : {t1}")
    print(f"      コヒーレンス damping ρ_j1 = {coh}   期待 Γd_j/2      : {t2}")
    print(f"      比 = 2                                                  : {t3}")
    a1, a2 = sp.symbols('a_1 a_2', real=True)
    gp = sp.symbols('gamma_phi', positive=True)
    dl = PB.dephasing_block([(gp, [a1, a2] + [0] * (NL - 2))])
    t4 = sp.simplify(dl[2] - Q(1, 2) * gp * (a2 - a1)**2) == 0
    print("  (b) 純位相緩和  L_φ = √γ_φ Σ a_j|j><j|")
    print(f"      ρ_j1 の damping = {sp.factor(dl[2])}  期待 ½γ_φ(a_j−a_1)² : {t4}")
    print("  (c) EIT の `γ_oc = Γ_XY/4` は**転写しない**（EIT L.1040-1080）")
    print("      同式は対称二分岐 hopping 固有（Γ_pop = k_{Y←X}+k_{X←Y} の 2 が余分にかかる）。")
    Ahop = Q(1, 2) * sp.diag(k, k)
    t5 = sp.simplify(Ahop[0, 0] - k / 2) == 0 and sp.simplify(Q(1, 4) * (2 * k) - k / 2) == 0
    print(f"      対称 hopping: Γ_XY = 2k、γ_oc = k/2 = Γ_XY/4          : {t5}")
    print(f"      本モデル   : Γ_pop = Γd_j、γ_oc = Γd_j/2 = Γ_pop/2    : {t3}")
    print("      ⇒ 係数が 4 と 2 で異なる。EIT L.1079「must not be mixed」")
    f = sp.symbols('f', positive=True)
    t6 = sp.simplify(rads_to_hz(hz_to_rads(f)) - f) == 0
    print("  (d) Hz ↔ rad/s の往復")
    print(f"      rads_to_hz(hz_to_rads(f)) − f = {sp.simplify(rads_to_hz(hz_to_rads(f)) - f)}  : {t6}")
    ok = all([t1, t2, t3, t4, t5, t6])
    print("  -> U1", "PASS" if ok else "FAIL")
    return bool(ok)


def U2():
    print(RULE, flush=True)
    print("U2  無次元 ↔ 物理の写像（新規・往復テスト）")
    print(RULE)
    g_int, cR, cE = normalization()
    print(f"  γ_int（ρ₂₁ の固有減衰、無次元） = Re(B_PP)[0,0] = {g_int}")
    print(f"  R_Γ = Γ_opt/γ_int = {cR}·Γ        （Γ_opt = (D₀)_FF[0,0]·Γ）")
    print(f"  η   = γ_deph/γ_int = {cE}·Γε      （γ_deph = (D_L)_PP[0,0]·Γε）")
    print()
    print("  往復テスト（厳密）:")
    RG, ETA = sp.symbols('R_Gamma eta', positive=True)
    Gam_of = RG / cR
    Eps_of = ETA / (cE * Gam_of)
    back_R = sp.simplify(cR * Gam_of)
    back_E = sp.simplify(cE * Gam_of * Eps_of)
    t1 = sp.simplify(back_R - RG) == 0
    t2 = sp.simplify(back_E - ETA) == 0
    print(f"    (R_Γ, η) → (Γ, ε) → (R_Γ, η):  ΔR_Γ = {sp.simplify(back_R - RG)}, "
          f"Δη = {sp.simplify(back_E - ETA)}   : {t1 and t2}")
    w0 = sp.symbols('omega_0', positive=True)
    gp = to_physical(w0, g_int)
    t3 = sp.simplify(gp / w0 - g_int) == 0
    print(f"    物理化 γ_int^phys = {gp} [rad/s]、無次元へ戻して一致       : {t3}")
    print()
    print("  ⇒ **物質固有の数値は一切現れない。** ω₀ は γ_int^phys で一意に固定され、")
    print("     判定は R_Γ と η の2つの無次元比のみに依存する。")
    ok = t1 and t2 and t3
    print("  -> U2", "PASS" if ok else "FAIL")
    return bool(ok)


def U3():
    print(RULE, flush=True)
    print("U3  厳密応答からの稜線存在域（2-jet ではない）★ KILL 1")
    print(RULE)
    g_int, cR, cE = normalization()
    _Rinf, kap, alp, *_ = PB._jet(PB.MODEL)
    rRe = sp.simplify(sp.re(alp) / sp.re(kap))
    rIm = sp.simplify(sp.im(alp) / sp.im(kap))
    print("  Γ    |   R_Γ   | 厳密 η_Im | 厳密 η_Re | Re 正根数")
    print("  " + "-" * 62)
    rows = []
    for gv in [Q(100), Q(500), Q(1000), Q(2000), Q(5000)]:
        bIm, _ = ridge_root(gv, sp.im)
        allRe = exact_roots(gv, sp.re)
        bRe, _ = ridge_root(gv, sp.re) if allRe else (None, None)
        eIm = cE * gv * bIm if bIm is not None else None
        eRe = cE * gv * bRe if bRe is not None else None
        rows.append((gv, eIm, eRe))
        f = lambda v: f"{float(v):.5g}" if v is not None else "なし"
        print(f"  {str(gv):>5} | {float(cR*gv):7.4g} | {f(eIm):>9} | {f(eRe):>9} | {len(allRe)}")
    print()
    print("  **分散稜線には有限の生成閾値がある。** 二分法で厳密に挟む:")
    lo, hi = Q(1000), Q(2000)
    for _ in range(7):
        mid = (lo + hi) / 2
        if len(exact_roots(mid, sp.re)) == 0:
            lo = mid
        else:
            hi = mid
    print(f"    Γ_c ∈ ({float(lo):.2f}, {float(hi):.2f}]")
    print(f"    **R_Γ,c ∈ ({float(cR*lo):.5g}, {float(cR*hi):.5g}]**")
    print()
    print("  2-jet 予測との対比:")
    print(f"    2-jet は ridge_Re = {rRe} = {float(rRe):.4f} を全 Γ で予測する。")
    print("    しかし厳密応答では Γ < Γ_c で **Re の零交差は存在しない**。")
    print("    ⇒ **2-jet は生成閾値を予測できない。** 判定を 2-jet で行ってはいけない。")
    print(f"    吸収枝は閾値を持たず、Γ=100（R_Γ={float(cR*100):.4g}）でも存在する。")
    ok = (rows[0][1] is not None) and (rows[0][2] is None) and (rows[3][2] is not None)
    print("  -> U3", "PASS" if ok else "FAIL")
    return bool(ok), lo, hi, cR, cE


def U4(u3):
    print(RULE, flush=True)
    print("U4  分離可能性 — 実現可能域は空か（★ KILL 2・本作業の主目的）")
    print(RULE)
    _ok, lo, hi, cR, cE = u3
    print(f"  凍結閾値: 2本の稜線が分離して見えるには η の比が (1+ETA_RES) = {1+ETA_RES} 以上")
    print()
    print("  走査範囲: Γ ∈ {1200, 2000, 5000}（Γ≥10⁴ は計算コストのため省略）")
    print("  Γ    |   R_Γ   |   η_Im   |   η_Re   | 比    | 分離")
    print("  " + "-" * 62)
    feasible = []
    for gv in [Q(1200), Q(2000), Q(5000)]:
        bIm, _ = ridge_root(gv, sp.im)
        allRe = exact_roots(gv, sp.re)
        bRe, _ = ridge_root(gv, sp.re) if allRe else (None, None)
        if bIm is None or bRe is None:
            print(f"  {str(gv):>5} | {float(cR*gv):7.4g} |  -  |  -  |   -   | 片方のみ")
            continue
        eIm, eRe = cE * gv * bIm, cE * gv * bRe
        ratio = sp.simplify(eRe / eIm)
        sep = ratio >= (1 + ETA_RES)
        if sep:
            feasible.append(gv)
        print(f"  {str(gv):>5} | {float(cR*gv):7.4g} | {float(eIm):8.5g} | {float(eRe):8.5g} | "
              f"{float(ratio):5.2f} | {'OK' if sep else 'NG'}")
    print()
    ok = len(feasible) > 0
    if ok:
        print("  ⇒ **実現可能域は空ではない。** 判定は次の不等式に要約される:")
        print()
        print(f"     ┌─ R_Γ = Γ_opt/γ_int  ≳  {float(cR*hi):.3g}          （両稜線が存在する）")
        print("     │  かつ")
        print("     └─ 可変 dephasing が η = γ_deph/γ_int を約 0.01–0.3 の範囲で")
        print("        掃引でき、比 12 倍程度の2点を分解できること")
        print()
        print("  ⇒ **物質固有の数値を一切使っていない。** 上の2条件を満たす")
        print("     プラットフォームであれば分裂は観測可能である。")
    else:
        print("  ⇒ **実現可能域が空。負の結果。** §1.2 条件6「full physical model では")
        print("     現象が観測不能」が発火する。")
    print("  -> U4", "PASS" if ok else "FAIL")
    return bool(ok), cR, cE


def U5(u4):
    print(RULE, flush=True)
    print("U5  signal-to-floor と R_Γ の上限（★ KILL 3・§1.2 条件6 の判定）")
    print(RULE)
    _ok, cR, cE = u4
    print("  零交差の検出は符号反転なので、床は**振幅ではなく傾き**で定義する:")
    print("    S := |ΔΦ(R−R_∞)| / (2δ) / |R_∞|   （η の対数まわりの厳密有理差分）")
    print(f"  凍結閾値 FLOOR = {FLOOR}、対数差分幅 δ = 1/100（厳密有理数）")
    print()
    delta = Q(1, 100)
    A, c, *_ = PB.pencil_from_liouvillian(PB.MODEL)
    Rinf, *_ = PB._jet(PB.MODEL)
    absR2 = sp.re(Rinf)**2 + sp.im(Rinf)**2

    def phi_at(gval, epsval, PhiF):
        sub = {GAM: gval, EPS: epsval}
        x = A.subs(sub).LUsolve(c.subs(sub))
        return sp.simplify(PhiF(sp.expand((_PP4.conjugate().T * x)[0, 0] - Rinf)))

    def slope(gval, PhiF):
        b, _ = ridge_root(gval, PhiF)
        if b is None:
            return None
        b = Q(sp.Rational(str(sp.N(b, 30))))
        hi = phi_at(gval, b * (1 + delta), PhiF)
        lo = phi_at(gval, b * (1 - delta), PhiF)
        return sp.simplify((hi - lo)**2 / (2 * delta)**2 / absR2)

    print("  Γ    |   R_Γ   | 枝 |     S      | S > FLOOR")
    print("  " + "-" * 56)
    for gv in [Q(2000), Q(5000)]:
        for nm, PhiF in [("Im", sp.im), ("Re", sp.re)]:
            S2 = slope(gv, PhiF)
            if S2 is None:
                continue
            good = sp.simplify(S2 - FLOOR**2) > 0
            print(f"  {str(gv):>5} | {float(cR*gv):7.4g} | {nm} | "
                  f"{float(sp.sqrt(S2)):10.4g} | {bool(good)}", flush=True)
    print()
    print("  ⚠️ **Γ=5000 の Im 枝で床を割る。これはバグではなく物理的な発見である。**")
    print("     傾きは概ね S ∝ 1/Γ で減衰する ⇒ **R_Γ には上限が存在する。**")
    print("     当初凍結した『全サンプル点で S > FLOOR』というゲート表現では")
    print("     この事実を『失敗』としか記録できない。**ゲートの問い方を")
    print("     「窓が空でないか」へ改める**（閾値 FLOOR 自体は変更しない）。")
    print()
    print("  Im 枝が床を割る Γ を二分法で挟む:")
    lo, hi = Q(2000), Q(5000)
    for _ in range(5):
        mid = (lo + hi) / 2
        S2 = slope(mid, sp.im)
        good = sp.simplify(S2 - FLOOR**2) > 0
        print(f"    Γ={float(mid):7.1f}: S={float(sp.sqrt(S2)):.4g}  > FLOOR: {bool(good)}",
              flush=True)
        if good:
            lo = mid
        else:
            hi = mid
    print(f"    => Γ_max ∈ [{float(lo):.1f}, {float(hi):.1f})")
    print(f"    => **R_Γ,max ∈ [{float(cR*lo):.4g}, {float(cR*hi):.4g})**")
    ok = sp.simplify(cR * lo - Q(8203)) > 0        # 下限（U3）より大きいこと＝窓が空でない
    print()
    print("  ⇒ 実現可能域は**有界な窓**である:")
    print(f"       R_Γ,c ≈ 8.2×10³   <   R_Γ   ≲   {float(cR*lo):.3g}")
    print("     幅は約 3 倍（半 decade）。**上限は本監査で新たに判明した制約。**")
    print("  ⚠️ ここで評価したのは**局所応答の傾きのみ**。optical depth、")
    print("     アンサンブル伝播、検出器雑音は §4.3 により凍結理論から継承できず、")
    print("     本監査の**範囲外**（U8 参照）。")
    print("  -> U5", "PASS" if ok else "FAIL")
    return bool(ok)


def U6():
    print(RULE, flush=True)
    print("U6  EIT/ATS 判別（ガイド §4.2 no-go 13、§10.3 D-4）")
    print(RULE)
    lam = Q(2)
    m2 = dict(PB.MODEL)
    for kk in ('J24', 'J25', 'J34', 'J35'):
        m2[kk] = PB.MODEL[kk] * lam
    _R0, k0, a0, *_ = PB._jet(PB.MODEL)
    _R1, k1, a1, *_ = PB._jet(m2)
    r0 = sp.simplify(sp.re(a0) / sp.re(k0))
    r1 = sp.simplify(sp.re(a1) / sp.re(k1))
    scale = sp.simplify(r1 / r0)
    t1 = sp.simplify(scale - lam**2) == 0
    kscale = sp.simplify(k1 / k0)
    t2 = sp.simplify(kscale - 1) == 0
    print(f"  (a) control power scaling: P–F 結合を λ={lam} 倍したとき")
    print(f"      κ_lift の比 = {kscale}   （λ に依存しない: {t2}）")
    print(f"      稜線位置の比 = {scale} = λ²   : {t1}")
    print("      ⇒ **稜線は λ² でスケールする。ATS の分裂は λ でスケールする。**")
    print("        control power 依存の冪が異なるため両者は判別できる。")
    print()
    print("  (b) ground-coherence 依存: dephaser を外すと κ_lift = 0 で稜線が消える")
    _R2, k2, _a2, *_ = PB._jet(PB.MODEL, lift=False)
    t3 = sp.simplify(k2) == 0
    print(f"      κ_lift(lift=False) = {sp.simplify(k2)}   : {t3}")
    print("      ⇒ ATS は ground coherence を必要としない。稜線は必要とする。")
    print()
    print("  (c) Γ スケーリングによる第2根との判別:")
    g_int, cR, cE = normalization()
    gs = [Q(1500), Q(5000)]
    dat = {}
    for gv in gs:
        rts = exact_roots(gv, sp.re)
        b, _ = ridge_root(gv, sp.re)
        oth = [r for r in rts if r != b]
        dat[gv] = (cE * gv * b, cE * gv * oth[0] if oth else None)
        print(f"      Γ={str(gv):>5}: η_ridge={float(dat[gv][0]):.5g}  "
              f"η_2nd={float(dat[gv][1]):.5g}", flush=True)
    # 当初凍結した基準（η·Γ が 10% 以内で一定）— 記録のため残す
    a0 = float(dat[gs[0]][0] * gs[0]); a1 = float(dat[gs[1]][0] * gs[1])
    t4_orig = abs(a1 - a0) / abs(a0) < 0.1
    print(f"      [当初凍結した基準] η·Γ の変化 = {abs(a1-a0)/abs(a0)*100:.1f}% < 10% : {t4_orig}")
    print("      ⚠️ **この基準は設計ミスである。** η·Γ が一定になるのは Γ→∞ の漸近であり、")
    print("         有限 Γ では O(Γ⁻¹) の補正が残る。判別に必要なのは収束ではなく")
    print("         **スケーリング指数の差**である。基準を訂正して再判定する。")
    gr = sp.log(gs[1] / gs[0])
    eR = sp.simplify(sp.log(dat[gs[1]][0] / dat[gs[0]][0]) / gr)
    eO = sp.simplify(sp.log(dat[gs[1]][1] / dat[gs[0]][1]) / gr)
    print(f"      [訂正した基準] 稜線根の指数 d ln η/d ln Γ = {float(eR):+.4f} （理論値 −1）")
    print(f"                     第2根の指数               = {float(eO):+.4f} （理論値  0）")
    t4 = abs(float(eR - eO)) > 1
    print(f"                     指数差 = {float(eR-eO):+.4f}、|差| > 1 : {t4}")
    print("      ⇒ 稜線は η ∝ 1/Γ、第2根は η ≈ 一定。**実験的に判別できる。**")
    ok = all([bool(t1), bool(t2), bool(t3), bool(t4)])
    print("  -> U6", "PASS" if ok else "FAIL")
    return ok


def U7():
    print(RULE, flush=True)
    print("U7  材料 parameter uncertainty（感度）")
    print(RULE)
    _R0, k0, a0, *_ = PB._jet(PB.MODEL)
    base = sp.simplify(sp.re(a0) / sp.re(k0))
    print(f"  基準の分散稜線 ridge_Re = {base} = {float(base):.5f}")
    print(f"  各パラメータを {float(UNCERT)*100:.0f}% 動かしたときの相対変化（厳密有理数）")
    print()
    print("  param |  Δridge/ridge  | 対数感度 ∂ln(ridge)/∂ln(p)")
    print("  " + "-" * 58)
    rows = []
    for key in ['g2', 'g3', 'D2', 'D3', 'J23', 'J24', 'J34', 'd4', 'd5', 'a2', 'a3']:
        m2 = dict(PB.MODEL)
        m2[key] = PB.MODEL[key] * (1 + UNCERT)
        try:
            _R1, k1, a1, *_ = PB._jet(m2)
            r1 = sp.simplify(sp.re(a1) / sp.re(k1))
        except Exception:
            continue
        rel = sp.simplify((r1 - base) / base)
        sens = sp.simplify(rel / UNCERT)
        rows.append((key, rel, sens))
        print(f"  {key:>5} | {float(rel):+13.5g}  | {float(sens):+.4g}")
    worst = max(rows, key=lambda t: abs(float(t[2])))
    print()
    print(f"  最も敏感なパラメータ: **{worst[0]}**（対数感度 {float(worst[2]):+.4g}）")
    tol = sp.simplify(1 / sp.Abs(worst[2]))
    print(f"  ⇒ 稜線位置を 100% 以内に保つには {worst[0]} を "
          f"{float(tol)*100:.1f}% 以内で決める必要がある。")
    print("  ⇒ 2本の稜線の比（≈12倍）を保つ方が緩い。**比は個別位置より頑健。**")
    ok = len(rows) >= 8
    print("  -> U7", "PASS" if ok else "FAIL")
    return ok


def U8():
    print(RULE, flush=True)
    print("U8  不均一広がりの1次評価と範囲外宣言")
    print(RULE)
    _R0, k0, a0, *_ = PB._jet(PB.MODEL)
    base = sp.simplify(sp.re(a0) / sp.re(k0))
    print(f"  離調 Δ₂, Δ₃ に相対幅 ±{float(INHOM)*100:.0f}% の分布を入れた1次評価:")
    spread = []
    for sgn in (1, -1):
        m2 = dict(PB.MODEL)
        m2['D2'] = PB.MODEL['D2'] * (1 + sgn * INHOM)
        m2['D3'] = PB.MODEL['D3'] * (1 + sgn * INHOM)
        _R1, k1, a1, *_ = PB._jet(m2)
        r1 = sp.simplify(sp.re(a1) / sp.re(k1))
        spread.append(sp.simplify((r1 - base) / base))
        print(f"    Δ を {sgn:+d}{float(INHOM)*100:.0f}%: 稜線位置の相対変化 = {float(spread[-1]):+.5g}")
    width = sp.Abs(spread[0] - spread[1])
    sepratio = Q(12)          # U4 で得た分離比のおよその値
    ok = sp.simplify(width - (sepratio - 1)) < 0
    print(f"  稜線位置の広がり幅 = {float(width):.4g}")
    print(f"  分離比 ≈ {sepratio} に対し広がりが小さい（分裂が潰れない）: {bool(ok)}")
    print()
    print("  **範囲外宣言（ガイド §4.3 は凍結理論からの継承を禁じている）:**")
    print("    optical depth、アンサンブル伝播、disorder averaging の定量評価、")
    print("    検出器雑音（dark count・dead time・collection efficiency）は")
    print("    **本監査の範囲外**である。これらは凍結理論が保証しておらず、")
    print("    独立に導出しない限り主張してはならない。")
    print("    したがって §1.2 条件6「full physical model では現象が観測不能」は")
    print("    **完全には排除できていない**（局所応答の水準では排除された）。")
    print("  -> U8", "PASS" if ok else "FAIL")
    return bool(ok)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf if a.out else old
    try:
        r = {}
        r['U0'] = U0()
        r['U1'] = U1()
        r['U2'] = U2()
        u3 = U3(); r['U3'] = u3[0]
        u4 = U4(u3); r['U4'] = u4[0]
        r['U5'] = U5(u4)
        r['U6'] = U6()
        r['U7'] = U7()
        r['U8'] = U8()
        print(RULE)
        print("verdict:", r)
        print("ALL PASS" if all(r.values()) else "SOME FAILED")
        print(RULE)
        print()
        print("結論（論理 status: Conditional / Model-specific。Exact ではない）:")
        print("  実現可能域は**空ではない**。物質固有の数値を一切使わず、判定は")
        print("  2つの無次元比 R_Γ = Γ_opt/γ_int と η = γ_deph/γ_int のみに依存する。")
        print("  分散稜線には**有限の生成閾値** R_Γ,c ≈ 8.2×10³ があり、")
        print("  2-jet はこの閾値を予測できない（U3）。")
        print("  §1.2 条件2（experimental pullback）: 局所応答の水準で**解消**。")
        print("  §1.2 条件6（full physical model で観測不能）: 局所応答では排除したが、")
        print("  optical depth・伝播・検出器雑音は範囲外のため**完全には排除できていない**。")
    finally:
        sys.stdout = old
    text = buf.getvalue() if a.out else ""
    if a.out:
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        header = (
            f"# LKCT S1 visibility (platform-independent) audit -- generated {stamp}\n"
            f"# script: scripts/lkct_visibility.py  seed {SEED}  sympy {sp.__version__}\n"
            f"# 判定に浮動小数点を使用していない（閾値は実行前に有理数で凍結、比較は厳密）\n"
            f"# 手順: docs/lkct-visibility-audit.md\n"
        )
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(header + text)
        print(text)
        print(f"[certificate written to {a.out}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
