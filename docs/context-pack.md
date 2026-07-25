# コンテキストパック（ChatGPTプロジェクトにアップロードする資料）

**このファイルは資料層である。命令を書かないこと**（命令は `redteam-instructions.md` → カスタム指示欄）。

**用途:** ChatGPTのプロジェクトに**ファイルとしてアップロード**する。
チャットごとに貼り直す必要はなく、更新時に差し替えるだけでよい。

**更新契機:** 新しい還元経路が見つかったとき／確定済み理論が増えたとき／記号を追加したとき。

---

> ⚠️ **現状このファイルは枠のみである。**
> 下の `TODO` は `THEORY_PROPOSAL_GUIDE.md` の §4・§5・§6.4 と対応しており、
> そちらが埋まった時点でここへ転記する。**埋まるまでアップロードしても効果は薄い。**

---

## 1. 記号・用語（→ ガイド §5）

| 記号 | 意味 | 備考 |
|---|---|---|
| *TODO* | | |

略称の展開:

| 略称 | 正式名称 |
|---|---|
| *TODO* | |

---

## 2. 前提として置かれている確定済み理論の適用範囲（→ ガイド §4.1）

新しい命題を判定する際、これらは**既に確立された事実として扱ってよい**。

| 理論 | 主結果 | 凍結された適用範囲（この外では保証されない） |
|---|---|---|
| RISEI | *TODO* | *TODO* |
| SMRT | *TODO* | *TODO* |
| EIT | *TODO* | *TODO* |

---

## 3. 抵触してはいけない制約（→ ガイド §4.2）

命題がこれらのいずれかを破る場合、**どの仮定を外したかが明示されていない限り、その命題は誤りである**。

- *TODO*（CPTP性、熱力学第二法則、既存no-go定理など）

---

## 4. 既知の還元先機構

赤チームが最低限検討すべき機構。**還元が成功するたびにここへ追記する。**

- Zeno効果 / Zeno narrowing
- 例外点（exceptional point, EP）
- Full counting statistics (FCS) / tilted-GKSL
- unravelling依存性
- 群同期（compact-group synchronization）
- 構造化系同定（structured state-space identification / controlled HMM）
- shared ancilla enlargement による説明
- bounded-memory process tensor
- 平均場近似の破れ
- 有限サイズ効果
- 対称性からの自明な帰結
- Riesz projector / Schur complement / Zeno型縮約 / 制御・realization理論の組合せ（Tube calculus regular branchの説明に使われた組）

---

## 5. 既に還元された（＝却下済みの）主張（→ ガイド §6.4）

**同じ経路の再探索を避けるために渡す。**
ただしリストにある機構へ無理に当てはめる偽陽性が増える副作用がある。
カスタム指示の「具体的な写像を数式で示せ」で潰す前提。判定が雑になったらこの節を外す。

出典：`docs/source-material/RISEI_Unique_Phenomena_Computation_Summary_and_Search_Strategy_2026-07-23.tex`（2026-07-23完了）。

| 主張 | 還元先 | 写像・極限操作 | 判定日 |
|---|---|---|---|
| Response–Mechanism Contextuality（reduced sector gluing obstruction） | shared ancilla enlargement | 共有ancillaを含む単一のcontext-independent additive GKSL模型への埋め込み | 2026-07-23 |
| 平均に盲目な protocol-order fluctuation | tilted-GKSL / FCS | standard tilted generatorでexact再現（最大誤差 \(1.84\times10^{-8}\)） | 2026-07-23 |
| Relative-gauge exact witness \(\Delta K_2=2\ell_Y(G-I)r_X\) | switched GKSL / FCSの代数 | write/relative-defect/read の三因子分解として導出可能 | 2026-07-23 |
| Continuous quantum gauge（\(SU(d)\) tree calibration atlas） | （非還元性未確立） | tree calibrationでの予測圧縮則が破綻。一般則としては不成立 | 2026-07-23 |
| Held-out quotient predictor | compact-group synchronization | 中立latent-frame estimatorと目的関数が完全一致（残差0） | 2026-07-23 |
| Global cycle-consistent quotient atlas（cycle threshold / abstention） | compact-group synchronization / 構造化系同定 | 予測値・fit residual・abstention判定が完全一致 | 2026-07-23 |
| Tube calculus（regular branch）全般 | Riesz理論 + Schur complement + Zeno型縮約 + 制御/realization理論 | 個別の再構成による説明可能性（凍結・保留、棄却ではない） | — |

> **探索順序の教訓：** 競合理論族を先に固定し、それが満たす恒等式・resource lower boundを先に抽出してから、
> それを破るwitnessを逆設計する順序に転換すること（現象を先に構成して後から還元監査する順序は非効率）。

---

## 6. 対象外（判定に持ち込まないもの）

- 投稿先の選定・新規性の価値判断（これは人間側の判断）
- 文章表現の良し悪し
