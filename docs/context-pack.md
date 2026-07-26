# コンテキストパック（ChatGPTプロジェクトにアップロードする資料）

**このファイルは資料層である。命令を書かないこと**（命令は `redteam-instructions.md` → カスタム指示欄）。

**用途:** ChatGPTのプロジェクトに**ファイルとしてアップロード**する。
チャットごとに貼り直す必要はなく、更新時に差し替えるだけでよい。

**更新契機:** 新しい還元経路が見つかったとき／確定済み理論が増えたとき／記号を追加したとき。

---

> **記入状況（2026-07-26）:** **全節記入済み。アップロード可能。**
> §2 適用範囲・§3 抵触禁止制約をガイド §4.1／§4.2 から転記した（2026-07-26）。
> §6.4 に提案21の実測設計を追記した（2026-07-26）。

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
| **RISEI**（Generalized RISEI, End-to-End Certified） | 物理的介入protocol、full-minus-protocol応答、subset-Möbius不可約成分、操作順序、response functional、protected Riesz cluster、source/readout選択幾何、有限資源、極限順序を統合。再利用可：Möbius分解の一意性、Riesz cluster invariance、Schur–Zeno展開、response-relevant strong dissipatorが可逆な場合のresolvent抑制、選択集合の局所codimension = 実Jacobian rank、stationary linear responseへの埋め込み | 有限次元・time-local GKSL。介入後も瞬間generatorがGKSL admissible。比較間で初期状態・probe・readout・観測窓・測定規約・正規化を固定。Schur–Zeno結果にはsemisimpleなresponse-relevant protected clusterとbounded fast resolventが必要。**Pattern (b) の任意GKSL普遍性は再利用不可** |
| **SMRT**（Sector-Mediated Response Theory） | sectorを切ったcounterfactualとfull responseの差である master sector-resolved response を exact zero・algebraic suppression・protected survival へ分類。二尺度・scaling-path依存のpolyhedral拡張を含む。再利用可：full-minus-cut差分のdoubling realization、有限個のKrylov/Cayley–Hamilton momentsによるexact-zero certificate、dissipative moment hierarchyと抑制次数、`ν∈{∞, 正の有限値, 0}` の排他的三分類、有限停止decision algorithm、exact arithmeticによる認証方針 | 有限次元・Markovian・weak-probe/linear response。応答が有限次元のrational transferとして表され、source/readoutと比較規約が固定されること。強散逸族 `A_Γ(z)=ΓD+B(z)` ではどのrateをscaleするかを物理入力として固定する。protected theoremにはsemisimple kernelとprotected blockの可逆性が必要。polyhedral結果は明記されたscaling pathと正則性条件の範囲のみ |
| **EIT no-go/go**（v6.2） | 任意材料の特定configurationについて dark-state rank、Lindblad stationary dark state、Schur-complement susceptibility、sector-resolved EIT no-go/go を判定。再利用可：`dim ker Ω = N_g − rank Ω`、pure stationary Lindblad stateの必要十分条件、exact Schur-complement response、`δχ_S = χ_full − χ_cut^(S)`、regular scalar caseの `δχ_S=0 ⇔ K_12K_21=0`、Krylov exact-zero定理、first nonzero momentによる抑制次数、singular dampingのprotected channel、symmetry audit | 有限次元、time-independent Markovian GKSL、stationary rotating frame、weak probe、unique steady stateまたはtrace-zero部分空間上でwell-definedなgroup inverse。分類対象は材料名ではなくconfiguration（準位・偏光・場・温度・observable・target sector）。**非Markov浴、strong-probe saturation、伝搬支配のcollective effectは範囲外** |

**再利用時の規則（ガイド §4.1）**

1. **定理名だけを再利用しない。** 仮定・比較規約・source/readout・functional・観測窓・limit protocol を一緒に移植する
2. 既存の数値結果を使う場合、元のparameter file・単位・rate convention・precision・fit window・乱数seed・commit hash を記録する
3. **Frozen theory の結論を新理論の新規性として数えない。** 新理論は、凍結結果から何を追加で予測・禁止・分類するかを示す
4. `Exact / Conditional / Conjecture / Numerical phenomenon / Model-specific observation` の status を維持する。昇格には新しい証明または認証が要る

**凍結の外側（ガイド §4.3、確定済み理論が一般定理として保証していない領域）**

genuinely non-Markovian memory kernel・colored noise・初期system–environment相関／無限次元Hilbert–Liouville空間・essential spectrum・連続体bath／generic many-body・熱力学極限scaling・相転移／strong-probe・非線形応答・saturation・多光子非摂動領域／gain medium・unstable generator・物理周波数窓内のpole crossing／nonsemisimple zero eigenvalue・Jordan block・Puiseux/fractional scaling／scaling対象が途中で変わる多parameter path・ランダムpath・adaptive path／ideal algebraic cutの実験実装可能性／ensemble propagation・optical depth・disorder averaging・detector noise／finite-grid近似kernelからcontinuum spectrumへの外挿／ergotropy・Fisher information・entropy production等の非線形functional／unrestricted process tensor・quantum comb・causal modelへの埋め込み。

---

## 3. 抵触してはいけない制約（→ ガイド §4.2）

命題がこれらのいずれかを破る場合、**どの仮定を外したかが明示されていない限り、その命題は誤りである**。

1. **GKSL/CPTP physicality** — 物理的介入は原則としてgenerator全体をGKSL admissibleに保つ変更である。任意の行列要素の削除を実験的介入と同一視しない
2. **Fixed comparison class** — full／cut／intervened protocol を比較するとき、初期状態・probe・readout・観測窓・operator ordering・measurement scheme・normalization を固定する。変更するならそれ自体をprotocol dataとして明示する
3. **no-go対象の取り違え禁止** — EIT/SMRT の no-go 対象は全応答の零点ではなく、指定sectorによる差分 `δχ_S` または master response である。`χ_full=0` は理想EITのgo signatureになりうるのでno-go判定に使わない
4. **有限点のnumerical zeroはexact zeroではない** — exact all-frequency zero は symbolic identity・有限Krylov moment certificate・adjugate identity・対称性の完全監査で証明する。浮動小数点samplingだけで「証明済み」と書かない
5. **full-rank strong damping no-go** — response-relevant部分空間上で scaled dissipator `D` が可逆かつ逆行列が一様有界なら、固定周波数窓のbounded responseは少なくとも `O(Γ^{-1})` に抑制される。追加のsingular scalingなしに `O(1)` protected response を主張しない
6. **protected responseの必要条件** — `ker D ≠ {0}` だけでは不十分。semisimpleなresponse-relevant protected Riesz subspace、非零のprojected source/readout、可逆なprotected block、非零のprotected transfer が要る。endpoint overlapだけで保護を判定しない
7. **fixed kernel lifting no-go** — 固定した `ε>0` でresponse-relevant kernelが持ち上がり `D_ε` が可逆かつbounded inverseを持つなら、`Γ→∞` でexact-kernel型のprotected asymptotic機構は消える。finite-window crossover を asymptotic phase と呼ばない
8. **Pattern (b) の任意GKSL普遍性は禁止** — Pattern (b) は response-relevant protected kernel、Schur–Zeno coupling、selection geometry、非零residue、許容摂動、固定されたlimit protocol を要する条件付き現象である
9. **universal codimension-one は禁止** — observable-selection setの局所codimensionは active real constraint map のJacobian rankで決まる。complex scalar constraint は一般に real codimension two になりうる
10. **極限交換禁止** — `Γ→∞`、kernel lifting `ε→0`、grid/domain size、continuum、thermodynamic limit の順序を黙って交換しない。異なるlimit protocolの結果を同一視しない
11. **symmetry zeroの完全監査** — symmetry-protected zero を主張するときは、Hamiltonian・全jump operator・steady state・source・readout・control polarization を同じprojectorがreduceすることを確認する。一項でも破ればexact zeroではなくperturbative suppressionとして扱う
12. **rate convention・次元整合性** — population relaxation rate と optical-coherence damping rate を混同しない（例：対称orbital hoppingでは `Γ_XY=2k` に対し各optical coherenceのdampingは `k/2=Γ_XY/4`）。すべての無次元化と単位変換をテストする
13. **EITとAutler–Townes splittingの混同禁止** — transparency dipだけではEITを同定できない。ground-coherence依存・control-power scaling・pole/residue・two-photon linewidth・full-minus-cut差分を確認する
14. **熱力学への拡張時の制約** — GKSL形式だけから熱力学第二法則を自動的に結論しない。bath・Hamiltonian・温度・detailed balance または採用するresource-theoretic assumptions を明示し、entropy production・passivity・energy bookkeeping を独立に検証する

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
| **因果的Loewner障害／Lamb shift の作用素反単調性（CIRT C2）** | **Löwner 1934**、多ポートFosterリアクタンス定理（Cauer 1931） | 自己エネルギー↔インピーダンスの辞書で逐語一致。透明窓＝$\mathrm{supp}\,\mu$外の実区間＝Löwnerの標準仮定 | 2026-07-26 |
| **最小bathモード数 $=\mathrm{rank}\,L=$ McMillan次数（CIRT C6）** | **Youla–Saito 1967**／**Mayo–Antoulas 2007**／退化行列Nevanlinna–Pick | 前者のabstractに"minimum number of reactances"、後者の看板定理が rank(Loewner)=McMillan次数 | 2026-07-26 |
| **有限判定手続き・dual witness・全解パラメトリゼーション（CIRT §6.1）** | Nevanlinna–Pick/Schurアルゴリズム。**Fei–Yeh–Zgid–Gull, PRB 104, 165111 (2021)** | 行列値で「solutions exist iff Pick matrix is PSD」を物理誌で既述。`Nevanlinna.jl`/`TRIQS`に実装済み | 2026-07-26 |
| **「サンプル点の正値性≠受動性」（CIRT C3の枠組み）** | passivity enforcement（Grivet-Talocia 2004 ほか） | 分野の存在理由そのもの。違反は点でなく**帯**構造 | 2026-07-26 |
| **ancilla閉性（CIRT C4）** | 正実類のSchur補元・受動的相互接続での閉性（Anderson & Vongpanitlerd 1973） | $h=-\Sigma$ の符号で4行。CIRT §4.5 の符号は逆 | 2026-07-26 |
| **自己エネルギー↔インピーダンスの辞書そのもの** | **Solgun–DiVincenzo 2015**（Multiport impedance quantization） | Brune合成→量子ハミルトニアン＋最小bathモード。circuit QEDの実用手法 | 2026-07-26 |
| **語領域受動性条件 WP1（提案23／WPOT）— 「受動実現の存在 ⇒ 語領域Loewner行列 `Π_n ⪰ 0`」** | **還元ではなく反証。先行研究は不要** | 受動（KMS）実現自身が 400/400 試行で `Π_n` の両符号半正定値性を破る。語なし 1×1 スカラーで既に破れる。`R=Σ_k c_k e^{θλ_k}` で `λ_k≤0` は熱性から従うが、`c_k=⟨E,v_k⟩⟨w_k,ρ₀⟩` の正値性は従わない（source と readout が独立に選べる） | 2026-07-26 |
| **Φ階層排他ゼロ（提案25／FHOT）— 「`δχ_S≡0`（線形応答）かつ `δF_S≠0`（QFI）は非線形汎関数固有の現象」** | **有限次元トモグラフィ完全性への還元（先行研究は不要）** | 最小模型で閉形式 `F_Q=4|χ|²/Σ_A`、`χ=D_A·g(Δ)` が残差0で成立。`δχ_S≡0` は population差 `D_A` の不変性に、`δF_S≠0` は population和 `Σ_A` の変化に完全帰着し、`Σ_A=tr(ρΠ_A)` は**線形汎関数**である。有限次元でトモグラフィ可能な設定では任意の状態汎関数が線形汎関数全体から決まるため、「線形汎関数に盲目・非線形汎関数に可視」という枠組み自体が原理的に空。分類予想（`r_nc>0`が必要条件）も `r_nc=0` かつ `δF_S≠0` の明示的反例で反証 | 2026-07-26 |

> **⚠️ 「quantum surplus」は量子効果ではない。** 成分ごとのKramers–Kronigが行列受動性を
> 含意しないのは古典多ポート受動性の定義そのもの（$Z+Z^*\succeq0$ であって成分ごとではない）。
> **この語を新現象の名として使わないこと。** 出典 `docs/literature-audit-cirt-passive-realizability.md`。

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
**【2026-07-25 追加】hyperedge order `h=3,4` の higher-order synchronization を含める**（Duncan–Kileel 2025, arXiv:2505.21932）。
pairwise `G_ij=X_jX_i^{-1}` だけを競合とみなすのは不十分 — hypergraph上のtriple/n-wise同期が既に存在する。
CHMP型baselineを実装し、depth-3 connected calibration objectをhyperedge potentialへ写せるかを検査すること。

**(d) Controlled HMM / structured state-space identification** — hidden-state数またはrealization order D≤6、input/intervention数 m≤8、output alphabet/readout channel最大4、protocol depth d≤4、P≤256、model selectionはcalibration dataだけでBICまたは交差検証、held-out利用は完全禁止。HMMと線形state-spaceは内部実装では別だが、文書上は一つの「有限hidden realization族」としてまとめる。

**(e) Bounded-memory process-tensor model** — memory Hilbert dimension D_M≤6、MPO bond dimension χ≤D_M²=36、memory depth/Markov order μ≤3、protocol depth d≤4、functional order k≤4、P≤256、local system dimensionは候補模型と同一。**full process tensorに表現できないことは要求しない** — D_M, χ, μ, d, k, Pを固定したbounded classに対するpredictive surplusのみを問う。

**(f) Active experimental design baseline** — adaptive round数最大4、選択できるcalibration protocol数最大32、calibration総shots最大1.2×10^5、objective は expected information gain またはBayesian D-optimality、posterior sample数4096、optimizer restart 32、held-out protocolへの問い合わせ禁止、出力はprediction・resource estimate・ABSTAINのいずれか。

### 6.2.1 【2026-07-25】文献監査による予算の修正

出典：`docs/literature-audit-report.md` §5、`docs/literature-audit-addendum.md`。
いずれも**競合を強くする**方向の変更であり、baselineを狭める禁止規定には触れない。

1. **C族拡張** — pairwise に加え hyperedge order `h=3,4` の higher-order synchronization を含める（上記(c)）
2. **D族の内部分離** — classical HMM／quasi-HMM・observable operator model／QHMM／switched linear realization を**別baselineとして記録する**（まとめて1族として扱わない）
3. **E族に rank certificate 追加** — fitted bond dimension だけでなく、temporal cut ごとの operator Schmidt spectrum と**認証された下界**を報告する。`χ≤36` は ansatz の上限であって最小値の証明ではない
4. **A族とE族の二重計上防止** — ancilla dimension `D_hidden` と process-tensor bond `χ` の変換関係を同一candidateで明示する
5. **F族に失敗判定を追加** — posterior predictive coverage と ABSTAIN を許す。**点予測の強制失敗を新規性に数えない**

### 6.2.2 【2026-07-25】P0-1 Interface realizability の命題を凍結する必要

`docs/literature-audit-addendum.md` §1 の指摘：

> 任意の classical control register と直和ancillaを無制限に許せば、
> 各チャネルのStinespring dilationをblock-controlする共通unitaryは**形式的に構成できる**。
> 従って「共通dilationが存在するか」だけでは非自明な問題にならない。

**判定前に、命題がどの形なのかを必ず確認すること。**

| ラベル | 問う対象 | 既知の近接分野 | 判定 |
|---|---|---|---|
| C-JOINT | 一つのjoint channelから各チャネルをmarginalとして**同時に**得る | channel compatibility / channel marginal problem | **既知還元の可能性大** |
| I-JOINT | classical outcomeとquantum outputを含むjoint instrumentが存在する | parallel instrument compatibility | **既知還元の可能性大** |
| P-PROG | 同一processorにprogramを与え、counterfactualごとに別チャネルを**選ぶ** | programmable channels / instruments | 差分が残り得る |
| D-SHARED | 同じisometry・environment state・couplingから、許されたreadout/controlだけで族を得る | Stinespring complement / post-processing preorder | 差分が残り得る |
| R-BOUND | 実装は存在するが**凍結ancilla/program/memory上限では不可能** | incompatibility robustness / memory cost | 差分が残り得る |

**counterfactualが同時出力ではなく介入ラベルで排他的に選択されるなら、通常のcompatibilityではなく P-PROG が近い。** この区別を外すと誤判定する。

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
- **shots/noise**: **【2026-07-25 改訂】** `1.2×10^5` は **calibration専用上限**。held-out は独立予算で最低 `1.28×10^5`。
  `2000` shots は **1 protocol あたりではなく 1 measurement setting あたりの上限**（protocol と setting は分離計上）。
  標準探索は `m=6`、`m=8` は予算拡張を要する stress test。詳細は `docs/p0-certificate-spec.md` §4.5。通常productionは相対calibration noise 1%、stress testは3%。control-amplitude drift標準偏差1%、timing jitterはpulse長の0.5%
- **held-out**: depth2の未使用edge、depth3の未使用protocol、depth4から事前固定した64protocol（sampling seed: 20260723）。候補生成・hyperparameter調整・停止判定には一切使用しない。active design baselineもheld-outへ問い合わせない

**【2026-07-26 追記】提案21（凍結資源実現ギャップ）の実測設計** — 上の一般設計とは別に、
generalized Hankel の prefix–suffix 閉包を満たすよう次のとおり凍結した（`docs/p0-certificate-spec.md` §4quater）。

| 項目 | 値 |
|---|---|
| calibration | **長さ ≤2 の全語 43 protocol**（深さ3は含まない）。1 setting・2000 shots で 86,000 |
| witness（held-out） | **深さ4の 64 語**（行・列語が長さ2の 8×8 部分行列 `H_wit` を張る）。2000 shots で 128,000 |
| held-out seed | **20260725**（提案21用に引き直し。seed 20260723 の集合は過去候補で使用済みのため blind でない） |
| settings/protocol | ≤2、標準は 1 |
| 合計 | 107 protocol / 214,000 shots |

**43×43 の Hankel 全体は測定しない** — 深さ4語 1296 個が必要で凍結予算の 20.25 倍になるため。

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
