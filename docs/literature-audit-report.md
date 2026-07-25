# 競合文献監査報告 — Pass 1

**監査日:** 2026-07-25  
**基準:** `docs/literature-audit-specification.md`  
**主対象:** P0 Resource-bounded mechanism separation  
**副対象:** P0 Interface realizability  
**状態:** 初回の広域監査。書誌と中心定理を確認済み。具体的candidateが未確定のため、最終的な新規性判定ではなく、最強のkill経路と次の設計制約を確定する。

---

## 0. 結論

現時点で中心問題をそのまま解いた単一の先行研究は確認されていない。しかし、現在の表現のままでは新規性を維持できない。特に次の二文献群が強い。

1. **有限HMM・state-spaceのminimal realization**  
   一般位置の有限HMMは有限長word確率からminimal realizationを復元でき、線形系ではHankel rankがminimal orderを与える。したがって「低depthで一致して高depthで分裂する」だけでは不十分である。本命は一般位置ではなく、**cancellation-protected / rank-deficient例外集合における、凍結資源内のlower bound**として定式化する必要がある。

2. **Higher-Order Group Synchronization**  
   pairwise ratio `G_ij = X_j X_i^{-1}` を破ってdepth 3のconnected objectへ移るだけでは不十分である。Duncan–Kileel (2025) はhypergraph上のtriple / n-wise local informationを直接同期し、同期可能性の必要十分条件とmessage-passing frameworkを与える。競合族Cはpairwise synchronizationだけでなく、**hyperedge order 3–4のhigher-order synchronization**を含めなければならない。

これに加え、process tensor / quantum comb はunrestricted representation criterionをほぼ完全に覆う。したがって新規性は「表現できない」ではなく、`D_M≤6, χ≤36, μ≤3, d≤4, P≤256, shots≤1.2×10^5` の下での予測不能性、または必要資源の下限に置くべきである。

**暫定判定:** `Prior-art killなし / Strong competitorあり / 中心命題の再定式化が必要`

---

## 1. 最重要のprior-art threat

### T1. Huang–Ge–Kakade–Dahleh (2016): finite-string HMM realization

- **文献:** *Minimal Realization Problems for Hidden Markov Models*, IEEE Transactions on Signal Processing 64, 1896–1904 (2016)
- **DOI:** `10.1109/TSP.2015.2510969`
- **arXiv:** `1411.3698`
- **status:** Conditional exact theorem（general-position HMM）
- **主結果:** 出力alphabet sizeを `d_out`、hidden orderを `k_HMM` とすると、measure-zero集合を除き、有限長wordのjoint probabilityからminimal quasi-HMM / HMM realizationを効率的に復元できる。arXiv abstractは `N > 4 ceil(log_{d_out} k_HMM)+1` を掲げ、本文はHankel / tensor-rank条件を明示する。
- **写像:** intervention labelをinput symbol、measurement outcomeをoutput symbol、protocol wordをfinite string、held-out responseを未観測word probabilityへ写す。
- **脅威:** depth≤2 matched / depth3 splitが一般位置で起こるなら、有限word realizationが全過程を固定する可能性が高い。
- **残る差分:** 本リポジトリの候補はcontrolled quantum processであり、stationary autonomous HMMではない。また、狙うcancellation-protected pairはまさにgeneral-position仮定を外れる可能性がある。
- **必要対応:** 候補ごとにgeneralized Hankel matrixを構成し、rank、smallest nonzero singular value、exceptional algebraic varietyをexactに記録する。

### T2. Duncan–Kileel (2025): higher-order synchronization

- **文献:** *Higher-Order Group Synchronization*
- **arXiv:** `2505.21932`
- **status:** Preprint; exact compatibility theorems + algorithmic guarantees
- **主結果:** hypergraph上のtriple / n-wise local informationからglobal group elementsを推定する一般枠組み。higher-order synchronizabilityの必要十分条件、compact group向けmessage passing、outlier/noise下の収束保証を与える。
- **写像:** depth-3 connected calibration objectをhyperedge potential、interface chartをvertex potential、protocol consistencyをhypergraph cycle consistencyへ写す。
- **脅威:** 「pairwise因子化を破ったためgroup synchronizationではない」という非還元性主張を直接無効化する。
- **残る差分:** quantum responseのfunctional、GKSL physicality、finite-shot予測を扱うわけではない。candidateのconnected tensorがgroup-valued hyperedge potentialへ写ることを示す必要がある。
- **必要対応:** 競合族Cにhyperedge order `h=3,4` を追加し、CHMP型baselineを実装する。

### T3. Chiribella–D’Ariano–Perinotti (2009): quantum comb realization

- **文献:** *Theoretical framework for quantum networks*, Physical Review A 80, 022339 (2009)
- **DOI:** `10.1103/PhysRevA.80.022339`
- **arXiv:** `0904.4483`
- **status:** Exact representation / realization framework
- **主結果:** causal quantum networkをquantum combとして表し、link productとdilationで逐次networkを実現する。
- **脅威:** unrestricted process/interface representationの不存在を新規性の核にできない。
- **残る差分:** 本リポジトリが問うのは単一の固定physical interface、有限memory、有限parameter、同一priorの下での**共通実現可能性**である。combごとに別ancilla・別networkを許す存在定理とは異なる。
- **必要対応:** Interface realizabilityは「各counterfactualの個別dilation」ではなく、「固定processor / fixed coupling / bounded program registerを共有する族のcompatibility」と定義する。

### T4. Pollock et al. (2018), Taranto et al. (2019): process tensor and quantum Markov order

- **文献:**
  - *Operational Markov Condition for Quantum Processes*, PRL 120, 040405 (2018), DOI `10.1103/PhysRevLett.120.040405`
  - *Non-Markovian quantum processes: Complete framework and efficient characterization*, PRA 97, 012127 (2018), DOI `10.1103/PhysRevA.97.012127`
  - *Quantum Markov Order*, PRL 122, 140401 (2019), DOI `10.1103/PhysRevLett.122.140401`
- **status:** Exact operational framework / conditional finite-memory results
- **主結果:** process tensorは任意のcontrol sequenceに対するmulti-time statisticsを与える。量子Markov orderは一般にinstrument-specificであり、単純な状態CMIだけでは尽くせない。
- **脅威:** multi-time / intervention dependenceそのものは既知。full process tensorに表現できることは新規性にならない。
- **残る差分:** bounded `D_M, χ, μ, P, shots` 下のpredictive surplusとlower bound。

### T5. Guo–Modi–Poletti (2020) および White et al. (2024/2025): MPO process learning

- **文献:**
  - *Tensor network based machine learning of non-Markovian quantum processes*, PRA 102, 062414 (2020), DOI `10.1103/PhysRevA.102.062414`, arXiv `2004.11038`
  - *Practical learning of multi-time statistics in open quantum systems*, arXiv `2412.17862`
  - *Unifying non-Markovian characterisation with an efficient and self-consistent framework*, arXiv `2312.08454`
- **status:** Numerical / experimental learning frameworks
- **主結果:** process tensorをMPO/LPDOとして学習し、未使用instrument sequenceのmulti-time statisticsを予測する。bond dimensionをeffective memory resourceとして扱う。
- **資源監査:** White et al. の実機例は3-step marginalsの推定に約 `4.4×10^7` shotsを用いており、本リポジトリの `1.2×10^5` shot上限を大幅に超える。ただしこれはlower boundではなく、実装例のcostにすぎない。
- **脅威:** held-out protocol prediction自体は既知。
- **必要対応:** candidate processのminimal temporal Hankel rankまたはoperator Schmidt rankから `χ>36` を証明する。単なるoptimizer failureは採用しない。

---

## 2. 競合族別判定

| 族 | 最強の既知能力 | 凍結予算への含意 | 暫定判定 |
|---|---|---|---|
| A Hidden-ancilla enlarged GKSL | structured bathを少数pseudomodeへ埋め込むexact Lindblad mappingが存在 | pseudomodeはbosonicでHilbert次元が無限の場合が多く、`D_hidden≤6`へ直ちには入らない | Strong competitor / direct killではない |
| B Tilted-GKSL / FCS | arbitrary driving protocol下のwork/heat statistics、quantum-jump trajectoryの全cumulantをtilted generatorで生成 | cumulant order≤4の順序依存は原則FCS側の守備範囲 | 既存候補をkill済み。新候補はFCS null identityを先に固定 |
| C Group synchronization | pairwise compact-group同期に加えhigher-order hypergraph同期が存在 | `h=3,4` baseline追加が必須 | Strong competitor |
| D Controlled HMM / state space | Hankel rankでminimal order、finite stringsからgeneric HMM realization、finite-sample Ho–Kalman | depth-3 splitだけでは不足。rank-deficient例外集合の証明が必要 | Strongest competitor |
| E Bounded-memory process tensor | full multi-time representation、MPO compression、instrument-specific Markov order | 新規性は `χ>36` または `μ>3` のlower boundへ限定 | Strong competitor |
| F Active design | Bayesian sequential design、adaptive process tomography、model-aware RL | 4 rounds / 32 protocols / 1.2e5 shotsでの性能を実装比較する必要 | Baseline。一般的kill theoremは未確認 |
| G Analytic gate | Schur/Zeno、Krylov/Hankel、symmetryで即時還元可能 | 数値探索の前にsymbolic check必須 | Mandatory kill layer |

---

## 3. 各族の主要文献と具体的差分

### A. Hidden ancilla / Markovian embedding

1. Pleasance, Garraway, Petruccione, *Generalized theory of pseudomodes for exact descriptions of non-Markovian quantum processes*, PRR 2, 043058 (2020), DOI `10.1103/PhysRevResearch.2.043058`, arXiv `2002.09739`.
   - Lorentzian structured spectral densityをdiscrete modes＋Markov reservoirsへexact mapping。
   - **差分:** finite-dimensional ancilla上限ではなくbosonic pseudomode。一般のcontrolled counterfactual familyのcommon interface theoremではない。

2. Tamascelli et al., *Nonperturbative Treatment of Non-Markovian Dynamics of Open Quantum Systems*, PRL 120, 030402 (2018), DOI `10.1103/PhysRevLett.120.030402`.
   - environment correlation matchingによるauxiliary open system mapping。
   - **差分:** resource-minimalityとheld-out control predictionを与えない。

3. Park et al., *Quasi-Lindblad pseudomode theory for open quantum systems*, PRB 110, 195148 (2024), DOI `10.1103/PhysRevB.110.195148`.
   - pseudomode representationを拡張し、効率的近似を与える。
   - **差分:** quasi-Lindblad表現を含み、candidate側のGKSL-admissible classと同一ではない場合がある。

### B. Tilted-GKSL / FCS

1. Esposito, Harbola, Mukamel, *Nonequilibrium fluctuations, fluctuation theorems, and counting statistics in quantum systems*, RMP 81, 1665 (2009), DOI `10.1103/RevModPhys.81.1665`.
2. Garrahan, Lesanovsky, *Thermodynamics of Quantum Jump Trajectories*, PRL 104, 160601 (2010), DOI `10.1103/PhysRevLett.104.160601`.
3. Silaev, Heikkilä, Virtanen, *Lindblad equation approach for the full counting statistics of work and heat in driven quantum systems*, PRE 90, 022103 (2014), arXiv `1312.3476`.

**監査結論:** mean-blind variance、protocol-order cumulant splitting、trajectory large deviationは既知形式へ還元される。新候補は同一tilted generator・counting fields≤2・counted channels≤4でcalibrationをexact matchedした上で、held-out functionalを破る必要がある。

### C. Compact / higher-order group synchronization

1. Perry et al., *Message-passing algorithms for synchronization problems over compact groups*, CPAM 71, 2275–2322 (2018), arXiv `1610.04583`.
2. Lerman, Shi, *Robust Group Synchronization via Cycle-Edge Message Passing*, FoCM (2022), arXiv `1912.11347`.
3. Liu, Yue, So, *A Unified Approach to Synchronization Problems over Subgroups of the Orthogonal Group*, arXiv `2009.07514`.
4. Duncan, Kileel, *Higher-Order Group Synchronization*, arXiv `2505.21932`.

**監査結論:** quotient atlasとcycle consistencyは完全に競合側の既知問題。higher-order connected witnessも自動的には逃げ道にならない。

### D. HMM / structured realization

1. Huang et al. (2016), DOI `10.1109/TSP.2015.2510969`.
2. Sarkar, Roozbehani, Dahleh, *Minimal Realization Problems for Jump Linear Systems*, CDC 2018, arXiv `1809.05948`.
3. Oymak, Ozay, *Non-asymptotic Identification of LTI Systems from a Single Trajectory*, arXiv `1806.05722`.
4. Ohta, *On the Realization of Hidden Markov Models and Tensor Decomposition*, IFAC-PapersOnLine 54, 725–730 (2021), DOI `10.1016/j.ifacol.2021.06.170`, arXiv `2008.11487`.
5. Aloy et al., *Identifiability and minimality bounds of quantum and post-quantum models of classical stochastic processes*, arXiv `2509.03004`.

**監査結論:** 最優先。candidateごとにclassical/quantum Hankel objectを構成し、`rank>6` またはQHMM lower bound `d_min>6` を示さない限り、bounded hidden realizationとの差分は主張できない。

### E. Process tensor / bounded memory

上記T4–T5に加え、Markov orderがinstrument-specificであるため、候補側だけに有利なinstrumentを選んではならない。競合にも同じinstrument setを与える。`χ≤36` はansatzの上限であり、minimal bond dimensionの認証が必要である。

### F. Active experimental design

1. Granade et al., *Robust Online Hamiltonian Learning*, NJP 14, 103013 (2012), DOI `10.1088/1367-2630/14/10/103013`, arXiv `1207.1655`.
2. Pogorelov et al., *Experimental adaptive process tomography*, PRA 95, 012302 (2017), DOI `10.1103/PhysRevA.95.012302`, arXiv `1611.01064`.
3. Belliardo et al., *Model-aware reinforcement learning for high-performance Bayesian experimental design in quantum metrology*, Quantum 8, 1555 (2024), DOI `10.22331/q-2024-12-10-1555`, arXiv `2312.16985`.
4. Wallace et al., *Learning the dynamics of Markovian open quantum systems from experimental data*, arXiv `2410.17942`.

**監査結論:** adaptive designは予算内で必ず勝つという定理ではないが、固定calibrationとの差がactive selectionの不足である可能性を排除するbaselineとして必須。

### G. Analytic reduction

1. Azouit, Sarlette, Rouchon, *Adiabatic elimination for open quantum systems with effective Lindblad master equations*, arXiv `1603.04630`.
2. Burgarth et al., *Generalized Adiabatic Theorem and Strong-Coupling Limits*, Quantum 3, 152 (2019), arXiv `1807.02036`.
3. Grigoletto et al., *Exact Model Reduction for Continuous-Time Open Quantum Dynamics*, arXiv `2412.05102`.

**監査結論:** Zeno/Schur/Krylov reductionは後処理ではなくcandidate生成前のsymbolic gateに置くべきである。

---

## 4. 中心命題への含意

### 4.1 維持できない表現

次の表現では新規性を主張できない。

- 「multi-time responseはsingle-time responseから分からない」
- 「pairwise dataが一致してもtriple dataが異なる」
- 「hidden ancillaを入れれば説明できるが大きい」— 最小次元の証明がない場合
- 「process tensorなら表現できるが非効率」— sample / bond lower boundがない場合
- 「pairwise group synchronizationでは説明できない」— higher-order synchronization未監査の場合

### 4.2 推奨する修正版

> 同一の凍結calibration datasetを与えられた競合族A–Fのうち、資源制約 `D_hidden,D_M≤6`, `χ≤36`, `μ≤3`, `d≤4`, `k≤4`, `P≤256`, `shots≤1.2×10^5` を満たすいかなるモデルも、事前固定されたdepth-3/4 held-out witnessを所定誤差以下で予測できない。一方、候補理論は同じ情報と資源で予測する。

これは存在命題だけでは弱い。最小限、次のどれかが必要である。

- exact Hankel-rank / operator-Schmidt-rank lower bound
- bounded-memory / hidden-dimension witness
- information-theoretic shot lower bound
- null identity violation
- fixed-interface compatibility no-go

---

## 5. 競合予算への修正提案

1. **C族を拡張:** pairwise compact-group synchronizationに加え、hyperedge order `h=3,4` のhigher-order synchronizationを含める。
2. **D族を分離記録:** classical HMM、quasi-HMM / observable operator model、QHMM、switched linear realizationを内部では別baselineとして扱う。
3. **E族にrank certificateを追加:** fitted bond dimensionだけでなく、temporal cutごとのoperator Schmidt spectrumとcertified lower boundを報告する。
4. **A族とE族の二重計上防止:** ancilla dimension `D_hidden` とprocess-tensor bond `χ` の変換関係を同一candidateで明示する。
5. **F族に失敗判定を追加:** posterior predictive coverageとABSTAINを許し、点予測の強制失敗を新規性に数えない。

---

## 6. 次の最短作業

1. candidateを一つに固定する前に、neutral notationでcalibration/held-out tensorを定義する。
2. generalized Hankel matrixとtemporal operator-Schmidt matrixをsymbolicまたはexact arithmeticで構成する。
3. 目標lower boundを `rank > 6`、`χ > 36`、または必要hyperedge order `>4` のいずれかに固定する。
4. Higher-Order Group Synchronizationを含むC族baselineを追加する。
5. 同じcandidateについて、comb/process-tensorのunrestricted representationとbounded representationを明確に分離する。
6. この監査を候補命題ごとの独立文献照合へ移す。理論名は伏せ、定義と命題だけを用いる。

---

## 7. 監査限界

- 具体的candidateがまだ凍結されていないため、文献とのexact mappingはfamily-levelに留まる。
- arXiv `2505.21932`, `2509.03004`, `2412.17862`, `2410.17942`, `2412.05102` は査読状況を個別に再確認する必要がある。
- PDF本文の一括保存はこのcommitでは行わず、合法的なopen-access URLと版を `references/manifest.csv` に記録した。
- 「該当文献を発見できなかった」ことは非還元性の証拠に数えていない。
