# 計画19: CIRT — 因果的インターフェース実現可能性理論（PRX投稿を見据えた新理論提案）

**作成日:** 2026-07-24
**位置づけ:** 実行構成でも数値計画でもない。RISEI/RISERの既存定理・数値証拠・**失敗監査**を踏まえ、
これまでの候補現象がすべて還元死してきた原因を構造的に回避する新理論を提案する検討書である。
実行を強制するものではなく、理論構築・証明・査読前検証のための設計図として次の判断材料に供する。

**計画18（操作的Newton fan理論）との関係:** 置換ではない。計画18の未着手項目
**N5「CP・TP制約の下で実現可能なNewton fanの分類」**に対し、CIRTは
「CPより真に強い制約は何か」という形で答えを与える立場にある（§8.3）。

---

## 0. 出発点：これまでの失敗はすべて同じ形で起きた

このリポジトリの失敗監査（`RISEI_Discovered_Phenomena_Integrated_Summary_2026-07-23.tex`
の status 付録、`docs/plans/10_competitor_null_invariant_objective_plan.md:5-12`）を並べると、
還元のされ方が一種類に収束していることが分かる。

| 候補現象 | 排他的一意性 | 還元先 |
|---|---|---|
| contextuality様 gluing obstruction | **FAIL** | **shared ancilla** — 全contextが1つの普通の加法的GKSLに再埋め込みされる |
| protocol-order fluctuation | **FAIL** | BCH交換子、射影された非可換性、Zeno reduction |
| mean-blind / noise-visible | **FAIL** | tilted-GKSL / FCS、量子回帰定理 |
| relative gauge / quotient atlas | **FAIL** | 群 synchronization（置換群 latent variable）、$G_{ij}=X_jX_i^{-1}$ の対分解 |
| resource-separation matched pair | **FAIL** | Bayes仮説検定、非線形OED |
| intervention-equivalence splitting | **FAIL** | 相関リザーバ理論、Kossakowski tomography、process discrimination |
| ternary irreducible response | **FAIL**（negative controlとして保持） | ラベル付き到達可能性、隠れMarkov模型 |

さらに `competitor_null_program` は **G2 FAIL（`n_survivors = 0`）**、
計画18 §5 は Zeno/Fano/non-normal との定量的差別化を **未確立** と明記している。

**共通構造はこうである。** RISEIの障害はすべて *組合せ論的・代数的* であった
（格子、Möbius、rank、余次元、多面体）。そして組合せ論的障害は、**自由度を足せば必ず消える**。
補助系を1つ足して、そこに手で書いたLindblad散逸を与えれば、どんなcontext族も
1つの加法的GKSLに埋め込める。これが7回連続で起きた。

直近に提示された DCIT（dilation frustration）も同じ形をしている。中心障害は
Kossakowski行列の PSD completion であり、(i) 既知のPSD completion定理（Grone et al. 1984）
の移植に見えるリスクと、(ii) shared-ancilla 逃避で消えるリスクを二重に負う。

> したがって次の理論に課すべき条件はただ一つである。
> **補助系を足しても消えない種類の障害を、最初から中心に置くこと。**

その条件を満たす物理量は、私の知る限り一つしかない。**因果性（受動性）**である。
受動的な部品をどう相互接続しても受動的なものしか作れない——これは組合せ論ではなく
解析学の閉性であり、自由度を足す操作の下で閉じている。

---

## 1. 理論名と中心命題

**CIRT — Causal Interface Realizability Theory**（因果的インターフェース実現可能性理論）。

### 中心命題（短縮形）

> **完全正値性は物理性ではない。** 生成子がGKSL許容であることは、それを生む環境が
> 存在することを保証しない。介入条件付き生成子族は、全contextでCPTPかつ
> 全Bohr周波数でKossakowski正値かつ各ポートで古典Kramers–Kronig整合でありながら、
> **単一の定常・受動的な環境からは因果的に生成され得ない**ことがある。

### 中心命題（厳密形）

> 定常bathへの弱結合という宣言されたarchitectureの下で、介入条件付き生成子族の
> $(\text{減衰率}, \text{Lamb shift})$ データは単一の**行列Herglotz関数**の境界値でなければならない。
> この解析的整合性は、Bohr周波数ごとの完全正値性より真に強い。透明窓上では、
> 非実現性は Lamb shift 行列の差分商の負固有値という**有限・厳密・gauge不変な証明書**で
> 判定でき、しかもこの障害は **Herglotz類がSchur補元と受動的相互接続で閉じている**ため、
> いかなる有限補助系dilationによっても解消できない。

---

## 2. 創設の問い（未解決性・分野横断性）

### 2.1 問い

標準的な開放系理論は常に一方向にしか進まない。

$$\text{bath を与える} \;\longrightarrow\; \text{Born–Markov} \;\longrightarrow\; \text{GKSL 生成子}$$

逆向きの問いは立てられていない。

> **与えられた有限次元Markov生成子（およびその介入条件付き族）に対し、
> それを再現する定常・受動的な環境は存在するか。CPTP性はその条件の
> どれだけを占めるか。残りはどのような有限証明書で反証できるか。**

これが未解決である理由ははっきりしている。GKSL = 物理的、という同一視が
暗黙の公理として置かれてきたためである。RISEIの `ass:physical-cut`
（`docs/theory_papers/Generalized_RISEI_Theory.tex:132-142`）はその同一視を
明示的に採用している数少ない文書の一つであり、CIRTはまさにそこを破る。

**注意（誠実な限定）:** 「文献不存在の証明」を主張しない。Kramers–Kronig、
Herglotz型自己エネルギー、positive-real性、Loewner定理はいずれも既知である（§10）。
未解決と判断しているのは、これらを**有限個の介入条件付き生成子データに対する
判定問題**として組み立て、CPより強い物理性判定として使い、
補助系閉性で非還元性を論証する、という接続である。§10の先行研究監査を
新規性主張の前に完了させることを必須とする。

### 2.2 分野横断先

| 分野 | CIRTが与えるもの |
|---|---|
| 開放量子系の基礎 | 「物理的な生成子」の定義を CP から CP＋因果的実現可能性へ改める |
| reservoir engineering・量子制御 | 最小bathモード数 $=$ Loewner rank（測定可能な整数）、達成可能な (損失, 分散) 領域の waterbed 境界 |
| 量子熱力学 | KMS対称補間。bath分解された熱流・仕事分解は対称証明書を通ったときのみ物理的 |
| 開放系同定・デバイス較正 | 「同じbath」仮説の有限反証試験。隠れ共有リザーバ、crosstalk、context drift の診断 |
| 分光・精密測定 | 透明窓（EIT窓、暗状態、DFS）における**行列**Kramers–Kronig試験。light shift 整合性の検定 |
| 数値多体 | 因果整合スペクトル関数。Nevanlinna解析接続の逆問題としての定式化 |
| 量子情報幾何 | 作用素単調関数 ↔ Morozova–Chentsov/Petz 単調計量。開放系分散への物理的辞書 |

「複数分野を横断しうるか」という要件に対する答えは、
**同じ一つの証明書（Loewner行列の正値性）が上の7分野すべてで同じ役割を果たす**、である。

---

## 3. 原始概念と architecture 宣言

RISEIの規律に従い、**結果を見る前に**次を凍結する。

### 3.1 architecture $\mathfrak A$

$$\mathfrak A=(\mathcal H_S,\ \{A_i\}_{i=1}^p,\ \text{bath state},\ W,\ \mathcal M)$$

- $\mathcal H_S$: 有限次元系。
- ポート $i=1,\dots,p$、相互作用 $H_{\rm int}=\sum_i A_i\otimes B_i$。**ポート基底は凍結する**（§9.5 で基底再定義に対する監査を行う）。
- bath は**定常**（$\langle B_i(t)B_j(s)\rangle$ が $t-s$ のみに依存）。
- $W\subset\mathbb R$: 透明窓（後述）。
- $\mathcal M$: source/readout access（RISEIの $p,c$ 選択をそのまま継承）。

### 3.2 インターフェース関数

bath相関 $C_{ij}(t)=\langle B_i(t)B_j(0)\rangle$ の片側Fourier変換

$$\Gamma_{ij}(z)=\int_0^\infty \! ds\, e^{izs}\,C_{ij}(s),\qquad \operatorname{Im}z>0 .$$

bath状態の正値性より $C(t)$ は作用素値正定値核であり（Bochner）、
$\gamma(\omega)=\int ds\,e^{i\omega s}C(s)\succeq0$、したがって
$\tfrac12(\Gamma+\Gamma^\dagger)\succeq0$ が上半平面で成り立つ（Carathéodory / positive-real 類）。

**インターフェース関数**を

$$\boxed{\;h(z):=i\,\Gamma(z)\;}$$

と定義する。$\operatorname{Im}h=\tfrac12(\Gamma+\Gamma^\dagger)\succeq0$ なので
$h$ は**行列Herglotz（Nevanlinna）関数**である。実軸上では

$$\boxed{\;h(\omega)=-S(\omega)+\tfrac{i}{2}\,\gamma(\omega)\;}$$

ここで $\gamma(\omega)$ は Kossakowski（レート）行列、$S(\omega)$ は Lamb shift 行列
（$H_{\rm LS}=\sum_\omega\sum_{ij}S_{ij}(\omega)A_i^\dagger(\omega)A_j(\omega)$）。

Herglotz表現定理より

$$h(z)=a+bz+\int_{\mathbb R}\Big[\frac{1}{t-z}-\frac{t}{1+t^2}\Big]d\mu(t),
\qquad a=a^\dagger,\quad b\succeq0,\quad \mu\succeq0 \tag{3.1}$$

（$\mu$ はPSD行列測度、$\int(1+t^2)^{-1}d\mu<\infty$）。$\mu$ が bath のスペクトル重みであり、
$\gamma(\omega)=2\pi\,\mu'(\omega)$、$S$ はその Hilbert 変換である。

**この一本の式が理論全体を統べる。** $\gamma$ と $S$ は独立なデータではなく、
一つのPSD測度 $\mu$ の虚部と実部である。GKSL理論は $\gamma(\omega)\succeq0$ を各 $\omega$ で
要求するだけで、$\gamma$ と $S$ を周波数をまたいで結ぶ (3.1) の存在を要求しない。
CIRTはそこを要求する。

### 3.3 介入

RISEIの `ass:physical-cut` と同じ物理操作（detuning、選択的dephasing、結合の物理的切断、
準位・偏光選択、Zeno測定チャネル、reservoir engineering）を扱う。ただし CIRT では
許容条件が変わる。

- **RISEI:** 瞬間生成子がGKSL許容なら物理的。
- **CIRT:** 介入族全体が、**一つの** Herglotz $h$ の（周波数を動かした／$\mu$ を減らした）
  制限として書けなければ物理的でない。

### 3.4 透明窓

$$W:\quad \gamma(\omega)=0\ \ (\omega\in W)\iff \mu(W)=0 .$$

物理的実体: EIT透明窓、暗状態、decoherence-free subspace、フォトニックバンドギャップ、
Purcell抑制帯、希土類イオンのゼロフォノン線近傍のスペクトルホール。
$W$ 上で $h$ は実解析的Hermite値であり $h(\omega)=-S(\omega)$。

---

## 4. 中心現象：因果的Loewner障害

### 4.1 定理C2（厳密）— 因果的Loewner正値性

**定理.** $\omega_1,\dots,\omega_n\in W$ を相異なる点とし、$np\times np$ ブロック行列

$$L_{ab}=\frac{h(\omega_a)-h(\omega_b)}{\omega_a-\omega_b}\ \ (a\ne b),
\qquad L_{aa}=h'(\omega_a)$$

を定める。このとき $L\succeq0$。さらに**各ブロック $L_{ab}$ 単体も $\succeq0$**。

**証明.** (3.1) より

$$h(\omega_a)-h(\omega_b)=(\omega_a-\omega_b)\Big[b+\int\frac{d\mu(t)}{(t-\omega_a)(t-\omega_b)}\Big],$$

よって $u_a(t):=(t-\omega_a)^{-1}$（実数）とおくと

$$L_{ab}=b+\int u_a(t)\,u_b(t)\,d\mu(t). \tag{4.1}$$

任意の $v_1,\dots,v_n\in\mathbb C^p$ に対し、$w(t):=\sum_a u_a(t)v_a$ とおけば

$$\sum_{a,b}v_a^\dagger L_{ab}v_b
=\Big(\sum_a v_a\Big)^\dagger b\Big(\sum_a v_a\Big)+\int w(t)^\dagger\,d\mu(t)\,w(t)\;\ge\;0 .$$

$b\succeq0$、$\mu\succeq0$ より両項とも非負。ゆえに $L\succeq0$。

ブロック単体について: $\operatorname{supp}\mu\cap W=\emptyset$ かつ $[\omega_a,\omega_b]\subset W$ だから、
$\operatorname{supp}\mu$ の任意の $t$ に対し $t\notin[\omega_a,\omega_b]$、したがって
$(t-\omega_a)$ と $(t-\omega_b)$ は同符号で $(t-\omega_a)(t-\omega_b)>0$。
(4.1) は $b\succeq0$ と正重み積分の和なので $L_{ab}\succeq0$。∎

$L_{aa}=b+\int(t-\omega_a)^{-2}d\mu$ も同じ式の $a=b$ 特別値であり整合する。

### 4.2 系C2a（最小witness — 微分不要、二点のみ）

$$\boxed{\ -\,\frac{S(\omega_1)-S(\omega_2)}{\omega_1-\omega_2}\ \succeq\ 0\qquad(\omega_1,\omega_2\in W)\ }
\tag{4.2}$$

すなわち **Lamb shift 行列は透明窓上で作用素反単調（operator antitone）でなければならない。**

必要なデータは、同一bathの下で系のBohr周波数を透明窓内の2点に置いたときの
Lamb shift 行列だけである。負固有値が1つ出れば、**定常受動bathは存在しない**ことが
厳密に証明される。full process tomography も bath tomography も要らない。

### 4.3 gauge不変性（この理論の構造的な強み）

(4.2) は $S$ の**差分商**のみを含む。したがって周波数非依存のHermitianシフト

$$S(\omega)\ \longrightarrow\ S(\omega)+K,\qquad K=K^\dagger \ \text{(bare Hamiltonianへの再吸収)}$$

の下で恒等的に不変である。

これは決定的である。DCITが自ら挙げた即時停止則
「Hamiltonian gauge／Lamb shift を入れると frustration が消える」は、
CIRTでは**構造的に起こり得ない**。「Lamb shift は $H$ に吸収すればよい」という
標準的な反論は、差分商の前で自動的に無効化される。

（$L$ の対角成分 $h'(\omega_a)$ は $b$ を含むが、$b\succeq0$ は追加条件であって
障害を弱めない。最小witness (4.2) は対角成分を一切使わない。）

> **[CG2監査による訂正 2026-07-25、`docs/cirt-cg2-covariance-audit.md`]**
> 上記の不変性主張は正しいが**不完全**である。「最小witnessは対角成分を使わないので $b$ の
> 影響を受けない」という直前の一文は**誤り**——式(4.1) $L_{ab}=b+\int u_au_b\,d\mu$ は
> $a\neq b$ でも成立し、$b$ は非対角ブロック $M=L_{12}$ にも入る。判定を保存する変換の全体は
> 加法群 $\{S\to S+K\}$ ではなく、
> $$S(\omega)\mapsto T^\dagger S(\omega)T+K-B\omega,\qquad T\ \text{定数可逆},\ B\succeq0\ \text{定数}$$
> という半群である。ただし $B\succeq0$ 方向は一方向的（PSDデータから違反を作れない）であり、
> 片側証明書としての健全性は影響を受けない。加えて、congruence方向（$T$）・$\omega$依存な
> 変換いずれについても、記号計算（CG2、T1・T3・T4）により実際に判定は保存されることを確認済み
> ——$\omega$依存の「gauge」は式(3.1)の行列Herglotz性と両立せず（上半平面へ解析接続できない）、
> ポート基底の凍結（§3.1）は規約ではなくこの構造的事実に支えられている。詳細と証明は
> `docs/cirt-cg2-covariance-audit.md` §3–4を参照。

> **[vacuousness反論への回答による訂正 2026-07-26、`docs/cirt-vacuousness-response.md` §4]**
> 上記は $B\succeq0$ が**自由な**追加変換であることを前提にしているが、これ自体が修理を要する。
> $B\succeq0$ を自由に許すと、任意の $M\succeq0$ は $\mu=0,\ b=M$（純リアクタンス $h(z)=a+bz$）
> で実現できてしまい、**2点witness $M\succeq0$ は2点実行可能性の必要条件であるだけでなく
> 十分条件にもなる**。したがって $n=2$ には Loewner不等式そのもの以上の補間論的内容が無い。
> 修理: 物理的bathは総スペクトル重み有限（$\int\gamma\,d\omega<\infty$）であり
> $\Gamma(z)\to0$（$z\to i\infty$）、ゆえに **$b=0$ が導かれる**。$b$ は自由パラメータとして
> 扱うべきではなく、有限重みからの帰結として宣言すべきである。これにより上記の抜け穴が閉じ、
> §10監査で格下げされた **C6（$\mathrm{rank}\,L=$最小bathモード数）が復活する**。
> 補間論的内容は $n\ge3$ で初めて現れる。詳細は `docs/cirt-vacuousness-response.md` §4を参照。

### 4.4 quantum surplus：coherence-only 障害

(4.2) の対角成分は

$$-\frac{S_{ii}(\omega_1)-S_{ii}(\omega_2)}{\omega_1-\omega_2}\ \ge\ 0$$

であり、これは**各ポートごとの古典 Kramers–Kronig**（透明窓での正常分散）そのもの、
教科書的既知事実である。行列条件 (4.2) はそれより真に強い。

最小反例（本設計時に確認済み、初等）:

$$M:=-\frac{S(\omega_1)-S(\omega_2)}{\omega_1-\omega_2}
=\begin{pmatrix}1&2\\2&1\end{pmatrix},
\qquad \operatorname{diag}M=(1,1)>0,\qquad \operatorname{spec}M=\{-1,\,3\}.$$

このデータは:

- 全contextで **CPTP**（透明窓では $\gamma=0$、$S$ は単なるHermite行列で常にGKSL許容）
- 各Bohr周波数で **Kossakowski 正値**、DCIT的な **PSD completion も成立**
- 各ポートで **古典KK正常分散**

を全部満たしながら、**因果的bathを一切持たない**。

DCITが「量子flagshipとして狙う」「未探索の数値現象候補」と書いた
coherence-only frustration が、CIRTでは**初等的かつ厳密に構成される**。
理由は数学的に明快である——スカラー単調性と行列単調性は真に異なる概念であり、
その差はLoewnerによって完全に理解されているからである。

> **現象の名前（本理論固有）:** 暗窓分散フラストレーション
> (dark-window dispersive frustration)、判定子は**因果的Loewner障害**。

> **[Edge (iii) 監査による訂正 2026-07-26、`docs/cirt-edge3-symmetry-audit.md` §4]**
> 本節の「per-portの古典記述では**原理的に**見えない」という表現は**過剰**である。
> 任意の実対称 $M$ はその固有基底で対角化されるため、ポートを悪い軸（利得の偏光軸）に
> 合わせて回転すれば、負固有値は **per-port の Kramers–Kronig 違反として古典的に見える**。
> surplus とは厳密には「**手持ちのポートが悪い軸と整列していない**」という状態である。
>
> 正しい言い方: **固定ポート基底では見えない／検出には基底走査を要する**。
> 行列判定の価値は原理的な強さではなく、**基底走査を不要にする効率**にある
> （固定基底で1回 $2\times2$ を再構成すれば足り、利得軸の事前知識も走査も要らない）。
>
> なお §12 の規律表が禁じている「行列Loewner条件は量子効果である」という誤りを、
> 本節見出しの「quantum surplus」は繰り返している。**改名すべきである**
> （実体は多ポート受動性の余剰であり量子効果ではない——`docs/literature-audit-cirt-passive-realizability.md`）。

### 4.5 非還元性の要石：ancilla閉性

§0で見たとおり、RISEIの候補を全滅させた逃避は「補助系を足して普通のGKSLに埋め込む」だった。
CIRTではこれが閉じない。

**定理C4（決定点・要証明）.** Herglotz / positive-real 類は Schur 補元と受動的相互接続の
下で閉じている。補助系 $A$ を経由した系の実効自己エネルギー

$$\Sigma_S(z)=V\big(z-H_A-\Sigma_A(z)\big)^{-1}V^\dagger$$

は、$\Sigma_A$ がHerglotz類なら再びHerglotz類に属する（自己共役作用素の
resolvent が Herglotz であることと、Herglotz摂動での閉性）。
したがって、**C2に違反するデータは、最終的に真の定常bathで終端するいかなる
有限ancilla鎖・いかなる受動的相互接続によっても実現できない。**

この主張の数学的土台は既存の受動回路合成理論（positive-real lemma / KYP、
Brune合成、Bott–Duffin、Redheffer star product、Krein–Langer）にある。
同時にこれは **RISEI自身のSchur–Riesz機構と同じ道具立て**である——
RISEIは Schur 補元を全面的に使いながら、それに付随する**正値性**を一度も使わなかった。

**なぜ組合せ論的障害と違うのか。** shared-ancilla 逃避が有効なのは、
補助系に「手で書いたLindblad散逸」を無償で与えてよいからである。CIRTはそれを禁じる:
補助系の散逸もまた環境から来なければならず、その環境のインターフェースも Herglotz である。
判定が再帰的に持ち上がり、閉性によって最後まで壊れない。
**これがRISEIの7連敗をもたらした逃避路を塞ぐ、初めての構造的論証である。**

CG3（§9）はこれを定理としてもcounter-searchとしても検証する。C4が偽なら理論は終わる。

---

## 5. 定理ラダー

| # | 定理 | 内容 | 地位 |
|---|---|---|---|
| C1 | Interface representation | 介入条件付きデータは単一の行列Herglotz $h=i\Gamma$ の境界値。$(\gamma,S)=(2\operatorname{Im}h,\,-\operatorname{Re}h)$ | architecture宣言（標準導出、仮定の明示が仕事） |
| **C2** | **因果的Loewner定理** | 透明窓上でブロックLoewner行列 $\succeq0$、各ブロックも $\succeq0$ | **厳密（§4.1に証明）** |
| **C3** | **CP ⊉ 因果性** | C2に違反するCPTP・PSD-completable・per-port-KK整合な生成子族が**有限幅で**存在 | **中心現象・要構成（CG1）** |
| **C4** | **ancilla閉性／非還元性** | 受動的dilationではC2違反を実現できない | **決定点・要証明（CG3）** |
| C5 | 実現可能性階層 | $n$点実現可能集合はLoewner $P_n$ 階層に沿って**真に**減少 ⟹ 因果性は有限予算で反証可能だが検証不可能 | 定理候補 |
| C6 | 閾値剛性・最小bath | $\det L=0$ ⟹ 補間関数は一意かつ有理、McMillan次数 $=\operatorname{rank}L=$ **最小bathモード数** | 定理候補 |
| C7 | cut–shift waterbed | セクターcut（$\Delta\mu\succeq0$ の除去）は $\Delta S(\omega)=-\int d\Delta\mu(t)/(t-\omega)$ を強制し、1次モーメント総和則を伴う。**タダのcutは存在しない** | 厳密系（C2と同型の議論） |
| C8 | Möbius–因果性の従属 | $h$ は $\mu$ に線形 ⟹ port cut はinterface levelで厳密にMöbius加法的。応答の高次Möbius成分は単一の因果interfaceに従属し、厳密な因果不等式を満たす | 定理候補 |
| C9 | response pullback | 系観測量から $S(\omega_a)$ を復元する最小 source/readout・context数・shot数。dual witness を測定量で書く | 条件付き定理候補 |
| C10 | 頑健証明書 | 残留吸収 $\gamma\le\varepsilon$ と測定CIに対する定量Loewner、ABSTAIN分岐 | 要証明 |
| C11 | KMS／熱的輸出 | $\gamma(-\omega)=e^{-\beta\omega}\gamma(\omega)$ は対称補間問題を課す。bath分解された熱流は対称証明書を通ったときのみ物理的 | 輸出定理候補 |

### C5 について（認識論的に新しい主張）

作用素単調性には次数階層 $P_1\supsetneq P_2\supsetneq\cdots\supsetneq P_\infty$ があり、
$P_n$ への所属は大きさ $n$ のLoewner行列の正値性そのものである。
$n$ 個のcontextで測れるのは $P_n$ までである。したがって

> **因果的実現可能性は、有限の介入予算で反証できるが、検証はできない。**

これは開放系モデル検証における非対称性を初めて定量化する主張であり、
RISEIの fail-closed / ABSTAIN 規律と完全に整合する（証明できないものは
ABSTAINに落とす、が理論の帰結として出てくる）。

### C7 について（RISEIの理想化を壊す帰結）

RISEIの `ass:physical-cut` は cut を「その周波数でのLindblad項の除去」として扱える前提に立つ。
因果性の下ではこれは不可能である。$\mu\to\mu-\Delta\mu$（$\Delta\mu\succeq0$）は

$$\Delta S(\omega)=-\int\frac{d\Delta\mu(t)}{t-\omega}$$

を**すべての周波数で**強制し、$-\Delta S$ 自身が再びHerglotzなのでcut帯の外では符号確定、
かつ $\int\Delta\gamma(\omega)\,d\omega/2\pi=\Delta\mu(\mathbb R)$ という厳密な総和則を伴う。

$$\boxed{\text{散逸を消すには、必ず決まった分だけ分散を支払わなければならない}}$$

——開放系版の waterbed 定理。これは RISEI の tube／Newton fan の議論に
新しい制約軸を持ち込む。

### C8 について（RISEIの既存厳密結果との接続点）

$h$ は $\mu$ に**線形**なので、ポートcutは interface level では厳密にMöbius加法的であり、
2次以上のMöbius成分は interface level では恒等的に消える。
`q2s1_closed_forms.json` の `mobius_double_difference = 0`（top元でのみ厳密ゼロ）は
この構造と整合する。応答の高次Möbius成分 $\Omega_T$ が非零なのは、応答が $h$ の
**非線形関数（resolvent）**だからであり、したがって

> すべての高次Möbius成分は**単一の加法的因果interfaceに従属する**。

RISEIの `cor:mobius-neutral`（$\int\Omega_T\,d\omega=0$）は、この従属関係の
**モーメント層**の1メンバーである（解析性のみを使う）。C2はそれに加えて
**bath正値性**を使う**正値性層**であり、真に強い。無限に多くの制約のうち
RISEIは1本だけを見つけていた、という位置づけになる。

---

## 6. 数学体系の閉性

CIRTの計算は fail-closed chain として閉じる。

```
context分解された応答
   ↓  凍結ポート基底での正準 (γ(ω_a), S(ω_a)) 抽出
   ↓  context非依存 bare H の消去（差分商なので構造的に自動、§4.3）
   ↓  透明窓監査 (γ ≤ ε on W)
   ↓  Loewner行列 L の組み立て
   ↓  固有値判定 / SDP feasibility
   ├─ CAUSAL   : 最小次数 + 全整合bathのNevanlinna線形分数パラメトリゼーション
   ├─ ACAUSAL  : dual witness v (v†Lv<0、測定contextのみにsupport)
   │             + 最小障害context対 + 必要な追加環境次元の下界
   └─ ABSTAIN  : 理由コード（窓不十分／CI過大／pullback不能）
```

### 6.1 なぜ閉じるのか

Nevanlinna–Pick／Loewner 理論は、この設計図が必要とする4つをすべて**既に完備している**。

| 必要なもの | 対応する既存結果 |
|---|---|
| 存在の必要十分条件 | Loewner行列／Pick行列の正値性（有限、SDP） |
| 反証証明書（dual witness） | 負固有ベクトル $v$、測定contextのみにsupport |
| 全解のパラメトリゼーション | Nevanlinna線形分数変換（自由Schurパラメータ）= gauge fiberの完全atlas |
| 最小資源 | 退化時の一意有理補間、McMillan次数 = 最小bathモード数 |

RISEIが「quotient atlas」「relative gauge」「ABSTAIN」「最小資源」として
手作りしてきたものが、ここでは**理論の native 構造として初めから揃っている**。
これは偶然ではなく、正しい数学的枠組みを選んだことの帰結である。

### 6.2 閉性の限界（誠実な記載）

閉性は「すべての無制限な実現可能性問題を解くこと」ではない。
**宣言したarchitectureごとに、有限判定・構成解・反証certificate・ABSTAINのいずれかを必ず返す**
ことで実現する。特に:

- 透明窓を持たない場合（$\gamma>0$ が至るところ）、実軸上の点データだけでは
  Pick条件が退化して**障害が消える**。C10（定量Loewner）が実質的な適用範囲を決める。
- 非定常bath・初期相関・強結合はarchitectureの外である（RISEIの deferred list を継承）。

---

## 7. RISEIから継承するもの・破る仮定

### 7.1 継承

- 介入Boolean格子とMöbius分解（`thm:mobius-unique`）
- source/readout selection と有限資源signature
- Schur補元機構（Schur–Riesz tube calculus の計算層）
- claim hierarchy（Definition → Exact → Conditional → Conjecture → Numerical phenomenon → Numerical certificate）
- Stop A–D と fail-closed / ABSTAIN 規律
- Q5 の実験座標 pullback $Q_{\rm exp}=J_\Theta^\top Q\, J_\Theta$（`q5_experimental_pullback_program/common/charts.py`）
- 結果を見る前に定義を凍結する規律

### 7.2 破る仮定：`ass:physical-cut`（A2）

RISEI は「瞬間生成子がGKSL許容であれば、その介入は物理的」と宣言する
（`Generalized_RISEI_Theory.tex:132-142`）。CIRTはこれを **必要だが不十分**とする。

帰結は3つ、いずれも既存資産に直接効く。

1. **RISEIの許容cut族の一部は非物理である可能性がある。** certified済みの現象を
   因果的許容性で再監査しなければならない。とくに pattern (b) の $\theta_c=\pi/2$ 点
   （Gate G4 FAIL、$r_\star=0$、$\varepsilon\approx3.664\times10^{-5}$ rad）:
   要求される介入族はそもそも因果的に実現可能か。
   **通れば** fine-tuning は物理的に許された細さであり、**通らなければ**
   G4 FAIL に数値的でなく物理的な説明が付く。どちらでも情報価値が高い。
2. **Möbius成分は独立な現象論データではない**（C8）。単一の加法的行列測度に従属し、
   厳密な因果不等式を満たさなければならない。
3. **計画18の未着手 N5** に答えを与える立場になる（§8.3）。

### 7.3 順序の変更

従来（RISEI／計画18）:

$$\text{generator}\to\text{sector intervention}\to\text{response classification}\to\text{Newton fan}$$

CIRT:

$$\text{generator族}\to\textbf{因果的実現可能性監査}\to\text{物理的介入族}\to\text{RISEI/Newton fan の分類}$$

CIRTはRISEIを否定せず、**どのsector calculusが同一の物理interfaceに対して正当化されるか**
を判定する前段理論になる。この点はDCITの設計意図と同じであり、CIRTはその意図を
還元されにくい数学の上で実装し直したものと見てよい。

---

## 8. 非還元性監査（Stop D 対策）

RISEIの7連敗はすべて Stop D（差別化の失敗）で起きた。したがってこの節が本設計図で
最も重要である。

### 8.1 各競合に対して示すべきこと

| 競合 | 危険 | CIRTが示さねばならない差 |
|---|---|---|
| **Kramers–Kronig／分散関係** | 「因果性の話は全部KKで既知」 | KKは**与えられた**感受率の性質であり判定手続きを与えない。CIRTは有限データからの**逆問題の判定**。KKはスカラー・点ごと、行列Loewner階層は真に強い（§4.4の $M$ が反例）。KKは最小bath次元も剛性も介入計算も与えない |
| **shared-ancilla GKSL埋め込み** | RISEIを7回殺した逃避 | **C4（§4.5）**。受動性は補助系合成で閉じる。これが立てば初めて構造的な非還元性が成立する。**立たなければ理論は終わる** |
| **DCIT／PSD completion／channel compatibility** | 「同じ障害の言い換え」 | すべて**周波数局所**層。C2違反は、各周波数のPSD性もglobal PSD completionも全部通った上でなお起きる。DCITはCIRTの真部分集合に降格する |
| **process tensor／quantum comb** | 「十分一般だから同じ判定を出せる」 | 実dilation由来なので非因果的対象は作らないが、**生成子レベルデータからrealizabilityを判定できない**。bathの周波数解析性も最小モード数も持たない。CIRTは $O(np^2)$ 個の実数から判定する。full process tomographyとの資源差を定量化すること |
| **unravelling／trajectory theory** | 「interface依存は既知」 | C2は $(\gamma,S)$ 同時の条件で jump frame 不変。unravellingの選択とは独立 |
| **quantum linear systems の physical realizability**（James–Nurdin–Petersen、Gough–James SLH） | 最も近い先行研究 | Gauss／線形限定、かつ**単一系**の交換関係保存条件。介入context間の補間・判定問題ではなく、有限次元GKSLのBohr周波数データも扱わない。**最重点の先行研究監査対象** |
| **pseudomode／Markovian embedding**（Tamascelli et al.） | 「同じ構成をしている」 | spectral densityを**与えて**bathを作る。実現可能性は仮定されており、逆問題を解かない |
| **operator monotone／Petz単調計量** | 「純数学の移植」 | 数学は既知。新規部分は**開放系分散への物理的辞書**と、それを物理性判定に使うこと |
| **古典Markov／HMM** | §4.4の $M$ が古典covariance completionで再現されうる | 対角（per-port）データは具体的スカラーbathで実現可能、行列データは実現不能、という分離を明示する（CG4） |

### 8.2 「KK関係は既知だから新しくない」への回答（想定査読）

正しく、かつ限定的に答える。

1. スカラーKKは既知。**行列Loewner階層は既知の物理的主張ではない**——
   「各ポートで正常分散なのに行列としては因果的bathが存在しない」という
   開放系の主張は文献に見当たらない（§10で確認する）。
2. KKは性質であって**判定手続きではない**。有限個の生成子データから
   YES/NO/ABSTAIN と dual witness を返す手続きは新しい。
3. KKは**最小bath次元**も**閾値剛性**も**介入計算**も与えない（C6, C7）。
4. 最大の新規性は **C4（ancilla閉性による非還元性）**である。
   これはKKの帰結ではなく、受動性の閉性の帰結である。

### 8.3 計画18（操作的Newton fan）との関係

計画18の N5「CP・TP制約の下で実現可能なNewton fanの分類」は未着手のままである。
CIRTは制約を CP から **CP＋因果性** に強めることでこの分類問題に
実質的な入力を与える。すなわち、$\nu(s)=a+z\,s$ の指数対 $(a,z)$ のうち
どれが因果的に実現可能かを問える。C7（waterbed）はその最初の制約である。

逆にCIRTは計画18を必要としない。両者は独立に成立し、接続は選択肢である。

---

## 9. 検証Gate（優先度順）

| 優先 | Gate | 目的 | 判定基準 |
|---:|---|---|---|
| 0 | **定義凍結** | 結果を見る前に固定 | architecture $\mathfrak A$、ポート基底、窓定義、比較class、競合baseline、一意性判定基準 |
| 1 | **CG1 exact seed** | C3を成立させる | C2の記号的証明＋C2違反する**具体的有限次元GKSL族**（qutritまたはΛ系、2ポート以上）。**違反領域が有限幅**であること（G4の轍を踏まない）が必須。**[2026-07-25更新]** CG2監査（下記）によりΛ系は非対角 $M$ を持てないことが判明（`docs/cirt-cg2-covariance-audit.md` §2）。CG1の具体構成は**縮退多重項構造**（縮退基底/励起2重項→単一準位、ポート=偏光チャンネル、つまみ=等方的光シフト）に差し替える必要がある。qutritまたはΛ系のままでは未着手のまま留める |
| 2 | **CG2 gauge監査** | 最大の想定反論を潰す | $S\to S+K$、jump frame unitary混合、$H_{\rm LS}$/bare $H$ 再分割、ポート基底再定義、secular近似の緩和——すべてで障害が残存すること。**判定: PASS（2026-07-25、`docs/cirt-cg2-covariance-audit.md`）。** congruence方向・$b$項・$\omega$依存gaugeいずれでも witness は保存される。ただし副産物として secular構造からΛ系がquantum surplusを持てないことが判明し、CG1の実装対象を変更する必要がある（§4.3に errata 追記済み。secular緩和の限界は未決） |
| 3 | **CG3 ancilla閉性** | **理論の決定点** | C4の証明、および $N=1,\dots,N_{\max}$ の受動dilationによる敵対的実現探索が全滅すること |
| 4 | CG4 quantum surplus | 古典還元を破る | 対角データは具体的スカラーbathで実現、行列データは実現不能、という明示的分離 |
| 5 | CG5 頑健性 | 実験可能性 | 残留吸収 $\gamma\le\varepsilon$ と測定CIを入れてもマージン $>0$。C10の定量Loewnerを証明 |
| 6 | CG6 競合blind監査 | Stop D | process tensor／channel compatibility／PSD completion／スカラーKK／pseudomode fit のいずれも違反を検出せず、CIRTだけがより少ない情報から検出 |
| 7 | CG7 RISEI再監査 | 仮定破りの回収 | pattern (b) 介入族と $\theta_c=\pi/2$ 点の因果的許容性を判定（§7.2） |
| 8 | CG8 実験pullback | 物理座標へ | Eu³⁺:Y₂SiO₅（`eu_platform_program` を再利用）または circuit-QED 多ポート。透明窓での測定可能な行列KK試験を予言。第二アーキテクチャで再現 |

**依存関係:** CG1 → CG2 → CG3 が直列の決定路である。CG3 が落ちれば以降を実行する意味はない。
CG1–CG3 は比較的安価であり、**早期に理論を殺せる設計**になっている。

### 9.1 Stop条件（PRX中心理論から降格）

次のいずれかが成立した時点で降格する。

- 反例族が測度ゼロ／fine-tuningのみ（**Gate G4 の再演**）
- **C4が偽**：有限ancilla受動dilationでC2違反が実現できてしまう
- 物理的制約により行列条件が対角条件から自動的に従う（quantum surplus消滅）
- 透明窓の理想化を外すとマージンが実験誤差以下に消える
- ポート基底の再定義またはsecular近似の緩和で違反が消える
- dual witness が結果を見た後のfitに依存する
- 先行研究監査（§10）で、同一の判定問題が既に定式化されていたことが判明する

> **[Edge (iii) 監査 2026-07-26 — 判定 ALIVE。`docs/cirt-edge3-symmetry-audit.md`]**
> 上の第1条件（測度ゼロ／G4の再演）と第3条件（quantum surplus消滅）について、
> CG2 T5 が許す唯一の構造（対称性保護された縮退2重項＋偏光ポート）で検証した。
>
> 懸念は「surplus を生む bath 異方性が、$H_{\rm LS}$ を通じて縮退そのものを分裂させ、
> secular の一致条件が cross term を潰す」というもの。**成立しなかった。**
> 14,400点の厳密有理格子・partial-secular 抑圧カーネル3種で、頑健 witness
> （$\alpha=\alpha'=1$、$\beta=1/2$、$\theta\approx43.6^\circ$、$t_g=2$、$\Gamma=7/20$）が
> 3カーネル全て・感度変種・全パラメータ $\pm1\%$ 摂動を生き延びた。$\beta$ 方向の可行幅 **36.6%**。
> **これらの停止条件は発火しない。**
>
> 副産物として2つの実質的な変更:
> 1. **発火条件は想定よりはるかに緩い。** 極が窓に近いほど $1/d^2$ で重みが増すため、
>    $\beta=1/2<\alpha=1$ で足り、**総スペクトル重みは正（媒質は正味吸収性）**。
>    「露骨に非受動な媒質でしか発火しない」という以前の評価は誤りだった
>    （`docs/cirt-vacuousness-response.md` §7 訂正ブロック）。
> 2. **§4.4 の表現は弱める必要がある**（同節の訂正ブロック）。
>
> **ただし §10 の最終条件（先行研究）による降格判定は動かない。**
> Edge (iii) が閉じても scope は `docs/cirt-vacuousness-response.md` §8 のままである。
>
> ~~**次の必須作業:** window honesty 検査。~~
>
> **[Window honesty 監査 2026-07-26 — 判定 ALIVE。`docs/cirt-window-honesty-audit.md`]**
> 上の**第4条件（透明窓の理想化を外すとマージンが消える）**を検証した。各極を HWHM $\Gamma_L$ の
> Lorentzian に置き換え（厳密形 $h(z)=\mu/(t_0-i\Gamma_L-z)$、数値求積で検証済み）、
> $\Gamma_L$ を掃引した。
>
> **有効範囲は $\Gamma_L\in[10^{-4},1/2]$ の4桁**にわたり、掃引範囲で**偽陽性は一度も出なかった**。
> $\Gamma_L=1/100$ では窓漏れ $\varepsilon_{\rm win}=3.6\times10^{-5}$ で witness は健在。
> **点極理想化は結論を作っていなかった。第4停止条件は発火しない。**
>
> 決定的だったのは新たに同定した**偽陽性チャネル**である: $M=\int d\mu/[(t-\omega_1)(t-\omega_2)]$ で
> $t$ が $(\omega_1,\omega_2)$ の内側だと分母が負になるため、**窓内に漏れた重みは PSD 測度でも
> $M$ に負に寄与する**（制御 NC9 が $\omega=0$ の PSD 極で $M=-4I$ を厳密確認）。
> この経路は実在し、極が窓の縁 $|t_p|\lesssim1.1$ かつ $\Gamma_L\gtrsim3/2$ で実際に発火するが、
> そこは窓の7〜8割が不透明な領域であり、もはや透明窓ではない。
>
> **副産物: §5 の C10（定量Loewner・頑健証明書、要証明）に定量的入力が入った。**
> $\varepsilon_{\rm win}\lesssim0.1$ なら偽陽性なし、$\gtrsim0.68$ なら判定無効——
> $\varepsilon_{\rm win}$ 自体が ABSTAIN 分岐の guard として機能する。
>
> **これで §9.1 の停止条件のうち4つ（測度ゼロ／quantum surplus 消滅／ポート基底再定義／
> 透明窓理想化）が検証済みで、いずれも発火していない。** ただし最終条件（先行研究監査、§10）
> による降格は**既に発火済み**であり、scope は変わらない。

降格しても CIRT は「開放系モデルの因果的整合性監査ツール」としての価値を保つ。
ただしPRXで主張する新しい開放系理論とは呼ばない。

---

## 10. 先行研究監査リスト（新規性主張の前に必須）

**この節を完了する前に新規性を主張してはならない。**

> **[監査完了 2026-07-25 — 判定: 仕様書 §9 の即時停止条件に該当。`docs/literature-audit-cirt-passive-realizability.md`]**
>
> 本節の監査を実行した結果、**C1・C2・C5・C6・C7、および §6.1 の有限判定体系はすべて先行研究**
> であることが確定した。さらに **C3 が「quantum surplus」と呼ぶ現象は量子的ではなく**、
> 古典多ポート受動性として教科書的に既知である（成分ごとのKramers–Kronigが行列受動性を
> 含意しないことは回路合成の定義そのもの）。**C4 も 1970年代回路理論（正実類のSchur補元閉性、
> Anderson–Vongpanitlerd 1973）の系**であり、「理論の決定点」ではない。
>
> 最重要の prior-art: Löwner 1934（C2・C5）／Youla–Saito 1967「minimum number of reactances」（C6）／
> Mayo–Antoulas 2007「rank(Loewner)=McMillan次数」（C6）／**Fei–Yeh–Zgid–Gull, PRB 104, 165111 (2021)**
> 「solutions exist iff the Pick matrix is PSD」＋出荷済みコードの文書（判定手続き全体）／
> Grivet-Talocia 2004 ほか passivity enforcement（C3の枠組み）／
> **Solgun–DiVincenzo, Ann. Phys. 361 (2015)**（自己エネルギー↔インピーダンス辞書は既に circuit QED の実用手法）。
>
> 本リスト §554 が「最重点」とする James–Nurdin–Petersen は**最も近い先行研究ではない**。
> 最も近いのは §556 に1行だけ挙がっている Nevanlinna 解析接続系列（Fei–Yeh–Gull）である。
>
> **判明した2つの脅威 — 両方に決着（2026-07-26）:**
> 1. **arXiv:2604.17058**（Liu, 2026、ユーザー供給PDFにより全文通読済み）— 開放量子系の記憶核に
>    対する"passivity-analyticity theorem"（Herglotz–Nevanlinna類）。**NEAR MISS と確定。**
>    Pick行列・Loewner行列・透明窓・作用素単調・Lamb shift・Kossakowski・secular・GKSLは
>    本文検索で0件。受動性判定は実軸上の各点符号チェックであり、周波数をまたぐ有限データ補間
>    実行可能性というCIRTのnicheは無傷。ただしRemark 10がCIRT側の機構分析（利得・反転・
>    パラメトリック増幅のみが必然的に違反を生む）を独立に裏書きし、companion work [34] は
>    「隠れた利得の検出」というCIRTと同じ着地点に向けて進行中——隙間は狭く閉じつつある。
>    詳細: `docs/cirt-vacuousness-response.md` §1・§6.1–6.2。
> 2. **vacuousness 反論** — 弱結合導出では $\gamma$ と $S$ は同一の $\Gamma(\omega)$ から生じるため、
>    bathから導出された生成子では Herglotz 性は自動的に成立し、障害は原理的に発生しない。
>    **反論の核は全面的に認める**——C2違反は新しいダイナミクスの発見ではなく、宣言された
>    architectureへの反証である。ただし透明窓上では $S|_W$ は窓外のスペクトル重みで決まり
>    窓内データからは決まらないため、退化しない補間問題として生き残る（守るべきは
>    「到達可能性」であって「不決定性」ではない）。副産物として $b$ 項の抜け穴を発見・修理し
>    （§4.3訂正、C6が復活）、検定力を閉形式で解くと発火には利得重みが吸収重みを上回る必要があり
>    そこでは非受動性は既に露骨——vacuousnessより鋭い実務上の限界。**理論の正体は
>    「因果性のプローブ」から「透明媒質中の隠れた利得を検出する多ポート検出器」へ変わる。**
>    最重要の未解決問題として、CG2が要求する縮退保護対称性をbathも共有すればquantum surplusが
>    恒等的にゼロになる二重拘束が残る（§9.1の停止条件、次作業の最優先）。
>    詳細: `docs/cirt-vacuousness-response.md`（全文）。
>
> **残る最小の空白:** 「Bohr周波数の $(\gamma,S)$ データに対する行列境界Nevanlinna–Pick実行可能性問題」
> という定式化のみ。新しい理論でも現象でも数学でもなく、**方法論的寄与＝計測機器**である。
> 現実的な投稿先は PRA / PRApplied。**PRX・PRL候補ではない。§11のPRX物語は撤回すべきである。**

- Kramers–Kronig関係、総和則、光学定理
- Loewner定理、作用素単調関数、行列単調性の次数階層 $P_n$（Donoghue; Hansen; Osaka–Tomiyama）
- 行列Nevanlinna–Pick補間（Ball–Gohberg–Rodman; Rosenblum–Rovnyak）、Loewner framework（Mayo–Antoulas）
- positive-real lemma／KYP補題、受動回路合成（Brune; Bott–Duffin）、Redheffer star product
- Krein–Langer：Herglotz類のSchur補元閉性（**C4の直接の土台**）
- quantum linear systems の physical realizability（James–Nurdin–Petersen; Gough–James SLH）——**最重点**
- pseudomode／Markovian embedding／擬モード表現（Tamascelli–Smirne–Huelga–Plenio; Mascherpa et al.）
- Nevanlinna解析接続（Fei–Yeh–Gull）、因果整合スペクトル関数の再構成
- Petz／Morozova–Chentsov 単調計量、量子Fisher情報族
- process tensor／operational quantum stochastic processes（Milz–Modi）
- channel compatibility（Kuramochi）、PSD completion（Grone et al.）
- 開放系system identification と識別可能性（Guţă–Kiukas）
- 量子Bode積分／waterbed（Yamamoto; Nurdin ほか、線形量子系）
- 分光: EIT/ATSにおける分散測定、希土類イオンのスペクトルホールと light shift

---

## 11. PRX投稿の物語

**Act I — 見落とされていた前提.** 開放系の全文献は bath → generator の向きに書かれ、
GKSL = 物理的 という同一視を検査しない。

**Act II — 新しい物理性.** 生成子データは単一の行列Herglotz関数の境界値でなければならない。
CP は各周波数の条件、因果性は周波数をまたぐ条件である。

**Act III — 新現象.** 透明窓上で、全ポートで古典KK正常・全contextでCPTP・
PSD completion も成立しながら、因果的bathを持たない生成子族が有限幅で存在する。
判定は $2p\times2p$ 行列の固有値1つ。

**Act IV — 逃げ道がない.** 受動性は補助系の合成で閉じているため、
補助系を足しても障害は消えない。組合せ論的障害との決定的な違い。

**Act V — 有限計算体系.** 存在条件・dual witness・全解のパラメトリゼーション・
最小bathモード数・閾値剛性・ABSTAINが一つの体系に閉じる。

**Act VI — 物理的帰結.** reservoir engineering、系同定、量子熱力学、分光、
多体数値、量子情報幾何で同じ証明書が働く。

### 中心の一文

> **開放量子系において、各介入ダイナミクスが完全正値であることは、
> それらが一つの因果的な環境から生じうることを保証しない。**

---

## 12. 表現の規律

| 誤 | 理由・正しい言い方 |
|---|---|
| 「Kramers–Kronig関係が新しい」 | ✗ KKは既知。新規性は**有限判定手続き・行列階層・ancilla閉性・介入計算の接続**にある |
| 「GKSL理論は間違っている」 | ✗ GKSLは正しい。**CPが物理性の十分条件ではない**と言う |
| 「因果性を破る生成子が存在する」 | ✗ 生成子は因果性を破らない。**定常受動bathから実現できない**と言う |
| 「Lamb shiftは自由パラメータではない」 | ✗ 単一のshiftは自由。**周波数をまたぐshiftの差分商**が拘束される、と言う |
| 「行列Loewner条件は量子効果である」 | ✗ 行列単調性は数学。**ポート間コヒーレンスにしか現れず、per-portの古典記述では原理的に見えない**、と言う |
| 「CIRTはDCITの一般化である」 | ✗ 独立に設計されている。**DCITの周波数局所障害はCIRTの真部分集合に含まれる**、と言う |
| 「因果的実現可能性を検証した」 | ✗ C5より有限予算では**反証しかできない**。「$n$ contextの範囲で反証されなかった」と言う |
| 「透明窓は理想化にすぎない」 | ✗ 実体がある（EIT窓、暗状態、DFS、バンドギャップ、スペクトルホール）。ただし残留吸収の定量評価（C10）は必須 |

claim hierarchy（Definition → Exact → Conditional → Conjecture → Numerical phenomenon →
Numerical certificate）と Stop A–D をそのまま継承する。
**本設計図で「Exact」なのは C2 と C7 のみであり、C3・C4 を含む他はすべて候補である。**

---

## 13. 最初に行うべき作業

大規模数値探索の前に、次の三つを行う。安価であり、いずれかが失敗すれば早期に止められる。

1. **C2の記号的証明を凍結し**、§4.4の $2\times2$ 反例を**実際の有限次元GKSL族に埋め込む**
   （qutritまたはΛ系、2ポート）。違反領域の幅を測る。→ CG1
2. **gauge監査を先に走らせる**（$S\to S+K$、jump frame混合、ポート基底再定義、
   secular近似の緩和）。ここで消えるなら理論はここで終わる。→ CG2
3. **C4を証明するか、反例を探す。** Krein–Langer の Schur補元閉性から
   開放系の主張を組み立てる。同時に $N$-ancilla受動dilationによる敵対的実現探索を回す。→ CG3

この三つを通過すれば、因果的Loewner障害は初めてPRX級の中心現象候補になる。

---

## 14. 最終評価

CIRTを提案する理由は、抽象度でも新奇さでもなく、**このリポジトリの失敗の形に
正面から答えている**という一点である。

- 7つの候補現象を殺した shared-ancilla 逃避を、**受動性の閉性**という構造で塞ぐ（C4）
- DCITが「狙う」と書いた coherence-only frustration を、**初等的かつ厳密に構成する**（§4.4）
- DCITの即時停止則「Hamiltonian gaugeで消える」を、**差分商の構造で自動的に無効化する**（§4.3）
- Gate G4 FAIL のような測度ゼロ現象ではなく、**開集合上の障害**を狙える（要検証、CG1）
- RISEIが手作りしてきた ABSTAIN・quotient atlas・最小資源が、
  Nevanlinna–Pick理論の **native 構造として既に完備**している（§6.1）
- RISEIの `cor:mobius-neutral` を、より大きな因果制約階層の**1メンバーとして位置づけ直す**（C8）

同時に、境界も明確である。

$$\boxed{\text{行列Loewner不等式そのものは新しい数学ではない}}$$

PRX候補になるのは、

$$\boxed{
\text{C3（有限幅のCP-but-acausal相）}
+\text{C4（ancilla閉性による非還元性）}
+\text{C9（有限応答witness）}
+\text{CG6（競合に対するblind predictive surplus）}
}$$

が一つの体系として成立したときであり、それ以前ではない。
とりわけ **C4 が理論の生死を決める**。C4が偽なら、CIRTもまた
「補助系を足せば消える障害」の8番目になる。

---

## 15. 参照ファイル一覧

- `docs/theory_papers/Generalized_RISEI_Theory.tex:132-142` — `ass:physical-cut`（**破る仮定 A2**）、
  `:120-183` 仮定 A1–A7、`:294-317` `thm:mobius-unique`、`:700-726` Stop A–D
- `docs/theory_papers/RISEI_Spectral_Pairing_Theorems.tex` — `thm:sum-rule`（$\mathrm{P.V.}\!\int\chi\,d\omega=\pi c^\top p$）、
  `cor:mobius-neutral`（$\int\Omega_T=0$、**C8のモーメント層メンバー**）、`thm:area-balance`、`lem:min-rule`
- `RISEI_Discovered_Phenomena_Integrated_Summary_2026-07-23.tex` — 現象status付録（**還元死の一覧、§0の出典**）
- `docs/plans/10_competitor_null_invariant_objective_plan.md:5-12` — 失敗史の圧縮記述（shared-ancilla 逃避）
- `docs/plans/18_tropical_valuation_anomaly_theory_proposal.md` — 操作的Newton fan理論、**未着手のN5**（§8.3）
- `patternb_gksl_program/summaries/gates_summary.json` — G4 FAIL（$r_\star=0$、$\varepsilon\approx3.664\times10^{-5}$ rad、**CG7の対象**）
- `q2_joint_only_selection_program/stageQ2S1_symbolic/docs/q2s1_closed_forms.json` — `mobius_double_difference = 0`（**C8と整合**）
- `competitor_null_program/summaries/gates_summary.json` — G2 FAIL、`n_survivors = 0`
- `q5_experimental_pullback_program/common/charts.py`, `common/pullback.py` — $Q_{\rm exp}=J_\Theta^\top Q\,J_\Theta$（**C9で再利用**）
- `eu_platform_program/` — Eu³⁺:Y₂SiO₅ production bundle（**CG8で再利用**）
- `patternb_gksl_program/common/schur.py` — Schur分割（**C4のSchur補元閉性と同じ道具**）

---

**本メモは判断材料であり、上記Gateのいずれを実行するかはユーザーの指示を待つ。**
