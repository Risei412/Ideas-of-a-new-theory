# プロジェクト現況（圧縮版）

**最終更新:** 2026-07-25 ／ 新規セッション・引き継ぎ用の1枚要約。詳細は各リンク先。

---

## 目的

**理論固有現象の発見** — その理論でしか出てこない現象と、その非還元性の論証。
既存理論の再整理は成果として数えない。投稿先想定は **PRX**。

## リポジトリ構成

| パス | 内容 |
|---|---|
| `THEORY_PROPOSAL_GUIDE.md` | **作業基準の本体**（803行）。提案前に必読 |
| `Frozen-Theories/` | 確定理論3件（RISEI・SMRT・EIT）。書き換えない |
| `Blueprints-of-theories/` | 草案5件（DCIT・トロピカル付値異常・因果インターフェース・実現可能性錐・保護の熱力学） |
| `docs/context-pack.md` | **ChatGPTにアップロードする資料層**（命令は書かない） |
| `docs/redteam-instructions.md` | ChatGPTのカスタム指示欄に貼る（還元／文献／校正の3種） |
| `docs/claim-template.md` | 各チャットに貼る主張の雛形 |
| `docs/stage0-checklist.md` | Stage 0 準備チェックリスト |
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
Tube calculus も固有現象とは判定されていないが、**棄却ではなく計算基盤として凍結**。

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

**記号衝突13件**（ガイド §5.3）— `Ω` `K` `Q` `Ξ` `ν` `C` `M` `P` `A` `G` `S` `z` `q` が理論間で別物。
特に `D` は理論では damping operator だが競合予算では hidden dimension。`D_damp`/`D_hidden` と書き分ける。

**計算環境** — Python/NumPy/SciPy/SymPy/mpmath 可、**QuTiP・CVXPY・Mathematica 不可**。
GKSL simulationは custom Liouville 実装、symbolic は SymPy で代替。

---

## 未決事項

1. **ガイド §1.2** — 代替投稿先の優先順位（過去の投稿履歴があれば）
2. **ガイド §7** — 競合論文表（ChatGPT文献調査で埋める）
3. **`context-pack.md` §2・§3** — ガイド §4.1・§4.2 からの転記（機械的作業、Claude側で実行可）
4. **RISEI の正式名称** — 凍結文書内に展開がなく未確認
5. **紛失資料3件** — `risei_uniqueness_competitor_audit/REPORT.md` 他。ゴミ箱から復旧予定
   （統合texに主要結果は保存済み。seed・optimizer設定・失敗ログは復元不可）

## 次のアクション

**Stage 0 の準備は実質完了。** P0の2件はどちらも着手可能。

- **Resource-bounded mechanism separation** — §6.3の最短起点・Priority 1 production・競合予算の凍結値すべてに直結。**最初の1本はこちらを推奨**
- **Interface realizability** — `Blueprints-of-theories/PRX_New_Theory_Blueprint_DCIT_2026-07-25.md` の dilation frustration と重なるため既存草稿を再利用できる可能性

---

## 提案時の禁止事項（ガイド §9）

- 固有現象が書けていないのに「新理論」と称する
- 非還元性の検討を省略する
- 「証明できる見込み」を「証明済み」と書く
- 既存文書の主張を確認せずに引用する
