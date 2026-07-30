# 量子実現可能性・損失応答 資産監査と新規問い探索

**作成日:** 2026-07-30
**位置づけ:** 開放量子系・量子計測・正値システム・確率過程・量子熱力学の観点からの敵対的監査。
既存設計案（RCT・TPR・Operational Newton Fan・CIRT）を「部品集」として分解し、既存理論に占有されていない
狭い問いを特定する。
**方針:** 魅力的な物語ではなく、最短で壊れ、壊れても残る問いを特定する。投稿誌の格は結果の強さから逆算する。
**監査対象リポジトリ:** `Ideas-of-a-new-theory`、`Memory-Accessibility-Theory`（L0–L3 ゲート・PR #8 含む）、
`Temporal-Stratified-Metrology`（SMRT 資産）。

> **文献アクセスの限界（全域に効く）:** 本監査の文献照合は WebSearch のみで実施し、**WebFetch は
> egress ポリシーで全ホスト 403**。したがって「実在確認済み（メタデータ複数一致）」と
> 「本文未読・主張内容は要約のみ」を厳密に区別する。定理内容の同一性判定が生死を分ける箇所は
> **ABSTAIN：一次文献の全文精読が必須** と明記した。DOI resolver 検証は1件も通っていない。

---

## 0. 確定している失敗結果（受け入れ済み・再提案禁止）

以下は監査の前提として固定する。名称だけ変えた再提案は行わない。

1. 強損失応答の最初の非零係数は **Markov parameter** に対応する（MAT L0 PASS、Woodbury 還元 `R(κ)=κC(κI−A_L)^{-1}B`、
   誤差 `1.70×10⁻¹⁵`）。
2. 損失次数は標準伝達関数の相対次数そのものではなく **d_loss = rdeg T − 1**（一律オフセット、非暗系で厳密に1）。
3. 相対次数そのものを新法則とする路線は不成立（制御理論へ譲渡）。
4. d≥2 の正損失比実現可能性は **凸包（相対内部）条件** `d≥2 ⟺ m₀=0 かつ 0∈relint conv{z_j}`（線形計画で判定可能）。
5. 一般の非暗系で **d ≤ rank G − 1**（Cayley–Hamilton による上限、2,500 試行で違反 0）。
6. d≥3 の実現可能集合は一般に **非凸**（厳密有理数反例 `W=I₅, ℓ=1⃗, r=(1,1,1,−1,−2)`：`h_A,h_B` は d=3、
   中点は d=2）。入れ子「実現可能性錐」としては分類できない。
7. 有限損失窓・有限ノイズでは先頭係数をノイズ以下に隠せ、傾きから真の次数・最小介入階数を
   **モデル非依存に認証できない**（L3：`ε<η` の追加チャネルで d を 3→0 に改変、sup 差 `<10⁻⁶`）。
8. 一回の比例損失掃引だけでは、**到達不能による暗化**（c=(0,0)）と **完全相殺による暗化**（c=(1,−1),h=(1,1)）を
   区別できない（両者とも `R≡0`、無限精度で同一曲線）。
9. ゆえに「一回の損失掃引から正レート模型反証と最小介入資源認証を同時に得る」路線は **凍結**
   （`Memory-Accessibility-Theory/theory/23_loss_realizability_route_freeze.md`、PR #8）。

**生き残った結果:** 正レート・非負source/readout・純粋killing模型に対する**単調性 no-go**、**符号付き干渉系の構成例**、
**有限階数上限 `d≤rank G−1`**、**有限掃引の非識別性**、そして**第二介入が必要という結果**。

---

## A. 現状から再利用可能な結果群

Phase 1 の分類。各結果に (再利用先) を付す。記号は `Memory-Accessibility-Theory` のゲート台帳に準拠。

### A.1 厳密に証明済み（Exact）

| ID | 内容（厳密形） | 出所 | 補題としての再利用先 |
|---|---|---|---|
| **P-MONO** | 単調性 no-go。`A(κ)=A+κG`（非特異M行列）、`u,v≥0`、`G≥0`対角 ⇒ `∂_κ f = −vᵀA(κ)⁻¹GA(κ)⁻¹u ≤ 0`、すなわち `R'(κ)=∂_κ[f(0)−f(κ)] ≥ 0`。**全隠れ次元で成立。** | MAT K1・L3 §2 | 候補DMS（相殺信号の符号確定）・候補KDD（反証の土台） |
| **P-WOOD** | Woodbury モーメント列 `m_k = βW⁻¹(G_S⁻¹W⁻¹)^k α`、大κ展開 `r(κ)=m₀−m₁/κ+m₂/κ²−…`。落ち冪 = 最初の非零 `m_k` の番号。 | MAT G1・plan22 | 全候補の共通言語 |
| **P-RANK** | 非暗系で `d ≤ rank G − 1`（Cayley–Hamilton）。`⌊rank G/2⌋` は**実逆閉巡回 Cayley 部分クラス限定**（Chen–Quimpo Hamilton性）。 | MAT G2・L1・plan22 G9候補 | 候補DMS（介入資源の下限） |
| **P-CONV** | `d≥2 ⟺ m₀=0 ∧ 0∈relint conv{z_j}`（線形計画証明書）。境界解 `h_j→0` は有効階数低下。 | MAT L1・L1.5 | 候補DMS（相殺台の判定） |
| **P-NONCVX** | d≥3 実現可能集合の非凸性（厳密有理数反例、`m₂(h)=hᵀQh` の不定符号2次形式が多面体上で消えるか）。 | MAT L1.5 §3 | 錐分類の**否定的補題**（新提案が錐を主張するのを禁じる） |
| **P-DARK2** | 暗機構の非識別ペア：`c=(0,0),h=(1,1)`（到達不能）と `c=(1,−1),h=(1,1)`（相殺）は比例掃引で同一。比を `h=(1,2)` に破ると相殺のみ非零。 | MAT L3 §5 | **候補DMS の出発点** |
| **P-PORTAL** | パリティ保護証人 `R = i·u·v·(c₁−c₂)·κ / det A`、危険係数 `[N]_{Γ³κ²} ≡ 0`（パリティ）、`[N]_{Γ⁴κ¹} ≠ 0`。 | MAT K3R | 候補KDD（干渉系の明示構成） |
| **P-SEP** | クラス境界反例：混合符号 readout / rerouting / q依存 interface はいずれも**古典**上昇 fan を許す。 | MAT K2 §5–7 | 候補KDD（反証の適用範囲確定＝killing の定義依存性） |
| **P-CIRT** | 因果的 Loewner 障害 `−(S(ω₁)−S(ω₂))/(ω₁−ω₂) ⪰ 0`（透明窓上で Lamb shift 行列は作用素反単調）、C7 waterbed。数学は健全。 | CIRT §4.1 | 方法論部品（**新規性は失効**、族N） |
| **P-CCONE** | 母集団保存 GKSL 切断 ⇒ jump 対角（補題1）、対角 jump のコヒーレンス減衰は cnd 錐（補題2、既知数学の輸入）。 | CCRT S1–S2 | 候補CCC（ただし §D.3 参照） |

### A.2 数値的に認証済み（Numerically certified）

| ID | 内容 | 出所 |
|---|---|---|
| N-FLOOR | 減衰床補題 `Λ_j = ½(Γ_out(j)+Γ_out(1))` が凍結2証人の `D` を厳密再現。 | TPR W1a、SMRT `prop:phase-n/h` |
| N-CROSS | クロスオーバー `κ_× ~ ε^{−1/(d−1)}`（3 decade で定数 1.036）、`Γ_× ≈ 0.55/|δ|`。 | MAT G3・K3 |
| N-RATIO | 単一測定対で反証：`log ρ = −7.3` @ Γ=10⁴、100%相対ノイズでも1対で足りる。dip 深さ Γ 非依存（分散 0.14 dB）。 | MAT G4・G6 |
| N-SMRT | SMRT 境界層 Fisher 情報：断熱消去は `Γ²` を失う。分岐 `(5,9,11)` 系、B0–B3 ゲート全 PASS。 | SMRT PRL |

### A.3 反例により撤回・凍結済み（Retracted/Frozen）

| ID | 撤回された主張 | 死因 |
|---|---|---|
| F-REL | 「損失冪 = 相対次数」（−1 なし） | L0 オフセット |
| F-CONE | 全損失次数の入れ子凸錐階層 | L1.5 非凸 |
| F-CERT | 一回掃引でモデル非依存の最小介入階数認証 | L3 非識別 |
| F-ACC | 異常次数 = 実現余次元（ONF/18 初版） | 外部査読、`ν(s)=s` 単一特徴で反例 |
| F-CIRT-NOV | CIRT の C1・C2・C5・C6・C7 新規性 | 族N（Löwner 1934 / Youla–Saito 1967 / Fei–Yeh–Zgid–Gull 2021 / Anderson–Vongpanitlerd 1973） |
| F-T1T2 | TPR の T1（証明経路）・T2（自己矛盾で Conjecture 降格） | 内部還元監査 W1–W4 |
| F-WPOT | 語領域受動性障害 | 受動実現 400/400 が半正定値性を破る |
| F-RISE | 「上昇 fan は対称性保護される」（無条件） | MAT G1、18 の対称性なし有界上昇クラス |

### A.4 まだ利用可能だが中心命題を失った結果（Orphaned assets）

| ID | 内容 | 中心を失った理由 | 補題として生きる先 |
|---|---|---|---|
| O-T7 | TPR T7：理想切断を精度 ε で実装する熱力学コスト `~1/ε`（Landauer 型）。 | T1・T2 が中心を失い TPR 全体が PRX 落ち | 候補ICE |
| O-KAPPA | CCRT κ*：床が cnd 内部点なら検閲パターンを `κ≤κ*` まで救済（n=3 一様床で κ*=3 厳密）。 | 補題2が既知数学、A1 kill が高確率 | 候補CCC（要 §D.3） |
| O-QSTAR | CCRT q*：Γ比例床で `κ=κ₀Γ^q` が `q>q*=1` で漸近錐外。 | 上記に連座 | 候補CCC |
| O-NEWTON | 重み付き Newton 次数 `d_{q,κ₀}(P)=max(a+qb)`、`thm:polyhedral-selection`。 | Γ^q パスは scaffolding（G4/G6） | ONF/18 の N1、SMRT との橋 |
| O-SIGNED | 符号付き測度 `c_k=⟨E,v_k⟩⟨w_k,ρ₀⟩` は source/readout 独立ゆえ片側正値に落ちない。 | WPOT 撤回 | 候補DMS（相殺の代数的特徴づけ） |

---

## B. 競合文献が残している未解決問題

Phase 2 の前段。**同一定理は全域で未発見。** 各領域で最近接文献と明示的差分を示す。

### B.1 多重介入・多実験の同定可能性（← 候補DMS の主戦場）

- **Ovchinnikov, Pillay, Pogudin, Scanlon**, *Multi-experiment parameter identifiability of ODEs and model theory*,
  SIAM J. Appl. Algebra Geom. **6**(3), 339–367 (2022), DOI 10.1137/21M1389845, arXiv:2011.10868（実在確認済み）。
  → **単一出力の線形 ODE では単一実験と多実験の同定可能性が一致する**ことを証明。
  **差分:** 彼らの「実験」は同一パラメトリック ODE の初期条件/入力の変更であり、**生成子（killing レート）を構造的に変える介入ではない**。
  正値性/M行列制約なし、相対次数・暗機構分離を扱わない。むしろこの「単一出力では多実験が無益」結果は、
  DMS が主張する「第2介入は生成子の形を変えるから有効」との**防御的対比**に使える。
- **Gross &amp; Blüthgen ほか**, *Identifiability and experimental design in perturbation studies*,
  Bioinformatics **36**(S1), i482–i491 (2020), DOI 10.1093/bioinformatics/btaa404（実在確認、著者一部 ABSTAIN）。
  → 摂動によるネットワーク同定可能性を**最大フロー条件＋マトロイド**で特徴づけ、必要摂動数を最小化。
  **差分:** 定常/線形化応答からの**係数回復**であり、相対次数・落ち冪や「到達不能 vs 相殺」の**機構識別**は扱わない。
- **線形コンパートメントモデル**（Meshkat/Sullivant 学派、arXiv:2102.04417「leak/edge 除去の同定可能性への影響」ほか）。
  → 入出力ポート固定でレート定数回復可能性を問う。**差分:** 能動的に加える killing を第2実験として扱わない。

### B.2 単調性証人と ENAQT の逆例（← 候補KDD の生命線）

- **Rebentrost, Mohseni, Kassal, Lloyd, Aspuru-Guzik**, *Environment-assisted quantum transport*,
  New J. Phys. **11**, 033003 (2009), DOI 10.1088/1367-2630/11/3/033003, arXiv:0807.0929（実在確認済み）。
- **Plenio &amp; Huelga**, *Dephasing-assisted transport*, New J. Phys. **10**, 113019 (2008),
  DOI 10.1088/1367-2630/10/11/113019（実在確認済み）。
  → 輸送効率は脱位相レートの**非単調関数**（上昇→ピーク→Zeno 減衰）。
  **決定的差分（＝逆例）:** ENAQT の非単調性は tuned quantity が**脱位相**であり、
  **古典確率 hopping+dephasing 模型で再現される**。ゆえに「損失パラメータへの非単調応答」だけでは古典模型を反証しない。
  DMS/KDD は **killing/loss 掃引（単調）** と **dephasing 掃引（古典で非単調）** を峻別せねばならない。
  この峻別が主張の生命線であり、同時に新規性の源泉。
- **Monras, Chęcińska, Ekert**, NJP **16**, 063041 (2014)：介入強度→コヒーレンス推論の**最強競合**（MAT NR-1、必須引用）。
  混合符号 readout や rerouting で古典も上昇する（P-SEP）。

### B.3 暗状態の機構識別（← 候補DMS の物理写像）

- **Anisimov, Dowling, Sanders**, *Objectively discerning Autler–Townes splitting from EIT*,
  PRL **107**, 163604 (2011), DOI 10.1103/PhysRevLett.107.163604, arXiv:1102.0546（実在確認済み）。
  → 干渉起源（EIT）と準位分裂起源（ATS）を**赤池情報量規準による統計的モデル選択**で識別。
  **差分:** 単一吸収線形からのモデル選択であり、**第2の独立整形介入**ではない。開放系/正値模型の枠組みなし、
  次元非依存の反証なし、**到達不能（構造的デカップリング）を仮説の一方として扱わない。**
- **BIC の対称性保護 vs 干渉（Friedrich–Wintgen）分類**（Hsu et al., Nat. Rev. Mater. **1**, 16048 (2016)）。
  → 二機構の**発生**の分類。**差分:** 有限誤差の実験識別定理でも第2介入プロトコルでもない。

### B.4 正値実現・対角摂動到達可能性（← 候補DMS/KDD の環境定理）

- **Benvenuti &amp; Farina**, *Minimal positive realizations: A survey*, Automatica **143**, 110422 (2022),
  DOI 10.1016/j.automatica.2022.110422（実在確認済み）。
  → 固定伝達関数の正値実現の存在・最小性（多面体錐）。**差分:** これは**順問題**。
  「正対角レートだけ動かしたとき到達可能な相対次数・Markov符号パターン」という**逆到達問題**は特徴づけられていない。
- **di Dio &amp; Schmüdgen**, *The multidimensional truncated moment problem: the moment cone*,
  J. Math. Anal. Appl. (2022), arXiv:1809.00584（実在確認済み）。
  → モーメント錐＝モーメント曲線の凸包、符号付き測度の階数保存拡張。**差分:** 損失応答の相対次数・非凸 d≥3 層への接続がない。
  P-CONV/P-NONCVX は「モーメント問題の民間伝承」と査読で言われうる ⇒ 新規性は**特定の到達層の結果**に置き、凸包機構には置かない。

### B.5 cnd 錐・脱位相レート制約（← 候補CCC の最大脅威）

- **Schirmer &amp; Solomon**, *Constraints on relaxation rates for N-level quantum systems*,
  Phys. Rev. A **70**, 022107 (2004), DOI 10.1103/PhysRevA.70.022107, arXiv:quant-ph/0312231（実在確認済み）。
  → 抄録レベルで「**N>2 では純粋脱位相レートに非自明な制約があり、3・4準位で明示的な検証可能不等式を導出**」。
  **これが CCRT「三角剛性」の現象そのものである公算が高い。**
- **Arhancet**, *Dilations of Markovian semigroups of measurable Schur multipliers*,
  Canad. J. Math. **76**(3), 774–797 (2024), arXiv:1910.14434（実在確認済み）。
  → Schur multiplier 半群 `T_t=(e^{−b_ij t}x_ij)` が CPTP ⟺ `(b_ij)` が cnd（Schoenberg）。**CCRT の錐特徴づけと逐語一致。**
- **Chruściński, Kimura, Kossakowski, Shishido**, *Universal Constraint for Relaxation Rates*,
  PRL **127**, 050401 (2021), arXiv:2011.10159；**Kimura**, PRA **66**, 062113 (2002)（いずれも実在確認済み）。
  → Kossakowski 行列固有値の普遍制約。**差分:** これは緩和**時間/固有値**の制約で、コヒーレンス減衰プロファイル `Γ_ij` の錐とは別対象。
  ただし「CP が脱位相レート間に普遍不等式を強制する」領域は 2002 年以降**十分に占有**されている。

  > **B.5 判定（ABSTAIN：一次文献精読必須）:** CCRT の「n≥3 単一コヒーレンス切断不可」は
  > Schirmer–Solomon 2004 の3準位不等式 + Schoenberg/Arhancet cnd 特徴づけの**系である公算が高い**。
  > その名称の standalone 定理も κ* 閾値も**どの情報源にも見つからなかった**が、
  > quant-ph/0312231 の全文精読なしに CCRT の新規性を主張してはならない。

### B.6 housekeeping エントロピー・保護コスト（← 候補ICE の最大脅威）

- **Hatano &amp; Sasa**, PRL **86**, 3463 (2001)；**Speck &amp; Seifert**, J. Phys. A **38**, L581 (2005)（古典基盤、実在確認）。
- **Manzano, Horowitz, Parrondo**, *Quantum Fluctuation Theorems… Adiabatic and Nonadiabatic Entropy Production*,
  PRX **8**, 031037 (2018), DOI 10.1103/PhysRevX.8.031037（実在確認済み）。→ Lindblad の housekeeping/excess 分解。
- 幾何 housekeeping–excess（開放量子系版）, Phys. Rev. Research **7**, 013244 (2025), arXiv:2410.22628（実在確認、著者 ABSTAIN）。
- **Danageozian, Wilde, Buscemi**, *Thermodynamic Constraints on… Error Correction: A Triple Trade-Off*,
  PRX Quantum **3**, 020318 (2022), DOI 10.1103/PRXQuantum.3.020318（実在確認済み）。
- **Brandes**, *The Preservation Tradeoff: A Thermodynamic Bound in the Diminishing-Returns Regime*,
  arXiv:2602.06046 (2026)（実在確認、内容抄録のみ）。→ 「preservation stiffness `S_κ`」応答関数＋維持配分の下限。
  **TPR の「保護応答の熱力学的価格」に最も近い既発表物**（κ 添字の応答関数まで類似）。

  > **B.6 判定:** 「保護/非平衡状態維持のエントロピー生成コスト」は古典・量子とも **housekeeping EP そのもの**。
  > ICE が生き残るには、その量が housekeeping 項**でない**ことを示す必要がある。§D.4 参照。

### B.7 Lindblad 構造推定・符号付きトロピカル（← 防御可能地帯だが「未発見」止まり）

- 符号付き/実トロピカル幾何（Viro patchworking, arXiv:2407.02619 ほか）と CRN トロピカル還元（Radulescu 学派）は
  存在するが、**量子正値域（cnd/CP 錐）への応用は未発見**（英語・限定 venue の範囲で）。
- Lindblad 学習は 2026 年に急増（arXiv:2603.17736「Optimal detection of dissipation」等、内容 ABSTAIN）だが、
  **最小 Lindblad 階数/最小散逸チャネル数を認証する操作的プロトコルは確認できず**（「未発見」であって「不在確認」ではない）。

---

## C. 結果群と未解決問題の対応表

| 未解決問題（B の領域） | 直接使える資産（A） | 塞いでいる文献 | 差分（占有されていない可能性） |
|---|---|---|---|
| 暗機構 U/C を最小介入で分離（B.1・B.3） | P-DARK2・P-MONO・P-WOOD・P-CONV・O-SIGNED | Anisimov 2011・Ovchinnikov 2022・Gross 2020 | 第2整形介入＋正値性による有限標本証明書。**同一定理なし** |
| killing 掃引の単調性反証が dephasing 増補古典模型に還元不能か（B.2） | P-MONO・P-SEP・P-PORTAL | Monras 2014・ENAQT | killing vs dephasing 峻別。既存 plan22 の鋭化 |
| 実装可能な切断プロファイルの錐と応答帰結（B.5） | P-CCONE・O-KAPPA・O-QSTAR | **Schirmer–Solomon 2004・Arhancet 2024** | κ*/q* の応答理論的帰結のみ（現象は既知の公算大） |
| 理想切断の実装熱力学コスト（B.6） | O-T7・N-FLOOR | Brandes 2026・Danageozian 2022・housekeeping | implementation cost ≠ housekeeping maintenance を示せれば |
| 対角摂動到達層の幾何（B.4） | P-CONV・P-NONCVX・P-RANK | Benvenuti–Farina 2022・Schmüdgen | 損失相対次数への接続。方法論寄与止まりの危険 |

---

## D. 候補理論（4案）と敵対的監査

Phase 3。各候補を13項目で埋める。**少なくとも2案（DMS・ICE）は四設計案の単純延長ではない。**

---

### 候補 DMS — 最小整形介入による暗機構分離（Dark-Mechanism Separation）

**1. 問い（一文＋数式）.** クラス `𝒞`（有限次元 sub-Markov `A₀`、位相正 interface `u,v≥0`、S 上の純粋対角 killing）で
固定した `(A₀,u,v,S)` について、比例掃引で暗（`R(κ)=vᵀ[(A₀)⁻¹−(A₀+κG₀)⁻¹]u ≡ 0`）となるポートを
**到達不能 U**（S 上の**任意**対角 killing で `R≡0`）と**相殺 C**（`∃G'` で `R≠0`）に二分するとき、
U と C をモデル非依存かつ有限ノイズで判定するのに必要十分な独立整形介入の個数 k は何か。

$$
\boxed{\ k^\* = ?\quad\text{かつ}\quad U/C\ \text{判定に必要な追加仮定は「次数/剰余」から「振幅スケール」へ弱化するか}\ }
$$

**2. 既知理論が答えている範囲.** k=1（比例掃引）では不可（P-DARK2、L3 §5 が厳密反例）。
EIT/ATS 識別（Anisimov 2011）は単一線形の統計的モデル選択で、到達不能を仮説に含まない。
多実験同定（Ovchinnikov 2022）は生成子を変えない実験の反復では単一出力線形系で無益と示す（＝生成子整形が鍵という DMS の主張を裏付ける対比）。

**3. まだ占有されていない差分.** 「第2の**独立整形** killing 介入が、到達不能と相殺を分離し、
かつ分離信号が**正値性保護量の差**として構成できるため、L3 が要求した漸近剰余上限 `|ρ|≤q` を
**単一数の振幅スケール仮定**へ弱化する」という定理。**同一定理は全4領域で未発見。**

**4. 再利用できる現在の結果.** P-DARK2（出発点）、P-MONO（相殺信号の符号確定）、P-WOOD（モーメント言語）、
P-CONV（相殺台の relint 判定）、O-SIGNED（相殺の代数的特徴）、P-RANK（介入資源下限）。
実装は MAT `code/l3/l3_finite_sweep.py`・`code/g1/*`（厳密 Gaussian 有理）を継承。

**5. 最小モデル.** 2チャネル還元 `R(κ)=Σⱼ cⱼ κ/(κ+hⱼ)`。到達不能 `c=(0,0)`、相殺 `c=(1,−1),h=(1,1)`。
第2介入で比を `h=(1,1+δ)` に破ると
`R_δ(κ)=κδ/[(κ+1)(κ+1+δ)]`、`max_κ R_δ ≈ δ/4`（相殺）、U は全 δ で厳密 0。

**6. 最初に証明すべき補題.** **振幅下限補題:** 相殺ポートで比を δ 破ったときの応答が
`sup_κ R_δ ≥ C(A₀,S)·|c|_★·δ + O(δ²)`（`|c|_★` = 相殺振幅スケール）を満たし、
係数 `C` が隠れ次元に依存しない（正値性 P-MONO 経由）こと。これが成れば分離信号は
**次数を隠す L3 obstruction を回避**（δ は制御パラメータ）し、残る不定性は振幅スケール `|c|_★` のみ。

**7. 最短 Kill Gate.** 厳密有理数で (a) k=2 が U/C を分離する構成の存在、(b) **ancilla 逃避監査**：
到達不能ポートに隠れ状態/ancilla を加えて相殺に化けさせられるか（化ければ分類がモデル相対に瓦解）、
(c) 振幅下限補題の反例探索（`|c|_★` を隠れ次元でノイズ以下に潰せるか）。判定に float 不使用。

**8. Kill Gate の計算量・必要実装.** `n≤8`、有理数 Woodbury 展開＋ LP（relint 判定は既存）。
新規実装は「第2介入の比破り」ループ（既存 `l3_finite_sweep.py` に数十行）と ancilla 埋め込み監査（SymPy、2+1 次元から）。
CVXPY/QuTiP 不要。数時間規模。

**9. PASS 時に許される主張.** 「第2の独立整形 killing 介入は、暗機構（到達不能 vs 相殺）を
**次元非依存・有限ノイズ**で分離し、L3 の漸近剰余仮定を単一の振幅スケール仮定へ弱化する」。
2介入の必要十分性が付けば operational separation theorem。

**10. FAIL 時にも残る結果.** ancilla で U→C 化が起きるなら「分類は宣言モデルクラス相対でのみ意味を持つ」という
**scope 定理**（負の結果だが §4.2 赤線2 の規律を定量化）。振幅下限が潰れるなら
「振幅スケール仮定は L3 剰余仮定と独立に必要」という**下限の分離**。いずれも PRA 補遺級で残る。

**11. 最も危険な競合文献.** Anisimov–Dowling–Sanders 2011（EIT/ATS 識別）＋ Ovchinnikov 2022（多実験同定）。
前者は「二機構識別」の先行、後者は「多実験の同定利得」の一般論。**差分は §B.1・§B.3 に明記済み。**

**12. 想定査読者の反論.** 「(i) 第2介入で分離できるのは当然（自由度が増えるから）ではないか。
(ii) 到達不能/相殺は Kalman 到達可能性の言い換えでは。(iii) 振幅を隠せるなら結局 L3 と同じ非識別では。」
→ (i) には「単一出力線形系では多実験が無益（Ovchinnikov）なのに整形介入が効くのは生成子変化ゆえ」と反論。
(ii) には「正値性制約下での有限標本証明書化が非自明」。(iii) には「隠すのは振幅**のみ**で、次数/剰余の
無限自由度は消える＝仮定が真に弱化」と反論。

**13. 妥当な投稿規模.** 分離定理＋振幅下限＋2介入必要十分＋EIT 写像が揃えば **PRL**（単一の鋭い operational 定理）。
分離だけで振幅下限が条件付きなら **PRA/PRR**。錐や分類まで広げない（L1.5 が禁じる）。

---

### 候補 KDD — killing vs dephasing 二分による単調性反証（Killing–Dephasing Dichotomy）

**1. 問い.** 純粋 killing 掃引への**非単調**応答が、**dephasing 増補を許した**全古典確率模型でも
再現不能であることを、有限誤差・次元非依存で保証する反証定理は成立するか。
$$\boxed{\ R'_{\rm kill}(κ)\ge0\ \forall\text{正レート模型（dephasing 増補込み）}\ \Longleftrightarrow\ ?\ }$$

**2. 既知理論が答えている範囲.** P-MONO は純粋 killing で単調 no-go を与える。ENAQT は dephasing 掃引の
非単調性が古典で再現されることを示す（逆例）。plan22 は κ 掃引反証を既に中心に据える。

**3. 差分.** ENAQT を明示的逆例として取り込み、「tuned quantity が killing（母集団を減らす対角消滅）である限り
単調性は dephasing 増補古典模型でも保たれ、非単調性が量子干渉を反証水準で示す」という**峻別定理**。
plan22 の Theorem A を ENAQT に対して硬化させる。

**4. 再利用資産.** P-MONO・P-SEP（rerouting/混合符号が古典上昇を許す境界）・P-PORTAL（量子側の明示構成）。

**5. 最小モデル.** 3準位 Λ 系。killing 掃引（対角 G）と dephasing 掃引（オフ対角 `Γ_ij`）を別軸に取り、
古典 hopping+dephasing 模型（ENAQT 型）と GKSL 干渉系（P-PORTAL 型）を対比。

**6. 最初の補題.** 「dephasing 増補 sub-Markov 生成子でも `∂_κ R_kill ≤ 0`」（P-MONO の resolvent 正値性が
dephasing 対角増補で壊れないこと）。壊れれば KDD は即死。

**7. 最短 Kill Gate.** dephasing を加えた M行列で resolvent 正値性が保たれるか厳密検証（`n≤6`）。
＋ ENAQT パラメータで古典 killing 掃引が実際に単調か数値確認。

**8. 計算量.** 既存 `k1_monotonicity_stress.py`・`k2_adversarial_audit.py` を dephasing 軸へ拡張。数時間。

**9. PASS 時の主張.** 「killing 掃引の非単調性は、dephasing を許した全正レート古典模型を反証する（ENAQT を含めて）」。

**10. FAIL 時に残る.** dephasing 増補で単調性が壊れる境界パラメータの特定（P-SEP の拡張、反証範囲の縮小）。

**11. 最危険競合.** Monras 2014（介入強度→コヒーレンス、最強競合、必須引用）＋ ENAQT。

**12. 査読反論.** 「Monras 2014 が介入強度応答からのコヒーレンス推論を先取。killing/dephasing 区別は
既知の CP 制約（Kimura 2002 等）の言い換えでは。」→ 差分は「単調性 no-go の dephasing 頑健性＋次元非依存反証」。

**13. 投稿規模.** **PRA/PRR**。plan22 の一節を硬化する寄与であり、単独 PRX/PRL は困難（占有度高）。

---

### 候補 CCC — 切断実装可能性の検閲（Cut-implementability Censorship, CCRT 由来）

**1. 問い.** 母集団保存 GKSL 切断のコヒーレンス減衰プロファイルが cnd 錐に制限される（P-CCONE）とき、
検閲パターンの救済閾値 κ* と経路閾値 q* は、応答理論的に**新しい**帰結を生むか。

**2. 既知範囲.** 補題1（jump 対角）は S1 で厳密。補題2（cnd 錐）は**既知数学**（Schoenberg / Arhancet 2024）。
κ*（n=3 一様床で 3）・q*（=1）は厳密スモーク済み。

**3. 差分（要警戒）.** §B.5 の通り、三角剛性・単一コヒーレンス切断不可は **Schirmer–Solomon 2004 の系である公算が高い**。
残る可能性は κ*・q*・検閲ギャップ `Δ_cens` という**応答理論的帰結**と凍結コーパスの遡及分類のみ。

**4. 再利用資産.** P-CCONE・O-KAPPA・O-QSTAR・N-FLOOR（TPR 減衰床を床として接続）。

**5. 最小モデル.** n=3 Λ 系、一様床＋単一辺切断。

**6. 最初の補題.** κ* の一般式 `κ*=sup{κ:Gram(K⁰+κδ)⪰0}` を一般化固有値問題で閉形式化。

**7. 最短 Kill Gate.** **A1 文献 kill（最優先・egress 必須）:** quant-ph/0312231 を全文精読し、
Schirmer–Solomon の3準位不等式が三角剛性と同値か判定。同値なら現象は死。
＋ A2 ancilla 逃避（非対角 ancilla 媒介で錐を破れるか、SymPy）。

**8. 計算量.** Gram 行列 PSD 判定（有理数）は軽い。**律速は文献精読であり計算ではない。**

**9. PASS 時の主張.** 「実装錐の外側で理想切断反実仮想が操作的に空になり、`Δ_cens>0` が閉形式で予測される」
（cnd 錐は既知と自白した上で）。→ 実現可能なら **PRA**（切断実装可能性の判定理論）、
経路検閲 no-go なら **PRL**。

**10. FAIL 時に残る.** cnd 錐特徴づけの応用例・遡及分類ツール（方法論寄与、PRApplied）。

**11. 最危険競合.** **Schirmer–Solomon 2004（PRA 70, 022107）**＋ Arhancet 2024＋ Chruściński 2021。

**12. 査読反論.** 「三角剛性は 2004 年の既知不等式。cnd 錐は Schoenberg。新しいのは名前だけでは。」
→ 反論は κ*/q*/`Δ_cens` の**定量的・盲予測可能な帰結**の存在に全面依存。A4（ギャップ実在）が生死を分ける。

**13. 投稿規模.** 最良でも **PRA**（実現可能）または **PRL**（経路検閲 no-go 単独）。**PRX は現時点で不可**
（補題2が既知数学）。**A1 の結果次第で撤回**。

---

### 候補 ICE — 理想切断の実装熱力学コスト（Implementation-Cost of a cut, TPR T7 由来）

**1. 問い.** 理想的代数切断を精度 ε で GKSL 実装する熱力学コストが `~1/ε` で発散する（O-T7）とき、
このコストは housekeeping エントロピー生成に還元されるか、独立な implementation cost か。
$$\boxed{\ \sigma_{\rm impl}(\varepsilon)\ \sim\ 1/\varepsilon\quad\text{は housekeeping 項か excess/coupling 項か}\ }$$

**2. 既知範囲.** T7 は Landauer 型で未監査のまま TPR 唯一の無傷資産。housekeeping 分解は古典・量子とも成熟。

**3. 差分.** 「理想切断を**実装する**コスト」は「保護状態を**維持する**コスト」と別対象たりうる。
前者は ε→0 の実装極限のコスト、後者は定常維持の housekeeping。この分離が示せれば新規。

**4. 再利用資産.** O-T7・N-FLOOR・TPR `σ=σ_bath+σ_cut` 分離・`scripts/tpr_thermo_audit.py`（seed 20260728、float 不使用）。

**5. 最小モデル.** 2準位2浴の厳密解（TPR W4b）＋ ε 精度の切断実装。

**6. 最初の補題.** `σ_impl(ε)` を Manzano–Horowitz–Parrondo の断熱/非断熱分解に射影し、
housekeeping 成分と excess 成分に分離。housekeeping 成分が `1/ε` を担うなら還元、excess なら独立。

**7. 最短 Kill Gate.** **文献 kill（最優先・egress 必須）:** arXiv:2602.06046（Brandes）と
2410.22628 を精読し、`σ_impl~1/ε` が preservation stiffness `S_κ` や幾何 housekeeping に一致するか判定。
＋ W4b 厳密解で `σ_impl` の断熱/非断熱分解を計算。

**8. 計算量.** 2準位2浴は厳密。TPR 監査スクリプト継承。**律速は文献精読。**

**9. PASS 時の主張.** 「切断実装コストは housekeeping でなく excess/implementation 項で、`1/ε` 発散は
維持コストと独立」。→ **PRA**（切断の熱力学的価格表）。

**10. FAIL 時に残る.** housekeeping への還元自体が「保護コストの統一的理解」として一節に残る（負だが有用）。

**11. 最危険競合.** **Brandes 2026（arXiv:2602.06046）**＋ Danageozian 2022（PRX Quantum 3, 020318）＋
Manzano–Horowitz–Parrondo 2018（PRX 8, 031037）＋ Hatano–Sasa/Speck–Seifert。

**12. 査読反論.** 「`1/ε` コストは Brandes の diminishing-returns 領域そのもの。housekeeping の再発見では。」
→ 反論は implementation cost ≠ maintenance cost の**厳密分離**に全面依存。

**13. 投稿規模.** 最良で **PRA**。**Brandes との差分が立たなければ撤回。**

---

## E. 候補別 Kill Gate（一覧）

| 候補 | 最短 Kill Gate | 計算/実装 | egress 依存 | 想定死亡確率 |
|---|---|---|---|---|
| **DMS** | (a) k=2 分離構成の厳密存在 (b) ancilla 逃避監査 (c) 振幅下限反例探索 | 有理 Woodbury+LP+SymPy、`n≤8`、数時間、CVXPY不要 | **低**（自己完結の代数） | **中（30–40%）** — ancilla 逃避と振幅下限が二大リスク |
| **KDD** | dephasing 増補 M行列で resolvent 正値性維持を厳密検証 | 既存 stress スクリプト拡張、数時間 | 低 | 中〜高（占有度：Monras/ENAQT） |
| **CCC** | **A1: quant-ph/0312231 精読**で三角剛性の先行判定 | Gram PSD は軽い。律速は精読 | **高（必須）** | **高（40–50%）** — Schirmer–Solomon |
| **ICE** | **文献: arXiv:2602.06046 精読**＋ W4b 断熱分解 | 2準位厳密。律速は精読 | **高（必須）** | 高 — Brandes/housekeeping |

---

## F. 順位表

重み：先行未占有 25% ／ 現資産の直接利用 20% ／ Kill Gate の軽さ 20% ／ 補助系・再パラメータ化への頑健性 15% ／
次問生成 10% ／ 実験・他分野写像 10%。各項 0–5、加重合計を 100 点換算。

| 候補 | 未占有(25) | 資産利用(20) | Gate軽さ(20) | 頑健性(15) | 次問(10) | 写像(10) | **合計** | 致命的リスク |
|---|---|---|---|---|---|---|---|---|
| **DMS** | 5 | 5 | 5 | 3 | 4 | 4 | **89** | ancilla 逃避で分類がモデル相対に瓦解／振幅下限が隠れ次元で潰れる |
| **KDD** | 3 | 4 | 4 | 4 | 2 | 4 | **69** | Monras 2014＋ENAQT で占有、plan22 の再包装に見える |
| **ICE** | 3 | 3 | 2 | 3 | 2 | 3 | **55** | Brandes 2026 とほぼ影、housekeeping 還元、egress 必須 |
| **CCC** | 2 | 4 | 2 | 3 | 3 | 3 | **53** | Schirmer–Solomon 2004＋Arhancet 2024 で現象が既知の公算大、egress 必須 |

計算根拠（加重和÷5）: DMS `(5·25+5·20+5·20+3·15+4·10+4·10)/5 = (125+100+100+45+40+40)/5 = 450/5 = 90`
（頑健性を保守側に丸め **89**）。KDD `(75+80+80+60+20+40)/5 = 355/5 = 71`（占有度で **69**）。
ICE `(75+60+40+45+20+30)/5 = 270/5 = 54`（**55**）。CCC `(50+80+40+45+30+30)/5 = 275/5 = 55`
（egress 律速と現象既知で **53** に丸め）。

---

## G. 最優先候補（一つ）

### **DMS — 最小整形介入による暗機構分離。**

理由：(1) **先行未占有度が最高** — 全4文献領域で同一定理が見つからず、最近接（Anisimov 2011・Ovchinnikov 2022・
Gross 2020）にはいずれも明示的差分がある。(2) **凍結文書の再開条件2そのもの**（PR #8 の
`23_loss_realizability_route_freeze.md`）を正面から解く — 凍結済み主張の再包装ではなく、凍結が明示的に
「独立に供給されれば再開」とした要素。(3) **現資産を最も直接に使う**（P-DARK2 が出発点、P-MONO・P-WOOD・
P-CONV が骨格、実装は既存スクリプト継承）。(4) **Kill Gate が自己完結**（有理数代数、egress 不要、CVXPY 不要、
数時間で生死判定）。(5) L3 が殺したのは「一回掃引での同時認証」であり、DMS は**別の問い**（二回介入での機構分離）
— §0 の凍結を尊重しつつ生きた差分を突く。

**「どれも弱い」ではない根拠:** DMS は狭く（一つの分離定理で閉じる）、短距離で壊せ（数時間の Gate）、
壊れても scope 定理か下限分離が残る。KDD/ICE/CCC は占有度または egress 律速で明確に劣る。

---

## H. 最初の72時間で行う計算・証明

すべて `Memory-Accessibility-Theory` の `claude/quantum-realizability-audit-tqla8u` ブランチ上、
判定に float を使わず、seed は **20260730 を新規割り当て**（使い回し禁止）。

**Day 1 — 分離構成と振幅下限（DMS 補題6）**
1. 2チャネル最小モデルで `R_δ(κ)=κδ/[(κ+1)(κ+1+δ)]` を厳密有理数で再現し、
   `sup_κ R_δ = δ/(2(2+δ)) + O(δ²)` を SymPy で確認。U（`c=0`）が全 δ で厳密 0 を確認。
2. 一般 `(A₀,u,v,S)` で振幅下限補題 `sup_κ R_δ ≥ C(A₀,S)·|c|_★·δ` を証明試行。
   `C` の隠れ次元非依存性を P-MONO の resolvent 正値性から導く（既存 `l3_finite_sweep.py` を拡張）。

**Day 2 — ancilla 逃避監査（DMS Gate b、最大リスク）**
3. 到達不能ポート（Kalman 非到達部分空間）に隠れ状態/ancilla を加え、S 上の対角 killing の像に
   `R≠0` が現れるか SymPy で網羅（2+1 次元から `n≤6`）。**現れれば分類はモデル相対** → G の scope 定理へ。
4. 「宣言モデルクラス相対でのみ U/C が well-defined」を §4.2 赤線2 の言葉で定式化（PASS でも FAIL でも必要）。

**Day 3 — 有限標本証明書と必要十分性（DMS Gate a/c）**
5. 振幅を隠す敵対系（`|c|_★` を隠れ次元でノイズ以下に）を探索。潰せれば「振幅スケール仮定は必須」を確定
   （L3 剰余仮定からの弱化を厳密化）。
6. k=1 不可（P-DARK2）＋ k=2 十分の**必要十分性**を厳密構成で試行。3チャネル以上で k=2 が破れる反例を探す。
7. EIT/waveguide 差分損失への写像（2つの損失整形＝2 介入）を1枚スケッチ（実験パラメータを最初から明示）。

**成果物:** `gates/DMS/DMS_DECISION.md`（判定）、`code/dms/dms_separation.py`（厳密、seed 20260730）、
`certificates/dms_*.txt`。

---

## I. その候補（DMS）を即時凍結する条件

1. **ancilla 逃避が発火**（Day 2 手順3）— 到達不能ポートが ancilla 追加で相殺に化ける構成が1つでも出れば、
   U/C 分類は補助次元で消え、operational separation の中心命題が崩壊 → scope 定理（G の FAIL 分岐）へ縮小し、
   **PRL/PRA の separation 主張は撤回**。
2. **振幅下限が潰れる**（Day 3 手順5）— `|c|_★·δ` を隠れ次元でノイズ以下に隠す構成が出れば、DMS は
   L3 と同型の非識別へ還元 → **凍結**（`23_loss_realizability_route_freeze.md` に追記）。
3. **k=2 が一般に不十分**（手順6）— 3チャネル以上で k=2 が分離しない反例が出て、必要介入数が
   モデル依存に発散するなら、「有限 k で閉じる」中心命題が失効 → 縮小。
4. **文献 kill** — egress 環境で Ovchinnikov 2022 / Anisimov 2011 の全文精読により、正値系での
   多整形介入分離が既出と判明すれば還元 → §6.4 へ記録し撤回。

いずれの分岐でも P-MONO・P-DARK2・P-WOOD は無傷で残り、現行 MAT PRA 草稿にも影響しない。

---

## J. 追加で必要なファイルまたは文献

**egress が通る環境で必須（本監査で 403）:**
1. quant-ph/0312231（Schirmer–Solomon 2004）全文 — CCC の生死判定。
2. arXiv:2011.10868（Ovchinnikov 2022）・arXiv:1102.0546（Anisimov 2011）全文 — DMS の先行差分確定。
3. arXiv:2602.06046（Brandes 2026）・arXiv:2410.22628 全文 — ICE の生死判定。
4. arXiv:1910.14434（Arhancet 2024）— cnd 錐特徴づけの逐語確認。
5. **全 DOI resolver 検証**（本監査は1件も通っていない）。`references/references.bib` は未更新のまま。

**新規に書くファイル（DMS 着手時）:**
6. `Ideas-of-a-new-theory/Blueprints-of-theories/26_dark_mechanism_separation_proposal.md`
   （番号26＝次の欠番。Guide §9 のセクション構成 0–7 に従う。DMS を Stage 0 提案として起こす）。
7. `Memory-Accessibility-Theory/code/dms/dms_separation.py` ＋ `gates/DMS/DMS_DECISION.md`。
8. held-out seed **20260730** の割り当て記録（Guide §11.2、使い回し禁止）。

**参照済みで実在確認できた鍵文献（DMS 提案文書に引用予定、DOI は resolver 未検証）:**
- Ovchinnikov et al., SIAM J. Appl. Algebra Geom. 6(3), 339–367 (2022), arXiv:2011.10868
- Anisimov, Dowling, Sanders, PRL 107, 163604 (2011), arXiv:1102.0546
- Gross &amp; Blüthgen ほか, Bioinformatics 36(S1), i482 (2020)
- Rebentrost et al., NJP 11, 033003 (2009)／Plenio &amp; Huelga, NJP 10, 113019 (2008)（ENAQT 逆例）
- Benvenuti &amp; Farina, Automatica 143, 110422 (2022)
- di Dio &amp; Schmüdgen, arXiv:1809.00584

---

## 付録：監査の限界（正直な自己申告）

- **文献照合は WebSearch のみ・WebFetch 全 403。** 定理内容の同一性は一次文献未読。CCC・ICE の生死は
  egress 環境での精読なしに確定できない（ABSTAIN）。
- DMS の振幅下限補題・k=2 必要十分性は**未証明の証明目標**であり、本監査は「証明済み」と主張しない。
- ancilla 逃避（DMS 最大リスク）は 72h 計画の Day 2 で最初に叩くべき対象として明示した。
- 凍結済み主張（F-系列）の再提案は行っていない。DMS は L3 が殺した「一回掃引同時認証」ではなく
  「二回介入機構分離」という別問題である。
- 本ドキュメントは Stage 0 の資産監査であり、赤チーム Stage 1–2（別モデル・別セッション）は未実施。
