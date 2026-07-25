# 計画18: 操作的Newton fan理論（PRX投稿を見据えた新理論提案）

**作成日:** 2026-07-24
**改訂:** 2026-07-24（rev.2 — 外部査読を受けてACCを撤回し、face–codimension則へ置換）
**位置づけ:** これは実行構成でも数値計画でもなく、RISEI/RISERの既存定理・数値証拠を土台として
理論を一段抽象化した新理論を提案する検討書である。実行を強制するものではなく、
理論構築・証明・査読前検証のための設計図として次の判断材料に供する。

**rev.2での変更（重要）:** 初版の中心命題であった「異常–余次元対応（ACC:
異常次数 = 実現余次元）」は**反例により撤回した**（§1.1）。中心は
face係数写像の正則値定理（N3）へ移し、論文としての決定点は
interface非同定可能性（N2）へ移す。トロピカル表現定理（N1）・
普遍wall crossover（N4）は残り、後者は一般化された。

---

## 0. 出発点：2つの厳密則は1つのアフィン式の特殊値である

このリポジトリで独立に認証された2つの厳密スケーリング則を並べる。

| 現象 | 認証箇所 | 厳密則 |
|---|---|---|
| pattern (a): Ω₁₂のp-ノルム階層 | `latest_theory_program` Gate G1 PASS | ν_T^(p) = 1 − 1/p （T=1,2；p=1〜20、最大偏差0.022） |
| pattern (b): 逆functional hierarchy | `patternb_gksl_program` Gate G3 PASS | (k_min^(∞), k_min^(1)) = (2, ∞)；`C_inf(Ω₁₂)=0.759>0`, `ν1(Ω₁₂)=1.005` |

s := 1/p ∈ [0,1] とおくと、両方とも**アフィン式 ν(s) = a + z·s の特殊値**として書ける：

- pattern (a) の単独セクター Ω₁: ν(s) = 1 − s → (a, z) = (1, −1)
- pattern (a) の Ω₁₂（joint、両汎関数で保護）: ν(s) ≡ 0 → (a, z) = (0, 0)
- pattern (b) の Ω₁₂（peak保護・面積非保護）: ν(0)=0（G3: C_inf>0）、ν(1)≈1.005 → (a, z) = (0, 1)

**この整列には初等的だが決定的な根拠がある。** 単一の特徴
R(ω) = h·f((ω−ω₀)/w)（f は固定形状、h=高さ、w=幅）に対し
$$\|R\|_p^p = h^p\, w \int |f|^p \quad\Longrightarrow\quad \|R\|_p \sim h\, w^{1/p}.$$
h ∼ Γ^{−a}、w ∼ Γ^{−z} と置けば、ただちに
$$\boxed{\nu(s) = a + z\,s,\qquad s = 1/p}$$
が出る。**a は高さ指数、z は幅指数**であり、傾き z の符号がそのまま
narrowing（z>0）／broadening（z<0）に対応する。
pattern (a) の (1,−1) は `thm:exact-model` の Θ(Γ)幅の棚（broadening）、
pattern (b) の (0,1) は Schur–Zeno narrowing（幅 ∼ J²/Γ、
`coherence_block.py` の A=B=2J²）に正確に対応する。

---

## 1. 理論名と中心主張

**操作的Newton fan理論**（Operational Newton Fan theory）。

一言で：*観測されるsector応答則は無介入generatorだけでは決まらない。
介入interfaceが応答有理関数のNewton多面体を定め、有限介入資源とnative散逸の
相対scaling rayがそのfaceを選ぶ。その結果得られる次数fanは、uncut responseだけからは
一般に復元できない。*

### 1.1 撤回した命題：異常–余次元対応（ACC）

初版では「異常次数 d（narrowing頂点の個数）= 実現余次元」を中心定理候補に置いた。
**これは誤りであり撤回する。** 反例は§0の初等計算そのものである：

> 単一の自己相似narrowing特徴（h ∼ Γ⁰, w ∼ Γ⁻¹）は ν(s)=s を与え、
> **傾き z>0 が特徴1個から、いかなる係数相殺もなしに生じる。**

初版のT3は「正の傾き ⟸ `lem:min-rule` の主要係数相殺 ⟸ 解析的条件1本 ⟸ 余次元1」
と連鎖させたが、**第一の含意が偽**である。加えて高次元でのrank–codimension計算は、
同一の指数構造に対して異なる余次元を許すため、d と codim の一対一対応は
一般則として維持できない。

**では pattern (b) の θ_c=π/2 fine-tuning（Gate G4 FAIL, ε≈3.664×10⁻⁵ rad）は
何の代償だったのか。** 傾き z=1 の代償ではなく、**joint成分の高さ指数 a を 0 に
落とす（generic face係数を消す）代償**である。余次元の出所は narrowing頂点の数ではなく、
**消すべき独立なface係数の本数**であり、これが下記N3の内容になる。

---

## 2. 創設の問い（未解決性・分野横断性）

**問い:** 「有限介入下の開放系において、sector応答の抑制則（どの汎関数に機構が見え、
どの資源pathでどのfaceが露出するか）は何によって決まるか。それは無介入generatorと
uncut responseだけから復元できるか。」

後半（非同定可能性）が本理論の決定的な問いである。分野横断先：

- **開放量子系の基礎**: 「同じ系」の定義を (generator, interface, resource protocol)
  の組へ拡張することを要求する。
- **量子制御・系同定**: 非同定可能性を no-go で終わらせず、
  「どのinterfaceを追加すれば隠れたsector lawを識別できるか」という
  **最小介入設計問題**へ変換できる。
- **分光学**: EIT/ATS/CPT の機構分類とは独立に、resource path に対する
  peak/area/L^p 応答の次数fanを分類軸として導入する。同じfanの共有は
  機構の同一性ではなく**有限介入下の操作的同値性**を意味する。
- **非エルミート物理**: EPでの方向依存scalingを非EP領域・有限介入へ拡張しうる。
  ただしNewton polygon・方向依存scalingの先行研究が近く、**競合が最も強い**。
  用語の移植だけでは新規性にならない。
- **古典Markov過程・反応ネットワーク**: 同じ有理応答とNewton supportを持ちうるが、
  tropical dominant-subsystem分類は既知。示すべき新規結果は
  「同一uncut kineticsを持ちながらinterfaceの違いで異なるsector fanを持つmatched pair」。
- **量子計測**: 応答増幅と情報量増大は同義ではなく、fanからQFI scalingは自動的には
  出ない。measurement modelとnoiseを含む独立証明が要る（現時点では予言段階）。

---

## 3. 定理ラダー

| # | 定理 | 内容 | 現時点の地位 |
|---|---|---|---|
| **N1** | Operational Newton-fan theorem | 宣言された正則条件下で ν_{S,𝓘}(**q**,s) が区分アフィン（トロピカル）になる | 条件付き厳密定理候補 |
| **N2** | Interface non-identifiability | 同一 𝓛₀ と同一uncut responseでも、異なる物理interfaceが異なるfanを与えうる | **matched-pair構成が必要（決定点）** |
| **N3** | Face–codimension theorem | 正則点で codim_ℝ ℳ_F = rank_ℝ Dc_F | 厳密定理候補（ACCの置換） |
| **N4** | Universal wall crossover | x = δθ·Γ^{Δν/m} による有限-Γ collapse | 既存M3を一般化可能 |
| **N5** | GKSL realizability | CP・TP制約下で実現可能なNewton fanの分類 | 将来の分類問題 |

### N1（条件付き厳密定理候補）Operational Newton-fan theorem
各Riesz特徴 k が (a_k, z_k) から単項 a_k + z_k·s を寄与し、
$$\nu(s) = \min_k\big(a_k + z_k\,s\big)$$
が s の凹区分アフィン関数になる。§0の3点整列が証拠。

**pole-residue展開だけでは不十分であり、少なくとも次を宣言する必要がある:**
- 有限個の漸近的自己相似Riesz cluster
- cluster間の漸近分離、または重なりの制御
- rescaled lineshapeの一様可積分性
- pole collisionと中心移動の制御
- 特徴間の関数レベル相殺がないこと、または相殺を含む拡張則
- logarithmic correction および連続スペクトルの除外、または別扱い

これらを宣言しない「一般のlinear-in-Γ GKSL定理」は証明範囲を超える可能性が高い。

### N2（決定点）Interface non-identifiability
同一の 𝓛₀ と同一のuncut responseを持ちながら、異なる物理interfaceが
異なるfanを与える **matched pair** の構成。

**N1・N3・N4だけなら、既存のtropical geometry・正則値定理・漸近解析の再編と
見なされる余地がある。N2が物理的matched pairとして成立して初めて、
generator-only ontologyでは有限介入応答を分類できないことが示される。**

**リポジトリ内の最も近い既存資産:** Integrated Summary §9 の
**sector equivalence分裂**（A ∼_{𝓘_S} B, A ∼_{𝓘_T} B, A ≁_{𝓘_S∨𝓘_T} B；
Λ-model で Liouvillian spectrum・populations・total emission が全て一致し
ground-state coherenceのみが分離、identifiability rank 0→2）。これは
「第二のflagship現象」として既に認証されており、N2のmatched pair構成の
出発材料になる。ただしN2が要求するのは「同一uncut response かつ 異なるfan」
であり、既存の分裂結果より強い条件である点に注意する。

### N3（厳密定理候補）Face–codimension theorem
あるfaceを除去または保護する係数条件 c_F(θ)=0 の解集合を ℳ_F とすると、
正則点において
$$\boxed{\operatorname{codim}_{\mathbb R}\mathcal M_F = \operatorname{rank}_{\mathbb R} Dc_F}$$
余次元を決めるのは異常頂点の数ではなく、**消すべき独立なface係数の本数**である。

**既存証拠の再配置:**
- Gate G4 FAIL（`patternb_gksl_program/summaries/gates_summary.json`）:
  8パラメータ中 θ_c のみが破綻し、精密化後の閾値 **ε ≈ 3.664×10⁻⁵ rad**
  （`refined_pos_failure`/`refined_neg_failure`）、Sobol success fraction は
  半径1%で0.5%・2%で0%。これは rank Dc_F = 1 の実測値として読む
  （「異常次数1だから余次元1」ではなく「消すべきface係数が1本だから余次元1」）。
- Q2 kernel-alignment no-go（`q2_joint_only_selection_program/stageQ2S1_symbolic/
  docs/q2s1_closed_forms.json`, QG1 PASS）: single-sector保護は
  「det(D₂)特異＋核整列条件」という測度ゼロpuncture setでしか成立しない。
  Möbius二重差分が top元でのみ厳密ゼロ（`mobius_double_difference = 0`、
  他は −g₁, −g₂, g₁+g₂+γ_reg で非零）——face係数がsector格子のどこで
  消えうるかの代数的構造そのもの。

### N4（既存M3の一般化）Universal wall crossover
tubeは中心原理そのものではなく、**face-selection boundaryの有限-Γ thickening**
として再解釈する。generic faceとprotected faceの指数差を Δν、
generic係数の消失次数を m（c(θ) ∼ (δθ)^m）とすると、crossover条件
(δθ)^m Γ^{Δν} ∼ 1 から普遍変数は
$$\boxed{x = \delta\theta\,\Gamma^{\Delta\nu/m}}$$
既存の認証済み結果（`patternb_gksl_program/stageP5c_phasemap/docs/
p5c_crossover_verdict.json`, Gate M3 PASS）
$$x_\theta = \frac{|\delta\theta_c|\,\Gamma}{J}\approx 1.04$$
（δθ_c=10⁻⁶〜10⁻⁴の5点で collapse定数 1.0423, 1.0409, 1.0400, 1.0388, 1.0349、
相対ばらつき0.04〜0.29%；J∈{0.5,1,2}でのΓ_θ slope 実測 −1.0011〜−1.0019、
予測 −1.0）は、**m=1, Δν=1 の特殊例**として位置づけられる。

この再編により、pattern (a)・pattern (b)・tube・Schur blind predictor・
EP共スケーリングを同じfan構造へ接続できる。

### N5（将来の分類問題）GKSL realizability
CP・TP制約の下で実現可能なNewton fanを分類する。

---

## 4. 数学体系の閉性

| 軸 | 閉じる定理 | 既存の土台 |
|---|---|---|
| 汎関数軸（s方向） | N1: Newton-fan表現定理 | §0の h·w^{1/p} 計算、`lem:min-rule` |
| 周波数軸（ω方向） | sum-rule中立性による強制対形成 | `thm:sum-rule`, `cor:mobius-neutral`, `thm:area-balance`, `thm:main` |
| パラメータ軸 | N3: face–codimension則 | `prop:stability`, tube-calculus (codim ℳ_Γ = rank J_f) |
| 有限Γ軸 | N4: universal wall crossover | stageP5c Gate M3 |
| セクター束軸 | 既存の `thm:mobius-unique` | そのまま継承 |
| interface軸 | **N2: 非同定可能性（決定点）** | Integrated Summary §9 equivalence分裂 |

claim hierarchy（Definition→Exact→Conditional→Conjecture→Numerical phenomenon）と
Stop A–D の停止規律をそのまま継承する。

---

## 5. Stop D 差別化

- **Zeno narrowing** は単項 (0,1) の起源を説明するが、Möbius束をまたぐmin-plus構造、
  face係数のrank–codimension則、interface非同定可能性のいずれも導かない。
- **Fano干渉**は符号構造を与えるがΓ-grading則（傾き z）を与えない。
- **non-normal応答の増幅**は機構であって grading law ではない。
- **Newton polygon / tropical解析それ自体は新しくない。** 新規性は
  「interface・resource path・functional hierarchy・no-go・blind predictionの接続」にある。
  この点を曖昧にすると非エルミート物理の先行研究との重複として処理される。
- 正直な記載: `competitor_null_program` は現状 **smoke段階のみ**
  （G2 FAIL、μ≥2 process tensor / SU(d) latent-group拡張は
  `case_survives_smoke_pending_mu2` として未実行）。Zeno/Fano/non-normalとの
  定量的差別化は**未確立**である。

---

## 6. 検証Gate（優先度順）

| 優先度 | Gate | 目的 | 判定基準 |
|---:|---|---|---|
| 1 | **Physical matched-interface pair** | N2と中心命題を直接成立させる | 同一 𝓛₀、同一uncut response、異なるfan |
| 2 | Newton-fan theorem audit | N1の正確な適用範囲を固定する | 仮定・例外・log補正・cluster衝突を明記 |
| 3 | 第二の非EP GKSL族 | Candidate A・EP依存という反論を除く | blind predictorが**事前**予測に成功 |
| 4 | Face–codimension統合 | N3を確立しACCの撤回を完結させる | rank 1–6とcrossoverを同じ係数写像で説明 |
| 5 | Classical Markov export | 分野横断性を期待から結果へ変える | 同じ定理・certificateでmatched pairを構成 |
| 6 | Experimental pullback | 観測可能量へ接続する | Eu³⁺:Y₂SiO₅等でpeak/area指数とwallを予測 |

なお、既存の未着手Gate **M4R**（再較正可能性）と PARTIAL の **M2R**（真の境界位置）は、
ACC撤回により「中心定理の決定実験」という地位を失い、
**N3のrank測定（優先度4）の入力データ**という位置づけに変わる。

### Stop条件
次のいずれかが成立すれば、PRX中心理論としての再評価が必要になる。
- interfaceを変えても、物理的に実装可能なmatched pairではfan差が生じない
- fanの区分アフィン性が広いGKSL族でlog補正やcluster衝突により崩れ、安定な定理域を定められない
- blind predictorがresponse scan後のfitに依存し、事前予測として機能しない
- 古典系への輸出が既存tropical reductionと区別できない

これらは失敗ではなく、主張の適用範囲を決める情報である。ただし投稿誌の選択は変わる。

---

## 7. 投稿誌の位置づけ

### 7.1 現時点の評価
中心命題は有力な理論候補であり、完成したPRX主張ではない。不足しているのは
抽象度ではなく、次の三つの実証である。
1. 同一 𝓛₀ と同一uncut responseを持つ物理的matched interface pair
2. Candidate A や true EP に依存しない第二のGKSL族
3. 古典Markov族または別分野への同一blind certificateの輸出

### 7.2 PRLとして圧縮する場合
次の一つの結果へ集中する：
> 有限次元Markov応答のsector suppression lawはresource pathによって
> polyhedrallyに選択されるが、そのlawはuncut responseのみからは一般に復元できない。

matched-pair no-goと一つの強い物理witnessに絞る。

### 7.3 PRXとしての完成条件
以下を一つの体系として示す必要がある：Newton-fan表現定理 ／ interface非同定可能性定理 ／
finite-Γ wall crossover ／ blind prediction protocol ／ 複数量子族と古典族への適用 ／
実験座標へのpullback。**PRXに必要なのは現象の数ではなく、異なる現象を同じ法則で予測し、
反証条件まで与えられることである。**

---

## 8. 表現の規律

### 中心命題（短縮形）
> 観測されるsector応答則は無介入generatorだけでは決まらない。interfaceが応答の
> Newton多面体を定め、有限介入資源のscaling pathがそのfaceを選ぶ。その結果得られる
> 次数fanはuncut responseだけからは一般に復元できない。

### 中心命題（厳密形）
> 有限次元Markovian weak-probe系の正則な漸近領域において、sector intervention
> interfaceは応答有理関数のNewton supportを定め、介入資源とnative散逸の相対scaling ray
> は露出faceを選択する。これによりsector-resolved functional suppression orderは
> 区分アフィンfanを形成する。このfanは無介入generatorまたはuncut responseのみの
> 不変量ではないが、generator・interface・sector・resource protocolが与えられれば
> 有限のpolyhedral certificateから計算できる。

### 避けるべき表現
| 誤 | 理由・正しい言い方 |
|---|---|
| 「full generatorが同じなのにfanが違う」 | 介入generator族までfull generatorに含めるなら誤り。**無介入generator 𝓛₀ が同じ**と言う |
| 「fanは同定不能である」 | **uncut-only dataからの**非同定可能性に限定する |
| 「EITとATSは同一機構である」 | 同じfanは**操作的同値性**を意味するだけで機構の同一性ではない |
| 「Newton fan自体が新しい」 | 新規性はinterface・resource path・functional hierarchy・no-go・blind predictionの**接続**にある |
| 「異常次数は余次元に等しい」（ACC） | **撤回済み**（§1.1）。face係数のrank–codimension則（N3）を用いる |

---

## 9. 最優先方針

$$\boxed{\text{matched interface pair を最優先で完成させ、N2 を理論の決定点にする}}$$

PRXへの可能性は理論の名称や抽象度ではなく、この一組の物理的反例と、
それを複数系で予測できるblind certificateによって決まる。

---

## 10. 参照ファイル一覧

- `docs/theory_papers/RISEI_Spectral_Pairing_Theorems.tex` — thm:sum-rule,
  thm:area-balance, lem:min-rule, thm:main, prop:sufficient
- `docs/theory_papers/Generalized_RISEI_Theory.tex` — thm:mobius-unique,
  claim hierarchy, Stop A–D, def:valuation, def:protection-depth
- `RISEI_Discovered_Phenomena_Integrated_Summary_2026-07-23.tex` §9 —
  sector equivalence分裂（N2の出発材料）
- `latest_theory_program/summaries/` — ν^(p)=1−1/p 則（Gate G1 PASS）
- `patternb_gksl_program/summaries/gates_summary.json` — G3/G4/M1/M2R/M3/S0/F1
- `patternb_gksl_program/stageP5c_phasemap/docs/p5c_crossover_verdict.json` —
  x_θ collapse定数（1.0349〜1.0423）
- `q2_joint_only_selection_program/stageQ2S1_symbolic/docs/q2s1_closed_forms.json` —
  kernel-alignment no-go、Möbius二重差分≡0
- `patternb_gksl_program/common/coherence_block.py` — Schur閉形式 A=B=2J²
- `docs/plans/10_PRX_publication_strategy.md` — 型B路線との接続

### 近接分野（先行研究監査の対象）
Process tensor / operational quantum stochastic processes；
open quantum system identification and realization theory；
path-dependent multicritical scaling；
Newton polygon and tropical analysis of exceptional points；
tropical reduction of reaction networks；EIT–ATS mechanism discrimination.

本メモは判断材料であり、上記Gateのいずれを実行するかはユーザーの指示を待つ。
