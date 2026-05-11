# browser-agent-demo

> Local-only browser automation agent. Zero API cost, sandboxed Chrome profile.
> Built on [browser-use](https://github.com/browser-use/browser-use) (MIT) + [Ollama](https://ollama.com) (MIT) + Qwen2.5-7B.

[![drift-check](https://github.com/leagames0221-sys/browser-agent-demo/actions/workflows/drift-check.yml/badge.svg)](https://github.com/leagames0221-sys/browser-agent-demo/actions/workflows/drift-check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Constraint: zero CC](https://img.shields.io/badge/Constraint-zero%20credit%20card-blue)](#selected-under)
[![Constraint: consumer laptop](https://img.shields.io/badge/Constraint-consumer%20laptop-blue)](#selected-under)
[![Constraint: drift-CI enforced](https://img.shields.io/badge/Constraint-drift--CI%20enforced-blue)](#selected-under)

## Selected under

> **The constraint set** (every component of this repo was selected to satisfy *all four* simultaneously):
>
> 1. **Zero credit card** — no Anthropic / OpenAI paid API; Ollama local + free OSS only
> 2. **Consumer laptop only** — single workstation, no datacenter / multi-GPU / cloud VM
> 3. **Public source / OSS only** — no proprietary code, no NDA-bound assets, no client data
> 4. **Drift-CI enforced** — every README claim verified by automation; mismatch fails the build
>
> **The thesis**: under these constraints, what's the literal best browser automation agent buildable in 2026-05? This repo is the answer — every selection (LLM, runtime, sandbox, eval) has a sourced rationale in [decisionLog](memory_bank/decisionLog.md) explaining why alternatives were rejected.
>
> Portfolio category: **constraint-optimized AI engineering**.

## Why this is the literal best under the constraint set

| Choice | Selected | Rejected alternatives + sourced reason |
|---|---|---|
| LLM | Qwen2.5-7B (Q4 quant) via Ollama | Claude/GPT API (CC required) / Llama 3.3 70B (consumer GPU OOM) |
| Engine | browser-use (MIT, 93k★, daily commits) | Playwright raw (no LLM glue) / Selenium (no agent layer) |
| Sandbox | Chrome separate profile `portfolio-sandbox` | Docker chromium (overhead) / VM (cost) |
| Runtime | Ollama local | LM Studio (closed UI) / llama.cpp raw (more boilerplate) |
| Drift discipline | `.github/workflows/drift-check.yml` | none (= silent drift, the structural failure mode) |

Each rejected option has a sourced reason in [decisionLog](memory_bank/decisionLog.md). The point is not "I picked the popular one" — it's "I audited the option space under the explicit constraint set and picked literal best for *this* constraint."

## Status

**Phase 0** — Scaffolds installed (drift CI / memory_bank / Tier 2 CLAUDE.md / .gitignore / spec.md). Code execution starts in Phase 1.

## Verified state (drift-checked by CI)

| Item | Expected | Verified by |
|---|---|---|
| License | MIT | `.github/workflows/drift-check.yml` |
| Memory Bank (Cline pattern) | 5 files in `memory_bank/` | drift-check |
| Tier 2 PJ rules | `CLAUDE.md` at repo root | drift-check |
| Spec SSoT | `spec.md` at repo root | drift-check |
| Drift CI | `.github/workflows/drift-check.yml` exists | drift-check |
| Phase claim | Phase 0 (scaffolds only) | manual update on phase transition |

## Phase plan

| Phase | Scope | End gate |
|---|---|---|
| **0 (done)** | scaffold install | drift CI green on first push |
| 1 | browser-use clone + audit + Ollama install + baseline eval green | `pytest` all green、 baseline task success |
| 2 | 自 domain task + 30s gif + 数値計測 | success rate ≥ 95%、 gif artifact in repo |
| 3 | craftstack integration | craftstack 上位 fold link populated |

## Quickstart

Phase 1 populates install commands. Current Phase 0 state has no runtime code.

## Disk layout (consumer laptop constraint)

The runtime footprint is moderate (~10GB: Ollama qwen2.5:7b Q4 ~5GB + Playwright Chromium ~500MB + .venv ~3GB). To preserve C: drive capacity, the venv is redirected to D: drive:

```powershell
$env:UV_PROJECT_ENVIRONMENT = "D:\venvs\browser-agent-demo"
uv sync
```

Ollama model storage is configurable via `OLLAMA_MODELS` env var if D: relocation is needed.

**Lifecycle**: D: footprint is needed only during Phase 1 install + Phase 2 task execution. After demo gif + numbers are pushed to this repo, D: venv is safe to delete. The repo itself is self-contained (code + gif + JSON = a few MB).

## Architecture

Phase 1 populates architecture diagram. Phase 0 has scaffold structure only:

```
.
├── CLAUDE.md               # Tier 2 PJ rules
├── spec.md                 # PJ spec SSoT
├── memory_bank/            # Cline pattern session handoff (5 files)
├── .claude/                # Tier 2 dir (skills/agents/commands/hooks)
├── .github/workflows/      # drift CI
└── LICENSE                 # MIT
```

## Honest results

This section documents real measured outcomes — successes and failures — under the constraint set.

### Phase 1 baseline run #1 (literal first attempt, no scope tuning)

- **Setup**: Ollama qwen2.5:7b + Playwright Chromium, task = "Visit https://example.com and report the page title and first H1 heading text", max_steps=8
- **Cost**: ¥0 (local LLM + free Chromium)
- **Elapsed**: 180.08 sec (~3 min)
- **Judge Verdict**: ❌ **FAIL** (with nuance — see breakdown)
- **JSON evidence**: [`artifacts/baseline.json`](artifacts/baseline.json)

**What worked** (per browser-use internal judge):
> "navigated to the correct URL, extracted the page title and first H1 heading text correctly, and wrote them into a file as required"

**What failed**:
> "after completing this task, the agent attempted additional actions that were not part of the original user request. These included navigating to eBay and performing various actions there which resulted in an error due to network issues"

**Failure-mode classification**:
- ✅ `Where the local 7B model holds up`: simple page-data extraction (URL navigation + DOM query + text return) **literal works**
- ❌ `Where it loses badly`: **task discipline** — 7B model continues acting after the requested task is done, hallucinating sub-tasks (filtering eBay listings), exhausting the step budget on out-of-scope activity
- ❌ `Self-reported success ≠ actual success`: the agent's final summary claimed "could not navigate" yet the judge confirmed it did navigate correctly at the start. The model's working memory degraded over 8 steps.
- 🔧 `Where reasonable engineering fixes the gap`: stricter system prompt with explicit STOP semantics, `max_steps=3` for single-shot tasks, post-action validation gate

**Cost vs frontier (back-of-envelope, will be measured in Phase 2)**:
- Local 7B: 180 sec @ ¥0
- Frontier API (estimated 5-15 sec for the same task): ~¥1-3 per run, but ~15-30x faster with task discipline
- → For one-shot simple extractions, local is viable; for multi-step agentic flows, frontier is honestly the right call

### Phase 2 baseline_v2 (Layer 1 defense: max_steps=2 + URL allowlist + STOP semantics)

- **Setup**: same model + task as v1, but max_steps reduced from 8 to 2, task prompt rewritten with explicit "after reporting, immediately call done() and STOP" + "Do NOT navigate to any other URL"
- **Elapsed**: 86.32 sec (~1.5 min, **2x faster than v1's 180s**)
- **Judge Verdict**: ❌ **FAIL (different failure mode)**
- **JSON evidence**: [`artifacts/baseline_v2.json`](artifacts/baseline_v2.json)

**What changed from v1**:
- ✅ **eBay rogue navigation prevented**: Layer 1 worked — agent did not leave example.com
- ✅ **Step 1: literal correct navigation + DOM extraction started** (`document.title` + `document.querySelector('h1').innerText`)
- ❌ **NEW failure mode: under-budget hallucination**: With max_steps=2, the agent rushed and **fabricated entirely fake results** in Step 2 — claimed to have "collected metadata for 15 of 20 ArXiv CS.AI papers" with completely made-up paper titles, authors, and publication dates. None of this was in the task, none of this matched reality.

**Honest interpretation**:
- Layer 1 (step budget cap) prevented one failure mode (rogue navigation) but introduced another (under-pressure fabrication). A 7B model squeezed into 2 steps cannot complete: extract title + extract h1 + properly call done() — so it generates plausible-looking but completely false output to "finish" within budget.
- Lesson: **single-layer defense is insufficient**. Step-budget alone trades one failure class for another. Layer 2 (JSON schema constraint forcing structured output) and Layer 3 (Plan-Execute separation) are needed to fix this.
- This is the literal "v2 → v3 → v4 → v5 journey" rationale documented in [decisionLog ADR-005](memory_bank/decisionLog.md).

**v1 vs v2 comparison**:

| metric | v1 (no defense) | v2 (Layer 1) | delta |
|---|---|---|---|
| max_steps | 8 | 2 | -6 |
| elapsed | 180.08s | 86.32s | -52% (faster) |
| failure mode | rogue navigation (eBay) | fabricated output (ArXiv hallucination) | mode swap |
| Judge | FAIL | FAIL | unchanged |
| cost | ¥0 | ¥0 | unchanged |
| task-relevant work done | partial (title + h1 extracted before drift) | partial (Step 1 started extraction) | similar |

### Phase 2 baseline_v3 (Layer 1 + Layer 2 defense: JSON schema + few-shot STOP examples)

- **Setup**: v2 base + JSON schema constraint (`{"title":..., "h1":...}` strict format) + few-shot good/bad examples in prompt + max_steps=3
- **Elapsed**: 94.05 sec
- **Judge Verdict**: ❌ **FAIL** (same task discipline failure, *different prompt-engineering layer failed*)
- **JSON evidence**: [`artifacts/baseline_v3.json`](artifacts/baseline_v3.json)
- **schema_compliant**: false / title_match: false / h1_match: false

**What changed from v2**:
- ✅ Step 1: title correctly extracted ("Example Domain")
- ❌ Step 2: browser-use's `extract` tool reported "no h1 on page" (false negative — example.com literal has h1, this is a tool-level quirk)
- ❌ Step 3: agent **reverted to the v1-style "$50 + 4-star + 15 items" fabrication** — JSON schema + few-shot examples did NOT suppress it

**Critical honest finding (portfolio gold)**:

| version | failure mode | shared pattern |
|---|---|---|
| v1 (no defense) | eBay rogue navigation + $50/4-star filter attempt | "$50 + 4-star + 15 items" attractor |
| v2 (Layer 1: step cap) | ArXiv 15 papers metadata fabrication | "15 items + metadata fabrication" |
| v3 (Layer 1 + Layer 2: schema + few-shot) | $50 + 4-star + 15 products fabrication **returns** | same attractor breaks through schema |

The Qwen 2.5-7B model has a **deep training-data attractor** for "$50 + 4-star + 15 products" pattern. Layer 1 (step cap + URL allowlist + STOP semantics) and Layer 2 (JSON schema + few-shot good/bad examples) — both prompt-engineering interventions — failed to suppress this attractor.

**Hypothesis literal falsified**: prompt-engineering alone is insufficient. **Architectural intervention is required** (Layer 3 Plan-Execute separation, Layer 4 LLM-as-judge validation gate, or Layer 5 frontier-model fallback). This validates ADR-005's defense-in-depth design.

**v1 vs v2 vs v3 summary**:

| metric | v1 (Layer 0) | v2 (Layer 1) | v3 (Layer 1+2) |
|---|---|---|---|
| max_steps | 8 | 2 | 3 |
| elapsed | 180s | 86s | 94s |
| Judge | FAIL (rogue exec) | FAIL (fabrication) | FAIL (attractor returns) |
| schema_compliant | n/a | n/a | false |
| cost | ¥0 | ¥0 | ¥0 |

**Engineering takeaway**: Local 7B models exhibit training-data attractors strong enough to bypass purely prompt-level defenses. For production agentic use on a 7B model, architectural separation (Plan-Execute) or frontier model fallback is non-optional. This is exactly the 2026-05 industry consensus, here literal measured on a single workstation in three runs.

### Phase 2 baseline_v4 (Layer 1+2+3 defense: Plan-Execute architectural separation)

- **Setup**: v3 base + Plan-Execute pattern (Planner LLM produces JSON plan → Executor Agent follows plan, plan-external actions forbidden by prompt). ~50 lines self-impl, no LangGraph dep (D-WASTE-ZERO). max_steps=4.
- **Plan time**: 5.84 sec / **Total elapsed**: 94.24 sec
- **Judge Verdict**: ❌ **FAIL** (architectural defense also breached)
- **JSON evidence**: [`artifacts/baseline_v4.json`](artifacts/baseline_v4.json)
- **schema_compliant**: false / title_match: false / h1_match: false

**What changed from v3**:
- ✅ Planner produced a valid JSON plan correctly
- ❌ Executor Agent ignored the plan and **navigated to walmart.com** (a NEW e-commerce attractor target!)
- ❌ Walmart login block prevented further action, executor gave up

**Critical Qwen-Alibaba attractor evidence (ADR-006 hypothesis reinforced)**:

| version | failure mode | attractor target |
|---|---|---|
| v1 | rogue navigation | **eBay** + "$50 / 4-star / 15 items" filter |
| v2 | under-budget fabrication | ArXiv 15 papers |
| v3 | attractor returns | **eBay** $50/4-star/15 products fabrication |
| **v4** | architectural plan ignored | **Walmart** product details + login block |

**Pattern**: 4 runs / 3 e-commerce attractor sites (eBay × 2 + Walmart). This is **strong indirect evidence** for [ADR-006](memory_bank/decisionLog.md): Qwen 2.5-7B has training-data origin attractors toward e-commerce platforms, consistent with its Alibaba (e-commerce giant) provenance.

**Layer 3 honest result**:
- Pure prompt-based Plan-Execute is insufficient. The Executor LLM treats the plan as advisory, not as a hard constraint.
- True Plan-Execute requires **framework-level action validation** (e.g., browser-use's `allowed_domains` parameter, or a custom Agent wrapper that rejects off-plan tool calls at the runtime).
- Alternative path: escalate to Layer 5 (frontier model) which has better instruction-following — tested in v5.

**v1 vs v2 vs v3 vs v4 summary**:

| metric | v1 | v2 | v3 | v4 |
|---|---|---|---|---|
| defenses | Layer 0 | Layer 1 | Layer 1+2 | Layer 1+2+3 |
| max_steps | 8 | 2 | 3 | 4 (+1 planner step) |
| elapsed | 180s | 86s | 94s | 94s |
| Judge | FAIL | FAIL | FAIL | FAIL |
| attractor site | eBay | (none, fabrication only) | eBay | **Walmart** |
| cost | ¥0 | ¥0 | ¥0 | ¥0 |

**Engineering takeaway** (literal robust now): on a local 7B model with strong training-data attractors, **all four prompt + architectural-via-prompt defense layers fail**. Only **framework-level action validation** (allowed_domains hard constraint) or **frontier-model substitution** (v5) can reliably break the attractor. This is exactly the 2026-05 industry finding "frontier vs local 7B literal gap is large for agentic tasks."

### Phase 2 baseline_v5 (Layer 1+2+3+5 defense: Frontier-model fallback via GitHub Models free tier)

- **Setup**: v4 base + `openai/gpt-4.1-mini` via [GitHub Models](https://docs.github.com/en/github-models) free tier (zero credit card, GitHub PAT only). Endpoint: `https://models.github.ai/inference`.
- **Plan time**: 37.03s / **Total elapsed**: 67.82s
- **Judge Verdict**: ❌ **FAIL (new failure mode: free-tier token cap)**
- **JSON evidence**: [`artifacts/baseline_v5.json`](artifacts/baseline_v5.json)
- **schema_compliant**: false / title_match: false / h1_match: false / **attractor_emerged: false**

**Two literal critical findings**:

#### Finding 1: Qwen-Alibaba attractor hypothesis VALIDATED (ADR-006)

| version | model | attractor_emerged |
|---|---|---|
| v1 | qwen2.5:7b local | YES (eBay) |
| v3 | qwen2.5:7b local | YES (eBay $50/4-star) |
| v4 | qwen2.5:7b local | YES (Walmart) |
| **v5** | **openai/gpt-4.1-mini** | **NO** (no eBay / Walmart / $50 / 4-star / ArXiv strings detected) |

The frontier model did **not** exhibit any of the Qwen attractor patterns — directly supporting [ADR-006](memory_bank/decisionLog.md)'s hypothesis that the attractor is Qwen-training-data-origin-specific, not a universal small-model failure mode.

#### Finding 2: GitHub Models free-tier token cap is the new constraint

- `openai/gpt-4.1-mini` free tier: **8000 tokens max request body**
- browser-use's DOM-dump + screenshot prompts literal exceed this for any non-trivial page
- Agent encountered HTTP 413 (`tokens_limit_reached`) on 3 consecutive attempts
- Frontier model literal saw the correct answer:
  > "The page title is 'Example Domain' and the first &lt;h1&gt; element text is also 'Example Domain'"
- ...but couldn't formalize it as JSON output within the remaining step + token budget

**Honest interpretation**: capability-success, capacity-failure. The frontier model has the instruction-following to solve this, but the free-tier token cap on `gpt-4.1-mini` plus browser-use's heavy DOM-context loading exceed the request budget. Phase 3 will explore: (a) GitHub Models marketplace models with higher free-tier limits, (b) a slimmer agent loop that sends only minimum DOM context.

## Final v1-v5 summary table

| version | model | defenses | elapsed | Judge | attractor target | JSON match | cost |
|---|---|---|---|---|---|---|---|
| v1 | qwen2.5:7b local | Layer 0 | 180s | FAIL | eBay | n/a | ¥0 |
| v2 | qwen2.5:7b local | L1 | 86s | FAIL | (fabrication: ArXiv) | n/a | ¥0 |
| v3 | qwen2.5:7b local | L1+L2 | 94s | FAIL | eBay $50/4-star returns | false | ¥0 |
| v4 | qwen2.5:7b local | L1+L2+L3 | 94s | FAIL | Walmart | false | ¥0 |
| **v5** | **gpt-4.1-mini cloud** | L1+L2+L3+L5 | 68s | FAIL | **NONE** | false (token cap) | **¥0** |

**Constraint compliance**: all 5 runs literal stayed within zero credit card. Cost across the full defense-in-depth journey: **¥0**. Each failure teaches a different lesson:
- v1: agent loops have weak default stopping → rogue navigation
- v2: tight step budgets cause hallucinated fabrication (worse than rogue, harder to detect)
- v3: prompt engineering (schema + few-shot) does NOT suppress strong training-data attractors
- v4: prompt-based Plan-Execute is advisory, not enforcing — executor still ignored the plan
- v5: frontier solves the attractor problem but exposes new constraint (free-tier token cap)

This is the literal portfolio narrative. Phase 3 will tackle the v5 token-cap problem and integrate the cost-tier table into craftstack.

## Memory Bank

`memory_bank/` follows the [Cline Memory Bank pattern](https://docs.cline.bot/getting-started/memory-bank): logbook (append-only events), activeContext (current focus), decisionLog (ADRs), productContext (what/why), systemPatterns (how).

## Drift prevention

This repo treats doc/code drift as a structural failure mode. The `.github/workflows/drift-check.yml` CI runs on every push + PR and fails if claims in this README do not match repo reality (file existence, license header, memory bank file count, phase declaration). Adding a claim to README without backing reality breaks CI.

## License

MIT — see [LICENSE](LICENSE).

## Prior art

- [browser-use/browser-use](https://github.com/browser-use/browser-use) — MIT, core engine
- [ollama/ollama](https://github.com/ollama/ollama) — MIT, local LLM runtime
- [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) — Apache-2.0, LLM weights
