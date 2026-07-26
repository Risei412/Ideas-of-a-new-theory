# CIRT — Window honesty 検査（T7）: 点極理想化を外す

**作成日:** 2026-07-26
**対象:** `docs/cirt-edge3-symmetry-audit.md` §6-1 が「必須の次作業」とした限界、
および CIRT §9.1 の第4停止条件「透明窓の理想化を外すとマージンが実験誤差以下に消える」
**実装:** `scripts/cirt_gauge_audit.py` の `run_T7()` ／ 制御 NC8–NC10
**生データ:** `docs/cirt-window-honesty.json`
**判定:** **ALIVE** — witness は点極理想化の除去を生き延びた

---

## 0. 結論

| 項目 | 結果 |
|---|---|
| **判定** | **ALIVE** |
| 有効な広がり $\Gamma_L$ の範囲 | $[10^{-4},\ 1/2]$ — **4桁**にわたる。fine-tuning ではない |
| 偽陽性の初出 | **掃引範囲内で一度も無し** |
| $\Gamma_L=1/100$ での窓漏れ | $\varepsilon_{\rm win}=3.6\times10^{-5}$（無視できる） |
| witness が消える広がり | $\Gamma_L\ge3/4$（窓半幅と同程度） |
| 制御 NC0–NC10 | **全 PASS** |

**T6 の ALIVE 判定は点極（デルタ関数）理想化の産物ではなかった。**
CIRT §9.1 の第4停止条件は**発火しない**。

副産物として、CIRT が §5 で「要証明」としていた **C10（定量Loewner・頑健証明書）の
定量的な中身**が得られた（§4）。

---

## 1. 検査した内容

T6 までの計算はスペクトル測度を**点質量**（デルタ関数）の和として扱っていた。
実際の線は有限幅を持ち、その裾は透明窓の内側にも重みを残す。本検査は各極を
HWHM $\Gamma_L$ の Lorentzian に置き換える。

厳密な広がり付き Herglotz 形（留数計算で導出し、数値求積で検証済み）:

$$h(z)=\frac{\mu}{t_0-i\Gamma_L-z},\qquad
S(\omega)=\frac{\mu\,(\omega-t_0)}{(\omega-t_0)^2+\Gamma_L^2},\qquad
\gamma(\omega)=\frac{2\mu\,\Gamma_L}{(\omega-t_0)^2+\Gamma_L^2}$$

$\Gamma_L\to0$ で T6 の点質量公式に戻る（**NC8** が相対誤差 $1.3\times10^{-10}$ で確認）。

---

## 2. 決定的な機構 — 偽陽性チャネル

$$M=\int\frac{d\mu(t)}{(t-\omega_1)(t-\omega_2)}$$

において、$t$ が $(\omega_1,\omega_2)$ の**内側**にあると分母は**負**である。したがって

> **窓の内側に漏れた重みは、$\mu$ が PSD であっても $M$ に負に寄与する。**

すなわち広がった線は、**純粋に受動的な媒質に対して witness を発火させうる**——偽陽性である。
これは CIRT の witness に対する、Edge (iii) とは独立な失敗様式である。

**NC9 がこの機構を厳密に確認した**: $\omega=0$（窓の中心）に置いた PSD 極は

$$M=\begin{pmatrix}-4&0\\0&-4\end{pmatrix}$$

という**負定値**の寄与を与える。

したがって本検査の判定は次の2条件の両立で定める。

- **(A) 偽陽性が無い**: 純 PSD の受動対照（2極版・3極版）で $M\succeq0$ が保たれる
- **(B) witness が生きる**: T6 の頑健 witness が3カーネル全てで依然発火する

---

## 3. 掃引結果

T6 の頑健 witness（$\alpha=\alpha'=1$、$\beta=1/2$、$\theta\approx43.6^\circ$、$t_g=2$、
$\Gamma_{\rm res}=7/20$）を固定し、$\Gamma_L$ を掃引した。

| $\Gamma_L$ | 偽陽性なし | 発火(3カーネル) | $\varepsilon_{\rm win}$ | $\max_W\lVert\gamma\rVert$ |
|---:|:---:|:---:|---:|---:|
| $10^{-4}$ | ✓ | ✓ | $3.6\times10^{-9}$ | $7.3\times10^{-5}$ |
| $1/100$ | ✓ | ✓ | $3.6\times10^{-5}$ | $7.3\times10^{-3}$ |
| $1/20$ | ✓ | ✓ | $9.1\times10^{-4}$ | $3.6\times10^{-2}$ |
| $1/10$ | ✓ | ✓ | $3.6\times10^{-3}$ | $7.2\times10^{-2}$ |
| $1/5$ | ✓ | ✓ | $1.4\times10^{-2}$ | $1.4\times10^{-1}$ |
| $2/5$ | ✓ | ✓ | $4.9\times10^{-2}$ | $2.5\times10^{-1}$ |
| **$1/2$** | ✓ | ✓ | $7.0\times10^{-2}$ | $2.8\times10^{-1}$ |
| $3/4$ | ✓ | **✗** | $1.2\times10^{-1}$ | $3.2\times10^{-1}$ |
| $1$ | ✓ | **✗** | $1.5\times10^{-1}$ | $3.1\times10^{-1}$ |

$\varepsilon_{\rm win}\equiv\max_{\omega\in W}\lVert\gamma(\omega)\rVert_{\rm op}\,/\,
\max_k(2\lVert\mu_k\rVert_{\rm op}/\Gamma_L)$（窓内の残留吸収を線のピーク吸収で規格化）。
**NC10** が $\varepsilon_{\rm win}$ の $\Gamma_L$ に対する単調性を確認している。

**有効範囲は $\Gamma_L\in[10^{-4},1/2]$ の4桁。** 上端では線幅が窓半幅と同程度になり
witness が消えるが、これは物理的に当然の振る舞いである（窓が窓でなくなる）。

---

## 4. 検査に歯があることの確認 — 偽陽性はどこで出るか

掃引範囲で偽陽性が一度も出なかったため、対照が弱すぎる可能性を排除する必要がある。
受動極の位置 $t_p$ を窓の縁へ寄せ、$\Gamma_L$ を上げて走査した。

| $t_p$ \ $\Gamma_L$ | $\le1$ | $3/2$ | $2$ |
|---:|:---:|:---:|:---:|
| $2$（witness 位置） | PSD | PSD | PSD |
| $3/2$ | PSD | PSD | PSD |
| $6/5$ | PSD | PSD | PSD |
| $11/10$ | PSD | PSD | **偽陽性** |
| $21/20$ | PSD | PSD | **偽陽性** |
| $1$（窓の縁） | PSD | **偽陽性** | **偽陽性** |

**偽陽性は実在する**（検査には歯がある）。ただし発生するのは、極が窓の縁 $|t_p|\lesssim1.1$ に
あり、かつ $\Gamma_L\gtrsim3/2$（窓の全幅と同程度以上）のときに限られる。

その領域の窓漏れ量を測ると:

| 状況 | $\varepsilon_{\rm win}$ |
|---|---:|
| witness、$\Gamma_L=1/100$ | $1\times10^{-4}$ |
| witness、$\Gamma_L=1/2$（上端） | $0.114$ |
| 偽陽性 $t_p=1,\ \Gamma_L=3/2$ | $0.680$ |
| 偽陽性 $t_p=11/10,\ \Gamma_L=2$ | $0.795$ |

> **偽陽性が起きるのは、窓のおよそ7〜8割が不透明になっている領域である。
> それはもはや透明窓ではない。**

---

## 5. 副産物 — C10（定量Loewner・頑健証明書）への定量的入力

CIRT §5 の定理ラダーは C10「残留吸収 $\gamma\le\varepsilon$ と測定CIに対する定量Loewner、
ABSTAIN分岐」を**要証明**としている。本検査はその定量的な中身を与える。

$$\boxed{\ \varepsilon_{\rm win}\lesssim0.1\ \Longrightarrow\ \text{偽陽性なし（witness は健全）}\ }$$
$$\varepsilon_{\rm win}\gtrsim0.68\ \Longrightarrow\ \text{受動媒質でも発火しうる（判定は無効）}$$

すなわち **$\varepsilon_{\rm win}$ 自体が十分な guard として機能する**。
測定された $\gamma$ から $\varepsilon_{\rm win}$ を評価し、閾値を超えていれば ABSTAIN に落とす、
という運用が可能である。これは C10 の完全な証明ではないが、
**ABSTAIN 分岐の発火条件を数値で与える**という点で実質的な前進である。

---

## 6. 限界（正直な記載）

1. **単一の $\Gamma_L$ を全極に共通で与えている。** 極ごとに異なる線幅は走査していない。
2. **Lorentzian 形状に固定**している。Gaussian / Voigt / 構造化スペクトル密度は未検証。
3. **$\varepsilon_{\rm win}$ の閾値 $0.1$ / $0.68$ は本 witness 幾何に対する経験値**であり、
   一般の証明ではない。C10 の証明そのものは未達である。
4. $p=2$、および T6 の頑健 witness 1点まわりのみ。witness 集合全体では走査していない。
5. 測定誤差・信頼区間は入れていない（C10 のもう半分）。

---

## 7. 本検査が CIRT の位置づけに与える影響

**scope は変わらない。** Pass 3 文献監査の判定（C1・C2・C5・C6・C7 と §6.1 の判定体系は
すべて先行研究）も、`docs/cirt-vacuousness-response.md` §8 の確定スコープ
（計測機器として PRApplied / PRA）も動かない。

変わったのは次の2点のみ:

1. **§9.1 の第4停止条件（透明窓の理想化）は発火しないことが確定した。**
   これで §9.1 の停止条件のうち、測度ゼロ・quantum surplus 消滅・ポート基底再定義・
   透明窓理想化の**4つが検証済みで、いずれも発火していない**。
   残るは C4 の形式化と、先行研究による降格（**これは既に発火済み**）である。
2. **C10 に定量的な入力が入った**（§5）。

---

## 8. 参照

- `scripts/cirt_gauge_audit.py` — `run_T7()`、制御 NC8–NC10、凍結基準は module docstring に逐語
- `docs/cirt-window-honesty.json` — 掃引の生データ
- `docs/cirt-edge3-symmetry-audit.md` §6-1（本検査を必須と指定）、§7-4
- `docs/cirt-vacuousness-response.md` §8（scope、変更なし）
- `docs/literature-audit-cirt-passive-realizability.md`（scope を決めている判定、変更なし）
- `Blueprints-of-theories/19_causal_interface_realizability_theory_proposal.md`
  §5 C10（**§5 で定量的入力**）、§9.1 第4停止条件（**発火せず**）
