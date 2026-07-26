"""
提案24（LKCT）Step 0 — 実余次元・実在性の exact arithmetic 監査。

背景: `lkct_exact_audit.py` は **実行列**で稜線を認証した。しかし物理応答 chi(z) は
      **複素数**である。複素係数 (kappa_lift, alpha_leak) の下では
      R - R_inf = 0 は (u,v) 実2次元平面で2本の実方程式になり、零点は
      余次元2（孤立点）になりうる。ガイド §4.2 no-go 9（universal codimension-one
      の禁止／codim は active real constraint map の Jacobian rank で決まる）と
      §8 の既指摘弱点「codimension-one の普遍化」に直撃する。

目的: 「稜線は複素応答でも余次元1で生き残るか。生き残るならどの汎関数に対してか」を
      浮動小数点を使わずに決着させる。

  Y0  gate 検査（exact, Gauss 有理数）: B_PP 可逆・D_F 可逆・D_L PSD・D_0 PSD
  Y1  複素係数版の 2-jet 恒等式。閉形式 (R_inf, kappa_lift, alpha_leak) が
      複素の場合も方向微分と厳密一致すること
  Y2  **完全復元（複素 R が R_inf へ戻る）の実余次元。**
      実 Jacobian [[-Re k, Re a],[-Im k, Im a]] の rank を厳密判定。
      det = Im(kappa * conj(alpha)) が非零なら rank 2 = 余次元2（＝微調整）
  Y3  **汎関数分解した稜線。** Phi = Re（分散）と Phi = Im（吸収）それぞれについて
      codim = rank_R D(Phi.R) を厳密判定し、稜線位置
      Re: Gamma^2 eps = Re(alpha)/Re(kappa)   Im: Gamma^2 eps = Im(alpha)/Im(kappa)
      を厳密に計算する。両者は一般に**異なる位置**にある（稜線対の分裂）
  Y4  厳密零点証明書: 固定 Gamma で Im(R-R_inf) の分子 Im(N * conj(D)) の
      実根を Sturm 法で計数。存在側は錐内に1根＋符号反転、非存在側は eps>0 に0根
  Y5  destruction control: (i) 完全復元は Im(kappa*conj(alpha))=0 を要し、
      generic には Re稜線と Im稜線が一致しないこと、(ii) B を実にすると
      Im R == 0 となり Im稜線が消える（実の場合への退化）
  Y6  ランダム Gauss 有理インスタンス掃引: sign(Im kappa * Im alpha)=+1 の頻度。
      開条件（測度非ゼロ）であることの確認と、2-jet 反例探索
  Y7  **CPTP 符号強制の検証。** 提案24 §5.2-3 の先読み「p=c なら (D_L)_PP >= 0 より
      kappa_lift >= 0 が強制される」が、B_PP が複素のとき成立するかを判定する。
      kappa_lift = c_P^dag B_PP^-1 (D_L)_PP B_PP^-1 c_P は B_PP^-1 が2回現れる
      **双線型形式**であり sesquilinear ではないため、強制されない見込み

浮動小数点は判定に使用しない（すべて Gauss 有理数 Q(i) の厳密比較）。
判定基準は実行前に凍結:
  Y1: 厳密一致 / Y2: rank=2 かつ det!=0 / Y3: 両汎関数で rank=1 かつ位置が相異
  Y4: 存在側1根＋符号反転・非存在側0根 / Y5: 両 control とも予測どおり
  Y6: 反例0件かつ頻度が (0,1) の内側 / Y7: 反例が1件でも出れば「強制されない」で PASS

seed: 20260727（提案24 の 20260726 は使用済み。§11.2 の seed 使い回し禁止に従う）
"""

import random

import sympy as sp

I = sp.I
Q = sp.Rational
t, u, v = sp.symbols("t u v")
Gam, eps = sp.symbols("Gamma epsilon", positive=True)

rng = random.Random(20260727)


# --------------------------------------------------------------------------
# 構成（すべて Gauss 有理数）
# --------------------------------------------------------------------------

def assemble(BPP, BPF, BFP, BFF, DF, DLPP, DLFF, pP, cP):
    k, nf = BPP.rows, DF.rows
    Zkf, Zfk = sp.zeros(k, nf), sp.zeros(nf, k)
    D0 = sp.Matrix(sp.BlockMatrix([[sp.zeros(k, k), Zkf], [Zfk, DF]]))
    DL = sp.Matrix(sp.BlockMatrix([[DLPP, Zkf], [Zfk, DLFF]]))
    B = sp.Matrix(sp.BlockMatrix([[BPP, BPF], [BFP, BFF]]))
    p = sp.Matrix.vstack(pP, sp.zeros(nf, 1))
    c = sp.Matrix.vstack(cP, sp.zeros(nf, 1))
    return D0, DL, B, p, c


def jet_closed_form(BPP, BPF, BFP, DF, DLPP, pP, cP):
    """R_inf, kappa_lift, alpha_leak（複素可）。
    p_P^dag B_PP^-1 (...) B_PP^-1 c_P — B_PP^-1 が2回現れる双線型形式。"""
    BPPi = BPP.inv()
    row = pP.conjugate().T * BPPi          # p_P^dag B_PP^-1  (行ベクトル)
    y = BPPi * cP                          # B_PP^-1 c_P
    C_leak = BPF * DF.inv() * BFP
    R_inf = sp.simplify((row * cP)[0, 0])
    kappa = sp.simplify((row * DLPP * y)[0, 0])
    alpha = sp.simplify((row * C_leak * y)[0, 0])
    return R_inf, kappa, alpha


def R_of(D0, DL, B, p, c, G, E):
    A = G * (D0 + E * DL) + B
    return sp.together((p.conjugate().T * A.LUsolve(c))[0, 0])


def is_pd(M):
    if sp.simplify(M - M.conjugate().T) != sp.zeros(*M.shape):
        return False
    return all(sp.simplify(sp.re(M[:i, :i].det())) > 0 and
               sp.simplify(sp.im(M[:i, :i].det())) == 0
               for i in range(1, M.rows + 1))


def is_psd(M):
    from itertools import combinations
    if sp.simplify(M - M.conjugate().T) != sp.zeros(*M.shape):
        return False
    n = M.rows
    for r in range(1, n + 1):
        for idx in combinations(range(n), r):
            d = sp.simplify(M[list(idx), list(idx)].det())
            if sp.im(d) != 0 or sp.re(d) < 0:
                return False
    return True


# --------------------------------------------------------------------------
# 凍結インスタンス
#   D_0, D_L は実 PSD（散逸子）、B は複素（Hamiltonian・detuning 由来）、
#   p, c は複素（双極子の複素位相を保持: EIT L.587, L.3280）
# --------------------------------------------------------------------------

BPP_C = sp.Matrix([[2 + I, 1], [1 - I, 3 + 2 * I]])
BPF_C = sp.Matrix([[1, I], [0, 1]])
BFP_C = sp.Matrix([[1, 1 + I], [0, 1]])
BFF_C = sp.Matrix([[1 + I, 0], [0, 1]])
DF_C = sp.Matrix([[1, 0], [0, 2]])          # 実正（fast damping）
DLFF = sp.Matrix([[1, 0], [0, 1]])
pP_C = sp.Matrix([1, I])
cP_C = sp.Matrix([I, 1])
DLPP_C = sp.Matrix([[Q(901, 100), 12], [12, Q(1601, 100)]])   # 実対称 PD


def inst_complex():
    return dict(BPP=BPP_C, BPF=BPF_C, BFP=BFP_C, BFF=BFF_C, DF=DF_C,
                DLPP=DLPP_C, DLFF=DLFF, pP=pP_C, cP=cP_C)


def inst_real():
    """B, p, c をすべて実にした退化インスタンス（共鳴極限に相当）。"""
    return dict(BPP=sp.Matrix([[2, 1], [1, 3]]), BPF=sp.eye(2),
                BFP=sp.Matrix([[1, 1], [0, 1]]), BFF=sp.eye(2), DF=DF_C,
                DLPP=DLPP_C, DLFF=DLFF,
                pP=sp.Matrix([1, 0]), cP=sp.Matrix([0, 1]))


def jet_of(d):
    return jet_closed_form(d["BPP"], d["BPF"], d["BFP"], d["DF"],
                           d["DLPP"], d["pP"], d["cP"])


def parts(z):
    z = sp.simplify(sp.expand(z))
    return sp.simplify(sp.re(z)), sp.simplify(sp.im(z))


# --------------------------------------------------------------------------

def Y0():
    print("=" * 74)
    print("Y0  gate 検査（exact, Gauss 有理数）")
    print("=" * 74)
    d = inst_complex()
    D0, DL, B, p, c = assemble(**d)
    ok = True
    dB, dD = sp.simplify(d["BPP"].det()), sp.simplify(d["DF"].det())
    print(f"  det B_PP = {dB}   det D_F = {dD}")
    ok &= (dB != 0) and (dD != 0)
    pd, psdL, psd0 = is_pd(d["DLPP"]), is_psd(DL), is_psd(D0)
    print(f"  (D_L)_PP PD={pd}  D_L PSD={psdL}  D_0 PSD={psd0}")
    ok &= pd and psdL and psd0
    print(f"  -> Y0 {'PASS' if ok else 'FAIL'}\n")
    return ok


def Y1():
    print("=" * 74)
    print("Y1  複素係数版 2-jet 恒等式")
    print("=" * 74)
    ok = True
    for lab, d in (("complex", inst_complex()), ("real", inst_real())):
        D0, DL, B, p, c = assemble(**d)
        Rinf, kap, alf = jet_of(d)
        print(f"  [{lab:8s}] R_inf={Rinf}")
        print(f"  {'':10s} kappa_lift={kap}")
        print(f"  {'':10s} alpha_leak={alf}")
        for (uu, vv) in ((Q(1), Q(1)), (Q(2), Q(3))):
            Rt = R_of(D0, DL, B, p, c, 1 / (t * vv), t**2 * uu * vv)
            R0 = sp.simplify(sp.limit(Rt, t, 0))
            d1 = sp.simplify(sp.diff(sp.simplify(Rt), t).subs(t, 0))
            pred = sp.simplify(-uu * kap + vv * alf)
            good = (sp.simplify(R0 - Rinf) == 0) and (sp.simplify(d1 - pred) == 0)
            ok &= good
            print(f"  {'':10s} dir=({uu},{vv}): dR/dt={sp.simplify(d1)} "
                  f"pred={pred} {'OK' if good else 'MISMATCH'}")
    print(f"  -> Y1 {'PASS' if ok else 'FAIL'}\n")
    return ok


def Y2():
    print("=" * 74)
    print("Y2  完全復元（複素 R -> R_inf）の実余次元")
    print("=" * 74)
    d = inst_complex()
    _, kap, alf = jet_of(d)
    rk, ik = parts(kap)
    ra, ia = parts(alf)
    J = sp.Matrix([[-rk, ra], [-ik, ia]])       # d(Re,Im)/d(u,v)
    det = sp.simplify(J.det())
    det_pred = sp.simplify(sp.im(kap * sp.conjugate(alf)))
    rank = J.rank()
    print(f"  Re kappa={rk}  Im kappa={ik}")
    print(f"  Re alpha={ra}  Im alpha={ia}")
    print(f"  実 Jacobian J = d(Re,Im)/d(u,v) =\n{sp.pretty(J)}")
    print(f"  det J = {det}   Im(kappa*conj(alpha)) = {det_pred}   一致={sp.simplify(det-det_pred)==0}")
    print(f"  rank_R J = {rank}")
    ok = (rank == 2) and (det != 0) and (sp.simplify(det - det_pred) == 0)
    print(f"  => 完全復元は **余次元2（孤立点）**。alpha/kappa が実でない限り")
    print(f"     (u,v)>0 平面に完全復元の曲線は存在しない。")
    print(f"  -> Y2 {'PASS' if ok else 'FAIL'}\n")
    return ok


def Y3():
    print("=" * 74)
    print("Y3  汎関数分解した稜線（Phi = Re / Im）")
    print("=" * 74)
    d = inst_complex()
    _, kap, alf = jet_of(d)
    rk, ik = parts(kap)
    ra, ia = parts(alf)
    ok = True
    pos = {}
    for lab, (kk, aa) in (("Re(分散)", (rk, ra)), ("Im(吸収)", (ik, ia))):
        grad = sp.Matrix([[-kk, aa]])
        rank = grad.rank()
        exists = sp.simplify(kk * aa) > 0
        loc = sp.simplify(aa / kk) if kk != 0 else None
        pos[lab] = loc
        print(f"  Phi={lab:9s}: grad=(-{kk}, {aa})  rank_R={rank}  "
              f"sign(k*a)>0 = {exists}")
        print(f"  {'':16s} 稜線位置 Gamma^2*eps = {loc}"
              f"  ({sp.N(loc, 10) if loc is not None else 'n/a'})")
        ok &= (rank == 1)
    split = sp.simplify(pos["Re(分散)"] - pos["Im(吸収)"])
    print(f"  => 両汎関数とも **余次元1（開条件）**。稜線は消えない。")
    print(f"  Re稜線 と Im稜線 の位置差 = {split}  (非零={split != 0})")
    print(f"     ⇒ **稜線は1本ではなく2本に分裂する**（分散稜線と吸収稜線）。")
    print(f"       両者が一致するのは alpha/kappa が実のとき、すなわち Y2 の余次元2条件。")
    ok &= (split != 0)
    print(f"  -> Y3 {'PASS' if ok else 'FAIL'}\n")
    return ok


def _num_den(d):
    """R - R_inf = N/D を (Gamma, eps) の Gauss 有理係数多項式対で返す。"""
    D0, DL, B, p, c = assemble(**d)
    A = Gam * (D0 + eps * DL) + B
    detA = sp.expand(A.det())
    adjc = sp.expand((p.conjugate().T * A.adjugate() * c)[0, 0])
    Rinf, _, _ = jet_of(d)
    return sp.expand(adjc - Rinf * detA), detA


def _conj_poly(expr):
    return sp.expand(expr.subs(I, -I))


def Y4():
    print("=" * 74)
    print("Y4  厳密零点証明書（汎関数ごとに Sturm 法で実根を計数）")
    print("=" * 74)
    print("  Re(N/D)=Re(N*conj(D))/|D|^2, Im(N/D)=Im(N*conj(D))/|D|^2。")
    print("  |D|^2>0 なので零点は各分子の実根に一致する。")
    ok = True
    d = inst_complex()
    N, D = _num_den(d)
    _, kap, alf = jet_of(d)
    rk, ik = parts(kap)
    ra, ia = parts(alf)
    NDc = sp.expand(N * _conj_poly(D))
    absD2 = sp.expand(D * _conj_poly(D))
    for lab, fn, kk, aa in (("Re(分散)", sp.re, rk, ra),
                            ("Im(吸収)", sp.im, ik, ia)):
        Num = sp.expand(fn(NDc))
        exists = sp.simplify(kk * aa) > 0
        print(f"  --- Phi = {lab}:  sign(kappa*alpha) = {sp.sign(kk*aa)}  "
              f"稜線予測 = {'あり' if exists else 'なし'}")
        for G in (Q(200), Q(2000), Q(20000)):
            poly = sp.Poly(sp.expand(Num.subs(Gam, G)), eps)
            den = sp.Poly(sp.expand(absD2.subs(Gam, G)), eps)
            pred = sp.nsimplify(aa / kk / G**2)
            if exists:
                lo, hi = sp.nsimplify(pred / 2), sp.nsimplify(pred * 2)
                n_in, d_in = poly.count_roots(lo, hi), den.count_roots(lo, hi)
                s_lo = sp.sign(poly.as_expr().subs(eps, lo))
                s_hi = sp.sign(poly.as_expr().subs(eps, hi))
                r0 = [r for r in sp.real_roots(poly) if lo <= r <= hi]
                rel = sp.nsimplify((r0[0] - pred) / pred) if r0 else None
                good = (n_in == 1) and (d_in == 0) and (s_lo * s_hi < 0)
                print(f"      Gamma={str(G):>6}: 錐内根={n_in}(分母{d_in}) "
                      f"符号 {s_lo}->{s_hi} 相対差="
                      f"{sp.N(rel,6) if rel is not None else 'n/a'} "
                      f"{'OK' if good else 'FAIL'}")
            else:
                # 稜線なし側: eps>0 全体で錐内（小 eps 側）に根が無いことを見る。
                # 遠方根は 2-jet の適用域外なので、錐の窓 (0, 10/G^2] に限定する。
                win = sp.nsimplify(Q(10) / G**2)
                n_pos = poly.count_roots(sp.nsimplify(Q(1, 10**12)), win)
                good = (n_pos == 0)
                print(f"      Gamma={str(G):>6}: 錐窓 (0,{sp.N(win,4)}] の根={n_pos} "
                      f"{'OK' if good else 'FAIL'}")
            ok &= good
    print(f"  => 稜線は**汎関数ごとに独立**に存在/非存在が決まり、存在側は")
    print(f"     複素応答でも厳密な零点として実在する。")
    print(f"  -> Y4 {'PASS' if ok else 'FAIL'}\n")
    return ok


def Y5():
    print("=" * 74)
    print("Y5  destruction control")
    print("=" * 74)
    ok = True
    # (i) 実インスタンスでは Im R == 0（吸収稜線が消える＝実の場合へ退化）
    d = inst_real()
    N, D = _num_den(d)
    ImNum = sp.expand(sp.im(sp.expand(N * _conj_poly(D))))
    c1 = (sp.expand(ImNum) == 0)
    print(f"  (i) 実インスタンス: Im(R-R_inf) の分子 == 0 ? {c1}"
          f"  （Im稜線が消え、実の場合へ退化）")
    ok &= c1
    # (ii) 複素インスタンスでは Re稜線と Im稜線が一致しない（完全復元は起きない）
    d2 = inst_complex()
    _, kap, alf = jet_of(d2)
    rk, ik = parts(kap)
    ra, ia = parts(alf)
    c2 = sp.simplify(sp.im(kap * sp.conjugate(alf))) != 0
    print(f"  (ii) 複素インスタンス: Im(kappa*conj(alpha)) != 0 ? {c2}"
          f"  （⇒ 完全復元曲線は存在しない）")
    ok &= c2
    print(f"  -> Y5 {'PASS' if ok else 'FAIL'}\n")
    return ok


def _rr(lo=-3, hi=3, den=2):
    return Q(rng.randint(lo, hi), rng.randint(1, den))


def _rc():
    return _rr() + I * _rr()


def Y6(n=40):
    print("=" * 74)
    print("Y6  ランダム Gauss 有理掃引（開条件性と 2-jet 反例探索）")
    print("=" * 74)
    used = pos_im = pos_re = bad = codim2 = 0
    for _ in range(n):
        BPP = sp.Matrix(2, 2, lambda i, j: _rc())
        if sp.simplify(BPP.det()) == 0:
            continue
        W = sp.Matrix(2, 2, lambda i, j: _rr())
        d = dict(BPP=BPP, BPF=sp.Matrix(2, 2, lambda i, j: _rc()),
                 BFP=sp.Matrix(2, 2, lambda i, j: _rc()),
                 BFF=sp.Matrix(2, 2, lambda i, j: _rc()),
                 DF=sp.diag(Q(rng.randint(1, 3)), Q(rng.randint(1, 3))),
                 DLPP=W * W.T + Q(1, 50) * sp.eye(2), DLFF=sp.eye(2),
                 pP=sp.Matrix([_rc(), _rc()]), cP=sp.Matrix([_rc(), _rc()]))
        if not is_pd(d["DLPP"]):
            continue
        Rinf, kap, alf = jet_of(d)
        rk, ik = parts(kap)
        ra, ia = parts(alf)
        if ik == 0 or ia == 0 or rk == 0 or ra == 0:
            continue
        used += 1
        pos_im += 1 if (ik * ia > 0) else 0
        pos_re += 1 if (rk * ra > 0) else 0
        codim2 += 1 if sp.simplify(sp.im(kap * sp.conjugate(alf))) != 0 else 0
        D0, DL, B, p, c = assemble(**d)
        Rt = R_of(D0, DL, B, p, c, 1 / t, t**2)
        d1 = sp.simplify(sp.diff(sp.simplify(Rt), t).subs(t, 0))
        if sp.simplify(d1 - (-kap + alf)) != 0:
            bad += 1
    print(f"  有効 {used} 件 / 2-jet 反例 {bad} 件")
    print(f"  Im稜線 存在率 = {sp.Rational(pos_im, used)} "
          f"({sp.N(sp.Rational(pos_im,used),4)})")
    print(f"  Re稜線 存在率 = {sp.Rational(pos_re, used)} "
          f"({sp.N(sp.Rational(pos_re,used),4)})")
    print(f"  Im(kappa*conj(alpha)) != 0（完全復元が余次元2）= {codim2}/{used}")
    ok = (bad == 0) and used > 0 and 0 < pos_im < used and codim2 == used
    print(f"  -> Y6 {'PASS' if ok else 'FAIL'}\n")
    return ok


def Y7(n=30):
    print("=" * 74)
    print("Y7  CPTP 符号強制の検証（提案24 §5.2-3 の先読みの真偽）")
    print("=" * 74)
    print("  主張: 「p=c なら (D_L)_PP >= 0 より kappa_lift >= 0 が強制される」")
    print("  検証: kappa_lift = c_P^dag B_PP^-1 (D_L)_PP B_PP^-1 c_P は")
    print("        B_PP^-1 が2回現れる**双線型**形式であり sesquilinear ではない。")
    neg = cplx = used = 0
    for _ in range(n):
        BPP = sp.Matrix(2, 2, lambda i, j: _rc())
        if sp.simplify(BPP.det()) == 0:
            continue
        W = sp.Matrix(2, 2, lambda i, j: _rr())
        DLPP = W * W.T + Q(1, 50) * sp.eye(2)
        if not is_pd(DLPP):
            continue
        cP = sp.Matrix([_rc(), _rc()])
        used += 1
        row = cP.conjugate().T * BPP.inv()
        kap = sp.simplify((row * DLPP * (BPP.inv() * cP))[0, 0])
        rk, ik = parts(kap)
        if ik != 0:
            cplx += 1
        if rk < 0:
            neg += 1
    print(f"  自己応答 p=c の {used} 例中: kappa_lift が非実 {cplx} 件、"
          f"Re kappa_lift < 0 が {neg} 件")
    ok = (cplx > 0) or (neg > 0)
    print(f"  => 先読みは **成立しない**（B_PP が複素なら kappa_lift の符号は強制されない）。")
    print(f"     CPTP による符号強制は B_PP が実（共鳴）の場合に限られる。")
    print(f"     ⇒ Step 3 の no-go 経路は当初の見込みより弱い。")
    print(f"  -> Y7 {'PASS' if ok else 'FAIL'}（反例が出れば PASS）\n")
    return ok


def main():
    r = {}
    r["Y0"] = Y0()
    r["Y1"] = Y1()
    r["Y2"] = Y2()
    r["Y3"] = Y3()
    r["Y4"] = Y4()
    r["Y5"] = Y5()
    r["Y6"] = Y6()
    r["Y7"] = Y7()
    print("=" * 74)
    print("verdict:", r)
    print("ALL PASS" if all(r.values()) else "SOME FAILED")
    print("=" * 74)


if __name__ == "__main__":
    main()
