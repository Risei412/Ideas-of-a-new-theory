"""
Gate P1/P2: 「受動性が吸収回復曲線を禁じる」no-go の最短生死判定。

背景（`docs/dark-ridge-novelty-verdict.md`）:
  三準位 Λ 系では Omega_p = 0 の定常状態が厳密に |g1><g1| になり（g1 が sink）、
  Im chi の分子が全単項式係数正の多項式になるため、吸収回復曲線は存在しなかった。
  残った問いは「符号を固定しているのは熱性・詳細釣合いなのか、dark-state 構造なのか」である。

本スクリプトは、g1 の sink 性だけを壊す jump operator を **一度に一本だけ** 追加し
（ガイド §4.4 の仮定変更予算、計算計画 §13.1 原因C）、Im chi の符号が反転するかを
exact に判定する。

  mode "w": L_w = sqrt(w) |g2><g1|   ground-state population transfer（光学的反転を作らない）
  mode "r": L_r = sqrt(r) |e><g1|    incoherent optical pump（反転を作りうる = LWI 配置）

判定の赤線（`docs/literature-master-table.csv` 行 N15, Liu 2026）:
  "only gain/inversion/parametric amplification ... violate passivity"
  => 符号反転に inversion / gain を要したら、その時点で先行研究へ還元されて死ぬ。
     生き残るのは「dark-state 構造だけが符号を固定している」場合のみ。

規約は `scripts/dark_ridge_lambda_model.py` をそのまま継承する
（C_chi = -1、vectorization、Im chi > 0 = 吸収）。判定に浮動小数点を使わない。
"""

from __future__ import annotations

import os
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dark_ridge_lambda_model import (  # noqa: E402
    BETA,
    C_CHI,
    EK,
    G1K,
    G2K,
    GAM12,
    I3,
    _solve_with_trace,
    hamiltonian,
    jump_operators,
    ket_bra,
    probe_superop,
    superop_commutator,
    superop_dissipator,
    vec_index,
)

W = sp.Symbol("w", positive=True)  # 追加チャネルのレート


def dissipator_rate(rate, A):
    """rate * D[A]。sqrt(rate) を作らないことで無理数を式に持ち込まない。

    `dark_ridge_lambda_model.superop_dissipator(sqrt(rate)*A)` と恒等的に等しい
    （下の T5 で毎回検算する）。radicals を避けるだけで、規約は同一である。
    """
    return rate * sp.Matrix(superop_dissipator(A))


def extra_jump(mode):
    if mode == "w":
        return ket_bra(G2K, G1K)   # g1 -> g2 population transfer
    if mode == "r":
        return ket_bra(EK, G1K)    # g1 -> e incoherent pump
    if mode == "none":
        return None
    raise ValueError(mode)


def liouvillian_ext(delta_p, delta2, omega_c, gamma1, gamma2, gamma12, mode, rate):
    Lsup = sp.Matrix(superop_commutator(hamiltonian(delta_p, delta2, omega_c)))
    Lsup += dissipator_rate(gamma1, ket_bra(G1K, EK))
    Lsup += dissipator_rate(gamma2, ket_bra(G2K, EK))
    Lsup += dissipator_rate(gamma12 / 2,
                            ket_bra(G1K, G1K) - ket_bra(G2K, G2K))
    A = extra_jump(mode)
    if A is not None:
        Lsup += dissipator_rate(rate, A)
    return sp.expand(Lsup)


def _solve_exact(A, b):
    """厳密な体上の線形解法。

    `Matrix.LUsolve` は結果を正規化しないため、9x9 でも入れ子分数が爆発して
    以降の `cancel` が事実上終わらない。DomainMatrix の分数体上で解くと
    各成分が既約分数として正規化される（厳密性は同じ、浮動小数点は介在しない）。
    """
    A = sp.Matrix(A).applyfunc(lambda e: sp.expand(sp.cancel(e)))
    b = sp.Matrix(b).applyfunc(lambda e: sp.expand(sp.cancel(e)))
    dA = DomainMatrix.from_Matrix(A).to_field()
    db = DomainMatrix.from_Matrix(b).convert_to(dA.domain)
    return dA.lu_solve(db).to_Matrix()


def _constrained_solve(Lsup, rhs, trace_value):
    """trace 行を置換した constrained solve（`_solve_with_trace` と同じ規約）。"""
    A = sp.Matrix(Lsup)
    b = sp.Matrix(rhs)
    for j in range(9):
        A[0, j] = 0
    for a in range(3):
        A[0, vec_index(a, a)] = 1
    b[0] = trace_value
    return _solve_exact(A, b)


def chi_ext(p, mode, rate):
    """chi と定常状態を返す（C_chi = -1 を継承）。"""
    Lsup = liouvillian_ext(p["Delta_p"], p["delta"], p["Omega_c"],
                           p["Gamma_1"], p["Gamma_2"], p["gamma_12"], mode, rate)
    rho0 = _constrained_solve(Lsup, sp.zeros(9, 1), sp.Integer(1))
    rho1 = _constrained_solve(Lsup, -(sp.Matrix(probe_superop()) @ rho0), sp.Integer(0))
    chi = C_CHI * sp.cancel(rho1[vec_index(EK, G1K)])
    return chi, rho0


# ---------------------------------------------------------------- 規約テスト


def convention_tests():
    """T0-T2 の再実行と、レート規約テスト（ガイド §4.2 no-go 12）。"""
    out = []
    G1v, G2v = sp.Rational(1, 2), sp.Rational(1, 2)
    p = dict(Gamma_1=G1v, Gamma_2=G2v, gamma_12=GAM12,
             Omega_c=sp.Rational(3), Delta_p=sp.Rational(1, 5), delta=sp.Rational(1, 7))

    for mode in ("w", "r"):
        L = liouvillian_ext(p["Delta_p"], p["delta"], p["Omega_c"],
                            p["Gamma_1"], p["Gamma_2"], p["gamma_12"], mode, W)
        tr_row = sp.zeros(1, 9)
        for a in range(3):
            tr_row += L[vec_index(a, a), :]
        out.append((f"[{mode}] T0a trace preservation",
                    sp.expand(tr_row) == sp.zeros(1, 9)))

        P = sp.zeros(9, 9)
        for a in range(3):
            for b in range(3):
                P[vec_index(a, b), vec_index(b, a)] = 1
        out.append((f"[{mode}] T0b hermiticity preservation",
                    sp.expand(P @ L.conjugate() @ P - L) == sp.zeros(9, 9)))

        # レート規約: 追加チャネル単体が各コヒーレンスを減衰させる率を確定する。
        # T5: rate 版 dissipator が sqrt(rate) 版と恒等的に一致すること
        A = extra_jump(mode)
        out.append((f"[{mode}] T5 dissipator_rate == superop_dissipator(sqrt(rate)*A)",
                    sp.expand(dissipator_rate(W, A)
                              - sp.Matrix(superop_dissipator(sp.sqrt(W) * A)))
                    == sp.zeros(9, 9)))

        Dx = sp.expand(dissipator_rate(W, A))
        for (a, b), label in [((EK, G1K), "rho_eg1"), ((G1K, G2K), "rho_g1g2")]:
            row = Dx[vec_index(a, b), :]
            coeff = sp.cancel(row[vec_index(a, b)])
            rest = sp.expand(row - coeff * sp.Matrix([[1 if j == vec_index(a, b) else 0
                                                       for j in range(9)]]))
            out.append((f"[{mode}] no-go 12: {label} の減衰率 = {coeff}"
                        + ("" if rest == sp.zeros(1, 9) else "（他成分への結合あり）"),
                        True))
    return out


# ---------------------------------------------------------------- Gate P1


OMC = sp.Symbol("Omega_c", positive=True)


def chi_infinity(mode, rate, base):
    """chi_inf(rate) := lim_{Omega_c -> oo} chi(Omega_c, gamma_12 = 0, rate)。

    比較クラス固定（ガイド §4.2 no-go 2）のため rate ごとに取り直す。
    自由記号は Omega_c のみに絞って解く（多記号だと式膨張で計算が終わらない）。
    """
    p = dict(base)
    p["Omega_c"] = OMC
    p["gamma_12"] = sp.Integer(0)
    chi, _ = chi_ext(p, mode, rate)
    return sp.limit(sp.cancel(chi), OMC, sp.oo)


def gate_p1_point(mode, rate, beta_value, base, chi_inf):
    """固定 (rate, beta) で F_abs / F_disp の正根と、その点での population を返す。"""
    p = dict(base)
    p["Omega_c"] = 2 * sp.sqrt(beta_value)
    p["gamma_12"] = GAM12
    chi, rho0 = chi_ext(p, mode, rate)

    diff = sp.cancel(sp.together(chi - chi_inf))
    num, den = sp.fraction(diff)
    num, den = sp.expand(num), sp.expand(den)
    f_abs = sp.expand(sp.im(num) * sp.re(den) - sp.re(num) * sp.im(den))
    f_disp = sp.expand(sp.re(num) * sp.re(den) + sp.im(num) * sp.im(den))

    roots_a = _pos_roots(f_abs)
    roots_d = _pos_roots(f_disp)
    inv = []
    for r in roots_a:
        pops = [sp.cancel(rho0[vec_index(a, a)].subs(GAM12, r)) for a in range(3)]
        inv.append(bool(sp.simplify(pops[2] - pops[0]) > 0))
    return roots_d, roots_a, inv


def gate_p1(mode, base, rate_values, beta_values):
    rows = []
    for rv in rate_values:
        chi_inf = chi_infinity(mode, rv, base)
        for bv in beta_values:
            rd, ra, inv = gate_p1_point(mode, rv, bv, base, chi_inf)
            rows.append((rv, bv, chi_inf, rd, ra, inv))
    return rows


def _pos_roots(expr):
    e = sp.cancel(sp.together(expr))
    if e == 0:
        return "identically zero"
    p = sp.Poly(sp.expand(sp.numer(e)), GAM12)
    if p.degree() == 0:
        return []
    return [r for r in sp.real_roots(p) if r.is_positive]


def main():
    print("=" * 72)
    print("Gate P1: 三準位 Λ + 一機構での吸収回復曲線探索 (exact arithmetic)")
    print("=" * 72)

    print("\n[規約テスト]")
    ok = True
    for name, passed in convention_tests():
        print(f"  {'PASS' if passed else 'FAIL'}  {name}")
        ok = ok and bool(passed)
    if not ok:
        print("\n規約テスト不合格。以降へ進まない。")
        return 1

    base = dict(Gamma_1=sp.Rational(1, 2), Gamma_2=sp.Rational(1, 2),
                Delta_p=sp.Rational(1, 5), delta=sp.Rational(1, 7))
    betas = [sp.Rational(1, 4), sp.Integer(1), sp.Integer(4), sp.Integer(25)]
    rates = [sp.Rational(1, 100), sp.Rational(1, 10), sp.Integer(1), sp.Integer(10)]

    verdicts = {}
    for mode, label in [("w", "P1a: L_w = sqrt(w)|g2><g1|  ground-state transfer"),
                        ("r", "P1b: L_r = sqrt(r)|e><g1|   incoherent optical pump")]:
        print(f"\n[{label}]")
        found_abs = False
        found_abs_without_inversion = False
        for rv, bv, chi_inf, rd, ra, inv in gate_p1(mode, base, rates, betas):
            tag = ""
            if isinstance(ra, list) and ra:
                found_abs = True
                tag = "   <== 吸収回復根あり  inversion=" + str(inv)
                if not all(bool(x) for x in inv):
                    found_abs_without_inversion = True
            print(f"  rate={rv} beta={bv}: chi_inf={chi_inf}  F_disp 正根={rd}  "
                  f"F_abs 正根={ra}{tag}")
        verdicts[mode] = (found_abs, found_abs_without_inversion)

    print("\n[回収テスト] rate -> 0 で三準位の結果（F_abs に正根なし）を再現するか")
    for mode in ("w", "r"):
        rows = gate_p1(mode, base, [sp.Rational(1, 10**6)], [sp.Integer(1)])
        _, _, _, _, ra, _ = rows[0]
        print(f"  [{mode}] rate=1e-6, beta=1: F_abs 正根={ra}"
              f"  -> {'PASS' if not (isinstance(ra, list) and ra) else 'FAIL'}")

    print("\n[符号反転の直接確認] Omega_c = 2 (beta = 1), rate = 1/10")
    print("  根の存在だけでなく、Im chi が実際に負（＝利得）へ抜けることと、")
    print("  そのとき probe 遷移に population inversion が無いことを同時に示す。")
    for mode in ("w", "r"):
        print(f"  --- mode {mode}")
        for g in [sp.Rational(1, 100), sp.Rational(1, 50), sp.Rational(1, 20),
                  sp.Rational(1, 10), sp.Rational(1, 5), sp.Rational(1, 2)]:
            p = dict(base)
            p["Omega_c"] = sp.Integer(2)
            p["gamma_12"] = g
            chi, r0 = chi_ext(p, mode, sp.Rational(1, 10))
            chi = sp.expand(chi)
            pops = [r0[vec_index(a, a)] for a in range(3)]
            sign = "gain " if sp.im(chi) < 0 else "absorb"
            print(f"    gamma_12={str(g):6s} Im chi={sp.nsimplify(sp.im(chi))} [{sign}]  "
                  f"rho_ee - rho_g1g1 = {sp.nsimplify(pops[2] - pops[0])} "
                  f"({'inverted' if pops[2] > pops[0] else 'NOT inverted'})")

    print("\n[判定]")
    for mode, (fa, fani) in verdicts.items():
        if not fa:
            print(f"  [{mode}] 吸収回復曲線なし。命題 N はこの機構では破れない。")
        elif fani:
            print(f"  [{mode}] 反転を伴わない符号反転あり => LWI 領域。族O 監査が必須。")
        else:
            print(f"  [{mode}] 符号反転はすべて population inversion を伴う "
                  f"=> 文献 N15 Remark 10 へ還元。FREEZE。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
