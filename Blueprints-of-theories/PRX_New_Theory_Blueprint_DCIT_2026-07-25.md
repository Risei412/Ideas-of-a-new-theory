# PRX候補：Dilation-Consistent Intervention Theory（DCIT）
## 開放系介入の共通実装可能性と「dilation frustration」の理論設計図

**作成日:** 2026-07-25  
**位置づけ:** RISEI／SMRTの既存成果と失敗監査を踏まえた、新しい開放量子系理論の候補設計図  
**判定:** PRX候補として優先探索する価値がある。ただし、現時点では「新理論として完成」ではなく、外部非還元性を試すための最有力設計である。

---

## 0. 結論

提案する中心理論は、

> **Dilation-Consistent Intervention Theory（DCIT）**  
> 日本語では「開放系介入の共通dilation整合性理論」

である。

中心の問いは、次のように置く。

> 有限個の介入条件の下で得られたGKSL generator族が、それぞれ個別にCPTPであるだけでなく、  
> **一つの共通したsystem–environment interfaceの異なる制御状態として同時に実現できるための必要十分条件は何か。**  
> また、共通実装が不可能な場合、その不可能性を最小の介入contextと有限の応答測定から証明できるか。

この問いは、従来の

\[
\text{各generatorがGKSLか}
\]

という「局所的な物理性」を、

\[
\text{generator族全体が一つの環境実装を共有できるか}
\]

という「大域的な物理性」へ拡張する。

理論固有の中心現象候補は、

\[
\boxed{
\text{すべての局所介入contextはCPTP}
\quad\text{だが}\quad
\text{全contextに共通するMarkovian dilationは存在しない}
}
\]

という **dilation frustration（共通実装フラストレーション）** である。

これは、tube、Zeno narrowing、EP、unravelling依存性のような一つの応答形状ではない。  
「個々のモデルが正しいこと」と「それらを同一装置のcounterfactualとして同時に語れること」が一致しない、という局所―大域現象である。

---

## 1. なぜこの方向を選ぶのか

### 1.1 既存RISEI／SMRTから引き継ぐ事実

共有資料と認証結果から、次の点はすでに明確である。

1. finite-dimensional、time-local GKSL模型族に対するSchur–Riesz tube calculusは、凍結した適用範囲ではend-to-endに認証されている。
2. Pattern (b)、tube、protocol-order fluctuation、relative gauge、quotient atlasは、現象または計算体系としては成立しても、Zeno、FCS、shared ancilla、group synchronization、structured system identificationなどへの還元を免れなかった。
3. sector cutは、Lindblad jump表現を変えると意味が変わりうる。したがって「どのchannelを切ったか」はgeneratorだけの不変量ではなく、物理interfaceの情報を必要とする。
4. Operational Newton fanは強い一般則候補だが、Newton geometryそのものは既知であり、PRXの新理論としてはphysical matched interfaceとpredictive surplusがなお必要である。

ここから分かるのは、次のことだと思う。

> これまでの理論は「介入を与えた後の応答」を精密に分類してきた。  
> しかし、その介入族がそもそも**同じ物理装置から同時に生成可能か**は、理論の外側に置かれていた。

DCITは、この手前の問題を中心にする。

### 1.2 壊す仮定

RISEIで暗黙に置いていた

> 各sector cutまたは各介入generatorは、同じ物理interfaceのcounterfactualとして利用できる

という仮定を外す。

新理論では、介入generator族を最初から物理的とはみなさない。  
まず共通dilation整合性を検査し、PASSした族にだけRISEI／SMRTのresponse calculusを適用する。

---

## 2. 未解決性の位置

### 2.1 既存理論がすでに解いていること

| 既存分野 | すでに扱えること | DCITが同じことを言うだけなら失敗 |
|---|---|---|
| GKSL理論 | 一つのgeneratorがCPTP semigroupを生成する条件 | 各generatorのCPTP検査だけ |
| Process tensor / quantum comb | 一つの多時刻量子過程と任意の操作列の確率 | full processを再構成して同じfeasibility問題を解くだけ |
| Quantum channel compatibility | 複数channelが一つのchannelのmarginalとして実現できるか | 離散channel compatibilityの単純な言い換え |
| Quantum trajectories / unravelling | 同じLindblad equationから異なる条件付き軌道が生じること | 「同じgeneratorでも測定で違う」という既知現象だけ |
| Open-system identification | 出力から識別可能なparameterの同値類とgauge | 通常のidentifiability rankだけ |
| PSD matrix completion | 局所Gram matrixが大域PSD completionを持つ条件 | Kossakowski行列への既知定理の形式的移植だけ |

Process tensor／combは一般の多時刻過程を表現できるため、「他理論では数式として書けない」という絶対的主張は採らない。  
実際、process tensorは多時刻操作に対して非常に一般的な枠組みである
([Milz and Modi, PRX Quantum 2021](https://link.aps.org/doi/10.1103/PRXQuantum.2.030201);
[Keeling et al., PRX Perspective 2026](https://journals.aps.org/prx/abstract/10.1103/1ncg-11hz))。

また、同じLindblad master equationに対して異なるenvironment measurementが異なるtrajectoryを与えることや、unravellingによりEPを制御できることも既知である
([Brown, Macieszczak, and Jack, 2025](https://arxiv.org/abs/2503.09261);
[Minganti et al., PRA 2022](https://arxiv.org/abs/2206.01639))。

したがって、DCITの新規性を

> generatorが同じでもinterfaceで結果が変わる

だけに置いてはいけない。

### 2.2 調査上、まだ体系化されていない問い

今回確認した近接文献では、次の問題を一つの有限次元Markovian理論として閉じたものは見つからなかった。

> 複数のintervention-conditioned GKSL generatorsが、宣言したport構造、bath相関、monitoring access、switching ruleを持つ**一つの共通連続時間dilation**の制限として実現できるかを判定し、  
> 不可能なら最小context、dual witness、必要な追加環境次元、有限測定costを返す理論。

これは文献不存在の証明ではなく、現時点の先行研究監査から得た研究上の空白である。

近い理論はある。

- channel compatibilityは「一つのchannelのmarginalか」を問う
  ([Kuramochi, 2017](https://arxiv.org/abs/1708.00150))。
- outputを用いたMarkov system identificationは、識別不能parameterをLie-group orbitとして特徴づける
  ([Guţă and Kiukas, 2017](https://arxiv.org/abs/1601.04355))。
- channel holonomyはKraus gaugeに共変なholonomyを定義する
  ([Kult, Åberg, and Sjöqvist, PRA 2008](https://arxiv.org/abs/0711.2140))。
- Lindblad gaugeによりheat、work、efficiencyの分解が変わることも知られている
  ([Nicacio and Maia, 2022](https://arxiv.org/abs/2204.02966))。

しかし、これらは「counterfactual generator族の共通物理実装可能性」と、その最小反証文法を主対象にはしていない。

---

## 3. 理論の原始概念

### 3.1 入力

有限介入context族を

\[
\mathcal C=\{U_1,\ldots,U_M\}
\]

とする。各contextで推定または理論的に与えられるgeneratorを

\[
\mathbf L_{\mathcal C}
=
\{\mathcal L_U:U\in\mathcal C\}
\]

とする。

さらに、比較前に物理interface architecture

\[
\mathfrak A
=
(\mathcal H_S,\mathcal P,\mathcal B,\mathcal G_{\rm phys},
\mathcal S,\mathcal M)
\]

を宣言する。

- \(\mathcal H_S\): system Hilbert space
- \(\mathcal P\): 制御可能なbath port集合
- \(\mathcal B\): 許容bath相関構造
- \(\mathcal G_{\rm phys}\): 物理的に同一視するgauge群
- \(\mathcal S\): port switching rule
- \(\mathcal M\): monitoring／readout access

### 3.2 共通dilation整合性

\(\mathbf L_{\mathcal C}\) がarchitecture \(\mathfrak A\) に関して整合的であるとは、

\[
\exists\ \mathfrak E,\{\Pi_U\}_{U\in\mathcal C}
\quad\text{s.t.}\quad
\mathcal L_U
=
\operatorname{Red}(\mathfrak E,\Pi_U)
\]

を満たす一つのMarkovian system–bath dilation \(\mathfrak E\) と、各contextを実装するport操作 \(\Pi_U\) が存在することと定義する。

整合的generator族の集合を

\[
\mathfrak C_{\mathfrak A}
=
\left\{
\mathbf L_{\mathcal C}:
\mathbf L_{\mathcal C}\ \text{has a common }\mathfrak A\text{-dilation}
\right\}
\]

と書き、**interface compatibility cone**と呼ぶ。

### 3.3 Frustration index

\[
\mathfrak F_{\mathfrak A}(\mathbf L_{\mathcal C})
=
\inf_{\widetilde{\mathbf L}\in\mathfrak C_{\mathfrak A}}
\sum_{U\in\mathcal C}
w_U
\left\|
\mathcal L_U-\widetilde{\mathcal L}_U
\right\|_{\rm op}.
\]

- \(\mathfrak F=0\): 共通実装可能
- \(\mathfrak F>0\): 宣言したarchitectureでは共通実装不可能

実験ではgenerator推定のconfidence regionを含め、

\[
\inf_{\mathbf L\in\mathrm{CI}}
\mathfrak F_{\mathfrak A}(\mathbf L)>0
\]

のときだけfrustrationを認証する。

---

## 4. 中心理論固有現象候補：dilation frustration

### 4.1 最小signed-cycle模型

四つのbath port \(1,2,3,4\) を考える。  
観測可能な二port contextは

\[
(12),\ (23),\ (34),\ (41)
\]

の四つだけとする。

各contextのKossakowski blockを

\[
C^{(ij)}
=
\begin{pmatrix}
1&s_{ij}r\\
s_{ij}r&1
\end{pmatrix},
\qquad
s_{12}=s_{23}=s_{34}=+1,\quad s_{41}=-1
\]

とする。

各blockの固有値は \(1\pm r\) なので、

\[
0\le r\le1
\]

なら四つの局所generatorはすべて正しいGKSL generatorである。

ところが、これらをprincipal blockとして持つ共通Kossakowski matrix

\[
C_{\rm global}\succeq0
\]

は、

\[
\boxed{r\le\frac1{\sqrt2}}
\]

のときに限って存在する。

したがって、

\[
\boxed{
\frac1{\sqrt2}<r\le1
}
\]

では、

\[
\text{全二port contextはCPTP}
\quad\text{だが}\quad
\text{共通四port Markov bathは存在しない}.
\]

これが最小のdilation-frustrated phaseである。

### 4.2 厳密な有限witness

signed cycle adjacencyを

\[
A_\square=
\begin{pmatrix}
0&1&0&-1\\
1&0&1&0\\
0&1&0&1\\
-1&0&1&0
\end{pmatrix}
\]

とすると、

\[
A_\square^2=2I.
\]

負固有空間へのprojector

\[
P_-=\frac12
\left(
I-\frac{A_\square}{\sqrt2}
\right)
\succeq0
\]

は、未観測chord \((13),(24)\) 上に成分を持たない。

任意のglobal completionに対し、

\[
\operatorname{Tr}(P_-C_{\rm global})
=
2(1-\sqrt2r)
\]

である。もし \(C_{\rm global}\succeq0\) なら左辺は非負でなければならないため、

\[
r\le1/\sqrt2
\]

が必要である。逆に、chordを0としたcompletionの固有値は
\(1\pm\sqrt2r\) なので十分性も従う。

よって

\[
\boxed{
W_\square
=
\sqrt2r-1
}
\]

は厳密なfrustration witnessである。

この4-cycleの数学自体はPSD completionの既知結果に近い
([Grone et al., 1984](https://www.math.uwaterloo.ca/~hwolkowi/henry/reports/pdcomplGJSW84.pdf))。
したがって、これだけでは新しい物理理論とは呼ばない。

新理論として必要なのは、この局所―大域 obstructionを

1. GKSL generator族の共通Hudson–Parthasarathy dilation条件へ厳密に対応させること
2. Lindblad gaugeとLamb shiftを含めても不変なwitnessへすること
3. system responseから有限測定で回収すること
4. 非可換couplingを持つ量子模型で、classical population modelには見えないfrustrationを示すこと

である。

### 4.3 PRX flagshipに必要な量子強化

最小4-cycleは理論のexact seedである。  
PRXの中心現象へ昇格させるには、

\[
\boxed{
\text{coherence-only dilation frustration}
}
\]

を構成する。

狙う条件は、

\[
\begin{aligned}
&P_{\rm diag}\mathcal L_U P_{\rm diag}
\quad\text{は全contextでclassically compatible},\\
&\text{population、steady rate、single-context FCSは一致},\\
&\text{coherence-sensitive Kossakowski cycleだけが}
\quad W_\square>0
\end{aligned}
\]

である。

候補はqutrit以上の系で、四つの非可換Gell-Mann couplingを用いる。  
これにより、単なる古典covariance completionではなく、

> classical shadowは一貫しているが、量子coherenceを含む共通bath realizationだけが不可能

という現象を狙う。

---

## 5. 定理ラダー

| 定理 | 内容 | PRXでの役割 |
|---|---|---|
| D1. Canonical interface extraction | 物理port basisを固定し、generatorからKossakowski／Hamiltonian dataをgauge-consistentに抽出 | sector cutの表現依存性を除く |
| D2. Common-dilation theorem | 宣言architectureでの共通Markovian dilationとPSD／Gram completion条件の同値性 | 理論の基礎定理 |
| D3. Chordal sufficiency theorem | context graphがchordalなら、overlap整合性と各cliqueのCPがglobal realizationを保証 | 有限分類則 |
| D4. Frustration theorem | nonchordal graphには、局所CPTPだが大域非実現なgenerator族が存在 | 中心現象 |
| D5. Dual witness theorem | 非実現性は、観測context上だけにsupportを持つ有限dual certificateで検出可能 | 実験可能性 |
| D6. Minimal grammar theorem | 最小obstruction supportが、分離に必要な最小context数と介入hypercycleを与える | resource理論との接続 |
| D7. Minimal dilation theorem | compatible族の最小bath mode数をPSD completion rankから決定または上下界化 | reservoir engineering |
| D8. Robust certificate theorem | noise confidence setとcompatibility coneの距離からfalse-certificateを制御 | blind validation |
| D9. Response pullback theorem | 適切なsource/readout集合からdual witnessをfull tomographyなしで回収 | RISEI／SMRT資産との接続 |

### 論理的status

- D4のsigned 4-cycle線形代数：exact seed
- D2の一般GKSL／HP-dilation対応：未証明
- D3、D5：固定Kossakowski architectureでは定理化可能性が高い
- D6、D7：architectureとcontext hypergraphを限定して証明する
- D8、D9：条件付き定理候補
- coherence-only frustration：未探索の数値現象候補

---

## 6. 計算体系を閉じる方法

DCITの計算は、次のfail-closed chainにする。

\[
\boxed{
\begin{gathered}
\text{context-resolved data}\\
\downarrow\\
\text{canonical GKSL extraction}\\
\downarrow\\
\text{overlap／gauge consistency}\\
\downarrow\\
\text{compatibility-cone feasibility}\\
\downarrow\\
\begin{cases}
\text{compatible: minimal dilation + prediction}\\
\text{incompatible: dual witness + minimal obstruction}\\
\text{insufficient data: ABSTAIN}
\end{cases}
\end{gathered}}
\]

### 6.1 入力

- contextごとのshort-time responseまたは推定generator
- 誤差共分散／confidence region
- port labelとswitching rule
- system coupling basis
- 許容bath correlation class
- source/readout access

### 6.2 出力

- `COMPATIBLE / FRUSTRATED / ABSTAIN`
- frustration index \(\mathfrak F_{\mathfrak A}\)
- 最小obstruction context
- sparse dual witness \(Z_\ast\)
- compatibleならminimal bath rank
- 次に測るべきcontext
- architecture failure certificate

### 6.3 有限性

- fixed-basis reciprocal Markov bath：PSD feasibility
- chordal graph：clique分解による有限判定
- nonchordal graph：SDPとdual certificate
- independent port architecture：Boolean Möbius成分のCP／消失判定
- unrestricted minimal-rank completion：一般には非凸なので、ここだけは厳密解を約束せず、上下界とABSTAIN branchを持つ

理論の閉性は「すべての無制限dilation問題を解くこと」ではなく、

> 宣言architectureごとに、有限判定、構成解、反証certificate、またはABSTAINを必ず返す

ことで実現する。

---

## 7. 既存理論の数学と計算結果をどう使うか

### 7.1 継承するもの

- RISEIの介入Boolean latticeとMöbius分解
- source/readout selection
- finite-resource signature
- blind predictionとfail-closed certificate
- Schur／Rieszによるresponse-relevant subspace抽出
- SMRTのsector-resolved response
- Newton fanのpath-dependent response分類

### 7.2 中心から外すもの

- tubeを新理論の中心現象にはしない
- EPを必須機構にしない
- Pattern (b)を普遍的なflagshipにしない
- uncut-response non-identifiabilityだけを中心no-goにしない
- 「同じgeneratorなら同じ系」という主張だけに依存しない

### 7.3 新しい順序

従来：

\[
\text{generator}
\to
\text{sector intervention}
\to
\text{response classification}
\]

DCIT：

\[
\text{generator family}
\to
\text{common-dilation audit}
\to
\text{physical intervention family}
\to
\text{RISEI／SMRT response classification}
\]

つまりDCITは、RISEI／SMRTを否定するのではなく、

> どのsector calculusが同一の物理interfaceに対して正当化されるか

を判定する前段理論になる。

---

## 8. 分野横断的な影響

### 8.1 開放量子系の基礎

「一つのGKSL generatorが物理的か」から、

\[
\text{counterfactual generator族が一つの環境を共有できるか}
\]

へ物理性の概念を拡張する。

### 8.2 Reservoir engineering／量子制御

独立に較正したloss port、pump port、monitoring portが、一つのdeviceで同時に実装可能かを事前判定できる。  
compatibleなら最小bath mode数を設計し、frustratedなら不足portまたはcontext-dependent bathを特定する。

### 8.3 開放系system identification

単なるparameter推定ではなく、

> 推定された複数モデルが同じ装置の異なる制御状態として整合しているか

を検定できる。hidden shared reservoir、crosstalk、context drift、Markov近似破れの診断になる。

### 8.4 Quantum trajectories／連続測定

複数のmonitoring schemeが、同じoutput fieldの異なる測定として共同実現可能かを分類する。  
単一unravellingのtrajectory差ではなく、unravelling族の共通実装可能性が対象になる。

### 8.5 量子熱力学

同じmaster equationでもgaugeによりheat／work分解が変わりうる。  
DCITは、複数bathへ割り当てたcurrentが一つの共通bath dilationから導けるかを検査し、物理的でないbath-resolved heat assignmentを排除できる可能性がある。

### 8.6 量子センシング

frustration witnessを、未知のbath相関、欠落環境mode、non-Markovian memoryを検出するnull testとして使える。

---

## 9. 競合理論への非還元監査

### 9.1 Process tensor／quantum comb

**危険:** 十分一般のcomb feasibilityが、同じ入力から同じcompatibility判定とdual witnessを返す可能性がある。

**DCITに必要なpredictive surplus:**

- full process tomographyなし
- generator／short-time responseだけ
- context graphから最小obstructionを事前予測
- minimal bath rankまたは追加contextを返す
- continuous-time Markov dilationの構造定理を返す

これが残らなければ、DCITはprocess tensorの応用へ降格する。

### 9.2 Channel compatibility

**危険:** common-dilation問題がstandard channel marginal compatibilityへ直接変換される可能性がある。

**必要な差:**

- semigroup generator level
- 同じsystem outputを持つcounterfactual control restrictions
- port switchingとHamiltonian cocycle
- continuous-time共通bath
- minimal environment rankとfinite response witness

### 9.3 PSD completion

**危険:** 理論全体がKossakowski matrixへの既知completion theoremの移植に見える。

**必要な差:**

- GKSL gauge不変なphysical port extraction
- Lamb shiftとcomplex bath correlationを含む定理
- response-only witness
- coherence-only frustration
- 複数architectureでのblind prediction

### 9.4 Unravelling／trajectory theory

**危険:** 同じLindblad equationの異なるmonitoringという既知現象に還元される。

**必要な差:**

> 与えられたunravelling間の差ではなく、unravelling族が一つのoutput-field dilationを共有できるかというglobal compatibilityを分類する。

### 9.5 Classical covariance／hidden Markov model

**危険:** signed-cycle seedは古典Gram completionでも再現できる。

**必要な量子Gate:**

\[
\text{classical diagonal restrictionはcompatible}
\quad\text{だが}\quad
\text{coherence-sensitive full modelはfrustrated}
\]

を成立させる。

---

## 10. 最優先計算プログラム

### Priority 0：定義の凍結

次を結果を見る前に固定する。

- common dilationのarchitecture class
- physical Lindblad gauge
- port switching rule
- Kossakowski basis
- response access
- competitor baseline
- uniqueness判定基準

### Priority 1：4-cycle exact seed

1. signed-cycle theoremをsymbolicに証明
2. SDP dual witnessと解析式を一致
3. unequal edge \(r_{ij}\) とcomplex phaseへ一般化
4. confidence intervalを含むrobust marginを導出

**Gate P1:** 局所CPTP／大域nonrealizable領域が有限幅で存在する。

### Priority 2：GKSL common-dilation theorem

1. fixed operator basisでgeneratorをcanonicalize
2. Lindblad unitary mixing、identity shift、Hamiltonian補償を整理
3. common Kossakowski／HP dilationとの必要十分条件を証明
4. independent port、correlated port、monitored portをbranch化

**Gate P2:** PSD completionが単なる形式対応でなく、物理的common dilationと同値になる。

### Priority 3：coherence-only frustration

qutritまたは二qubit最小模型を逆設計する。

目標：

\[
\begin{aligned}
&\text{全population data一致},\\
&\text{各local contextはCPTP},\\
&\text{classical baselineはcompatible},\\
&\text{coherence responseだけがdual witnessを復元}.
\end{aligned}
\]

**Gate P3:** classical covariance／HMMへの完全還元が破れる。

### Priority 4：response pullbackと最小文法

- full generator tomographyを用いない
- short-time derivative、linear response、noise spectrumのどれが最小か比較
- 最小context数
- 最小source/readout数
- 必要shot数
- detector inefficiency threshold

**Gate P4:** finite-resource witnessとfailure certificateが成立する。

### Priority 5：競合理論blind audit

同一データ、prior、calibration budgetで比較する。

- process tensor／comb feasibility
- channel compatibility SDP
- generic PSD completion
- input-output system identification
- hidden Markov model

**Gate P5:** DCITだけが、より少ない情報からminimal obstruction、追加port、minimal bath rankの少なくとも一つをheld-outで予測する。

### Priority 6：cross-architecture validation

最低二系統を使う。

1. circuit QED／multiport reservoir engineering
2. trapped-ionまたはphotonic programmable dissipation

第三候補としてcontinuous monitoring／homodyne outputを用いる。

NVセンターは、最初のflagshipに無理に使わない。物理portの独立制御とbath相関較正が十分に可能な段階で適用する。

---

## 11. PRX投稿の物語

### Act I：局所的物理性の盲点

各介入条件では完全に正しいGKSL generatorが得られる。  
従来なら、それらを同一deviceのon／off counterfactualとして扱ってしまう。

### Act II：新しい物理性

共通dilation compatibility coneを定義する。

\[
\text{individual CPTP}
\not\Rightarrow
\text{joint physical realizability}
\]

を中心命題にする。

### Act III：新現象

最小signed 4-cycleでdilation-frustrated phaseを厳密に示す。  
さらにcoherence-only frustrationを量子flagshipとして示す。

### Act IV：定理と有限計算

chordal／nonchordal分類、dual witness、minimal grammar、minimal bath rank、noise certificateを一つの計算体系に閉じる。

### Act V：物理的帰結

reservoir engineering、system identification、trajectory monitoring、quantum thermodynamicsで同じcompatibility certificateが働くことを示す。

### 中心命題

> 開放量子系の物理性は、各intervention-conditioned generatorの完全正値性だけでは決まらない。  
> counterfactual generator族が一つの環境interfaceを共有できるかという大域的整合性が必要であり、局所的にはCPTPでありながら大域的に実現不能なdilation-frustrated phaseが存在する。  
> その相は有限contextのdual response witnessから判定できる。

---

## 12. 他候補との比較

| 候補 | 未解決性 | 非還元性の見込み | 計算閉包 | 現在の判断 |
|---|---|---|---|---|
| Operational Newton fan | 高い | 中。tropical／EP scalingが近い | 高い | PRL主線として強い |
| Resource-indexed observation grammar | 高い | 低～中。process discriminationが強い競合 | 高い | 方法論／探索基盤 |
| Unravelling-interface holonomy | 中～高 | 中。channel holonomyとtrajectory gaugeが近い | 中 | 高リスク副案 |
| **DCIT / dilation frustration** | **高い** | **中～高。ただしP3/P5必須** | **高い** | **PRX候補の最優先** |

---

## 13. PRX Gateと停止則

### 必須Gate

1. **Exact phenomenon:** 局所CPTP／大域nonrealizableの有限幅相
2. **Physical equivalence:** common HP dilationとcompatibility coneの同値性
3. **Quantum surplus:** coherence-only frustration
4. **Finite witness:** full process tomographyなしのdual certificate
5. **Blind prediction:** held-out contextまたは追加bath modeを予測
6. **Cross-architecture:** 少なくとも二つの量子実装
7. **External uniqueness:** 同一条件のprocess tensor、channel compatibility、PSD completion監査を通過

### 即時停止則

次のいずれかなら、PRXの新理論候補から降格する。

- common-dilation判定がstandard channel compatibilityの変数名変更だけである
- 量子模型がclassical covariance completionと同じwitnessしか持たない
- full process tomographyが必要で、圧縮された予測余剰がない
- Hamiltonian gauge／Lamb shiftを入れるとfrustrationが消える
- 物理的port switchingでは任意の局所familyが自動的に共通実装できる
- 実験誤差内でfrustrated phaseが消える
- dual witnessが結果を見た後のfitに依存する

この場合でも、DCITは「介入モデルの整合性監査」として価値を持つ。  
ただし、PRXで主張する新しい開放系理論とは呼ばない。

---

## 14. 最初に行うべき作業

最初の大規模数値探索ではなく、次の三つを先に行う。

1. signed 4-cycleをGKSL Kossakowski blocksへ埋め込んだ最小qutrit模型を作る
2. physical Lindblad gaugeを固定したcommon-dilation theoremの正確な仮定を書く
3. process tensor／channel compatibility／PSD completionの三baselineを同時実装する

この三つでP2またはP3が失敗するなら、早い段階で候補を止められる。  
逆に通過すれば、dilation frustrationは初めてPRX級の中心現象候補になる。

---

## 15. 最終評価

私は、DCITが今ある候補の中ではいちばん「これまでの失敗から学んだ設計」になっていると思う。

- tubeのように既知機構の組合せへ還元されることを避ける
- interface dependenceを既知のunravelling差だけで終わらせない
- sector cutが物理的かを理論内部で判定する
- exactな最小現象から始められる
- finite algorithm、dual witness、failure certificateまで閉じられる
- reservoir engineering、system identification、trajectory theory、thermodynamicsへ同じ問いが届く

ただし、いちばん大切な境界も明確である。

\[
\boxed{
\text{4-cycle PSD obstructionだけでは新理論ではない}
}
\]

PRX候補になるのは、

\[
\boxed{
\text{common Markov dilationの物理定理}
+
\text{coherence-only frustration}
+
\text{finite response witness}
+
\text{competitorに対するblind predictive surplus}
}
\]

が一つの体系として成立したときである。

その条件を満たすなら、中心の一文は次になる。

> **開放系では、個々の介入ダイナミクスが物理的であることは、それらが同じ物理装置の介入可能な世界として共存できることを保証しない。**

