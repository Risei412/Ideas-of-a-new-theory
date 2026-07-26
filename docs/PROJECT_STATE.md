# プロジェクト現況（圧縮版）

**最終更新:** 2026-07-25 ／ 新規セッション・引き継ぎ用の1枚要約。詳細は各リンク先。

---

## 目的

**理論固有現象の発見** — その理論でしか出てこない現象と、その非還元性の論証。
既存理論の再整理は成果として数えない。投稿先想定は **PRX**。

## リポジトリ構成

| パス | 内容 |
|---|---|
| `THEORY_PROPOSAL_GUIDE.md` | **作業基準の本体**（約900行）。提案前に必読 |
| `Frozen-Theories/` | 確定理論3件（RISEI・SMRT・EIT）。書き換えない |
| `Blueprints-of-theories/` | 草案6件（DCIT・トロピカル付値異常・因果インターフェース・実現可能性錐・保護の熱力学・**凍結資源実現ギャップ(21)**） |
| `docs/context-pack.md` | **ChatGPTにアップロードする資料層**（命令は書かない） |
| `docs/redteam-instructions.md` | ChatGPTのカスタム指示欄に貼る（還元／文献／校正の3種） |
| `docs/claim-template.md` | 各チャットに貼る主張の雛形 |
| `docs/stage0-checklist.md` | Stage 0 準備チェックリスト |
| `docs/literature-audit-report.md` | **文献監査 Pass 1**（30件、競合族A–G） |
| `docs/literature-audit-addendum.md` | **文献監査 Pass 2**（26件、H compatibility / L 下界） |
| `docs/literature-audit-specification.md` | 監査の基準 |
| `docs/literature-master-table.csv` | 全56件の索引（threat level・decisive difference つき） |
| `docs/reduction-targets.md` | 族ごとの target object / kill test / survival certificate |
| `docs/p0-certificate-spec.md` | **P0の証明書仕様と実行順序**（ベクトル値判定・入れ子条件・7ステップ） |
| `docs/claims/` | Stage 1 の主張リスト（赤チーム投入用・中立記法） |
| `references/` | `references.bib` + `manifest.csv`（PDFは未取得、URL索引のみ） |
| `docs/source-material/` | 内部資料4件（RISEI改訂版PDF・競合監査tex・Tubeロードマップ・SMRTスモーク） |

## 検証工程（ガイド §11）

**ChatGPTは共著者でなく赤チーム。** 合意ではなく生き残りでフィルタする。

```
Stage 0 提案生成（Claude/Fable 5、未推敲）
  → 1 主張抽出 → 2 還元試行(ChatGPT) → 3 文献照合 → 4 数値検証 → 5 改訂/放棄
  → 還元が成功しなくなるまで反復 → 6 英文化（最後）
```

- 1チャット1主張／重要な主張は別チャットで3回／**1回でも還元成功なら死**
- 命令はカスタム指示欄、資料はプロジェクトファイル、主張は各チャット貼付

---

## 決定済み事項

**探索方針の転換（最重要）** — 現象を先に構成して後から還元監査する順序は非効率と判明。
**競合理論族の恒等式を先に固定 → それを破る構成を逆設計** する順序へ（ガイド §6.4末尾）。

**却下済み6候補**（2026-07-23 競合監査完了、再提案禁止 → ガイド §6.4）
shared ancilla / tilted-GKSL・FCS / compact-group synchronization / 構造化系同定 へ還元。
うち4件は**最終監査まで生き延びた「惜しかった」候補**で、死因はすべて
**pairwise relative-chart因子化 `G_ij=X_jX_i^{-1}` への還元**（ガイド §6.5）。
Tube calculus も固有現象とは判定されていないが、**棄却ではなく計算基盤として凍結**。

**生成を繰り返す際の運用ルール**（ガイド §6.6・§9・§11.2）
- 却下が出たら **ガイド §6.4／§6.5・`context-pack.md` §5・本ファイル を同一コミットで更新**
- **提案番号は再利用しない**（欠番＝1本死んだ記録）
- **held-out を提案間で使い回さない** — 分割するか seed を引き直し、対応を提案文書に記録

**仮定変更の予算**（ガイド §4.4）— 原則1つ、不可分な補助仮定含め最大2つ、3つ以上は不採用。
新規性は仮定を多く外したことでは評価しない。

**探索対象（ガイド §6.1、優先度順）**

| 優先 | 空白地帯 | 壊す仮定 |
|---|---|---|
| **P0** | Interface realizability | ideal cut primacy |
| **P0** | Resource-bounded mechanism separation | unrestricted representation criterion |
| P1 | Multiparameter scaling geometry ／ Exact-to-approximate kernel crossover ／ Nonlinear functional hierarchy | fixed scaling path ／ exact protected kernel ／ linear response functional |
| P2 | Nonsemisimple protected geometry ／ Bounded-memory extension | semisimple kernel ／ time-local Markovity |
| P3 | Strong-probe extension | weak-probe approximation |

**競合理論族6族＋解析的kill gate**（`context-pack.md` §6）— 予算を数値凍結済み。
標準監査 `m3-6, d1-3, k1-3, D1-4, μ1-2, P≤128` ／ 拡張 `m7-8, d4, k4, D5-6, μ3, P≤256`。

**文献監査56件完了**（2026-07-25、`docs/literature-audit-report.md` + `-addendum.md`、`references/`）
競合族A〜G＋H（compatibility）＋L（sample-complexity下界）に対応づけ済み。**prior-art killはないが、P0両方とも再定式化が必要:**
- **P0-1** — 「共通dilationが存在しない」は無制限なら常に構成可能。C-JOINT/I-JOINT/P-PROG/D-SHARED/R-BOUND のどれを問うか凍結が必要。前2者は既知のchannel/instrument compatibilityへ還元される公算大
- **P0-2** — 「低depth一致・高depth分裂」だけでは不十分（Huang 2016）。cancellation-protected例外集合＋凍結資源内の下界として定式化する
- **§6.5に記録した「depth-3へ移行すれば逃げられる」は誤り**。Duncan–Kileel 2025 の higher-order group synchronization が塞いでいる（訂正済み）
- 競合予算を5点修正（C族にhyperedge order `h=3,4` 追加ほか）— `context-pack.md` §6.2.1

**記号衝突13件**（ガイド §5.3）— `Ω` `K` `Q` `Ξ` `ν` `C` `M` `P` `A` `G` `S` `z` `q` が理論間で別物。
特に `D` は理論では damping operator だが競合予算では hidden dimension。`D_damp`/`D_hidden` と書き分ける。

**計算環境** — Python/NumPy/SciPy/SymPy/mpmath 可、**QuTiP・CVXPY・Mathematica 不可**。
GKSL simulationは custom Liouville 実装、symbolic は SymPy で代替。

---

## 未決事項

1. ~~ガイド §1.2 代替投稿先~~ — **2026-07-25完了**（PRX → PRX Quantum → PRL → PRA/PRB、降格条件6件つき）
2. **ガイド §7** — 競合論文表。文献56件は `docs/literature-master-table.csv` に索引済み。ガイド§7への転記は候補確定後（現時点はfamily-levelのため）
3. **`context-pack.md` §2・§3** — ガイド §4.1・§4.2 からの転記（機械的作業、Claude側で実行可）
4. **RISEI の正式名称** — 凍結文書内に展開がなく未確認
5. **紛失資料3件** — `risei_uniqueness_competitor_audit/REPORT.md` 他。ゴミ箱から復旧予定
   （統合texに主要結果は保存済み。seed・optimizer設定・失敗ログは復元不可）

## 次のアクション

**P0の証明書仕様と実行順序を確定した → `docs/p0-certificate-spec.md`。**

**P0 は単一の数値目標ではなくベクトル値判定。** 族ごとに固有の単位で証明書を立て、
各証明書は**入れ子**（calibration側で競合の存在を示し、full側で容量超過を示す）でなければならない。
**`P0-D の達成 ≠ P0 の達成`。**

**実行順序:**
1. ~~shot予算とprotocol数の整合性を修正~~ — **完了（凍結、下記）**
2. ~~理想データで到達可能な `σ₇` をスモーク~~ — **完了・判定 GO**
2bis. ~~認証対象を凍結予算で測れる部分行列へ移す~~ — **完了（2026-07-26、下記）**
3. P0-D用の6状態以下HMMをcalibration側に明示構成 ← **現在ここ**
4. full側のrank-7 minorをexact arithmeticで認証
5. 統計模型から `τ_H(α)` を導出
6. P0-D成立後、P0-A・P0-Eの明示構成へ（**SDPを使わず明示構成** — CVXPY不在のため）
7. P0-D単独なら**PRL型**、複数族を排除できたら**PRX型**へ戻す

**ステップ1の凍結結果（`p0-certificate-spec.md` §4.4–4.7）:**
- `1.2×10⁵` shots は **calibration 専用上限**。held-out は独立予算で最低 `1.28×10⁵`
- **protocol と measurement setting を分離計上。** `2000` shots は **1 setting あたりの上限**（一律値ではない）
- 出典の tree-scaling 表から、測定/edge が gauge次元 `q` に比例（q=3→7、q=8→18、permutation→4）と判明。
  **「7 measurements」は protocol 数ではなく setting 数**で確定
- 標準探索 `m=6`、`m=8` は予算拡張を要する stress test
- **上限が持つのは 1 setting/protocol のときだけ。** 2設定で1.5–1.8×超過。
  二段階配分（1000–2000 shots/setting）を守れるのは **settings ≤ 2** まで
- `scripts/budget_manifest.py` で全 protocol-setting pair を列挙（`docs/budget-manifest.csv`）

**ステップ2の結果（`p0-certificate-spec.md` §4ter）— 判定 GO:**
- Hankel は `43×43`（m=6, depth≤4語）、`H_cal` は `7×7` — 入れ子構造が自然に出る
- **要求水準を訂正:** 二項上界 `σ_entry ≤ 1/(2√n)` を使うと `2τ_H = 0.2933`（先の 0.544 は約1.9倍の過大評価だった）
- 正規化は **`‖M_u‖₂=1`（縮小写像・CPTP的）** を採用。スペクトル半径1は成分が1を超え非物理
- 入れ子条件 `det(H_cal)=0` を課すと σ₇ は約2.4倍落ちる（制約なし0.38 → 中央値0.162）
- **ランダム構成では届かない** — 合格率は1 settingで6.8%、2 settingで1.7%
- **最適化すればクリア** — 射影付き山登り120反復で 0.402 → **0.609**（settings≤4まで許容）
- → **ステップ3–4の構成は最適化して作ること。ランダム試行では失敗する**

**ステップ2bis の結果（`p0-certificate-spec.md` §4quater）— 認証対象を差し替え:**
- **43×43 Hankel は凍結予算で測れない。** 全成分に深さ4語 1296 個が要り、held-out 凍結値
  （深さ4を64 protocol）の **20.25倍**。§1 の prefix–suffix 閉包の警告の具体例
- **calibration の protocol 設計も Hankel の語構造と不一致だった**（深さ2を16/36しか測らず、
  Hankel が使わない深さ3に24 protocol を割いていた）
- → **認証対象を「行・列語がすべて長さ2の 8×8 部分行列 `H_wit` の `σ₇`」へ変更。**
  深さ4語がちょうど64個で凍結 held-out 予算と一致し、**予算変更は不要**
- → **calibration を「長さ2以下の全語＝43 protocol」へ引き直し**（深さ3を除外）。prefix–suffix 閉包が成立
- 実測（`scripts/minor7_smoke.py`）: `σ₇(H_wit) = 0.1934`（要求 `2τ_H(8) = 0.1265`、余裕 **1.53×**）。
  **交錯不等式により部分行列版は構成側に不利**（同点で `σ₇(H_full)=0.66–0.75`）、ランダム合格率は **0%**
- **確定予算（m=6）:** calibration 43 + held-out 64 = **107 protocol、214,000 shots**（1 setting）。
  settings=2 も可だが held-out が 1000 shots/setting となり余裕 1.08×。**標準は settings=1**
- 副次効果: 認証対象が exact minor 認証の対象と一致し、Hankel 成分間の相関問題も消えた

**提案21（Stage 0/1 完了）:** `Blueprints-of-theories/21_resource_bounded_mechanism_separation_proposal.md`、
主張リストは `docs/claims/21_claims.md`（5主張・計13チャット）。**次は Stage 2（赤チーム還元試行）**。

**共通の作業**（`literature-audit-report.md` §6）: 候補を固定する前に neutral notation で
calibration/held-out tensor を定義し、generalized Hankel matrix と temporal operator-Schmidt matrix を
exact arithmetic で構成する。

---

## 提案時の禁止事項（ガイド §9）

- 固有現象が書けていないのに「新理論」と称する
- 非還元性の検討を省略する
- 「証明できる見込み」を「証明済み」と書く
- 既存文書の主張を確認せずに引用する
