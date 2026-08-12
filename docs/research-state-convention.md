# `research_state/summary.json` 規約

## 目的

Research CI（`research_ci_get_context`）が読む GitHub 側の状態は、サイズ制限で
**行数順に truncate される**（重要度順ではない）。実測で `NV-EIT-space` の702行中
348行しか読めなかった例がある。理論ごとに `research_state/summary.json` を1個
置くのは、truncate されても骨格（claim・anomaly・non-claim・Notion紐づけ）が
最初に読まれる位置に来るようにするため。

Notion 側の Research Questions DB・Theory Programs DB が「問い・Gate・witness
provenance の authority」であるのに対し、`summary.json` は **その理論のホーム
repository が持つ、機械可読な現況の写し**という位置づけ。権威は常に Notion 側
（`docs/research-state-convention.md` は Notion を上書きしない）。

## 配置

```
<theory-dir>/research_state/summary.json
```

monorepo 内の `Fixed-Response-Operational-Synthesis/` や
`NV-Blue-Charge-Control_seed_YYYY-MM-DD/` のように、理論ディレクトリ直下に置く。
専用 repository へ分割した後は repository root 直下に置く。

## スキーマ（v0.1）

```jsonc
{
  "schema_version": "0.1",
  "repo": "owner/repo",              // このファイルが属する GitHub repository
  "path": "TheoryDir/",              // repo 内でのディレクトリ（専用repoならルート）
  "branch": "main",
  "commit": "<40-char sha>",          // このファイルを生成/更新した時点の HEAD
  "staging_note": "...",              // monorepo に同居している場合の注記。専用repo化後は削除可

  "notion": {
    "research_asset_page": "<Notion page id>",   // Research Assets DB の対応行
    "research_asset_url": "https://app.notion.com/p/...",
    "research_question_id": "RQ-NN",              // 該当する場合
    "research_question_page": "<Notion page id>",
    "theory_program_id": "TP-NN",                 // Theory Program に昇格済みの場合のみ
    "theory_program_page": "<Notion page id>"      // 未昇格なら null
  },

  "repository_creation_gate": { "verdict": "...", "source": "...", "date": "..." },

  "claims": [
    { "id": "W1", "statement": "...", "status": "verified|unverified|failed|hold",
      "strength": "exact|conditional|conjecture", "code": "path/to/src.py",
      "output": "path/to/result.json" }
  ],
  "non_claims": ["..."],
  "known_absorbers": ["..."],

  "open_anomalies": [
    { "id": "...", "text": "...", "kind": "unresolved_completeness_question|narrowed_claim_after_kill|..." }
  ],
  "next_gates": [ { "id": "W4", "description": "..." } ],

  "generated_by": "who/what generated this, when, from which source files. Not auto-maintained."
}
```

`open_anomalies` は claims と同格の第一級フィールドとして扱うこと。
Research CI Core の Gate 0 は「内部の anomaly から始めよ、問いを発明するな」を
要求しているが、anomaly が散文（`PROJECT_STATE.md` の注記等）にしか存在しないと
truncate で真っ先に失われる。ここに構造化しておく。

## 維持ルール（自動ではない）

`summary.json` は **自動更新されない**。以下のときに、同じコミットで手動更新する。

- claim の status/strength が変わったとき（新しい gate が PASS/FAIL したとき）
- `open_anomalies` に該当する新しい失敗・発見があったとき
- Notion 側で Research Question / Theory Program が新規発行・昇格したとき
  （`notion.*` フィールドを実際の ID で埋める）
- repository を専用化して分割したとき（`repo`/`path`/`staging_note` を更新）

この規約に従う主体は、この repository で作業する人間と Claude セッションの両方。
理論の主張・証拠を更新するコミットには `research_state/summary.json` の更新を
含めること。

## Notion 側の対応する registry

Notion の **Research Assets** データソース（`collection://16b497dc-880a-4944-948e-38e1be9e64cd`）
が repo/branch/commit の構造化 registry として既に存在する（`Repository` /
`Branch` / `Commit Hash` / `Resource Type` / `Canonical URL` フィールド）。
新しい理論ディレクトリを作ったら、このデータソースに `Resource Type: GitHub
Directory` の行を1つ追加し、`Research Questions` / `Theory Programs` リレーションで
繋いだ上で、その Notion page id を `summary.json.notion.research_asset_page` に
書き戻す。**Research Questions DB や Theory Programs DB のスキーマは変更しない**
——`Evidence`（url）と `Repository Index`（自由記述）は既存の用途のまま使う。
