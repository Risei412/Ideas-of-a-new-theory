# 凍結資源実現ギャップ理論（Frozen-Resource Realization-Gap Theory / FRRG）

## 一行サマリ

calibration データ（depth≤2）を厳密に再現する 6 状態古典 HMM が明示的に存在するにもかかわらず、full データ（depth≤4）は D_cl≤6 のいかなる古典実現でも再現不能であることを、有限 shot 予算内で認証できる matched pair（入れ子証明書）の存在を主張する。

**作成日:** 2026-07-25
**位置づけ:** ガイド §6.1 P0「Resource-bounded mechanism separation」への Stage 0 提案。`docs/p0-certificate-spec.md` のステップ3–4（P0-D 証明書の構成と認証）を理論の中心命題として定式化したもの。
**型（§2）:** (B) 数学的定理型（no-go／資源下界）＋数値証明書。統合型 (D) 寄り。対象系は有限次元・操作的インターフェース（controlled word response）。想定読者は量子情報・システム同定・開放系。
**判定:** **PRL 型候補**。P0-D（古典 HMM 族の排除）単独では P0 全体の達成ではない（`p0-certificate-spec.md` §5）。P0-A / P0-E / P0-DQ / P0-C は独立 gate であり、本提案の範囲外。複数族を排除できた時点で PRX 型へ昇格を検討する。

**番号について:** `Blueprints-of-theories/` の既存最大は `plan20_`（番号 20 を占有）。§9 の番号規約（通し番号・再利用禁止・最大値+1）に従い本提案は 21 とする。

---

## 0. 結論

**中心の問い:** 同一の観測インターフェース（固定した alphabet・depth・shot 予算）の下で、「このデータは凍結資源内の競合モデルでは説明できない」という主張は、どのような場合に有限の証明書として成立するか。

文献監査（`docs/literature-audit-report.md`）により、一般位置ではこの主張は成立しない（Huang et al. 2016: 一般位置の有限 HMM は有限長 word 確率から minimal realization が復元される）。したがって主張が生き残る場所は **一般位置の外＝rank-deficient / cancellation-protected な例外集合** に限られる。そこに「calibration では競合が実在する」という入れ子条件を重ねたものが本理論の固有現象である。

**理論固有現象（boxed 命題）:**

> **［認証付き実現ギャップ / Certified Realization Gap］（status: Conditional — 構成目標。ステップ2のスモークで到達可能性は GO 判定済み、明示構成は未完）**
>
> intervention alphabet `u ∈ {1,…,m}`（m=6）、語集合 𝒲_cal（長さ ≤2）、𝒲_full（長さ ≤4）、opnorm 正規化 `‖V_u‖₂ ≤ 1` の下で、次を同時に満たす 7 次元 full 実現 ℱ_full = (V_u, c, p) と 6 状態古典 HMM M_D が存在する：
>
> (i) **［入れ子条件・calibration 側の存在］** M_D は状態数 D_cl ≤ 6、非負・正規化を満たす明示的な古典 HMM であり、
> `P_{M_D}(w) = R_full(w)` が **すべての** `w ∈ 𝒲_cal` について厳密（exact arithmetic）に成り立つ。
>
> (ii) **［full 側の容量超過］** 行・列語がすべて長さ2である 8×8 部分行列 `H_wit`（成分は深さ4の語ちょうど64個）が
> `rank(H_wit) ≥ 7` を満たし、これは非零 7×7 minor の exact arithmetic 評価で認証される。
> `rank(H_wit) ≥ 7` は `rank(H_full) ≥ 7` を含意する。
> 同時に `H_cal`（添字は長さ ≤1 の語、7×7）は `rank(H_cal) ≤ 6`（(i) の帰結として自動成立）。
>
> (iii) **［有限 shot での認証可能性］** `σ₇(H_wit) ≥ 2τ_H(8) = 0.1265`（2000 shots/setting、settings=1、
> 二項上界 `σ_entry ≤ 1/(2√n)`、Weyl 摂動評価）。よって rank ≥ 7 は凍結 shot 予算内のノイズ下でも維持される。
>
> ※ (ii)(iii) の認証対象は当初 43×43 の `H_full` 全体だったが、それは凍結 shot 予算の 20.25 倍を要し
> 実行不能であることが判明したため、8×8 部分行列へ差し替えた（`p0-certificate-spec.md` §4quater）。
>
> **帰結（資源下界）:** D_cl ≤ 6 のいかなる非負古典 HMM も 𝒲_full 上のデータを再現できない。
> しかもこの排除は、calibration データだけを見る限り「6 状態で十分」に見える系に対して成立する。
> すなわち本現象は、**Huang 型の一般位置同定が失効する rank-deficient 例外集合
> `{det H_cal = 0}` の上における、凍結資源内の下界**である（§6.1 の 2026-07-25 制約に整合する形）。

主張しないこと（scope の明示）：本命題は族 D（古典 HMM）のみを排除する。hidden ancilla 付き GKSL（族 A）、process tensor（族 E）、QHMM（族 DQ）、群同期（族 C）は排除しない。**P0-D の達成 ≠ P0 の達成**。

---

## 1. なぜこの方向を選ぶのか

### 1.1 既存理論から引き継ぐ事実（§4 参照）

- **応答の形:** `R_full(w) = p† V_{w_k}···V_{w_1} c`。SMRT / RISEI の rational transfer・doubling realization と同形（SMRT の再利用可能な結果「有限次元 rational transfer としての応答表現」「exact arithmetic を用いる認証方針」を継承）。
- **exact 認証の流儀:** SMRT の「有限個の moment / minor による exact-zero certificate」「浮動小数点 sampling を exact claim にしない」（§4.2 赤線 4、§10.3A）をそのまま踏襲し、rank 認証を exact arithmetic（SymPy 有理数）で行う。
- **有限資源の勘定:** RISEI の protocol 資源コストの発想（`𝒞[π]`, `𝒞_req`）を、shot 予算・setting 数・protocol 数として具体化した凍結予算（`p0-certificate-spec.md` §4.4–4.7）を使う。
- **数値的土台（実施済み）:** ステップ2スモーク（`scripts/sigma7_smoke.py`）— Hankel 43×43、H_cal 7×7、opnorm 正規化採用、`σ₇(H_full)` は射影付き山登りで 0.609 到達（要求 0.2933）、判定 GO。
  続くステップ2bis（`scripts/minor7_smoke.py`）で**認証対象を 8×8 部分行列へ差し替え**、`σ₇(H_wit) = 0.1934` 到達（要求 `2τ_H(8) = 0.1265`、余裕 1.53×）。ランダム構成の合格率は 0%（43×43 版の 6.8% より厳しい）。

### 1.2 壊す仮定 ← 新規性の源泉

**壊す仮定は一つ（§4.4 予算内）:** **unrestricted representation criterion** — 「モデルの hidden state / ancilla / memory の表現力に制限を置かず、『表現できるか否か』で理論を比較する」という前提。

これを壊し、**資源を族ごとに凍結した比較クラス**（本提案では古典状態数 `D_cl ≤ 6`）へ置き換える。表現不能性ではなく「凍結資源内での再現不能性＋その有限証明書」を主張の単位とする。

§4.4 の必須記述：

1. **外す仮定:** unrestricted representation criterion（上記）。
2. **維持する仮定:** 有限次元・time-local な操作的インターフェース、fixed comparison class（初期状態・probe・readout・観測窓・正規化を固定：赤線 2）、opnorm（縮小写像）正規化、凍結 shot 予算・setting 上限。Frozen-Theories の他の仮定はどれも外さない。
3. **代替する数学的構造:** 族ごとの凍結資源クラス＋入れ子証明書（calibration 側の存在証明 × full 側の容量超過証明）のベクトル値判定。
4. **失効する既存定理:** なし（Frozen-Theories の定理はどれも表現力無制限の主張をしていない）。失効するのは競合側の一般位置同定定理の**適用可能性**（Huang 2016 は general position 仮定が `det H_cal = 0` 上で外れる）。
5. **継承できる既存定理:** SMRT の realization 形式・exact certificate 方針、EIT/SMRT の「数値 zero ≠ exact zero」規律、RISEI の資源コストの語彙。
6. **元の理論を回収する極限:** `D_cl` の制限を外す（→ ∞）と、rank(H_full)=7 の線形実現が自明に存在し、ギャップは消える。一般位置（`det H_cal ≠ 0`）に戻すと Huang 型同定が働き、calibration データが実現を一意化してやはりギャップの「隠れ方」が消える。既存の実現理論・システム同定にそのまま接続する。
7. **仮定変更がなければ現象が消える control:** (a) 資源凍結を外した対照（D_cl=7 を許す）では full データを再現する競合が明示構成できること、(b) 入れ子条件を外した対照（generic な rank-7 実現）では calibration 側にも 6 状態 HMM が存在せず「最初から表現不能な過程を選んだ自明な勝利」に退化すること、の両方を数値で示す（§5 ステップ C）。

---

## 2. 理論の定式化

### 2.1 記号（§5.3 の衝突回避）

| 記号 | 意味 | 衝突回避メモ |
|---|---|---|
| `u ∈ {1,…,m}` | intervention label（m=6 標準） | alphabet に集合記号を割り当てない（𝒜/A は使わない） |
| `w = u_1⋯u_k` | intervention word、`𝒲_L` = 長さ ≤L の語集合 | — |
| `𝒲_cal = 𝒲_2`, `𝒲_full = 𝒲_4` | calibration / full 語集合 | 集合 C と書かない（`C` 衝突回避） |
| `H_wit` | 認証対象の witness 部分行列（8×8、行・列語は長さ2、成分は深さ4語64個） | §5.3 で `S` は sector と衝突するため、部分行列には `S` を使わず `H_wit` を新規割当 |
| `ℱ_full = (V_u, c, p)` | 7 次元 full 実現。`R_full(w) = p† V_{w_k}···V_{w_1} c` | 遷移行列に `M` を使わない（`M` 衝突回避、`V_u` を新規割当） |
| `M_D = (T^{cl}_u, b_0)` | 古典 HMM 競合。`P_{M_D}(w) = 𝟙† T^{cl}_{w_k}···T^{cl}_{w_1} b_0` | `M_D` は spec 由来の修飾付き記号。`D_cl` = 古典状態数（`D_damp`/`D_hidden` と書き分け） |
| `H_full`, `H_cal` | generalized Hankel（43×43、**解析用の概念的対象。実測しない**）と、添字が長さ ≤1 の語である 7×7 ブロック | — |
| `σ₇`, `τ_H` | 第7特異値、Hankel 摂動許容量 | — |
| `α` | 有意水準（`τ_H(α)` はステップ5で導出） | — |

`Ω K Q Ξ ν C M P A G S z q` は無修飾で使用しない。

### 2.2 定義

**定義 1（観測インターフェース）.** alphabet サイズ m、prefix/suffix 長 ≤2 の語集合を固定する。実測するのは全 1555 語ではなく、**calibration の 43 語（長さ ≤2）と witness の 64 語（`H_wit` を張る深さ4語）の計 107 語**である。各値は確率スケール `[−1,1]`（opnorm 正規化により `|R(w)| ≤ 1` 保証）。shot 予算は凍結値（calibration ≤ 1.2×10⁵ shots、held-out 独立予算 ≤ 1.28×10⁵、1000–2000 shots/setting、settings ≤ 2、標準は 1）。

**定義 2（凍結資源クラス 𝔇₆）.** 状態数 `D_cl ≤ 6`、非負遷移 `T^{cl}_u ∈ ℝ_{≥0}^{6×6}`（列和 ≤1 の substochastic、正規化規約はステップ3で凍結して記録する）、非負初期分布 `b_0` を持つ古典 controlled HMM の全体。

**定義 3（入れ子証明書）.** 組 `(ℱ_full, M_D, 𝒲_cal, 𝒲_full)` が次を満たすとき P0-D 証明書と呼ぶ：
(i) `P_{M_D}(w) = R_full(w)` ∀`w ∈ 𝒲_cal`（exact）、(ii) `H_wit` 内の非零 7×7 minor による `rank(H_wit) ≥ 7`（exact、ゆえに `rank(H_full) ≥ 7`）、(iii) `σ₇(H_wit) ≥ 2τ_H(8)`（数値、誤差評価付き）。

**主命題（= §0 の boxed 命題）.** P0-D 証明書を持つ組が存在する。status: Conditional（構成目標）。

**補題 1（入れ子の自動成立）.** (i) が成り立てば `H_cal` の全成分は 6 次元実現 M_D の word 確率に一致するので `rank(H_cal) ≤ 6`、特に `det(H_cal) = 0`。すなわち構成は自動的に例外集合 `{det H_cal = 0}` 上に載る。status: Exact（自明、Hankel の factorization `H_cal = 𝒪𝒞_ctrb` 型の標準論法。ただし prefix–suffix 閉包を保った添字設計が前提 — spec §1 の警告どおり）。

**補題 2（ノイズ頑健性）.** `‖ΔH_wit‖₂ ≤ τ_H(8)` なら Weyl の不等式より `σ₇(H_wit + ΔH_wit) ≥ σ₇(H_wit) − τ_H(8) > 0`。判定条件は `σ₇(H_wit) > τ_H(8; α)`。status: Exact（Weyl の適用自体）。
**ただし `τ_H` の値そのものは未確定** — 現行の `(√a+√b)σ_entry` は独立同分布成分の乱雑行列に対する評価であり、Hankel は同一語を共有する成分が完全に相関するため、構造化ノイズ下の評価へ置き換える必要がある。`τ_H(α)` の統計模型はステップ5（未完、§6 参照）。

**注意（非対称性）.** `rank(H_cal) ≤ 6` は 6 状態**非負** HMM の存在を保証しない（quasi-HMM との差、spec §1）。だからこそ (i) は LP feasibility ではなく**明示構成**で与える。本提案の構成順（§5）は M_D を先に置くので、この非対称性は構成上自動的に処理される。

---

## 3. 理論固有現象

### 3.1-1 固有現象の定義

§0 の boxed 命題。名称：**certified realization gap ／ 認証付き実現ギャップ**（英日併記、§5.4 規約）。

現象の核は「ギャップの値」ではなく **ギャップの認証可能性の局在**である：一般位置では原理的に存在できず（Huang 2016 が塞ぐ）、資源無制限でも存在できず（7 次元実現が自明に再現）、**例外集合 × 凍結資源 × 入れ子条件の交差点にのみ**現れる。

### 3.1-2 非還元性の証明または論拠

§4 で詳述。要点：主張の単位が「現象の再現」ではなく「凍結資源内の下界の有限証明書」であるため、競合モデルがデータを再現すること自体は反駁にならない — 再現に要した資源が凍結値を超えていることが主張内容である（`docs/reduction-targets.md` Pass-1 結論「最短の信頼できる経路は resource lower-bound theorem」に沿う）。

### 3.1-3 観測可能量（observable signature）

- **物理量:** 有限 shot 推定された witness 部分行列 `Ĥ_wit`（8×8）の第7特異値 `σ₇(Ĥ_wit)`、および calibration 残差 `max_{w∈𝒲_cal} |P_{M_D}(w) − R̂(w)|`。
- **現れ方:** 閾値型。`σ₇(Ĥ_wit) > τ_H(8; α)` かつ calibration 残差が二項誤差内、という**同時成立**が signature。単独ではどちらも自明。
- **検出手段とコスト:** 数値実験（custom NumPy/SymPy、QuTiP/CVXPY 不要）。shot コストは凍結予算内で完結する設計（m=6、1 setting: calibration 86,000 shots＝長さ≤2 の全語43本、held-out 128,000 shots＝`H_wit` の深さ4語64本、合計 214,000）。実験実装は将来課題（§6）。
- **有限サイズ・有限精度:** ステップ2bis で確認済み — 理想データで `σ₇(H_wit)=0.1934` まで構成可能、要求 `2τ_H(8)=0.1265`（1 setting）に対し 1.53× の余裕。有限 shot での可視性はまさに (iii) が保証する設計になっている。

### 3.1-4 反証条件

以下のいずれかが成立したら本提案（の中心命題または新規性）は棄却・縮小する：

1. **kill test D（最重要）:** 赤チームまたは数値探索が、`D_cl ≤ 6`・`P ≤ 256` の controlled HMM で 𝒲_full 上の全データを事前登録許容誤差内で再現する（`reduction-targets.md` D 族 kill test）。
2. ステップ3の構成が失敗する — 非負性・正規化・calibration 厳密一致・`σ₇ ≥ 2τ_H` を同時に満たす組が、最適化を尽くしても見つからない（ランダムでは 6.8% しか通らないことは既知。最適化でも通らなければ死）。
3. `τ_H(α)` の正直な統計模型（ステップ5）が要求水準を 0.609 超へ押し上げる。
4. 一般位置の摂動に対して現象が測度零でしか存在せず、かつ摂動半径が shot ノイズより小さい（＝実験的に到達不能な集合）と判明する。※例外集合上の現象であること自体は設計だが、**認証マージン `σ₇ − 2τ_H` が例外集合からの距離に対して安定であること**は要求する（§5 ステップ D）。
5. 本 witness が族 D 以外の**より弱い**既知資源勘定（例：線形 quasi-realization の次数 7 という事実だけ）に完全に還元され、非負性凍結が何も足していないと示される — すなわち「D_cl≤6 非負 HMM の排除」と「次数 ≤6 線形実現の排除」が本構成上区別不能である場合。この場合、主張は既知の Hankel rank 論法の言い換え（L0–L1）に落ちる。区別のための ablation を §5 ステップ C に置く。

### 3.1-5 既存理論との一致領域（sanity check）

- `D_cl` 無制限 → 7 次元線形実現が全データを再現（標準実現理論に一致）。
- 一般位置（`det H_cal ≠ 0`）→ Huang 2016 の同定が適用可能になり、calibration＋有限 word で実現が固定される（既知理論に一致）。
- ノイズ零・shot 無限 → 判定は exact rank 判定に退化（標準の Hankel rank 理論に一致）。
- m=1（単一 intervention）→ 通常の自律 HMM / モーメント問題に退化。

### 3.2 固有性の自己評価

現時点 **L2–L3 の間**。構造（例外集合×凍結資源×入れ子）は既存枠組みで自然には出ないが、非還元性の最終判定は赤チーム工程（Stage 2）を通るまで確定しない。L3 と書くのは还元監査通過後。

---

## 4. 非還元性の検討

前提：死因テンプレート（§6.5）は「pairwise relative-chart 因子化 `G_ij = X_j X_i^{-1}` への還元」。本提案は**そもそも chart / gauge / 群値データの推定問題を含まない**ことを最初に確認する。データは word 応答のスカラー列、証明書は線形代数的 rank / 特異値下界であり、ノードごとの latent frame も、その商も、cycle consistency も現れない。

### 4.1 既知の一般的機構への還元

| 機構 | 還元試行の予想経路 | 反論（なぜ還元されないと考えるか） |
|---|---|---|
| **shared ancilla / enlarged GKSL** | 「hidden ancilla を足せば full データを再現できる」 | 再現できてよい。本主張は古典 D_cl≤6 の排除であり、量子拡張の存在は主張と両立する（族 A は独立 gate として未主張）。却下済み候補 1 と異なり「量子で説明できないこと」を主張しない |
| **tilted-GKSL / FCS** | 「word 応答は tilted generator の cumulant 階層で書ける」 | 書けてよい。FCS 模型は 𝔇₆ の元ではない。却下済み候補 2・3 と異なり、witness の**値**（例：ΔK₂ 型の exact 式）に固有性を置いていない。固有性は資源下界の証明書に置く |
| **compact-group synchronization（pairwise）** | 「calibration/held-out 構造は gauge fitting と同型」 | データから群値 edge/hyperedge potential への写像が存在しない（スカラー応答の Hankel であり、`G_ij` 型の相対量が定義されない）。却下済み候補 5・6 の死因構造そのものが不在 |
| **higher-order group synchronization（h=3,4；Duncan–Kileel 2025）** | 「depth-3 connected witness は hyperedge potential で説明可能」 | 同上 — 本 witness は「pairwise を破る depth-3 量」ではなく rank 下界であり、群への写像が主張されない。ただし**構造的論証だけで済ませず**、§6.5 の要件に従い h=3,4 baseline の実装照合を Stage 2 で行う（§5 ステップ E）。「群値 hyperedge potential へ写らないことの構造的論証」枠を狙う |
| **構造化系同定 / minimal realization（Huang 2016, Ohta 2021）** | 「有限 word から realization を復元して終わり」 | 一般位置定理は `det H_cal = 0` 上で適用不能。さらに同定は「実現を見つける」問題で、本主張は「凍結資源内に実現が**ない**」問題。同定成功はむしろ kill test の失敗（=候補側の生存）を意味しない点に注意して Stage 2 に出す |
| **Zeno / Schur / adiabatic elimination** | 「実効低次元模型で説明」 | 実効模型が非負 6 状態 HMM の形に落ちるなら kill test D に吸収される（別経路ではない）。落ちないなら排除対象外の族 |
| **Kalman / linear realization（G 族 gate）** | 「rank(H_full)=7 は線形実現論の自明な帰結」 | ここが最も危険な還元（§6 に再掲）。差分は (a) 非負性凍結（quasi-HMM と HMM の差）、(b) 入れ子（calibration 側の非負存在）、(c) 有限 shot 認証マージン。この 3 点を外した主張はしない |

### 4.2 Frozen-Theories への還元

- **RISEI:** 資源コストの語彙は借りるが、RISEI は競合モデル族に対する下界を与えない。Möbius 分解・protected cluster の結果は本命題に使われない（衝突なし・依存なし）。
- **SMRT:** realization 形式と exact certificate 方針を継承する（§1.1）。SMRT の三分類（ν∈{∞,(0,∞),0}）は full-minus-cut 差分の漸近に関する主張で、競合資源の下界ではない。SMRT から本命題は導出できない。
- **EIT no-go/go:** 対象が sector 差分 `δχ_𝕊` の零・非零であり、資源勘定を含まない。共有するのは exact arithmetic の規律のみ。

### 4.3 却下済み・惜しかった 6 候補との差分（§6.4 / §6.5）

6 件すべてに共通する死因は pairwise relative-chart 因子化への還元、すなわち「観測データ → ノード間相対量 `G_ij` → 群同期問題」という写像の存在だった。本提案では：

1. データに chart 構造がない（単一の応答 functional の word 列。ノード集合も edge も定義されない）。
2. 主張が「witness の非零値」ではなく「凍結クラス全体に対する下界＋その有限証明書」。惜しかった 4 候補はいずれも witness/predictor の**値や予測性能**に固有性を置き、中立 estimator に値ごと一致されて死んだ。下界主張は「一致される」ことでは死なない — 一致した競合の資源が凍結値以下だった場合のみ死ぬ（それが kill test D）。
3. Matched operational equivalence（惜しかった候補 1）との差分が最も重要：同候補も matched pair と有限資源 certificate `(d_min,k_min)=(2,2), N_5% ≤ 137` を持っていた。差分は (a) 当時は一般位置上の構成で、Huang 型復元に対する防御がなかった、(b) 競合クラスが凍結されておらず「どの族に対する下界か」が未定義だった、(c) 入れ子条件（calibration 側の競合の実在）がなかった。本提案はこの 3 点を仕様として最初から組み込む。

### 4.4 競合論文（§7 対応、family-level）

文献監査 56 件（literature-master-table）に基づく。最大脅威は T1 Huang 2016（一般位置同定）と D05 Riechers–Elliott（QHMM 下界の先行）。前者は例外集合設計で回避し、後者は**古典族に限定した主張**とすることで衝突しない（QHMM の閾値を書かない — spec §1 の警告に従う）。族 C の h=3,4 は §5 ステップ E で baseline 照合。

---

## 5. 検証計画

held-out の扱い（§11.2）：**再抽出方式**を採用する。既存 seed `20260723` の held-out 集合（depth-4 64 protocols）は過去の候補設計に使用済みのため本提案では使わない。本提案の held-out は新規 seed **`20260725`** で depth-4 から 64 protocols を引き直す。seed と割当のこの記録が §11.2 の要件を満たす。

### ステップ A（= spec ステップ3）：M_D と ℱ_full の明示構成

**構成順序が本質：M_D（calibration 側）を先に置き、full 側を後から接木する。** これにより入れ子条件 (i) と `det H_cal = 0`（補題 1）が構成上自動成立し、LP feasibility が不要になる。

1. **M_D の構成:** `T^{cl}_u ∈ ℚ_{≥0}^{6×6}`（u=1..6）を有理数成分で置く。正規化規約（substochastic の向き・出力規約）をここで凍結し文書化する。初期分布 `b_0 ∈ ℚ_{≥0}^6`、`Σ b_0 = 1`。ランダム有理初期値から出発。
2. **ℱ_full のブロック接木 ansatz:**
   ```
   V_u = [ T^{cl}_u   x_u ]      c = [ b_0 ]      p = [ 𝟙 ]
         [ f_u†       g_u ]          [ 0  ]          [ ρ_u… 実際は p_7 ≠ 0 ]
   ```
   第 7 状態の寄与が depth ≤2 の語で厳密に消えるよう線形制約を課す。最小の十分条件の一例：`f_u† b_0 = 0` ∀u（入口が初期分布と直交）かつ `c_7 = 0`。このとき状態 7 を通る最短の寄与語は長さ 3（`b_0 → T^{cl}_s → f 経由で 7 → x で復帰/読出`）となり、𝒲_cal 上で `P_{M_D}(w) = R_full(w)` が**恒等的に**（数値一致でなく構造的に）成立する。制約は u あたり 1 本の線形式で、自由度（7²·6+α で 300 超）に対して十分緩い。
   ※この ansatz が σ₇ 要求と衝突する場合の代替：depth-2 寄与のペア相殺（`Σ` 条件付き）へ緩和する。どちらを採ったか記録する。
3. **正規化:** `‖V_u‖₂ ≤ 1` を射影（特異値クリップ後に非負ブロック構造へ再射影）で維持。opnorm 規約はステップ2の凍結決定。
4. **最適化:** 目的関数 `σ₇(H_wit)`（行・列語を長さ2から選んだ 8×8 部分行列。行列自体の選択は最大体積ヒューリスティクス＝主成分部分空間への pivoted QR）、制約（非負性・接木線形制約・opnorm）付き射影山登り。ステップ2bis の実績（1500 反復で 0.0618→0.1934）と同じ機構をブロック構造上で回す。目標 `σ₇(H_wit) ≥ 0.19`（= 1.5 × 0.1265、マージン付き）、下限合格 0.1265（1 setting）／0.1789（2 settings）。
   **ランダム構成の合格率は 0%** なので最適化は必須（ステップ2bis）。反復数に対して単調改善が続いていたため、上記到達値は下界であり上限ではない。
5. **有理化:** 最適化解を分母上限付き有理数へ丸め、接木制約を exact に再充足（線形制約なので有理射影で厳密に解ける）。丸めによる `σ₇(H_wit)` 劣化を測り、劣化後も `≥ 2τ_H(8)` を確認。

**成果物:** `model.yaml` 相当（V_u, T^{cl}_u, b_0, c, p の有理数値、正規化規約、seed、commit hash）＋ §10.4 の reproducibility bundle。

### ステップ B（= spec ステップ4）：SymPy による exact 認証

1. `H_wit` の 8×8 全成分（深さ4語64個）を `sympy.Rational` の行列積で厳密計算。`H_cal`（7×7）も同様。prefix–suffix 閉包を保つ添字生成は `minor7_smoke.py` の `words_upto` / `depth2_block` と同一規約（spec §1 の警告対応）。
   **43×43 の `H_full` 全体は構成しない** — 深さ4語 1296 個を要し凍結予算の 20.25 倍になるため（spec §4quater）。認証は `H_wit` 内で閉じる。
2. **rank ≥ 7 の認証:** 浮動小数点 LU で pivot 候補の行・列 7 本を選び、その 7×7 部分行列の行列式を `sympy` の分数演算（Bareiss）で評価。非零なら認証完了。第一候補が零なら pivot 選び直し（最大 20 候補）。
3. **rank(H_cal) ≤ 6 の認証:** 補題 1 により構造的に成立するが、独立検証として `det(H_cal) = 0` を exact に確認（構成のバグ検出を兼ねる）。
4. **独立実装照合（§10.1）:** NumPy 倍精度の SVD で `H_wit` の σ 系列を計算し、exact rank 判定と矛盾しないことを確認する。
5. `σ₇(H_wit)` は浮動小数点で報告し、後退誤差上界（`‖H_wit‖ε_mach` スケール）を併記。**exact 主張は rank のみ、`σ₇` は数値量**と明記する（§9 禁止事項の遵守）。

### ステップ C：control（§4.4-7 と反証条件 5 の ablation)

- **C1（資源解除 control）:** D_cl = 7 を許した非負 HMM が full データを再現できることを明示構成（ℱ_full 自体の非負化または相似変換で探す。見つからなければ「非負 7 状態でも不可」という追加情報として記録 — この場合、主張はより強くなるが非負実現次元の別問題が開く）。
- **C2（入れ子解除 control）:** generic rank-7 実現（det H_cal ≠ 0）では calibration 側 6 状態 HMM が存在しない（fit 残差が二項誤差の 10 倍超）ことを確認 — 「自明な勝利」との差を数値で示す。
- **C3（非負性の寄与の分離）:** 反証条件 5 への防御。`rank(H_cal) ≤ 6` を満たす**quasi**-realization（負値許容）と非負 HMM の判別が本構成で効いているか：もし任意の quasi 実現が自動的に非負化できてしまう領域なら、非負性凍結は空転しており主張を「次数 ≤6 線形実現の排除」（既知論法）へ格下げする。

### ステップ D：頑健性

- 例外集合からの距離に対するマージン安定性：構成点の近傍摂動（相対 10⁻³〜10⁻¹）で (i) の残差と `σ₇(H_wit)` の変化を測る。認証は摂動後の再射影点で行う。
- shots/setting の格下げ表（2000/1395/1000）に対する合否マップ。settings ≤ 2 の凍結制約下での動作点を明記。
- **`H_wit` の行・列語の選び方への依存**：最大体積ヒューリスティクスで選んだ 8×8 が最良とは限らない。別の選び方でマージンがどれだけ変わるかを記録し、選択規則を事前登録する（選び直しによる多重比較を避けるため）。

### ステップ E（Stage 2 準備）：族 C baseline 照合

h=3,4 の higher-order synchronization baseline に対する写像不能性の確認は、赤チームに委ねる前に自前で一度実施する：本データからの群値 hyperedge data の構成を**試みて**、写像が定義できない（または定義するとデータを説明しない）ことを記録する。§6.5 の要件「実装した上で破る」または「写らないことの構造的論証」への対応。

### 予算整合（凍結値との照合）

| 項目 | 値 | 凍結制約 |
|---|---|---|
| m / depth / prefix-suffix | 6 / ≤4 / ≤2 | 標準探索 m=6 |
| calibration | **43 protocols**（長さ≤2 の全語＝prefix–suffix 閉包）× 1–2 settings | 1 setting: 86,000 ／ 2 settings: 1395 shots/setting で 120,000（上限 1.2×10⁵） |
| held-out | **64 protocols**（`H_wit` の深さ4語、seed 20260725） | 1 setting: 2000 shots で 128,000 ／ 2 settings: 1000 shots で 128,000（上限 1.28×10⁵） |
| settings/protocol | ≤ 2（**標準は 1**） | 2 settings では held-out が下限ちょうどの 1000 shots/setting、余裕 1.08× |
| `σ₇(H_wit)` 要求 | 0.1265（1 setting）／0.1789（2 settings） | ステップ2bis で 0.1934 到達・GO |
| **合計** | **107 protocols** | **214,000 shots**（1 setting） |

> 旧設計（calibration 46 protocol に深さ3を含む、認証対象 43×43）は破棄した。深さ3は calibration からも
> witness からも外れている。深さ3を使う設計へ戻す場合は予算を引き直すこと（spec §4quater.4）。

### ステップ 5（spec ステップ5、本提案では仕様のみ）

`τ_H(α)` の統計模型（二項分散の非一様性、行列 Bernstein 型か経験ブートストラップか）を導出し、有意水準付き判定に置換する。**未完了である**ことを明記する。

---

## 6. 弱点と未解決点（§8 フォーマット）

- **最も危険な既知還元:** 「これは Hankel rank の標準論法（Kalman/線形実現）＋非負性の飾りにすぎない」（反証条件 5／ステップ C3）。非負性と入れ子が実質的に効いていることを示せなければ L1 に落ちる。次点で Huang 2016 — 例外集合上でも別の有限同定定理（例外 variety 上の identifiability）が文献に存在する可能性は未監査。
- **最も弱い仮定:** 接木 ansatz（`f_u† b_0 = 0`）が opnorm 制約・非負制約と同時に `σ₇(H_wit) ≥ 0.1265` を許すか。ステップ2bis のスモークは**ブロック構造なし・非負制約なし**のランダム実現で行われており、構造制約付きで到達可能かは未検証。ここが折れたら中心命題ごと折れる。**交錯不等式により部分行列版は 43×43 版より構成側の要求が厳しい**（同一点で `σ₇(H_full)=0.66–0.75` に対し `σ₇(H_wit)=0.19`）点にも注意。
- **最も脆い数値操作:** (a) 有理化での `σ₇(H_wit)` 劣化、(b) minor 選択の pivot 依存（零 minor を引き続ける可能性）、(c) `σ₇` と `2τ_H` の差が小さい場合の判定の precision 依存。**(d) `τ_H` の評価式そのもの** — 現行の `(√a+√b)σ_entry` は独立同分布成分を仮定した乱雑行列評価だが、Hankel は同一語を共有する成分が完全に相関する構造化ノイズであり、この式は正当化されていない（ステップ5で置換）。
- **最も不足している物理接続:** 本提案は操作的インターフェースの word 応答として抽象的に立てており、GKSL 系の具体的 protocol（どの介入がどの `V_u` を実現するか）への pullback がない。matched interface（赤線 2）の物理実装は完全に未着手。PRL 型としても「physical realization の 1 例」は要求されうる。
- **PRX を阻む一点:** P0-D 単独は「次数 6 以下の古典・線形実現は存在しない」という狭い主張であり、族 A（hidden ancilla、監査でいう『説明できるが大きい（最小次元の証明なし）』）が開いたまま。PRX には最低でも P0-A または P0-E の入れ子証明書が追加で要る。
- **stop condition:** (1) ステップ A の最適化が 10⁴ 反復オーダーで `σ₇(H_wit) ≥ 0.1265` に到達しない、(2) kill test D が成立、(3) ステップ C3 で非負性が空転と判明、(4) Stage 2 の 3 チャット判定で 1 回でも還元成功 — のいずれかで中心主張を撤回・縮小し §6.4 へ記録する。
- **その他未解決:** `τ_H(α)` 未導出（ステップ5、上記 (d) と連動）。ステップ2/2bis の分位点は 40–60 例で標本が小さい — 設計凍結前に再実行。QHMM（族 DQ）の定義固定は本提案では扱わない。

---

## 7. 参考文献

すべて `docs/literature-master-table.csv` ／ `docs/literature-audit-report.md` に索引済みのもののみ（本提案での新規文献なし）。確認状態は監査記録に従う。

1. Huang, Ge, Kakade, Dahleh, *Minimal Realization Problems for Hidden Markov Models*, IEEE Trans. Signal Processing 64, 1896–1904 (2016). DOI `10.1109/TSP.2015.2510969`, arXiv `1411.3698`.（T1・最大脅威）
2. Duncan, Kileel, *Higher-Order Group Synchronization*, arXiv `2505.21932` (2025, preprint).（T2・族 C higher-order gate）
3. Riechers, Elliott, *Identifiability and minimality bounds of quantum and post-quantum models of classical stochastic processes*, arXiv `2509.03004`.（D05・QHMM 下界。本提案は古典族限定で衝突回避）
4. Zonnios, arXiv `2412.12812`.（D06・QHMM 定義依存性。族 DQ を扱う際に要精読 — 本提案では未使用）
5. Ohta, *On the Realization of Hidden Markov Models and Tensor Decomposition*, IFAC-PapersOnLine 54, 725–730 (2021). DOI `10.1016/j.ifacol.2021.06.170`.
6. Perry et al., *Message-passing algorithms for synchronization problems over compact groups*, CPAM 71, 2275–2322 (2018), arXiv `1610.04583`.
7. Lerman, Shi, *Robust Group Synchronization via Cycle-Edge Message Passing*, FoCM (2022), arXiv `1912.11347`.

内部文書：`docs/p0-certificate-spec.md`（証明書仕様・ステップ2結果）、`docs/reduction-targets.md`（D 族 kill test / survival certificate）、`docs/literature-audit-report.md` §4.1（維持できない表現）、`scripts/sigma7_smoke.py`（数値的土台）。
