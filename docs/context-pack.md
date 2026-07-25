# コンテキストパック（ChatGPTプロジェクトにアップロードする資料）

**このファイルは資料層である。命令を書かないこと**（命令は `redteam-instructions.md` → カスタム指示欄）。

**用途:** ChatGPTのプロジェクトに**ファイルとしてアップロード**する。
チャットごとに貼り直す必要はなく、更新時に差し替えるだけでよい。

**更新契機:** 新しい還元経路が見つかったとき／確定済み理論が増えたとき／記号を追加したとき。

---

> **記入状況（2026-07-25）:** §1 記号表・§5 却下リスト・§6 競合予算・§7 未解決項目は記入済み。
> **§2 適用範囲・§3 抵触禁止制約のみガイド §4.1／§4.2 からの転記待ち。**
> この2節が埋まればアップロード可能な状態になる。

---

## 1. 記号・用語（→ ガイド §5）

### 1.1 共通記号（3理論で一致）

| 記号 | 意味 |
|---|---|
| `Γ` | 支配的な散逸スケール／漸近スケール |
| `D` | fast damping-shape operator（`A_Γ(z)=ΓD+B(z)`） |
| `B(z)` | 遅い／周波数依存ブロック |
| `S, T, U` | 操作的sectorまたはsector部分集合 |
| `𝒢_S` | sector選択的な GKSL-admissible 介入生成子 |
| `c` / `p†` | probe source ／ readout covector |
| `κ` | 介入強度 |

### 1.2 RISEI

`π` 順序付き介入protocol｜`𝒰_π` protocol依存propagator｜`C_π^(n)` connected n-time cumulant｜
`R_π^(n)` full-minus-protocol応答｜`Ω_T^(n)` subset-Möbius不可約応答｜`Ξ_{S,T}^(n)` order-irreducible応答｜
`Φ` 応答functional｜`ν_Φ` functional依存valuation｜`N_∞, N_1` 応答ノルム｜`Σ_π^(n)` scaling signature｜
`k_min^(n,Φ)` protection depth｜`𝒞[π]`/`𝒞_req` protocolコスト/最小同定コスト｜`P_𝒞` Riesz projector｜
`K_Z` Schur–Zeno結合｜`f`/`J_f` 選択写像/Jacobian｜`ℳ_Γ` 選択多様体｜`𝒜` admissible perturbation class｜
`Λ` limit protocol｜`ℰ_full` response-defect｜`Q_tube` Gram行列｜`𝒯_{ε,Γ}` response tube｜
`z_loss`/`z_jet` 無次元crossover座標｜`q_*` Schur self-energy指数｜`κ_eff`/`α_eff`｜`Δ_prot` 保護スケール｜
`C_cancel` cancellation condition number

### 1.3 SMRT

`𝒱_full ≅ ℂ^{N_full}` full response space｜`A_{full,Γ}(z)=ΓD_full+B_full(z)` native response family｜
`𝔈=(A_{full,Γ},c_full,p_full,K)` experiment specification｜`𝔓=(𝒢_S,κ₀,q)` path specification｜
`K ⋐ Ω` 観測窓（`Ω`は周波数領域）｜`q` scaling path指数（`κ=κ₀Γ^q`）｜
`ℛ_S^op`/`ℛ_{S,Γ}^ideal` operational/ideal master sector-resolved response｜
`ν_S(q;κ₀)` valuation、`ν ∈ {∞} ∪ (0,∞) ∪ {0}` の排他的三分類｜`𝔉` exact function field

### 1.4 EIT

`ℋ_g, ℋ_e` 下位/励起manifold｜`Ω` optical coupling map（`Ω_c` control Rabi）｜`C` dipole coupling行列｜
`A(z)` optical-coherence生成子｜`G=A^{-1}` resolvent｜`K_ab` coherent-response kernel｜
`S_a`/`S_g=G_g-CA^{-1}B` 対角応答/Schur補｜`M_n=p†X^nν` resolvent moment｜`Q` reducing symmetry operator｜
`P=Proj(ker D)` protected-subspace projector｜`γ_g` lower-coherence decay/detuning｜`β=|Ω_c|²/4` control intensity｜
`Ξ` 正規化full local probe response｜`χ_full`/`χ_cut^(𝕊)`/`δχ_𝕊` full応答/切断counterfactual/差分｜
`ν=D^{-1}c` moment symbol｜`C_abs` 相対吸収コントラスト

### 1.5 ⚠️ 衝突記号 — 判定時に必ず確認すること

**同じ文字が理論ごとに別物を指す。命題中にこれらが無修飾で現れたら、どの理論の意味かを確認してから判定すること。**
文脈の取り違えは、還元の成否判定そのものを誤らせる。

| 記号 | RISEI | SMRT | EIT |
|---|---|---|---|
| **`Ω`** | subset-Möbius不可約応答 | **周波数領域** | **optical coupling map** |
| **`K`** | Schur–Zeno結合 `K_Z` | **観測窓** | **coherent-response kernel** |
| **`Q`** | tube Gram行列／補projector | — | **reducing symmetry operator** |
| **`Ξ`** | order-irreducible応答 | — | **正規化full probe response** |
| **`ν`** | valuation | valuation（RISEIと整合） | **moment symbol `D^{-1}c`** |
| **`C`** | cumulant／コスト | — | **dipole coupling行列** |
| **`M`** | 選択多様体 | — | **resolvent moment** |
| **`P`** | Riesz projector／puncture集合 | **path spec `𝔓`** | protected projector（RISEIと整合） |
| **`A`** | admissible perturbation class | response family | 生成子（SMRTと整合） |
| **`G`** | 介入生成子（SMRTと整合） | cut生成子 | **resolvent `A^{-1}`** |
| **`S`** | sector | sector | **対角応答／Schur補** |
| **`z`** | **無次元座標** `z_loss`,`z_jet` | 複素周波数 | 複素周波数 |
| `q` | Schur self-energy指数 | scaling path指数 | — |

> ⚠️ **`D` の三重衝突に特に注意。** 凍結理論では `D` = fast damping-shape operator（`A_Γ(z)=ΓD+B(z)`）だが、
> **§6 の競合予算表では `D` = hidden dimension**、さらに `D_M` = memory Hilbert dimension である。
> 命題や判定文で `D` が現れたら、散逸演算子か次元パラメータかを必ず確認すること。

### 1.6 略称

| 略称 | 正式名称 |
|---|---|
| RISEI | *要確認*（凍結文書内に展開なし） |
| SMRT | Sector-Mediated Response Theory |
| EIT | Electromagnetically Induced Transparency |
| ATS | Autler–Townes Splitting |
| CPT | Coherent Population Trapping |
| DCIT | Dilation-Consistent Intervention Theory（草案段階） |
| GKSL | Gorini–Kossakowski–Sudarshan–Lindblad |
| CPTP | Completely Positive Trace Preserving |
| FCS | Full Counting Statistics |
| EP | Exceptional Point |
| QFI | Quantum Fisher Information |
| HMM | Hidden Markov Model |
| MPO | Matrix Product Operator |
| SNR | Signal-to-Noise Ratio |

---

## 2. 前提として置かれている確定済み理論の適用範囲（→ ガイド §4.1）

新しい命題を判定する際、これらは**既に確立された事実として扱ってよい**。

| 理論 | 主結果 | 凍結された適用範囲（この外では保証されない） |
|---|---|---|
| RISEI | *TODO* | *TODO* |
| SMRT | *TODO* | *TODO* |
| EIT | *TODO* | *TODO* |

---

## 3. 抵触してはいけない制約（→ ガイド §4.2）

命題がこれらのいずれかを破る場合、**どの仮定を外したかが明示されていない限り、その命題は誤りである**。

- *TODO*（CPTP性、熱力学第二法則、既存no-go定理など）

---

## 4. 既知の還元先機構

赤チームが最低限検討すべき機構。**還元が成功するたびにここへ追記する。**

- Zeno効果 / Zeno narrowing
- 例外点（exceptional point, EP）
- Full counting statistics (FCS) / tilted-GKSL
- unravelling依存性
- 群同期（compact-group synchronization）
- 構造化系同定（structured state-space identification / controlled HMM）
- shared ancilla enlargement による説明
- bounded-memory process tensor
- 平均場近似の破れ
- 有限サイズ効果
- 対称性からの自明な帰結
- Riesz projector / Schur complement / Zeno型縮約 / 制御・realization理論の組合せ（Tube calculus regular branchの説明に使われた組）

---

## 5. 既に還元された（＝却下済みの）主張（→ ガイド §6.4）

**同じ経路の再探索を避けるために渡す。**
ただしリストにある機構へ無理に当てはめる偽陽性が増える副作用がある。
カスタム指示の「具体的な写像を数式で示せ」で潰す前提。判定が雑になったらこの節を外す。

出典：`docs/source-material/RISEI_Unique_Phenomena_Computation_Summary_and_Search_Strategy_2026-07-23.tex`（2026-07-23完了）。

| 主張 | 還元先 | 写像・極限操作 | 判定日 |
|---|---|---|---|
| Response–Mechanism Contextuality（reduced sector gluing obstruction） | shared ancilla enlargement | 共有ancillaを含む単一のcontext-independent additive GKSL模型への埋め込み | 2026-07-23 |
| 平均に盲目な protocol-order fluctuation | tilted-GKSL / FCS | standard tilted generatorでexact再現（最大誤差 \(1.84\times10^{-8}\)） | 2026-07-23 |
| Relative-gauge exact witness \(\Delta K_2=2\ell_Y(G-I)r_X\) | switched GKSL / FCSの代数 | write/relative-defect/read の三因子分解として導出可能 | 2026-07-23 |
| Continuous quantum gauge（\(SU(d)\) tree calibration atlas） | （非還元性未確立） | tree calibrationでの予測圧縮則が破綻。一般則としては不成立 | 2026-07-23 |
| Held-out quotient predictor | compact-group synchronization | 中立latent-frame estimatorと目的関数が完全一致（残差0） | 2026-07-23 |
| Global cycle-consistent quotient atlas（cycle threshold / abstention） | compact-group synchronization / 構造化系同定 | 予測値・fit residual・abstention判定が完全一致 | 2026-07-23 |
| Tube calculus（regular branch）全般 | Riesz理論 + Schur complement + Zeno型縮約 + 制御/realization理論 | 個別の再構成による説明可能性（凍結・保留、棄却ではない） | — |

> **探索順序の教訓：** 競合理論族を先に固定し、それが満たす恒等式・resource lower boundを先に抽出してから、
> それを破るwitnessを逆設計する順序に転換すること（現象を先に構成して後から還元監査する順序は非効率）。

### 5.1 上記のうち「最終監査まで生き延びた」4件の到達点

**単純な還元では死んでいない候補。** 判定時、命題がこれらと同じ構造に到達しているだけでは
非還元性の根拠にならないことに注意する。

| 候補 | 到達点 | 死因 |
|---|---|---|
| Matched operational equivalence | 単独介入で spectrum・stationary state・1〜4次cumulant一致（`D_TV≤1.40e-16`）。深さ2でvarianceのみ分裂。最小分離資源 `(d_min,k_min)=(2,2)`、`N_5%≤137` | 下記3件と共に最終監査で棄却 |
| Exact second-cumulant witness | `ΔK_2=2ℓ_Y(G−I)r_X`。48例で最大残差 `1.64e-15`、ランダムMarkov 1500模型で非零率99.4%、量子GKSL 300模型で100% | switched GKSL + FCS の代数から導出可能 |
| Held-out quotient predictor | 20 calibrationから未使用30 protocolを数値精度内で予測。point gauge回収35/36 に対し held-out予測は36/36成功 | 中立compact-group latent-frame estimatorと**目的関数・予測値・残差が完全一致（残差0）** |
| Global cycle quotient atlas | 冗長度1.5で tree estimatorの誤差 `8.40e-3` → `5.81e-16` に回復。161 calibration ⇒ 217 held-out予測。ABSTAIN certificate付き | 同上。ABSTAIN判定まで中立モデルと一致 |

**4件すべての死因は同一：pairwise relative-chart因子化 `G_ij = X_j X_i^{-1}` への還元。**
「局所同値 → 大域的obstruction → 有限資源certificate」という構造を達成しても、それ自体は固有性にならない。

---

## 6. 競合理論族の資源予算（Priority 0 凍結値）

出典：ChatGPT提案、2026-07-25。「まず現象を構成してから還元監査する」順序を反転し、
**競合理論族の資源上限を先に凍結してから、それを破る構成を逆設計する**ための土台。
標準監査で早期killされなかった候補だけ、拡張・最終kill監査まで上げる。

### 6.1 共通の資源上限

| 項目 | 標準監査 | 拡張・最終kill監査 |
|---|---|---|
| 介入数 m | 3–6 | 7, 8 |
| protocol depth d | 1–3 | 4 |
| cumulant / functional order k | 1–3 | 4 |
| hidden dimension D | 1–4 | 5, 6 |
| memory depth μ | 1–2 | 3 |
| 自由実数パラメータ数 P | ≤128 | ≤256 |
| optimizer restart | 16 | 32 |

### 6.2 競合理論族ごとの固定値

**(a) Enlarged GKSL with hidden ancilla** — ancilla Hilbert dimension D_hidden 標準1–4／最終6、P≤256、jump operator数最大 2·D_hidden+m、protocol depth d≤4、初期相関は原則積状態（許す場合はRISEI側にも同じpriorを与える）、ancilla readout禁止（観測可能量は元のvisible systemに限定）。

**(b) Tilted-GKSL / full counting statistics** — cumulant order k≤4、protocol depth d≤4、counting field数最大2、counted jump channel数最大4、hidden ancillaなし（必要なら(a)として別計上）、parameter budgetは元のvisible GKSLと同一。

**(c) Compact-group synchronization** — matrix representation dimension r_G≤4、Lie algebra dimension q_G≤15、対象群は permutation群、SO(2)、SO(3)、SU(2)、SU(3)、SU(4)およびblock表現、calibration graph redundancy ρ∈{1.0,1.5,2.0}、global optimizer restart 32、予測形式はpoint predictionまたはcertified ABSTAIN。候補にchart/gauge/relative frameがない場合はN/A可。

**(d) Controlled HMM / structured state-space identification** — hidden-state数またはrealization order D≤6、input/intervention数 m≤8、output alphabet/readout channel最大4、protocol depth d≤4、P≤256、model selectionはcalibration dataだけでBICまたは交差検証、held-out利用は完全禁止。HMMと線形state-spaceは内部実装では別だが、文書上は一つの「有限hidden realization族」としてまとめる。

**(e) Bounded-memory process-tensor model** — memory Hilbert dimension D_M≤6、MPO bond dimension χ≤D_M²=36、memory depth/Markov order μ≤3、protocol depth d≤4、functional order k≤4、P≤256、local system dimensionは候補模型と同一。**full process tensorに表現できないことは要求しない** — D_M, χ, μ, d, k, Pを固定したbounded classに対するpredictive surplusのみを問う。

**(f) Active experimental design baseline** — adaptive round数最大4、選択できるcalibration protocol数最大32、calibration総shots最大1.2×10^5、objective は expected information gain またはBayesian D-optimality、posterior sample数4096、optimizer restart 32、held-out protocolへの問い合わせ禁止、出力はprediction・resource estimate・ABSTAINのいずれか。

### 6.3 解析的kill gate（予算を持たない第7層）

上記6族とは別に、候補を即座に殺せるsymbolic reduction layerを必須監査として置く：
BCH / nested commutator expansion、Dyson path expansion、Krylov reachability / labelled path counting、
Schur complement / Zeno reduction、Kalman controllability・observability、quantum regression theorem、
symmetry・selection-rule reduction。文書表記は「**競合モデル6族＋解析的reduction gate**」。

> 実例：三者不可約応答候補（Ω_i=Ω_ij=0, Ω_123≠0）は頑健に成立したが、四状態Markov過程のlabelled
> reachabilityとDyson path expansionへ直ちに還元された。6族だけでは同じ候補を再発掘する。

### 6.4 共通prior・calibration・noise（凍結）

- **prior**: J_ref=1、γ,κ∼LogUniform(10⁻²,10²)、ReH_ij,ImH_ij∼Uniform(−1,1)
- 初期状態とreadoutは候補生成後に変更しない。nuisance parameterは候補・競合の両方へ同じpriorで与える
- sectorラベルをRISEI側だけに与えない。priorに含めるなら競合側にも同じラベル付きgenerator情報を与える
- **calibration graph**: depth1は全protocol、depth2はρ=1.5の連結グラフ（両順序測定）、depth3は24protocolをseed固定で選択、depth4はcalibration対象外
- **shots/noise**: 1protocolあたり2,000shots、総上限1.2×10^5shots。通常productionは相対calibration noise 1%、stress testは3%。control-amplitude drift標準偏差1%、timing jitterはpulse長の0.5%
- **held-out**: depth2の未使用edge、depth3の未使用protocol、depth4から事前固定した64protocol（sampling seed: 20260723）。候補生成・hyperparameter調整・停止判定には一切使用しない。active design baselineもheld-outへ問い合わせない

---

## 7. 未解決の異常・矛盾（→ ガイド §6.3）

> **前提：現時点で確定した理論間矛盾はない。** 以下は、既存理論のどれが支配するか未決着である境界、
> 数値現象と一般証明の間の不一致、有限資源下でのpredictive-surplus候補である。

| 項目 | 現状 | 次の最短検証 |
|---|---|---|
| Resource-bounded same-data gap | 単純な三者応答はreachabilityへ還元された。しかしpath support・path count・低次mixed Krylov momentsを一致させたcancellation-protected ternary pairは未検証 | §6の予算で6族を固定し、depth≤2をmatched、depth3をheld-out witnessとして逆設計 |
| 有限gap exact zeroと漸近zeroの差 | 数値的machine zeroはあるが、有限gapでのfull-Liouvillian対称性証明がない。一般に証明されているのは漸近抑制のみ | full Liouvillianと候補superoperatorのcommutatorをSymPyでexact判定 |
| Exact / approximate kernel crossover | 裸のΓε/γ₀ collapseは失敗。projected slow-loss jetは凍結模型で成功したが、一般クラスの十分条件は未証明 | 2つ以上の新architectureでblind jet prediction |
| Calibration redundancy boundary | calibration数を増やしても誤差が単調に減らず、ρ=1.5で突然EXACTになる例がある。group synchronizationは再現するが境界定理がない | observability Gram spectrumからPREDICT/ABSTAIN境界を事前予測 |

**RISEI固有現象探索の最短起点は1番目**（Priority 1 productionへ直結）。
**最短の数学的定理プロジェクトは2番目**（新理論に直結しなくても、exact/asymptoticの論理的不整合を短距離で決着できる）。

---

## 8. 対象外（判定に持ち込まないもの）

- 投稿先の選定・新規性の価値判断（これは人間側の判断）
- 文章表現の良し悪し
