"""
提案21（RRT: Ramification Response Theory）の予備スモーク。

目的: 非半単純な protected kernel（D の零固有値に Jordan block）を持つ
      pencil A_Gamma(z) = Gamma*D + B + z*I について、
      (1) 固有分岐の Puiseux 指数が 1/ell 刻みになること
      (2) 応答汎関数の p-ノルム valuation が nu(s) = a + z*s, z = -1/ell となること
      (3) 半単純核（control）では整数指数へ戻ること
      (4) Jordan構造を eps で持ち上げると Gamma ~ eps^{-ell} で crossover すること
      を、独立実装なしの一次スモークとして測る。

注意: これは「証明」ではない。有限Gamma・有限窓・浮動小数点の測定である。
      主張の logical status は Numerical phenomenon。

実行: python3 scripts/ramification_smoke.py
依存: numpy のみ（QuTiP/Mathematica 不使用）
"""
import numpy as np

SEED = 11
n = 3


def setup(seed=SEED):
    rng = np.random.default_rng(seed)
    B = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)) + 0.5 * n * np.eye(n)
    p = rng.normal(size=n)
    c = rng.normal(size=n)
    P = rng.normal(size=(n, n))
    return B, p, c, P


def D_jordan():
    """ker D が非半単純（0固有値に J2）+ 高速方向1本。"""
    D = np.zeros((n, n))
    D[0, 1] = 1.0
    D[2, 2] = 1.0
    return D


def D_semisimple():
    """destruction control: 同じ kernel 次元だが半単純。"""
    return np.diag([0.0, 0.0, 1.0])


def branch_exponents(D, B, Gs):
    """固有値の |lambda| の log-log 傾き（Puiseux 指数の測定）。"""
    mags = np.array([np.sort(np.abs(np.linalg.eigvals(G * D + B))) for G in Gs])
    return np.diff(np.log10(mags), axis=0) / np.diff(np.log10(Gs))[:, None]


def response_norm(D, B, p, c, G, order, npts=40001):
    W = max(1.0, 5 * G ** 0.6)          # 窓は Gamma とともに広げる（fast branch を落とさない）
    w = np.linspace(-W, W, npts)
    a = np.abs([p @ np.linalg.solve(G * D + B + 1j * x * np.eye(n), c) for x in w])
    if order == np.inf:
        return a.max()
    return np.trapezoid(a ** order, w) ** (1.0 / order)


def nu_fan(D, B, p, c, Gs, orders=(1, 2, 4, np.inf)):
    out = {}
    for o in orders:
        vals = [response_norm(D, B, p, c, G, o) for G in Gs]
        out[o] = -np.polyfit(np.log10(Gs), np.log10(vals), 1)[0]
    return out


def main():
    B, p, c, P = setup()
    Gs_ev = np.array([1e3, 1e4, 1e5, 1e6, 1e7, 1e8])
    print("== (1) 固有分岐指数  d log|lambda| / d log Gamma")
    print("  非半単純 (J2 kernel):")
    print(branch_exponents(D_jordan(), B, Gs_ev))
    print("  半単純 control:")
    print(branch_exponents(D_semisimple(), B, Gs_ev))

    Gs = np.array([1e2, 1e3, 1e4, 1e5, 1e6])
    print("\n== (2)(3) p-ノルム valuation  nu(s)=a+z*s,  s=1/p")
    for name, D in (("非半単純 (J2 kernel)", D_jordan()),
                    ("半単純 control     ", D_semisimple())):
        f = nu_fan(D, B, p, c, Gs)
        print("  %s: %s" % (name, {("inf" if k == np.inf else k): round(v, 3)
                                   for k, v in f.items()}))

    print("\n== (4) Jordan持ち上げ eps による crossover（nu_1 のみ）")
    print("  window      eps=0     eps=1e-3   eps=1e-2")
    Dj = D_jordan()
    for lo in (2, 3, 4, 5, 6, 7):
        Gw = np.array([10.0 ** lo, 10.0 ** (lo + 0.5), 10.0 ** (lo + 1)])
        row = []
        for e in (0.0, 1e-3, 1e-2):
            vals = [response_norm(Dj + e * P, B, p, c, G, 1) for G in Gw]
            row.append(-np.polyfit(np.log10(Gw), np.log10(vals), 1)[0])
        print("  1e%d-1e%d  %s" % (lo, lo + 1, "  ".join("%+.3f" % v for v in row)))


if __name__ == "__main__":
    main()
