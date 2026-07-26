# CIRT — Edge (iii) 対称性二重拘束の検証（T6）

**作成日:** 2026-07-26
**対象:** `docs/cirt-vacuousness-response.md` §5 が「最重要の未解決問題」として記録した Edge (iii)
**実装:** `scripts/cirt_gauge_audit.py` の `run_T6()` ／ `run_edge3_controls()`（NC0–NC7）
**生データ:** `docs/cirt-edge3-audit.json`
**判定:** **ALIVE** — CIRT は Edge (iii) では死ななかった

---

## 0. 結論

| 項目 | 結果 |
|---|---|
| **判定** | **ALIVE** |
| 走査点数 | 14,400（厳密有理格子） |
| witness 数 | Lorentzian 444 / root 471 / hard 486 |
| **3カーネル共通の witness** | **444**（カーネル依存 = **false**。人工物ではない） |
| 頑健 witness | $\alpha=\alpha'=1$、$\beta=1/2$、$u=2/5$（$\theta\approx43.6^\circ$）、$t_g=2$、$\Gamma=7/20$ |
| $\beta$ 方向の可行幅 | **36.6%**（相対）— fine-tuning ではない |
| 負制御 NC0–NC7 | **全 PASS** |
| 既存 CG2（T5,T1,T3,T2,T4）回帰 | **全 PASS** |

Edge (iii) の懸念——「surplus を生む異方性が、同時に縮退を解いて surplus を潰す」——は
**成立しなかった**。頑健な witness が3カーネル全て・traceless 感度変種・全パラメータの $\pm1\%$
摂動を生き延びた。CIRT §9.1 の第一停止条件（測度ゼロ／fine-tuning）は**発火しない**。

**ただし、この検証は同時に、私がこれまでに書いた主張を3つ反証した。**それらは §3 に記録する。
とくに §3.2・§3.3 は既存文書の訂正を要する。

**そして最も重要な留保:** ALIVE は CIRT の scope を**変えない**。§5 を参照。

---

## 1. 検証した命題

CG2 の T5 が確定した唯一の生存構造（対称性保護された縮退2重項＋偏光ポート＋等方的つまみ）で、
bath が系の対称性を破る（異方的である）とき:

- 異方性は非対角 $S_{12}$ を生む（＝ quantum surplus の源）
- **同じ異方性**は $H_{\rm LS}$ を通じて縮退2重項を分裂させる（$\delta>0$）
- 分裂は Bohr 周波数の一致を壊し、secular 近似が cross term を抑圧する

**問い:** 抑圧を受けてなお $\lambda_{\min}(M_{\rm eff})<0$ かつ port 基底の対角が正、という点が
**有限幅で**存在するか。存在しなければ CIRT は死ぬ。

---

## 2. Lemma 0（NC0 で厳密に確認）— 行列構造はどこに宿るか

$A_i$ は Hermitian であり、固有演算子分解は**両分枝**を持つ:

$$A_i(+\omega_0)=|g,i\rangle\langle e|\ \text{(下降)},\qquad A_i(-\omega_0)=|e\rangle\langle g,i|\ \text{(上昇)}$$

$H_{\rm LS}=\sum_\omega\sum_{ij}S_{ij}(\omega)A_i^\dagger(\omega)A_j(\omega)$ に代入すると

$$A_i^\dagger(+\omega_0)A_j(+\omega_0)=\delta_{ij}|e\rangle\langle e|
\quad\Longrightarrow\quad (\mathrm{tr}\,S)\,|e\rangle\langle e|\ \ \textbf{スカラー}$$
$$A_i^\dagger(-\omega_0)A_j(-\omega_0)=|g,i\rangle\langle g,j|
\quad\Longrightarrow\quad \sum_{ij}S_{ij}|g,i\rangle\langle g,j|\ \ \textbf{行列そのもの}$$

> **Lemma 0.** $S$ の $p\times p$ 行列構造は**縮退多重項上でのみ、かつ負の Bohr 周波数側でのみ**可視である。
> そこでは $H_{\rm LS}$ の多重項への制限が**ポート基底で書いた $S(\omega)$ そのもの**であり、
> 非縮退側ではスカラー $\mathrm{tr}\,S$ に潰れる。

帰結として、分裂量は $2|S_{12}|$ ではなく**固有値の全スプレッド**

$$\delta=\sqrt{(S_{11}-S_{22})^2+4S_{12}^2}$$

である。対角異方性だけでも縮退は解けるが surplus には寄与しない——**分裂は surplus より生成が安い**。

**NC0 が捕まえた実装上の罠:** 既存 `run_T5` は下降演算子のみを使っている。その規約では
$H_{\rm LS}$ は恒等的にスカラーで、非対角がどこにも現れない。さらに **Gram 行列の階数は
両規約とも 2 になる**ため、T5 の rank 判定は $S_{12}$ の可観測性に対して**必要条件であって
十分条件ではない**。NC0 なしに実装していれば「surplus はゼロ」という**偽の DEAD 判定**が出ていた。

---

## 3. 本検証が反証した、私自身の従来の主張3件（記録）

リポジトリの失敗監査の規律に従い、誤りを残す。

### 3.1 「$\Gamma\gtrsim4s$ が必要」（`cirt-vacuousness-response.md` §7 の派生主張）— 誤り

臨界点と比較していたための過大評価。実際の要求は $\Gamma\gtrsim1.1\,s$ 程度であり、
本検証の頑健 witness は $\Gamma=7/20$、$\bar\delta=1/3$、$\bar\delta/\Gamma\approx0.95$ で成立した。

### 3.2 「$\beta>\alpha$ が必要＝発火するのは非受動性が露骨な領域だけ」（同 §7）— **誤り**

§7 は**全ての極が窓から等距離**という暗黙の仮定の下で $\beta\in(1,2)$ を導いていた。
実際には $M=\sum_k\mu_k/[(t_k-\omega_1)(t_k-\omega_2)]$ であり、極が窓に近いほど $1/d^2$ で重みが増す。
本 witness では吸収極が $\pm5$、利得極が $t_g=2$ にあり、重み比は $(99/4)/(15/4)=6.6$ 倍。
その結果 **$\beta=1/2<\alpha=1$ で witness が成立**する。

$$\boxed{\text{総スペクトル重み}=\alpha+\alpha'-\beta=3/2>0\ \Longrightarrow\ \textbf{媒質は正味吸収性}}$$

すなわち**「閾値下のレーザーであり実験者は既に知っている」という §7 の結論は成立しない**。
必要なのは、窓の近くにある**適度な偏光利得特徴**だけであり、媒質全体は吸収性でよい。
**これは §7 の悲観的評価に対する実質的な訂正であり、CIRT の実用価値を上方修正する。**

### 3.3 「surplus ⟺ 偏光軸が回転する（$[S(\omega_1),S(\omega_2)]\neq0$）」— **誤り**

`docs/cirt-vacuousness-response.md` および Edge (iii) 設計時に、これを基底非依存の実験観測量として
提示した。**誤りである。** 頑健 witness では

$$\lVert[S(\omega_1),S(\omega_2)]\rVert=0\quad\text{（厳密ゼロ）}$$

でありながら $\lambda_{\min}(M_{\rm eff})<0$ が成立する。

誤りの所在: $[S_1,S_2]=0$ は「$M$ が **$S$ の共通固有基底**で対角」を意味するのであって、
「**ポート基底**で対角」を意味しない。surplus はポート基底についての主張なので含意が切れる。

さらに、単一の rank-1 異方性極を持つ模型では
$S(\omega)=f(\omega)I+g(\omega)P_\theta$ となり、**$[S(\omega_1),S(\omega_2)]=0$ は構造的に恒真**である
（記号計算で確認済み）。回転が起きるには**異なる角度の異方性極が2つ以上**必要。

**正しい言い方:** 偏光軸の回転は surplus の**十分条件であって必要条件ではない**。

---

## 4. さらに判明した、CIRT の修辞に対する重要な限定

$p=2$ の頑健 witness は $M=aI-bP_\theta$（$P_\theta$ は rank-1）の形をしており、
$\det M=a(a-b)$、固有値は $\{a,\ a-b\}$、固有基底は $P_\theta$ の固有基底（＝利得の偏光軸）である。

したがって **ポートを利得軸に合わせて回転すれば、$M$ は $\mathrm{diag}(a,\ a-b)$ となり、
$a-b<0$ は per-port の Kramers–Kronig 違反として古典的に見える。**

これは $p=2$ に限らない一般的事実である。任意の実対称 $M$ はその固有基底で対角化されるので、
**行列 surplus が「あらゆる per-port 測定に対して不可視」ということはあり得ない。**
surplus とは厳密には「**手持ちのポートが悪い軸と整列していない**」という状態である。

**公平な評価:** それでも行列判定には価値がある。

| | 行列判定（CIRT） | per-port 判定 |
|---|---|---|
| 必要な測定 | 固定基底で1回、2×2 を再構成 | 基底を**走査**して悪い軸を探す |
| 事前知識 | 不要 | 利得軸を知らないと走査が要る |

すなわち行列判定は **原理的に強いのではなく、基底走査を不要にするぶん効率的**である。
`19_...md` §4.4 の「per-port の古典記述では原理的に見えない」という表現は**過剰**であり、
「固定ポート基底では見えない／基底走査を要する」に改めるべきである。

---

## 5. ALIVE は CIRT の scope を変えない

Edge (iii) は**構造的な未解決問題を1つ閉じた**が、それ以上のことはしない。

- Pass 3 文献監査（`docs/literature-audit-cirt-passive-realizability.md`）の判定
  ——C1・C2・C5・C6・C7 と §6.1 の判定体系はすべて先行研究——は**まったく動かない**
- vacuousness 反論の Edge (i)（bath 由来データでは C2 は恒等的に成立）は**認めたまま**
- §4 により「per-port には原理的に不可視」という主張も**弱める**必要がある

**確定スコープは `cirt-vacuousness-response.md` §8 のまま:**

> 複合仮説 {定常・受動・弱結合・secular・因子化初期状態・凍結ポート基底・共通環境} に対する
> 有限・gauge 不変な反証試験。価値は物理ではなく**計測機器**として。投稿先は PRApplied / PRA。

**唯一の上方修正は §3.2 である。** 発火に必要なのは「正味非受動な媒質」ではなく
「正味吸収性の媒質に、窓の近くにある適度な偏光利得特徴」であり、これは §7 が想定したより
**はるかに現実的な実験条件**である。CIRT の計測機器としての価値はこの分だけ上がる。

---

## 6. 本検証の限界（正直な記載）

1. **極をデルタ関数として扱っている。** 実際の Lorentzian 裾が窓内に残す吸収
   （window honesty、$\max_{\omega\in W}\lVert\gamma(\omega)\rVert\le\varepsilon$）を検査していない。
   利得極が $t_g=2$ と窓端 $\omega=1$ に近いため、**この検査は必須の次作業**である。
   裾が窓を汚せば witness は無効になりうる。
2. **partial-secular の抑圧因子は ansatz である。** 3カーネルで一致したことは頑健性の証拠だが、
   厳密な導出ではない。unified GKLS からの導出は行っていない。
3. **格子は $\alpha=\alpha'=1$ に固定**している。非対称な吸収は走査していない。
4. **$p=2$ のみ。** $p\ge3$ は未検証。
5. 数値検証（`cirt-vacuousness-response.md` §7 の閉形式に対応する数値スイープ）は
   ユーザーのスコープ選択により未実施のまま。ただし §3.2 により、その閉形式の前提
   （等距離極）自体が特殊ケースであったことが判明している。

---

## 7. 勧告

1. **`docs/cirt-vacuousness-response.md` §7 を訂正する**（§3.2）。「$\beta>\alpha$ が必要」
   「非受動性が露骨な領域でしか発火しない」は誤り。極の距離を含めた正しい条件に置き換える。
2. **同 §5 の Edge (iii) を「決着済み・ALIVE」に更新する**。併せて §3.3 の「偏光軸回転」
   を十分条件に格下げする。
3. **`19_...md` §4.4 の表現を弱める**（§4）。「per-port では原理的に不可視」→
   「固定ポート基底では不可視、検出には基底走査を要する」。
4. **window honesty 検査を次の作業とする**（§6-1）。利得極が窓に近いことが witness の生命線
   （§3.2）である以上、裾の漏れは理論の実効性を直接左右する。
5. Pass 3 の判定と §5 の scope は**変更しない**。

---

## 8. 参照

- `scripts/cirt_gauge_audit.py` — `run_T6()`、`run_edge3_controls()`（NC0–NC7）、
  凍結判定基準は module docstring に逐語
- `docs/cirt-edge3-audit.json` — 生データ（14,400点の走査結果と厳密証明書）
- `docs/cirt-cg2-covariance-audit.md` §2 — T5（Edge (iii) の出発点）
- `docs/cirt-vacuousness-response.md` §5（Edge (iii) 提起）、§7（**§3.2 で訂正**）、§8（scope）
- `docs/literature-audit-cirt-passive-realizability.md` — Pass 3（scope を決めている判定）
- `Blueprints-of-theories/19_causal_interface_realizability_theory_proposal.md`
  §4.4（**§4 で表現の訂正が必要**）、§9.1（停止条件——**発火せず**）
