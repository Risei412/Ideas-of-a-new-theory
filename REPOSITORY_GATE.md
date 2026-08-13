# 専用リポジトリ作成ゲート

**最終更新:** 2026-08-12
**適用範囲:** この monorepo（`Risei412/Ideas-of-a-new-theory`）から理論を切り出して
GitHub 上に専用 repository を作るかどうかの判定。

---

## 0. 原則 — repository は一時的な作業場であって、理論の家ではない

**成熟は repository への入場条件ではなく、repository からの卒業条件である。**

現状がそれを示している。最も成熟した3理論（RISEI・SMRT・EIT）は
`Frozen-Theories/` に LaTeX で置かれており、**専用 repository を持っていない**。
一方 `Risei412/NV-EIT-space` は EIT の**決着していない反証作業**（Gate E、F5B/F5C）
のために存在する。凍結された定理は monorepo に、生きている反証作業は専用 repo に、
という分業が既に成立している。

したがって「理論が成熟したので repository を与える」という運びは採らない。
それをやると repository 数が理論数に比例して単調増加する。
**専用 repository は、反証作業が monorepo に収まらなくなったときにだけ切り、
決着したら畳んで monorepo へ帰す。**

判定は2段。**Gate A（科学）が通っても Gate B（分離の必要）が通らなければ作らない。**
その場合は monorepo 内のディレクトリ＋`research_state/summary.json` のまま続ける
（→ [`docs/research-state-convention.md`](docs/research-state-convention.md)）。

> 既存の2つの GO 証明書（`Fixed-Response-Operational-Synthesis/REPOSITORY_CREATION_GATE.md`、
> `NV-Blue-Charge-Control_seed_2026-08-11/TP16_bridge/repository_go_certificate.md`）は
> **どちらも Gate A しか判定していない。そして事実、どちらも repository になっていない**
> ——両方とも monorepo 内のディレクトリのままである。本ゲートはその実運用を明文化したもので、
> 遡って分割を認可するものではない。

---

## 1. Gate A — 科学的条件（既存2件の GO 証明書から抽出）

6項目すべて PASS を要する。1項目でも落ちれば作らない。

| # | 条件 | 意味 |
|---|---|---|
| **A1** | 内部吸収の先行実施 | 大規模計算に入る前に、手持ちの Theory Programs のどれかに吸収されないことを確認済み |
| **A2** | registry-clean な constraint residue | 広い主張は既に殺されており、**残差が具体的に一文で書ける** |
| **A3** | 中核削除テスト | 中核の構造を削除する操作が定義されている（例: TP-16 の `ΔH → 0`） |
| **A4** | 削除下で最安の帰結が壊れる | A3 の削除で、その理論の最も安い帰結が実際に消えることを確認済み |
| **A5** | 非空虚な falsification control | 「常に成立してしまう」ことを排除する負制御が存在する |
| **A6** | 明示的な non-claims | 新規と主張**しない**ものが列挙されている |

**A2 の判定基準:** 残差は「既知理論 A ＋ 既知理論 B」「パラメータ変更」「プラットフォーム変更」
「自然な一般化」であってはならない（Research CI Core の規則と同一）。

**Gate A は論文レベルの新規性証明ではない。** 両先例とも明記している——
「This GO authorizes development and falsification. It is not a manuscript-level
novelty certificate.」「This is not a final novelty PASS for publication.」
Gate A が言えるのは「隔離したコード・定理試行・新規性監査を割り当てる価値がある」までである。

---

## 2. Gate B — 分離の必要条件（増えすぎ防止の本体）

Gate A を通った候補にのみ適用する。**5項目すべてを満たさなければ、monorepo に残す。**

### B1 枠が空いているか

**専用 repository の枠は1つ。** これは美意識ではなく、Research CI の能力上限である。

- Research CI beta-0.2 仕様 §5 は「1 user = 1 active seed」を前提に設計されている
- `research_ci_get_context` が返す seed は現在 `nv-eit-sector-response` の1件のみで、
  読む GitHub repository も `Risei412/NV-EIT-space` の1つだけ

**したがって2つ目の専用 repository は、Research CI から見えない。**
問い生成の入力にも、重複検出の対象にもならない。

枠が埋まっている状態で新設するには、**どの理論が CI の視界から外れるかを
明示的に書いて枠を移譲する**こと。これは held-out seed の使い回し禁止と同じ規律で、
「黙って増やす」ことだけを禁じている。移譲先は Notion の Research Assets 行と
`summary.json.notion` に記録する。

### B2 計算基盤が独立しているか

monorepo の `scripts/` を継承する必要があるなら、**残す**。

具体例: LKCT の GKSL / superoperator 層は、新規に書く前に
`scripts/wpot_null_smoke.py:186` の `_thermal_gksl`（列スタック vectorization・
KMS 詳細釣合いレート規約・3種の非熱的負制御）を継承することが決まっている。
これを別 repository へ切ると規約が二重管理になり、負制御の定義がずれる。

### B3 独立した held-out 予算と seed が要るか

held-out を提案間で使い回さない規律（`PROJECT_STATE.md` の運用ルール）があるため、
新しい seed 番号と独立した shot 予算が必要になった時点で分離の理由になる。
逆に、monorepo の凍結予算（例: calibration 43 + held-out 64 = 107 protocol）を
共有したままでよいなら、分離の理由にならない。

### B4 共有の権威文書を巻き込まないか

**新しい器を作ると、ルートにある共有文書が一緒に動く事故が既に1回起きている。**

```
commit f6917b2 "Add a new throey-seed" (2026-08-11)
R100  THEORY_PROPOSAL_GUIDE.md → Fixed-Response-Operational-Synthesis/THEORY_PROPOSAL_GUIDE.md
```

monorepo の作業基準の本体（914行）が理論シードのディレクトリへ移動し、
`CLAUDE.md` と `docs/PROJECT_STATE.md` のリンクが切れた状態が約1日続いた（2026-08-12 に復旧）。

分割時は、移動対象に次が含まれていないことを確認する:
`THEORY_PROPOSAL_GUIDE.md` / `CLAUDE.md` / `REPOSITORY_GATE.md`（本ファイル） /
`docs/PROJECT_STATE.md` / `docs/research-state-convention.md` /
`docs/context-pack.md` / `docs/redteam-*.md` / `docs/claim-template.md` /
`docs/literature-*`（全理論共通の文献監査） / `references/`。

### B5 context 圧が実測で立っているか

`research_ci_get_context` の GitHub 状態はサイズ順に truncate される（重要度順ではない）。
実測値: `NV-EIT-space` は 702行中 348行のみ読み込まれ、Notion 側も 210行中 88行だった。

monorepo の `research_state/summary.json` 群を合わせても CI が読み切れているなら、
分離しても読める量は増えない——**むしろ B1 により、切った側が完全に見えなくなる。**
分離が context 圧の解決になるのは、**枠を移譲して切った側を active seed にする場合だけ**である。

---

## 3. 同居が既定（co-tenancy）

**複数の理論が1つの器を共有するのが既定で、分割は例外である。**

既に実践されている: `NV-Blue-Charge-Control_seed_2026-08-11/` は
**2つのプログラム**（DLA bridge の決定論的 Hamiltonian 幾何と、TP-16 の確率的
charge transcript / retry / completion コスト）を同居させ、
`theory/core_principles.md` に「Boundary between programmes」という節で
所有領域の境界を明記している。

同居させる条件:
- kill 条件を共有する、または
- 計算基盤（`scripts/`、GKSL 規約、held-out 予算）を共有する

分割してよいのは、**kill 条件が独立であることを示せた場合のみ**。
「概念的に別テーマだから」は分割の理由にならない。

---

## 4. 退役条件 — 枠を返す3つの経路

専用 repository は必ずどれかで終わる。終わらせずに放置しない。

| 経路 | 条件 | 処理 |
|---|---|---|
| **E1 決着** | 論文化、または no-go として確定 | 凍結成果物を monorepo の `Frozen-Theories/` へ戻し、repository を archive。**枠を返す** |
| **E2 停滞** | 直近の gate 結果から3ヶ月、新しい gate 判定が出ていない | monorepo のディレクトリへ差し戻す。資産（負制御・検定器）は `scripts/` へ回収。**枠を返す** |
| **E3 死** | 中心条件が反証された（例: 提案23 WPOT の WP1 反証） | `KILLED.md` に死因を記録し、**提案番号は欠番のまま再利用しない**。repository は archive。**枠を返す** |

E2 の3ヶ月は運用値であり、実績を見て調整してよい。判定の対象は
**コミット数ではなく gate 結果**である（コミットが続いていても gate が動いていなければ停滞）。

---

## 5. 作ってはいけない基準

以下は **repository を作る理由にならない**。

- **数学的・構造的に健全であること。**
  CIRT（提案19）は6つの停止条件のうち発火したのが「先行研究」1つだけで、
  「理論は数学的・構造的には健全で、失ったのは新規性だけ」と判定されたが、**降格した**。
  健全さは Gate A の A2（residue が registry-clean であること）を代替しない。
- **理論が重要／成熟していること。** §0 の通り、成熟は卒業条件である。
- **ファイル数が増えたこと、ディレクトリが見づらいこと。**
  それは `research_state/summary.json` と命名規約（`src/X.py → results/X_result.json`）で解く。
- **早すぎる作成。** 提案23（WPOT）は**作成同日に Stage A で中心条件 WP1 が反証され撤回**された。
  Gate A を通す前に器を作れば、1日で死ぬ repository ができる。
- **「いずれ論文になるから」。** 論文の artifact が要るのは投稿時であり、E1 で作れば足りる。

---

## 6. 手順

1. Gate A を判定し、証明書を候補ディレクトリ内に置く（下のテンプレート）
2. Gate B を判定する。**1つでも欠ければここで停止し、monorepo に残す**
3. B1 で枠を移譲する場合、どの理論が CI 非可視になるかを証明書に明記する
4. 分割を実行する場合、B4 のリストが移動対象に含まれていないことを確認する
5. Notion の **Research Assets** に新しい repository 行を作り、
   `Repository` / `Branch` / `Commit Hash` / `Canonical URL` を埋め、
   対応する Research Question / Theory Program へリレーションを張る
6. 新 repository の `research_state/summary.json` に Notion page id を書き戻す
7. Theory Program の `Repository Index` と `docs/PROJECT_STATE.md` を同一コミットで更新する

### 証明書テンプレート

```markdown
# Repository Gate — <理論名> — <YYYY-MM-DD>

## Verdict
GO / GO WITH CLAIM RESTRICTION / NO-GO (monorepo に残す)

## Gate A — 科学的条件
| # | 条件 | 判定 | 根拠 |
|---|---|---|---|
| A1 | 内部吸収の先行実施 | PASS/FAIL | 吸収を試した Theory Program 名 |
| A2 | registry-clean residue | PASS/FAIL | 残差を一文で |
| A3 | 中核削除の定義 | PASS/FAIL | 削除操作 |
| A4 | 削除下で最安の帰結が壊れる | PASS/FAIL | 帰結と壊れ方 |
| A5 | 非空虚な falsification control | PASS/FAIL | 負制御 |
| A6 | 明示的な non-claims | PASS/FAIL | 箇条書きへのリンク |

## Gate B — 分離の必要条件
| # | 条件 | 判定 | 根拠 |
|---|---|---|---|
| B1 | 枠が空いている / 移譲先を明記 | PASS/FAIL | 現 active seed と、CI 非可視になる理論名 |
| B2 | 計算基盤が独立 | PASS/FAIL | 継承が要る `scripts/` の有無 |
| B3 | 独立した held-out 予算 | PASS/FAIL | seed 番号と予算 |
| B4 | 共有権威文書を巻き込まない | PASS/FAIL | 移動対象の確認結果 |
| B5 | context 圧の実測 | PASS/FAIL | truncate の実測値 |

## 事前登録した退役条件
E1 決着: <何をもって決着とするか>
E2 停滞: <直近 gate 結果の日付＋3ヶ月>
E3 死: <中心条件と、その反証が何であるか>

## Explicit non-claims
- ...

## 明記事項
この GO は開発と反証の認可であり、manuscript-level の新規性証明ではない。
```
