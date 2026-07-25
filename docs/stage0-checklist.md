# Stage 0 準備チェックリスト

Fable 5 による理論提案生成（Stage 0）に向けて必要な資料と、ChatGPT側（還元・文献調査）に渡すもの・依頼事項をまとめる。
資料が揃うたびにチェックしていく運用とする。

---

## A. Stage 0（Claude / Fable 5 提案生成）に必要な資料

### A-1. 競合理論族の定義と資源予算 【必須・最重要】

`docs/source-material/RISEI_Unique_Phenomena_Computation_Summary_and_Search_Strategy_2026-07-23.tex` の Priority 0 に列挙された6族について、それぞれの予算を数値で固定する。

- [ ] enlarged GKSL with hidden ancilla → `D_hidden` の上限
- [ ] tilted-GKSL / full counting statistics
- [ ] compact-group synchronization
- [ ] controlled HMM / structured state-space identification
- [ ] bounded-memory process-tensor model → memory dimension、memory depth `μ` の上限
- [ ] active experimental design baseline
- [ ] 上記6族で確定か、追加・削除があるか

固定が必要なパラメータ（Priority 1 production の範囲を踏襲するか確認）：

- [ ] 介入数 `m` の範囲
- [ ] protocol depth `d` の範囲
- [ ] cumulant / functional order `k` の範囲
- [ ] hidden dimension `D` の上限
- [ ] memory depth `μ` の上限
- [ ] 共通で与える prior、calibration graph、shots、noise、held-out protocol

### A-2. 探索の起点 【必須】

- [ ] §6.1 現在の関心方向（優先順位付き）— RISEI介入構造 / SMRT polyhedral・二尺度 / EIT / Blueprints-of-theories内の他候補（トロピカル付値異常・因果インターフェース・保護の熱力学）のいずれか
- [ ] 今回の提案で「壊してよい仮定」の許可範囲 — §4.3 適用範囲外リストのうち踏み込んでよい範囲

### A-3. 探索空間の絞り込み 【必須に近い】

- [ ] §6.2 パラメータ空間の空白地帯（§4.3の12項目から探索価値のあるものを選別）
- [ ] §6.3 未解決の異常・矛盾

### A-4. Revised_Generalized_RISEI_Theory_2026-07-21 【必須】

- [ ] テキスト形式（`.tex` / `.md`）で入手 — 前回のPDFは本文抽出に失敗
- [ ] §8の記録元（§18, §9, §11–§13, §14, §20等）を辿れる状態にする

### A-5. 精度が上がる資料

- [ ] `.tex`巻末の内部計算レポート R1〜R12、特に：
  - [ ] `risei_uniqueness_competitor_audit/REPORT.md`
  - [ ] `RISEI_Unique_Phenomena_Search_Strategy_2026-07-23(1).md`
  - [ ] `RISEI_Response_Mechanism_Contextuality_Alternative_Idea_2026-07-23(1).md`
- [ ] `RISEI_実験プラットフォーム_投稿戦略_理論凍結方針_2026-07-23.md`
- [ ] 「惜しかった」候補の記録（完全還元より情報量が多い）
- [ ] 計算環境の実態（SymPy / QuTiP等が実際に使えるか）

### A-6. Claude側で代行できる作業

- [ ] §5 記法・用語の統一表の作成（`Frozen-Theories/`の3ファイルから抽出）
- [ ] `docs/context-pack.md` §1〜§3 の転記（ガイド§4.1・§4.2・§4.3から）
- [ ] §7 競合論文表の枠組み作成（分野リストのみ、実在確認は別途必要）

---

## B. ChatGPT 還元プロジェクトに渡すもの

### B-1. アップロードする資料

- [ ] `docs/context-pack.md`（§1〜§3記入後）
- [ ] ガイド §4.2 赤線14項目
- [ ] ガイド §4.3 適用範囲外リスト
- [ ] ガイド §6.4 却下リスト（還元先・写像つき）
- [ ] §5 記号表

**渡さないもの:** ガイド本体、提案文書そのもの（同調誘導を避けるため）。

### B-2. カスタム指示への追加

- [ ] `.tex`巻末の判定用チェックリスト12項目を `docs/redteam-instructions.md` の出力形式に組み込む

### B-3. 依頼事項（優先順）

1. [ ] hidden-dimension escalation — `D_hidden = 1,2,3,...D_max` でwitnessが消える次元があるか各段階で判定
2. [ ] 恒等式の探索そのもの — 競合模型（pairwise latent-group / 有限hidden-state / bounded-memory process）が満たすresponse-tensor恒等式を挙げさせる
3. [ ] pairwise factorizationからの脱出可否 — depth-3以上のconnected tensorだけが破れる構成の検討
4. [ ] triangle holonomyの不十分性チェック — group/hidden-state enlargement後も破れるかの判定
5. [ ] 早期kill 5項目の各PASS/FAIL判定

---

## C. ChatGPT 文献調査プロジェクトに渡すもの

### C-1. 渡す資料

- [ ] 命題と定義のみ（`claim-template.md`形式、理論名・略称は伏せる）
- [ ] §5 記号表
- [ ] 検索対象の分野キーワード（C-2参照）

### C-2. 依頼事項

1. [ ] 競合理論族の標準文献の特定：
   - compact-group synchronization / phase synchronization over graphs
   - structured state-space identification / controlled HMM
   - process tensor / quantum comb / bounded-memory process
   - full counting statistics / tilted generator
   - Riesz projector・Schur complementの開放系応答への応用
   - Zeno型縮約 / singular perturbation
2. [ ] 先行研究の判定 — 「決定的な差分が書けない論文」を最優先で報告
3. [ ] 恒等式の既知性チェック — Priority 1で見つかった候補identityが既に証明されているか
4. [ ] DOI/arXiv番号必須。出せない場合は「特定できず」と明記

### C-3. 注意

LLMは存在しない文献を生成する。DOI実在確認まで §7 には「未確認」フラグ付きで記入する。Claudeが挙げた文献も同じ扱いとする。
