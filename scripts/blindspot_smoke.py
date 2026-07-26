"""
提案23（DIBT: Dark-Interface Blindness Theory）の予備スモーク。

目的: 暗セクター支持の介入対 (M_1, M_1 + Delta_S) について、
  (1) 深さ < beta_esc の全 protocol でトランスクリプトが「厳密に」一致すること
      （数値マッチングではなく、台構造による代数的相殺であること）
  (2) 脱出深さ beta_esc がゲート構造で設計可能であること（2段ゲートで beta_esc=4）
  (3) 脱出ギャップの因子化則: G[x,y] = (pi M_x u)(v M_y 1)、rank G <= rank Delta_S
  (4) destruction control: 初期分布の暗セクター漏れ eta で盲点が線形に破れること、
      右零条件 v^T 1 = 0 を壊すと深さ2で即座に見えること
  を古典 labeled Markov 模型（substochastic letters）で確認する。

注意: これは「証明」ではなく、量子GKSL版でもない。logical status は
      Exact（構成した class 内の恒等式）+ Model-specific observation。
      深さ<beta_esc の一致は浮動小数点の偶然ではなく、
      pi^T Delta = 0（台が暗セクター行のみ）と Delta 1 = 0（行和ゼロ）から
      端位置の Delta が必ず消えるためである。

実行: python3 scripts/blindspot_smoke.py
依存: numpy のみ
"""
import itertools

import numpy as np


def word_prob(Ms, pi, w):
    x = pi.copy()
    for a in w:
        x = x @ Ms[a]
    return x.sum()


def max_gap(Ms, Msp, pi, L, m):
    return max(abs(word_prob(Ms, pi, w) - word_prob(Msp, pi, w))
               for w in itertools.product(range(m), repeat=L))


def model_A(seed=22):
    """基本模型: n=5, 暗セクター={3,4}, rank-1 摂動, beta_esc=3."""
    rng = np.random.default_rng(seed)
    n, m = 5, 3
    raw = rng.uniform(0.1, 1.0, size=(m, n, n))
    norm = raw.sum(axis=(0, 2))
    M = [raw[a] / norm[:, None] for a in range(m)]
    pi = np.zeros(n)
    pi[:3] = rng.uniform(size=3)
    pi /= pi.sum()
    v = rng.normal(size=n)
    v -= v.mean()
    s = 0.5 * min(M[0][3, j] / (-v[j]) for j in range(n) if v[j] < 0)
    Delta = np.zeros((n, n))
    Delta[3] = s * v
    Mp = [M[0] + Delta] + [M[a].copy() for a in range(1, m)]
    assert (Mp[0] >= 0).all()
    return n, m, M, Mp, pi, Delta


def model_B(seed=23):
    """2段ゲート模型: 暗={4,5} へは gateway 状態3経由のみ、
    gateway へは文字2のみ → beta_esc=4 を設計。
    摂動 v の台は M[0] の暗行の正成分に限定する（非負性でスケールが潰れないため）。"""
    rng = np.random.default_rng(seed)
    n, m = 6, 3
    raw = rng.uniform(0.1, 1.0, size=(m, n, n))
    for a in range(m):
        raw[a][:, [4, 5]] = 0.0
        raw[a][3, [4, 5]] = rng.uniform(0.1, 1.0, 2)
        if a != 2:
            raw[a][:, 3] = 0.0
        raw[a][3, 3] = 0.0
    raw += 1e-12
    norm = raw.sum(axis=(0, 2))
    M = [raw[a] / norm[:, None] for a in range(m)]
    pi = np.zeros(n)
    pi[:3] = rng.uniform(size=3)
    pi /= pi.sum()
    v = np.zeros(n)
    v[:3] = rng.normal(size=3)
    v[:3] -= v[:3].mean()
    s = 0.5 * min(M[0][4, j] / (-v[j]) for j in range(n) if v[j] < 0)
    Delta = np.zeros((n, n))
    Delta[4] = s * v
    Mp = [M[0] + Delta] + [M[a].copy() for a in range(1, m)]
    assert (Mp[0] >= 0).all()
    return n, m, M, Mp, pi, Delta


def main():
    print("== (1) 基本模型 (beta_esc = 3): 深さ別最大ギャップ")
    n, m, M, Mp, pi, Delta = model_A()
    for L in range(1, 5):
        print("  depth %d: %.3e" % (L, max_gap(M, Mp, pi, L, m)))

    print("\n== (3) 脱出ギャップの因子化則 G[x,y] = pi M_x Delta M_y 1")
    one = np.ones(n)
    G = np.array([[pi @ M[x] @ Delta @ M[y] @ one for y in range(m)]
                  for x in range(m)])
    sv = np.linalg.svd(G, compute_uv=False)
    print("  特異値:", sv, " → rank(G) = 1 = rank(Delta_S)")
    err = max(abs(abs(word_prob(M, pi, (x, 0, y)) - word_prob(Mp, pi, (x, 0, y)))
                  - abs(G[x, y])) for x in range(m) for y in range(m))
    print("  深さ3実測ギャップとの最大差: %.2e" % err)

    print("\n== (4a) destruction control: 初期分布に暗セクター漏れ eta")
    for eta in (1e-2, 1e-3, 1e-4):
        pi2 = pi * (1 - eta)
        pi2[3] = eta
        g = max(max_gap(M, Mp, pi2, L, m) for L in (1, 2))
        print("  eta=%.0e  depth<=2 max gap = %.3e  (gap/eta = %.4f)"
              % (eta, g, g / eta))

    print("\n== (4b) destruction control: 右零条件 v^T 1 = 0 を破壊")
    D2 = Delta.copy()
    D2[3] += 0.05 * Delta[3].__abs__().max() * np.sign(Delta[3].sum() + 1e-30)
    D2[3, 0] += 0.01
    Mp2 = [M[0] + D2] + [M[a].copy() for a in range(1, m)]
    print("  depth<=2 max gap = %.3e （盲点が壊れる）"
          % max(max_gap(M, Mp2, pi, L, m) for L in (1, 2)))

    print("\n== (2) 2段ゲート模型 (設計 beta_esc = 4)")
    n, m, M, Mp, pi, Delta = model_B()
    for L in range(1, 6):
        print("  depth %d: %.3e" % (L, max_gap(M, Mp, pi, L, m)))
    best = max(((w, abs(word_prob(M, pi, w) - word_prob(Mp, pi, w)))
                for w in itertools.product(range(m), repeat=4)),
               key=lambda t: t[1])
    print("  最大ギャップ語:", best[0], "（予測: 先頭=2 [gatewayポンプ], 3文字目=0 [介入]）")


if __name__ == "__main__":
    main()
