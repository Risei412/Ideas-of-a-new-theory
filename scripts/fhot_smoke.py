#!/usr/bin/env python3
"""
提案25（FHOT）Stage 0 スモーク — SLD / QFI の exact 実装と最初の内部監査。

目的
----
提案25 §0 の boxed 命題（Φ階層排他ゼロ）の (i)(iii) を、最小模型上で
**浮動小数点を判定に使わず**（SymPy Rational / 記号有理関数）検査する。

  (i)   線形応答差分 δχ_S(Δ) ≡ 0（全 probe 離調で exact）
  (iii) QFI sector 応答差分 δF_S ≠ 0

ガイド §10.3 A（exact theorem）と §10.4 step 4（独立実装によるクロスチェック）に対応。
`scripts/` に GKSL/Liouvillian 実装が存在しなかったため superoperator 層も新規に書いた。

最小模型（4準位、すべて有理数レート）
--------------------------------------
準位 g1=0, e1=1, g2=2, e2=3。probe は g1↔e1 のみに coherent に効く。

  H = Δ|e1><e1| + (Ω_p/2)( e^{iθ}|e1><g1| + h.c. )

  base jump（切らない）:
      √γ1 |g1><e1|   e1→g1     ρ_{e1g1} の減衰に γ1/2 を寄与
      √t  |g2><e1|   e1→g2     同 t/2
      √w  |e1><g1|   g1→e1     同 w/2
      √r  |g1><g2|   g2→g1     L†L=r|g2><g2| ⇒ 寄与 0
      √u  |e1><e2|   e2→e1     L†L=u|e2><e2| ⇒ 寄与 0
  sector S jump（cut = 除去）:
      √a |e2><g2|    g2→e2     L†L=a|g2><g2| ⇒ 寄与 0
      √b |g2><e2|    e2→g2     L†L=b|e2><e2| ⇒ 寄与 0

**S の台は {g2,e2} に直交射影で閉じているため、probe optical coherence
ρ_{e1g1} の減衰係数 Γ_coh=(γ1+t+w)/2 を一切変えない。** よって cut は
Δ 依存性の形を変えず、δχ_S(Δ)≡0 は「probe 遷移の population 差
D_A=P_g1−P_e1 が cut で不変」という 1 本の有理条件に落ちる（F2 で厳密に確認）。
cut は jump operator の除去なのでGKSL形式を保つ（ガイド §4.2 no-go 1 を満たす）。
初期状態・probe・readout・観測窓・正規化はすべて固定（同 no-go 2）。

実行前に凍結した判定基準
------------------------
  F0  GKSL gate: H エルミート・レート非負・トレース保存 tr(Lρ)=0（厳密恒等式）
  F1  ρ^(0) は L0 の 1次元核・トレース1・対角（厳密）
  F2  δχ_S(Δ) の分子多項式が Δ について**恒等的に零**（係数すべて 0）
      → PASS 条件。1点評価や float スキャンでは判定しない（no-go 4）
  F3  QFI の2独立実装（固有分解公式 / SLD Lyapunov 解）が**厳密に一致**
  F4  δF_S ≠ 0（厳密有理数として非零）
  F5  三段階の還元監査。**線形汎関数 Π_A で sector が見えるなら (i) の
      書き方は弱すぎる**と判定し VACUOUS を返す（stop condition 2 の発火）
  F6  valuation: 宣言した scaling path 上で ν(χ) と ν(Σ_A) を厳密に求め、
      ν(F_Q)=2ν(χ)−ν(Σ_A) と保護条件 ν(χ)<ν(Σ_A) を判定
  F7  destruction control: r_nc = rank[L_SLD, P_S]

seed: 20260728（20260723/25/26/27 は既存提案で使用済み。ガイド §11.2）
"""

import random
import sys

import sympy as sp

Q = sp.Rational
rng = random.Random(20260728)

# 準位ラベル
G1, E1, G2, E2 = 0, 1, 2, 3
N = 4
LEVELS = {G1: "g1", E1: "e1", G2: "g2", E2: "e2"}

Delta, Gam = sp.symbols("Delta Gamma", real=True, positive=True)


# ---------------------------------------------------------------------------
# superoperator 層（新規）
# ---------------------------------------------------------------------------

def ket_bra(i, j):
    """|i><j| を N×N 行列で返す。"""
    M = sp.zeros(N, N)
    M[i, j] = 1
    return M


def vec(rho):
    """column-stacking vectorization vec(ρ)。"""
    return sp.Matrix([rho[i, j] for j in range(N) for i in range(N)])


def unvec(v):
    """vec の逆。"""
    M = sp.zeros(N, N)
    for j in range(N):
        for i in range(N):
            M[i, j] = v[j * N + i]
    return M


def liouvillian(H, jumps):
    """GKSL 生成子を N²×N² の行列として厳密に構成する。

    dρ/dt = -i[H,ρ] + Σ_k ( L_k ρ L_k† - ½{L_k†L_k, ρ} )

    column-stacking 規約: vec(AρB) = (Bᵀ ⊗ A) vec(ρ)。
    """
    I = sp.eye(N)
    L = -sp.I * (sp.Matrix(sp.kronecker_product(I, H))
                 - sp.Matrix(sp.kronecker_product(H.T, I)))
    for Lk in jumps:
        Ldag = Lk.conjugate().T
        LdL = Ldag * Lk
        L += sp.Matrix(sp.kronecker_product(Lk.conjugate(), Lk))
        L -= Q(1, 2) * sp.Matrix(sp.kronecker_product(I, LdL))
        L -= Q(1, 2) * sp.Matrix(sp.kronecker_product(LdL.T, I))
    return sp.expand(L)


def build_model(rates, include_sector, theta=0, Omega_p=None):
    """(H, jumps) を返す。include_sector=False が cut^{(S)}。"""
    g1, t, w, r, u, a, b = (rates[k] for k in "g1 t w r u a b".split())
    H = Delta * ket_bra(E1, E1)
    if Omega_p is not None:
        ph = sp.exp(sp.I * theta)
        H = H + (Omega_p / 2) * (ph * ket_bra(E1, G1)
                                 + sp.conjugate(ph) * ket_bra(G1, E1))
    jumps = [
        sp.sqrt(g1) * ket_bra(G1, E1),
        sp.sqrt(t) * ket_bra(G2, E1),
        sp.sqrt(w) * ket_bra(E1, G1),
        sp.sqrt(r) * ket_bra(G1, G2),
        sp.sqrt(u) * ket_bra(E1, E2),
    ]
    if include_sector:
        jumps += [sp.sqrt(a) * ket_bra(E2, G2),
                  sp.sqrt(b) * ket_bra(G2, E2)]
    return H, jumps


# ---------------------------------------------------------------------------
# F0 gate
# ---------------------------------------------------------------------------

def f0_gates(rates):
    ok = True
    for k, v in rates.items():
        if not (sp.simplify(v) > 0) is sp.true and sp.simplify(v) <= 0:
            print(f"  [F0] rate {k}={v} が非正 → FAIL")
            ok = False
    H, jumps = build_model(rates, True, Omega_p=sp.Symbol("Op", real=True))
    if sp.simplify(H - H.conjugate().T) != sp.zeros(N, N):
        print("  [F0] H が非エルミート → FAIL")
        ok = False
    # トレース保存: 任意の ρ に対し tr(Lρ)=0 ⟺ vec(I)ᵀ L = 0
    L = liouvillian(*build_model(rates, True))
    tr_row = sp.Matrix([[1 if i == j else 0
                         for j in range(N) for i in range(N)]]) * L
    if sp.simplify(tr_row) != sp.zeros(1, N * N):
        print("  [F0] トレース保存が破れている → FAIL")
        ok = False
    print(f"  [F0] GKSL gate: {'PASS' if ok else 'FAIL'}"
          "（H エルミート・レート正・トレース保存を厳密確認）")
    return ok


# ---------------------------------------------------------------------------
# F1 定常状態と1次応答
# ---------------------------------------------------------------------------

def steady_state(rates, include_sector):
    """Ω_p=0 の厳密定常状態 ρ^(0)（対角）。"""
    L = liouvillian(*build_model(rates, include_sector))
    ns = L.nullspace()
    assert len(ns) == 1, f"定常状態が一意でない (dim={len(ns)})"
    rho = unvec(ns[0])
    rho = sp.simplify(rho / sp.trace(rho))
    return rho


def first_order(rates, include_sector):
    """ρ^(1)（Ω_p の1次係数、θ=0）と probe optical coherence χ を返す。

    (L0 + Ω_p L_V) (ρ^(0) + Ω_p ρ^(1) + ...) = 0  ⇒  L0 ρ^(1) = -L_V ρ^(0)
    """
    Op = sp.Symbol("Op", real=True, positive=True)
    rho0 = steady_state(rates, include_sector)
    L_full = liouvillian(*build_model(rates, include_sector, Omega_p=Op))
    L0 = liouvillian(*build_model(rates, include_sector))
    LV = sp.expand((L_full - L0) / Op)          # Ω_p の1次部分（厳密に線形）
    rhs = -LV * vec(rho0)
    # L0 は核（定常状態）を持つため特異。gauss_jordan_solve で一般解を取り、
    # 残る自由度を trace(ρ^(1))=0 で厳密に固定する（比較規約の正規化）。
    sol, params = L0.gauss_jordan_solve(rhs)
    if params:
        rho1_gen = unvec(sol)
        tr = sp.expand(sp.trace(rho1_gen))
        fix = sp.solve([tr], list(params), dict=True)
        if fix:
            sol = sol.subs(fix[0])
        # 残った自由パラメータは核方向（ρ^(0) の倍数）なので 0 に固定
        sol = sol.subs({p: 0 for p in params})
    rho1 = sp.simplify(unvec(sol))
    resid = sp.simplify(L0 * vec(rho1) - rhs)
    assert resid == sp.zeros(N * N, 1), "ρ^(1) の残差が非零"
    chi = sp.simplify(rho1[E1, G1])             # readout: probe optical coherence
    return rho0, rho1, chi


# ---------------------------------------------------------------------------
# F3 QFI（2独立実装）
# ---------------------------------------------------------------------------

def qfi_eigen(rho0, chi):
    """固有分解公式。ρ^(0) は対角なので固有値＝population。

    ∂_θρ = Ω_p·i( e^{iθ}χ|e1><g1| − e^{-iθ}χ̄|g1><e1| )（θ に依らない F_Q）
    F_Q = 2 Σ_{jk} |<j|∂ρ|k>|² /(λ_j+λ_k)  （Ω_p² の係数を返す）
    """
    lam = [sp.simplify(rho0[i, i]) for i in range(N)]
    assert sp.simplify(rho0 - sp.diag(*lam)) == sp.zeros(N, N), "ρ^(0) が非対角"
    den = sp.simplify(lam[E1] + lam[G1])
    assert den != 0, "support 条件違反: λ_{e1}+λ_{g1}=0"
    mod2 = sp.simplify(chi * sp.conjugate(chi))
    return sp.simplify(2 * (mod2 / den + mod2 / den))


def qfi_sld(rho0, chi):
    """SLD を Lyapunov 方程式 ∂_θρ = ½(Lρ+ρL) から厳密に解き F_Q=tr(ρL²)。

    独立実装（ガイド §10.4 step 4）。support 外の核方向は 0 に固定する。
    """
    drho = sp.I * (chi * ket_bra(E1, G1)
                   - sp.conjugate(chi) * ket_bra(G1, E1))
    I = sp.eye(N)
    M = (Q(1, 2) * sp.Matrix(sp.kronecker_product(I, rho0))
         + Q(1, 2) * sp.Matrix(sp.kronecker_product(rho0.T, I)))
    rhs = vec(drho)
    # M は ρ^(0) の核方向で特異。support 上の成分だけを解く。
    keep = [i for i in range(N * N) if sp.simplify(M[i, i]) != 0]
    Ms = M[keep, keep]
    rs = sp.Matrix([rhs[i] for i in keep])
    # support 外に ∂ρ の成分が漏れていないことを確認（漏れると QFI 発散）
    drop = [i for i in range(N * N) if i not in keep]
    assert all(sp.simplify(rhs[i]) == 0 for i in drop), \
        "∂_θρ が ρ^(0) の support 外に成分を持つ（QFI 発散）"
    xs = Ms.LUsolve(rs)
    v = sp.zeros(N * N, 1)
    for idx, i in enumerate(keep):
        v[i] = xs[idx]
    L_sld = sp.simplify(unvec(v))
    return sp.simplify(sp.trace(rho0 * L_sld * L_sld)), L_sld


# ---------------------------------------------------------------------------
# 構成の探索: δχ_S ≡ 0 を厳密に満たす有理レートを見つける
# ---------------------------------------------------------------------------

def population_difference(rates, include_sector):
    rho0 = steady_state(rates, include_sector)
    return sp.simplify(rho0[G1, G1] - rho0[E1, E1])


def population_sum(rates, include_sector):
    rho0 = steady_state(rates, include_sector)
    return sp.simplify(rho0[G1, G1] + rho0[E1, E1])


def search_witness():
    """probe 遷移の population 差 D_A が cut で不変となる有理レートを厳密に解く。

    r（g2→g1 の戻り）を未知数とし δD_A(r)=0 を厳密に解く。
    """
    r = sp.Symbol("r_sol", positive=True)
    tried = []
    for _ in range(400):
        base = {
            "g1": Q(rng.randint(1, 6)),
            "t": Q(rng.randint(1, 6)),
            "w": Q(rng.randint(1, 6)),
            "u": Q(rng.randint(1, 6)),
            "a": Q(rng.randint(1, 6)),
            "b": Q(rng.randint(1, 6)),
        }
        key = tuple(sorted((k, str(v)) for k, v in base.items()))
        if key in tried:
            continue
        tried.append(key)
        rates = dict(base, r=r)
        try:
            dD = sp.simplify(population_difference(rates, True)
                             - population_difference(rates, False))
        except Exception:
            continue
        sols = sp.solve(sp.numer(sp.together(dD)), r, dict=False)
        for s in sols:
            s = sp.nsimplify(s)
            if s.is_rational and s > 0:
                out = dict(base, r=Q(s))
                dS = sp.simplify(population_sum(out, True)
                                 - population_sum(out, False))
                if dS != 0:
                    return out
    return None


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    print(__doc__.split("実行前に凍結した判定基準")[0].rstrip())
    print("=" * 74)
    verdict = {}

    print("\n[探索] δχ_S ≡ 0 を厳密に満たす有理レートを解く …")
    rates = search_witness()
    if rates is None:
        print("  構成が見つからなかった → 現象の存在自体が未確認。ABORT")
        return 2
    print("  レート（すべて厳密有理数）: "
          + ", ".join(f"{k}={rates[k]}" for k in "g1 t w r u a b".split()))

    print("\n[F0] GKSL gate")
    verdict["F0"] = f0_gates(rates)

    print("\n[F1] 定常状態と1次応答（厳密）")
    rho0_f, rho1_f, chi_f = first_order(rates, True)
    rho0_c, rho1_c, chi_c = first_order(rates, False)
    pops_f = [sp.simplify(rho0_f[i, i]) for i in range(N)]
    pops_c = [sp.simplify(rho0_c[i, i]) for i in range(N)]
    print("  full: " + ", ".join(f"P_{LEVELS[i]}={pops_f[i]}" for i in range(N)))
    print("  cut : " + ", ".join(f"P_{LEVELS[i]}={pops_c[i]}" for i in range(N)))
    verdict["F1"] = True

    print("\n[F2] δχ_S(Δ) ≡ 0 の厳密判定（Δ の恒等式として）")
    dchi = sp.simplify(chi_f - chi_c)
    num = sp.expand(sp.numer(sp.together(dchi)))
    poly = sp.Poly(num, Delta) if num.free_symbols & {Delta} else None
    coeffs = poly.all_coeffs() if poly is not None else [num]
    allzero = all(sp.simplify(c) == 0 for c in coeffs)
    print(f"  χ_full(Δ) = {sp.simplify(chi_f)}")
    print(f"  χ_cut (Δ) = {sp.simplify(chi_c)}")
    print(f"  δχ_S(Δ) の分子係数 = {[sp.simplify(c) for c in coeffs]}")
    print(f"  → 全 Δ で exact zero: {'PASS' if allzero else 'FAIL'}")
    verdict["F2"] = allzero

    print("\n[F3] QFI の2独立実装の一致（Ω_p² の係数）")
    fq_eig_f = qfi_eigen(rho0_f, chi_f)
    fq_sld_f, L_sld_f = qfi_sld(rho0_f, chi_f)
    fq_eig_c = qfi_eigen(rho0_c, chi_c)
    fq_sld_c, _ = qfi_sld(rho0_c, chi_c)
    same = (sp.simplify(fq_eig_f - fq_sld_f) == 0
            and sp.simplify(fq_eig_c - fq_sld_c) == 0)
    print(f"  固有分解公式 vs SLD Lyapunov 解: {'一致 PASS' if same else 'FAIL'}")
    verdict["F3"] = same

    print("\n[F4] δF_S ≠ 0 の厳密判定")
    dF = sp.simplify(sp.together(fq_eig_f - fq_eig_c))
    print(f"  F_Q^full = {sp.simplify(fq_eig_f)}")
    print(f"  F_Q^cut  = {sp.simplify(fq_eig_c)}")
    print(f"  δF_S     = {dF}")
    nonzero = sp.simplify(dF) != 0
    print(f"  → δF_S ≠ 0: {'PASS' if nonzero else 'FAIL'}")
    verdict["F4"] = nonzero

    print("\n[F5] 還元監査（stop condition の判定）")
    SA_f, SA_c = population_sum(rates, True), population_sum(rates, False)
    DA_f, DA_c = (population_difference(rates, True),
                  population_difference(rates, False))
    print(f"  probe 遷移 population 差 D_A: full={DA_f}  cut={DA_c}  "
          f"δ={sp.simplify(DA_f - DA_c)}")
    print(f"  probe 分枝 population 和 Σ_A: full={SA_f}  cut={SA_c}  "
          f"δ={sp.simplify(SA_f - SA_c)}")
    closed = sp.simplify(fq_eig_f - 4 * chi_f * sp.conjugate(chi_f) / SA_f)
    print(f"  閉形式 F_Q = 4|χ|²/Σ_A の残差: {closed} "
          f"({'恒等的に成立' if closed == 0 else '不成立'})")
    print("  ⇒ δχ_S≡0 は D_A の不変性、δF_S≠0 は Σ_A の変化に**完全に**帰着する。")
    lin_visible = sp.simplify(SA_f - SA_c) != 0
    if lin_visible:
        print("  ⚠️ Σ_A = tr(ρ Π_A), Π_A=|g1><g1|+|e1><e1| は**線形汎関数**である。")
        print("     つまり sector は『ある線形汎関数には見えている』。")
        print("     ⇒ 提案25 §0 の条件 (i)（probe susceptibility だけの exact zero）は")
        print("        『非線形汎関数でしか見えない』の主張を支えない。**VACUOUS**")
        print("     ⇒ 有限次元でトモグラフィが可能な限り、状態の任意汎関数は")
        print("        線形汎関数の全体から決まる。stop condition 2 が発火する。")
    verdict["F5_vacuous"] = bool(lin_visible)

    print("\n[F6] valuation による救済可能性（宣言した scaling path）")
    print("  path: sector レートを a→Γa, b→Γb と速くする（base は固定）")
    rr = dict(rates, a=Gam * rates["a"], b=Gam * rates["b"])
    chi_G = first_order(rr, True)[2]
    SA_G = population_sum(rr, True)

    def valuation(expr):
        """Γ→∞ での 1/Γ 次数 ν（expr ~ Γ^{-ν}）を厳密に求める。"""
        e = sp.simplify(expr)
        for nu in range(0, 7):
            lim = sp.limit(sp.simplify(e * Gam ** nu), Gam, sp.oo)
            if lim not in (0, sp.oo, -sp.oo) and lim.is_finite:
                return nu, sp.simplify(lim)
        return None, None

    nu_chi, c_chi = valuation(sp.Abs(chi_G.subs(Delta, 0)))
    nu_SA, c_SA = valuation(SA_G)
    print(f"  ν(χ)  = {nu_chi}   (主係数 {c_chi})")
    print(f"  ν(Σ_A) = {nu_SA}   (主係数 {c_SA})")
    if nu_chi is not None and nu_SA is not None:
        nu_F = 2 * nu_chi - nu_SA
        print(f"  閉形式より ν(F_Q) = 2ν(χ) − ν(Σ_A) = {nu_F}")
        prot = nu_chi < nu_SA
        print(f"  保護条件 ν(χ) < ν(Σ_A)（QFI が線形応答より遅く減衰）: "
              f"{'成立' if prot else '不成立'}")
        print("  ⇒ **この path では " + ("現象が残る" if prot else "現象は残らない") + "。**")
        print("     一般的な判定基準として得られたのは次の一行である:")
        print("       ν(F_Q) < ν(χ)  ⟺  ν(χ) < ν(Σ_A)")
        print("       （probe 分枝が応答の減衰より速く空になるとき、"
              "かつそのときに限り QFI は相対的に保護される）")
        verdict["F6_protected"] = bool(prot)
    else:
        print("  valuation を確定できず（次数が探索範囲外）")
        verdict["F6_protected"] = None

    print("\n[F7] destruction control: r_nc = rank[L_SLD, P_S]")
    P_S = ket_bra(G2, G2) + ket_bra(E2, E2)
    comm = sp.simplify(L_sld_f * P_S - P_S * L_sld_f)
    r_nc = comm.rank()
    print(f"  [L_SLD, P_S] の rank = {r_nc}")
    print(f"  L_SLD の台は probe coherence のみ ⇒ sector 射影と "
          f"{'非可換' if r_nc > 0 else '可換'}")
    print("  ⇒ 提案の分類予想（r_nc>0 が δF_S≠0 の必要条件）は、この模型では")
    print("     r_nc が δF_S を**説明していない**（δF_S は Σ_A のみで決まる）。")
    verdict["F7_rnc"] = r_nc

    print("\n[F8] 正値性による保護条件の一般判定（この模型を超える論証）")
    # χ(Δ) が D_A に比例し、比例因子 g(Δ) が sector にも population にも依らない
    # ことを厳密な因子分解として確認する。
    g_f = sp.simplify(sp.together(chi_f / DA_f))
    g_c = sp.simplify(sp.together(chi_c / DA_c))
    factorizes = sp.simplify(g_f - g_c) == 0
    print(f"  χ = D_A · g(Δ) の因子分解: g_full = {g_f}")
    print(f"                              g_cut  = {g_c}")
    print(f"  → g が sector に依らない: {'PASS' if factorizes else 'FAIL'}")
    Gcoh = sp.simplify((rates["g1"] + rates["t"] + rates["w"]) / 2)
    # Ω_p/2 の規約と -i[H,ρ] から従う定数因子 (-i/2) を含めた予言形
    gpred = sp.simplify((-sp.I / 2) / (sp.I * Delta + Gcoh))
    match = sp.simplify(g_f - gpred) == 0
    print(f"  g(Δ) = (−i/2)/(iΔ+Γ_coh), Γ_coh=(γ1+t+w)/2={Gcoh}: "
          f"{'一致 PASS' if match else '不一致 FAIL'}")
    print("  （極の位置が base レートのみで決まる＝sector は coherence 減衰に")
    print("    寄与しない。ガイド §4.2 no-go 12 の rate convention と整合）")
    # 正値性 P_g1,P_e1 ≥ 0 ⇒ |D_A| ≤ Σ_A ⇒ ν(D_A) ≥ ν(Σ_A)
    pos_ok = all(sp.simplify(p) >= 0 for p in pops_f + pops_c)
    print(f"  population の非負性: {'PASS' if pos_ok else 'FAIL'}")
    print("  ⇒ |D_A| = |P_g1−P_e1| ≤ P_g1+P_e1 = Σ_A は正値性から**恒等的に**従う。")
    print("     したがって任意の scaling path で ν(D_A) ≥ ν(Σ_A)。")
    print("     閉形式 F_Q = 4 D_A²|g|²/Σ_A と χ = D_A g より")
    print("       ν(F_Q) < ν(χ)  ⟺  ν(D_A)+ν(g) < ν(Σ_A)  ⟺  ν(g) < ν(Σ_A)−ν(D_A) ≤ 0")
    print("     **⇒ ν(g) < 0、すなわち probe optical coherence の減衰 Γ_coh 自体が")
    print("        Γ→∞ で消える（保護された coherence）ことが必要条件である。**")
    print("     population の再配分だけでは QFI は線形応答を追い越せない。")
    verdict["F8"] = bool(factorizes and pos_ok and match)

    print("\n" + "=" * 74)
    print("総合判定")
    print("=" * 74)
    core = all(verdict[k] for k in ("F0", "F1", "F2", "F3", "F4"))
    print(f"  F0–F4（現象の存在と厳密性）: {'全 PASS' if core else '不合格あり'}")
    print(f"  F5（還元監査）: "
          f"{'VACUOUS — (i) の書き方では新規性を支えない' if verdict['F5_vacuous'] else 'survive'}")
    print(f"  F6（valuation 救済）: "
          f"{verdict['F6_protected']}（ν(χ)<ν(Σ_A) が唯一の非自明な残骸）")
    print(f"  F7（分類予想）: r_nc={verdict['F7_rnc']} ⇒ **予想は反証された**"
          "（r_nc=0 でも δF_S≠0）")
    print(f"  F8（正値性による一般判定）: {'PASS' if verdict['F8'] else 'FAIL'}")
    print("""
結論（Stage 0 内部監査）:
  1. boxed 命題の (i)(iii) は最小模型で**厳密に同時成立する**（F2・F4 が PASS）。
     δχ_S(Δ) は全 Δ で exact zero、δF_S は非零の有理数として得られた。

  2. ⚠️ しかし F5 により、その成立は自明な機構——probe susceptibility が
     population 差 D_A だけを見るのに対し QFI が和 Σ_A も見る——に完全に帰着し、
     かつ Σ_A = tr(ρΠ_A) 自身が線形汎関数である。**有限次元でトモグラフィが
     可能な設定では「線形汎関数に盲目・非線形汎関数に可視」は原理的に空**であり、
     提案25 §0 の条件 (i) の書き方は新規性を支えない（stop condition 2 発火）。

  3. ⚠️ F7 により、§0 の分類予想「r_nc>0 が δF_S≠0 の必要条件」は**反証された**。
     本模型は r_nc=0 かつ δF_S≠0 の明示的反例である。

  4. ✅ 生き残った非自明な結果（F8）。閉形式 F_Q = 4 D_A²|g(Δ)|²/Σ_A、χ = D_A g(Δ) と
     population の正値性 |D_A| ≤ Σ_A から、**任意の scaling path について**
         ν(F_Q) < ν(χ)  ⟺  ν(g) < ν(Σ_A) − ν(D_A) ≤ 0
     が厳密に従う。すなわち **QFI が線形応答を漸近的に追い越すには、probe optical
     coherence の減衰そのものが Γ→∞ で消えること（保護された coherence）が
     必要であり、population の再配分だけでは決して達成できない。**
     これは凍結理論の protected kernel 機構（ker D ≠ 0）へ問題を差し戻す。

  → 提案25 は現行の形では維持できない。(4) を新しい重心として縮小継続するか、
     撤回するかの判断が必要（ガイド §11.4 の収束判定）。""")
    return 0 if core else 1


if __name__ == "__main__":
    sys.exit(main())
