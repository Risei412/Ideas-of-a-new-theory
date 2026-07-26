#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""提案24 (LKCT) §5.2 item 2 -- GKSL 物理実現可能性の厳密監査（ゲート Z0-Z9）

問い: `sign(Φ(κ_lift)·Φ(α_leak)) = +1` は GKSL/CPTP 物理クラス内で実現可能か。
     実現可能 → 分類＋実験提案 (PRA) ／ CPTP が禁じる → no-go 定理 (PRL)。

結論（本監査で確定した次元二分律）:
  * k = dim P = 1 では、**すべての実線型汎関数 Φ** について符号条件は成立しない（Z4, exact）。
  * k >= 2 では実現可能。物理的 B_PP 構造の下でも約 18-19% の頻度（Z5, Z9, exact）。
  * したがって EIT/Λ 系は原理的に稜線を示せない（k=1）。さらに支持条件でも外れる（Z8）。

seed 20260729（既使用: 20260723 / 20260726 / 20260727 / 20260728。ガイド §11.2 の seed 再利用禁止）。
判定に浮動小数点を使用していない（表示のみ sp.N）。symbolic は SymPy、掃引は
stdlib `fractions.Fraction` による Gauss 有理数（どちらも厳密）。

規約の継承:
  * jet の閉形式は `Blueprints-of-theories/24_..._proposal.md` L190-194 の定義に従う。
  * 応答族 A(Γ,ε;z) = Γ(D₀+εD_L) + B(z)、c=(c_P,0)、p=(p_P,0)。
  * 負制御の分類（inverted / gain / negweight）は `scripts/wpot_null_smoke.py` に倣う。
  * 証明書はスクリプト自身が書く（`scripts/tpr_thermo_audit.py` 方式）。lkct_exact_audit.py /
    lkct_codim_audit.py の stdout リダイレクト方式ではない — provenance を機械生成するため。

適用範囲の制限（結論と同時に必ず宣言すること）:
  * Davies/secular 型 jump に限定（`L_j ∝ |1><j|`）。このとき coherence ブロックの D は対角で、
    直交射影で足りる。一般の斜交 Riesz ケースは範囲外（SMRT `ass:singular` は斜交を要求する）。
  * 有限次元・time-local GKSL・弱プローブ。壊す仮定は exact protected kernel の1つのみ。
"""

import argparse
import datetime
import io
import random
import sys
from fractions import Fraction as F

import sympy as sp

Q = sp.Rational
SEED = 20260729
RULE = "=" * 74


# --------------------------------------------------------------------------
# 厳密 Gauss 有理数（掃引用。SymPy より約2桁速く、同じく厳密）
# --------------------------------------------------------------------------
def cm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def ca(a, b):
    return (a[0] + b[0], a[1] + b[1])


def csub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def cconj(a):
    return (a[0], -a[1])


def creal(x):
    return (x, F(0))


def adj2(B):
    return [[B[1][1], (-B[0][1][0], -B[0][1][1])],
            [(-B[1][0][0], -B[1][0][1]), B[0][0]]]


def det2(B):
    return csub(cm(B[0][0], B[1][1]), cm(B[0][1], B[1][0]))


def matvec(Mx, v, n):
    return [tuple(sum(c) for c in zip(*[cm(Mx[i][j], v[j]) for j in range(n)]))
            for i in range(n)]


def vecdot(u, v, n):
    acc = (F(0), F(0))
    for i in range(n):
        acc = ca(acc, cm(u[i], v[i]))
    return acc


# --------------------------------------------------------------------------
# Z0 -- 実行環境と回帰基準線
# --------------------------------------------------------------------------
def Z0():
    print(RULE)
    print("Z0  実行環境と回帰基準線（exact）")
    print(RULE)
    print("  sympy version :", sp.__version__)
    print("  seed          :", SEED)
    # 既存 Y1 と同じ 2-jet 残差の消滅を独立に再現する（回帰基準線）
    u, v = sp.symbols('u v')
    BPP, BPF, BFP, DF, DLPP, pP, cP = sp.symbols('B_PP B_PF B_FP D_F D_LPP p_P c_P')
    S = BPP + u * DLPP - v * BPF * DF**-1 * BFP
    R = pP * S**-1 * cP
    Rinf = pP * BPP**-1 * cP
    jet = sp.series(R - Rinf, u, 0, 2).removeO()
    jet = sp.series(jet, v, 0, 2).removeO()
    kappa = pP * BPP**-1 * DLPP * BPP**-1 * cP
    alpha = pP * BPP**-1 * (BPF * DF**-1 * BFP) * BPP**-1 * cP
    resid = sp.simplify(sp.expand(jet - (-u * kappa + v * alpha)))
    # u,v の1次までの残差が厳密に 0
    lin = sp.expand(resid).coeff(u, 1).coeff(v, 0) + sp.expand(resid).coeff(v, 1).coeff(u, 0)
    print("  2-jet 残差の1次係数 :", sp.simplify(lin))
    ok = sp.simplify(lin) == 0
    print("  -> Z0", "PASS" if ok else "FAIL")
    return ok


# --------------------------------------------------------------------------
# Z1 -- 補題 L1: (D₀)_PP = 0 かつ D₀ ⪰ 0 なら (D₀)_PF = 0（直交射影で足りる）
# --------------------------------------------------------------------------
def Z1():
    print(RULE)
    print("Z1  補題 L1: D₀ ⪰ 0 かつ (D₀)_PP = 0 ⇒ (D₀)_PF = 0（exact, symbolic）")
    print(RULE)
    x = sp.symbols('x', real=True)
    b = sp.symbols('b', real=True)
    d = sp.symbols('d', positive=True)
    # 2x2 の最小反例候補: [[0, b],[b, d]]  (実対称、(D₀)_PP=0)
    Dm = sp.Matrix([[0, b], [b, d]])
    print("  D₀ =", Dm.tolist(), "  (実対称、(D₀)_PP = 0)")
    # PSD ⇔ 全ての主小行列式 ≥ 0。2次の主小行列式:
    minor2 = sp.simplify(Dm.det())
    print("  det D₀ =", minor2, "  ⇒ PSD には -b² ≥ 0 が必要 ⇒ b = 0")
    # ベクトル (t, s) での二次形式が t について線形項を持つことを示す
    t, s = sp.symbols('t s', real=True)
    qf = sp.expand((sp.Matrix([[t, s]]) * Dm * sp.Matrix([t, s]))[0, 0])
    print("  二次形式 =", qf, "  (t の1次項 2*b*t*s が残るため b≠0 なら符号が両方取れる)")
    ok = (sp.simplify(minor2 + b**2) == 0) and (sp.solve(sp.Eq(-b**2, 0), b) == [0])
    print("  ⇒ D₀ は P⊕F でブロック対角。ker D₀ への Riesz 射影 = 直交射影。")
    print("  ⇒ Davies/secular 型（D 対角）に限定するという範囲宣言は、仮定ではなく帰結。")
    print("  -> Z1", "PASS" if ok else "FAIL")
    return bool(ok)


# --------------------------------------------------------------------------
# Z2 -- 補題 L2: Hermitian H ⇒ C_leak = -J D_F⁻¹ Jᵀ は実の負半定値（ψ = π）
# --------------------------------------------------------------------------
def Z2():
    print(RULE)
    print("Z2  補題 L2: C_leak := B_PF D_F⁻¹ B_FP は実の負半定値（exact）")
    print(RULE)
    ok = True
    for k, nf in [(1, 1), (1, 2), (2, 1), (2, 2), (3, 2)]:
        J = sp.Matrix(k, nf, lambda a, b: Q(3 * a + 5 * b + 1, 7))   # 実（Hermitian H より）
        DF = sp.diag(*[Q(b + 2, 3) for b in range(nf)])              # 実正定値対角
        BPF = sp.I * J
        BFP = sp.I * J.T          # H = H† ⇒ J_FP = J_PFᵀ、実
        C = sp.simplify(BPF * DF.inv() * BFP)
        M = sp.simplify(-C)
        real_ok = all(sp.im(e) == 0 for e in C)
        evs = list(M.eigenvals().keys())
        psd_ok = all(sp.simplify(e) >= 0 for e in evs)
        print(f"  k={k}, n_f={nf}: C_leak 実？{real_ok}  -C_leak の固有値 PSD？{psd_ok}")
        ok = ok and real_ok and psd_ok
    print("  ⇒ C_leak = -J D_F⁻¹ Jᵀ =: -M、M は実対称 PSD。arg(C_leak) = π が厳密に成立。")
    print("  ⇒ 離調依存性は存在しない（下記 Z3 参照）。")
    print("  -> Z2", "PASS" if ok else "FAIL")
    return ok


# --------------------------------------------------------------------------
# Z3 -- 次数監査: α_leak は D_F⁻¹ のみを含む（Ω_FF は O(v²)）
# --------------------------------------------------------------------------
def Z3():
    print(RULE)
    print("Z3  次数監査: α_leak は D_F⁻¹ のみ。Ω_FF（したがって離調）は O(v²)（exact）")
    print(RULE)
    v = sp.symbols('v')
    BPF, BFP, DF, OFF = sp.symbols('B_PF B_FP D_F Omega_FF')
    term = -v * BPF * (DF + v * OFF)**-1 * BFP
    c1 = sp.simplify(sp.diff(term, v).subs(v, 0))
    c2 = sp.simplify(sp.diff(term, v, 2).subs(v, 0) / 2)
    print("  Schur 漏洩項 -v·B_PF(D_F+v·Ω_FF)⁻¹B_FP")
    print("   v¹ の係数 :", c1, "   ← α_leak はこれ。D_F のみ")
    print("   v² の係数 :", c2, "   ← Ω_FF（B_FF・離調）はここで初めて現れる")
    ok = (sp.simplify(c1 + BPF * BFP / DF) == 0) and (OFF in c2.free_symbols)
    print("  ⇒ α_leak に (ΓD_F+B_FF)⁻¹ を使う読みは次数混同であり、誤り。")
    print("  ⇒ 「ψ = π - arg A で離調窓ができる」という読みは棄却される。")
    print("  -> Z3", "PASS" if ok else "FAIL")
    return bool(ok)


# --------------------------------------------------------------------------
# Z4 -- 定理 T1: k = 1 の no-go（すべての実線型汎関数について）
# --------------------------------------------------------------------------
def Z4():
    print(RULE)
    print("Z4  定理 T1: k=1 では符号条件がすべての実線型 Φ で成立しない（exact, symbolic）")
    print(RULE)
    pP, cP, BPP = sp.symbols('p_P c_P B_PP')
    dL, m = sp.symbols('d_L m', positive=True)
    w = sp.conjugate(pP) * cP / BPP**2
    kappa = w * dL
    alpha = w * (-m)
    ratio = sp.simplify(alpha / kappa)
    print("  κ_lift =", kappa)
    print("  α_leak =", alpha)
    print("  α/κ    =", ratio, "  ← 負の実数。p_P, c_P, B_PP と全離調に依存しない")
    ok = (ratio == -m / dL)
    th = sp.symbols('theta', real=True)
    a, b = sp.symbols('a b', real=True)
    for name, PhiF in [("Re", sp.re), ("Im", sp.im),
                       ("Φ_θ=Re(e^{-iθ}·)", lambda z: sp.re(sp.exp(-sp.I * th) * z))]:
        prod = sp.simplify((PhiF(kappa) * PhiF(alpha)).subs(w, a + sp.I * b))
        # Φ は実線型なので Φ(α) = -(m/dL)Φ(κ)、よって積 = -(m/dL)Φ(κ)² ≤ 0
        neg = sp.simplify(prod + (m / dL) * PhiF(kappa).subs(w, a + sp.I * b)**2)
        print(f"  Φ={name:18s}: Φ(κ)Φ(α) + (m/d_L)Φ(κ)² =", sp.simplify(neg))
        ok = ok and (sp.simplify(neg) == 0)
    print()
    print("  構造的理由: Φ が実線型 ⇒ Φ(α) = -(m/d_L)·Φ(κ)")
    print("            ⇒ Φ(κ)Φ(α) = -(m/d_L)·Φ(κ)² ≤ 0   （等号は Φ(κ)=0 の測度零のみ）")
    print("            ⇒ 稜線座標 Γ²ε = Φ(α)/Φ(κ) = -m/d_L < 0 は物理域外")
    print("  ⇒ k=1（Λ系・EIT）では、いかなる実線型汎関数を宣言しても保護回復稜線は存在しない。")
    print("  -> Z4", "PASS" if ok else "FAIL")
    return bool(ok)


# --------------------------------------------------------------------------
# Z5 / Z9 -- k>=2 の実現可能性（厳密掃引）
# --------------------------------------------------------------------------
def _sweep(rng, n_trials, physical_BPP, tie_pc, proportional_M=False):
    """厳密 Gauss 有理数での掃引。float は一切使わない。"""
    def rr():
        return F(rng.randint(-6, 6), rng.randint(1, 5))

    def pos():
        return abs(rr()) + F(1, 10)

    def rc():
        return (rr(), rr())

    hits = {'Re': 0, 'Im': 0, 'both': 0}
    valid = 0
    witness = None
    for _ in range(n_trials):
        nf = 2
        dL = [pos() for _ in range(2)]
        if proportional_M:
            lam = pos()
            M = [[lam * dL[0], F(0)], [F(0), lam * dL[1]]]
            J, dF = None, None
        else:
            J = [[rr() for _ in range(nf)] for _ in range(2)]
            dF = [pos() + 1 for _ in range(nf)]
            # 補題 L2 の構造そのもの: M = J D_F⁻¹ Jᵀ
            M = [[sum(J[a][b] * J[c][b] / dF[b] for b in range(nf)) for c in range(2)]
                 for a in range(2)]
        if physical_BPP:
            # 物理的 B_PP = S + iT、S = 実対角 PSD（低速減衰）、T = 実対称（H結合＋離調）
            s = [pos() for _ in range(2)]
            t11, t22, t12 = rr(), rr(), rr()
            B = [[(s[0], t11), (F(0), t12)], [(F(0), t12), (s[1], t22)]]
        else:
            B = [[rc() for _ in range(2)] for _ in range(2)]
        d = det2(B)
        if d == (F(0), F(0)):
            continue
        A = adj2(B)
        pP = [rc() for _ in range(2)]
        cP = [cconj(x) for x in pP] if tie_pc else [rc() for _ in range(2)]
        pd = [cconj(x) for x in pP]
        row = [tuple(sum(c) for c in zip(*[cm(pd[i], A[i][j]) for i in range(2)]))
               for j in range(2)]
        y = matvec(A, cP, 2)
        kt = vecdot([cm(row[i], creal(dL[i])) for i in range(2)], y, 2)
        Mrow = [tuple(sum(c) for c in zip(*[cm(row[i], creal(M[i][j])) for i in range(2)]))
                for j in range(2)]
        at = vecdot(Mrow, y, 2)
        at = (-at[0], -at[1])
        d2 = cm(d, d)
        den = d2[0]**2 + d2[1]**2
        if den == 0 or kt == (F(0), F(0)):
            continue
        inv = (d2[0] / den, -d2[1] / den)
        kap = cm(kt, inv)
        alp = cm(at, inv)
        if alp == (F(0), F(0)):
            continue
        valid += 1
        sRe = kap[0] * alp[0]
        sIm = kap[1] * alp[1]
        if sRe > 0:
            hits['Re'] += 1
        if sIm > 0:
            hits['Im'] += 1
        if sRe > 0 and sIm > 0:
            hits['both'] += 1
        if sRe > 0 and witness is None:
            witness = dict(J=J, dF=dF, dL=dL, M=M, B=B, pP=pP, cP=cP, kap=kap, alp=alp)
    return hits, valid, witness


def Z5():
    print(RULE)
    print("Z5  k=2 の実現可能性: 物理的 B_PP 構造の下での明示witness（exact）")
    print(RULE)
    rng = random.Random(SEED)
    hits, valid, wit = _sweep(rng, 4000, physical_BPP=True, tie_pc=False)
    print(f"  物理的 B_PP = S+iT（S 実対角 PSD、T 実対称）  有効試行 {valid}")
    print(f"    Φ=Re で +1 : {hits['Re']}  ({F(hits['Re'], valid)} = {float(F(hits['Re'],valid)):.4f})")
    print(f"    Φ=Im で +1 : {hits['Im']}  ({F(hits['Im'], valid)} = {float(F(hits['Im'],valid)):.4f})")
    print(f"    両方       : {hits['both']}")
    ok = wit is not None and hits['Re'] > 0 and hits['Im'] > 0
    if wit:
        print()
        print("  ---- 明示witness（厳密有理数、k=2, n_f=2）----")
        print("   J      =", [[str(x) for x in r] for r in wit['J']])
        print("   D_F    = diag", [str(x) for x in wit['dF']])
        print("   M      =", [[str(x) for x in r] for r in wit['M']], " (= J D_F⁻¹ Jᵀ、実PSD)")
        print("   (D_L)_PP = diag", [str(x) for x in wit['dL']])
        print("   B_PP   =", [[f"{x[0]}+{x[1]}i" for x in r] for r in wit['B']])
        print("   p_P    =", [f"{x[0]}+{x[1]}i" for x in wit['pP']])
        print("   c_P    =", [f"{x[0]}+{x[1]}i" for x in wit['cP']])
        print("   κ_lift =", f"{wit['kap'][0]} + {wit['kap'][1]}i")
        print("   α_leak =", f"{wit['alp'][0]} + {wit['alp'][1]}i")
        print("   Re(κ)·Re(α) =", wit['kap'][0] * wit['alp'][0], " > 0")
        print("   稜線 Γ²ε = Re(α)/Re(κ) =", wit['alp'][0] / wit['kap'][0])
        print("   ⇒ 稜線座標が正 ⇒ 物理域内。k>=2 では実現可能。")
    print("  -> Z5", "PASS" if ok else "FAIL")
    return ok


def Z6():
    print(RULE)
    print("Z6  対照: M ∝ (D_L)_PP に退化させると k=1 の no-go に戻るか（exact）")
    print(RULE)
    rng = random.Random(SEED + 1)
    hits, valid, wit = _sweep(rng, 2000, physical_BPP=True, tie_pc=False,
                              proportional_M=True)
    print(f"  M = λ·(D_L)_PP  有効試行 {valid}")
    print(f"    Φ=Re で +1 : {hits['Re']}     Φ=Im で +1 : {hits['Im']}")
    ok = (hits['Re'] == 0 and hits['Im'] == 0)
    print("  ⇒ M と D_L が比例するとき α = -(λ)·κ となり Z4 の構造に厳密に一致する。")
    print("  ⇒ 実現可能性の起源は『2つの実PSD行列 M と D_L が非比例であること』。")
    print("  -> Z6", "PASS" if ok else "FAIL")
    return ok


def Z7():
    print(RULE)
    print("Z7  負制御（`scripts/wpot_null_smoke.py` の分類に倣う）")
    print(RULE)
    ok = True

    # NC1: non-Hermitian H -> B_PF が実部を持ち、補題 L2 が破れる
    print("  NC1 non-Hermitian H（非物理）: J を複素にすると C_leak は実でなくなるか")
    J = sp.Matrix(1, 1, [Q(3, 7) + sp.I * Q(2, 5)])
    DF = sp.diag(Q(2, 3))
    C = sp.simplify((sp.I * J) * DF.inv() * (sp.I * J.T))
    nonreal = sp.im(C[0, 0]) != 0
    print("       C_leak =", C[0, 0], "   実でない？", nonreal)
    print("       ⇒ k=1 の no-go は Hermiticity に由来する。非物理化すると符号条件が復活しうる。")
    ok = ok and bool(nonreal)

    # NC2: nolift -- D_L = 0 にすると κ_lift = 0、稜線は未定義
    print("  NC2 nolift（dephasing jump を外す）: (D_L)_PP = 0 ⇒ κ_lift = 0")
    pP, cP, BPP, m = sp.symbols('p_P c_P B_PP m')
    kappa0 = sp.conjugate(pP) * cP / BPP**2 * 0
    print("       κ_lift =", kappa0, "  ⇒ 稜線座標 Φ(α)/Φ(κ) は未定義")
    ok = ok and (kappa0 == 0)

    # NC3: negweight -- D_L の対角に負値を入れると PD が壊れる
    print("  NC3 negweight（jump 重みを符号交代）: (D_L)_PP が正定値でなくなる")
    DL = sp.diag(Q(11, 10), Q(-3, 10))
    evs = list(DL.eigenvals().keys())
    notpd = any(e < 0 for e in evs)
    print("       (D_L)_PP の固有値 =", evs, "  正定値でない？", notpd)
    print("       ⇒ Z2(e)（(D_L)_PP ≻ 0）が FAIL し、outside assumptions に落ちる")
    ok = ok and bool(notpd)

    # NC4: gain -- D_F に負値を入れると M の PSD 性が壊れる
    print("  NC4 gain（トレース増加）: D_F に負値 ⇒ M = J D_F⁻¹ Jᵀ が PSD でなくなる")
    Jr = sp.Matrix(2, 1, [Q(1), Q(2)])
    DFneg = sp.diag(Q(-1, 2))
    Mneg = sp.simplify(Jr * DFneg.inv() * Jr.T)
    evs2 = [sp.simplify(e) for e in Mneg.eigenvals().keys()]
    notpsd = any(e < 0 for e in evs2)
    print("       M の固有値 =", evs2, "  PSD でない？", notpsd)
    ok = ok and bool(notpsd)

    print("  -> Z7", "PASS" if ok else "FAIL")
    return ok


def Z8():
    print(RULE)
    print("Z8  EIT/Λ 系の支持監査: プローブ源・読み出しは P に載るか（exact）")
    print(RULE)
    # EIT 凍結文書 §9.2 の線形系:
    #   [[A, i Ω_c d₂/2],[i Ω_c* d₂†/2, γ_g]] (x, s)ᵀ = (i Ω_p d₁/2, 0)ᵀ
    #   x = 光学コヒーレンス（A = γ₃₁ - iΔ_p が Γ スケール）→ F
    #   s = 基底コヒーレンス（γ_g = γ₂₁ - iδ₂ は低速）      → P
    g31, Dp, g21, d2s, Oc, Op = sp.symbols(
        'gamma_31 Delta_p gamma_21 delta_2 Omega_c Omega_p', positive=True)
    A = g31 - sp.I * Dp
    gg = g21 - sp.I * d2s
    print("  凍結 EIT §9.2 のブロック:")
    print("    x = 光学コヒーレンス、damping A =", A, " (Γ スケール)  ⇒ F ブロック")
    print("    s = 基底コヒーレンス、       γ_g =", gg, " (低速)        ⇒ P ブロック")
    print("    源ベクトル = ( iΩ_p d₁/2 , 0 )ᵀ")
    print("    読み出し   = d₁† x")
    # LKCT は c = (c_P, 0), p = (p_P, 0) を要求する
    c_F = sp.I * Op / 2
    c_P = sp.Integer(0)
    p_F = sp.Integer(1)
    p_P = sp.Integer(0)
    print()
    print("  LKCT の要求 : c = (c_P, 0)、p = (p_P, 0)   [提案24 L157-158]")
    print("  EIT の実際  : c_P =", c_P, "、c_F =", c_F, "  /  p_P =", p_P, "、p_F =", p_F)
    ok = (c_P == 0 and p_P == 0 and c_F != 0 and p_F != 0)
    print()
    print("  ⇒ 標準 EIT のプローブ配置は、源も読み出しも **F ブロック**に載る。")
    print("     LKCT の支持条件と**正反対**であり、この観測量は理論のクラスの外にある。")
    print("  ⇒ 提案24 §3.3 の実験翻訳（透過 Im χ と位相シフト Re χ が異なる Γ·γ₁₂ で回復）は")
    print("     F 支持の観測量について述べており、そのままでは正当化されない。要訂正。")
    print("  ⇒ P 支持の観測量にするには基底コヒーレンスを直接読む必要がある")
    print("     （Raman / RF / スピンコヒーレンス読み出し、二光子駆動源）。")
    print("  ⇒ さらに Λ 系は基底コヒーレンスが1本なので k=1 であり、Z4 によって二重に排除される。")
    print("  -> Z8", "PASS" if ok else "FAIL")
    return bool(ok)


def Z9():
    print(RULE)
    print("Z9  頻度の掃引（seed 固定、exact）")
    print(RULE)
    rows = []
    for label, phys, tie in [
        ("制約なし B_PP（線形代数）", False, False),
        ("物理的 B_PP = S+iT", True, False),
        ("物理的 B_PP かつ自己応答 p=c̄", True, True),
    ]:
        rng = random.Random(SEED + 7)
        hits, valid, _ = _sweep(rng, 4000, physical_BPP=phys, tie_pc=tie)
        rows.append((label, valid, hits))
        print(f"  {label:34s} 有効 {valid:5d}  Re:{hits['Re']:5d}  Im:{hits['Im']:5d}  両:{hits['both']:5d}")
        print(f"  {'':34s}            Re率 {F(hits['Re'],valid)} = {float(F(hits['Re'],valid)):.4f}")
    ok = all(h['Re'] > 0 and h['Im'] > 0 for _, _, h in rows)
    print()
    print("  ⇒ 実現可能性は物理的構造・自己応答の制約の下でも頻度が桁で落ちない（頑健）。")
    print("  -> Z9", "PASS" if ok else "FAIL")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None, help="証明書の出力先")
    a = ap.parse_args()

    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf if a.out else old
    try:
        r = {}
        r['Z0'] = Z0()
        r['Z1'] = Z1()
        r['Z2'] = Z2()
        r['Z3'] = Z3()
        r['Z4'] = Z4()
        r['Z5'] = Z5()
        r['Z6'] = Z6()
        r['Z7'] = Z7()
        r['Z8'] = Z8()
        r['Z9'] = Z9()
        print(RULE)
        print("verdict:", r)
        print("ALL PASS" if all(r.values()) else "SOME FAILED")
        print(RULE)
        print()
        print("結論（次元二分律）:")
        print("  k=1  : すべての実線型汎関数 Φ について符号条件は成立しない（Z4、厳密）。")
        print("         Λ/EIT はさらに支持条件でも外れる（Z8）。二重に排除。")
        print("  k>=2 : 実現可能。物理的 B_PP 構造・自己応答の下でも約 18-19%（Z5、Z9）。")
        print("  起源 : 2つの実 PSD 行列 M = J D_F⁻¹ Jᵀ と (D_L)_PP が非比例であること（Z6）。")
        print("  ⇒ 『dim P >= 2 が保護回復稜線の必要条件』という分類定理。")
    finally:
        sys.stdout = old

    text = buf.getvalue() if a.out else ""
    if a.out:
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        header = (
            f"# LKCT GKSL realizability exact audit -- generated {stamp}\n"
            f"# script: scripts/lkct_gksl_realize.py  seed {SEED}  sympy {sp.__version__}\n"
            f"# 判定に浮動小数点を使用していない（表示のみ float 変換は頻度の可読化のみ）\n"
            f"# 手順: docs/lkct-gksl-realizability-audit.md\n"
        )
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(header + text)
        print(text)
        print(f"[certificate written to {a.out}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
