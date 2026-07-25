# 文献監査 Pass 3 — CIRT / 受動実現可能性（競合族 N）

**作成日:** 2026-07-25
**対象:** `Blueprints-of-theories/19_causal_interface_realizability_theory_proposal.md`（CIRT）§10「先行研究監査リスト」
**位置づけ:** 仕様書 `docs/literature-audit-specification.md` に従う Pass 3。P0「Interface realizability」の副問題に対応。
**新設する競合族:** **N — 受動実現可能性 / 正実関数・回路合成・Loewner枠組み**
（Pass 1–2 の族 A–G・H・L はすべて量子側であり、この文献層を一度も見ていない）

---

## 0. 結論 — 仕様書 §9 の即時停止条件に該当する

> **CIRT の数学的主張 C1・C2・C5・C6・C7、および §6.1 が「理論の native 構造」と呼ぶ
> 有限判定手続き・dual witness・全解パラメトリゼーション・最小資源は、すべて先行研究である。**
> さらに、C3 が「quantum surplus」と呼ぶ現象は**量子的ではなく**、古典多ポート受動性として
> 教科書的に既知である。

仕様書 §6.2 のkill条件 4「interface obstruction が既知の compatibility / dilation 定理の直接の系である」
に該当し、§9「中心命題と差分のない先行研究が見つかる」による即時停止条件が成立する。
惰性で調査を続けず、中心命題の**撤回・縮小・再定式化**へ戻ることを勧告する。

加えて、CIRT が知らなかった**2つの新規脅威**が見つかった（§4）。うち一方（vacuousness）は
理論に内容があるかどうかそのものを問うものであり、文献照合とは独立に決着させる必要がある。

---

## 1. 監査の限界（先に読むこと）

**この監査では DOI の resolver 検証が一度もできていない。**

本セッションの egress ポリシーが `doi.org`、`api.crossref.org`、`arxiv.org`、`link.aps.org`、
`journals.aps.org`、ScienceDirect、IEEE Xplore、SIAM を含む全出版社ホストへの CONNECT を
403 で拒否する（`curl -sS "$HTTPS_PROXY/__agentproxy/status"` が `connect_rejected` の
policy denial を記録。`https://doi.org/10.1016/0016-0032(67)90582-0` への直接取得も 403 を確認）。

したがって:

- **本監査の全文献は仕様書 §4.2 の基準では「未確認」である。** 到達できたのは検索エンジンの
  索引（abstract・書誌メタデータ・出版社URL文字列）のみで、原文は1本も読んでいない。
- **`references/references.bib` には一切追加していない。** 同ファイルは DOI 検証済みという
  取り決めであり、その条件を満たせないため。
- 下の表の DOI は「検索結果中に当該識別子を含む出版社URLが出現した」ことのみを意味する。
  §5 に検証状態を1本ずつ明記した。
- **egress が通る環境で DOI 解決を再実行することが、本監査の必須の残作業である。**

ただし、この限界は結論を変えない。決定的な文献の abstract 本文（Youla–Saito の
"minimum number of reactances"、Fei–Yeh–Zgid–Gull の "solutions exist if and only if the Pick
matrix is positive semidefinite" 等）は検索結果中に逐語で現れており、判定はその逐語部分に
依拠している。

---

## 2. CIRT の主張ごとの判定

| CIRT | 主張 | 判定 | 先行研究 |
|---|---|---|---|
| **C1** | 介入条件付きデータは単一の行列Herglotz $h=i\Gamma$ の境界値。$(\gamma,S)$ はその虚部・実部 | **教科書** | Breuer & Petruccione §3.3 が既に**ポート添字つき**で $\Gamma_{ij}(\omega)=\tfrac12\gamma_{ij}(\omega)+iS_{ij}(\omega)$ を定義。$\gamma\succeq0$ は Bochner の定理から標準。$h$ の Herglotz 性はこの1行の言い換え |
| **C2** | 因果的Loewner定理（透明窓上で $-\Delta S/\Delta\omega\succeq0$、Lamb shift は作用素反単調） | **IDENTICAL（1934年）** | Löwner 1934 の「易しい半分」の行列版そのもの。透明窓＝$\mathrm{supp}\,\mu$ 外の実区間＝Löwner の定理の標準仮定。$\omega_1\to\omega_2$ 極限は**多ポートFosterリアクタンス定理**（Foster 1924 のスカラー版を Cauer 1931 が n-port へ拡張）。無損失正実行列の Foster 部分分数展開が残差行列PSDを与えるため2行で従う |
| **C3** | quantum surplus：各ポートで古典KK正常なのに行列条件が破れる。反例 $\begin{psmallmatrix}1&2\\2&1\end{psmallmatrix}$ | **数学は既知。「quantum」は誤り** | 多ポート正実性の定義そのもの（$Z+Z^*\succeq0$ であって成分ごとではない）。「element-wise causality は matrix-level passivity を含意しない」は古典電磁気・回路合成で教科書的。Foster の定理が per-port で偽・行列で真であることこそ Cauer 1931 が必要だった理由。反例行列は**教科書的に実現不能なリアクタンス行列**であって発見ではない |
| **C4** | ancilla閉性（受動dilationで違反は消せない） | **1970年代回路理論の系** | 正実類が Schur補元と受動的相互接続で閉じることは Anderson & Vongpanitlerd 1973 で標準。本リポジトリでも符号を直せば4行で証明できることを確認済み（会話記録） |
| **C5** | 実現可能性階層 $P_1\supsetneq P_2\supsetneq\cdots$、有限予算では反証可能・検証不能 | **IDENTICAL** | Löwner 1934 の有限次階層そのもの。厳密な gap は Hansen–Ji–Tomiyama, *Bull. LMS* 36 (2004) 53–58；Simon, *Loewner's Theorem on Monotone Matrix Functions*, Springer GMW 354 (2019) 第14章。「反証可能・検証不能」は認識論的な言い換えであって定理ではない |
| **C6** | 閾値剛性・最小bathモード数 $=\mathrm{rank}\,L=$ McMillan次数 | **IDENTICAL（三重に被弾）** | (i) Youla & Saito 1967 の abstract に "realizations employing a **minimum number of reactances** are studied in great detail" と明記。(ii) Mayo & Antoulas 2007（Loewner枠組みの創設論文）の看板定理が **rank(Loewner)= McMillan次数**。(iii) 退化行列Nevanlinna–Pick の標準結果（Pick行列が特異 ⟹ 解は一意かつ有理、次数 = rank）。**「最小bathモード数」は「McMillan次数」の改名である** |
| **C7** | cut–shift waterbed（散逸を消せば分散を払う）と総和則 | **Herglotz表現の線形性。定理ですらない** | Bernland–Luger–Gustafsson, *J. Phys. A* 44:145205 (2011) が受動系のHerglotz総和則を一般に証明済み。古典側の祖先は Bode のリアクタンス積分定理と Bode–Fano 限界。"sum rules and waterbed effects" は既存の呼称でもある（arXiv:2411.19634） |
| **§6.1** | 有限判定・dual witness・全解パラメトリゼーション・最小資源が「native構造として既に揃っている」 | **本人が既に認めている** | CIRT §6.1 の表自体が Nevanlinna–Pick/Loewner 理論への帰属を明記し、§14 は「行列Loewner不等式そのものは新しい数学ではない」と枠で囲っている。**本監査は §6.1 の記述が正しいことを確認したにすぎない** |

---

## 3. 最重要の prior-art threat（順位つき）

### T-N1. Fei, Yeh, Zgid & Gull（2021）— 数学的中核への直撃、しかも物理誌

- Fei, Yeh & Gull, "Nevanlinna Analytical Continuation", *Phys. Rev. Lett.* **126**, 056402 (2021)
- Fei, Yeh, Zgid & Gull, "Analytical continuation of matrix-valued functions: Carathéodory formalism", *Phys. Rev. B* **104**, 165111 (2021)

この系列は既に、(i) 物理量の**行列値** Herglotz/Nevanlinna 関数を扱い、(ii) **Pick行列のPSD性を
決定可能な存在条件として使い**、(iii) 負固有値を「データが因果的に実現不能」の診断に使っている。
検索結果に逐語で現れる記述:

> "deriving an existence criterion for Carathéodory interpolants directly based on input data,
> where solutions exist **if and only if the Pick matrix is positive semidefinite**"

> "If the Pick matrix is positive definite, an infinite number of solutions to the interpolation
> problem exists; if it is positive semidefinite but not positive definite, **there is a unique solution**."

後者は CIRT の C6「$\det L=0$ ⟹ 補間関数は一意かつ有理」の**逐語一致**であり、しかも
`Nevanlinna.jl` / `TRIQS/Nevanlinna` という**出荷済みソフトウェアのドキュメント**に書かれている。

**CIRT が変えているのは Pick 行列に入れる物理データだけ**（Matsubara Green関数値 → Bohr周波数の
$(\gamma,S)$）。**CIRT はこの2本を §13 で既に引用している**（`:556` 行）にもかかわらず、
§10 の監査で「Nevanlinna解析接続」を一項目として挙げるだけで、中核が同一であることを扱っていない。

**判定: DIRECT HIT。** 引用して差分を説明しない限り desk reject される。

### T-N2. Youla & Saito 1967 — C6 を1967年に殺す

"Interpolation with positive real functions", *J. Franklin Inst.* **284**(2):77–108。
abstract に「有限データからの正実関数補間を回路論の枠組みで解き、**最小リアクタンス数**による
実現を詳細に研究した」と明記。CIRT の辞書（自己エネルギー↔インピーダンス）を通せば
「最小リアクタンス数」＝「最小bathモード数」である。**判定: IDENTICAL。**

### T-N3. Mayo & Antoulas 2007 / Antoulas 2005 — Loewner枠組みそのもの

- Mayo & Antoulas, *Linear Algebra Appl.* **425**(2):634–662 (2007) — Loewner枠組みの創設論文。
  **rank(Loewner)= McMillan次数**、および「最小 McMillan 次数の有理モデルと最小次数実現を
  データから直接」得ることが看板定理。
- Antoulas, *Syst. Control Lett.* **54**:361–374 (2005) — "based on positive real interpolation,
  and is **inspired by the similarity between Löwner and Pick matrices**"。

CIRT が中心的構造洞察として提示する Loewner ↔ Pick ↔ 正実 の三角形が、21年前に活字になっている。
**判定: C6 に IDENTICAL、§6.1 の枠組み主張に STRICT GENERALIZATION。**

### T-N4. Grivet-Talocia 2004 ほか — 「サンプル点の正値性 ≠ 受動性」は分野の存在理由

- Grivet-Talocia, *IEEE TCAS-I* **51**(9):1755–1769 (2004) — Hamiltonian行列の虚固有値で受動性を判定し、
  摂動論で**受動性違反が起きる周波数帯**を特定する。手法が存在するのは答えが点ごとの可否ではなく
  **帯構造**だからである。
- Gustavsen & Semlyen, *IEEE Trans. Power Delivery* **14**(3):1052–1061 (1999)（vector fitting）と
  half-size test matrix 系列。
- Triverio, Grivet-Talocia et al., "Stability, Causality, and Passivity in Electrical Interconnect
  Models", *IEEE Trans. Adv. Packaging* **30**(4):795–808 (2007) — 題名が CIRT の主題そのもの。
- `scikit-rf` は `passivity_test()`（代数的、違反**帯**を返す）と `passivity_enforce()`（有限サンプル、
  狭い違反帯にはサンプル不足の警告つき）を分けている。**オープンソースライブラリの警告文字列**である。

**判定: C3 の概念的枠組みに IDENTICAL。2000年代初頭から工学の常識。**

### T-N5. Solgun & DiVincenzo 2015 — 辞書自体が circuit QED の既存手法

"Multiport impedance quantization", *Ann. Phys.* **361**:605–669 (2015)。
多ポート正実インピーダンス行列の **Brune 合成**（Foster の場当たり的拡張を置き換える）から
量子ハミルトニアンを構成し、**bathモードの明示的な最小集合**と $T_1$ 予測を得る。
関連: Parra-Rodriguez et al., "Quantum fluctuations in electrical multiport linear systems"（arXiv:2110.14604）。

**判定: CIRT は「自己エネルギー↔インピーダンス」の辞書を自分の寄与として主張できない。**
既に circuit QED の実用手法である。CG8 が circuit-QED 多ポートを実験候補に挙げている以上、
この文献群を無視できない。

---

## 4. CIRT が知らなかった新規脅威

### 4.1 arXiv:2604.17058（Liu, 2026年4月投稿）— **未読・最優先で読むこと**

"Kramers-Kronig Relations and Causality in Non-Markovian Open Quantum Dynamics: Kernel, State,
and Effective Kernel"（改題版: "Causality from Projection and Hardy-Space Analyticity of
Non-Markovian Memory Kernels"）。検索結果によれば、Nakajima–Zwanzig記憶核が
ベクトル値Hardy空間 $H^p_+(\mathcal B)$ に属することを証明し、

- **CP-Hardy obstruction theorem**: 近似核の上半平面極は非CPTPな簡約ダイナミクスを含意
- **passivity-analyticity theorem**: 散逸核を **Herglotz–Nevanlinna 類**に結びつける
- moment-based Carleman diagnostic

を示す。**開放量子系において「解析的クラスへの所属を、完全正値性を超える物理性の障害として使う」
という CIRT とまったく同じ修辞的・構造的な動きを、3か月前に行っている。**

現時点で分かる範囲では、記憶核の解析性・極を扱っており、**有限個のBohr周波数データからの
Pick行列判定問題は立てていない**ように見える。しかし egress 遮断のため**全文を読めていない**。

> **この論文を通読するまで CIRT の新規性主張を書いてはならない。**
> Pick/補間の判定基準が含まれていれば CIRT は死ぬ。

### 4.2 vacuousness 反論 — 文献ではなく理論の内部整合性の問題

**これが最も危険である。** 標準的な弱結合導出では $\gamma$ と $S$ は**同一の** $\Gamma(\omega)$ から
生じる:

$$\gamma_{ij}(\omega)=\Gamma_{ij}(\omega)+\Gamma_{ji}^*(\omega),\qquad
S_{ij}(\omega)=\tfrac{1}{2i}\big(\Gamma_{ij}(\omega)-\Gamma_{ji}^*(\omega)\big)$$

そして $\Gamma$ は単一の相関関数 $C(s)$ の片側Fourier変換である。したがって
**bathから導出された生成子では Herglotz 性は自動的に成立し、障害は原理的に発生しない。**
$S$ は $\gamma$ から定数を除いて既に決まっており、拘束されるべき自由度が存在しない。

C2 が非自明になるのは、$(\gamma,S)$ が bath から導出されず、**現象論的に手で置かれた**か、
**トモグラフィで独立に推定された**場合に限られる。その設定は実在する（人は現象論的Lindblad模型に
勝手なレートと勝手なHamiltonianシフトを書く。Lindbladian learning も行われている）が、
そのとき CIRT が与えるのは:

$$\boxed{\text{当てはめた開放系模型が、定常受動bathから生成され得ないことを検出する整合性試験}}$$

であって、新しい物理現象の発見ではない。**これは工学の passivity enforcement（T-N4）が
マクロモデルに対して行っていることの量子版である。**

CIRT §11「PRX投稿の物語」Act III が「有限幅で存在する」と書く生成子族は、この観点では
「bathから導出していない模型を書けば当然そうなる」という同語反復に近づく。
**この反論に答えられない限り、C3 は空虚である。**

---

## 5. 文献リストと検証状態

**全件 DOI 未解決**（§1）。「検索照合」= 当該DOI文字列を含む出版社URLが検索結果に出現したことのみ。

| ID | 文献 | DOI（未解決） | 検証 | 脅威 |
|---|---|---|---|---|
| N01 | Löwner, *Math. Z.* 38:177–216 (1934) | 10.1007/BF01170633 | 検索照合 | **kill C2, C5** |
| N02 | Foster, *Bell Syst. Tech. J.* 3(2):259–267 (1924) | 10.1002/j.1538-7305.1924.tb01358.x | 検索照合 | kill C2（極限形） |
| N03 | Youla & Saito, *J. Franklin Inst.* 284(2):77–108 (1967) | 10.1016/0016-0032(67)90582-0 | 検索照合＋abstract逐語 | **kill C6** |
| N04 | Mayo & Antoulas, *Linear Algebra Appl.* 425(2):634–662 (2007) | 10.1016/j.laa.2007.03.008 | 検索照合 | **kill C6** |
| N05 | Antoulas, *Syst. Control Lett.* 54:361–374 (2005) | 10.1016/j.sysconle.2004.07.007 | 検索照合＋abstract逐語 | strong（§6.1） |
| N06 | Grivet-Talocia, *IEEE TCAS-I* 51(9):1755–1769 (2004) | 10.1109/TCSI.2004.834527 | 検索照合 | **kill C3の枠組み** |
| N07 | Gustavsen & Semlyen, *IEEE Trans. Power Deliv.* 14(3):1052–1061 (1999) | 10.1109/61.772353 | 検索照合 | strong |
| N08 | Fei, Yeh & Gull, *Phys. Rev. Lett.* 126:056402 (2021) | 10.1103/PhysRevLett.126.056402 | 検索照合 | **kill 判定手続き** |
| N09 | Fei, Yeh, Zgid & Gull, *Phys. Rev. B* 104:165111 (2021) | 10.1103/PhysRevB.104.165111 | 検索照合＋abstract逐語 | **kill C6・判定手続き** |
| N10 | Solgun & DiVincenzo, *Ann. Phys.* 361:605–669 (2015) | 10.1016/j.aop.2015.07.005 | 検索照合 | **kill 辞書の新規性** |
| N11 | Bernland, Luger & Gustafsson, *J. Phys. A* 44:145205 (2011) | 10.1088/1751-8113/44/14/145205 | 検索照合 | **kill C7** |
| N12 | Brune, *J. Math. Phys. (MIT)* 10:191–236 (1931) | 10.1002/sapm1931101191 | 検索照合 | background（PR⟺受動実現） |
| N13 | Anderson, *SIAM J. Control* 5 (1967) | 10.1137/0305011 | 検索照合 | background（行列PR lemma） |
| N14 | Benner, Goyal & Van Dooren, *SIAM J. Matrix Anal. Appl.* 45(2):1035–1053 (2024) | 10.1137/23M1580528 | 検索照合 | strong |
| N15 | **Liu, arXiv:2604.17058 (2026)** | — | **未読** | **要通読・最優先** |
| N16 | "All electromagnetic scattering bodies are matrix-valued oscillators", *Nat. Commun.* 14:7724 (2023) | 10.1038/s41467-023-43221-2 | 検索照合 | **kill C3の「quantum」** |
| N17 | Tupkary et al., *Phys. Rev. A* 105:032208 (2022) | 10.1103/PhysRevA.105.032208 | 検索照合 | medium（「CPは物理性でない」の既存版） |
| N18 | Levy & Kosloff, *EPL* 107:20004 (2014) | 10.1209/0295-5075/107/20004 | 検索照合 | medium（同上） |
| N19 | Simon, *Loewner's Theorem on Monotone Matrix Functions*, Springer GMW 354 (2019) | 10.1007/978-3-030-22422-6 | 検索照合 | kill C5 |
| N20 | Delsarte, Genin & Kamp, *Int. J. Circuit Theory Appl.* 9 (1981) | 10.1002/cta.4490090204 | 検索照合 | background |
| N21 | Cauer (1931) — Foster定理のn-port拡張 | — | **書誌未特定** | kill C2（要特定） |
| N22 | Anderson & Vongpanitlerd, *Network Analysis and Synthesis* (1973) | — | 書籍・未読 | **kill C4**（正実類のSchur補元閉性） |
| N23 | Breuer & Petruccione, *The Theory of Open Quantum Systems* (OUP 2002) §3.3 | ISBN 9780199213900 | 節番号未検証 | **kill C1** |
| N24 | Ball, Gohberg & Rodman, *Interpolation of Rational Matrix Functions*, OT45 (1990) | — | 書籍・未読 | kill C6 |

**引用衛生の要修正点**（Pass 3 で判明）:
- half-size test matrix の帰属は Gustavsen & Semlyen であり Grivet-Talocia ではない
- Tamascelli et al. の PRL は **vol. 120**（既存 `literature-master-table.csv` A02 は正しい）
- CIRT §8.1 が「最も近い先行研究」と呼ぶ James–Nurdin–Petersen は**最も近くない**。
  JNP は Gauss/線形系の CCR 保存という代数条件であり、bath の存在を前提にしている。
  最も近いのは N08/N09 の Nevanlinna 解析接続系列である

---

## 6. 残る最小の空白（正直な記載）

「$(\gamma(\omega_k),S(\omega_k))$ を Bohr 周波数で与えたとき、単一の定常受動 bath が存在するか」
を**行列境界 Nevanlinna–Pick 実行可能性問題として立てた**論文は見つからなかった。
残るのはその一点のみであり、性格は次のとおり:

$$\boxed{\text{既知の2定理を、誰も入力していなかった物理対象に対する判定手続きへ溶接した方法論的寄与}}$$

- 新しい理論ではない
- 新しい物理現象ではない
- 新しい数学ではない
- §4.2 の vacuousness 反論に答えられなければ、**空虚**である

投稿先として現実的なのは PRA または PRApplied（EIT文書 §7 の「最も現実的な縮退先」と一致）。
**PRX・PRL 候補ではない。**

---

## 7. 勧告

1. **CIRT の PRX 候補としての位置づけを撤回する。** §14 の
   「C3＋C4＋C9＋CG6 が揃えば PRX 候補」という条件は、C4 が 1970年代回路理論の系であり
   C3 の数学が古典多ポート受動性である以上、成立しない。
2. **arXiv:2604.17058 を通読する。** これが済むまで新規性主張を書かない（§4.1）。
3. **vacuousness 反論に答える**（§4.2）。答えられなければ理論は終わる。文献照合では決着しない、
   理論内部の問題である。
4. **CG1・CG3 に着手しない。** CG3（C4のancilla閉性）は既知定理の系であることが判明したため、
   「理論の決定点」ではなくなった。CG1 は CG2 監査により最小模型の差し替えが必要な状態にある。
5. egress が通る環境で **DOI 解決を再実行**し、`references/references.bib` を更新する（§1）。
6. 生き残らせる場合は、**方法論論文として**、N03・N04・N08・N09・N10 を正面から引用し、
   「開放量子系コミュニティがこの層を輸入していない」という位置づけで書く。

---

## 8. 参照

- `docs/literature-audit-specification.md` §4.2（実在確認）、§6.1（判定規則）、§6.2（kill条件）、§9（停止条件）
- `docs/literature-master-table.csv` — 族 N の行を追加（本監査）
- `docs/cirt-cg2-covariance-audit.md` — CG2 監査（Λ系の失格、§4.3 errata）
- `Blueprints-of-theories/19_causal_interface_realizability_theory_proposal.md` §6.1、§8.1、§10、§13、§14
- `EIT_Minimal_Testbed_for_Global_Bath_Realizability_2026-07-25.md` §5 危険1（「既存理論そのものだった」— 的中）
