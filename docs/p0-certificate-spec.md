# P0 証明書仕様

**確定日:** 2026-07-25
**対象:** ガイド §6.1 の P0（Interface realizability / Resource-bounded mechanism separation）
**根拠:** `literature-audit-report.md`（30件）・`literature-audit-addendum.md`（26件）・`reduction-targets.md`

---

## 0. 原則

**P0 は単一の数値目標ではない。族ごとの証明書のベクトル値判定である。**

`rank > 6` / `χ > 36` / hyperedge order `> 4` の三択にしてはならない。
同じ数値「6」でも族ごとに意味する資源が異なるため、**その族固有の単位**で立てる必要がある。

| 競合族 | 凍結資源 | 排除に必要な証明書 |
|---|---|---|
| D-classical | 古典状態数 `D_cl ≤ 6` | classical Hankel rank `> 6` |
| A-hidden GKSL | hidden Hilbert次元 `D_hidden ≤ 6` | `dim K > (d·D_hidden)²`（qubitなら **> 144**） |
| E-process tensor | memory bond dimension `χ ≤ 36` | temporal-cut operator Schmidt rank `> 36` |
| DQ-QHMM | quantum memory次元 `D_q ≤ 6` | QHMM固有の次元下界（定義依存） |
| C-synchronization | hyperedge order `≤ 4` | irreducible order `> 4`（**独立gate。他族を排除しない**） |

系が qubit なら族Aの上限は `(2·6)² = 144`。**スカラー Hankel rank を族Aへ流用してはならない** —
より自然には reachable-observable space そのものについて `dim K > 144` を認証する。
族Eの operator Schmidt rank も別の flattening・別の minor・別の摂動評価を要する。

---

## 1. 各証明書は「入れ子」でなければならない

**平坦な容量超過だけでは、「低容量モデルには最初から表現不能な過程を選んだ」という自明な勝利になる。**
matched-pair の物語が成立しない。

さらに重要な点として、**容量の上界は競合の存在を保証しない。**
有限 Hankel rank `≤ 6` が直接保証するのは6次元以下の**線形／quasi-HMM**実現であり、
確率非負性を持つ古典 HMM の存在には追加の実現可能性条件が要る。
**この非対称性は全族に共通する** — CP/TP・comb条件・positivity はいずれも次元の線形勘定では出ない。

| 証明書 | calibration側（**存在**を示す） | full側（容量超過を示す） |
|---|---|---|
| **P0-D** | `∃` 6状態以下の古典HMM。明示構成 or 非負性feasibility（LP） | `rank H_{C∪T} ≥ 7` |
| **P0-A** | `∃` `D_hidden≤6` の**GKSL-admissible** dilation（CP/TP・積初期状態・ancilla readout禁止込み） | `dim K_full > (d·D_hidden)²` |
| **P0-E** | `∃` `χ≤36` の**妥当な** process tensor（comb条件・positivity込み） | `OSR_c(Υ_full) ≥ 37` |
| **P0-DQ** | `∃` `D_q≤6` の QHMM（**定義を先に固定**） | 定義固有の spectral／factorization invariant |
| **P0-C** | order `≤ 4` で calibration が合う | irreducible order `> 4` |

**P0-D の厳密形:**

```
∃ M_D,  D_cl ≤ 6 :  P_{M_D}(w) = P_*(w)  ∀w ∈ C
                     rank H_{C∪T} ≥ 7
```

第一行が「calibration に本当に適合する競合が存在する」、第二行が「full data には適合不可能」を保証する。

> ⚠️ **Hankel 部分行列の prefix–suffix 閉包に注意。**
> calibration と held-out から作る行・列集合は、正しい prefix–suffix 構造を持つよう設計すること。
> 単にデータ点を表形式で切り分けるだけでは Hankel 部分行列にならない。

### QHMM の閾値を安易に書かないこと

Hilbert次元 `D_q` の量子モデルは演算子空間に `D_q²` 程度の線形自由度を持つため、
粗い排除条件は `rank H > D_q²`（`D_q≤6` なら `> 36`）が候補になる。
**しかしこれは QHMM の instrument構造・stationarity・pure/mixed memory・出力規約に依存する。**

classical Hankel rank ／ PSD-rank・quantum factorization dimension ／ spectral invariant ／
quantum memory cost を**分離**し、D05（Riechers–Elliott, arXiv:2509.03004）と
D06（Zonnios, arXiv:2412.12812）が実際にどの QHMM 定義へ下界を与えるかを固定してから閾値を書く。
単純に `> 6` や `> 36` と書くのは危険。

---

## 2. ノイズ頑健版

族Dについて、観測誤差による行列摂動を `‖ΔH‖₂ ≤ τ_H` と抑えれば、Weyl の不等式から

```
σ_7(H_full + ΔH) ≥ σ_7(H_full) − τ_H > 0
```

となり、`rank ≥ 7` がノイズ下でも維持される。**判定条件は `σ_7(H_full) > τ_H(α)`。**

族Eには `σ_37` を operator-Schmidt flattening に対して、
族Aには reachable-observable map に対して、**それぞれ別に**定義する必要がある。

**τ_H の目安（要確認）:** 2000 shots/protocol、成分あたり統計誤差 `≈ 1/√2000 ≈ 0.022`。
`30×30` 程度の Hankel 行列なら、ランダム行列の評価で `‖ΔH‖₂ ≈ (√m+√n)·σ_entry ≈ 0.24`。
（Frobenius 評価 `√(mn)·σ_entry ≈ 0.67` は緩すぎる）
**σ₇ がこの水準を超えられるかは、構成前にスモークで確認する。**

---

## 3. 実行順序

| # | 作業 | 完了条件 |
|---|---|---|
| **1** | **shot予算とprotocol数の整合性を修正する** | 下記 §4 の不整合を解消し、凍結値を更新 |
| **2** | 理想データで到達可能な `σ₇` をスモークする | ノイズなしで `σ₇` の到達水準を測定 |
| **3** | P0-D用の6状態以下HMMを calibration 側に**明示構成**する | 非負性・正規化を満たす具体的な `M_D` |
| **4** | full側の rank-7 minor を exact arithmetic で認証する | SymPy で非零 7×7 minor |
| **5** | 統計模型から `τ_H(α)` を導出する | 有意水準 `α` 付きの閾値 |
| **6** | P0-D成立後、P0-A・P0-E の明示構成へ進む | 各族の入れ子証明書 |
| **7** | 投稿先を判定 | P0-D単独 → **PRL型** ／ 複数族排除 → **PRX型** |

### 順序に関する注記

- **ステップ2を3より先に置くのが要点。** σ₇ が理想データでも小さいと分かってから設計をやり直すのが最も高くつく。総shot上限は凍結値なので後から緩められない
- **ステップ6で SDP を使わない。** 計算環境に CVXPY・Mathematica がないため、族A・Eの calibration 側は
  feasibility を解くのではなく**明示構成**で示す。matched pair は自分で設計するので構成可能なはずであり、
  環境制約を受けず証明書としても強い
- **ステップ7の分岐は §1.2 の降格条件に対応する。** P0-D単独では族Aが排除されていないため、
  監査の「維持できない表現」の「hidden ancillaを入れれば説明できるが大きい（最小次元の証明なし）」に該当する。
  主張は「**次数6以下の古典・線形実現は存在しない**」という狭い形になり、PRX ではなく PRL 形が妥当

---

## 4. ステップ1で解消すべき不整合【2026-07-25 検算済み】

凍結値：`2000 shots/protocol`、`calibration総上限 1.2×10⁵ shots` → **最大60 protocols**。

### 4.1 calibration 側は収まる（ただし余裕は小さい）

| m | depth1 | depth2 edge | depth2 protocol | depth3 | 計 | shots | 判定 |
|---:|---:|---:|---:|---:|---:|---:|---|
| 3 | 3 | 3 | 6 | 24 | 33 | 66,000 | OK |
| 4 | 4 | 5 | 10 | 24 | 38 | 76,000 | OK |
| 6 | 6 | 8 | 16 | 24 | 46 | 92,000 | OK |
| 8 | 8 | 11 | 22 | 24 | 54 | 108,000 | OK（余裕12,000） |

（depth2 は連結グラフ `ρ=1.5` → `⌈1.5(m−1)⌉` edge、両順序で2倍）

### 4.2 ⚠️ held-out 側の shot 予算が存在しない【本体】

| m | depth2未使用 | depth3未使用 | depth4固定 | 全held-out shots |
|---:|---:|---:|---:|---:|
| 6 | 14 | 96 | 64 | 348,000 |
| 8 | 34 | 312 | 64 | 820,000 |

**depth-4 の64 protocol だけで 128,000 shots となり、calibration 総上限 `1.2×10⁵` を単独で超える。**
m=8 の全held-out は calibration 予算の約7倍。

`1.2×10⁵` が calibration 専用なのか総予算なのかが未定義であり、
held-out 検証のコストがどこにも計上されていない。

### 4.3 「両順序測定」の解釈が未確定

上表は「1 edge あたり2 protocol（両順序）」で計算している。
しかし出典 `.tex` の `SU(d)` gauge fitting では **1 edge あたり7 measurements**（`7(m−1)` calibration）だった。
この規約なら m=8 で depth2 だけで `11×7 = 77` protocol、合計109 protocol = **218,000 shots** となり
calibration 単独で上限を82%超過する。

### 4.4 ステップ1の決定事項

1. `1.2×10⁵` は **calibration専用か総予算か**
2. **held-out 検証の shot 予算**をいくつにするか（depth-4 の64 protocol は必須）
3. 「両順序測定」は **1 edge あたり2 protocol か、複数測定設定か**
4. 上記を踏まえ `shots/protocol` を下げるか、`m` の標準監査上限を下げるか、総予算を上げるか

**τ_H(α) はここで決まる shots/protocol に直接依存するため、ステップ5より前に確定させる必要がある。**

---

## 5. 到達点の呼称

**P0-D の達成は P0 全体の達成ではない。** 提案文書・要約・コミットメッセージで区別すること。

- `P0-D 達成` — 次数6以下の古典・線形実現を排除した
- `P0 達成` — 凍結資源内の**全族**（D・A・E・DQ）を排除した
