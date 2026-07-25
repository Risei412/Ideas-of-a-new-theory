# P0-D 応答の理論導出可能性 監査

**実施日:** 2026-07-25
**問い:** 認証済みの P0-D 応答 `R_*`（`docs/p0-certificate-spec.md` §4quater）を、
候補理論（DCIT・CIRT・RISEI・SMRT）は実際に生成できるか。
**結論:** **導出は可能。ただし導出しても固有性は得られない。**

---

## 0. 要約

| 問い | 答え | 根拠 |
|---|---|---|
| RISEI/SMRT は `R(w)` の形を作れるか | **できる** | §1（protocol propagator の因子化） |
| その `R_*` は族A（hidden ancilla GKSL）を排除するか | **しない。桁が足りない** | §2（`dim K = 7` vs 予算 324） |
| DCIT は `R_*` を導出できるか | **現時点では不可** | §3（Priority 4 未着手） |
| P0-D の構造は固有現象になりうるか | **なりにくい。既に7回失敗した形** | §4（CIRT §0 の失敗監査） |
| P0-D の成果は無駄か | **無駄ではない。位置づけが違う** | §6 |

---

## 1. RISEI は word-Hankel の形を供給できる【肯定的結果】

`Frozen-Theories/Generalized_RISEI_Theory_EndToEnd_Certified_2026-07-23.tex` より：

- `def:protocol`（L156–164）— protocol は**順序付きリスト** `π = [(S_1,κ_1,I_1),…,(S_m,κ_m,I_m)]`。
  「Two protocols with the same sector set but different temporal order are distinct.」
  → **介入語 `w` の概念が理論側に既にある。**
- `ass:finite-time`（L166–176）— 主対象は protocol-resolved propagator
  `U_π(t,t_0) = T exp[∫ L_{Γ,π,0}(τ) dτ]`。

**補助仮定を1つ置けば因子化する。** 窓 `I_j` を互いに素・固定長 `Δt`・連続に取ると、
時間順序積は各窓ごとの伝播子の積に分解する：

```
U_π = M_{w_k} ⋯ M_{w_1},        M_u = exp(L_u Δt)
```

`L_u` は GKSL 許容（`ass` L141）なので **各 `M_u` は CPTP**。
POVM 要素 `E`（`0 ⪯ E ⪯ I`）と初期状態 `ρ_0` を固定すれば

```
R(w) = Tr[E M_{w_k} ⋯ M_{w_1} ρ_0] ∈ [0,1]
```

となり、**前回凍結した確率規約（§4quater）がそのまま自動的に満たされる。**
SMRT 側も `p†_full … c_full`（source `c_full`／readout covector `p†_full`、L121–130）という
同じ双線形形を持つ。

> **この写像は資産として残す。** どの候補理論を採るにせよ、「理論の応答 → 介入語の Hankel」
> という橋は共通に必要であり、上の1つの補助仮定（互いに素・固定長の窓）で渡せることが分かった。

## 2. しかし rank 障害は族Aの予算に対して桁が足りない【否定的結果】

`scripts/p0d_family_a_audit.py`（厳密有理数演算）の出力：

```
Hankel rank vs prefix/suffix length:
  half=0 (1x1)   rank R_* = 1,  rank R_D = 1
  half=1 (7x7)   rank R_* = 6,  rank R_D = 6      ← calibration は一致
  half=2 (43x43) rank R_* = 7,  rank R_D = 6      ← ここで分裂（P0-D）

dim K (飽和した reachable-observable 次元) = 7
```

`docs/reduction-targets.md` §A の族A target object は `dim K ≤ (d·D_hidden)²`。
凍結予算 `D_hidden ≤ 6` の下で：

| 系 | `d` | 族A予算 `(d·6)²` | `dim K` | 判定 |
|---|---:|---:|---:|---|
| qubit | 2 | 144 | 7 | 排除できない |
| **qutrit** | **3** | **324** | **7** | **排除できない（46.3倍の開き）** |
| ququart | 4 | 576 | 7 | 排除できない |

rank 7 を張るには Liouville 次元 `d² ≥ 7` ⇒ **最小で qutrit（`d=3`, `d²=9`）**。
そこでの族A予算は 324 で、`dim K = 7` はその **1/46**。

> **正確な言い方：** これは「族Aへ還元された」ではない（明示的な `D_hidden ≤ 6` dilation は
> 構成していない）。正しくは **「P0-D証明書は族Aに対する証拠を一切与えない」** —
> 排除の必要条件 `dim K > (d·D_hidden)²` を、どの系次元でも満たさない。

## 3. DCIT は現時点では `R_*` を導出できない

`Blueprints-of-theories/PRX_New_Theory_Blueprint_DCIT_2026-07-25.md` より：

- DCIT の中心witnessは `W_□ = √2 r − 1`（§4.2）。これは bath port の **context graph 上の
  静的な PSD completion 量**であり、時間方向の語・深さの構造を持たない。
- 時間応答への写像は **Priority 4「response pullbackと最小文法」** に置かれているが、
  設計図上まだ着手されていない（Gate P4 未達）。
- したがって「DCIT が `R_*` を生成するか」は**現時点では問える状態にない。**
  先に Priority 4 を閉じる必要がある。

加えて CIRT §0 は、DCIT 自身が
「(i) 既知のPSD completion定理（Grone et al. 1984）の移植に見えるリスク、
(ii) shared-ancilla 逃避で消えるリスク」を二重に負うと指摘している。

## 4. P0-D の構造は、すでに7回失敗している形である【最重要】

`Blueprints-of-theories/19_causal_interface_realizability_theory_proposal.md` §0 の失敗監査表には、
本作業と同型の候補が既に2件載っている：

| 候補現象 | 判定 | 還元先 |
|---|---|---|
| **resource-separation matched pair** | **FAIL** | Bayes仮説検定、非線形OED |
| **ternary irreducible response** | **FAIL** | ラベル付き到達可能性、**隠れMarkov模型** |

同§0の診断：

> RISEIの障害はすべて *組合せ論的・代数的* であった（格子、Möbius、**rank**、余次元、多面体）。
> そして組合せ論的障害は、**自由度を足せば必ず消える**。補助系を1つ足して、そこに手で書いた
> Lindblad散逸を与えれば、どんなcontext族も1つの加法的GKSLに埋め込める。**これが7回連続で起きた。**

`THEORY_PROPOSAL_GUIDE.md` §6.5 の教訓も同じ：

> **「局所同値 → 大域的obstruction → 有限資源certificate」という構造まで作り込んでも、
> それだけでは固有性にならない。** 上記はすべてこの構造を達成した上で死んでいる

**P0-D 証明書はまさにこの構造である** — depth≤3 で局所同値、depth-4 で大域的 rank 障害、
`σ₇ > τ_H` で有限資源certificate。§2 の数値はこの一般則の定量的な確認になっている。

## 5. RISEI 自身の非fine-tuning仮定との衝突

RISEI `ass:robustness`（L194）：

> A new response class or physical phenomenon must persist on a finite parameter region,
> remain stable under specified perturbations, or possess a clearly identified finite
> codimension. **An isolated exact zero is not sufficient by itself.**

現行構成は `g_u·c = 0`、`rank B_D = 6`、`Δ ≡ 0 (depth≤3)` という**厳密等式**に依存しており、
素朴にはこの仮定に抵触する。対処は2つあり、どちらも実施可能：

1. **calibration 一致を開条件に言い換える。** 証明書が要求しているのは本来
   「calibration に適合する6状態HMMが**存在する**」ことであり、実験的には
   **測定誤差内での一致**で十分である。この形なら開条件になり、fine-tuning 批判は構造的に無効化される。
   （full 側の `σ₇ > τ_H` は元々開条件なので問題ない）
2. **matched-pair 多様体の余次元を明示的に数える。** `ass:robustness` が要求する
   "clearly identified finite codimension" はこれで満たせる。未実施（次の作業）。

**なお、この fine-tuning は意図的なものである。** ガイド §6.1 の文献監査注記は P0-2 を
「**cancellation-protected / rank-deficient な例外集合における**、凍結資源内の lower bound」
として定式化せよと指示しており、非一般位置に置くこと自体は設計どおり。
問題は fine-tuning の有無ではなく、**それが §4 の還元を防がない**ことにある。

## 6. P0-D の成果をどう位置づけるか

**取り消さないもの（有効な資産）:**

- **古典資源分離としての主張** — 「凍結資源内で6次元以下の古典・線形実現は存在しない」は
  厳密に成立しており、`scripts/p0d_certify.py` が全項目を有理数演算で検証している。
  spec §3 が予告していた **PRL型の狭い主張**としては使える。
- **構成手法** — 非負HMMを先に置く／冪零鎖で depth を制御する／偏差を零特異方向に整合させる／
  設計格子で Hankel ブロックを測定可能にする、の4点は再利用可能な技法である。
- **§1 の RISEI→word-Hankel 写像** — どの候補理論でも必要になる橋。

**取り消すもの:**

- **「P0-D が理論固有現象への経路である」という位置づけ。** §2・§4 より、rank 障害は
  族Aの予算に対して桁が足りず、かつ自由度追加で消える種類の障害である。
  P0 全体（族A・E・DQ の排除）へ rank 証明書を積み増して到達する見込みはない。

## 7. 次にどこを叩くか

CIRT §0 の処方は明確である：

> 次の理論に課すべき条件はただ一つである。
> **補助系を足しても消えない種類の障害を、最初から中心に置くこと。**
> その条件を満たす物理量は、私の知る限り一つしかない。**因果性（受動性）**である。

その主張の要石が **CIRT 定理C4（Herglotz類の ancilla 閉性）** であり、設計図に
「C4が偽なら理論は終わる」と明記された**未証明**の命題である。
本監査と同時に `scripts/cirt_c4_smoke.py` でスモークした。

### C4 スモークの結果【判定: GO（反例なし）】

`python3 scripts/cirt_c4_smoke.py --depth 5 --trials 200`（p=2 ポート、深さ1–5、各200試行）。

検査項目：(a) `Im h(z) ⪰ 0`（上半平面）、(b) C2a `−(S(ω₁)−S(ω₂))/(ω₁−ω₂) ⪰ 0`
（透明窓内の点対）、(c) 全n点ブロック Loewner `L ⪰ 0`。

| モード | 試行 | 違反 | 内訳 (Imh/C2a/L) |
|---|---:|---:|---|
| passive-chain（受動ancilla鎖、深さ1–5） | 1000 | **0** | 0/0/0 |
| passive-spectral（有限階数の定常bath） | 1000 | **0** | 0/0/0 |
| ctrl-gain（利得項で受動性を破る） | 1000 | 653 | 581/**0**/432 |
| ctrl-negweight（スペクトル測度を不定符号にする） | 1000 | 1000 | 1000/809/1000 |

**検定力の確認（重要）:** 対照群だけで Im h が1581件、C2a が809件、L が1432件の違反を検出した。
特に **C2a を発火させられるのは negweight 対照のみ**（gain 対照では0件）であり、
最小witnessの検定力は不定符号スペクトル測度によってのみ担保される。
negweight 対照の C2a 最小固有値は **−4.95** まで達しており、
CIRT §4.4 の標的 `M = [[1,2],[2,1]]`（最小固有値 −1.0）を検出できる感度がある。

**結論:** 受動ancilla鎖 2000 例のいずれも Herglotz 閉性・C2 Loewner 条件を破らなかった。
**C4 と整合的**であり、rank障害を殺した shared-ancilla 逃避が、この障害に対しては
（少なくとも有限受動鎖の範囲で）効かないことを示唆する。

> ⚠️ **これは反例の不在であって C4 の証明ではない**（ガイド §9）。
> 検査したのは有限次元・有限深さの受動鎖に限られる。C4 の一般証明は未着手のままである。
> また本スモークは CIRT が固有現象を持つことを示すものではない — 塞いだのは
> 「7連敗をもたらした逃避路」1本のみである。
