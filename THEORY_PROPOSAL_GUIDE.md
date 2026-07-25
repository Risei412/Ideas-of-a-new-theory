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

| 投稿先 | 適する内容 | 要求される厳密性 |
|---|---|---|
| PRX Quantum | 量子情報・開放量子系寄りの結果 | PRXと同等 |
| PRA / PRD | 個別現象の定量的解析 | 中〜高 |
| PRL | 単一の鋭い主張 | 高（ただし短い） |
| Quantum / JHEP 等 | 数学的構造が主 | 定理として閉じていること |

> **TODO:** 実際の優先順位・過去の投稿履歴があれば記入。

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

探索提案がこの外側を扱う場合、少なくとも次を記す。

1. 外した仮定
2. 代替する数学的構造
3. どの凍結定理が残り、どれが失効するか
4. 新たに必要なsanity checkと反例
5. 極限・数値・実験の検証計画

---

## 5. 記法・用語の統一

複数文書を後で統合できるよう、記号を揃える。

| 記号 | 意味 | 備考 |
|---|---|---|
| *TODO* | | |

規約:

- 新しい概念には英語名と日本語名を両方与える（例：dilation frustration ／ 共通実装フラストレーション）
- 略称は初出時に必ず展開する（DCIT, RISEI, SMRT …）
- 既存文書と衝突する記号を使わない。衝突した場合はこの表を更新する。

---

## 6. 探索対象と却下リスト

### 6.1 現在の関心方向（優先度順）

> **TODO:** 例：開放量子系の介入構造／トロピカル幾何と付値異常／因果構造の実現可能性／保護の熱力学 …

### 6.2 パラメータ空間の空白地帯

既存理論が扱っていない領域。新現象はここに潜む。

> **TODO:** 極端な極限、未検証のスケール、複数構造の組み合わせなどを列挙。

### 6.3 未解決の異常・矛盾

既存理論同士で説明がつかない事象。新理論のトリガー候補。

> **TODO:**

### 6.4 却下・保留になったアイデア（再提案禁止）

| アイデア | 却下理由（何に還元されたか） | 判定日 |
|---|---|---|
| *TODO* | | |

> 既存文書によれば、tube、Pattern (b)、protocol-order fluctuation、relative gauge、quotient atlas 等は
> Zeno／FCS／shared ancilla／群同期／構造化系同定 などへの還元を免れなかったと記録されている。
> 正確な理由と適用範囲を所有者が確認のうえ、この表に転記すること。

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
| 理論固有性の監査不足 | tubeやPattern (b)候補がZeno、EP、FCS、shared ancilla、群同期、control/system identification等へ還元された | 既知機構、Frozen-Theories、競合論文の三方向で非還元性を検査し、還元された候補を却下表へ移す | §3, §6；探索メモ群 |
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
ファイル名は `NN_<theory_slug>_proposal.md`（NNは連番）。

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
