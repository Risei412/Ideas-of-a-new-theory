# 文献監査 Pass 4 — 族O（汎関数依存の非古典性・観測依存エントロピー）

**監査日:** 2026-07-26
**基準:** `docs/literature-audit-specification.md`
**対象:** ガイド §6.1 P1「**Nonlinear functional hierarchy**」（壊す仮定: linear response functional）
**発端:** 「観測の組み合わせでのみ信号が得られる理論は可能か。先行例でどれだけ解決されているか」という問い
**状態:** 判定完了。**着手前kill。**

---

## 0. 結論

**判定: 死。この方向は提案として立てられない。**

kill は**二重**であり、しかも**内部killが外部文献より先に、かつ決定的に成立している**。

| # | kill経路 | 根拠 | 強さ |
|---|---|---|---|
| **K1** | **凍結 RISEI が既に定義・定理化している** | `Generalized_RISEI_Theory_EndToEnd_Certified_2026-07-23.tex` L271, L335, L345, L1238, L1441, L1484–85, L1565–67 | **決定的**（exact、egress不要、行番号で照合済み） |
| **K1b** | その具体化は既に還元済み | ガイド §6.4 第2行「平均に盲目な protocol-order fluctuation」→ tilted-GKSL/FCS、**早期kill**（最大誤差 `1.84×10⁻⁸`） | 決定的（記録済み） |
| **K2** | 外部：KD非正値性 ⟺ 一般化文脈依存性 | 族O、下記 §2 | 強（ただし §5 の監査限界つき） |
| **K2b** | 外部：観測依存エントロピーの粗視化順序定理 | 族O、下記 §3 | 強 |

**重要:** ガイド §6.1 で P1「Nonlinear functional hierarchy」枠が空いていたのは、
**未探索だからではなく、その内容を凍結理論が既に占有しているから**である。
ガイド §4.1 再利用規則3「**Frozen theoryの結論を新理論の新規性として数えない**」に直接抵触する。

---

## 1. K1 — 内部kill（決定的）

監査対象の命題候補はこうであった。

> 汎関数依存 valuation `ν_Φ` が汎関数階層上で離散的に飛び、その段差が protected cluster 構造からのみ決まる。
> 平均・線形応答では消え、work/QFI/noise でのみ現れる不可約機構。

これは**そのまま凍結 RISEI の中身**である。以下すべて凍結文書内に実在する（行番号は上記 tex）。

| 対象 | 凍結文書での位置 | 内容 |
|---|---|---|
| 汎関数依存 valuation | **L271 `def:valuation`** | `ν_Φ[R] = −lim_{Γ→∞} log Φ[R](Γ)/log Γ`（boxed 定義） |
| scaling signature | L283 `def:signature` | `Σ_π^(n) = (ν_max, ν_1, ν_pt, z_t, z_ω, m_log, …)` — **多成分の汎関数別指数** |
| 観測依存 protection depth | **L335 `def:protection-depth`** | `k_min^(n,Φ) = min{ |T| : ν_Φ[Ω_T^(n)] = 0 }`（boxed 定義） |
| **「平均に隠れ、揺らぎに見える」** | **L345** | `k_min^(1,pt) > k_min^(2,noise)` ——本文の地の文で *"a collective mechanism hidden in the mean becomes visible at lower intervention order in fluctuations"* と明記 |
| 汎関数階層の段差の**判定手続き** | **L1238 Gate G4** | *primary classification test* が `k_min^(1,Φ) ≠ k_min^(2,Φ)` |
| 非線形プローブの可視化次数 | Gate G5 | `m_min(S) = min{ m : χ_S^(m) ≠ 0 }` |
| 旧理論の回収 | L490 `cor:old-nu` | 固定周波数の点汎関数を選ぶと `ν_Φ` は旧スカラー指数 `ν` に落ちる |
| 位置づけの宣言 | **Abstract** | 除去した6仮定の一つが *"classification by a single pointwise exponent"* |
| ステータス表 | L1484–85 | 「Class: One exponent `ν` → **Functional-dependent valuation and scaling signature**」／「Protection depth: `k_min` → `k_min^(n,Φ)`」 |

つまり「単一の点指数による分類を捨て、汎関数ごとに valuation と保護深さを分ける」ことは、
**一般化 RISEI の看板の生成物そのもの**であり、しかも `k_min^(1,Φ) ≠ k_min^(2,Φ)` は
**探索すべき新現象ではなく、既に凍結されている判定ゲート（G4）**である。

### 1.1 前セッションの誤り（訂正）

前回の回答で「P1 Nonlinear functional hierarchy は空き枠であり、`ν_Φ`・`k_min^(n,Φ)` を土台にできるから有利」と述べたのは**逆**である。
土台にできること自体が、それが新規性になり得ないことを意味していた。**この推奨は撤回する。**

### 1.2 K1b — 具体化は既に還元されている

`k_min^(1,pt) > k_min^(2,noise)` の具体的な実現（平均では見えず二次累積量の順序依存分裂として現れる機構）は、
ガイド §6.4 第2行「**平均に盲目な protocol-order fluctuation**」として既に構成され、
**tilted-GKSL / FCS に最大誤差 `1.84×10⁻⁸` で再現されて早期killされている**（2026-07-23）。

すなわちこの方向は、抽象レベル（K1）でも具体レベル（K1b）でも、リポジトリ内で決着済みである。

---

## 2. K2 — 外部：Kirkwood–Dirac 準確率（族O-KD）

「観測の組み合わせでのみ信号が出る」の最も自然な外部定式化は、KD 準確率の非正値性である。ここは飽和している。

### 2.1 最強の脅威：KD非正値性 ⟺ 一般化文脈依存性

- **O01** *Kirkwood-Dirac representations beyond quantum states (and their relation to noncontextuality)*, arXiv `2405.04573` (2024)
- **O09** Schmid et al., *A structure theorem for generalized-noncontextual ontological models*, Quantum (2024-03-14)

KD 表現は状態だけでなくチャネル・測定を含む**全量子論の合成的表現**へ拡張され（functoriality・linearity・quasistochasticity を満たす）、
その**非正値性が一般化文脈依存性のシグネチャ**であることが示されている。
実正値な KD 表現の存在は非文脈的存在論模型の存在を含意する。

> **これはこのリポジトリで既に死んでいる場所に着地する。**
> ガイド §6.4 第1行「Response–Mechanism Contextuality」は **shared-ancilla enlargement へ早期kill**（2026-07-23）。
> 提案19（CIRT）§4 でも同じ FAIL が再現している。
> **KD 経由でこの方向へ入ると、リポジトリ内で2回死んでいる還元先へ自分から歩いて行くことになる。**

### 2.2 非古典性は「稀」ではなく「一般」

- **O02** *Almost no experiments have classical Kirkwood-Dirac representations*, arXiv `2405.17557` (2024)

KD古典性は非生成的（ほとんどすべての実験が非古典的 KD 表現を持つ）。
したがって「観測の組み合わせにしか出ない信号」を**稀な理論固有現象**として売ることはできない。
ガイド §3.2 の L3（新しい構造からのみ生じる）を主張する土台が消える。

### 2.3 資源理論・計量論のスロットも埋まっている

- **O03** Thio, Yang, Halpern, de Bièvre, Barnes, Arvidsson-Shukur, *Kirkwood-Dirac Nonpositivity is a Necessary Resource for Quantum Computing*, arXiv `2506.08092`, PRL (2025)
- **O04** Arvidsson-Shukur et al. (2020, 2023) — 後選択計量における KD 負値性 → Fisher 情報の優位。異常弱値による信号増幅

「平均では消えるが QFI では現れる」は**既に資源理論として定理化**されている。
ガイド §6.1 P1 の狙い文「mean/energy では消え、work/QFI/noise でのみ現れる不可約機構」は、
この文献群の記述と**目的語まで一致**する。

### 2.4 熱力学スロット（計画20 TPR への波及）

- **O05** *Quasiprobabilities in quantum thermodynamics and many-body systems*, arXiv `2403.17138`（総説）
- **O06** *Quasiprobability Thermodynamic Uncertainty Relation*, arXiv `2508.14354` (2025)

KD ベースの仕事分布は、コヒーレント／非可換なエネルギー揺らぎを捉え、
**その実部と虚部がエネルギー・エントロピーのトレードオフに直接効く**ことが総説水準で確立している。

> ⚠️ **これは族Oの副産物として計画20（TPR）への脅威でもある。**
> TPR の重心は §W4b の μ 軸（EP分離則）へ移されているが、
> 「保護応答の熱力学的価格表」を準確率の実部/虚部の言葉で書くと O05/O06 と衝突しうる。
> **TPR の既知最大脅威（housekeeping entropy production, Hatano–Sasa / Speck–Seifert）と併せて照合すること。**

---

## 3. K2b — 外部：観測依存エントロピー（族O-OE）

- **O07** Šafránek, Deutsch, Aguirre, *A brief introduction to observational entropy*, arXiv `2008.04409`, Found. Phys. (2021)
- **O08** *Observational entropy, coarse-grained states, and the Petz recovery map*, NJP (2023), DOI `10.1088/1367-2630/accd11`
- **O10** *Observational entropy with general quantum priors*, Quantum (2024-11-14)

粗視化（任意の quantum instrument / POVM）を指定して初めてエントロピーが定義される枠組み。
確立済みの中心定理は次の2つで、いずれも「観測の選択が答えを決める」構造を**既に定理として**与えている。

1. **細粒化に関する単調性** — 粗視化を細かくすると観測エントロピーは単調に変化する。粗いほど検出される散逸仕事は小さい。
2. **後処理単調性と十分性** — 出力統計に対する確率的後処理の下で単調非減少。
   ある粗視化の統計が別の粗視化から復元できるなら、その統計は**十分**である。

> **含意:** 「粗い観測では信号が消え、細かい／組み合わせた観測でのみ出る」という主張は、
> **粗視化の順序構造に関する既知の単調性定理と十分性判定に吸収される。**
> 「消える／出る」の境界を新現象として立てるには、**十分性が破れる**ことを示さねばならず、
> それは新しい主張ではなく O07/O08 の判定基準の適用結果になる。

---

## 4. 何が残るか（残余、優先度は低い）

正直に記録する。完全なゼロではないが、**提案を立てるに足りない。**

族Oの文献はすべて**状態・実験の非古典性**（KD）または**粗視化とエントロピーの順序**（OE）を扱っており、
**散逸極限 `Γ→∞` における汎関数別の漸近指数**そのものは扱っていない。その対象は RISEI 側の `ν_Φ` である。

しかしそれは K1 により凍結済みであり、残余は次の一点に縮む。

> 凍結 RISEI は `k_min^(n,Φ)` を**定義し、判定ゲート G4 として運用する**が、
> `k_min^(1,pt) > k_min^(2,noise)` を**強制する／禁じる定理は持たない**（L345 は例示であって定理ではない）。
> したがって「GKSL 構造から汎関数階層の段差を強制または禁止する分類定理」は形式的に空いている。

**それでも推奨しない理由:**

1. 具体化は K1b により既に FCS へ還元済み。同じ場所へ戻る公算が高い。
2. 「no-go 側」（GKSL では段差が生じない）に振れた場合でも、tilted-GKSL が同じ出力を出せば §1.2 降格条件
   「既存制御理論または Zeno 理論の標準計算で同じ出力が得られる」に該当する。
3. 仮に成立しても、それは凍結理論の**補題**であって新理論ではない。ガイド §4.1 規則3。

**もし将来これを拾うなら**、提案23（WPOT）の死因が直接効く（`docs/wpot-stage-a-report.md`）：

> `source ρ₀` と `readout E` を独立に選べる functional では、正値性は片側条件として降りない。
> witness を設計するなら**両側挟み込み**（`E` と `ρ₀` を KMS 内積で結ぶ）が必須。

汎関数階層の witness はまさに source と readout を独立に振る構造を持つため、
**この制約を初手で満たさない設計は着手前に死ぬ。**

---

## 5. 監査限界

**ガイド §10.3 および Pass 1–3 と同じ水準で、正直に記録する。**

- **本 Pass では文献の全文を1件も開けていない。** `arxiv.org/abs`・`/pdf`・`ar5iv`・
  `export.arxiv.org` API・Semantic Scholar API はいずれも **HTTP 403 / CONNECT tunnel failed** で拒否された。
  取得できたのは検索エンジン経由の書誌情報と要約スニペットのみである。
- したがって **O01–O10 の中心主張は「要約水準で確認」であり、定理の仮定・quantifier は未照合**である。
  DOI resolver 検証も未実施（Pass 3 と同じ未解消の制約）。
- **この限界は本 Pass の判定を弱めない。** 判定の重心は **K1（内部kill）**にあり、
  こちらは凍結 tex を行番号まで直接照合した exact な根拠で、egress を必要としない。
  外部文献（K2/K2b）は補強であって、単独の根拠ではない。
- 逆に言えば、**K2/K2b を根拠に他の方向を殺すことは、全文照合まで行わない限りしてはならない。**
- `references/references.bib` は本 Pass でも未更新（PDF 未取得のため）。索引は
  `docs/literature-master-table.csv` の族O行のみ。

---

## 6. 判定と反映先

**判定:** `内部kill（決定的） / 外部prior-art飽和 / 着手前に却下`

ガイド §6.6 に従い、同一コミットで以下を更新した。

1. `THEORY_PROPOSAL_GUIDE.md` §6.4（却下リスト）／ §6.1（P1 枠に注記）
2. `docs/context-pack.md` §5（同一表のミラー）
3. `docs/PROJECT_STATE.md`（決定済み事項）
4. `docs/literature-master-table.csv`（族O 10件を追加、計86件）

**提案番号は消費していない。** 提案文書を作成する前に死んだため、欠番は発生しない（ガイド §9 番号規約）。
