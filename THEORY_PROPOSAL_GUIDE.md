# 新理論提案ガイド（AIエージェント向け作業基準）

**対象:** このリポジトリで新しい理論を提案・設計するAIエージェント（Claude等）
**最終更新:** 2026-07-25
**運用方針:** 理論提案のたびに §5〜§8 を追記・更新していく生きた文書とする。

---

## 0. このファイルの役割

新理論を提案するとき、エージェントは**まずこのファイルを読み**、以下を確認してから作業に入る。

1. どこに投稿する想定か（§1）
2. 何をもって「新理論」と認めるか（§2、§3）
3. 何を土台にしてよく、何と矛盾してはいけないか（§4）
4. 既に却下された方向・既存の競合論文はどれか（§6、§7）
5. どの形式で出力するか（§9）

**最重要原則:** このリポジトリで求めているのは「既存理論の再整理」ではなく、
**その理論でしか出てこない現象（理論固有現象）の発見**である。§3を提案の中心に置くこと。

---

## 1. 投稿先とフォーマット基準

### 1.1 第一想定：Physical Review X (PRX)

#### 公式上の位置づけ（2026-07-25確認）

Physical Review X (PRX) は、物理学および隣接分野を対象とする、**広範かつ高度に選択的な完全オープンアクセス誌**である。理論提案は、少なくとも次のいずれかに該当する水準を目標とする。

- 基礎的な理論的・実験的発見を与える。
- 急速に発展する分野でランドマークとなる結果を与える。
- 既存理解にパラダイム転換をもたらす。
- 複数の物理分野を結び、広い読者に影響する創造的かつ実質的な前進を与える。

単に「新しい定義を導入した」「既存計算を統一した」「一つの模型で珍しい挙動が出た」だけでは弱い。PRX候補としては、**新しい問い、一般原理、閉じた証明または強い検証、反証可能な予言**が一つの物語として結ばれている必要がある。

#### 記事種別・長さ・提出形式

- 想定記事種別は **Research Article** とする。
- Research Article には公式の語数上限はない。ただし、長さは科学的内容によって正当化されなければならない。
- 固定された図表数上限は公式著者案内に明記されていない。各図は主張に不可欠で、本文中で参照され、単独で理解できるcaptionを持つこと。
- 初回投稿はPDFで査読可能だが、採択後の処理と数式抽出を考え、**REVTeXによるLaTeX原稿**を標準とする。
- 本文は American English で作成する。
- PRXでは参考文献に論文タイトルを含める。
- **250語以内の非専門家向け Popular Summary** が必要である。
- APSの現行方針に従い、**Data Availability Statement** を含める。数値結果を主要根拠とする場合は、コード、入力、乱数seed、主要出力、再現手順の公開方針も明記する。
- PRXは完全オープンアクセス誌であり、採択時には原則としてAPCの支払い責任が生じる。投稿前に所属機関・研究費の扱いを確認する。

#### 読者と構成

導入、議論、結論は、量子光学・開放系・数理物理の専門外の物理学者にも、次の4点が伝わるように書く。

1. 何が未解決だったのか。
2. なぜ既存理論では解けなかったのか。
3. 今回導入した概念または定理が何を可能にしたのか。
4. その結果が他分野の問い・実験・設計原理をどう変えるのか。

推奨構成:

1. Title / Abstract
2. Introduction and one-paragraph novelty statement
3. Physical question and failure of existing descriptions
4. Definitions and assumptions
5. Main theorem(s) or central phenomenon
6. Minimal witness and non-reducibility audit
7. Generality, robustness, and falsification tests
8. Experimental or computational realization
9. Discussion, limitations, and broader consequences
10. Methods / Appendices
11. Data Availability Statement
12. References with titles

Supplemental Materialは補助的導出、追加図、パラメータ表、再現情報に使う。**中心命題の理解または成立に不可欠な仮定・証明・反例をSupplemental Materialだけに置かない。**

#### このリポジトリでのPRX判定ゲート

以下のうち一つでも満たせない場合、PRX候補とは呼ばず、探索中・PRL圧縮候補・専門誌候補のいずれかに分類する。

- [ ] **Novelty:** 先行研究との差分を一段落で言い切れ、既知機構への還元監査を通過している。
- [ ] **Fundamental importance:** 個別材料・単一模型を超える一般則、または複数分野に効く新しい問いを提示する。
- [ ] **Theoretical closure:** 定義、仮定、主定理、反例、適用限界が区別され、主張の論理が閉じている。
- [ ] **Predictive surplus:** 既知結果の再説明だけでなく、事前に計算できる新しい予測、設計則、分類、またはno-goを与える。
- [ ] **Falsifiability:** 棄却条件、null test、対照模型、または実験・数値で区別可能なwitnessがある。
- [ ] **Robustness:** 数値精度、摂動、有限サイズ、有限時間、観測窓、極限順序に対する監査がある。
- [ ] **Broad readability:** Popular Summaryと導入だけで、専門外の物理学者が意義を説明できる。
- [ ] **Reproducibility:** 主結果が独立実装または解析計算でクロスチェックされ、再現用資産が保存されている。

#### 公式情報源

- APS, *About Physical Review X*（scope、selectivity、acceptance criteria）
- APS, *Physical Review X: Information for Authors*（article types、audience、format）
- APS, *Length Limits and Guidelines for Physical Review Article Types*（Research Articleはno length limit）
- APS, *Web Submission Guidelines for Physical Review*（Popular Summaryは250語以内）
- APS, *Editorial Policies and Practices*（Data Availability Statement等）

> 公式要件は更新されうるため、実際の投稿直前にAPSのPRX著者ページを再確認すること。

### 1.2 代替投稿先（PRXに届かない場合の降格先）

| 優先 | 投稿先 | 適する内容 | 要求される厳密性 |
|---|---|---|---|
| 1（本命） | **PRX** | 分野横断的な基礎的発見・ランドマーク級の成果 | §1.1 の判定ゲート8項目 |
| 2 | **PRX Quantum** | 量子情報・量子センシング中心の結果 | PRXと同等 |
| 3 | **PRL** | 単一の鋭い法則・no-go | 高（ただし短い） |
| 4 | **PRA / PRB** | 開放系・非Hermitian・量子光学の専門的完成 | 中〜高 |

**降格を検討する条件**（出典：`docs/source-material/RISEI_Branch_Complete_Tube_Calculus_PRX_Roadmap_2026-07-22.md` §11）

以下のいずれかに該当する場合、PRXではなく投稿先の変更または論文分割を検討する。
**該当しても成果が失敗になるわけではない** — 適切な誌へ振り分ける判断材料である。

- 一般化が単なる数値branch追加に留まり、定理がregular branchのみ
- experimental pullbackができず、抽象parameterのまま
- held-out predictionが弱い
- 既存制御理論またはZeno理論の標準計算で同じ出力が得られる
- 対象現象以外へのpredictive surplusがない
- full physical modelでは現象が観測不能

**振り分けの目安:**

| 状況 | 行き先 |
|---|---|
| 鋭い一法則にまとまる | PRL |
| 量子情報・量子センシングが中心 | PRX Quantum |
| 開放系・非Hermitian・量子光学の専門的完成 | PRA / PRB |

> **注:** 本リポジトリの対象は有限次元Markovian開放量子系（EIT/量子光学プラットフォーム、NV・SnV・Eu:YSO等）である。
> PRD（素粒子・場・重力）およびJHEPは領域が異なるため候補から外す。

---

## 2. 提案する理論の「型」

提案時に、以下のどれに当たるかを必ず明示する。

- **(A) 現象論的理論** — 新しい観測可能現象を予言する
- **(B) 数学的定理型** — 必要十分条件・no-go定理・分類定理を与える
- **(C) 枠組み型** — 既存理論群を包含し、新しい不変量や整合条件を定義する
- **(D) 統合型** — 上記の複合（このリポジトリの既存文書は概ねこれ）

あわせて明示する項目:

- 対象系（有限次元／無限次元、閉じた系／開放系、古典／量子）
- 対象スケール・エネルギー領域
- 想定読者（量子情報、統計力学、数理物理、幾何 …）

---

## 3. 【中核】理論固有現象（Theory-Specific Phenomenon）

**このセクションが埋まらない提案は、提案として成立しない。**

### 3.1 必須記述項目

1. **固有現象の定義**
   その理論の構造からのみ生じる現象を、1つのboxed命題として書く。
   （例：既存文書のDCITにおける "dilation frustration"）

2. **非還元性の証明または論拠**
   以下のすべてについて「この現象は既知の何々に還元されない」ことを論じる。
   - 既存の一般的機構（Zeno効果、例外点、FCS、unravelling依存性、群同期、系同定 …）
   - Frozen-Theories 内の確定済み理論（§4）
   - §7 の競合論文の結果

   > **還元されてしまった場合は、その事実を記録して §6 の「却下リスト」に追加する。**
   > 失敗の記録もこのリポジトリの資産である。

3. **観測可能量（observable signature）**
   - どの物理量に、どういう形（発散、不連続、閾値、位相、順序依存性 …）で現れるか
   - 検出手段：実験／数値計算／解析的判定のいずれか、そのコスト
   - 有限サイズ・有限精度でも見えるか

4. **反証条件**
   何が観測されたらこの理論は棄却されるか。

5. **既存理論との一致領域**
   ある極限で既知の結果を再現することを示す（sanity check）。

### 3.2 固有性の強さの階層

提案時に自己評価すること。

| レベル | 内容 | PRX適合度 |
|---|---|---|
| L0 | 既存理論の言い換え | 不可 |
| L1 | 既存現象の新しい説明 | 弱い |
| L2 | 既存枠組みでは自然に出ないが、原理的には導出可能 | 要検討 |
| L3 | 新しい構造からのみ生じ、既存機構に還元されないことを示せる | **目標** |
| L4 | L3 かつ定量的予言があり、既存の実験・数値データで検証可能 | 最良 |

---

## 4. 既存理論との関係

### 4.1 土台として使ってよい確定済み理論（`Frozen-Theories/`）

| ファイル | 内容 | 適用範囲（凍結された前提） | 再利用可能な結果 |
|---|---|---|---|
| `Generalized_RISEI_Theory_EndToEnd_Certified_2026-07-23.tex` | 物理的介入protocol、full-minus-protocol応答、subset-Möbius不可約成分、操作順序、response functional、protected Riesz cluster、source/readout選択幾何、有限資源、極限順序を統合した一般化RISEI | 有限次元・time-local GKSL。介入後も瞬間generatorがGKSL admissible。比較間で初期状態、probe、readout、観測窓、測定規約、正規化を固定。Schur–Zeno結果にはsemisimpleなresponse-relevant protected clusterとbounded fast resolventが必要。functional、許容摂動クラス、limit protocolを明示する。 | Möbius分解の一意性、Riesz cluster invariance、Schur–Zeno expansion、response-relevant strong dissipatorが可逆な場合のresolvent suppression、選択集合の局所codimension = 実Jacobian rank、stationary linear responseへの埋め込み、`R_π^(n)`, `Ω_T^(n)`, `Ξ_{S,T}^(n)`, `ν_Φ`, `Σ_π^(n)`, `Λ`, `C_req` の定義。Pattern (b) の任意GKSL普遍性は再利用不可。 |
| `SMRT_two_scale_polyhedral_theorem_integrated_2026-07-24 (1).tex` | sectorを切ったcounterfactualとfull responseとの差であるmaster sector-resolved responseを、exact zero・algebraic suppression・protected survivalへ分類するSMRT。二尺度・scaling-path依存を扱うpolyhedral拡張を含む。 | 有限次元・Markovian・weak-probe/linear response。応答が有限次元のrational transferとして表され、source/readoutと比較規約が固定されること。強散逸族 `A_Γ(z)=ΓD+B(z)` では、どのrateをscaleするかを物理入力として固定する。protected theoremにはsemisimple kernelとprotected blockの可逆性が必要。二尺度polyhedral結果は凍結文書に明記されたscaling pathと正則性条件の範囲だけで使う。 | full-minus-cut差分のdoubling realization、有限個のKrylov/Cayley–Hamilton momentsによるexact-zero certificate、dissipative moment hierarchyと抑制次数、singular dissipator上のprotected transfer、`ν∈{∞, positive finite, 0}` の排他的三分類、有限停止decision algorithm、exact arithmeticを用いる認証方針。polyhedral face/fanとpath-dependent valuationに関する結果は、元定理の仮定をそのまま継承する場合のみ再利用する。 |
| `EIT_no_go_go_theory_v6_2_English.tex` | 任意材料の特定configurationについて、dark-state rank、Lindblad stationary dark state、Schur-complement susceptibility、sector-resolved EIT no-go/goを判定する理論 | 有限次元、time-independent Markovian GKSL、stationary rotating frame、weak probe、unique steady stateまたはtrace-zero部分空間上のwell-defined group inverse。分類対象は材料名ではなく、準位、偏光、場、温度、observable、target sectorを含むconfiguration。非Markov浴、strong-probe saturation、伝搬支配のcollective effectは範囲外。 | `dim ker Ω = N_g-rank Ω`、pure stationary Lindblad stateの必要十分条件、exact Schur-complement response、`δχ_S = χ_full-χ_cut^(S)`、regular scalar caseの `δχ_S=0 ⇔ K_12K_21=0`、Krylov exact-zero theorem、first nonzero momentによるsuppression order、singular dampingのprotected channel、symmetry audit、Rb/NV/SiV/SnVのsanity-check分類。 |

#### 再利用時の規則

1. **定理名だけを再利用しない。** 仮定、比較規約、source/readout、functional、観測窓、limit protocolを一緒に移植する。
2. 既存の数値結果を使う場合、元のparameter file、単位、rate convention、precision、fit window、乱数seed、commit hashを記録する。
3. Frozen theoryの結論を新理論の新規性として数えない。新理論は、凍結結果から何を追加で予測・禁止・分類するかを示す。
4. `Exact / Conditional / Conjecture / Numerical phenomenon / Model-specific observation` のstatusを維持する。statusの昇格には新しい証明または認証が必要。

### 4.2 抵触してはいけないno-go定理・制約

以下は、新理論が黙って破ってはいけない「赤線」である。回避する場合は、外した仮定と新しい整合条件を明示する。

1. **GKSL/CPTP physicality**  
   RISEIの物理的介入は、原則としてgenerator全体をGKSL admissibleに保つ変更である。任意の行列要素の削除を、そのまま実験的介入と同一視しない。

2. **Fixed comparison class**  
   full、cut、intervened protocolを比較するとき、初期状態、probe、readout、観測窓、operator ordering、measurement scheme、normalizationを固定する。変更する場合は、それ自体をprotocol dataとして明示する。

3. **no-go対象の取り違え禁止**  
   EIT/SMRTのno-go対象は、全応答の零点ではなく、指定sectorによる差分 `δχ_S` またはmaster responseである。`χ_full=0` は理想EITのgo signatureになりうるため、no-go判定に使わない。

4. **有限点のnumerical zeroはexact zeroではない**  
   exact all-frequency zeroは、symbolic identity、有限Krylov moment certificate、adjugate identity、対称性の完全監査などで証明する。浮動小数点samplingだけでは証明済みと書かない。

5. **full-rank strong damping no-go**  
   response-relevant部分空間上でscaled dissipator `D` が可逆で逆行列が一様有界なら、固定周波数窓のbounded responseは少なくとも `O(Γ^{-1})` に抑制される。追加のsingular scalingなしに `O(1)` protected responseを主張しない。

6. **protected responseの必要条件**  
   `ker D ≠ {0}` だけでは不十分。semisimpleなresponse-relevant protected Riesz subspace、非零のprojected source/readout、可逆なprotected block、非零のprotected transferが必要である。endpoint overlapだけで保護を判定しない。

7. **fixed kernel lifting no-go**  
   固定した `ε>0` によりresponse-relevant kernelが持ち上がり、`D_ε` が可逆かつbounded inverseを持つなら、`Γ→∞` でexact-kernel型のprotected asymptotic mechanismは消える。finite-window crossoverをasymptotic phaseと呼ばない。

8. **Pattern (b) の任意GKSL普遍性は禁止**  
   Pattern (b) は、response-relevant protected kernel、Schur–Zeno coupling、selection geometry、非零residue、許容摂動、固定されたlimit protocol等を必要とする条件付き現象である。

9. **universal codimension-oneは禁止**  
   observable-selection setの局所codimensionは、active real constraint mapのJacobian rankで決まる。complex scalar constraintは一般にreal codimension twoになりうる。

10. **極限交換禁止**  
    `Γ→∞`, kernel lifting `ε→0`, grid/domain size、continuum、thermodynamic limitの順序を黙って交換しない。異なるlimit protocolから得た結果を同一視しない。

11. **symmetry zeroの完全監査**  
    symmetry-protected zeroを主張するときは、Hamiltonian、全jump operator、steady state、source、readout、control polarizationを同じprojectorがreduceすることを確認する。一項でも破ればexact zeroではなくperturbative suppressionとして扱う。

12. **rate convention・次元整合性**  
    population relaxation rateとoptical-coherence damping rateを混同しない。例として対称orbital hoppingでは、population imbalance rate `Γ_XY=2k` に対し各optical coherenceのdampingは `k/2=Γ_XY/4` となる。すべての無次元化と単位変換を自動テストする。

13. **EITとAutler–Townes splittingの混同禁止**  
    transparency dipだけではEITを同定できない。ground-coherence依存、control-power scaling、pole/residue、two-photon linewidth、full-minus-cut差分を確認する。

14. **熱力学への拡張時の制約**  
    GKSL形式だけから熱力学第二法則を自動的に結論しない。bath、Hamiltonian、温度、detailed balanceまたは採用するresource-theoretic assumptionsを明示し、entropy production、passivity、energy bookkeepingを独立に検証する。

### 4.3 適用範囲外（凍結の外側）

次の領域は、確定済み理論が一般定理として保証していない。新理論の探索空間になりうるが、Frozen-Theoriesの結論をそのまま外挿してはいけない。

- genuinely non-Markovian memory kernel、colored noise、initial system–environment correlation
- infinite-dimensional Hilbert/Liouville space、essential spectrum、連続体bathを明示的に残す模型
- generic many-body・thermodynamic-limit scaling、相転移を伴う極限
- strong-probe、nonlinear response、saturation、multi-photon nonperturbative regime
- gain medium、unstable generator、physical frequency window内のpole crossing
- nonsemisimple zero eigenvalue、Jordan block、Puiseux/fractional scalingが必要な場合
- scaling対象が途中で変わる多parameter path、ランダムpath、adaptive path（凍結されたpolyhedral theoremの範囲外の場合）
- ideal algebraic cutの実験実装可能性、異なるimplementation family間の同値性
- ensemble propagation、optical depth、disorder averaging、detector noiseを含む実験可視性
- finite-grid approximate kernelからcontinuum spectrumへの外挿
- ergotropy、Fisher information、entropy production等の非線形functional。RISEIの差分記法は移植できても、滑らかさ・passivity ordering・thermodynamic consistencyは別途証明が必要
- unrestricted process tensor、quantum comb、causal modelへの埋め込み。表現可能性とRISEI固有の分類・予測能力は別問題として監査する

### 4.4 仮定変更の予算

**各提案は、Frozen-Theoriesの主要仮定のうち、原則として一つだけを外す。**

- 追加で外してよいのは、中心仮定と**数学的に不可分な補助仮定一つまで**とする。
- 二つの仮定を外す場合、**それぞれが現象に必要であることをablation testで示す**。
- **三つ以上の独立した仮定を同時に外す提案は採用しない。**

仮定を外す前に、以下を記述する。

1. 外す仮定
2. **外さず維持する仮定**
3. 代替する数学的構造
4. 失効する既存定理
5. 継承できる既存定理
6. 元の理論を回収する極限
7. **仮定変更がなければ現象が消えることを示すcontrol**

> **新規性は「仮定を多く外したこと」では評価しない。**
> 最小の仮定変更で、既存理論に還元されない現象、分類、no-go、
> または resource-bounded predictive surplus を得た提案を優先する。

---

## 5. 記法・用語の統一

複数文書を後で統合できるよう、記号を揃える。
出典：`Frozen-Theories/` の3文書 + `docs/source-material/Revised_Generalized_RISEI_Theory_2026-07-21.pdf` 付録A。

### 5.1 共通記号（3理論で一致 — 安全に使える）

| 記号 | 意味 | 出典 |
|---|---|---|
| `Γ` | 支配的な散逸スケール／漸近スケール | RISEI・SMRT・EIT すべてで一致 |
| `D` | fast damping-shape operator（`A_Γ(z)=ΓD+B(z)` の `D`） | SMRT `D_full`・EIT `D` |
| `B(z)` | 遅い／周波数依存ブロック | SMRT `B_full(z)` |
| `S, T, U` | 操作的sectorまたはsector部分集合 | RISEI・SMRT |
| `𝒢_S` | sector選択的な GKSL-admissible 介入生成子 | RISEI `𝒢_{S_j}`・SMRT `𝒢_S` |
| `c` / `p†` | probe source ／ readout covector | SMRT・EIT（RISEIは `f` に吸収） |
| `κ` | 介入強度 | RISEI `κ_j(t)`・SMRT `κ=κ₀Γ^q` |

### 5.2 理論別の主要記号

**Generalized RISEI**（`Generalized_RISEI_Theory_EndToEnd_Certified_2026-07-23.tex` §Notation、Revised版付録A）

| 記号 | 意味 |
|---|---|
| `π` | sector・強度・時間窓を含む順序付き介入protocol |
| `𝒰_π` | protocol依存propagator |
| `C_π^(n)` | connected n-time cumulant |
| `R_π^(n)` | full-minus-protocol 介入応答 |
| `Ω_T^(n)` | subset-Möbius 不可約応答 |
| `Ξ_{S,T}^(n)` | order-irreducible 応答 |
| `Φ` | 応答の特徴を選ぶ functional |
| `ν_Φ` | functional依存の漸近valuation |
| `N_∞, N_1` | supremum / 絶対積分 応答ノルム |
| `Σ_π^(n)` | 多成分scaling signature |
| `k_min^(n,Φ)` | observable・feature依存の protection depth |
| `𝒞[π]` / `𝒞_req` | protocol資源コスト ／ 最小同定コスト |
| `P_𝒞` | response-relevant spectral cluster への contour Riesz projector |
| `K_Z` | leading Schur–Zeno 実効結合 |
| `f` / `J_f` | realified 選択写像 ／ 実選択Jacobian `D_θ f` |
| `ℳ_Γ` | 局所選択多様体 `f^{-1}(0)` |
| `𝒜` | admissible perturbation class |
| `Λ` | 順序付き limit protocol |
| `ℰ_full` | 有限Γ response-defect ベクトル |
| `Q_tube` | cluster制限 Schur derivative Gram行列 |
| `𝒯_{ε,Γ}` | 有限Γ operational response tube |
| `z_loss` / `z_jet` | 無次元 slow-loss/protection比 ／ blind projected crossover座標 |
| `q_*` | 有限窓 Schur self-energy 指数 |
| `κ_eff` / `α_eff` | 応答重み付き Schur保護係数 ／ projected slow-loss微分 |
| `Δ_prot` | Schur誘起 cluster保護スケール |
| `C_cancel` | Möbius cancellation condition number |
| `Cert` | end-to-end 有限数値証明書 |

**SMRT (Sector-Mediated Response Theory)**（notation節なし、本文から抽出）

| 記号 | 意味 |
|---|---|
| `𝒱_full ≅ ℂ^{N_full}` | full response space |
| `A_{full,Γ}(z) = ΓD_full + B_full(z)` | native response family |
| `𝔈 = (A_{full,Γ}, c_full, p_full, K)` | experiment specification |
| `𝔓 = (𝒢_S, κ₀, q)` | path specification |
| `K ⋐ Ω` | 観測窓（`Ω` は周波数領域） |
| `q` | scaling path 指数（`κ = κ₀Γ^q`） |
| `ℛ_S^op` / `ℛ_{S,Γ}^ideal` | operational ／ ideal master sector-resolved response |
| `ν_S(q;κ₀)` | valuation。`ν ∈ {∞} ∪ (0,∞) ∪ {0}` の排他的三分類 |
| `𝔉` | exact function field（決定可能な同一性判定を持つ） |

**EIT no-go/go**（`EIT_no_go_go_theory_v6_2_English.tex` 付録A）

| 記号 | 意味 |
|---|---|
| `ℋ_g, ℋ_e` | 下位／励起 manifold |
| `Ω` | instantaneous optical coupling map（`Ω_c`: control Rabi） |
| `C` | dipole coupling vector 行列 |
| `A(z)` | optical-coherence 生成子 |
| `G = A^{-1}` | resolvent / Green演算子 |
| `K_ab` | 非対角 coherent-response kernel |
| `S_a` / `S_g = G_g - CA^{-1}B` | 対角 optical response ／ Schur complement |
| `M_n = p†X^nν` | resolvent moment |
| `Q` | reducing symmetry operator |
| `P = Proj(ker D)` | protected-subspace projector |
| `γ_g` | 複素 lower-coherence decay/detuning |
| `β = \|Ω_c\|²/4` | control intensity parameter |
| `Ξ` | 正規化 full local probe response |
| `χ_full` / `χ_cut^(𝕊)` / `δχ_𝕊` | full応答 ／ sector切断counterfactual ／ 差分 `χ_full - χ_cut^(𝕊)` |
| `ν = D^{-1}c` | moment symbol |
| `C_abs` | 相対吸収コントラスト |

### 5.3 ⚠️ 衝突している記号（新理論で無修飾に使わない）

**同じ文字が理論ごとに別物を指す。** 新提案でこれらを使う場合、**必ず添字か修飾を付けて出典を明示する**こと。

| 記号 | RISEI | SMRT | EIT | 深刻度 |
|---|---|---|---|---|
| **`Ω`** | subset-Möbius不可約応答 `Ω_T^(n)` | 周波数領域（`z ∈ Ω`） | optical coupling map | **最悪。3つとも別物** |
| **`K`** | Schur–Zeno結合 `K_Z` | 観測窓 `K ⋐ Ω` | coherent-response kernel `K_ab` | **高。3つとも別物** |
| **`Q`** | tube Gram行列 `Q_tube`／補spectral projector | — | reducing symmetry operator | **高** |
| **`Ξ`** | order-irreducible応答 `Ξ_{S,T}^(n)` | — | 正規化full probe response | 高 |
| **`ν`** | valuation `ν_Φ` | valuation `ν_S`（**RISEIと整合**） | moment symbol `ν = D^{-1}c` | 中（EITのみ別物） |
| **`C`** | cumulant `C_π^(n)`／コスト `𝒞[π]` | — | dipole coupling行列 | 中 |
| **`M`** | 選択多様体 `ℳ_Γ` | — | resolvent moment `M_n` | 中 |
| **`P`** | Riesz projector `P_𝒞`／puncture集合 `𝒫` | path spec `𝔓` | protected projector `P`（**RISEIと整合**） | 中 |
| **`A`** | admissible perturbation class `𝒜` | response family `A_{full,Γ}` | 生成子 `A(z)`（**SMRTと整合**） | 中 |
| **`G`** | 介入生成子 `𝒢_S`（**SMRTと整合**） | cut生成子 `𝒢_S` | resolvent `G = A^{-1}` | 中 |
| **`S`** | sector | sector | 対角応答 `S_a`／Schur補 `S_g` | 中 |
| **`z`** | 無次元座標 `z_loss`, `z_jet` | 複素周波数 | 複素周波数 | **中〜高。要注意** |
| **`q`** | Schur self-energy指数 `q_*` | scaling path指数 | — | 低（どちらも指数） |

**RISEI内部の重複:** Revised版付録Aで `P` が「protected spectral projector」と「puncture集合」の両方に割り当てられている。新提案では puncture を `𝒫_punc` 等に改名して使うこと。

**`D` の三重衝突（最も事故りやすい）:** 凍結理論では `D` = fast damping-shape operator（`A_Γ(z)=ΓD+B(z)`）。
一方 `docs/context-pack.md` §6 の**競合理論族の資源予算では `D` = hidden dimension**、`D_M` = memory Hilbert dimension。
提案文書で両方を扱う場合、散逸演算子側を `D_damp`、次元側を `D_hidden` と明示的に書き分けること。

### 5.4 規約

- **新しい概念には英語名と日本語名を両方与える**（例：dilation frustration ／ 共通実装フラストレーション）
- **略称は初出時に必ず展開する**（下表）
- **§5.3 の衝突記号を無修飾で使わない。** 使う場合は `Ω^{RISEI}_T` のように理論を明示するか、新しい文字を割り当てる
- 新しい記号を導入したら §5.2 に追記し、衝突が生じたら §5.3 を更新する

| 略称 | 正式名称 |
|---|---|
| RISEI | *要確認* — 凍結文書内に展開なし。所有者確認が必要 |
| SMRT | Sector-Mediated Response Theory |
| EIT | Electromagnetically Induced Transparency |
| ATS | Autler–Townes Splitting |
| CPT | Coherent Population Trapping |
| DCIT | Dilation-Consistent Intervention Theory（開放系介入の共通dilation整合性理論。草案段階） |
| GKSL | Gorini–Kossakowski–Sudarshan–Lindblad |
| CPTP | Completely Positive Trace Preserving |
| FCS | Full Counting Statistics |
| EP | Exceptional Point |
| QFI | Quantum Fisher Information |
| HMM | Hidden Markov Model |
| MPO | Matrix Product Operator |
| SNR | Signal-to-Noise Ratio |

---

## 6. 探索対象と却下リスト

### 6.1 現在の関心方向・空白地帯（優先度順）

既存理論が扱っていない領域。**壊す仮定は §4.4 の予算に従い、原則として一つ。**

| 優先度 | 空白地帯 | 壊す仮定 | 狙う現象・問い |
|---|---|---|---|
| **P0** | **Interface realizability** | ideal cut primacy | 複数の介入counterfactualが同一dilation/interface上で共存できる条件 |
| **P0** | **Resource-bounded mechanism separation** | unrestricted representation criterion | bounded competitorでは分離不能な最小protocol・functional・shots |
| P1 | **Multiparameter scaling geometry** | fixed scaling path | physical resource pathによるresponse law・face・class選択 |
| P1 | **Exact-to-approximate kernel crossover** | exact protected kernel | 有限窓保護と真の漸近抑制を分けるdouble-scaling law |
| P1 | **Nonlinear functional hierarchy** | linear response functional | mean/energyでは消え、work/QFI/noiseでのみ現れる不可約機構 |
| P2 | **Nonsemisimple protected geometry** | semisimple kernel | fractional valuation、Jordan-sensitive response class |
| P2 | **Bounded-memory extension** | time-local Markovity | 有限memoryで初めて生じるprotocol-exclusive witness |
| P3 | **Strong-probe extension** | weak-probe approximation | response orderによって初めて可視化されるsector |
| 翻訳層 | **Experimental visibility** | ideal detector / local response | SNR、propagation、ensemble averaging下で残るobservable signature |

**P0 の2件は §6.3 の未解決項目1（Resource-bounded same-data gap）および §11 の Priority 1 production へ直結する。**

> **【2026-07-25 文献監査による制約】** `docs/literature-audit-report.md` / `-addendum.md`（計56件）より。
> P0の2件はいずれも、**現在の素朴な表現では新規性を主張できない**ことが判明している。
>
> **P0-1 Interface realizability** — 「共通dilationが存在しない」だけでは非自明にならない
> （無制限のcontrol registerと直和ancillaを許せば block-control で常に構成できる）。
> **C-JOINT / I-JOINT / P-PROG / D-SHARED / R-BOUND のどれを問うのかを凍結すること**（`context-pack.md` §6.2.2）。
> 前2者は既知の channel/instrument compatibility へ還元される可能性が高い。
>
> **P0-2 Resource-bounded mechanism separation** — 「低depthで一致し高depthで分裂する」だけでは不十分
> （一般位置の有限HMMは有限長word確率からminimal realizationを復元できる：Huang et al. 2016）。
> **cancellation-protected / rank-deficient な例外集合における、凍結資源内のlower bound** として定式化する必要がある。
>
> **【2026-07-25 確定】P0 の証明書仕様は `docs/p0-certificate-spec.md` に分離した。**
> P0 は単一の数値目標ではなく、**族ごとの証明書のベクトル値判定**である
> （族D: Hankel rank `>6` ／ 族A: `dim K > (d·D_hidden)²` ／ 族E: OSR `>36` ／ QHMM: 定義依存 ／ 同期: order `>4`）。
> 各証明書は**入れ子**でなければならない — calibration側で競合の**存在**を示し、full側で容量超過を示す。
> **`P0-D の達成 ≠ P0 の達成`。** 実行順序も同ファイル §3。
>
> **維持できない表現**（`literature-audit-report.md` §4.1）:
> 「multi-time responseはsingle-time responseから分からない」／「pairwise dataが一致してもtriple dataが異なる」／
> 「hidden ancillaを入れれば説明できるが大きい（最小次元の証明なし）」／「process tensorなら表現できるが非効率（下界なし）」／
> 「pairwise group synchronizationでは説明できない（higher-order未監査）」

### 6.2 現在の探索対象外

以下は §4.3 の適用範囲外のうち、**当面は探索しない**と決めた領域。
§4.3（凍結が保証しない領域）とは区別する — こちらは「扱えないから外す」ではなく「今は狙わないから外す」。

- unrestricted infinite-dimensional continuum
- generic many-body / thermodynamic-limit theory
- gain medium または unstable generator
- continuum spectrum を finite-grid だけから推定する問題
- unrestricted process tensor への表現不能性
- non-Markovity、strong nonlinearity、many-body極限を**同時に**導入する提案（§4.4 の予算違反）

### 6.3 未解決の異常・矛盾

> **前提：現時点で確定した理論間矛盾はない。** 以下は、既存理論のどれが支配するか未決着である境界、
> 数値現象と一般証明の間の不一致、有限資源下での predictive-surplus 候補である。

| 項目 | 現状 | 次の最短検証 |
|---|---|---|
| **Resource-bounded same-data gap** | 単純な三者応答はreachabilityへ還元された。しかしpath support・path count・低次mixed Krylov momentsを一致させたcancellation-protected ternary pairは未検証 | 競合6族を予算固定し、depth≤2をmatched、depth3をheld-out witnessとして逆設計 |
| **有限gap exact zeroと漸近zeroの差** | 数値的machine zeroはあるが、有限gapでのfull-Liouvillian対称性証明がない。一般に証明されているのは漸近抑制のみ | full Liouvillianと候補superoperatorのcommutatorをSymPyでexact判定 |
| Exact / approximate kernel crossover | 裸の `Γε/γ₀` collapseは失敗。projected slow-loss jetは凍結模型で成功したが、一般クラスの十分条件は未証明 | 2つ以上の新architectureでblind jet prediction |
| Calibration redundancy boundary | calibration数を増やしても誤差が単調に減らず、`ρ=1.5` で突然EXACTになる例がある。group synchronizationは再現するが境界定理がない | observability Gram spectrumからPREDICT/ABSTAIN境界を事前予測 |

- **RISEI固有現象探索の最短起点は1番目**（§6.1 の P0-2 に対応、Priority 1 production へ直結）
- **最短の数学的定理プロジェクトは2番目**（新理論に直結しなくても、exact/asymptoticの論理的不整合を短距離で決着できる）

### 6.4 却下・保留になったアイデア（再提案禁止）

出典：`docs/source-material/RISEI_Unique_Phenomena_Computation_Summary_and_Search_Strategy_2026-07-23.tex`（競合理論監査、2026-07-23完了）。

**列の意味:**
- **還元の強さ** — `早期kill`（smoke段階で死亡）／`production後`／`最終監査`（長く生き延びた＝情報量が多い）
- **残る資産** — 固有性は失われたが、計算・実験設計・方法論として再利用できるもの。**空欄でない候補は §6.5 も参照**

| アイデア | 還元先 | 還元の強さ | 残る資産 | 判定日 |
|---|---|---|---|---|
| Response–Mechanism Contextuality（reduced sector gluing obstruction） | shared-ancilla enlargement（共有ancillaを含む単一のcontext-independent additive GKSL模型から生成したデータ） | **早期kill** | なし（negative controlとして保存） | 2026-07-23 |
| 平均に盲目な protocol-order fluctuation（二次累積量の順序依存分裂） | tilted-GKSL / FCS で最大誤差 \(1.84\times10^{-8}\) 以内に再現 | **早期kill** | 現象自体は頑健（10%摂動500例で符号保持率100%）。FCS内の例として有効 | 2026-07-23 |
| Relative-gauge splitting（exact witness \(\Delta K_2=2\ell_Y(G-I)r_X\) 自体） | switched GKSL + FCS の代数から導出可能 | production後 | **exact式** `ΔK_2=2ℓ_Y(G−I)r_X`（write/relative-defect/read の三因子分解）と明示的消失条件 | 2026-07-23 |
| Continuous quantum gauge / tree calibration atlas（\(SU(d)\) scaling production） | （非還元性未確立）tree calibrationでの予測圧縮則が破綻 | production FAIL | **`K≥q` は必要条件だが十分条件でない**という否定的知見。破綻要因の分類（local rank不足・非線形branch・tree伝播誤差・global chart inconsistency） | 2026-07-23 |
| Held-out quotient predictor（observational stabilizerによる quotient class） | compact-group latent-frame estimatorと目的関数が完全一致（残差0） | **最終監査** | **quotient class** `[P_i]=P_iH_i`。「内部chartの非一意性 ⇏ 予測の非一意性」という方法論 | 2026-07-23 |
| Global cycle-consistent quotient atlas（cycle threshold / predict-or-abstain） | compact-group synchronization / 構造化系同定と予測・棄却判定が完全一致 | **最終監査** | **predict-or-abstain certificate**（点推定を強制せずABSTAINを返す安全機構）。cycle冗長度1.5での予測可能性境界 | 2026-07-23 |
| **語領域受動性障害（WPOT／提案23、次元自由受動排除 DFPE）** | **還元ではなく反証。** 受動実現自身が主張を破る（400/400試行） | **早期kill**（Stage A、作成同日） | **機構的必要条件:** `source ρ₀` と `readout E` を独立に選べる functional では、受動性は片側正値性として語領域に降りない（`R=Σc_k e^{θλ_k}` の `λ_k≤0` は熱性から従うが `c_k≥0` は従わない）。**次に受動性witnessを設計するなら両側挟み込み（`E`と`ρ₀`をKMS内積で結ぶ）が必須。** 検定器 `scripts/wpot_null_smoke.py` は再利用可 | 2026-07-26 |

> **Tube calculus（regular branch）についての注記：** 上表とは別に、Tube calculus自体も現時点ではRISEI固有現象とは判定されていない。
> regular tube geometryとその主要な発生機構は、Riesz理論・Schur complement・Zeno型縮約・制御/realization理論の組合せで再構成できるためである。
> ただし棄却ではなく、**完成済みの計算基盤・実験予言系として凍結**し、固有現象探索とは別の資産として保持する方針が取られている（§4.1参照）。

**探索順序の教訓（重要）：** 上記6件はいずれも「まず現象を構成し、後で還元監査した」結果である。
出典文書は、この順序が非還元性を証明する上で非効率であるとし、次の順序へ転換した。

1. 競合理論族（shared-ancilla拡張GKSL、tilted-GKSL/FCS、compact-group synchronization、構造化系同定、bounded-memory process tensor）を**先に固定する**
2. それらが必ず満たす恒等式・rank制約・resource lower boundを**先に抽出する**
3. その恒等式を破るwitnessを**逆設計する**

新候補を探索する際は、この順序（競合理論のnull identityを先に固定 → それを破る構成を逆設計）に従うこと。

### 6.5 「惜しかった」候補（設計の教材）

**完全に死んだ候補より、あと一歩だったものの方が情報量が多い。**
§6.4 で `最終監査` まで生き延びた候補は、単純な還元では死んでいない — どこまで進めて、
**最後に何で死んだか**が次の設計の材料になる。

| 候補 | どこまで到達したか | 最後に何で死んだか |
|---|---|---|
| **Matched operational equivalence** | 単独介入では spectrum・stationary state・full count distribution・1〜4次cumulantが一致（\(D_{TV}\le1.40\times10^{-16}\)）。深さ2で `TS` protocolのvarianceのみ分裂。**最小分離資源 \((d_{\min},k_{\min})=(2,2)\)、\(N_{5\%}\le137\)** の有限資源certificateまで取得 | 固有性は未決着のまま、下記3件と共に最終監査で棄却 |
| **Exact second-cumulant witness** | \(\Delta K_2=2\ell_Y(G-I)r_X\) のexact式。4状態全24 permutation・両順序48例で最大残差 \(1.64\times10^{-15}\)、次元3〜8のランダムMarkov 1500模型で非零率99.4%、量子GKSL 300模型で非零率100% | 式そのものが switched GKSL + FCS の代数から導出可能 |
| **Held-out quotient predictor** | 20 calibrationから未使用30 protocolを数値精度内で予測。gauge非一意な辺があっても held-out予測の差は \(5.55\times10^{-17}\) 以下。次元3,4,5のランダム36模型で point gauge回収35/36 に対し **held-out予測は36/36成功** | 中立なcompact-group latent-frame estimatorと**目的関数・予測値・残差が完全一致（残差0）** |
| **Global cycle quotient atlas** | tree方式の破綻を、冗長calibration graph・group synchronization型初期化・global cycle-consistent fit・prediction interval・abstention certificateへ置換。冗長度1.5で tree estimatorの最大誤差 \(8.40\times10^{-3}\) が \(5.81\times10^{-16}\) まで回復。**161 calibration ⇒ 217 held-out予測** | 同上。ABSTAIN判定まで中立モデルと一致 |

**この4件から読み取るべき教訓:**

- **「局所同値 → 大域的obstruction → 有限資源certificate」という構造まで作り込んでも、それだけでは固有性にならない。** 上記はすべてこの構造を達成した上で死んでいる
- 死因はすべて同じ — **pairwise relative-chart因子化 \(G_{ij}=X_jX_i^{-1}\) へ還元された**こと
- 非零のtriangle holonomyだけでは不十分。一般group synchronizationも不整合cycleを扱える

> ⚠️ **【2026-07-25 訂正】depth-3への移行だけでは逃げられない。**
> 本節は当初「次の候補は全pairwise dataを一致させたまま depth-3以上のconnected tensorだけが破れる方向を優先する」と記録していたが、
> **文献監査 T2（Duncan–Kileel 2025, arXiv:2505.21932 _Higher-Order Group Synchronization_）がこの逃げ道を塞いでいる。**
> 同論文は hypergraph 上の triple / n-wise 局所情報から大域的group elementを推定する枠組みで、
> higher-order synchronizability の必要十分条件と compact group 向け message passing を与える。
> したがって「pairwise因子化を破ったので群同期ではない」という論証は**成立しない**。
>
> **現在の要件:** depth-3への移行に加えて、以下のいずれかが必要。
> - hyperedge order `h=3,4` の higher-order synchronization baseline を**実装した上で**破ること
> - 必要 hyperedge order が `>4` であることの証明
> - group-valued hyperedge potential へ写らないことの構造的論証（quantum response functional / GKSL physicality / finite-shot予測のいずれかが本質的に効くこと）
>
> 詳細は `docs/literature-audit-report.md` §1 T2 および `docs/reduction-targets.md` C族。

### 6.6 記録の運用ルール

**却下が出るたびに、以下を同一コミットで更新すること。** 片方だけ更新すると赤チームが古い前提で判定し続ける。

1. 本ファイル §6.4（および `最終監査` まで到達していれば §6.5）
2. `docs/context-pack.md` §5（同じ表のミラー）
3. `docs/PROJECT_STATE.md` の「決定済み事項」

**番号は再利用しない。** 却下された提案の連番は欠番として残す（欠番自体が「ここで1本死んだ」という記録になる）。

---

## 7. 関連研究・競合論文

新規性主張の根拠、および査読対策として蓄積する。

| 論文（著者・年・誌） | 主張 | 本リポジトリの理論との類似点 | 決定的な差分 | 引用 |
|---|---|---|---|---|
| *TODO* | | | | 必須／参考 |

記入基準:

- **決定的な差分**が書けない論文は、競合ではなく**先行研究**であり、新規性を脅かす。最優先で検討する。
- 査読者が引用を要求しそうな論文は、実際に引用しなくても表には載せる。

---

## 8. 過去に指摘された弱点

同じ失敗を繰り返さないため、提案時に下表を自己監査する。ここでいう「指摘」は、査読報告に限らず、Frozen-Theoriesの改訂、計算認証、探索失敗、ロードマップ上のstop conditionを含む。

| 弱点 | 何が問題だったか | 今後の必須対応 | 主な記録元 |
|---|---|---|---|
| 任意GKSLへの過剰な普遍化 | protected responseに必要なresponse-relevant kernelを持たない反例がある | theoremのquantifierを宣言し、必要条件・反例・admissible classを併記する | `Revised_Generalized_RISEI_Theory_2026-07-21` §18 |
| codimension-oneの普遍化 | selection conditionがcomplexまたは複数制約なら実codimensionは1とは限らない | `codim = rank_R DF` を計算し、rank-dropとpunctureを分ける | 同 §9, §18 |
| theorem / conjecture / numericsの混同 | finite ensembleや高精度係数を普遍定理へ昇格させた | 全主張にlogical statusを付け、昇格条件を明記する | 同 §2, §18 |
| exact kernelとapproximate kernelの混同 | finite-gridや有限Γの狭いlossをexact protected phaseと誤認しうる | `x=Γλ_min/J_eff`、limit order、kernel-destroyed controlを必須化する | 同 §11–§13、Tube Calculus Roadmap |
| finite-Γ tubeをopen asymptotic phaseと解釈 | tube幅は条件下で `Γ^{-1}` にcollapseしうる | manifold、finite-Γ tube、survival gateを別々に報告する | 同 §11、Tube Calculus Roadmap |
| physical matched interfaceの不足 | fullとcutでsource/readout/steady stateまで変える、または非GKSLのentry deletionを物理介入と呼ぶ危険 | physical protocol familyを定義し、ideal cutはderived limitとして扱う。比較クラスを固定する | `Revised Generalized RISEI` §3, §15；本guide初期監査項目 |
| predictive surplusの不足 | 既知現象を新しい言葉で再記述するだけではPRXに届かない | blind prediction、inverse design、new witness、no-go boundary、未使用dataでの検証のいずれかを要求する | Tube Calculus Roadmap Step 9；本guide初期監査項目 |
| 理論固有性の監査不足 | tubeやPattern (b)候補がZeno、EP、FCS、shared ancilla、群同期、control/system identification等へ還元された（2026-07-23の競合理論監査で完了。§6.4参照） | 既知機構、Frozen-Theories、競合論文の三方向で非還元性を検査し、還元された候補を却下表へ移す。今後は競合理論のnull identityを先に固定してから逆設計する順序へ転換する（§6.4末尾） | §3, §6；`docs/source-material/RISEI_Unique_Phenomena_Computation_Summary_and_Search_Strategy_2026-07-23.tex` |
| 全応答の零点をno-goと誤認 | perfect EITでは `χ_full=0` だがsector contributionは非零 | no-go objectを `δχ_S` / master responseに固定する | `EIT_no_go_go_theory` §5；SMRT notes §2.4 |
| floating-point samplingによるexact claim | 多数の周波数点で0でもidentityの証明にはならない | exact arithmetic、Krylov moments、adjugate、symbolic factorizationを使う | SMRT notes §8–§9 |
| Möbius差分のcancellation fragility | 大きな項の差として小信号が出ると、precision依存の偽信号になりうる | `C_cancel`、floor、multiprecision、analytic reconstructionを報告する | `Revised Generalized RISEI` §14 |
| pole label追跡への依存 | degeneracyやpole exchangeでラベルが飛び、機構が変わったように見える | individual poleではなくRiesz projectorとcluster responseをcontinuationする | 同 §7、§14 |
| mechanism attributionの過剰主張 | full responseの予測に成功しても、Schur/Riesz機構への帰属が不十分な場合がある | “prediction succeeds but mechanism attribution fails”を正式branchとして残す | Tube Calculus Roadmap Step 5 |
| 次元解析・rate mappingの甘さ | population rateとcoherence damping、Hzとrad/s、normalized parameterを混同すると指数・閾値が変わる | 単位付き入力、dimensionless sanity test、rate-convention tableを保存する | `EIT_no_go_go_theory` Example 2.2；本guide初期監査項目 |
| 実験可視性の不足 | kernel goや理論的nonzeroは、有限SNR・linewidth・optical depthで見えることを保証しない | signal-to-floor、control budget、ensemble averaging、EIT/ATS判別、材料parameter uncertaintyを別gateにする | `EIT_no_go_go_theory` §7–§9；`Revised Generalized RISEI` §14 |
| onset predictorの過信 | 現行predictorは保守的で、class全体のtight boundではない | right-censoring、local slope、fit-window convergenceを報告し、universal onsetと呼ばない | `Revised Generalized RISEI` §18–§19 |
| 係数の普遍化 | minimal modelの `0.41` 等を普遍定数と誤認しうる | 構造的scalingとmodel-specific coefficientを分離する | 同 §13 |
| 非Markov・無限次元・多体系への早すぎる拡張 | 新現象の起源が介入構造かmemory/continuumか判別できなくなる | まず有限次元time-local GKSL内で閉じ、拡張時は失効する定理を列挙する | 同 §20 |
| PRX向け物語の散漫さ | 現象・定理・実験候補を並べるだけでは中心命題が見えない | 一つの未解決問い、一つの中心定理、一つの決定的witnessを主軸にする | §1のPRX判定ゲート |

### 提案時の弱点申告フォーマット

各提案の「弱点と未解決点」には、最低限次を含める。

- **最も危険な既知還元:** どの既存理論に吸収される可能性が高いか
- **最も弱い仮定:** 外れると中心命題が失効する条件
- **最も脆い数値操作:** cancellation、fit、grid、continuation等
- **最も不足している物理接続:** 実装、SNR、材料parameter、matched interface等
- **PRXを阻む一点:** 現時点でdesk rejectionを招きうる最大の不足
- **stop condition:** 何が成立したら中心主張を撤回・縮小・別誌へ移すか

---

## 9. 提案の出力フォーマット

新理論の提案は `Blueprints-of-theories/` に以下の構成のMarkdownで置く。
ファイル名は `NN_<theory_slug>_proposal.md`。

**番号規約:**
- `NN` は**リポジトリ全体の通し番号。重複させない**（現状 `19_` が2件あるが、これ以降は追随しない）
- **却下されても番号は再利用しない。** 欠番のまま残す — 欠番自体が「ここで1本死んだ」という記録になる
- 次に使う番号は `Blueprints-of-theories/` の最大値 +1。`plan20_` のような接頭辞の揺れは踏襲しない

```markdown
# 理論名（英語名 / 略称）
## 一行サマリ

**作成日:**
**位置づけ:**
**判定:** （PRX候補として探索する価値があるか、現時点での完成度）

## 0. 結論
中心の問い、および理論固有現象を boxed 命題で提示する。

## 1. なぜこの方向を選ぶのか
1.1 既存理論から引き継ぐ事実（§4 を参照）
1.2 壊す仮定 ← 新規性の源泉。必ず明示する。

## 2. 理論の定式化
定義、公理、主定理（型は §2 に従って宣言）

## 3. 理論固有現象
§3 の必須記述項目 1〜5 をすべて埋める。

## 4. 非還元性の検討
既知機構・確定済み理論・競合論文（§7）のそれぞれに対して還元されないことを論じる。
還元されるものが見つかった場合は正直に記録する。

## 5. 検証計画
数値実験・実験提案・解析的検証のいずれか。実行可能な粒度で。

## 6. 弱点と未解決点
自己批判。査読者が突く点を先回りする。

## 7. 参考文献
```

### 出力時の禁止事項

- 固有現象が書けていないのに「新理論」と称すること
- 非還元性の検討を省略すること
- 「証明できる見込み」を「証明済み」と書くこと
- 既存文書の主張を確認せずに引用すること

---

## 10. 検証環境

### 10.1 基本方針

解析証明、symbolic certification、数値探索、open-system simulationを一つのツールに依存させない。主結果は原則として、**少なくとも二つの独立な実装または一つの解析証明と一つの数値実装**で照合する。

この節に挙げるversionは固定せず、実行ごとに実際のversion、OS、precision、commit hashを記録する。QuTiPやMathematicaが利用できない環境では、同等機能による代替を明示する。

### 10.2 推奨ツール

| 目的 | 第一選択 | 補助・独立検証 | 注意 |
|---|---|---|---|
| exact symbolic algebra | Mathematica | Python/SymPy、SageMath | `FullSimplify`の出力だけを証明とせず、仮定、分母の非零条件、factorization、resultant、Groebner basis等を保存する |
| rational matrix / Krylov certificate | Mathematica または SymPy | SageMath | 行列要素は可能な限り整数・有理数・代数数で保持する。浮動小数点へ早期変換しない |
| GKSL/Lindblad simulation | QuTiP | custom NumPy/SciPy Liouville implementation、Mathematica | QuTiPの結果だけでexact identityを主張しない。jump operator、rate convention、vectorization conventionを保存する |
| steady state / group inverse / resolvent | SciPy、QuTiP、Mathematica | mpmathによるmultiprecision | ordinary inverseとDrazin/group inverseを混同しない。trace-zero subspaceまたはsteady-state projectorを明示する |
| Riesz projector / cluster continuation | SciPy Schur decomposition、contour quadrature | Mathematica eigensystem / resolvent contour | individual eigenvalue labelではなくprojector distance、subspace angle、contour gapを監視する |
| asymptotic fitting / fan / tube | Python（NumPy, SciPy, pandas） | Mathematica | fit window、local slope、right-censoring、model comparison、bootstrapを保存する |
| multiprecision | mpmath、Mathematica arbitrary precision | Arb/SageMath | Möbius cancellationが大きい場合はprecision sweepを必須にする |
| convexity・CPTP・SDP feasibility | CVXPY + 利用可能なSDP solver | Mathematica optimization | solver status、tolerance、primal/dual residual、certificateを保存する。数値feasibleを厳密存在証明と同一視しない |
| reproducibility / tests | pytest、Jupyterまたはscript、Git | Mathematica `.wl` test scripts | notebook単体を唯一の実行経路にしない。CLIで再実行できるscriptを用意する |
| visualization | Matplotlib | Mathematica | 色だけに意味を持たせず、線種・marker・labelを併用する |

### 10.3 主張別の最低検証基準

#### A. Exact theorem / exact no-go

必須:

1. exact arithmeticでのsymbolic derivation
2. 分母、regular point、spectral gap等の仮定一覧
3. finite Krylov/adjugate/symmetry certificate
4. 小次元の直接展開によるsanity check
5. random numerical substitutionによる反例探索

禁止:

- machine precisionの周波数scanだけで `≡0` と書くこと
- `Chop` や任意thresholdでexact zeroを作ること

#### B. Conditional theorem

必須:

1. 仮定をmachine-checkableなgateへ変換
2. 各gateのmarginを出力
3. gate failure時に結論を返さず、`outside assumptions` と分類
4. 仮定を一つずつ壊すdestruction test

#### C. Numerical phenomenon

必須:

1. grid、domain、time step、precision convergence
2. 少なくとも一つの独立実装
3. parameter perturbationとrandom seed ensemble
4. null model / destroyed-mechanism control
5. fit-window dependence、local exponent、right-censoring
6. raw dataとplot生成scriptの保存

#### D. Physical open-system claim

必須:

1. Hamiltonian Hermiticity、jump rates非負、trace preservation、CPTP/GKSL form
2. steady-state residualとpositivity
3. source/readout、polarization、normalization、unit convention
4. EIT/ATSまたは他の競合機構を区別するcontrol
5. 実験parameter uncertainty、SNR、finite observation window

### 10.4 標準ワークフロー

1. **Model specification**  
   `model.yaml` または同等ファイルにHilbert basis、Hamiltonian、jump operators、sector、source、readout、units、scaled rates、parameter rangeを記述する。

2. **Symbolic minimal model**  
   Mathematica/SymPyで最小模型をexactに構築し、dimension、trace preservation、moments、determinants、factorizationを確認する。

3. **Unit tests**  
   既知極限、zero coupling、symmetry limit、textbook Λ、full-rank damping、singular-kernel exampleを自動テストする。

4. **Independent implementation**  
   QuTiPとcustom Liouville code、またはMathematicaとPythonの結果を同一parameter setで比較する。

5. **Precision and convergence sweep**  
   precision、grid、domain、time step、contour radius、fit windowを変え、主結論が安定する範囲を記録する。

6. **Destruction controls**  
   protected kernel、selection condition、sector coupling、symmetry、physical interfaceを一つずつ破壊し、現象が予測どおり消えるか確認する。

7. **Claim classification**  
   出力を `Exact / Conditional / Conjecture / Numerical / Model-specific / Failed / Known-theory reduction` に分類する。

8. **Reproducibility bundle**  
   最低限、次を保存する。

   ```text
   environment.yml / requirements.txt
   Mathematica_version.txt
   model.yaml
   symbolic_certificates/
   src/
   tests/
   configs/
   raw_data/
   figures/
   logs/
   README_reproduce.md
   git_commit.txt
   ```

### 10.5 Claude等AIエージェントへの実行規則

- ツールが実際に接続・installされているかを確認する前に「検証済み」と書かない。
- Mathematicaが使えない場合、必要なsymbolic certificateをSymPy/SageMathで代替し、代替に伴う限界を報告する。
- QuTiPが使えない場合、custom Liouville implementationを用い、少なくともtrace preservationと既知例で検証する。
- 長時間計算の前に、small-size smoke test、unit test、runtime estimateを実行する。
- 数値計算が停止した場合、単なる`failed`ではなく、physical failure、numerical instability、outside scope、insufficient precision、mechanism attribution failureのいずれかを返す。
- AIが生成した証明・コードは、人間が読めるcertificate、test、再現手順を伴わない限り確定結果としてFrozen-Theoriesへ移さない。


---

## 11. 検証ワークフロー（Claude ↔ ChatGPT）

### 11.0 原則

**ChatGPTは共著者ではなく赤チーム（敵対的検証者）として使う。**

2つのLLMに協調的に推敲させると、両者が「もっともらしい方向」へ同調し、
**誤った主張が滑らかな文章になって残る**。これが最悪の結果である。
特に §3 の非還元性は、LLM同士が合意しても何の保証にもならない。
役割を非対称にし、合意ではなく**生き残り**でフィルタする。

関連ファイル:

- `docs/redteam-instructions.md` — ChatGPTのカスタム指示（コピペ元）
- `docs/context-pack.md` — プロジェクトにアップロードする資料層
- `docs/claim-template.md` — 各チャットに貼る主張の雛形

### 11.1 工程

| Stage | 作業 | 担当 | 成果物 |
|---|---|---|---|
| 0 | 提案の生成（**未推敲のまま**） | Claude | `Blueprints-of-theories/NN_*_proposal.md` |
| 1 | 検証すべき主張の抽出 | 所有者 | 主張リスト（`claim-template.md` 形式） |
| 2 | **還元の試行** ← 工程の本体 | ChatGPT(赤チーム) | 判定・写像・残る差分 |
| 3 | 文献照合 | ChatGPT(調査役) | §7 の競合論文表 |
| 4 | 数式・数値の独立検証 | 計算環境 | 数値結果 |
| 5 | 改訂または放棄の判断 | Claude | 改訂稿／却下記録 |
| 6 | 英文化・整形（**最後**） | ChatGPT(校正) | 投稿形式の原稿 |

**Stage 1〜5 を、還元が成功しなくなるまで回す。**

### 11.2 各Stageの注意

**Stage 0 — 文章を綺麗にしない。** 粗い方が接合部の弱さが見える。

**Stage 1 — 主張だけを抜き出す。** 文書全体を渡すと「全体としてよく書けている」という
無害な感想が返るだけである。また文書に含まれる「なぜ新しいか」の枠付けが同調を誘導する。

**Stage 2 — 望む結論を伝えない。**
「これは新理論です、確認してください」ではなく「これを既知の機構に還元してください」と命じる。
- 1チャット1主張（同一スレッドでは前の判定との整合を取ろうとし、独立判定にならない）
- 重要な主張は別チャットで3回。**1回でも還元成功が出たら、その主張は死んだものとして扱う**
- 還元に成功したら §6.4 へ記録して次へ。**これは失敗ではなく工程が正しく機能した証拠である**

**Stage 3 — LLMは存在しない文献を生成する。** DOI/arXiv番号を実在確認するまで §7 に「未確認」フラグを付ける。

**Stage 4 — 両方のLLMを信用しない層。**
次元解析、極限での既存理論の再現（§3.1-5）、反例の数値スキャンを実際に計算する。
**LLM二者が一致した式ほど危険**である（同じ訓練データ由来の同じ誤りを共有しうる）。

> ⚠️ **held-out を提案間で使い回さない。**
> `docs/context-pack.md` §6.4 で held-out は `seed 20260723`（depth4から64 protocol等）に固定されている。
> **この同じ集合を提案1・提案2で使うと、2本目以降は blind ではなくなる** —
> 提案1のheld-out結果を見た人間／エージェントが提案2を設計する時点で情報が漏れている。
> 形式上は「候補生成にheld-outを使っていない」が、実質は汚染されている。
>
> **運用（どちらか）:**
> - **分割**：64 protocolを提案ごとに割り当てる（例：提案あたり16、4本で使い切り）
> - **再抽出**：提案ごとに新しいseedで引き直し、**どのseedがどの提案に対応するかを提案文書に記録する**
>
> どちらの場合も、使用したseedと割当を提案の §5 検証計画に明記すること。
> これは baseline を狭めているわけではないため §4.4 の予算違反にはあたらないが、
> **blindness だけが静かに失われる**ので明文化しておく。

**Stage 6 — 順序を守る。** 論理が固まる前に推敲すると、内容の弱さが文体で隠れる。

### 11.3 ChatGPT側の構成

命令と資料を混ぜない。プロジェクトにアップロードしたファイルは検索で必要部分だけ引き出されるため、
命令をファイルに置くとチャットによって拾われない。

| 層 | 置き場所 | 中身 | 更新頻度 |
|---|---|---|---|
| 命令 | **カスタム指示欄** | 役割、還元の強制、出力形式、DOI要求 | ほぼ固定 |
| 資料 | **プロジェクトファイル** | `context-pack.md` | 月単位 |
| 検証対象 | **各チャットに直接貼る** | 主張1件のみ | 毎回 |

**還元プロジェクトと文献調査プロジェクトは分ける。** 混ぜると赤チームの役割が薄まる。

### 11.4 収束判定（先に決めておく）

| 条件 | 判定 | 行き先 |
|---|---|---|
| 3ラウンド連続で新しい還元経路が出ず、かつ観測可能量が数値的に確認できた | 採用 | `Frozen-Theories/` |
| 還元に成功した | 却下 | §6.4 に記録 |
| 「まだ検討が必要」が3ラウンド以上続く | 打ち切り | §6.4 に記録 |

打ち切り基準がないと、部分的に有望な提案を無限に磨き続けることになる。
**却下記録が溜まること自体が探索空間を狭める資産である。**

### 11.5 リポジトリ運用

各提案を独立ブランチ（`theory/NN-slug`）で進め、ラウンドごとにコミットする。
どの指摘でどう変わったかの監査証跡が残り、それ自体が次の提案の材料になる。
却下されたブランチはマージせず、§6.4 に要約を転記する。

### 11.6 落とし穴

- **早すぎる推敲** — Stage 6 を前倒しすると弱点が見えなくなる
- **同調の誘発** — 「これは有望ですか？」と聞かない。「これを壊してください」と聞く
- **架空の文献** — DOI確認まで §7 に確定として載せない
- **却下を惜しむ** — 還元されたものを「まだ違う角度があるはず」と延命しない
