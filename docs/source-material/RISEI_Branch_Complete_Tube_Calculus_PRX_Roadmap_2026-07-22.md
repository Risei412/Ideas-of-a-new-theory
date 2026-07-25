# RISEI理論における分岐完備型Tube Calculusの成立手順とPRX投稿ストーリー

**作成日:** 2026-07-22  
**位置づけ:** 研究ロードマップ / PRX投稿構成案  
**基礎資料:**

- `content-5.tex`（Generalized RISEI Theory + Local Schur–Riesz Tube Calculus 統合版）
- `Revised_Generalized_RISEI_Theory_2026-07-21(1).pdf`
- `RISEI_future_direction_new_open_system_field(1).md`
- Riesz・Zeno・制御理論の代表論文パック

---

## 0. この文書でいう「条件のない計算体系」

ここで目指すものは、数学的仮定を一切持たない理論ではない。

有限次元、time-local GKSL、物理的に許容された介入、宣言されたsource/readout・response functional・観測窓など、**理論の舞台を定める前提**は残る。

目標は、現在のように局所定理の成立条件を利用者が事前に保証しなければ計算を開始できない体系から、

> **入力モデルを受け取った計算体系自身が、正則tube、特異tube、chart遷移、物理的消失、適用範囲外を有限手順で診断し、それぞれに証明書または数値証明書を返す体系**

へ進むことである。

したがって、本ロードマップではこれを

> **分岐完備型（branch-complete）Tube Calculus**

と呼ぶ。

現在の条件付き局所Schur–Riesz tube定理は捨てない。一般体系の中の最も精密で計算効率のよい **regular branch** として保持する。

---

# Part I. 現在地

## 1. すでに成立している計算鎖

統合版RISEI理論では、定常・強散逸領域において次の順方向計算が構築されている。

\[
(\mathcal L_\Gamma,p,c)
\longmapsto
P_{\mathcal C}(\Gamma)
\longmapsto
\theta_c(\Gamma)
\longmapsto
J_f(\Gamma)
\longmapsto
Q_{\mathrm{tube}}(\Gamma)
\longmapsto
z_{\mathrm{loss}}(\Gamma)
\longmapsto
\text{response class}.
\]

各出力の意味は次の通りである。

| 出力 | 役割 |
|---|---|
| \(P_{\mathcal C}\) | response-relevant Riesz cluster |
| \(\theta_c\) | \(\Gamma\)-adaptiveなtube中心 |
| \(J_f\) | selection manifoldの接・法線構造とcodimension |
| \(Q_{\mathrm{tube}}\) | finite-\(\Gamma\) tube断面のGram metric |
| \(z_{\mathrm{loss}}\) | tube幾何とは独立な物理的slow-loss gate |
| response class | protected / crossover / loss-dominated等の判定 |

現在の理論で最も重要な概念的分離は、

\[
\boxed{
\text{selection manifold}
\neq
\text{finite-}\Gamma\text{ tube geometry}
\neq
\text{Pattern (b) survival}
}
\]

である。

## 2. 条件付き局所定理の現在の条件

現行の局所定理は、主に次の条件の下で正確に成立する。

1. generator、source、readout、intervention dataの局所 \(C^2\) 正則性
2. affine-in-\(\Gamma\) slow/fast chart
3. fast blockの一様可逆性
4. response-relevant Riesz clusterのcontour separationとconstant rank
5. selection Jacobianのconstant real rank
6. full / cluster / Schur derivativeのattribution bound
7. quadratic Taylor remainderを制御できる局所窓
8. slow-loss/protection ratioの独立評価

この条件内では、selection setは局所多様体となり、normal tube断面は

\[
\delta\theta^{\mathsf T}
Q_{\mathrm{tube}}
\delta\theta
\leq \varepsilon^2
\]

で与えられる楕円体として予測される。

## 3. 現在までの数値的な支持

統合版に記録されたproduction計算では、少なくとも次が確認されている。

- 5準位・6準位の複数architecture
- rank 3・rank 4 tube
- near-rank-drop case
- \(\Gamma\in[10^4,10^6]\)でのadaptive continuation
- 最大tube surface error \(5.779\times10^{-4}\)
- 最大Schur/full derivative error \(9.222\times10^{-4}\)
- Riesz cluster attribution error 約 \(2.5\times10^{-9}\)
- width exponentはほぼ1、すなわちregular affine chartで \(w_i\sim\Gamma^{-1}\)
- real Jacobian rank 1〜6の検証
- 42本の独立normal方向でPattern (b)が破壊され、root・tangent方向では保持
- cross-model productionとheld-out modelでの予測成立
- slow-loss ratioによるprotected / crossover / loss-dominated分類の一致

これらは、**regular branchの計算体系がすでに閉じている**ことを支持する。ただし、任意のGKSL generatorに対する普遍定理ではない。

---

# Part II. 分岐完備型計算体系を成立させるステップ

## 4. 基本方針

条件を単純に削除するのではなく、各条件を次のいずれかへ変換する。

1. **内部診断量**へ変える
2. **別branchへの切替条件**へ変える
3. **物理的不成立のcertificate**へ変える
4. **宣言された理論範囲外のcertificate**へ変える

完成形は、単一公式ではなく、有限個の局所定理・特異定理・遷移則・停止証明書を束ねた **tube atlas** になる。

---

## Step 0. 条件付きregular branchを凍結する

### 目的

一般化の途中で、すでに成立した局所計算体系を壊さない。

### 作業

- 現在のT1–T6条件を固定
- regression test suiteを作成
- 既存production全件を自動再現
- \(P_{\mathcal C},\theta_c,J_f,Q_{\mathrm{tube}},z_{\mathrm{loss}}\) の出力形式を固定
- full / cluster / Schurの三層比較を標準化

### 完了条件

理論・コードの更新後も、既存positive modelとnegative controlが同じ分類を返す。

### 意義

条件付き局所定理は、一般化後も最も高速で誤差評価の明瞭なbranchとして残る。

---

## Step 1. 条件を「事前仮定」から「内部診断」へ変える

### 目的

利用者が条件成立を手作業で保証する必要をなくす。

### 必要なdiagnostics

- contour separation margin
- Riesz projector rankとprojector distance
- fast resolvent norm
- Schur expansion residual
- Jacobian singular values
- Taylor remainder estimator
- attribution errors \(\eta_R,\eta_S\)
- Möbius cancellation condition number
- numerical floor / SNR
- slow-loss/protection ratio

### 出力

各条件について

\[
\texttt{PASS},\quad
\texttt{MARGINAL},\quad
\texttt{FAIL}
\]

と定量的marginを返す。

### 完了条件

正則tube計算を開始する前に、全条件が機械的に監査される。

---

## Step 2. non-affine strong-dissipation familyへの拡張

### 現在の制限

\[
\mathcal L_\Gamma=\Gamma D+B
\]

というaffine chart。

### 一般化対象

\[
\mathcal L_\Gamma
=
\sum_{a=1}^{m}g_a(\Gamma)D_a+B(\Gamma).
\]

例：

\[
g_1(\Gamma)=\Gamma,
\qquad
g_2(\Gamma)=\Gamma^\alpha,
\qquad
B(\Gamma)=B_0+\Gamma^{-\beta}B_1.
\]

### 必要な理論

- dominant balanceの自動選択
- effective fast scale \(h(\Gamma)\) の定義
- generalized Schur expansion
- 複数scale間のcrossover判定
- logarithmic / fractional / piecewise scalingへの対応

### 期待される一般則

regular affine branchの

\[
w_i\sim\Gamma^{-1}
\]

を、

\[
\boxed{w_i\sim h(\Gamma)^{-1}}
\]

というeffective-scale lawの特殊例として位置づける。

### 判定計算

- \(\alpha,\beta\) sweep
- dominant-scale exchange
- held-out scaling path
- local exponentとpower-log model比較

### 完了条件

affine caseを正確に回収しつつ、複数scale系でtube幅・中心輸送・survival gateを予言できる。

---

## Step 3. constant-rank条件をstratified selection geometryへ拡張する

### 現在の制限

\(\operatorname{rank}_{\mathbb R}J_f=r\) が局所一定。

### 一般化

selection setを一枚の滑らかな多様体ではなく、

\[
\mathcal M
=
\bigcup_{\alpha}\mathcal M_\alpha
\]

というstratified setとして扱う。

### 調べる現象

- rank drop
- branch merging / splitting
- cusp
- self-intersection
- puncture
- normal directionの消失
- tube断面の円筒化・扇形化
- principal widthの発散または非解析性

### 必要な計算

- \(J_f\) のsingular value continuation
- higher-order jet \(D^2f,D^3f\)
- local algebraic normal form
- tangent cone / normal cone
- stratumごとのRiesz continuity
- branch transition graph

### 目標定理

> 各constant-rank stratum上ではregular local tube theoremが成立し、rank-drop集合ではhigher-order jetが特異断面とbranch接続を決定する。

### 完了条件

rank dropを「失敗」ではなく、stratum transitionとして分類できる。

---

## Step 4. Riesz cluster gap closureをchart transitionとして扱う

### 現在の制限

一つの固定contourがresponse-relevant clusterをconstant rankで囲む。

### 問題

gap closureでは個別cluster chartが壊れるが、物理的tubeが消えたとは限らない。

### 必要なbranch

1. **single-cluster continuation**
2. **merged-cluster continuation**
3. **multi-chart overlap**
4. **true spectral-support loss**

### 必要な計算

- adaptive contour surgery
- cluster merger / split detection
- projector subspace angle
- merged-cluster response reconstruction
- chart overlap consistency
- full-response direct tubeとの比較

### 目標

\[
\text{physical tube disappearance}
\quad\text{と}\quad
\text{Riesz chart transition}
\]

を有限手順で区別する。

### 完了条件

gap closure時に、次のいずれかを返す。

- tube persists under chart enlargement
- tube bifurcates
- response attribution changes cluster
- physical tube vanishes
- declared finite-dimensional chartでは未決定

---

## Step 5. Schur attribution条件を導出量へ変える

### 現在の条件

\[
\|D\mathcal E_{\mathrm{full}}-D\mathcal E_{\mathcal C}\|
\leq\eta_R,
\qquad
\|D\mathcal E_{\mathcal C}-G_{\mathrm{Schur}}\|
\leq\eta_S.
\]

### 目標

\(\eta_R,\eta_S\) を外部仮定ではなく、

- spectral gap
- resolvent norm
- off-cluster coupling
- Schur remainder
- source/readout norm

から計算するa priori / a posteriori boundへ変える。

### 二つのbranch

#### Mechanism-resolved branch

attribution boundが十分小さい場合、tubeをprotected Riesz clusterとSchur mechanismへ帰属する。

#### Direct-response branch

attributionが弱い場合、full responseからtube境界は計算するが、機構帰属は保留する。

### 完了条件

\[
\text{prediction succeeds but mechanism attribution fails}
\]

を正式な出力classとして扱える。

---

## Step 6. quadratic ellipsoidをhigher-order tube geometryへ拡張する

### 現在の近似

\[
\|\mathcal E(\theta_c+\delta\theta)\|_W^2
=
\delta\theta^{\mathsf T}Q_{\mathrm{tube}}\delta\theta
+O(\|\delta\theta\|^3).
\]

### 条件破壊時に起こりうる断面

- degenerate ellipsoid
- cylinder
- cusp
- asymmetric lobe
- multi-lobe
- non-convex section

### 拡張

\[
\mathcal E
=
G\delta\theta
+\frac12H[\delta\theta,\delta\theta]
+\frac16T[\delta\theta,\delta\theta,\delta\theta]
+\cdots
\]

を用い、必要最小次数まで自動昇格する。

### モデル選択

- quadratic
- quadratic + cubic
- local polynomial
- direct boundary continuation

を誤差基準で切り替える。

### 完了条件

楕円体近似の失敗を検出し、higher-order断面または直接境界へ自動遷移できる。

---

## Step 7. exact kernel・approximate kernel・slow lossを統一する

### 既存の区別

- exact protected kernel
- fixed kernel lifting
- finite-window approximate protection
- slow-loss dominated regime

### 統一変数候補

\[
x
=
\frac{\Gamma\lambda_{\min}}{J_{\mathrm{eff}}},
\qquad
z_{\mathrm{loss}}
=
\frac{\gamma_{\mathrm{slow}}}{\Delta_{\mathrm{prot}}}.
\]

### 必要な分類

| regime | 幾何 | 応答 |
|---|---|---|
| exact protected | tubeあり | Pattern (b) survival可能 |
| approximate kernel, \(x\ll1\) | pre-asymptotic tube | finite-window survival |
| crossover, \(x=O(1)\) | tube変形 | functional class切替 |
| lifted kernel, \(x\gg1\) | regular protected mechanism消失 | joint peakも抑制 |
| slow-loss dominated | 幾何が残る場合あり | Pattern (b)は消失 |

### 完了条件

geometry classとsurvival classを独立軸として返す。

---

## Step 8. branch-completeな有限アルゴリズムを構成する

### 入力

\[
\mathfrak I
=
(\mathcal L_{\boldsymbol\lambda},
\pi,
 p,
 c,
 \Phi,
 W,
 \Lambda,
 \mathcal A,
 \Xi_{\mathrm{exp}})
\]

- generator family
- intervention protocol
- source/readout
- functionalと観測窓
- limit protocol
- admissible perturbation class
- experimental parameter map \(\Xi_{\mathrm{exp}}\)

### 出力branch

1. **Regular ellipsoidal tube**
2. **Higher-order regular tube**
3. **Stratified / rank-drop tube**
4. **Riesz chart transition**
5. **Approximate-kernel crossover tube**
6. **Geometry present, survival lost**
7. **No response-relevant tube**
8. **Predictive geometry without mechanism attribution**
9. **Outside declared scope certificate**

### 必須certificate

- branch選択理由
- spectral margin
- rank margin
- approximation error
- cancellation condition
- SNR / numerical floor
- physicality / stability
- failureが物理的かcoordinate的か

### 完了条件

計算が停止するとき、単なる`failed`ではなく、上記のいずれかを必ず返す。

---

## Step 9. 逆問題を構築する

順方向計算だけでは、理論は「説明器」に留まる。

### 逆tube問題

望ましいtube特性

\[
(\theta_c,
\operatorname{codim},
\{w_i\},
\text{axis bundle},
\text{survival margin})
\]

から、

\[
(\mathcal L,p,c,\pi)
\]

または実験制御値を設計する。

### 目的関数例

- tube volume最大化
- 最小幅最大化
- slow-loss margin最大化
- calibration cost最小化
- source/readout実装可能性
- Möbius cancellation fragility最小化

### 完了条件

理論が、既知のtubeを再現するだけでなく、未探索モデル・実験条件を提案する。

---

## Step 10. 実験パラメータ空間へのpullback

### 理論パラメータと実験パラメータ

\[
\theta=\Theta(\xi),
\]

ここで \(\xi\) は、たとえば

- magnetic field
- polarization angle
- microwave amplitude / phase
- detuning
- optical power
- dephasing rate
- strain
- pulse timing
- detector quadrature

である。

### experimental tube metric

局所Jacobian \(J_{\Theta}=D_\xi\Theta\) を用いて

\[
Q_{\mathrm{exp}}
=
J_{\Theta}^{\mathsf T}
Q_{\mathrm{tube}}
J_{\Theta}.
\]

実験誤差共分散 \(\Sigma_\xi\) があれば、

\[
\mathbb E[\delta\theta^{\mathsf T}Q_{\mathrm{tube}}\delta\theta]
=
\operatorname{Tr}(Q_{\mathrm{exp}}\Sigma_\xi)
\]

により実験的robustnessを予測する。

### 出力

- 最適operating point
- 許容誤差
- 最も危険なcontrol direction
- tangent recalibration direction
- expected success probability
- SNR付きの観測窓

### 完了条件

実験者が直接設定できる単位と誤差で予言を提示できる。

---

## Step 11. blind validationを行う

### 必須の三層

1. **held-out mathematical models**
2. **held-out physical GKSL architectures**
3. **held-out experimental parameter sets**

### blind predictionの対象

- tube中心
- codimension
- principal axes
- widths
- branch transition point
- survival class
- Pattern (b)の有無
- observability margin

### 禁止事項

- full responseを見てから係数調整
- test modelをtraining setへ戻す
- fit windowの後付け選択
- negative controlの除外

### 完了条件

予言値、誤差帯、失敗条件を事前登録し、full modelまたは実験との比較で評価する。

---

## Step 12. Riesz・Zeno・制御理論への還元／非還元監査

この作業は、一般計算体系が固まった後の最終ゲートである。ただし文献監査自体は早期から並行する。

### 還元を示す部分

- Riesz projectorによるspectral cluster
- Schur / Zeno effective dynamics
- reachability / observability / transfer zero
- singular perturbation

これらはRISEIの基礎部品として明示的に認める。

### 非還元性として立証すべき追加出力

- physical sector interventionとsubset-Möbius irreducible response
- functional-dependent existence hierarchy
- source/readout selection manifoldとpuncture
- finite-\(\Gamma\) tube metricとexperimental pullback
- geometry classとsurvival classの分離
- protocol costとminimal identification resource
- chart failureとphysical disappearanceの分類

### 最も強い分離例

既存理論の主要データが等しい二つのモデルまたはprotocolを構成する。

例：

- 同じspectrum
- 同じRiesz rank
- 同じleading Zeno generator
- 同じ通常のfull response

であるにもかかわらず、RISEIでは

\[
\Omega_{12},
\quad
\Sigma_\pi,
\quad
Q_{\mathrm{tube}},
\quad
C_{\mathrm{req}}
\]

が異なり、実験protocolで分離できることを示す。

### 完了条件

「既存理論でも書ける」ことと、「既存理論の標準的不変量・計算体系だけで同じ予言を得られる」ことを区別し、RISEIのpredictive surplusを証明する。

---

# Part III. 完成判定

## 5. 分岐完備型Tube Calculusの完成条件

次の条件をすべて満たした段階を、計算体系の完成とみなす。

### A. 数学的閉包

- regular branchの定理
- non-affine branchの漸近定理
- stratified/rank-drop局所定理
- chart transition rule
- higher-order tube rule
- geometry–survival separation
- finite terminationまたは明示的scope certificate

### B. 計算的閉包

- 自動branch判定
- 誤差評価
- negative controls
- continuation failureの分類
- reproducible output schema
- full / cluster / Schur / experimentalの比較

### C. 予測的閉包

- held-out modelでblind prediction
- physical full modelでの検証
- 実験単位での中心・幅・遷移予言
- 不確かさ伝播
- 反証可能なnegative prediction

### D. 理論的新規性

- 既存理論への還元範囲
- RISEI固有の追加出力
- 非還元分離例
- Pattern (b)以外への適用可能性、または同一計算体系による別現象の分類

---

## 6. 完成時の中心主張候補

安全で強い中心主張は、次の形になる。

> **有限次元time-local GKSL開放系に対し、物理的介入protocol、source/readout、response functional、limit protocol、および実験制御写像を入力すると、RISEIの分岐完備型tube atlasは、応答選択集合のregularまたはsingular geometry、finite-parameter許容領域、chart transition、物理的survival class、および適用不能certificateを有限手順で返し、未計算の実験動作領域を定量予言する。**

この主張は、

- arbitrary GKSLに一つの係数則が成立する
- Pattern (b)がすべての開放系で発生する
- codimension oneが普遍的である

とは言わない。

強さは無制限な普遍性ではなく、**宣言された広いモデルクラス内で、成功と失敗の全branchを計算可能にすること**に置く。

---

# Part IV. PRX投稿のストーリー

## 7. 論文の物語

### Act 1. 見えていなかった現象

開放系の応答は、通常、spectrum、steady state、全応答、単一normなどで記述される。

RISEIによるsector interventionとMöbius分解では、単独sectorのpeakが消える一方、joint irreducible peakだけが有限に残り、integrated weightは消失するPattern (b)が発見された。

さらに、この現象はparameter spaceの一様なphaseではなく、source/readout selection setの周囲に形成されるfinite-\(\Gamma\) tubeとして現れる。

### Act 2. 局所機構の発見

現象の中心には、

- response-relevant protected Riesz cluster
- Schur–Zeno effective coupling
- source/readout selection geometry
- functional hierarchy
- independent slow-loss gate

が存在する。

条件付き局所定理とproduction計算により、tube中心、codimension、断面、主軸、幅、survival windowを予測できることが示された。

### Act 3. 条件付き理論の限界

しかし、affine chart、constant rank、fixed contour、quadratic sectionなどの条件が壊れると、現在の体系は停止する。

ここで重要なのは、停止が

- tubeの物理的消失
- chartの失敗
- clusterの再編
- rank-drop特異点
- slow-lossによる応答消失

のどれを意味するか分からないことである。

### Act 4. 仮定をbranchへ変換する

本研究の中心的進展は、局所定理の条件を削除することではなく、条件破壊を診断可能なbranchへ変えることである。

その結果、一般計算体系は

\[
\text{regular tube}
\rightarrow
\text{stratified tube}
\rightarrow
\text{chart transition}
\rightarrow
\text{physical disappearance}
\]

を一つのatlasとして分類する。

現在の楕円tube定理はregular stratumとして厳密に回収される。

### Act 5. 計算体系から実験予言へ

experimental-control Jacobianを通してtube metricを実験パラメータへpullbackし、

- どの磁場・偏光・位相・detuningで中心に入るか
- どの誤差方向が危険か
- どこまでずれてもjoint peakが残るか
- どのslow lossでPattern (b)が消えるか
- chart transitionがどこで起こるか

を、full modelを実行する前に予言する。

### Act 6. blind test

held-out modelsと物理platformに対して予言を固定し、full GKSL calculationまたは実験で検証する。

成功だけでなく、

- tubeが存在しない
- geometryはあるがsurvivalしない
- regular chartではなくmerged clusterが必要

というnegative predictionも検証する。

### Act 7. 理論的な追加情報

Riesz理論はspectral subspaceを、Zeno理論はstrong-dissipation effective dynamicsを、制御理論はreachability・observability・transfer zeroを与える。

最終段階では、それらの部品を正確に回収したうえで、RISEIが追加する

- intervention-resolved irreducibility
- functional-dependent existence
- observation-selection geometry
- finite-parameter calibration tube
- survival gate
- minimal observability resource

が、既存の標準出力だけからは決定できないことを分離例で示す。

### Act 8. 結論

RISEIはPattern (b)を説明するためだけの理論ではなく、

> **開放系の内部機構が、どの介入・観測・functional・有限資源の組で可視化されるかを、幾何と計算によって予言する理論**

として完成する。

---

## 8. PRX向けの主図構成

### Figure 1. Phenomenon and conceptual gap

- full responseでは見えにくいPattern (b)
- \(N_\infty\)と\(N_1\)のreverse hierarchy
- selection manifoldとfinite-\(\Gamma\) tube

### Figure 2. Branch-complete tube atlas

中央に入力モデルを置き、

- regular ellipsoid
- rank-drop stratum
- chart transition
- approximate-kernel crossover
- geometry without survival
- no-tube certificate

へ分岐する計算フロー。

### Figure 3. Regular theorem and quantitative prediction

- Riesz cluster
- selection Jacobian
- \(Q_{\mathrm{tube}}\)
- full response boundaryとの一致

既存productionの精度を示す。

### Figure 4. Singular transitions

- rank drop
- cluster merger
- non-affine scale exchange
- quadratic-to-higher-order section

を一枚のphase/atlas図で示す。

### Figure 5. Experimental pullback and blind prediction

- theory parameter tube
- experimental parameter tube
- error covariance
- predicted operating window
- full modelまたは実験結果

### Figure 6. Predictive surplus over component theories

同じspectrum / Riesz rank / leading Zeno generatorを持つ二例が、RISEIの\(\Omega_{12}\)、tube metric、minimal resourceで分離される例。

---

## 9. 論文本文の構成案

1. **Introduction**  
   観測される全応答ではなく、介入と測定によるmechanism visibilityを問題にする。

2. **Pattern (b) and finite-parameter tubes**  
   現象、functional hierarchy、有限幅tube。

3. **Conditional local Schur–Riesz calculus**  
   regular branchの定理と既存production。

4. **From assumptions to diagnostic branches**  
   non-affine、rank drop、gap closure、attribution failure。

5. **Branch-complete tube atlas**  
   theorem suite、algorithm、certificates。

6. **Inverse design and experimental pullback**  
   \(Q_{\mathrm{exp}}\)、誤差伝播、calibration cost。

7. **Blind predictions in physical models**  
   少なくとも一つの現実的full model、できれば異なる二architecture。

8. **Reduction and predictive surplus**  
   Riesz、Zeno、controlへの還元と非還元分離例。

9. **Discussion**  
   適用範囲、非Markov・無限次元・many-bodyへの将来拡張。

---

# Part V. 投稿判断とリスク管理

## 10. PRX投稿へ進むGate

次が揃えばPRXを本命にできる。

### Gate P1. Branch completeness

regular / singular / transition / disappearance / out-of-scopeが有限手順で分類される。

### Gate P2. Theorem suite

少なくともregular theoremに加え、non-affineまたはstratified branchに解析結果がある。

### Gate P3. Blind validation

held-out modelで中心、幅、transition、negative resultを事前予言できる。

### Gate P4. Experimental prediction

現実的パラメータと不確かさから、測定可能な予言を返す。

### Gate P5. Cross-architecture relevance

一つのminimal modelだけでなく、少なくとも別architectureまたはphysical full modelで成立する。

### Gate P6. Predictive surplus

既存理論への還元を示したうえで、RISEI固有の出力による分離例がある。

### Gate P7. Falsifiability

理論が成立する領域だけでなく、tube不在・survival消失・chart遷移も予言する。

---

## 11. PRXストーリーが弱くなる場合

次の場合は投稿先または論文分割を再検討する。

- 一般化が単なる数値branch追加に留まり、定理がregular branchのみ
- experimental pullbackができず、抽象parameterのまま
- held-out predictionが弱い
- 既存制御理論またはZeno理論の標準計算で同じ出力が得られる
- Pattern (b)以外へのpredictive surplusがない
- full physical modelではtubeが観測不能

この場合でも成果は失敗ではない。

- 鋭い一法則ならPRL
- 量子情報・量子センシング中心ならPRX Quantum
- 開放系・非Hermitian・量子光学の専門的完成ならPRA / PRB等

という分岐が残る。

---

## 12. 範囲を広げすぎないための停止則

分岐完備型計算体系は、無限の一般化を要求しない。

次を満たせば、いったん体系を閉じる。

1. 宣言されたfinite-dimensional time-local GKSL class内で全branchが停止する
2. gap closureの一部が未解決でも、明示的out-of-scope certificateを返す
3. 非Markov・無限次元・many-bodyは将来拡張として分離する
4. experimental pullbackとblind predictionを優先する
5. 新しい抽象層を追加する前にpredictive surplusを確認する

目標は「すべての開放系を説明すること」ではなく、

> **成功する場合と失敗する場合を同じ精度で予言できる、閉じた計算体系を作ること**

である。

---

# Part VI. 推奨実行順

## 13. 優先順位

### Priority 0

現行regular branchのfreezeとregression suite。

### Priority 1

non-affine strong-dissipation familyとeffective-scale width law。

### Priority 2

constant-rank破壊とstratified/rank-drop tube。

### Priority 3

attribution boundの自動評価とdirect-response branch。

### Priority 4

cluster gap closureとmulti-chart Riesz atlas。

### Priority 5

higher-order tube geometry。

### Priority 6

exact/approximate kernelとslow-lossの統一分類。

### Priority 7

branch-complete algorithmとcertificate schema。

### Priority 8

inverse tube designとexperimental pullback。

### Priority 9

held-out blind validationとphysical full-model prediction。

### Priority 10

Riesz・Zeno・制御理論への還元／非還元監査、中心主張のfreeze、PRX原稿化。

---

## 14. 一文でまとめた研究計画

> **現行の条件付きSchur–Riesz tube定理をregular branchとして保持し、その成立条件が破れる場合をnon-affine、stratified、multi-chart、higher-order、loss-dominatedの各branchへ分解することで、入力モデルからtubeの存在・形状・遷移・消失・実験許容幅を有限手順で返す分岐完備型RISEI計算体系を構築する。完成後は、held-out full modelと実験パラメータによるblind prediction、およびRiesz・Zeno・制御理論に対するpredictive surplusを示し、PRXへ投稿する。**

---

## 15. 最終的な位置づけ

この研究の価値は、条件をすべて消すことそのものにはない。

本当に重要なのは、従来は「定理の仮定が破れたので計算停止」とされていた場所を、

- 新しいtube geometry
- chart transition
- mechanism attribution failure
- physical survival loss
- true absence

へ分解し、それぞれを予言可能にすることにある。

その段階でRISEIは、Pattern (b)という一つの現象の説明から、

\[
\boxed{
\text{intervention}
+
\text{spectral geometry}
+
\text{source/readout selection}
+
\text{functional hierarchy}
+
\text{experimental calibration}
\longrightarrow
\text{mechanism visibility prediction}
}
\]

という、開放系に対する計算原理へ進む。
