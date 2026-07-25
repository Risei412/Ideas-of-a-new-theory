# 入れ子容量崖理論（Nested Capacity Cliff Theory / NCCT）
## 一行サマリ

深さ≤2のcalibration応答では6状態以下の古典HMMと厳密一致するのに、深さ≤4のfull応答では
いかなる6次元以下の古典・線形実現も凍結shot予算内で棄却される——そのような
「入れ子になった容量崖」を持つGKSL介入interfaceが存在し、その存在領域が
cancellation-protectedな例外集合として安定であることを主張する理論。

**作成日:** 2026-07-25
**位置づけ:** ガイド §6.1 P0「Resource-bounded mechanism separation」。壊す仮定は
unrestricted representation criterion の1つ。`docs/p0-certificate-spec.md` のステップ3–4を
理論命題として定式化した Stage 0 草稿（未推敲）。
**判定:** P0-D 単独達成なら **PRL型**（「次数6以下の古典・線形実現は存在しない」という狭い主張）。
族A・Eへの入れ子証明書拡張が成立した場合のみPRX型へ昇格を検討する。
**P0-D の達成は P0 全体の達成ではない**（spec §5 の呼称規約を遵守する）。

**理論の型（ガイド§2）:** (B) 数学的定理型（有限資源分離定理・no-go）＋(A)の要素
（有限shotで観測可能なwitness）。対象系は有限次元・time-local GKSL の介入応答interface。
想定読者は量子情報・確率過程・システム同定。

---

## 0. 結論

**中心の問い:** 同一の観測interfaceに対して、「そのデータを生成できる機構のクラス」を
無制限に許すと（unrestricted representation criterion）、あらゆる候補が
process tensor や十分大きな hidden ancilla に吸収され、機構の分離は原理的に不可能になる。
では、**表現力に凍結予算を課したとき、量子機構と古典機構が有限shotで分離される
interfaceは存在するか。その存在領域はどんな構造を持つか。**

> **【boxed命題：入れ子容量崖 / Nested Capacity Cliff】**
>
> 介入alphabet 𝒲（|𝒲| = m = 6）、深さ ℓ ≤ 4、opnorm正規化（縮小写像規約）の
> 応答interfaceのクラスにおいて、次を同時に満たす組 (M_*, M_D) が存在する：
>
> 1. **生成側:** M_* は系次元 d = 3 の GKSL 介入模型（letter ごとの応答写像
>    E_w は縮小写像、応答は R(w) = p† E_{w_ℓ}···E_{w_1} c の形）。
> 2. **calibration側（存在証明）:** M_D は状態数 D_cl ≤ 6 の古典HMM
>    （非負・正規化を満たす明示構成）で、深さ ≤ 2 の全calibration語 w ∈ W_cal に対し
>    P_{M_D}(w) = R_{M_*}(w) が**厳密に**成立する。
> 3. **full側（容量超過）:** 深さ ≤ 4 の語集合 W_cal ∪ W_ho 上のHankel行列
>    H_{full} が σ₇(H_{full}) ≥ 2τ_H = 0.2933（2000 shots/setting、settings ≤ 2）を満たし、
>    有意水準 α で rank(H_{full}) ≥ 7 が認証される。
>    したがって**凍結資源（D_cl ≤ 6、P ≤ 256、shot予算表）内のいかなる古典HMM・
>    いかなる6次元以下の線形実現（quasi-HMM／weighted automaton を含む）も
>    full データに適合しない。**
> 4. **例外集合の保護（理論固有部分）:** 条件2は一般のHMM同定定理（generic
>    identifiability）が適用されない**正余次元の代数的例外集合**上でのみ成立し、
>    NCCTはこの集合の余次元・接空間・摂動安定性（集合内摂動でσ₇の下界が保持される
>    margin）を与える。
>
> witness は単一chartのHankel特異値であり、**relative-chart対象 G_ij = X_j X_i^{-1}
> をそもそも定義しない**（過去の却下候補6件の共通死因を構造的に回避する）。

**最小次元条件（NCCTの自明でない帰結の一つ）:** 生成側の量子次元は d = 3 が最小である。
d = 2 では reachable-observable space の次元が高々 d² = 4 のため rank(H) ≤ 4 となり、
rank 7 の witness は原理的に構成できない（族G Krylov gate で即死する）。
逆に d = 3 は線形次元 9 を持ち、rank 7 ≤ 9 と整合する。
すなわち分離は「**qutrit 1個（3準位） vs 古典7状態以上**」という形で最も鋭く現れる。
線形次元では 9 vs 7 であり量子が有利なわけではないことを隠さない——
分離は状態数（メモリの物理単位）の勘定においてのみ生じる。

---

## 1. なぜこの方向を選ぶのか

### 1.1 既存理論から引き継ぐ事実（ガイド§4）

- **SMRT / RISEI の応答形式:** 応答interfaceは R(w) = p† E_{w_ℓ}···E_{w_1} c の
  有限次元rational transfer構造を持つ（SMRTのexperiment specification
  𝔈 と同形。`scripts/sigma7_smoke.py` で採用済みの形）。介入letterは
  𝒢_S^{RISEI} 型の sector選択的 GKSL-admissible 生成子の有限時間propagatorとして実装する。
- **比較規約の固定（赤線2）:** 初期状態 c、readout p†、観測窓、正規化は
  全protocol・全競合模型で固定する。
- **正規化:** opnorm（縮小写像）正規化を採用（spec §4ter で決定済み。|R(w)| ≤ 1 保証）。
- **shot予算（spec §4.5 凍結値）:** calibration 1.2×10⁵ 上限（m=6 で 92,000）、
  held-out（depth-4全64 protocol）独立予算 1.28×10⁵、shots/setting は 1000–2000 の
  二段階配分、settings ≤ 2。
- **σ₇ 到達可能性（spec §4ter, GO判定）:** 理想データで射影付き山登り120反復により
  σ₇ = 0.609 に到達済み。要求 2τ_H = 0.2933 に対し2倍超の余裕がある。
  ただし入れ子条件（det H_cal = 0 の弱い形）でランダム構成の中央値は 0.162 であり、
  **最適化構成が必須**。

### 1.2 壊す仮定 ← 新規性の源泉

**外す仮定（1つ）:** unrestricted representation criterion。
「どんな隠れ自由度・ancilla・process tensorを使ってもデータを説明できれば同値」
という判定基準を捨て、**競合機構クラスに凍結予算（D_cl ≤ 6、P ≤ 256、shot上限）を
課した上での適合可能性**を分離の判定基準にする。

**維持する仮定（明示）:** 有限次元・time-local GKSL、weak-probe線形応答形式、
固定比較クラス（赤線2）、opnorm正規化、有限depth・有限shot。
非Markov・無限次元・強probe・many-bodyへは踏み込まない（§4.3遵守、予算1つで完結）。

**代替する数学的構造:** 各競合族の null identity（族D: rank(H) ≤ D_cl）を先に固定し、
それを破るwitnessを逆設計する。これはガイド§6.4末尾の転換方針
（競合理論のnull identityを先に固定 → 逆設計）に従う**最初の提案**である。

**失効する既存定理:** なし（凍結理論の定理はどれも表現コストを主張していない）。
**継承する既存定理:** SMRTのrational transfer構造・Krylov moment機構、
RISEIの介入protocol形式。
**元の理論を回収する極限:** 予算 D_cl → ∞ で標準的realization theory
（rank(H) = 最小線形実現次元）に一致し、分離は消える（§3.1-5参照）。
**control（仮定変更がなければ現象が消えること）:** unrestricted criterionの下では
族E（process tensor, χ ≤ 36 ですら）が本interfaceを表現できるため分離は定義されない。
分離現象は予算を課して初めて出現する。

---

## 2. 理論の定式化

### 2.1 定義

- **介入interface:** 𝔍 = (𝒲, ℓ_max, c, p†, 正規化規約, shot予算表)。
  𝒲 は m = 6 個の介入letterの集合。語 w = w_1…w_ℓ、ℓ ≤ ℓ_max = 4。
  応答 R(w) ∈ [−1, 1]（opnorm規約下）。
- **letter応答写像:** E_w（‖E_w‖₂ ≤ 1）。生成模型 M_* では E_w は d = 3 の
  GKSL介入generatorの有限時間propagatorをvectorization（9次元Liouville空間）した
  上でreadout関連部分空間へ制限したもの。
  （記号注意：ガイド§5.3 の衝突リストにある Ω/K/Q/Ξ/ν/C/M/P/A/G/S/z/q は
  本提案では無修飾で使わない。Hankel は H、特異値は σ_i、閾値は τ_H、
  古典次元は D_cl、hidden次元は D_hidden と書く。）
- **Hankel行列:** H[u, v] = R(u·v)、prefix/suffix 長 ≤ 2（depth ≤ 4 語）で 43×43。
  H_cal はその depth ≤ 2 部分（7×7、prefix/suffix長 ≤ 1）。
  **prefix–suffix閉包に注意**（spec §1 警告）：行・列集合は語の連接構造を保つよう取る。
- **族Dのnull identity（既知定理・新規性に数えない）:** 状態数 D_cl の古典HMM
  （および任意の D_cl 次元線形実現）に対し rank(H) ≤ D_cl。
- **入れ子証明書（spec §1 の厳密形）:**
  ```
  ∃ M_D,  D_cl ≤ 6 :  P_{M_D}(w) = R_{M_*}(w)  ∀w ∈ W_cal   （深さ ≤ 2）
                       rank(H_{W_cal ∪ W_ho}) ≥ 7             （exact 認証）
                       σ₇(H) ≥ 2τ_H                            （ノイズ頑健 margin）
  ```
- **分離深さ（新概念・英日併記）:** separation depth / 分離深さ
  d_sep(M_*, 予算b) = min{ℓ : 深さ ≤ ℓ の制限データが予算bの競合族を margin τ で棄却}。
  本提案の主張は d_sep(M_*, 族D予算) ∈ {3, 4} かつ深さ2では厳密一致、である。
- **分離profile（新概念）:** separation profile / 分離プロファイル
  vec_sep = (d_sep^{(D)}, d_sep^{(A)}, d_sep^{(E)}, d_sep^{(DQ)}, d_sep^{(C)})。
  P0はこのベクトルの判定であり、本提案が主張するのは第1成分のみ（spec §0 遵守）。

### 2.2 主張（logical status 付き）

- **T1（存在・構成的）[Conjecture → 数値構成で Numerical へ昇格予定]:**
  §0 boxed命題の組 (M_*, M_D) が存在する。証明は明示構成による
  （§5 の検証計画ステップ3–4）。
- **T2（margin）[Conditional]:** T1の構成は σ₇ ≥ 2τ_H = 0.2933 を満たし、
  Weyl不等式 σ₇(H+ΔH) ≥ σ₇(H) − ‖ΔH‖₂ により、‖ΔH‖₂ ≤ τ_H なる観測ノイズ下でも
  rank ≥ 7 の判定が有意水準 α で保持される。
  （τ_H = 0.1466 は二項上界 σ_entry ≤ 1/(2√n)、N = 43、n = 2000 による。spec §4ter）
- **T3（例外集合の構造）[Conjecture]:** 深さ ≤ 2 厳密一致の制約は、生成模型の
  parameter空間内で余次元 ≦ 43 − dim(gauge軌道) の代数的部分多様体を定める。
  この集合上で σ₇ は連続であり、T1の構成点の近傍（集合内）で σ₇ ≥ 2τ_H が
  開条件として保持される。したがって現象は fine-tuning の一点ではなく
  **正の次元を持つ安定な例外集合**上で生じる。
  （余次元の正確な勘定は gauge 自由度（相似変換で E_w を同時共役しても R(w) 不変）の
  次元を引く必要がある。ここは未計算。Stage 4 で確定する。）
- **T4（最小次元）[Exact・証明は3行]:** rank(H_{M_*}) ≤ d² より、rank 7 の witness には
  d ≥ 3 が必要。d = 3 で十分か（rank 7〜9 が実現するか）は T1 の構成に含まれる。
- **T5（既知理論との整合・回収極限）[Exact・既知]:** D_cl ≥ rank(H) を許せば
  古典実現は常に存在（quasi-realizationなら即時、正値HMM実現は positive realization
  problem の解を要する）。予算 → ∞ で分離は消滅し標準realization theoryへ還元される。

---

## 3. 理論固有現象（ガイド§3 必須5項目）

### 3.1-1 固有現象の定義

§0 の boxed 命題（入れ子容量崖）。特に固有なのは条件4：
**「cancellation-protected な例外集合上の、凍結資源内 lower bound」**という構造。
generic HMM identifiability（一般位置の有限HMMは有限長word確率から復元可能：
Huang et al. 2016）が**適用されない集合を意図的に構成し、その集合の構造自体
（余次元・安定性・margin landscape）を理論の対象にする**。
ガイド§6.1 の2026-07-25制約が要求する形と一致させている。

### 3.1-2 非還元性の証明または論拠

§4 で詳述。要点のみ：witnessが単一chartの容量下界であり、
比較・相対化・gauge・quotientのいずれの構造も持たないため、
過去6候補を殺した pairwise relative-chart 因子化への還元経路が**定義できない**。

### 3.1-3 観測可能量（observable signature）

- **物理量:** 深さ ≤ 4 の介入語応答から組んだ 43×43 Hankel行列の第7特異値 σ₇。
- **現れ方:** 閾値型。σ₇ > τ_H(α) なら rank ≥ 7 が有意水準 α で成立。
  深さを 2 → 4 に上げたときに**適合可能性がLP feasibleからinfeasibleへ不連続に転移**
  する（容量崖）。
- **検出手段とコスト:** 数値計算＋（将来）実験。calibration 92,000 shots（m=6）＋
  depth-4 held-out 128,000 shots。settings ≤ 2。凍結予算内に収まる（spec §4.5）。
- **有限サイズ・有限精度:** T2 のWeyl margin により2000 shots/settingで判定可能。
  ランダム構成では届かない（合格率6.8%）ため、**最適化構成された模型でのみ**
  有限shotで見える——これも現象の一部（例外集合上でのみ生じる）として明示する。

### 3.1-4 反証条件

以下のいずれかが成立したら中心命題を撤回する：

1. 凍結予算内の古典HMM（D_cl ≤ 6, P ≤ 256）が、事前登録された選択手続きの下で
   full データ（held-out含む）を許容誤差内で再現する（族D kill test）。
2. 事前登録した最適化予算（§5）を使い切っても、入れ子条件（深さ≤2厳密一致）と
   σ₇ ≥ 2τ_H を同時に満たす構成が得られない。
3. T3 の例外集合が空、または構成点が孤立点（集合内摂動で即座に σ₇ < 2τ_H）と判明する。
4. 生成側 d = 3 GKSL 模型の reachable-observable 次元が実は ≤ 6 に縮約される
   （族G Krylov gate で発見された場合）。

### 3.1-5 既存理論との一致領域（sanity check）

- 予算 D_cl → ∞：標準realization theoryに一致（T5）。
- 深さ ≤ 2 制限：構成により古典模型と厳密一致（分離ゼロ）。
- shots → ∞：σ₇ 判定は exact rank 認証（SymPy minor）に収束する。
- r = 6 の生成模型：σ₇ ≈ 10⁻¹⁵（数値的rank 6）を smoke で確認済み——
  null model が正しく null を返す。

---

## 4. 非還元性の検討

reduction-targets.md の族A–Iに沿って個別に検討する。

### 4.1 族D（controlled HMM / 線形実現）——排除対象そのもの

本提案は族Dを**その族自身のnull identity（rank(H) ≤ D_cl）で**排除する。
rank ≥ 7 は正値HMMだけでなく**任意の6次元線形実現（quasi-HMM・weighted automaton）**
を同時に排除する点で、正値性に依存しない強い形。
残る注意：cancellation-protected 集合は generic identifiability 定理の適用外であることが
設計の前提なので、「genericには同定可能」という文献は本提案への反証にならない
（逆に、例外集合の存在自体は同文献の仮定の裏側として整合的）。

### 4.2 族A（hidden ancilla GKSL）——排除しない（明示的に主張外）

生成模型 M_* 自身が d = 3 の GKSL であり族Aに属する。したがって
**「hidden ancillaでは説明できない」という主張はしない**（監査の「維持できない表現」
リスト遵守）。主張は「次数6以下の**古典・線形**実現は存在しない」に限定する。
族Aの入れ子証明書（dim K_full > 144 等）は将来の拡張（PRX昇格条件）であり本稿の範囲外。

### 4.3 族B（tilted-GKSL / FCS）——witnessの型が異なる＋主張外

FCSは量子模型族であり、族Aと同様に排除対象でない。過去の却下候補
（mean-blind fluctuation）はFCSの**導関数階層内の恒等式**に還元されたが、
本witnessは cumulant 階層の量ではなく応答Hankelの特異値であり、
還元の写像先が存在しない。ただし「FCS模型がfullデータを再現できること」自体は
問題ない（量子側の説明可能性は主張と両立する）。

### 4.4 族C（compact-group synchronization、higher-order含む）——構造的に写像先がない

**過去6候補の共通死因への正面対応。** 死因はすべて、witnessが相対chart
G_ij = X_j X_i^{-1} の（不）整合性として表現できたことによる。本提案では：

1. データは語 w に対するスカラー応答 R(w) のみ。**「2つのchartの比」に当たる対象が
   interfaceに存在しない**。ペア (i,j) にラベルされた相対量が一切ないため、
   group-valued edge/hyperedge potential への写像は定義域から構成できない。
2. witnessは整合性（cycle consistency の破れ）ではなく**容量（rank下界）**である。
   synchronization は「不整合データから大域chartを推定する」枠組みであり、
   rank下界を回復する道具ではない。
3. それでも Duncan–Kileel 型 higher-order 監査（h = 3, 4）を独立gateとして実施する
   （§5 ステップ6）。spec §0 の通り**族Cは独立gateであり、P0-Dの達成は族Cを排除しない**。
   万一、語構造 w = w_1…w_ℓ を hyperedge とみなす写像で応答が group potential に
   埋め込めた場合は、その写像を記録して§6.4へ送る。

### 4.5 族E（process tensor）——排除しない（明示的に主張外）

χ ≤ 36 の process tensor は本interfaceを表現できる（はず）。主張外。
「process tensorなら表現できるが非効率」という**下界なしの表現は書かない**
（維持できない表現リスト遵守）。

### 4.6 族G（解析的reduction gate）

- **Krylov縮約:** T4 で正面から使用。d = 3 の reachable-observable 次元が
  witness 構成後も ≥ 7 であることを SymPy で確認する（§5 ステップ4に含める）。
- **BCH/Dyson:** witnessは摂動展開の低次項の異常ではなく非摂動的なrank量。
  ただし深さ4語の応答が深さ≤2語の応答の多項式で書ける可能性（それなら rank は
  上がらない）を排除するため、exact minor 認証を行う——これがまさにステップ4。
- **Kalman/線形実現:** 4.1 に同じ（linear realization ≤ 6 も排除される）。
- **quantum regression / symmetry:** 生成模型の対称性による次元縮約は
  Krylov確認に含まれる。gauge対称性（相似変換）は T3 の余次元勘定で明示的に商を取る。

### 4.7 Frozen-Theories 3件との関係

RISEI・SMRT・EITはいずれも応答の値・分類・保護を扱い、**応答を再現する機構の
表現コスト**については何も主張していない。矛盾する定理はない。
本提案はSMRTのrational transfer構造を生成側クラスとして継承し（§1.1）、
その上に容量の層を追加する。凍結結果の結論を新規性に数えていない
（rank ≤ D_cl は既知、SMRT構造も既知。新規なのは入れ子構成の存在と例外集合の構造）。

### 4.8 §6.4/§6.5 の却下・惜しかった候補6件との差分

| 過去候補 | witnessの型 | 本提案との構造差 |
|---|---|---|
| Response–Mechanism Contextuality | sector gluing obstruction | 本提案はgluingを主張しない。単一interfaceの容量のみ |
| mean-blind fluctuation | 順序依存の2次cumulant | cumulantでなくrank。FCS階層に写像先なし |
| Relative-gauge splitting | ΔK₂ = 2ℓ_Y(G−I)r_X（相対chart量そのもの） | 相対量を定義しない |
| SU(d) tree calibration atlas | gauge chart の大域貼り合わせ | chartもatlasも使わない |
| Held-out quotient predictor | quotient class 予測 | 予測の一意性でなく表現の不可能性 |
| Global cycle quotient atlas | cycle consistency / ABSTAIN | cycleが存在しない（ペアデータがない） |

共通死因（pairwise因子化）は「witnessが相対chartの関数だった」ことに起因する。
本提案のwitnessは chart-free（gauge不変ですらなく、gaugeの概念が発生しない）。
**これは偶然ではなく設計原理である**：競合のnull identityから逆設計したため、
witnessの型が最初から「競合族が必ず満たす恒等式の破れ」に固定されている。

### 4.9 最も危険な還元先（自己申告）

**「これは新理論ではなく、既知のrealization theory＋既知のHMM同定理論の
一適用例（うまく作った反例1個）にすぎない」という還元。**
これが本提案のdesk rejection筋である。反論の骨子：
(i) generic理論は例外集合の**存在**は含意するがその**構造**（余次元・安定性・
有限shot margin landscape・最小量子次元 d=3）を与えない、
(ii) 入れ子（calibration側の存在証明＋full側の排除）という**対の構成**は
既知定理の適用では出ない、(iii) 予算・shot・有意水準まで凍結した
**事前登録型の分離certificate**は方法論的新規性を持つ。
ただし (iii) だけではPRXどころかPRLも危うい。**T3（例外集合の構造定理）が
埋まらない場合、本提案は「証明書付き数値構成」であって理論ではない**。
この点を§6の筆頭に置く。

---

## 5. 検証計画

### 5.0 held-out 汚染防止（ガイド§11.2 警告への対応）

seed 20260723 の held-out 64 protocol は**本提案では使わない**（過去提案での使用状況が
不明のため）。本提案専用に新しい seed を引き直す：**seed 20260725210**（本提案番号21を
埋め込み）。depth-4 held-out 64 protocol をこのseedで抽出し、候補生成・最適化・
停止判定には一切使用しない。この割当を本節に記録した（再抽出方式）。

### 5.1 ステップ3の実装：M_D の明示構成（calibration側の存在証明）

構成順序は「M_D 先行」とする（positive realization problem を回避するため）：

1. **M_D を先に設計する。** D_cl = 6 の古典HMM：letter w ごとの部分確率行列
   T_w ∈ ℝ^{6×6}_{≥0}（Σ_w T_w が行確率的）、初期分布 π₀ ∈ Δ⁵、readout重み。
   有理数成分で構成し、非負性・正規化を exact に満たすことを SymPy で確認。
   自由parameter数は P ≤ 256 の予算内（6×6×6 + 6 + 6 = 228）。
2. **深さ ≤ 2 の目標値を確定する。** M_D の calibration応答
   {P_{M_D}(w) : |w| ≤ 2}（43値）を exact 有理数で計算。
3. **M_* を制約付き最適化で構成する。** d = 3 GKSL介入模型のparameter
   （Hamiltonian、jump operators、介入letterごとのgenerator変更、propagator時間）を、
   (a) 深さ≤2応答が目標値に一致（43本の等式制約）、
   (b) opnorm ≤ 1、(c) σ₇(H_full) 最大化、の下で射影付き山登り
   （sigma7_smoke.py の手法を等式制約版に拡張）。
   **最適化予算の事前登録:** restart 32、反復 5000/restart。これで
   σ₇ ≥ 2τ_H に届かなければ反証条件2が発動（m や d の設計を見直し、変更は記録する）。
4. **一致の厳密化。** 数値最適化解の近傍で、等式制約を SymPy の有理数化
   （連分数近似 → exact代入検証）により厳密一致へ引き込む。
   引き込みで σ₇ がどれだけ劣化するかを記録（劣化後も ≥ 2τ_H が要件）。

**リスクの明示:** smoke で確認済みなのは弱い入れ子条件（det H_cal = 0）のみ。
43本の等式制約ははるかに強く、feasibilityは未確認。**これが本提案の最初の
go/no-go 実験である。** 失敗した場合の縮退案：等式を許容誤差 ε_cal（shot noise の
1/10 以下）付きの近似一致に緩め、「厳密一致」主張を「統計的識別不能」主張へ
降格する（判定もPRL型からさらに下がりうることを認める）。

### 5.2 ステップ4の実装：rank-7 minor の exact 認証（full側）

1. M_* の応答 R(w)（深さ ≤ 4 全語）を有理数（または代数的数）で exact 計算。
   propagator は有理近似ではなく、**生成側を最初から有理行列の積で設計する**
   （E_w を直接有理縮小行列として構成し、GKSL実装可能性は別レイヤーで確認する
   二段構え。GKSL propagator の exact 表現が困難な場合の fallback）。
2. H_full（43×43）を組み、7×7 小行列式で非零のものを SymPy `Matrix.det()`
   （exact演算）で1つ以上認証。行・列の選択は prefix–suffix 閉包を保つ。
3. σ₇ は倍精度＋mpmath 多倍長の両方で計算し一致を確認（独立実装2系統の要件）。
4. Weyl margin の統計側：τ_H(α) を二項モデルから導出し、α = 0.01 での
   判定閾値を事前登録。判定式 σ₇^{observed} > τ_H(α) + τ_H を固定。

### 5.3 競合fit（kill test の実行）

1. **族D fit:** D_cl = 1..6 の各次元で、事前登録した最適化手続き
   （restart 16、P ≤ 128 標準）により full データへの最良fitを求め、
   残差が許容誤差を超えることを確認（hidden-dimension escalation、
   stage0-checklist B-3-1 に対応）。
2. **族C 独立gate:** h = 3, 4 の higher-order synchronization baseline を実装し、
   応答データを group potential へ写す試みを行う（写像が構成できない、を
   確認作業として記録する。構成できたら§6.4行き）。
3. **族G gate:** M_* の観測Krylov次元を exact 計算し ≥ 7 を確認。

### 5.4 ChatGPT 赤チームへ渡す主張（claim-template 形式、Stage 1 で抽出予定）

- 主張1: boxed命題の条件1–3（構成の存在）
- 主張2: T3（例外集合の余次元と安定性）
- 主張3: T4（最小量子次元 d = 3）
- 主張4: 「witnessは group-valued hyperedge potential へ写らない」（族C論証）

各主張は別チャット・3回・還元命令形式で（ガイド§11.2）。

---

## 6. 弱点と未解決点（弱点申告フォーマット準拠）

- **最も危険な既知還元:** §4.9 に詳述。「既知realization theoryの一適用例」への還元。
  T3 が埋まらなければ理論を名乗れない。次点：族Cのhigher-order監査で
  語→hyperedge の予期しない写像が見つかること。
- **最も弱い仮定:** 深さ≤2厳密一致（43等式）のfeasibility。smokeが確認したのは
  det H_cal = 0 のみで、真の入れ子制約でσ₇がどこまで残るか未検証。
  ここが崩れると boxed命題の条件2が近似版へ降格する。
- **最も脆い数値操作:** (a) 等式制約付き山登りの収束（射影が非凸集合への射影になる）、
  (b) 有理数化引き込みでのσ₇劣化、(c) 43×43 Hankelの成分が確率スケールに
  収まらない場合の正規化再設計。
- **最も不足している物理接続:** E_w を「有理縮小行列」として設計した場合、
  それが実際に d = 3 GKSL介入propagatorとして実装可能かの逆問題が未解決。
  実装不能なら「GKSL介入模型」の看板が外れ、単なる線形系の反例になる
  （物理的意義が大きく下がる）。実験プラットフォーム（Eu:YSO / NV）への
  翻訳は現段階で全く手つかず。
- **PRXを阻む一点:** P0-D 単独では「hidden ancilla を入れれば説明できる」
  可能性が排除されておらず、主張は古典・線形排除に限定される。
  spec §3 ステップ7 の通り**PRL型**。PRX昇格には族A・Eの入れ子証明書が必要で、
  それは本稿の範囲外。
- **stop condition:** §3.1-4 の反証条件1–4。特に、事前登録した最適化予算内で
  σ₂τ_H 到達に失敗した時点で、m・d の設計変更1回のみ許し、
  それでも失敗なら本提案を§6.4へ記録して撤回する。
- **未解決点（明示）:** T3 の余次元勘定（gauge軌道次元の計算）。
  positive realization problem を回避する構成順序（M_D先行）が
  σ₇ 最大化と両立するかどうか。held-out shot 予算（1.28×10⁵）の資金的裏付け。

---

## 7. 参考文献

実在確認（DOI/arXiv照合）は Stage 3 で行う。それまで全件に確認状態フラグを付す。

| 文献 | 関連 | 状態 |
|---|---|---|
| Huang et al., "Minimal realization problems for hidden Markov models" (2016, IEEE Trans. Signal Process. と記憶) | generic HMM identifiability。本提案の例外集合設計の前提 | **未確認**（ガイド§6.1で言及済みだがDOI未照合） |
| Duncan & Kileel, "Higher-Order Group Synchronization" arXiv:2505.21932 (2025) | 族C higher-order baseline | 文献監査T2で確認済み |
| Riechers & Elliott, arXiv:2509.03004 | QHMM次元下界（族DQ、本稿範囲外だが分離profileの将来成分） | spec記載・**本文未読** |
| Zonnios, arXiv:2412.12812 | 同上 | spec記載・**本文未読** |
| Gu, Wiesner, Rieper, Vedral, "Quantum mechanics can reduce the complexity of classical models" (Nat. Commun. 2012 と記憶) | 定常確率過程での量子メモリ優位。**先行研究として最優先で差分を書く必要**：あちらは定常過程・漸近レート、本提案は介入interface・有限shot・入れ子certificate | **未確認** |
| positive realization problem の標準文献（Benvenuti & Farina のsurveyと記憶） | M_D先行構成の理論的根拠 | **未確認** |
| classical Hankel rank と weighted automata の標準文献（Carlyle–Paz / Fliess） | null identity の出典 | **未確認** |

**§7 表への転記時の注意:** Gu et al. 系統（quantum memory advantage of stochastic
processes）は「決定的な差分が書けない論文」になるリスクが最も高い。
差分候補は (i) 介入（controlled）interface vs 定常過程、(ii) 有限shot事前登録
certificate vs 漸近的メモリレート、(iii) 入れ子構造（calibration一致の同時要求）。
Stage 3 で最優先照合とする。
