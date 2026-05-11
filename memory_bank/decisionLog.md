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

---

## ADR-004 (2026-05-11): 2026-05 agent benchmark 実測値 calibration

**Context**: session 中に 「frontier model でも 50-78% task fail」 と発言、 これは 2024 paper (AgentBench / WebArena / OSWorld 初版) data の引用。 2026-05 時点で literal 大幅改善された数値を再確認する必要、 portfolio thesis の data drift 防止 (D-DRIFT-PREVENT-INFRA literal 順守、 自身の主張も verify 対象)。

**Decision**: 2026-05 最新 benchmark 値を sourced で literal 記録、 portfolio Honest results section + cost-tier table の比較 baseline として固定。

**Sources (D8 verified, WebSearch 2026-05-11)**:
- [Top 7 agentic benchmarks 2026 (MarkTechPost)](https://www.marktechpost.com/2026/04/26/top-7-benchmarks-that-actually-matter-for-agentic-reasoning-in-large-language-models/)
- [Claude Sonnet 4.6 vs GPT-5 2026 (SitePoint)](https://www.sitepoint.com/claude-sonnet-4-6-vs-gpt-5-the-2026-developer-benchmark/)
- [Berkeley CRDI April 2026 benchmark gaming research](https://moogician.github.io/blog/2026/trustworthy-benchmarks-cont/)

**Verified 2026-05 values**:
- SWE-bench Verified: 87.6% Claude Opus 4.7
- Terminal-Bench 2.0: 82.7% GPT-5.5 / 69.4% Claude Opus 4.7
- GAIA: 74.6% Claude Sonnet 4.5
- GDPval: 84.9% GPT-5.5
- WebArena: 61.7% IBM CUGA (early 2025、 14% → 62% の 4.4x leap)
- OSWorld: human 72.36%、 best model 12.24% (2024 初版) → OSWorld-Verified upgrade で改善中

**Caveat (★★)**: Berkeley April 2026 paper が "automated agent broke all 8 major agent benchmarks by reward hacking" 報告、 87% SOTA は ★★ tier (gaming 可能性)。 portfolio 内 honest results は **literal 自実測値のみ** に依拠、 SOTA 数値は文脈情報として扱う。

**Consequences**:
- ✅ portfolio で 「frontier vs local 7B gap」 を honest に比較可能 (frontier 80-87% vs local 7B 想定 30-75%)
- ✅ 「無料制約下 で frontier の literal X% に近づける」 という portfolio thesis の literal 数値 frame 確定
- ⚠️ benchmark score 自体が gaming risk あり → 自実測 + JSON evidence + drift-CI の 3 重 verify が必須

**Verify**: Phase 2 baseline_v2-v5 で literal 実測値を artifacts/ 配下に JSON 出力、 README cost-tier table が JSON evidence と CI で照合。

---

## ADR-005 (2026-05-11): 5-layer defense-in-depth 設計 (task discipline 対策)

**Context**: baseline_v1 で task discipline failure 発生 (Qwen 2.5-7B が task 完了後 eBay に prompt injection 級暴走、 max_steps 8 浪費、 Judge FAIL)。 2026-05 agentic AI 業界 consensus = **「single silver bullet 無、 defense in depth が唯一の path」** (前述 ADR-004 sources、 + [Anthropic Computer Use research](https://www.anthropic.com/news/3-5-models-and-computer-use))。 portfolio として task discipline 問題を解く journey を literal 設計する必要。

**Decision**: baseline_v2 から v5 まで progressive に 5 layer の defense を literal 追加、 各 layer ごとに JSON evidence + README Honest results 更新:

| version | 追加 layer | 想定 success rate (★★) | 想定所要時間 |
|---|---|---|---|
| v1 (current) | Layer 0 (none) | ~30-50% (literal FAIL today) | 180s |
| **v2** (next) | Layer 1: max_steps=2 + URL allowlist + STOP semantics (system prompt) | ~50-60% | ~60s |
| v3 | + Layer 2: JSON schema constraint + few-shot STOP examples | ~60-70% | ~45s |
| v4 | + Layer 3: Plan-Execute architecture (内蔵 simple pattern、 LangGraph 級は scope 外) | ~65-75% | ~30s |
| v5 | + Layer 5: GitHub Models frontier fallback (cost-tier table 完成) | ~80-87% | ~10s |

**Sources (D8)**:
- [LangGraph Plan-Execute pattern](https://github.com/langchain-ai/langgraph)
- [GitHub Models marketplace (free tier, no CC)](https://github.com/marketplace/models)
- 前述 Berkeley 2026 / Anthropic / OpenAI sources

**Consequences**:
- ✅ portfolio narrative の literal 完成形: v1 暴走 → v5 frontier-comparable の 4-step improvement journey
- ✅ recruiter signal 「defense in depth + 計測 + honest + improvement velocity」 の 4 軸 simultaneous
- ✅ 全 layer が zero-CC constraint 内 (Ollama local + GitHub Models free tier + 自実装 wrapper)
- ⚠️ Layer 3 (Plan-Execute) は内蔵 simple impl のみ、 LangGraph 級 architecture は scope 外 (D-WASTE-ZERO)
- ⚠️ Layer 5 frontier fallback は GitHub Models rate limit (~50 calls / day free tier、 2026-05 推定 ★) 内で運用、 超過時は honest 記録

**Verify**: 各 v に対し `artifacts/baseline_v{N}.json` を literal 出力、 drift-CI で 5 file 存在 + 内容 sanity check、 README cost-tier table が JSON 由来自動生成。
