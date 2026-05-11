# browser-agent-demo — Tier 2 PJ-local rules

> Tier 1 (~/.claude/SECRETARY_MASTER.md / ARA / Security) を auto-import 済。
> 本 file は PJ 固有規約のみ記述。 universal な doctrine は Tier 1 が担う。

## PJ Identity

- 案件: portfolio 用 browser automation agent demo (HIVE と無関係な独立 artifact)
- 目的: AI が browser を操作する RPA 実例を local LLM のみで構築、 API 課金 0 円で動く完成品を GitHub public で示す
- scope: Phase 0 scaffold → Phase 1 baseline → Phase 2 自 domain task + demo gif → Phase 3 craftstack 統合
- target audience: 採用担当 / 受託先 / OSS 利用者

## PJ 固有 verify priority

Tier 1 default (D-VERIFY-PRIORITY) を継承、 加えて:
1. `pytest` (browser-use 同梱 eval harness が green か)
2. `pip-audit` (D-NPM-3GUARD 相当の Python 版)
3. `gh workflow run drift-check` (README claims vs reality 自動 verify)

## PJ 固有 用語

- **task**: browser agent が実行する 1 件の作業単位 (例: 競合 site 巡回 → CSV 出力)
- **sandbox profile**: Chrome 別 profile `portfolio-sandbox`、 prod 認証情報 混入禁止
- **prior art**: `github.com/browser-use/browser-use` (採用元 OSS、 audit 済)

## PJ 固有 forbidden / required

- 禁止: prod 認証情報の sandbox profile 混入、 client 機密 data の task 投入、 commit メッセージに secret 混入
- 必須: 全 commit で README の verified state section が drift-check と一致、 prior art clone 時に commit msg へ `derived from browser-use@<sha>` literal 記録

## 関連 doc

- `spec.md`: PJ 仕様 SSoT (機能 / 非機能 / 完了条件)
- `memory_bank/`: Cline pattern 5 file (logbook / activeContext / decisionLog / productContext / systemPatterns) — D-HANDOFF-DUTY 順守
- `.github/workflows/drift-check.yml`: README claims 自動 verify
- `.gitignore`: Security Master apply (.env / .venv / __pycache__ / Chrome profile data)

## Memory Bank pattern (D-HANDOFF-DUTY literal 順守)

session 開始時:
1. `memory_bank/activeContext.md` を Read (current focus)
2. `memory_bank/logbook.md` 末尾 § を Read (前任 session 最終 entry)
3. 必要なら `decisionLog.md` の ADR を Read

session 終了時:
1. `memory_bank/logbook.md` に本 session entry を append (timestamp / 作業 / error / 進捗 / 申し送り)
2. ADR 級決定があれば `decisionLog.md` に新規 ADR
3. focus 変更時のみ `activeContext.md` 更新
