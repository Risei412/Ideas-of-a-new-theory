# 文献監査追補 — Compatibility / Common Dilation と Sample-Complexity Lower Bounds

**監査日:** 2026-07-25  
**対象:** P0-1 Interface realizability / survival certificate  
**既存基準:** `docs/literature-audit-specification.md`  
**既存監査:** `docs/literature-audit-report.md`  
**状態:** Pass 2。文献26件を追加し、既存30件と合わせて56件を索引化した。

---

## 0. 結論

### (a) Compatibility / common dilation

`dilation frustration` は、定義を凍結しない限り新概念とは判定できない。既知の channel compatibility、instrument compatibility、quantum channel marginal problem、programmability が直接の prior-art threat である。

特に危険なのは次の三結果である。

1. **Heinosaari–Miyadera (2017):** 二つのチャネルがcompatibleであることと、一方が他方のStinespring complementary channelのpost-processingであることを結び付ける。
2. **Leppäjärvi–Sedlák (2024):** instrument compatibilityについて、complementary instrumentのpost-processingによる対応物を与える。
3. **Hsieh–Lostaglio–Acín (2022):** 複数の局所ダイナミクスが一つのglobal channelのmarginalになり得るかをquantum channel marginal problemとして定式化し、SDPとincompatibility witnessを与える。

したがって、DCITが単に

> 与えられた複数のチャネル／instrumentに同時joint extensionが存在しない

と主張するなら、既知の incompatibility / marginal problem の言い換えである可能性が高い。

一方、counterfactualが同時出力ではなく、介入ラベルに応じて一つだけ選択されるなら、通常のcompatibilityではなく **programmable processor / common implementation** が近い。この区別を外すと誤判定する。

### (b) Shot lower bound

White et al. の約 `4.4×10^7` shots は、特定の再構成手順の実装コストであって minimax lower bound ではない。この数を survival certificate に使うことはできない。

下界を主張するには、実験アクセス模型を凍結した上で、次のいずれかを証明する必要がある。

- 二点法：held-out witnessで離れる二過程のcalibration transcriptを近く保ち、channel discriminationのconverseから必要shot数を下げる。
- packing + Fano法：多数のhard processesを構成し、1 query当たりのmutual informationを上から抑える。
- restricted-measurement reduction：single-copy / incoherent / no-quantum-memory等の制約下で、既知のstate/channel tomography下界へ還元する。

一般のprocess tensorに対する、任意のadaptive interventionを許した完全なminimax shot下界は、今回確認した文献群には見当たらない。従って、state/process tomographyの次元下界をそのままDCITのheld-out scalar responseへ移植してはならない。DCIT固有のhard subfamilyが必要である。

**暫定判定:**  
`(a) prior-art threat = critical`  
`(b) certificate route = viable, but access model and hard family are not yet frozen`

---

## 1. 「共通 Stinespring dilation」の曖昧性

有限個のチャネル族に対し、任意のclassical control registerと直和ancillaを無制限に許せば、各チャネルのStinespring dilationをblock-controlする共通unitaryは形式的に構成できる。従って「共通dilationが存在するか」だけでは非自明な問題にならない。

少なくとも次を別命題として区別する。

| ラベル | 問う対象 | 既知の近接分野 | 非自明化に必要な凍結 |
|---|---|---|---|
| C-JOINT | 一つのjoint channelから各チャネルをmarginalとして同時に得る | channel compatibility / channel marginal problem | 出力分割、marginal map、no-signalling条件 |
| I-JOINT | classical outcomeとquantum outputを含むjoint instrumentが存在する | parallel instrument compatibility | joint outcome、quantum output、post-processing |
| P-PROG | 同一processorにprogramを与え、counterfactualごとに別チャネルを選ぶ | programmable channels / programmable instruments | program次元、program state、processor、誤差 |
| D-SHARED | 同じisometry・environment state・couplingから、許されたreadout/controlだけで族を得る | Stinespring complement / post-processing preorder | isometry、environment初期状態、許可する後処理 |
| R-BOUND | 上記の実装は存在するが、凍結ancilla/program/memory上限では不可能 | incompatibility robustness / memory cost | `D_E`, `D_prog`, `χ`, `μ`, error norm |

DCITの `dilation frustration` は、C-JOINT/I-JOINTなら既知結果に近い。P-PROG/D-SHARED/R-BOUNDなら差分が残り得るが、共有資源と自由操作を明記しなければならない。

---

## 2. Compatibility 文献群（H）

### H01–H04: 基礎定義、complementary channel、witness

1. **H01 Heinosaari–Miyadera–Ziman (2016), _An invitation to quantum incompatibility_**  
   measurementからchannelまでのcompatibilityを整理するreview。定義と記法の入口。

2. **H02 Heinosaari–Miyadera (2017), _Incompatibility of quantum channels_**  
   compatible channelsを一つのbroadcasting channelのmarginalとして定義。Stinespring complementary channelとpost-processingを用いるcharacterizationが、DCITのcommon-dilation主張に最も直接的。

3. **H03 Kuramochi (2018), _Quantum incompatibility of channels with general outcome operator algebras_**  
   outcome algebraを一般化し、channel compatibilityをconcatenation/conjugationで特徴付ける。classical outcomeとquantum outputを同じ言葉で扱う際に必要。

4. **H04 Carmeli–Heinosaari–Toigo (2019), _Witnessing incompatibility of quantum channels_**  
   incompatibility witnessをaffine functionalとして構成し、state-discrimination taskとの operational meaning を与える。DCIT witnessが既知witness coneと一致するかを検査する基礎。

### H05–H07: Marginal problem / SDP

5. **H05 Haapasalo–Kraft–Miklin–Uola (2021), _Quantum marginal problem and incompatibility_**  
   state marginal problemとchannel incompatibilityを対応付け、互換性判定のSDP hierarchyを与える。

6. **H06 Girard–Plávala–Sikora (2021), _Jordan products of quantum channels and their compatibility_**  
   channel compatibilityをstate marginal problemへ写し、SDP formulationと十分条件を与える。

7. **H07 Hsieh–Lostaglio–Acín (2022), _Quantum Channel Marginal Problem_**  
   「局所ダイナミクス群が一つのglobal dynamicsとcompatibleか」を直接扱う。SDPとincompatibility witnessを含み、P0-1に対する最優先のkill文献。

### H08–H10: Instrument compatibility

8. **H08 Mitra–Farkas (2022), _On the compatibility of quantum instruments_**  
   traditional compatibilityとparallel compatibilityを区別し、後者がmeasurement/channel compatibilityをともに含むと論じる。counterfactualの出力意味論を凍結する際に必須。

9. **H09 Mitra–Farkas (2023), _Characterizing and quantifying the incompatibility of quantum instruments_**  
   parallel incompatibility robustnessとfree post-processingを解析。bounded-resource版へ接続する。

10. **H10 Leppäjärvi–Sedlák (2024), _Incompatibility of quantum instruments_**  
    instrument compatibilityとcomplementary instrumentのpost-processingによるcharacterizationを与える。H02のinstrument版に最も近い。

### H11–H12: Programmability

11. **H11 Ji–Chitambar (2024), _Incompatibility as a Resource for Programmable Quantum Instruments_**  
    programmable instrument deviceとquantum memory resourceを扱う。counterfactualが排他的に選択されるDCIT interfaceには、simultaneous compatibilityよりこちらが近い可能性がある。

12. **H12 Buscemi–Chitambar–Zhou (2020), _A Complete Resource Theory of Quantum Incompatibility as Quantum Programmability_**  
    incompatibilityをprogrammable measurement deviceのresource theoryとして特徴付ける。`dilation frustration` のresource-theoretic再記述を監査する基礎。

---

## 3. Sample-complexity lower-bound 文献群（L）

### L01–L03: Shadow / state tomography

1. **L01 Aaronson (2018), _Shadow Tomography of Quantum States_**  
   多数の既知測定の期待値を同時推定する問題を定式化し、次元・測定数・精度に依存するlower boundを与える。DCITへ使う場合、process Choi stateと許可測定の対応を明示する必要がある。

2. **L02 Chen–Cotler–Huang–Li (2022), _Exponential separations between learning with and without quantum memory_**  
   quantum memoryなしのshadow tomographyに `Ω(min(M,2^n))` 型下界を与え、memory/sample trade-offを示す。DCITの実験装置がshot間のquantum memoryを持たない場合に直接関係する。

3. **L03 Lowe–Nayak (2025), _Lower bounds for learning quantum states with single-copy measurements_**  
   single-copy measurement、measurement familyの固定、adaptivityの有無を分けたstate/shadow tomography下界。アクセス模型を曖昧にしないための基準。

### L04–L08, L14: Channel / process tomography

4. **L04 Oufkir (2023), _Sample-Optimal Quantum Process Tomography with Non-Adaptive Incoherent Measurements_**  
   non-adaptive incoherent measurementでは、diamond-norm process tomographyに `Ω(d_in^3 d_out^3 / ε^2)` copiesが必要。ancilla-assistedでも成立。

5. **L05 Fawzi–Oufkir–França (2025), _Lower Bounds on Learning Pauli Channels with Individual Measurements_**  
   Pauli channel学習に対し、non-adaptive/adaptive individual-measurement模型の指数的dimension下界を与える。structured competitorにもhard familyが存在することを示す。

6. **L06 Wilde–Berta–Hirche–Kaur (2020), _Amortized Channel Divergence for Asymptotic Quantum Channel Discrimination_**  
   adaptive channel discriminationのconverseを構成する道具。DCIT固有の二点法で、任意adaptive policyのtranscript distinguishabilityを抑える候補。

7. **L07 Mele–Bittel (2026), _Optimal learning of quantum channels in diamond distance_**  
   Kraus rank `k` を含む一般チャネル学習のquery scalingをほぼ決定。full channel tomographyをcertificateに使う場合のdimension baseline。

8. **L08 Oufkir–Girardi (2026), _Improved Lower Bounds for Learning Quantum Channels in Diamond Distance_**  
   diamond distance学習に明示的な `ε` 依存を持つnear-optimal lower boundを与える。coherent queryを含む一般的模型との距離を測る。

14. **L14 Bravo-Prieto–Gong–Mele (2026), _Quantum memory advantage for quantum process tomography_**  
    adaptive incoherent protocolsを含むno-quantum-memory模型で `Ω(d_in^3 d_out^3 / ε^2)`、coherent protocolsで `Θ(d_in^2 d_out^2 / ε^2)` を与える。2026-07-15公開の新しいpreprintであり、P0 shot予算に最も近いが、査読前として扱う。

### L09–L11: Lindbladian learning

9. **L09 Ivashkov et al. (2026), _Ansatz-Free Learning of Lindbladian Dynamics In Situ_**  
   sparse Lindbladian学習を扱い、粗いtime resolution等のアクセス制約がsample complexityを悪化させるhard instancesを解析する。DCITのtime gridを凍結する必要性を示す。

10. **L10 Arad–Chen–Guo–Rebentrost–Yu (2026), _Near-Optimal Learning of Local Lindbladians_**  
    local Lindbladian係数学習について、`Ω(Λ^2/ε^2)` channel usesと `Ω(Λ/ε^2)` total evolution timeを、adaptive algorithms・arbitrary ancillas/measurementsにも成立する形で示す。

11. **L11 Möbus–Bergamaschi–França–Rouzé (2026), _Robust Structure Learning of k-local Lindbladians_**  
    product-state preparation、short time、local Pauli measurement等のrestricted access下でのlower boundを含む。DCIT実験模型に近ければ直接使える。

### L12–L13: Multi-time learningへの橋

12. **L12 Raza–Caro–Eisert–Khatri (2024), _Online learning of quantum processes_**  
    multi-time processを含むonline learningを扱うが、中心はmistake/computational boundsであり、一般のshot-minimax lower boundそのものではない。

13. **L13 Kunjummen–Tran–Carney–Taylor (2023), _Shadow process tomography of quantum channels_**  
    process Choi stateとshadow estimationを接続する上界側の基礎。L01–L03の下界をchannel/processへ移す際の測定対応を点検するために必要。

---

## 4. DCITに対する compatibility kill test

候補counterfactual familyを `{\mathcal N_x}_{x∈X}`、instrument familyを `{\mathcal I_x}` とする。

### Test A: joint-channel / marginal SDP

1. 各 `\mathcal N_x` のChoi operator `J_x` を構成する。
2. H07のchannel marginal problemとして、一つのpositive semidefinite `J_joint` が各 `J_x` を所定のpartial traceで与えるかをSDP判定する。
3. infeasibleならdual witnessを抽出する。
4. DCIT witnessがこのdual coneの元と一致するなら、新規機構ではなく既知のchannel incompatibility witnessである。

### Test B: complementary-channel post-processing

1. 一つの候補チャネル `\mathcal N_1` のminimal Stinespring isometry `V` とcomplement `\mathcal N_1^c` を構成する。
2. `\mathcal N_2 = \Theta \circ \mathcal N_1^c` を満たすchannel `\Theta` の存在をCP/TP制約つきSDPで検査する。
3. instrumentの場合はH10のcomplementary instrumentへ置換する。

### Test C: programmability

counterfactualが同時出力でない場合、joint marginal testだけでは誤ったno-goになり得る。固定processor `\mathfrak P` とprogram states `π_x` について

`\mathcal N_x(ρ) = Tr_E[\mathfrak P(ρ⊗π_x)]`

を満たすかを問う。非自明な主張には `dim(program)`, `dim(E)`, program orthogonality, approximation error, allowed readout を凍結する。

### 判定

- **既知還元:** C-JOINT/I-JOINTのinfeasibilityまたは既知robustnessだけで説明できる。
- **差分候補:** P-PROG/D-SHAREDで、同時compatibilityとは異なる共有制約が本質。
- **強いsurvival:** unrestricted implementationは存在するが、任意の許容processorについて `D_prog>D_max` または `D_E>D_max` を証明。

---

## 5. DCIT固有 shot lower bound の証明テンプレート

### 5.1 先に凍結するアクセス模型

下界定理の前に次を固定する。

- 1 shotで許されるstate preparation
- intervention setとdepth
- protocol選択のadaptivity
- ancillaとshot間quantum memory
- 一つのunknown processをcoherently複数回呼ぶことの可否
- time resolutionとtotal evolution time
- measurement class
- 出力対象（full process、channel、held-out scalar witness）
- 誤差norm、成功確率 `1-δ`

### 5.2 二点法

二つの物理過程 `\Theta_0,\Theta_1` を構成し、

1. held-out targetが `|g(\Theta_0)-g(\Theta_1)| ≥ 2ε`、
2. 任意の許容1-shot queryで得られる情報が小さい、
3. calibration dataでは両者がexactまたは許容誤差内で一致、

となるようにする。任意の `n`-shot adaptive policyのtranscript分布 `P_0^{(n)},P_1^{(n)}` をWilde et al. 型amortized divergenceで

`D(P_0^{(n)} || P_1^{(n)}) ≤ n D_A(\Theta_0 || \Theta_1)`

と抑える。仮説検定converseから、誤り確率 `≤δ` に必要な

`n ≥ c_δ / D_A(\Theta_0 || \Theta_1)`

を得る。ここで `c_δ` は採用するPinsker / Bretagnolle–Huber / Stein型不等式に応じて明記する。

### 5.3 Packing + Fano法

`M` 個の過程 `{\Theta_v}` を、target metricでpairwise `2ε` 以上離し、1 query当たりmutual informationを `I_max` 以下に抑える。Fano不等式から

`n ≥ ((1-δ) log M - log 2) / I_max`

を得る。Oufkir系process tomography lower boundは、channel packingと各measurementのinformation boundを組み合わせるため、proof architectureとして最も参考になる。

### 5.4 使用禁止の推論

- 一つのalgorithmが `4.4×10^7` shotsを使った ⇒ 全algorithmがそれ以上必要
- full process tomographyが高価 ⇒ 一つのheld-out scalarも同じだけ高価
- optimizerが収束しない ⇒ information-theoretic lower bound
- classical-shadow上界が大きい ⇒ 下界も大きい
- state tomography下界 ⇒ causal intervention制約を確認せずprocess tensor下界

---

## 6. 優先読解順

### P0-1 compatibility

1. H07 channel marginal problem
2. H02 complementary-channel characterization
3. H10 complementary-instrument characterization
4. H08 traditional vs parallel instrument compatibility
5. H11 programmable instruments
6. H04/H05/H06 witness・SDP

### Shot lower bound

1. L06 amortized channel divergence
2. L04/L14 process tomography lower bounds
3. L02/L03 memory・single-copy lower bounds
4. L10 local Lindbladian minimax lower bound
5. L01 shadow tomography
6. L08 coherent diamond-distance lower bound

---

## 7. 次の実作業

1. DCITのcounterfactualを C-JOINT / I-JOINT / P-PROG / D-SHARED のどれとして主張するか一つに固定する。
2. 候補familyのChoi operatorsを作り、H07 SDPとH02/H10 post-processing testを実行する。
3. `dilation frustration` が既知dual witnessか、program/memory dimension下界かを判定する。
4. shot下界について、full tomographyではなくheld-out witnessに一致するhard pairを作る。
5. 同じpairに対してamortized divergenceまたはFano情報量を計算し、`1.2×10^5` shotsを超える条件を数式で出す。

---

## 8. 監査限界

- H/L文献の書誌、公開版、中心主張は確認したが、DCITの具体的Choi operatorsが未凍結のためexact reduction判定は未実施。
- L07–L11、L14は2026年preprintを含む。最新結果として優先索引するが、査読済み定理と同列には扱わない。
- 今回の収集は合法的な公開URLと書誌を索引化したもので、PDF binary自体はリポジトリへ追加していない。
- 「一般process tensorのminimax lower boundを発見できなかった」ことは不存在証明ではない。現時点の監査範囲で未確認という意味に限定する。
