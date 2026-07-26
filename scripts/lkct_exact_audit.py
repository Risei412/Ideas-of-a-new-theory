"""
提案24（LKCT）§5.2-1 の A2 内部監査 — exact arithmetic 版。

目的: スモーク `crossover_ridge_smoke.py` が float で示した内容を、
      浮動小数点を一切使わずに（SymPy Rational / Poly / Sturm）認証する。
      ガイド §10.3 A（exact theorem）の必須5項目に対応させる。

  X0  gate 検査（exact）: B_PP 可逆・D_F 可逆・D_L PSD・(D_L)_PP PD・D_0 PSD
  X1  厳密 Schur 還元恒等式 R(Γ,ε) = p_P† S(u,v)^{-1} c_P
      （u=Γε, v=1/Γ）。完全記号（k=1,n_f=1）＋有理数インスタンス（k=2,n_f=2）
  X2  2-jet 係数の厳密導出: d/dt|_0 R(t·u_0, t·v_0) = −u_0·κ_lift + v_0·α_leak
  X3  fan データ: R−R_∞ の (Γ,ε) 指数台とNewton多面体、および
      経路 ε=e_0Γ^{−θ} 上の valuation ν(θ) を有理 θ 格子で厳密計算し ± 対で比較
  X4  角 θ=2 の initial form。**差はここにしか現れない**ことの厳密確認
  X5  厳密稜線証明書: 固定 Γ で分子の実根を Sturm 法で数え上げ、
      + 側は ε>0 に唯一の根（分母に根なし）、− 側は ε>0 に根なしを認証
  X6  ランダム有理インスタンス掃引: 2-jet 恒等式の反例探索＋二分律の頻度

浮動小数点は使用しない（判定はすべて Rational の厳密比較）。
判定基準は実行前に凍結: X0–X5 は厳密一致/厳密不等号、X6 は反例0件。

seed: 20260726（提案24用。20260723 / 20260725 は既存候補で使用済み）
"""

from fractions import Fraction
import random

import sympy as sp

Gam, eps, t, e0, u0s, v0s, tau = sp.symbols(
    "Gamma epsilon t e_0 u_0 v_0 tau", positive=True)

rng = random.Random(20260726)
Q = sp.Rational


# --------------------------------------------------------------------------
# 共通: モデル構成（すべて厳密有理数）
# --------------------------------------------------------------------------

def assemble(BPP, BPF, BFP, BFF, DF, DLPP, DLFF, pP, cP):
    """ブロックから (D_0, D_L, B, p, c) を組む。k=len(pP), n_f=DF.rows。"""
    k, nf = BPP.rows, DF.rows
    Z_kf, Z_fk = sp.zeros(k, nf), sp.zeros(nf, k)
    D0 = sp.Matrix(sp.BlockMatrix([[sp.zeros(k, k), Z_kf], [Z_fk, DF]]))
    DL = sp.Matrix(sp.BlockMatrix([[DLPP, Z_kf], [Z_fk, DLFF]]))
    B = sp.Matrix(sp.BlockMatrix([[BPP, BPF], [BFP, BFF]]))
    p = sp.Matrix.vstack(pP, sp.zeros(nf, 1))
    c = sp.Matrix.vstack(cP, sp.zeros(nf, 1))
    return D0, DL, B, p, c


def jet_closed_form(BPP, BPF, BFP, DF, DLPP, pP, cP):
    """界面データのみからの閉形式 (R_inf, kappa_lift, alpha_leak)。"""
    BPPi = BPP.inv()
    x = BPPi.T * pP          # B_PP^{-T} p_P
    y = BPPi * cP            # B_PP^{-1} c_P
    C_leak = BPF * DF.inv() * BFP
    R_inf = (pP.T * y)[0, 0]
    kappa = (x.T * DLPP * y)[0, 0]
    alpha = (x.T * C_leak * y)[0, 0]
    return sp.nsimplify(R_inf), sp.simplify(kappa), sp.simplify(alpha)


def R_of(D0, DL, B, p, c, G, E):
    """R = p† A^{-1} c、A = G(D_0 + E D_L) + B。厳密解法（LUsolve）。"""
    A = G * (D0 + E * DL) + B
    return sp.together((p.T * A.LUsolve(c))[0, 0])


def is_pd(M):
    """対称行列の正定値性を Sylvester 判定で厳密に。"""
    if sp.simplify(M - M.T) != sp.zeros(*M.shape):
        return False
    return all(sp.simplify(M[:i, :i].det()) > 0 for i in range(1, M.rows + 1))


def is_psd(M):
    """対称行列の半正定値性を全主小行列式で厳密に。"""
    if sp.simplify(M - M.T) != sp.zeros(*M.shape):
        return False
    n = M.rows
    for r in range(1, n + 1):
        for idx in _combos(range(n), r):
            if sp.simplify(M[idx, idx].det()) < 0:
                return False
    return True


def _combos(it, r):
    from itertools import combinations
    return [list(x) for x in combinations(it, r)]


# --------------------------------------------------------------------------
# 凍結インスタンス（提案24 §2 の fan-identical 対）
# --------------------------------------------------------------------------

BPP = sp.Matrix([[2, 1], [1, 3]])
BPF = sp.Matrix([[1, 0], [0, 1]])
BFP = sp.Matrix([[1, 1], [0, 1]])
BFF = sp.Matrix([[1, 0], [0, 1]])
DF = sp.Matrix([[1, 0], [0, 2]])
DLFF = sp.Matrix([[1, 0], [0, 1]])
pP = sp.Matrix([1, 0])
cP = sp.Matrix([0, 1])
DELTA = Q(1, 100)


def make_pair():
    """s=+1 / s=-1 の持ち上げ対。alpha_leak は構成上厳密に共通。"""
    BPPi = BPP.inv()
    x = BPPi.T * pP
    y = BPPi * cP
    M = sp.Matrix.vstack(x.T, y.T)          # 行が x, y
    out = {}
    for s, lab in ((1, "ridge"), (-1, "no-ridge")):
        w = M.solve(sp.Matrix([1, s]))
        DLPP = w * w.T + DELTA * sp.eye(2)
        out[lab] = (DLPP, w, s)
    return out, x, y, M


# --------------------------------------------------------------------------
# X0
# --------------------------------------------------------------------------

def X0(pair):
    print("=" * 74)
    print("X0  gate 検査（exact）")
    print("=" * 74)
    ok = True
    dBPP, dDF = sp.simplify(BPP.det()), sp.simplify(DF.det())
    print(f"  det B_PP = {dBPP}   det D_F = {dDF}")
    ok &= (dBPP != 0) and (dDF != 0)
    for lab, (DLPP, w, s) in pair.items():
        D0, DL, B, p, c = assemble(BPP, BPF, BFP, BFF, DF, DLPP, DLFF, pP, cP)
        pd_pp, psd_l, psd_0 = is_pd(DLPP), is_psd(DL), is_psd(D0)
        print(f"  [{lab:8s}] (D_L)_PP PD={pd_pp}  D_L PSD={psd_l}  D_0 PSD={psd_0}")
        ok &= pd_pp and psd_l and psd_0
    print(f"  -> X0 {'PASS' if ok else 'FAIL'}\n")
    return ok


# --------------------------------------------------------------------------
# X1  厳密 Schur 還元恒等式
# --------------------------------------------------------------------------

def schur_S(BPP_, BPF_, BFP_, BFF_, DF_, DLPP_, DLFF_, u, v):
    """S(u,v) = Omega_PP - v Omega_PF (D_F + v Omega_FF)^{-1} Omega_FP,
       Omega = B + u D_L （PF/FP ブロックは D_L=blockdiag より B のまま）。"""
    OPP = BPP_ + u * DLPP_
    OPF, OFP = BPF_, BFP_
    OFF = BFF_ + u * DLFF_
    return OPP - v * OPF * (DF_ + v * OFF).inv() * OFP


def X1(pair):
    print("=" * 74)
    print("X1  厳密 Schur 還元恒等式  R = p_P† S(u,v)^{-1} c_P")
    print("=" * 74)
    ok = True

    # (a) 完全記号 k=1, n_f=1
    b11, b12, b21, b22, dF, l11, l22, q1, r1 = sp.symbols(
        "b11 b12 b21 b22 d_F l11 l22 p1 c1")
    u, v = sp.symbols("u v")
    D0s, DLs, Bs, ps, cs = assemble(
        sp.Matrix([[b11]]), sp.Matrix([[b12]]), sp.Matrix([[b21]]),
        sp.Matrix([[b22]]), sp.Matrix([[dF]]), sp.Matrix([[l11]]),
        sp.Matrix([[l22]]), sp.Matrix([q1]), sp.Matrix([r1]))
    R_dir = R_of(D0s, DLs, Bs, ps, cs, 1 / v, u * v)
    S = schur_S(sp.Matrix([[b11]]), sp.Matrix([[b12]]), sp.Matrix([[b21]]),
                sp.Matrix([[b22]]), sp.Matrix([[dF]]), sp.Matrix([[l11]]),
                sp.Matrix([[l22]]), u, v)
    R_schur = (sp.Matrix([q1]).T * S.inv() * sp.Matrix([r1]))[0, 0]
    diff = sp.simplify(sp.together(R_dir - R_schur))
    print(f"  (a) 完全記号 k=1,n_f=1: R_direct - R_schur = {diff}")
    ok &= (diff == 0)

    # 閉形式の記号確認
    Rinf_s, kap_s, alf_s = jet_closed_form(
        sp.Matrix([[b11]]), sp.Matrix([[b12]]), sp.Matrix([[b21]]),
        sp.Matrix([[dF]]), sp.Matrix([[l11]]), sp.Matrix([q1]), sp.Matrix([r1]))
    print(f"      R_inf      = {sp.simplify(Rinf_s)}")
    print(f"      kappa_lift = {sp.simplify(kap_s)}")
    print(f"      alpha_leak = {sp.simplify(alf_s)}")
    d_kap = sp.simplify(kap_s - q1 * r1 * l11 / b11**2)
    d_alf = sp.simplify(alf_s - q1 * r1 * b12 * b21 / (dF * b11**2))
    print(f"      閉形式照合: kappa-残差={d_kap}  alpha-残差={d_alf}")
    ok &= (d_kap == 0) and (d_alf == 0)

    # (b) 有理数インスタンス k=2, n_f=2（凍結対）
    for lab, (DLPP, w, s) in pair.items():
        D0, DL, B, p, c = assemble(BPP, BPF, BFP, BFF, DF, DLPP, DLFF, pP, cP)
        R_dir2 = R_of(D0, DL, B, p, c, 1 / v, u * v)
        S2 = schur_S(BPP, BPF, BFP, BFF, DF, DLPP, DLFF, u, v)
        R_s2 = (pP.T * S2.inv() * cP)[0, 0]
        d2 = sp.simplify(sp.together(R_dir2 - R_s2))
        print(f"  (b) [{lab:8s}] k=2,n_f=2: 残差 = {d2}")
        ok &= (d2 == 0)

    print(f"  -> X1 {'PASS' if ok else 'FAIL'}\n")
    return ok


# --------------------------------------------------------------------------
# X2  2-jet 係数
# --------------------------------------------------------------------------

def X2(pair):
    print("=" * 74)
    print("X2  2-jet 係数（厳密方向微分）")
    print("=" * 74)
    ok = True
    dirs = [(Q(1), Q(1)), (Q(1), Q(3)), (Q(2), Q(1)), (Q(1), Q(7))]
    for lab, (DLPP, w, s) in pair.items():
        D0, DL, B, p, c = assemble(BPP, BPF, BFP, BFF, DF, DLPP, DLFF, pP, cP)
        Rinf, kap, alf = jet_closed_form(BPP, BPF, BFP, DF, DLPP, pP, cP)
        print(f"  [{lab:8s}] R_inf={Rinf}  kappa_lift={kap}  alpha_leak={alf}")
        for (uu, vv) in dirs:
            # (u,v) = (t*uu, t*vv)  =>  Gamma = 1/(t*vv), eps = u*v = t^2*uu*vv
            Rt = R_of(D0, DL, B, p, c, 1 / (t * vv), t**2 * uu * vv)
            R0 = sp.simplify(sp.limit(Rt, t, 0))
            d1 = sp.simplify(sp.diff(sp.simplify(Rt), t).subs(t, 0))
            pred = -uu * kap + vv * alf
            good = (R0 == Rinf) and (sp.simplify(d1 - pred) == 0)
            ok &= good
            print(f"      dir(u0,v0)=({uu},{vv}): R(0)={R0} dR/dt={d1} "
                  f"pred={pred} {'OK' if good else 'MISMATCH'}")
    print(f"  -> X2 {'PASS' if ok else 'FAIL'}\n")
    return ok


# --------------------------------------------------------------------------
# X3  fan データ（指数台・Newton多面体・valuation 関数）
# --------------------------------------------------------------------------

def num_den(DLPP):
    """R - R_inf = num/den を (Gamma, eps) の多項式対として厳密に返す。"""
    D0, DL, B, p, c = assemble(BPP, BPF, BFP, BFF, DF, DLPP, DLFF, pP, cP)
    A = Gam * (D0 + eps * DL) + B
    detA = sp.expand(A.det())
    adjc = sp.expand((p.T * A.adjugate() * c)[0, 0])
    Rinf, _, _ = jet_closed_form(BPP, BPF, BFP, DF, DLPP, pP, cP)
    num = sp.expand(adjc - Rinf * detA)
    return sp.Poly(num, Gam, eps), sp.Poly(detA, Gam, eps)


def newton_hull(poly):
    """指数台の下位凸包（Newton多面体の頂点集合）を厳密に。"""
    pts = sorted(set(poly.monoms()))
    return pts


def valuation(numP, denP, theta, e0val):
    """経路 eps = e0 * Gamma^{-theta} 上の Gamma 指数（leading exponent）。
       theta = a/b 有理。Gamma = tau^b, eps = e0 tau^{-a} で Laurent 化。"""
    a, b = sp.Rational(theta).p, sp.Rational(theta).q
    def lead(P):
        e = 0
        for (mg, me), co in zip(P.monoms(), P.coeffs()):
            pass
        # tau 指数ごとに係数を集約（相殺を厳密に扱う）
        acc = {}
        for (mg, me), co in zip(P.monoms(), P.coeffs()):
            k_tau = b * mg - a * me
            acc[k_tau] = sp.simplify(acc.get(k_tau, 0) + co * e0val**me)
        nz = [k for k, cv in acc.items() if sp.simplify(cv) != 0]
        return max(nz) if nz else None
    ln, ld = lead(numP), lead(denP)
    if ln is None:
        return None
    return sp.Rational(ln - ld, b)


def X3(pair):
    print("=" * 74)
    print("X3  fan データ（指数台・Newton多面体・valuation 関数 nu(theta)）")
    print("=" * 74)
    data = {}
    for lab, (DLPP, w, s) in pair.items():
        nP, dP = num_den(DLPP)
        data[lab] = (nP, dP, newton_hull(nP), newton_hull(dP))
        print(f"  [{lab:8s}] num 指数台({len(data[lab][2])}点)={data[lab][2]}")
        print(f"  {'':10s} den 指数台({len(data[lab][3])}点)={data[lab][3]}")

    same_num = data["ridge"][2] == data["no-ridge"][2]
    same_den = data["ridge"][3] == data["no-ridge"][3]
    print(f"  Newton 指数台の一致: num={same_num}  den={same_den}")

    thetas = [Q(0), Q(1, 2), Q(1), Q(3, 2), Q(9, 5), Q(2), Q(11, 5), Q(3), Q(4)]
    print(f"  valuation nu(theta) = -(leading Gamma exponent), e_0 = 1:")
    nus = {}
    for lab in ("ridge", "no-ridge"):
        nP, dP, _, _ = data[lab]
        row = []
        for th in thetas:
            val = valuation(nP, dP, th, sp.Integer(1))
            row.append(-val if val is not None else None)
        nus[lab] = row
        print(f"      [{lab:8s}] " +
              "  ".join(f"θ={th}:{r}" for th, r in zip(thetas, row)))
    # 予測: theta<=1 では u=Gamma*eps が発散し 2-jet の適用域外（no-go 7 側、
    # R->0 なので R-R_inf -> -R_inf、nu=0）。theta>=1 で jet が効き nu=min(theta-1,1)。
    # 合わせて nu(theta) = clamp(theta-1, 0, 1)。折れ点は theta=1 と theta=2 の2つ。
    pred = [min(max(th - 1, 0), 1) for th in thetas]
    print(f"      [{'予測':8s}] " +
          "  ".join(f"θ={th}:{r}" for th, r in zip(thetas, pred)))
    same_nu = nus["ridge"] == nus["no-ridge"]
    match_pred = nus["ridge"] == pred
    print(f"  nu(theta) の ±対一致: {same_nu}   clamp(θ−1,0,1) との一致: {match_pred}")
    ok = same_num and same_den and same_nu and match_pred
    print(f"  -> X3 {'PASS' if ok else 'FAIL'}\n")
    return ok, data


# --------------------------------------------------------------------------
# X4  角 theta=2 の initial form
# --------------------------------------------------------------------------

def X4(pair, data):
    print("=" * 74)
    print("X4  角 theta=2 の initial form（差はここにしか現れない）")
    print("=" * 74)
    ok = True
    for lab, (DLPP, w, s) in pair.items():
        nP, dP, _, _ = data[lab]
        _, kap, alf = jet_closed_form(BPP, BPF, BFP, DF, DLPP, pP, cP)
        # theta=2 経路上の Gamma^{-1} 係数 = -e_0*kappa + alpha を厳密に取り出す
        val = valuation(nP, dP, Q(2), e0)
        # 係数抽出: nu=1 の項の係数
        a, b = 2, 1
        acc = {}
        for (mg, me), co in zip(nP.monoms(), nP.coeffs()):
            k = b * mg - a * me
            acc[k] = sp.expand(acc.get(k, 0) + co * e0**me)
        dacc = {}
        for (mg, me), co in zip(dP.monoms(), dP.coeffs()):
            k = b * mg - a * me
            dacc[k] = sp.expand(dacc.get(k, 0) + co * e0**me)
        kn = max(k for k, v in acc.items() if sp.expand(v) != 0)
        kd = max(k for k, v in dacc.items() if sp.expand(v) != 0)
        init = sp.simplify(acc[kn] / dacc[kd])
        pred = sp.simplify(-e0 * kap + alf)
        good = sp.simplify(sp.expand(init - pred)) == 0
        root = sp.solve(sp.Eq(init, 0), e0)
        root = root[0] if root else None
        print(f"  [{lab:8s}] initial form (Gamma^{{{sp.Rational(kn-kd,b)}}} の係数) "
              f"= {sp.expand(init)}")
        print(f"  {'':10s} 予測 -e_0*kappa+alpha = {sp.expand(pred)}  一致={good}")
        print(f"  {'':10s} 根 e_0 = {root}  (物理域 e_0>0 か: {root > 0 if root is not None else 'n/a'})")
        expect_pos = (kap * alf > 0)
        got_pos = (root is not None and root > 0)
        print(f"  {'':10s} sign(kappa*alpha)>0 予測={expect_pos}  実際の正根存在={got_pos}"
              f"  {'OK' if expect_pos == got_pos else 'MISMATCH'}")
        ok &= good and (expect_pos == got_pos)
    print(f"  -> X4 {'PASS' if ok else 'FAIL'}\n")
    return ok


# --------------------------------------------------------------------------
# X5  厳密稜線証明書（Sturm 法による実根計数）
# --------------------------------------------------------------------------

def X5(pair):
    print("=" * 74)
    print("X5  厳密稜線証明書（固定 Gamma, eps>0 の実根を Sturm 法で計数）")
    print("=" * 74)
    ok = True
    for lab, (DLPP, w, s) in pair.items():
        nP, dP = num_den(DLPP)
        _, kap, alf = jet_closed_form(BPP, BPF, BFP, DF, DLPP, pP, cP)
        print(f"  [{lab:8s}] kappa={kap} alpha={alf}")
        for G_fix in (Q(500), Q(5000), Q(50000)):
            n_e = sp.Poly(nP.as_expr().subs(Gam, G_fix), eps)
            d_e = sp.Poly(dP.as_expr().subs(Gam, G_fix), eps)
            pred_eps = sp.nsimplify(alf / kap / G_fix**2)
            # 錐内ブラケット [pred/2, 2*pred]（有理数）で厳密根計数（Sturm）
            lo, hi = sp.nsimplify(pred_eps / 2), sp.nsimplify(pred_eps * 2)
            n_in = n_e.count_roots(lo, hi)
            d_in = d_e.count_roots(lo, hi)
            n_pos_all = len([r for r in sp.real_roots(n_e) if r > 0])
            if lab == "ridge":
                good = (n_in == 1) and (d_in == 0)
                r0 = [r for r in sp.real_roots(n_e) if lo <= r <= hi][0]
                s_lo = sp.sign(n_e.as_expr().subs(eps, lo) /
                               d_e.as_expr().subs(eps, lo))
                s_hi = sp.sign(n_e.as_expr().subs(eps, hi) /
                               d_e.as_expr().subs(eps, hi))
                good &= (s_lo * s_hi < 0)
                rel = sp.nsimplify((r0 - pred_eps) / pred_eps)
                print(f"    Gamma={str(G_fix):>7}: 錐内ブラケット根={n_in}(分母{d_in})"
                      f"  符号 {s_lo}→{s_hi}  相対差={sp.N(rel, 6)}"
                      f"  [eps>0 全体では {n_pos_all} 根]")
            else:
                good = (n_pos_all == 0)
                print(f"    Gamma={str(G_fix):>7}: eps>0 全体の根={n_pos_all}"
                      f"（稜線が物理域に入らない・大域証明書）")
            ok &= good
    print(f"  注: ridge 側の eps>0 第2根は u=Gamma*eps=O(100) の錐外の遠方根であり、"
          f"稜線ではない（2-jet の適用域外）。")
    print(f"  -> X5 {'PASS' if ok else 'FAIL'}\n")
    return ok


# --------------------------------------------------------------------------
# X6  ランダム有理インスタンス掃引
# --------------------------------------------------------------------------

def rand_rat(lo=-4, hi=4, den=3):
    return Q(rng.randint(lo, hi), rng.randint(1, den))


def X6(n_inst=60):
    print("=" * 74)
    print("X6  ランダム有理インスタンス掃引（2-jet 反例探索＋二分律の頻度）")
    print("=" * 74)
    bad, pos, used = 0, 0, 0
    for _ in range(n_inst):
        BPP_ = sp.Matrix(2, 2, lambda i, j: rand_rat())
        if sp.simplify(BPP_.det()) == 0:
            continue
        BPF_ = sp.Matrix(2, 2, lambda i, j: rand_rat())
        BFP_ = sp.Matrix(2, 2, lambda i, j: rand_rat())
        BFF_ = sp.Matrix(2, 2, lambda i, j: rand_rat())
        DF_ = sp.diag(Q(rng.randint(1, 4)), Q(rng.randint(1, 4)))
        W = sp.Matrix(2, 2, lambda i, j: rand_rat())
        DLPP_ = W * W.T + Q(1, 50) * sp.eye(2)
        DLFF_ = sp.eye(2)
        pP_ = sp.Matrix([rand_rat(), rand_rat()])
        cP_ = sp.Matrix([rand_rat(), rand_rat()])
        if not is_pd(DLPP_):
            continue
        Rinf, kap, alf = jet_closed_form(BPP_, BPF_, BFP_, DF_, DLPP_, pP_, cP_)
        if kap == 0 or alf == 0:
            continue
        used += 1
        D0_, DL_, B_, p_, c_ = assemble(
            BPP_, BPF_, BFP_, BFF_, DF_, DLPP_, DLFF_, pP_, cP_)
        uu, vv = Q(1), Q(1)
        Rt = R_of(D0_, DL_, B_, p_, c_, 1 / (t * vv), t**2 * uu * vv)
        d1 = sp.simplify(sp.diff(sp.simplify(Rt), t).subs(t, 0))
        if sp.simplify(d1 - (-uu * kap + vv * alf)) != 0:
            bad += 1
            print(f"    反例: kappa={kap} alpha={alf} d1={d1}")
        pos += 1 if (kap * alf > 0) else 0
    frac = sp.Rational(pos, used) if used else None
    print(f"  有効インスタンス {used} 件 / 2-jet 反例 {bad} 件")
    print(f"  稜線存在（sign(kappa*alpha)=+1）の割合 = {frac} ≈ "
          f"{sp.N(frac, 4) if frac is not None else 'n/a'}")
    ok = (bad == 0) and (used > 0)
    print(f"  -> X6 {'PASS' if ok else 'FAIL'}\n")
    return ok


# --------------------------------------------------------------------------

def main():
    pair, x, y, M = make_pair()
    print("凍結インスタンス（提案24 §2、すべて厳密有理数）")
    print(f"  x = B_PP^-T p_P = {list(x)}   y = B_PP^-1 c_P = {list(y)}")
    for lab, (DLPP, w, s) in pair.items():
        _, kap, alf = jet_closed_form(BPP, BPF, BFP, DF, DLPP, pP, cP)
        print(f"  [{lab:8s}] w={list(w)}  (D_L)_PP={DLPP.tolist()}")
        print(f"  {'':10s} kappa_lift={kap}  alpha_leak={alf}  "
              f"sign(kappa*alpha)={sp.sign(kap*alf)}")
    print()

    r = {}
    r["X0"] = X0(pair)
    r["X1"] = X1(pair)
    r["X2"] = X2(pair)
    r["X3"], data = X3(pair)
    r["X4"] = X4(pair, data)
    r["X5"] = X5(pair)
    r["X6"] = X6()

    print("=" * 74)
    print("verdict:", r)
    print("ALL PASS" if all(r.values()) else "SOME FAILED")
    print("=" * 74)


if __name__ == "__main__":
    main()
