# EITを最小実験場とする大域的bath実現可能性理論

**副題:** 局所的CPTP性と単一の因果的・受動的環境による大域的実現可能性の分離  
**作成日:** 2026-07-25  
**位置づけ:** 新理論候補の判定用ロードマップ。現時点では未証明の仮説と、証明済み／既知の数学を明確に分離する。  
**想定する第一段階:** 理論・数値による proof of principle  
**想定する第二段階:** EIT分光を用いた実験的有限証明書の取得

---

## 0. 結論

EITを今後も「説明すべき現象」として扱うだけでは、新しい一般理論へ進む余地は狭い。そこで役割を変更する。

> **EITを、開放系の一般的な物理性仮定を検査し、必要なら破るための最小実験場として用いる。**

検査対象はGKSL理論そのものではない。破るべき候補は、次の局所から大域への含意である。

\[
\boxed{
\begin{aligned}
&\text{各周波数・各制御条件で生成子がGKSL}\
&+\text{各ポートで通常の因果応答に整合}\
&\Longrightarrow\text{全データが一つの定常・受動bathから生成可能}
\end{aligned}}
\]

本計画が狙う中心命題は、

\[
\boxed{
\text{local physicality}\not\Rightarrow\text{global bath realizability}
}
\]

である。

EIT透明窓は、吸収を小さく抑えながら分散とLamb shiftを大きく観測できるため、この不整合を少数の周波数点と少数のポートで露出させる候補になる。

---

## 1. 何を「一般理論」と呼ぶのか

### 1.1 対象

有限次元量子系について、複数の制御条件 \(c\)、Bohr周波数 \(\omega\)、結合ポート \(i,j\) で得られる有効生成子族

\[
\{\mathcal L_c(\omega)\}_{c,\omega}
\]

を考える。

各点では、減衰行列 \(\gamma_c(\omega)\) が

\[
\gamma_c(\omega)\succeq 0
\]

であり、生成子がGKSL形を持つとする。この条件は、各点での完全正値性を保証する。しかし、異なる周波数・制御条件で得られた \(\gamma\) とLamb shift行列 \(S\) が、同一の物理bathから同時に生じることまでは保証しない可能性がある。

### 1.2 大域的実現可能性

定常bathとの弱結合を宣言した場合、減衰とLamb shiftは独立ではなく、一つの行列値解析関数の境界値でなければならない。

規約を固定して

\[
h(z)=-S(z)+\frac{i}{2}\gamma(z)
\]

と置き、\(h\) が上半平面の行列Herglotz関数になるarchitectureを考える。

このとき、実現可能性問題は次になる。

> 有限個の測定データ \(\{\gamma(\omega_a),S(\omega_a)\}\) を補間する、正の行列測度を持つ単一の \(h(z)\) は存在するか。

### 1.3 本理論の仮称

本計画では、一般理論候補を次のいずれかで呼ぶ。

- **Global Bath Realizability Theory, GBRT**
- **Causal Bath Compatibility Theory, CBCT**
- 既存計画との接続を維持する場合は **CIRTのEIT最小witness部門**

名称はまだ固定しない。まず非自明な定理とwitnessが成立するかを確認する。

---

## 2. EIT最小実験場

## 2.1 最小系

第一候補は三準位Λ系である。

\[
|g_1\rangle,\quad |g_2\rangle,\quad |e\rangle
\]

- probe: \(|g_1\rangle\leftrightarrow|e\rangle\)
- control: \(|g_2\rangle\leftrightarrow|e\rangle\)
- control Rabi周波数: \(\Omega_c\)
- probe detuning: \(\Delta_p\)
- two-photon detuning: \(\delta\)
- excited-state decay・ground-state dephasingを含む

ただし、通常の単一probe感受率だけでは行列値条件を検査できない。したがって、最低二つの結合ポートを導入する。

### ポート候補

1. 二つの偏光モード
2. 二つの遷移双極子方向
3. 二つの空間モード
4. 二つのground-state superpositionへの位相制御probe

ポート結合を

\[
H_{\mathrm{int}}=\sum_{i=1}^{2} A_i\otimes B_i
\]

と書く。

## 2.2 最小測定点

最小構成は、透明窓内の二周波数

\[
\omega_1,\omega_2\in W
\]

と二ポートである。

理論検証では二点から開始するが、実験的頑健性を評価する段階では三点以上を用いる。二点だけでは、局所的な較正誤差や導関数近似を排除しにくいためである。

## 2.3 測る量

各周波数で、複素応答行列

\[
\chi(\omega)=\chi'(\omega)+i\chi''(\omega)
\]

または、それと対応づけられる自己エネルギー・Lamb shift行列を再構成する。

二ポートのHermitian部分を再構成するには、少なくとも次の入力ベクトルを用いる。

\[
\begin{aligned}
v_1&=(1,0)^T,\\
v_2&=(0,1)^T,\\
v_3&=\frac{1}{\sqrt2}(1,1)^T,\\
v_4&=\frac{1}{\sqrt2}(1,i)^T.
\end{aligned}
\]

各入力について \(v_k^\dagger\chi(\omega)v_k\) を測れば、対角成分だけでなく実部・虚部の交差成分を復元できる。

問題は、測定された \(\chi\) がbathの \(h\) とどの規約・近似で一致するかである。このpullbackの導出は中心課題であり、単に感受率行列をLoewner行列へ代入してはならない。

---

## 3. 主張の階層

主張は、一度に最大のものを掲げず、次の順序で閉じる。

## Claim 0: 局所的物理性

全測定点・全制御条件について、

\[
\gamma_c(\omega_a)\succeq0
\]

であり、対応する有効生成子がCPTPであることを確認する。

これは新規な主張ではない。後の反例が単なる負の減衰率や非物理パラメータによるものではないことを保証するnegative controlである。

## Claim 1: 行列値の大域的整合条件

宣言した定常・受動bath architectureの下では、透明窓上のデータから作るLoewner型行列が正半定値でなければならない。

二点の最小候補は

\[
M_{12}
=-\frac{S(\omega_1)-S(\omega_2)}{\omega_1-\omega_2}.
\]

目標とする必要条件は

\[
M_{12}\succeq0.
\]

三点以上ではブロックLoewner行列を構成する。

## Claim 2: 最小反例

次を同時に満たすΛ系またはその最小拡張を構成する。

1. 各周波数で生成子はGKSL
2. 各単独ポートのスカラー応答は通常の因果・分散関係に整合
3. 各対角成分の二点差分は許容
4. 行列全体では

\[
\lambda_{\min}(M_{12})<0
\]

5. 違反は単一点ではなく、有限幅のパラメータ領域に残る

これが成立すれば、

> 各局所検査を通過する開放系模型族が、単一の宣言されたbath architectureとは両立しない

ことの最小witnessになる。

## Claim 3: 有限データcertificate

測定誤差を含む有限データから、

- REALIZABLE
- NON-REALIZABLE
- ABSTAIN

を返す半決定手続きを構築する。

非実現可能性は、誤差集合内の全行列について負固有値が残る場合にのみ宣言する。

## Claim 4: 補助系に対する不変性

最も強い主張は次である。

> 有限個の受動ancilla、追加bathモード、受動的相互接続を加えても、Loewner負性による障害は修復できない。

これは自明ではない。成立には、許容するdilation classを先に固定し、そのクラスにおけるHerglotz性・positive-real性・Schur補元の閉性を厳密に示す必要がある。

## Claim 5: 分野横断的な同一certificate

同じ行列正値性判定を、少なくとも次の三系で実行する。

1. EITまたはCPT透明窓
2. reservoir-engineered qubit / circuit-QED
3. フォトニックバンドギャップ、スペクトルホール、または数値自己エネルギー

定理とcertificateが変更なしに作用した場合にのみ、分野横断性を主張する。

---

## 4. 理論を立てる計算手順

以下は順序を崩してはならない。特に、反例探索を先に行い、後から競合理論の予算を狭めることは禁止する。

## Phase 0: architectureの凍結

### 固定するもの

- 系のHilbert空間次元
- bathの定常性
- 受動性の定義
- 弱結合・Markov・secular近似の範囲
- ポート基底
- 許容ancillaの種類と数
- active element、time-dependent bath、feedbackを許すか
- 透明窓の定義
- 観測可能量から \(S,\gamma\) への写像

### 出力

`architecture_contract.md`

### Gate A0

主張の適用範囲外リストが明示されていること。

---

## Phase 1: 数学定理の符号・仮定監査

### 目的

Herglotz表現、行列値Nevanlinna補間、Loewner正値性が、本計画の符号規約と透明窓条件で本当に成立するかを確認する。

### 計算・証明

1. bath相関から \(h(z)\) までを第一原理から導出
2. \(S\) と \(\gamma\) の符号規約を固定
3. 二点差分商の正値性を記号計算で再確認
4. 透明窓が区間でない場合、ブロック単体の正値性が維持されるか確認
5. 導関数を使わない二点certificateと、完全Loewner行列を区別
6. 非零吸収 \(\|\gamma\|\le\varepsilon\) への拡張境界を導出

### Gate A1

- 反例探索前に、必要条件の定理が完全に証明されている
- 既知定理の単なる再記述部分と、新しい物理的帰結が分離されている

---

## Phase 2: Λ系のsymbolic response

### 目的

EIT系の観測応答から、bath compatibility certificateへ至る写像を導出する。

### 実装

- MathematicaまたはSymPy: Liouvillianの記号消去
- QuTiP: 定常状態と線形応答の数値照合
- 変数: \(\Omega_c,\Delta_p,\delta,\Gamma_e,\gamma_{gs}\)、交差散逸、相関位相

### 求めるもの

\[
\chi_{ij}(\omega),\quad
S_{ij}^{\mathrm{eff}}(\omega),\quad
\gamma_{ij}^{\mathrm{eff}}(\omega)
\]

### 必須監査

- susceptibilityとbath self-energyを混同していないか
- control fieldによるFloquet性を定常bathの性質と誤認していないか
- effective eliminationで人工的な非Herglotz性を生んでいないか

### Gate A2

測定可能応答からcertificateへのpullbackが、近似次数と誤差を含めて明示されること。

---

## Phase 3: 最小witness探索

### 探索問題

局所的制約を満たしながら、正規化Loewner余裕

\[
\eta=-\frac{\lambda_{\min}(L)}{\|L\|_2}
\]

を最大化する。

### 制約

\[
\gamma(\omega_a)\succeq0,
\qquad
\text{各スカラーprojectionは許容},
\qquad
\text{安定な定常状態},
\qquad
\text{有限probe近似が成立}.
\]

### 探索法

1. 粗いSobol探索
2. 局所最適化
3. continuationによる違反領域追跡
4. interval arithmeticまたは高精度計算による符号認証

### 暫定判定基準

以下の数値は探索前に凍結し、結果を見て変更しない。

- **decisive:** \(\eta\ge0.05\)
- **viable:** \(0.01\le\eta<0.05\)
- **fragile:** \(0<\eta<0.01\)
- **fail:** 高精度化・誤差評価後に負性が消える

これらは物理法則ではなく、探索の頑健性を評価するための暫定規約である。

### Gate A3

負固有値が、少なくとも二つの独立パラメータ方向に有限幅を持つこと。

---

## Phase 4: 局所検査を通ることの証明

反例候補について、次を個別に証明する。

1. 各contextのChoiまたはGKSL条件
2. 各ポート単独のスカラーKramers–Kronig整合性
3. positive decay rates
4. 安定性
5. 透明窓または低吸収窓
6. basis changeで消えない物理的負性

### Gate A4

「単に元から非物理な模型だった」という反論を排除できること。

---

## Phase 5: gauge・basis・観測可能性

### 問題

行列のoff-diagonal成分は、ポート基底の再定義で変化する。したがって、単なる行列表現の負固有値では不十分である。

### 必要事項

- 許容基底変換を定義
- certificateがcongruence変換の下で不変であることを示す
- 実験装置の偏光・位相基準と理論ポートを対応づける
- driftを含むtomography誤差を推定する

### Gate A5

負性が座標の取り方ではなく、宣言した物理ポートarchitectureに属すること。

---

## Phase 6: 有限吸収・有限誤差のSDP

### 目的

理想透明窓 \(\gamma=0\) を、現実的な低吸収窓へ拡張する。

測定値の信頼領域を \(\mathcal U\) とし、

\[
\exists\,\widetilde L\in\mathcal U:\widetilde L\succeq0
\]

をSDPで判定する。

- 解が存在する: REALIZABLEまたはABSTAIN
- 全候補が負性を持つ: NON-REALIZABLE

### 実装候補

- CVXPY / MOSEK / SDPA
- bootstrapによる複素応答の共分散推定
- systematic errorを別の不確かさ集合として扱う

### Gate A6

実験分解能の少なくとも5倍のmarginでNON-REALIZABLEが残ることを、暫定的な実験目標とする。

---

## Phase 7: competitor・dilation攻撃

これは本計画で最も重要な段階である。

### 攻撃する競合族

1. より大きな受動bath
2. 有限ancilla付きGKSL
3. classical coupled oscillator / transfer-function model
4. 非Markovian memory kernel
5. Floquet bath
6. active medium
7. 複数bathの切替・context drift
8. hidden port

### 判定

- **受動ancillaで再現可能:** 強い非還元性主張は失敗
- **active/nonstationary bathでのみ再現可能:** architecture依存のno-goとして維持
- **任意の有限dilationで再現可能:** CIRT中心主張としては死亡

### Gate A7

少なくとも「宣言した受動・定常architectureの有限dilation全体」に対する閉性を証明すること。

---

## Phase 8: 第二・第三分野への輸出

EITだけで完結させない。

### 必須候補

- circuit-QEDまたはreservoir-engineered qubit
- photonic bandgap / spectral hole / numerical self-energy

### 条件

- 定理を変更しない
- certificateを変更しない
- 物理量へのpullbackだけを各系で導出する

### Gate A8

同一の非実現性判定が、少なくとも二つの非EIT系で新しいモデル選択を生むこと。

---

## 5. 最も危険で、証明が困難な点

## 危険1: 既存理論そのものだった

Herglotz関数、positive-real性、Loewner補間、passive realization、量子線形系のphysical realizabilityは既知である。

したがって、

> Herglotz関数を開放系へ使った

だけでは新理論にならない。

新規性は、少なくとも次の結合に置く必要がある。

\[
\boxed{
\text{有限次元多準位系}
+\text{局所CPTP模型族}
+\text{有限測定certificate}
+\text{共通bath仮説の反証}
+\text{dilation閉性}
}
\]

**危険度:** 最高  
**最初に行うこと:** 文献監査

---

## 危険2: EIT応答はbath関数ではない

EIT感受率は、control drive、内部coherence、測定ポート、放射場伝播を含む有効応答である。bath correlationの片側Fourier変換と同一ではない。

ここを誤ると、得られたLoewner違反は単に「能動駆動系の応答を受動bath条件に誤適用した」結果になる。

**危険度:** 最高  
**必要な証明:** 観測 \(\chi\) からbath self-energyまたは実現可能性関数への厳密なpullback

---

## 危険3: control fieldが受動性を破っている

EITは外部controlからエネルギーを受ける。系全体を見れば能動的・周期駆動的であり、単純な受動Herglotz条件が適用できない可能性がある。

回避策は二つある。

1. controlを系Hamiltonianの既知の外部操作として分離し、未知bath部分だけに受動性を要求する
2. Floquet-Herglotzまたはscattering passivityへ一般化する

後者は理論を大幅に難しくする。

**危険度:** 最高

---

## 危険4: off-diagonal成分が操作的に測れない

行列条件の新規性は交差成分に宿る。しかし、位相安定な二ポートtomographyができなければ、理論上のcertificateを実験から取得できない。

**危険度:** 高  
**回避策:** 四つのsuperposition probeによる完全tomography、基準位相の同時較正

---

## 危険5: ancillaを足せば修復される

過去の候補が死亡した主因である。

Herglotz類が受動的相互接続や適切なSchur補元で閉じることは期待できるが、任意の量子ancilla・測定feedback・context-dependent couplingまで含めて閉じるとは限らない。

したがって、

> いかなる補助系でも修復不能

とは最初から主張しない。まず、

> 凍結した定常・受動・有限dilation classでは修復不能

を証明する。

**危険度:** 最高  
**PRX可否を決める核心:** この閉性定理

---

## 危険6: 負性が微調整された一点にしか存在しない

行列負性を作ること自体は難しくない。物理的価値は、現実的パラメータの開集合に残るかで決まる。

**危険度:** 高  
**必須検証:** continuation、interval certification、装置分解能との比較

---

## 危険7: 非Markov性で説明されるだけになる

局所GKSL fitの不整合は、共通bath非実現性ではなく、Markov近似の破綻やcontext driftを示しているだけかもしれない。

これは完全な失敗ではない。むしろcertificateを、

- 共通bath仮説の否定
- Markov近似の否定
- 定常性の否定
- 隠れた能動要素の存在

のどれかを示すarchitecture witnessとして解釈できる。

ただし、原因を一意に決めるには追加測定が必要である。

---

## 6. 成功時に何を主張できるか

## 最小成功

> EIT透明窓の有限個の分光データから、各点でCPTPな有効模型族が単一の定常・受動bathとは両立しないことを証明する行列certificateを与えた。

これはEIT固有の新しい整合性試験として成立する。

## PRL級の成功候補

> 完全正値性は、大域的な環境実現可能性を保証しない。最小Λ系において、局所CPTP性とスカラー因果性をすべて満たしながら、単一の定常・受動bathを排除する有限・頑健・gauge不変なwitnessを示した。

必要条件:

- 低次元の明示例
- 開集合での頑健性
- 実験から取得可能
- 既存physical-realizability理論との差が明確
- EIT以外にも直接的含意がある

## PRX級の成功候補

> 有限次元開放系模型族のbath実現可能性について、必要十分条件、dual certificate、最小実現次元、誤差つき判定、受動dilation閉性を与え、複数分野へ同一の判定体系を輸出した。

PRXに必要なのは一つの反例ではなく、**実現可能性を計算する理論体系**である。

---

## 7. 投稿先候補

投稿先は結果の強さによって分岐させる。

| 投稿先 | 適する完成形 | 現時点の位置づけ |
|---|---|---|
| **Physical Review Letters** | 最小Λ系で局所CPTP性と大域bath非実現性を明確に分離。有限・頑健・操作的witnessを提示 | 第一目標。反例と一般定理を短く圧縮できた場合 |
| **Physical Review X** | 必要十分条件、dilation閉性、最小bath次元、誤差つきアルゴリズム、複数分野への輸出 | 長期目標。理論体系が閉じた場合のみ |
| **Physical Review A** | EIT/CPT/量子光学に焦点を絞った行列Kramers–Kronig試験、Λ系の詳細計算、実験提案 | 最も現実的な縮退先 |
| **Physical Review Research** | 分野横断的だがPRLほど単一の鋭い主張に圧縮できない、または体系的数値・方法論が中心 | 方法論・包括的検証の候補 |

### 公式基準との対応

- PRLは、重要問題の解決、新しい研究方向、高い影響を持つ方法、広い読者への特別な関心を求める。本計画では「CPTP性と環境実現可能性の分離」がその核になる。
- PRXは、基礎的発見、新しい分野間接続、重要な新方向、パラダイムの変更、または高影響のcommunity toolを求める。必要十分な判定体系と複数分野への輸出が不可欠である。
- PRAは原子・分子・光物理および量子科学における高品質で重要な成果を対象とする。EIT最小模型と分光certificateに限定した場合に適合する。
- Physical Review Researchは物理全般の理論・実験・方法論・学際研究を対象とする。体系的だがLetter型に圧縮しにくい成果の候補になる。

**参照:** APS各誌の公式Aboutページ（PRL, PRX, PRA, Physical Review Research）、2026-07-25確認。

---

## 8. 投稿戦略の判定木

```text
Loewner型必要条件を厳密証明できるか
├─ No → 理論案を停止または数学規約を修正
└─ Yes
   └─ EIT観測からcertificateへのpullbackを導出できるか
      ├─ No → EIT案は停止。別の受動系へ移す
      └─ Yes
         └─ 局所CPTPかつ行列負性を持つ開集合witnessがあるか
            ├─ No → no-goまたはnegative resultとして再評価
            └─ Yes
               └─ 実験誤差下でも負性が残るか
                  ├─ No → 数理例。PRA/PRResearch以下を検討
                  └─ Yes
                     └─ 受動dilationで修復不能か
                        ├─ No → EIT固有の整合性試験としてPRA候補
                        └─ Yes
                           ├─ 最小反例＋一般定理 → PRL候補
                           └─ 必要十分理論＋複数分野 → PRX候補
```

---

## 9. 最初に実行する計算

優先順位は次の通りである。

### Priority 0: 文献・数学監査

- 行列Herglotz/Nevanlinna補間
- quantum linear systemsのphysical realizability
- passive network synthesis
- multiport Kramers–Kronig
- open-system Lamb shift reconstruction
- EIT susceptibility tomography

**目的:** 既知定理の再発見を避ける。

### Priority 1: 二ポートΛ系の完全な線形応答

- Liouvillianを構築
- 四入力による \(2\times2\) 応答行列の再構成
- 透明窓内の二点・三点データを生成
- effective \(S,\gamma\) へのpullbackを検証

### Priority 2: constrained witness search

- 各点GKSL制約
- scalar projectionの整合性制約
- Loewner最小固有値を目的関数にする
- Sobol探索からcontinuationへ移行

### Priority 3: adversarial competitor test

- classical oscillator
- hidden passive mode
- finite ancilla
- non-Markovian kernel
- active/Floquet explanation

### Priority 4: 誤差つきSDP

- 測定ノイズ
- 位相drift
- 残留吸収
- モデル近似誤差

---

## 10. この計画の評価

### 長所

- 初期計算が低次元であり、短い段階で生死を判定できる
- EITで吸収と分散を同時に扱える
- 成功すればreservoir engineering、開放系同定、分光、数値自己エネルギーへ接続できる
- PRXまで届かなくても、PRLまたはPRAへ縮退できる
- 過去の失敗原因だった「自由度追加による還元」を正面から攻撃できる

### 短所

- 数値計算より、数学的定義と既存研究との差別化が難しい
- EITが外部駆動系であるため、受動性の適用範囲が危うい
- off-diagonal responseの実験tomographyが必要
- ancilla閉性が証明できなければ、一般理論としての非還元性は弱い

### 現時点の総合判断

この案は、**計算可能性については現実的**である。最小Λ系、\(2\times2\) 応答行列、数点の周波数、固有値計算、低次元SDPで初期決着をつけられる。

しかし、最大の障害は計算量ではない。

\[
\boxed{
\text{EITで測る応答が、本当に共通bath実現可能性を証言する量なのか}
}
\]

そして、

\[
\boxed{
\text{その障害が、受動ancillaを追加しても消えないのか}
}
\]

この二点が理論の生死を決める。

前者が成立し、後者が不成立ならPRAまたは限定的PRL候補。両者が成立し、有限データ判定体系まで閉じればPRX候補になる。

---

## 11. 暫定論文タイトル

### PRL型

**Local Complete Positivity Does Not Imply Global Bath Realizability**

### EITを前面に出す場合

**An EIT Witness of Global Incompatibility among Locally Physical Open-System Models**

### PRX型

**Global Bath Realizability of Finite-Dimensional Open Quantum Dynamics**

---

## 12. 最終的な一文

> **EITを説明するのではない。EITを用いて、局所的には完全に物理的に見える開放系模型族が、単一の物理環境としては共存できないことを検査する。**

この一文が理論・計算・実験の全てを貫く中心軸になる。
