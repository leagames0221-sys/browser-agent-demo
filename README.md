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

Phase 2 next: v3 with Layer 2 (JSON schema constraint + few-shot STOP examples) will test whether structured output gates the fabrication failure.

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
