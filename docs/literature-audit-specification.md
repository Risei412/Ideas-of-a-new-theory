# 競合文献監査仕様書

**作成日:** 2026-07-25  
**対象リポジトリ:** `Risei412/Ideas-of-a-new-theory`  
**主対象:** P0 — Resource-bounded mechanism separation  
**副対象:** P0 — Interface realizability  
**工程上の位置:** Stage 3 文献照合。還元判定・数値検証とは分離する。

---

## 0. 目的

この監査の目的は参考文献一覧を作ることではない。次の問いに答えるため、競合理論族の**最強の既知結果、成立仮定、表現資源、必須恒等式、下限・不可能性定理**を抽出する。

> 同じ calibration data を与え、hidden dimension・memory depth・protocol depth・functional order・parameter count・shots を固定したとき、既存の競合理論は held-out response をどこまで予測できるか。できない場合、その失敗は単なる optimizer failure ではなく、表現不能性または資源下限として証明できるか。

主たる用途は、競合が必ず満たす null identity / rank constraint / resource lower bound を先に固定し、それを破る witness を逆設計することである。

この文献調査の段階では、本リポジトリの命題が正しいか、新規性があるかを判定しない。各文献が「どこまで既に行ったか」と「何を仮定したか」だけを確定する。

---

## 1. 監査対象と優先順位

### 1.1 最優先の中心問題

**Resource-bounded same-data gap**

- calibration: depth 1 は全 protocol、depth 2 は冗長度 `ρ=1.5` の連結グラフ（両順序）、depth 3 は seed 固定の24 protocol
- held-out: depth 2 の未使用 edge、depth 3 の未使用 protocol、depth 4 の事前固定64 protocol
- candidate と competitor に同一の prior、noise、nuisance parameter、sector information を与える
- held-out data はモデル選択、hyperparameter tuning、停止判定に使用しない
- path support、path count、低次 mixed Krylov moments を一致させたまま、depth 3 以上の connected response が分離する可能性を主に調べる

### 1.2 副問題

**Interface realizability**

複数の GKSL-admissible intervention counterfactual が、単一の system–environment dilation、共通環境状態、共通制御インターフェース上で同時実現できるための compatibility 条件を調べる。個々の map / generator の dilation existence と、族としての common realizability を区別する。

### 1.3 今回の対象外

- unrestricted infinite-dimensional continuum
- generic many-body / thermodynamic-limit theory
- gain medium、unstable generator
- finite-grid だけから continuum spectrum を推定する研究
- unrestricted process tensor による表現可能性だけを示す研究
- non-Markovity、strong nonlinearity、many-body limit を同時導入する研究
- 材料固有の数値最適化だけで、一般的な恒等式・下限・表現能力を与えない研究

---

## 2. 競合モデル6族＋解析的reduction gate

### A. Enlarged GKSL with hidden ancilla

調査事項:

- finite-dimensional Markovian embedding / pseudomode / reaction-coordinate / collision-model dilation の表現定理
- visible reduced dynamics・multi-time statistics・controlled interventionsを再現するための最小 ancilla dimension
- common dilation、programmable channel、instrument compatibility、superchannel realization の条件
- product initial state と initial system–environment correlation の差
- visible-only readout 制約の下での識別可能性

凍結予算:

- `D_hidden = 1–4`（標準）、最終監査は最大6
- 自由実数パラメータ `P ≤ 256`
- jump operator 数 `≤ 2 D_hidden + m`
- protocol depth `d ≤ 4`
- 原則 product initial state、ancilla readout 禁止

### B. Tilted-GKSL / full counting statistics

調査事項:

- quantum jump trajectories、counting fields、tilted generator、dynamical large deviations
- multi-time / ordered cumulants、finite-time FCS、switched generator、control protocol 下のFCS
- 低次 cumulant の一致が高次・held-out protocol に課す恒等式
- hidden Markov / transfer-matrix realizationとの同値性および最小次数

凍結予算:

- cumulant / functional order `k ≤ 4`
- protocol depth `d ≤ 4`
- counting fields 最大2
- counted jump channels 最大4
- hidden ancilla は含めず、必要なら A として別計上

### C. Compact-group synchronization

調査事項:

- group synchronization、angular synchronization、cycle consistency、connection Laplacian
- permutation / `SO(2)` / `SO(3)` / `SU(2–4)` の noisy synchronization
- gauge ambiguity と held-out relative transformation prediction
- exact recovery、stability、sample complexity、outlier robustness、predict-or-abstain certificate
- `G_ij = X_j X_i^{-1}` を超える higher-order / hypergraph synchronization の既知結果

凍結予算:

- representation dimension `r_G ≤ 4`
- Lie algebra dimension `q_G ≤ 15`
- calibration redundancy `ρ ∈ {1.0, 1.5, 2.0}`
- optimizer restart 32
- output は point prediction または certified ABSTAIN

### D. Controlled HMM / structured state-space identification

調査事項:

- controlled HMM、input-output HMM、predictive state representation、observable operator model
- switched / bilinear / quantum state-space realization と minimal realization order
- Hankel rank、Kalman reachability/observability、identifiability、experiment design
- finite data での order selection、generalization、lower bounds
- same low-depth data を持つ異なる realization の higher-depth separation

凍結予算:

- hidden-state number / realization order `D ≤ 6`
- intervention数 `m ≤ 8`
- output channels 最大4
- protocol depth `d ≤ 4`
- `P ≤ 256`
- model selection は calibration data の BIC または cross-validation のみ

### E. Bounded-memory process tensor

調査事項:

- quantum comb / process tensor / quantum stochastic process
- finite Markov order、memory dimension、MPO / tensor-network representation
- instrument-specific Markov order と universal Markov order の区別
- memory dimension、bond dimension、temporal correlation length の認証・下限
- process tensor tomography、compressed learning、causal breaks
- bounded class 内の held-out protocol prediction と sample complexity

凍結予算:

- memory Hilbert dimension `D_M ≤ 6`
- MPO bond dimension `χ ≤ D_M^2 = 36`
- memory depth / Markov order `μ ≤ 3`
- protocol depth `d ≤ 4`
- functional order `k ≤ 4`
- `P ≤ 256`

### F. Active experimental design baseline

調査事項:

- Bayesian optimal experimental design、expected information gain、D-optimality
- adaptive quantum process / Hamiltonian / Lindbladian learning
- active model discrimination と abstention
- finite-shot sample complexity と minimax / information-theoretic lower bound
- restricted protocol menu 下での optimal design

凍結予算:

- adaptive rounds 最大4
- candidate calibration protocols 最大32
- calibration total shots `≤ 1.2 × 10^5`
- posterior samples 4096
- optimizer restart 32
- held-out protocol への問い合わせ禁止

### G. 解析的reduction gate

次の各機構について、候補を即時還元できる定理・恒等式・最小反例を調べる。

- BCH / Magnus / nested-commutator expansion
- Dyson path expansion、labelled path counting
- Krylov reachability、mixed moments、Hankel rank
- Schur complement、Feshbach map、adiabatic elimination、Zeno reduction
- Kalman controllability / observability、minimal realization
- quantum regression theorem と multi-time correlation
- symmetry、selection rule、commutant、invariant subspace

この層には数値予算を与えない。数式上の写像が成立すれば、その時点で candidate は kill される。

---

## 3. 共通の凍結条件

| 資源 | 標準監査 | 拡張・最終kill監査 |
|---|---:|---:|
| intervention数 `m` | 3–6 | 7–8 |
| protocol depth `d` | 1–3 | 4 |
| functional order `k` | 1–3 | 4 |
| hidden dimension `D` | 1–4 | 5–6 |
| memory depth `μ` | 1–2 | 3 |
| 自由実数パラメータ数 `P` | ≤128 | ≤256 |
| optimizer restart | 16 | 32 |

共通prior・noise:

- `J_ref = 1`
- `γ, κ ~ LogUniform(10^-2, 10^2)`
- `Re H_ij, Im H_ij ~ Uniform(-1,1)`
- 1 protocol あたり2,000 shots、総上限 `1.2 × 10^5`
- production noise 1%、stress test 3%
- control-amplitude drift 1%、timing jitter 0.5%
- sampling seed `20260723`

文献が異なる資源定義を用いる場合、上表へ変換する写像を示す。変換不能なら「比較不能」と記録し、都合よく同一視しない。

---

## 4. 情報源の採用基準

### 4.1 優先順位

1. 原著査読論文、著者最終稿、公式journal page
2. arXiv原稿（査読版との差分を確認）
3. 標準的review / monograph
4. 学会資料・thesis（原著で欠ける導出やnegative resultに限る）

検索結果のスニペット、二次解説、LLMの記憶だけでは採用しない。

### 4.2 実在確認

各文献について以下を最低2経路で照合する。

- DOI resolver またはjournal公式ページ
- arXiv abstract / PDF metadata
- Crossref、INSPIRE、PubMed等の書誌database（分野に応じて）

DOI/arXivが確認できない文献は「未確認」とし、確定表に入れない。

### 4.3 主張の強度

文献中の結果を次に分類する。

- `Exact theorem`
- `Conditional theorem`
- `Asymptotic theorem`
- `Numerical evidence`
- `Experimental observation`
- `Review statement`
- `Author conjecture`

abstractの表現を定理として扱わない。仮定、quantifier、finite/asymptotic、noise-free/noisyを原文で確認する。

### 4.4 PDF収集

- open-accessの合法的な原著PDFを優先する
- 同一論文のjournal版とarXiv版を重複保存しない。差分が重要な場合のみ両方保持する
- PDFが取得できない場合は、DOI、arXiv、公式landing pageをmanifestに残す
- ファイル名は `FirstAuthor_Year_ShortTitle_arXiv-or-DOI.pdf`
- 各PDFのSHA-256、取得元、取得日、版をmanifestへ記録する

---

## 5. 1文献ごとの抽出様式

```markdown
### [ID] 著者・年・誌・タイトル
- DOI:
- arXiv:
- 公式URL:
- 版・確認日:
- 競合族: A/B/C/D/E/F/G（複数可）
- 論理status: Exact / Conditional / Asymptotic / Numerical / Experimental / Review / Conjecture
- 対象系:
- 主張:
- 成立仮定:
- 入力されるcalibration data:
- 予測対象:
- 表現資源: D_hidden, D_M, χ, μ, d, k, P, shots（該当分のみ）
- 必須恒等式・rank constraint:
- resource lower bound / impossibility result:
- 本リポジトリとの具体的写像:
- 類似点:
- 決定的な差分:
- 差分なしの場合: 「先行研究の可能性」と明記
- どの候補をkillし得るか:
- 残る未解決部分:
- 引用: 必須 / 参考 / 不要
- 確信度: 高 / 中 / 低
- 根拠箇所: theorem / equation / section / page
```

「具体的写像」は文章だけで済ませず、可能なら次の形で書く。

\[
\text{repository object} \longleftrightarrow \text{literature object},
\qquad
\text{repository protocol} \longmapsto \text{control/instrument sequence}.
\]

---

## 6. 判定規則

### 6.1 文献単位

- **Prior-art threat:** 決定的な差分がなく、同等以上の仮定と資源で中心命題を既に示す
- **Strong competitor:** 中心命題そのものではないが、同じ held-out prediction を凍結予算内で達成し得る
- **Partial reduction:** 一部のobservable、protocol depth、functional orderだけを説明する
- **Background:** 概念・道具は近いが、中心問題へ直接の写像がない
- **N/A:** 比較対象となる構造を持たない

### 6.2 候補をkillする条件

次のいずれかが具体的写像とともに成立すれば、固有性主張を撤回する。

1. 既存理論が同一calibration dataから同一held-out responseを凍結予算内で予測する
2. 候補witnessが既知の恒等式、symmetry、Dyson/Krylov path、FCS cumulant、group synchronization、state-space realization、bounded-memory process tensorへexactに写る
3. 資源超過を主張していたが、既知の圧縮・minimal realization定理により予算内へ落ちる
4. interface obstructionが既知のcommon dilation / compatibility theoremの直接の系である

### 6.3 生き残り条件

「検索で見つからなかった」は生き残りではない。少なくとも次が必要である。

- 各競合族で代表原著、最強の一般定理、最新の主要拡張を確認
- 既知の表現定理を凍結予算へ換算
- 解析的reduction gateを全項目実行
- 競合側の最良モデルでも破れない null identity または resource lower bound を抽出
- 独立した3回の還元監査で還元成功が出ない

---

## 7. 検索戦略

### Pass 1 — 語彙とseed文献

各族についてreviewと高被引用原著から標準語彙、代表定理、著者群を確定する。

### Pass 2 — 最強結果

`minimal dimension`, `finite memory`, `identifiability`, `realization theorem`, `lower bound`, `impossibility`, `sample complexity`, `exact recovery`, `multi-time`, `controlled`, `instrument-specific` を組み合わせる。

### Pass 3 — 反例・negative result

`non-identifiability`, `no-go`, `incompatible`, `insufficient statistics`, `indistinguishable processes`, `same marginals different joint`, `hidden dimension witness`, `memory witness` を検索する。

### Pass 4 — 引用連鎖

seed文献の被引用・引用文献から、より一般的な定理と最新拡張を追跡する。reviewだけで止めない。

### Pass 5 — 交差領域

- FCS × controlled HMM
- process tensor × finite Markov order × MPO
- common dilation × instruments × superchannels
- group synchronization × hypergraph / higher-order consistency
- system identification × active experimental design
- Krylov/Hankel rank × multi-time quantum response

### Pass 6 — 新規性脅威の逆検索

本リポジトリの理論名を使わず、中立化した中心命題、定義、witnessだけで検索する。理論名による自己参照や同調を避ける。

---

## 8. 成果物

1. `docs/literature-audit-report.md`  
   競合族別の結果、prior-art threat、null identity、resource lower bound、未解決境界。
2. `docs/literature-master-table.csv`  
   1行1文献の機械可読表。
3. `references/references.bib`  
   DOI/arXivを検証済みのBibTeX。
4. `references/manifest.csv`  
   PDF名、SHA-256、取得元、取得日、版、ライセンス・入手可否。
5. `references/papers/`  
   合法的に取得可能な原著PDF。取得不能なものはmanifestにlanding pageを残す。
6. `docs/reduction-targets.md`  
   文献から抽出した null identity / rank constraint / resource lower bound のみを、逆設計に使える形で集約。

最終報告では、文献数ではなく次を明示する。

- 中心命題を直接脅かす最重要文献
- 6族それぞれの最強の既知表現能力
- 凍結予算内で再現できる範囲
- 現時点で文献上残る最小の空白
- 次に逆設計すべきwitness
- 追加調査が必要な不確実点

---

## 9. 完了条件と停止条件

### 完了条件

- 6競合族それぞれで、review 1本以上、基礎原著2本以上、2019年以降の主要拡張2本以上を確認
- 解析的reduction gateの7項目すべてに代表定理または標準参照を割り当てる
- 全採用文献のDOIまたはarXivを実在確認
- 各文献に決定的な差分と根拠箇所を記入
- strongest prior-art threatを少なくとも3本選び、中心命題への写像を数式で示す
- PDF取得の成否をmanifestへ記録

### 即時停止・方針変更条件

- 中心命題と差分のない先行研究が見つかる
- 凍結予算内で全held-out predictionを達成する既知アルゴリズムが見つかる
- proposed null identityが既知の標準恒等式の直接の系である
- 文献上の用語定義が本リポジトリと非同値で、資源比較が成立しない

この場合、調査を惰性的に続けず、該当文献と具体的写像を最優先で報告し、中心命題の撤回・縮小・再定式化へ戻る。

---

## 10. Deep Research実行用の短縮指示

```text
この文献監査では、新規性を肯定しない。対象は有限次元の開放量子系における resource-bounded same-data gap と interface realizability である。

競合モデル6族（hidden-ancilla enlarged GKSL、tilted-GKSL/FCS、compact-group synchronization、controlled HMM/structured state-space identification、bounded-memory process tensor、active experimental design）と、解析的reduction gate（BCH/Magnus、Dyson path、Krylov/Hankel、Schur/Zeno、Kalman、quantum regression、symmetry）を調べよ。

各文献について DOI/arXiv を実在確認し、主張、成立仮定、入力calibration data、予測対象、必要資源、恒等式・rank constraint・lower bound、中心問題への具体的写像、決定的な差分、根拠箇所を記録せよ。差分がなければ「先行研究の可能性」と明記する。

検索で見つからないことを非還元性の証拠としない。reviewだけで止めず、原著と最新拡張を追う。最終的に、最重要のprior-art threat、各競合族の最強結果、凍結予算内で再現可能な範囲、残る最小の空白、逆設計すべきnull identity / resource lower boundを提示せよ。
```
