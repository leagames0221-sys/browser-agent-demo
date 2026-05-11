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

---

## ADR-006 (2026-05-11): Qwen training-data attractor causal hypothesis — Alibaba e-commerce origin

**Context**: baseline_v1 (no defense) と baseline_v3 (Layer 1+2 defense) の **両方** で同型の 「$50 + 4-star + 15 items」 fabrication attractor が literal 発現。 prompt engineering (Layer 1+2) では literal 抑制不能。 attractor の **causal origin** を honest に仮説化し、 portfolio research finding として literal 公開する価値あり。

**Hypothesis (★★ tier, single-LLM observation)**:

Qwen 2.5-7B-Instruct は [Alibaba Cloud Qwen team](https://github.com/QwenLM) 製 LLM。 Alibaba は world's largest e-commerce company (Taobao / Tmall / AliExpress)、 訓練 corpus に **e-commerce product listings / reviews / filter UI patterns が他社 model より literal 高比率で存在する** 可能性が高い (公式 training data composition は未公開、 ★★ tier の推論)。

→ 「商品検索 + 価格フィルタ ($50 以下) + 評価フィルタ (4-star+) + 商品リスト 15 items」 は Alibaba LLM の **訓練 data 由来 strong attractor** であり、 task disengagement 時に LLM が default に fall back する pattern として literal 発現する仮説。

**Implications**:
1. **Model selection 時の training-data origin awareness**: e-commerce attractor を避けたい場合は 非 Alibaba LLM 候補 (Llama / DeepSeek / Mistral) を検討すべき
2. **Universal training-data attractor の存在**: 全 LLM が org-specific attractor を持つ可能性、 OpenAI 系は SEO/marketing 文体、 Google 系は 検索結果 pattern、 Anthropic 系は (推測) academic citation pattern 等
3. **Defense layer 設計への literal 反映**: prompt engineering alone では attractor 抑制不能 (v3 で literal 証明)、 **architectural intervention (Plan-Execute / LLM-as-judge gate)** が真に必要

**Sources (D8)**:
- [QwenLM organization](https://github.com/QwenLM) - Alibaba Cloud Qwen team
- [Qwen2.5 Technical Report](https://arxiv.org/abs/2412.15115) - training data composition は 「diverse high-quality」 とのみ記述、 e-commerce 比率は 非公開
- 自実測: baseline_v1 (180s, eBay rogue + $50/4-star filter attempt) + baseline_v3 (94s, $50/4-star/15-products fabrication) の 2 run consistent evidence

**Caveat (D9 ★★)**:
- Single-LLM observation、 n=1 model、 2 runs。 statistical significance 主張は literal 不能、 hypothesis tier
- 同 attractor が他 size Qwen (1.5B / 14B / 32B / 72B) でも literal 発現するかは未測定
- 比較対象 (Llama / DeepSeek 等) の同 task 走行は本 PJ Phase 2 scope 外 (D-WASTE-ZERO、 portfolio narrative 上 必要性低)

**Consequences**:
- ✅ portfolio research finding として literal 公開、 「model 選定時に training-data origin を意識する engineer」 signal
- ✅ recruiter / AI lab 向けに 「面白い observation を honest 開示できる」 signal、 Anthropic / OpenAI research 系職種で literal valuable
- ⚠️ Qwen team / Alibaba 公式 stance は (推測 hypothesis なので) 一切示唆せず、 user 観察として literal 提示
- ⚠️ ★★ tier hypothesis であることを README + ADR で literal 明示、 「証明」 主張は禁止

**Verify**: README `## Honest results` section に hypothesis box として literal 配置、 v4 (Plan-Execute) で attractor が architecturally suppressed されるか literal 観察 = hypothesis の indirect verification。
