# browser-agent-demo

> Local-only browser automation agent. Zero API cost, sandboxed Chrome profile.
> Built on [browser-use](https://github.com/browser-use/browser-use) (MIT) + [Ollama](https://ollama.com) (MIT) + Qwen2.5-7B.

[![drift-check](https://github.com/leagames0221-sys/browser-agent-demo/actions/workflows/drift-check.yml/badge.svg)](https://github.com/leagames0221-sys/browser-agent-demo/actions/workflows/drift-check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

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
