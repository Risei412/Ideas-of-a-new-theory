# Stage 0 準備チェックリスト

Fable 5 による理論提案生成（Stage 0）に向けて必要な資料と、ChatGPT側（還元・文献調査）に渡すもの・依頼事項をまとめる。
資料が揃うたびにチェックしていく運用とする。

---

## A. Stage 0（Claude / Fable 5 提案生成）に必要な資料

### A-1. 競合理論族の定義と資源予算 【確定 — 2026-07-25、ChatGPT提案】

`docs/source-material/RISEI_Unique_Phenomena_Computation_Summary_and_Search_Strategy_2026-07-23.tex` の Priority 0 に列挙された6族。**標準監査／拡張・最終kill監査の二段階**で予算を固定する方針が確定した。詳細は `docs/context-pack.md` §6「競合理論族の資源予算」に転記済み。

- [x] enlarged GKSL with hidden ancilla → `D_hidden` 標準1–4、最終6。総自由パラメータ P≤256
- [x] tilted-GKSL / full counting statistics → k≤4, d≤4, counting field数最大2, counted channel数最大4
- [x] compact-group synchronization → r_G≤4, q_G≤15, 対象群 permutation/SO(2)/SO(3)/SU(2)/SU(3)/SU(4)、ρ∈{1.0,1.5,2.0}
- [x] controlled HMM / structured state-space identification → D≤6, m≤8, readout channel最大4, P≤256
- [x] bounded-memory process-tensor model → D_M≤6, χ≤36, μ≤3, d≤4, k≤4, P≤256
- [x] active experimental design baseline → adaptive round最大4, calibration protocol最大32, 総shots最大1.2×10^5
- [x] **6族で確定。ただし「解析的kill gate」（BCH/Dyson/Krylov reachability/Schur-Zeno/Kalman controllability/quantum regression theorem/symmetry reduction）を予算を持たない第7層として追加** — 文書表記は「競合モデル6族＋解析的reduction gate」

固定パラメータ（標準監査／拡張監査の二値）：

- [x] 介入数 m：標準3–6、拡張7–8
- [x] protocol depth d：標準1–3、拡張4
- [x] cumulant / functional order k：標準1–3、拡張4
- [x] hidden dimension D：標準1–4、拡張5–6
- [x] memory depth μ：標準1–2、拡張3
- [x] 自由パラメータ数 P≤128（標準）／P≤256（拡張）、optimizer restart 16／32
- [x] 共通prior：J_ref=1、γ,κ∼LogUniform(10⁻²,10²)、ReH_ij,ImH_ij∼Uniform(−1,1)
- [x] calibration graph：depth1全件、depth2はρ=1.5の連結グラフ・両順序測定、depth3は24件seed固定、depth4はcalibration対象外
- [x] shots/noise：1protocolあたり2000shots、総上限1.2×10^5、通常1%/stress3%、control-amplitude drift 1%、timing jitter 0.5%
- [x] held-out：depth2未使用edge・depth3未使用protocol・depth4の事前固定64protocol、seed 20260723、候補生成/調整/停止判定に使用禁止

### A-2. 探索の起点 【必須】

- [ ] §6.1 現在の関心方向（優先順位付き）— RISEI介入構造 / SMRT polyhedral・二尺度 / EIT / Blueprints-of-theories内の他候補（トロピカル付値異常・因果インターフェース・保護の熱力学）のいずれか
- [ ] 今回の提案で「壊してよい仮定」の許可範囲 — §4.3 適用範囲外リストのうち踏み込んでよい範囲

### A-3. 探索空間の絞り込み 【§6.3は確定、§6.2は未定】

- [ ] §6.2 パラメータ空間の空白地帯（§4.3の12項目から探索価値のあるものを選別）
- [x] §6.3 未解決の異常・矛盾 — 2026-07-25、ChatGPT提案で4件確定。**前提として「現時点で確定した理論間矛盾はない」ことを明記**（数値と証明の隙間・有限資源下の未決着・一般定理のない境界現象のみ）。詳細は`docs/context-pack.md` §7参照。
  1. Resource-bounded same-data gap（最短起点。Priority 1 productionに直結）
  2. 有限gap exact zeroと漸近zeroの差（最短の数学的定理プロジェクト）
  3. Exact/approximate kernel crossoverの一般十分条件未証明
  4. Calibration redundancy boundary（ρ=1.5での急激なEXACT化に境界定理なし）

### A-4. Revised_Generalized_RISEI_Theory_2026-07-21 【必須・紛失フォルダ内、後日共有予定】

- [ ] テキスト形式（`.tex` / `.md`）で入手 — 前回のPDFは本文抽出に失敗。ゴミ箱の紛失フォルダに含まれる可能性あり
- [ ] §8の記録元（§18, §9, §11–§13, §14, §20等）を辿れる状態にする

### A-5. 精度が上がる資料

**紛失フォルダがゴミ箱にあり、後日共有予定。** 2026-07-25時点でChatGPT側の作業領域に残存確認できたもの／できないもの：

- [x] 統合計算・探索戦略.tex（＝リポジトリの `RISEI_Unique_Phenomena_Computation_Summary_and_Search_Strategy_2026-07-23.tex`）— 残存
- [x] `RISEI_実験プラットフォーム_投稿戦略_理論凍結方針_2026-07-23.md` — 残存。Euをpositive demonstration、NVをcollapse/turn-on/negative controlに使う役割分担、理論凍結・材料翻訳層のみ更新する方針を含む
- [ ] `RISEI_Observation_Grammar_Adaptive_Equivalence_Splitting_Idea_2026-07-23(1).md` — 残存（未受領、内容未確認）
- [x] `RISEI_Branch_Complete_Tube_Calculus_PRX_Roadmap_2026-07-22(1).md` — 残存（リポジトリに既に格納済み）
- [ ] `risei_uniqueness_competitor_audit/REPORT.md` — **未確認/紛失中**（統合.texに主要結果は保存されているため科学的結論は復元可能。seed・optimizer設定・中間表・失敗runログは復元不可）
- [ ] `RISEI_Unique_Phenomena_Search_Strategy_2026-07-23(1).md` — **未確認/紛失中**
- [ ] `RISEI_Response_Mechanism_Contextuality_Alternative_Idea_2026-07-23(1).md` — **未確認/紛失中**
- [x] 「惜しかった」候補の記録 — 2026-07-25、ChatGPT提案で確定。**最も情報量が多い4件**（早期killされた3件とは区別して保存）：
  1. Matched operational equivalence — (d_min,k_min)=(2,2), N_5%≤137 の有限資源certificate
  2. Exact second-cumulant witness — ΔK_2=2ℓ_Y(G−I)r_X のexact式と明示的消失条件
  3. Held-out quotient predictor — 20 calibrationから30未使用protocolを数値精度内で予測
  4. Global cycle quotient atlas — 予測可能領域とABSTAIN領域を有限資源で分離
  （対照：Response–Mechanism Contextuality・mean-blind fluctuation・naive ternary responseは早期killされたnegative controlとして保存）
- [x] 計算環境の実態 — 2026-07-25確認。詳細は下表

**計算環境の実態（2026-07-25、ChatGPT側の環境で確認）:**

| ツール | 状態 |
|---|---|
| Python 3.13.5 | 使用可能 |
| NumPy 2.3.5 | 使用可能 |
| SciPy 1.17.0 | 使用可能 |
| SymPy 1.14.0 | 使用可能 |
| mpmath 1.3.0 | 使用可能 |
| pandas 2.2.3 | 使用可能 |
| matplotlib 3.10.8 | 使用可能 |
| NetworkX 3.6.1 | 使用可能 |
| scikit-learn 1.8.0 | 使用可能 |
| pdfLaTeX (TeX Live 2025) | 使用可能 |
| QuTiP | **未インストール** |
| CVXPY | **未インストール** |
| Mathematica / wolframscript | **利用不可** |
| SageMath | **利用不可** |
| Julia / Octave | **利用不可** |

→ ガイド§10の「推奨ツール」表のうち、GKSL/Lindblad simulationはQuTiP前提だが未導入。当面はNumPy/SciPyでのcustom Liouville実装、symbolic証明はSymPy（Mathematicaの代替）で進める前提に修正が必要。§10.5「Claude等AIエージェントへの実行規則」の代替方針がそのまま適用される。

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
