# プロジェクト現況（圧縮版）

**最終更新:** 2026-07-26 ／ 新規セッション・引き継ぎ用の1枚要約。詳細は各リンク先。

---

## 目的

**理論固有現象の発見** — その理論でしか出てこない現象と、その非還元性の論証。
既存理論の再整理は成果として数えない。投稿先想定は **PRX**。

## リポジトリ構成

| パス | 内容 |
|---|---|
| `THEORY_PROPOSAL_GUIDE.md` | **作業基準の本体**（約900行）。提案前に必読 |
| `Frozen-Theories/` | 確定理論3件（RISEI・SMRT・EIT）。書き換えない |
| `Blueprints-of-theories/` | 草案9件（DCIT・トロピカル付値異常・因果インターフェース(19, 🔻降格確定)・実現可能性錐・**保護の熱力学(計画20, TPR, ⚠️段階1監査済)**・凍結資源実現ギャップ(21)・分岐指数応答理論(22, RRT)・暗界面盲点理論(23, DIBT)・**持ち上げ核クロスオーバー理論(24, LKCT)**） |
| `docs/context-pack.md` | **ChatGPTにアップロードする資料層**（命令は書かない） |
| `docs/redteam-instructions.md` | ChatGPTのカスタム指示欄に貼る（還元／文献／校正の3種） |
| `docs/claim-template.md` | 各チャットに貼る主張の雛形 |
| `docs/redteam-packet-23.md` | 提案23（DIBT）Stage A 送付シート一式（A1/A2、シート1〜7） |
| `docs/stage0-checklist.md` | Stage 0 準備チェックリスト |
| `docs/literature-audit-report.md` | **文献監査 Pass 1**（30件、競合族A–G） |
| `docs/literature-audit-addendum.md` | **文献監査 Pass 2**（26件、H compatibility / L 下界） |
| `docs/literature-audit-specification.md` | 監査の基準 |
| `docs/literature-master-table.csv` | 全76件の索引（threat level・decisive difference つき）。**族N（受動実現可能性）20件を追加** |
| `docs/literature-audit-cirt-passive-realizability.md` | **文献監査 Pass 3**（族N・20件）。CIRT降格の根拠 |
| `docs/cirt-*.md`（5件） | **CIRT監査一式**（CG2／vacuousness／Edge iii／window honesty／CG3） |
| `scripts/cirt_gauge_audit.py` | CIRT検証の実装（T1–T8、負制御NC0–NC10、判定基準は実行前凍結） |
| `docs/reduction-targets.md` | 族ごとの target object / kill test / survival certificate |
| `docs/tpr-kill-plan.md` | **計画20（TPR）の生死判定手順 W1–W10 と投稿先決定フロー**（PRX8ゲート・降格条件6件に写す） |
| `docs/tpr-stage-a-report.md` | **計画20 段階1 内部還元監査の判定**（T1 の証明経路失効・T2 自己矛盾・T4 修復） |
| `scripts/tpr_thermo_audit.py` | 計画20 段階1 の実装（W1a–W4b、負制御2種、seed 20260728、判定に float 不使用） |
| `docs/p0-certificate-spec.md` | **P0の証明書仕様と実行順序**（ベクトル値判定・入れ子条件・7ステップ） |
| `docs/claims/` | Stage 1 の主張リスト（赤チーム投入用・中立記法） |
| `certificates/` | P0-D・LKCT・**TPR** の exact 証明書（有理数データ＋ゲート判定） |
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

**提案23（WPOT）撤回【2026-07-26、作成同日】** — Stage A で中心条件 WP1 を反証。
`docs/wpot-stage-a-report.md`。受動実現 400/400 試行が `Π_n` の半正定値性を破り、
**語なし 1×1 スカラーの時点で破れている**。死因は「source `ρ₀` と readout `E` が独立に選べる
functional では、受動性は片側正値性として語領域に降りない」という構造的性質。
**番号23は欠番。** 残す資産は機構的必要条件（両側挟み込みが必須）と検定器
`scripts/wpot_null_smoke.py`（負制御4モード）。
**CIRT C4（周波数領域の ancilla 閉性）とは矛盾しない** — 死んだのは周波数領域→語領域の写像。

**提案25（FHOT）撤回【2026-07-26、作成同日】** — Stage 0 内部監査で中心命題が VACUOUS と判定。
`scripts/fhot_smoke.py`（F0–F8）、`docs/fhot-stage0-internal-audit.md`。
最小模型で閉形式 `F_Q=4|χ|²/Σ_A`、`χ=D_A·g(Δ)` が残差0で成立し、`δχ_S≡0` は population差
`D_A` の不変性に、`δF_S≠0` は population和 `Σ_A` の変化に完全帰着、かつ `Σ_A=tr(ρΠ_A)` は
**線形汎関数**である。死因は「有限次元でトモグラフィが可能な設定では状態の任意の汎関数が
線形汎関数全体から決まるため、線形汎関数に盲目・非線形汎関数に可視という枠組み自体が
原理的に空」という構造的性質（先行研究照合ではなく自己内部監査で確定）。
分類予想（`r_nc>0` が必要条件）も `r_nc=0` かつ `δF_S≠0` の明示的反例で反証。
**番号25は欠番。** 残す資産は機構的必要条件（population正値性から
`ν(F_Q)<ν(χ) ⟺ ν(g)<ν(Σ_A)−ν(D_A)≤0`——QFI保護には probe coherence の減衰が消えることが
必要で population 再配分だけでは不可能）と検定器 `scripts/fhot_smoke.py`
（`scripts/` 初のGKSL superoperator層・SLD/QFIの2独立実装、提案24の次工程で再利用可）。
**ガイド §6.1 の空白地帯「P1 Nonlinear functional hierarchy」は再挑戦時、資源制限（P0-2）か
無限次元のどちらかを同時導入しない限り不可能という制約が判明した。**

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

## CIRT（提案19）— 監査完了・降格確定【2026-07-26】

**判定: 🔻 降格。** 新理論としては成立しない。多ポート量子デバイスの**較正診断ツール**として
PRApplied / PRA 水準。詳細は `Blueprints-of-theories/19_causal_interface_realizability_theory_proposal.md`
の冒頭ステータスヘッダ。**提案番号19は却下ではないので欠番にしない**（ガイド §9 の番号規約）。

**§9.1 の6停止条件のうち、発火したのは「先行研究」の1つだけ:**

| 停止条件 | 検証 | 結果 |
|---|---|---|
| 反例族が測度ゼロ／fine-tuning | T6 | 発火せず（可行幅36.6%） |
| C4が偽 | T8 | 発火せず（C4は真。ただし既知） |
| 行列条件が対角条件から自動的に従う | T5/T6 | 発火せず |
| 透明窓の理想化でマージン消失 | T7 | 発火せず（有効幅4桁） |
| ポート基底再定義／secular緩和で消失 | T3/T5 | 発火せず |
| **先行研究で同一の判定問題が既出** | **Pass 3** | **発火** ← これだけ |

**理論は数学的・構造的には健全で、失ったのは新規性だけである。**

**再提案禁止の中身（族N、`docs/literature-audit-cirt-passive-realizability.md`）:**
自己エネルギー↔インピーダンスの辞書で、次はすべて先行研究である。

- 因果的Loewner定理／Lamb shift の作用素反単調性 → **Löwner 1934**、多ポートFoster定理（Cauer 1931）
- $P_n$ 階層・「有限予算で反証可能・検証不能」 → Löwner 1934、Hansen–Ji–Tomiyama 2004
- 最小bathモード数 $=\mathrm{rank}\,L=$ McMillan次数 → **Youla–Saito 1967**（"minimum number of
  reactances"）、**Mayo–Antoulas 2007**（rank Loewner = McMillan次数）、退化行列Nevanlinna–Pick
- 有限判定・dual witness・全解パラメトリゼーション → Nevanlinna–Pick/Schur。
  **Fei–Yeh–Zgid–Gull, PRB 104, 165111 (2021)** が行列値で「solutions exist iff Pick matrix is PSD」を
  物理誌で述べ、`Nevanlinna.jl`/`TRIQS` に実装済み
- 「サンプル点の正値性≠受動性」 → passivity enforcement 分野の存在理由（Grivet-Talocia 2004 ほか）
- 自己エネルギー↔インピーダンス辞書そのもの → **Solgun–DiVincenzo 2015**（circuit QED の実用手法）
- ancilla閉性（C4） → 正実類のSchur補元閉性、Anderson & Vongpanitlerd 1973

**「quantum surplus」は量子効果ではない。** 成分ごとのKKが行列受動性を含意しないのは
古典多ポート受動性の定義そのもの。**この語を新現象の名として使わないこと。**

**残る最小の空白:** 「Bohr周波数の $(\gamma,S)$ データに対する行列境界Nevanlinna–Pick
実行可能性問題」という定式化のみ。方法論的寄与であり、新理論でも新現象でも新数学でもない。

**監査の限界（要再実行）:** egressポリシーにより **DOIのresolver検証が1件もできていない**
（arXiv:2604.17058 のみユーザー供給PDFで通読）。`references/references.bib` は未更新のまま。
egressが通る環境でDOI解決を再実行することが必須の残作業。

---

## 未決事項

1. ~~ガイド §1.2 代替投稿先~~ — **2026-07-25完了**（PRX → PRX Quantum → PRL → PRA/PRB、降格条件6件つき）
2. **ガイド §7** — 競合論文表。文献56件は `docs/literature-master-table.csv` に索引済み。ガイド§7への転記は候補確定後（現時点はfamily-levelのため）
3. ~~**`context-pack.md` §2・§3** — ガイド §4.1・§4.2 からの転記~~ — **2026-07-26 完了。
   `context-pack.md` は全節記入済みで ChatGPT プロジェクトへアップロード可能**
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
3. ~~P0-D用の6状態以下HMMをcalibration側に明示構成~~ — **完了（2026-07-26）**
4. ~~full側のrank-7 minorをexact arithmeticで認証~~ — **完了（2026-07-26）**
4bis. **有限shot余裕 (iii) が未達 → 判定方式の再設計** ← **現在ここ**
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

**ステップ3–4の結果（`p0-certificate-spec.md` §4quinquies）— exact 部分は成立、有限shotは未達:**
- **構成の骨格が改善した。** 全体を7状態 controlled sub-Markov 過程に取り、`p_7 = 0` かつ `f_u·b_0 = 0`
  とすると calibration 一致が**恒等式として**成立し、`rank(H_cal) ≤ 6` も自動。根探索が不要になった。
  非負の世界では `f_u·b_0 = 0` は台の disjoint 性と同値。`R(w) ∈ [0,1]` が全語で保証される
- **exact 認証 C1–C5 すべて PASS**（`certificates/p0d_certificate_2026-07-26.txt`）。
  真の6状態 sub-Markov 競合の存在・calibration 恒等式（43語）・`det(H_cal)=0`・非零 7×7 minor・確率性。
  **⇒ 中心命題の (i)(ii) は Conditional から Exact へ昇格**
- **⚠️ (iii) 有限shot余裕は未達。独立な2つの問題:**
  - **閾値の正規化が誤っていた（2倍緩い）。** `σ_entry ≤ 1/(2√n)` は `[0,1]` の割合の上界だが、
    採用した opnorm 正規化はレンジ幅2。正しくは `σ₇/レンジ幅 ≥ 2√N/√n`。
    **訂正するとステップ2は 1.04×（辛うじて）、ステップ2bis は 0.76× で FAIL**
  - **物理性（非負 substochastic）を課すとさらに落ちる。** 10⁴反復・8リスタート・台分割掃引で
    最良 0.0666（要求 0.1265 の **0.53倍**）、有理化後 0.0536（0.42倍）
- **構造的な理由:** 入れ子条件 `f_u·b_0 = 0` が隠れ状態の1段励起を禁じるため、第7方向は
  2段の substochastic 減衰を受け、他の6方向より構造的に小さい。
  **入れ子条件と有限shot余裕は反発する**（最適化の失敗ではない）
- **選択肢:** (a) shot を 3.6倍（7,215/setting）／(b) 安全係数を2→1（余裕ゼロ）／
  **(c) 判定を作用素ノルム＋Weyl から統計的検定へ置換（本命）**／(d) (iii) を落とす（新規性が消える）
- stop condition (1) は発火したが、失敗しているのは**判定方式**であって現象ではないため、
  撤回ではなく縮小・再設計とする。(c) を試してなお届かなければ撤回

**提案21（Stage 0/1 完了）:** `Blueprints-of-theories/21_resource_bounded_mechanism_separation_proposal.md`、
主張リストは `docs/claims/21_claims.md`（5主張・計13チャット）。
**主張1（入れ子構成の存在）は構成的に証明済み** — Stage 2 では真偽ではなく
「既知の構成に還元されるか」を問う。主張1のブロックは証明済みの内容（全体が7状態確率モデル）へ差し替えた。
**主張4 は否定的決着によりキューから除外**（判定方式の再設計後に立て直す）。

**Stage 2 は投入可能な状態になった**（`docs/claims/21_claims.md` §0.5 に実行手順）。
命令は `redteam-instructions.md` §A をカスタム指示欄へ、資料は `context-pack.md` をアップロード、
検証対象は §2 の枠内のみを各チャットに貼る。**主張3 → 1 → 2 → 5 の順に各3チャット、計12チャット。**

> **Stage 2 は Claude では代行できない**（ガイド §11.0 の役割非対称性）。別モデル・別セッションで実行する。

**提案22（RRT・分岐指数応答理論）— Stage 0 のみ完了、赤チーム未投入:**
`Blueprints-of-theories/22_ramification_response_theory_proposal.md`。
自己評価は **L2**（既存枠組みでは自然に出ないが原理的には導出可能）。**L3 を主張していない。**
理論固有性の最大の脅威は例外点(EP)／Lidskii摂動論への還元（§5.1 A1）。
未通過のため現時点で**PRX候補ではない**。判定は「還元リスク高。ただし kill test が短距離で実行可能」。

**提案23（DIBT・暗界面盲点理論）— Stage A 送付パケット準備完了:**
`Blueprints-of-theories/23_dark_interface_blindness_theory_proposal.md`、
送付シートは `docs/redteam-packet-23.md`（シート1〜7、A1: シート1-3・6、A2: シート4-5、文献調査: シート7）。
**PRX候補として探索する価値がある**と自己評価。送付順序はシート1→4→5を先行させ、
このうちどれかが「還元成功」なら stop condition（同文書§4）を適用してから残りを回す。
**まだ実際の赤チーム投入（Stage 2）は行われていない。**

**提案24（LKCT・持ち上げ核クロスオーバー理論）— A2内部監査完了・⚠️判断待ち【2026-07-26】**
`Blueprints-of-theories/24_lifted_kernel_crossover_theory_proposal.md`。
ガイド §6.1 **P1「Exact-to-approximate kernel crossover」**（壊す仮定: exact protected kernel）を
占有する初の草案。固有現象は**保護回復稜線**（核持ち上げ補正と Schur 漏洩補正が
`Γ²ε = α_leak/κ_lift` 上で相殺）と**稜線二分律**（`sign(κ_lift·α_leak)` による二分）。

**A2 内部監査（exact arithmetic、`scripts/lkct_exact_audit.py` X0–X6 全PASS、
判定に浮動小数点不使用、証明書 `certificates/lkct_fan_blindness_2026-07-26.txt`、
評価 `docs/lkct-fan-blindness-exact-audit.md`）の結果は両面である。**

- **🆙 得たもの:** **C1・C2 が Conditional → Exact へ昇格。**
  2-jet は近似ではなく**厳密 Schur 還元恒等式**`R = p_P†S(u,v)^{-1}c_P` の解析的 Taylor 展開
  （残差厳密に 0）。稜線は陰関数定理により**厳密な解析曲線**として存在し、
  物理域へ入る条件が `sign(κ_lift·α_leak)=+1` と同値であることが証明された。
  Sturm 法による厳密根計数で錐内一意性と符号反転を認証、2-jet 予測との相対差は
  `2.67e-3 → 2.68e-5`（1 decade あたり厳密に 1/10）。
- **⚠️ 失ったもの:** **C3（fan 盲目性）の広い版は否定。stop condition 1 が文字通りの読みで発火。**
  Newton 指数台も `ν(θ)` も ± 対で完全一致する（＝非署名トロピカル化には確かに不可視）が、
  **差は角 θ=2 の initial form `−e₀κ_lift+α_leak` の根の符号にすべて集約される。**
  initial form は標準的な係数付きトロピカル対象であり、**符号付き／実トロピカル幾何**
  （Viro patchworking 等）が正面から扱う層に落ちる。
  **「fan に盲目だから固有」という新規性の論法は使えない。**
- 副産物: `ν(θ) = clamp(θ−1,0,1)` で**折れ点は2個**（θ=1 と θ=2）と判明し本文を訂正。
  二分律の頻度は厳密有理数で **27/54 = 1/2**（float の 48.8% と整合）。

**→ (b) 縮小継続を選択（2026-07-26）。** 新規性の重心を
**「GKSL 物理クラス内で `sign(Φ(κ_lift)·Φ(α_leak))=+1` が実現可能か」という分類問題**へ移した。
**stop condition 2 を再定義**——実現不能なら撤回ではなく **no-go 定理**
「完全正値性は保護回復を禁じる」として論文化する（§2 型(B)、§1.2「鋭い一法則→PRL」）。
**投稿先は二段構え**：実現可能 → 分類＋実験提案で **PRA**／CPTP no-go → **PRL**。
**PRX は現時点で不可**（§1.1 ゲート8項目中 Novelty 不合格、§1.2 降格条件
「experimental pullback ができず抽象 parameter のまま」に該当）。

**Step 0 実余次元監査 完了（`docs/lkct-codimension-reality-audit.md`、
`scripts/lkct_codim_audit.py` Y0–Y7 全PASS、seed 20260727、判定に float 不使用、
証明書 `certificates/lkct_codimension_2026-07-26.txt`）— 初版の誤りを1件発見し、現象が豊かになった:**

- **⚠️ 初版 §0 の boxed 命題は誤りだった。** 物理応答は複素であり、`R → R_∞` の完全復元は
  実2次元 `(Γ,ε)` 平面で **余次元2（孤立点）**（`det J = Im(κ·conj α) ≠ 0`、rank 2）。
  曲線としての主張はガイド §4.2 no-go 9 違反・§8 既指摘弱点「codimension-one の普遍化」の再発。
- **✅ 汎関数を宣言すれば余次元1で生き残る。** `Φ ∈ {Re, Im}` で `rank_ℝ = 1`、
  存在条件 `sign(Φ(κ)·Φ(α))=+1` は**開条件**（ランダム40例で存在率 Im 3/5・Re 2/5）。
  Sturm 法で存在側は錐内1根＋符号反転、相対差 `−3.16e-3 → −3.15e-5`（1/Γ）、非存在側は0根。
- **🆕 稜線対の分裂を発見。** 分散稜線と吸収稜線が別位置に分裂し、分裂幅は閉形式
  `Δ_split = Im(κ·conj α)/[Re(κ)·Im(κ)]`。**分裂ゼロの条件は完全復元の余次元2条件と厳密に一致。**
  観測量が1つから**3つ**（2本の位置＋分裂幅）へ増え、EIT では透過と位相シフトが
  **異なる `Γ·γ₁₂` で回復する**という強い実験予言になった。
- **⚠️ Step 3 の「CPTP 符号強制」先読みは撤回。** `κ_lift = c_P†B_PP⁻¹(D_L)_PP B_PP⁻¹c_P` は
  `B_PP⁻¹` が2回現れる**双線型形式**で sesquilinear ではないため符号は強制されない
  （自己応答30例中 `κ_lift` 非実 30件・`Re κ_lift<0` 16件）。
  **no-go 分岐（PRL）の公算は下がり、実現可能分岐（PRA）の公算が上がった。**
  ただし線形代数レベルの反例であり、GKSL 由来の `B_PP` の追加構造は未検証。
- **RISEI 内部重複の精査:** 提案24 は生き残るが、**`Γ_× ∝ ε^{-1/2}` は RISEI L.990 に既出**
  （`z_jet`・`γ_phys=γ_0+εΓ`・`Γ²ε` の組み合わせも既出）。§4.1 に自白を追記した。
  生きている差分は5点（resolvent 閉形式／複素・符号つき係数／符号二分律／厳密零曲線／
  切片の閉形式盲予測）。**RISEI はステータス表 L.1616 で `Positive κ_eff, α_eff` を
  適用条件として宣言しており、本提案はその除外レジームを占有する位置づけ。**

**次工程:** (1) 符号付き／実トロピカル幾何の文献監査（**未実施・egress 必要**）、
(2) **GKSL 物理実現の系統探索**（現在の新規性の重心。出発点は SMRT `prop:phase-h` の
4準位 GKSL `D=diag(0,0,1/2)` と EIT §9.2 の Λ系）、(3) 赤チーム Stage 1–2。
**superoperator 層は新規に書く必要がある。**
ただし「`scripts/` に GKSL/Liouvillian 実装は存在せず」は**訂正**（2026-07-26）：
`scripts/wpot_null_smoke.py:186` の `_thermal_gksl` が列スタック vectorization・
KMS 詳細釣合いレート規約・3種の非熱的負制御（inverted/gain/negweight）を実装済みで、
`gibbs()`・`_kraus_to_super()` も揃っている。**新規に書く前にこの規約を継承すること。**

---

## 計画20（TPR・保護応答の熱力学）— 段階1 内部還元監査 完了・⚠️判断待ち【2026-07-26】

`Blueprints-of-theories/plan20_thermodynamics_of_protection_proposal.md`。
2026-07-24 のアップロード以来 §11 ループに未投入だったが、**内部還元監査を実施した。**
手順 `docs/tpr-kill-plan.md`、判定 `docs/tpr-stage-a-report.md`、
実装 `scripts/tpr_thermo_audit.py`（seed 20260728、W1a–W4b 全9ゲート PASS、判定に float 不使用）、
証明書 `certificates/tpr_reduction_2026-07-26.txt`。

**判定: 撤回ではない。ただし中心の2定理 T1・T2 は中心命題の座を失った。
現時点で PRX 候補ではない**（§1.1 ゲート8項目中 Novelty・Theoretical closure が不合格）。

- **⚠️ T1 の証明経路が失効。** 提案は「`ass:singular` の非自明核仮定は有限温度 Davies では
  満たせない」と書くが、`ass:singular` は `0∉spec D_j` の場合を**明示的に許容**する。
  正しい機構は**減衰床補題** `Λ_j = ½(Γ_out(j)+Γ_out(1))`（凍結の `prop:phase-n`・`prop:phase-h` の
  `D` を厳密再現）で、有限温度の逆過程が応答ブロック全体に一律の減衰床を敷く。
  そこから先は **T1(a) = 赤線5 の系、T1(c) = 赤線7 の系**。新規なのは辞書
  `ε=½e^{−βΔ}`・**持ち上げ行列 = 恒等行列**のみ。
- **⚠️ 仮定 (E3) が load-bearing。** 斜交 Riesz 射影を許すと有限温度でも Class III が成立する
  明示反例を構成（負制御で直交射影では消えることを確認）。提案は (E3) を装飾扱いしている。
- **⚠️ T2 は自己矛盾。** `ass:singular` より `Ran P = Ker D` なので `R_{S,0}` の担い手は
  Γ スケールで減衰しない。「Γ位相緩和が `c_⊥` を破壊し再生成電流が要る」という導出は
  設定と両立しない。**Conditional ですらなく Conjecture。**
- **🆙 T4 は修復可能。** `σ = σ_bath + σ_cut` と分離すれば `σ_bath` は `ass:bivariate` を満たし
  `thm:polyhedral-selection` を継承できる。log 補正は `σ_cut`（＝T7 の対象）のみ。
  **提案 §6 Stop条件4 はこの分離で先回り解消される。**
- **🆕 μ の起源が変わる。** 2準位2浴の厳密解で `μ=0 ⟺ Γスケール浴が詳細釣合い`
  （単一温度なら `σ≡0` が全 Γ で厳密）。T3 の言う「dark 支持か否か」ではない。
  ただし保護ブロック上での判定は段階2（W6）の課題。
- **T1(c) と提案24 LKCT は重複しない。** 融解端 `ε^{−1}` と LKCT 稜線 `ε^{−1/2}` は別スケール（厳密確認）。
  **提案24 への寄与:** 熱的切片は `D_L = I` なので LKCT の `κ_lift` が `c_P†B_PP^{-2}c_P` に確定する。
- **📌 §10「参照ファイル一覧（実在確認済み）」は 8件中6件が偽。**
  `Theorem and proofs/` `PhaseH/` `PhaseN/` `PhaseM/` `RoomT/` `results/` は一度もコミットされていない。
  Gate P1 はモデル逆解きが要り、**P6・T6 は突合先が存在しない**。`prop:phase-n` のみ即実行可。
  §0 の「熱力学0件」全域監査も提案19・23 の着地以降は失効。

**推奨は (b) 縮小継続** — 重心を **T7 ＋ μ軸（EP分離則）** へ移し、T1 を辞書へ格下げ、T2 を撤回。
投稿先は **PRA**（切断の熱力学的価格表）。

**次工程（最優先）:** **housekeeping entropy production（Hatano–Sasa / Speck–Seifert 系）との文献照合。**
W4b の μ 軸がこれに還元されれば新規性が消える。**現時点の最大の脅威で、egress が要る。**
その判定が出るまで PRX/PRL を名乗らない。次いで W6（三分岐の構造判定）、W10（T7 単独路線）。

**提案25（FHOT）— 撤回済み【2026-07-26、作成同日】。詳細は「決定済み事項」の該当項目を参照。**
文書は `Blueprints-of-theories/25_functional_hierarchy_obstruction_theory_proposal.md` に
撤回の監査結果つきで残す（欠番、削除しない）。残す資産と一般教訓は上記「決定済み事項」参照。

> **番号規約の訂正（2026-07-26）：** RRTは当初「提案21」を名乗っていたが、
> 番号21は`21_resource_bounded_mechanism_separation_proposal.md`（FRRG）が先に占有しており、
> ガイド§9の「番号は重複させない」に反する重複だった。RRTを**22**、DIBTを**23**へ繰り上げて解消した
> （ファイル名・文書内自己参照・`docs/redteam-packet-22.md`→`-23.md`・関連スクリプトのコメントを含め一括修正）。

**共通の作業**（`literature-audit-report.md` §6）: 候補を固定する前に neutral notation で
calibration/held-out tensor を定義し、generalized Hankel matrix と temporal operator-Schmidt matrix を
exact arithmetic で構成する。

---

## 提案時の禁止事項（ガイド §9）

- 固有現象が書けていないのに「新理論」と称する
- 非還元性の検討を省略する
- 「証明できる見込み」を「証明済み」と書く
- 既存文書の主張を確認せずに引用する
