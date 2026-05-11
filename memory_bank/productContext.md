# Product Context — browser-agent-demo

## What

local LLM (Ollama + Qwen2.5-7B) で動く browser automation agent demo。 browser-use を core engine に、 自 domain task + 数値計測 + 30 秒 demo gif を 1 つの GitHub public repo に集約。

## Why

portfolio として AI 駆動開発の strong hire 級 signal を立てる必要、 かつ HIVE 内部構造は秘匿。 動く artifact + 数値 + 第三者再現性 で 「中身見せず能力示す」 戦略の 1 件目。

## Target audience

- 採用担当 (AI lab / 上位 startup / 受託 premium 帯)
- 受託案件先 (4 社: BCG / ミスミ / Goodpatch / ロフト)
- OSS community (browser-use / Ollama / 日本語 AI ops 領域)

## Success signals (採用側が読み取るもの)

1. **動く artifact**: clone → run で同 gif 再生成可能、 詐称不能
2. **数値**: 成功率 95%+ / 平均所要時間 60s 以内 / API cost 0 円
3. **drift CI**: README claims が code reality と literal 同期、 文書/実態 不一致の構造的回避
4. **prior art 順守**: browser-use を fork-with-attribution、 ゼロ生成しない判断
5. **security 配慮**: Chrome 別 profile + .gitignore + pip-audit + Dependabot

## Anti-signals (構造的に避けるもの)

- Phase 0 で literal な数値 claim を README に置かない (drift 必至、 CI fail)
- HIVE 内部参照 (SECRETARY_MASTER / ARA / Security Master の具体 architecture) を repo に literal 書かない
- prod 認証情報 / client 機密 data の commit
- gif / 動画に sensitive UI が映り込まないこと (Phase 2 撮影前に literal review)
