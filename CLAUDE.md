# このリポジトリでの作業方針

理論の草稿を蓄積するリポジトリ。

- `Blueprints-of-theories/` — 草案段階の理論（Markdown）
- `Frozen-Theories/` — 確定・認証済みの理論（LaTeX）。原則として書き換えない。

## 新理論を提案するとき

**必ず [`THEORY_PROPOSAL_GUIDE.md`](THEORY_PROPOSAL_GUIDE.md) を先に読むこと。**
投稿先の基準、使ってよい既存理論、却下済みのアイデア、出力フォーマットがそこにある。

最重要原則：求めているのは既存理論の再整理ではなく、
**その理論でしか出てこない現象（理論固有現象）とその非還元性の論証**である。

現況の1枚要約は [`docs/PROJECT_STATE.md`](docs/PROJECT_STATE.md)。新規セッションはここから読むと早い。

## 理論を専用リポジトリへ切り出すとき

**必ず [`REPOSITORY_GATE.md`](REPOSITORY_GATE.md) を先に読むこと。**
専用リポジトリは一時的な作業場であり、成熟した理論の家ではない（成熟＝卒業条件）。
枠は1つで、増やすには枠の移譲を明記する。Gate A（科学）が通っても
Gate B（分離の必要）が通らなければ monorepo に残す。

理論ディレクトリの機械可読な現況は `research_state/summary.json` に置く。
スキーマと維持ルールは [`docs/research-state-convention.md`](docs/research-state-convention.md)。

## 検証ワークフロー

提案は ChatGPT を赤チーム（敵対的検証者）として回す。工程は同ガイド §11。

- `docs/redteam-instructions.md` — ChatGPT のカスタム指示（コピペ元）
- `docs/context-pack.md` — プロジェクトにアップロードする資料層
- `docs/claim-template.md` — 各チャットに貼る主張の雛形
