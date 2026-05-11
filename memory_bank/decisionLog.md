# Decision Log — browser-agent-demo

> ADR (Architecture Decision Record) 形式。 重要決定のみ append。

---

## ADR-001 (2026-05-11): browser-use を core engine として採用

**Context**: portfolio で AI 駆動 browser automation demo を構築する必要、 ゼロから書くと debt 爆発 (D-PRIOR-ART-FIRST 違反)。

**Decision**: `github.com/browser-use/browser-use` (MIT、 star 30k+、 active maintained) を core engine として採用。 自 repo は task 定義 + 自 domain dataset + 数値計測 + demo gif 生成に集中。

**Consequences**:
- ✅ install ~ baseline eval まで 1-2 日に圧縮
- ✅ MIT で commercial portfolio に literal 流用可
- ⚠️ Playwright (browser-use 依存) が Chromium DL + npm package を持つ → D-NPM-3GUARD 適用必須
- ⚠️ prompt injection risk (browser が悪意 site を踏む) → sandbox profile + 信頼 site 限定で防御

**Verify**: Phase 1 で `pip-audit` + `npm audit` (Playwright 経由) 両方 green、 baseline eval pass。

---

## ADR-002 (2026-05-11): LLM backend は Ollama + Qwen2.5-7B (Q4_K_M) で固定

**Context**: API 課金 0 円を AC として、 consumer laptop で動く LLM が必要。

**Decision**: Ollama (local LLM runtime, MIT) + `qwen2.5:7b` Q4 quant 採用。 vision 必要時のみ `llama3.2-vision` に切替検討。

**Consequences**:
- ✅ API key 不要、 オフライン稼働可
- ✅ ~5GB DL で consumer GPU 推論可
- ⚠️ Opus / GPT-5 級の品質は出ない → task は Qwen 7B で realistic に green になる scope に設計

**Verify**: baseline eval 成功率 + 平均所要時間 を `memory_bank/logbook.md` に Phase 1 完了時 記録。

---

## ADR-003 (2026-05-11): Chrome 別 profile `portfolio-sandbox` で隔離

**Context**: AI 駆動 browser が prod 認証情報を読まないよう構造的に隔離する必要 (D-NEW-PJ-SANDBOX-CHECK)。

**Decision**: Chrome 別 profile を作成し、 dummy 認証情報のみ投入。 `.gitignore` で `chrome_profile/` 除外、 commit 混入防止。

**Consequences**:
- ✅ OS-level isolation の 90% 達成 (D9 ★★ tier、 完全 isolation は Docker 化が真本命だが個人 demo scope では別 profile で literal 十分)
- ⚠️ user が prod profile に誤切替する human error の余地は残る → README に literal 警告明記

**Verify**: Phase 1-2 で AI agent 実行時 cookie / saved password が dummy 範囲のみであることを目視 + log で確認。
