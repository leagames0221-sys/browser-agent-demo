# Active Context — browser-agent-demo

## Current phase

**Phase 0** — Scaffold install (in progress, completing in this session)

## Current focus

GitHub repo の Phase 0 scaffold install を完遂し、 initial push で drift-check workflow が green になることを実測 verify する。

## Next concrete steps

1. PJ_REGISTRY.yaml (`~/.claude/PJ_REGISTRY.yaml`) に `browser_agent_demo` entry 追加
2. `git add . && git commit -m "Phase 0: scaffold install"` + `git push`
3. `gh run watch` で drift-check workflow が green になるか実測
4. green 確認後、 logbook に Phase 0 完了 entry append
5. Phase 1 着手 (browser-use clone → audit → 自 repo 抽出 → Ollama install → baseline eval)

## Blockers

なし (Phase 0 scope 内)。

## Out of scope (current phase)

- 実 task 実装 (Phase 2)
- gif 生成 (Phase 2)
- craftstack 統合 (Phase 3)
